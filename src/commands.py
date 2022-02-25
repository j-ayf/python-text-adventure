import logging
import re

import components
import config
import inventory
import locations
import time

log = logging.getLogger(__name__)


class Command:

    def __init__(self, command: str):
        """Constructor for Command. Strips special characters and extra spaces. Then creates a list of single words."""
        self.command_list = command

    @property
    def command_list(self):
        """Returns a list of words of the command"""
        return self._command_list

    @command_list.setter
    def command_list(self, command):
        """Strips special characters from what the player typed and puts individual words into a list"""
        command = command.lower()
        # Using Regex to strip everything but numbers and letters from the command
        command = re.sub('[^a-z0-9 ]', '', command)
        self._command_list = command.split(' ')
        # remove empty indexes
        while '' in self.command_list:
            self._command_list.remove('')

    def analyze(self):
        """Check the words given by player and executes appropriate functions"""
        # There's only one player so the object can be directly accessed.
        player = components.Component.get_all_components()['Player'][0]

        # necessary to prevent index out of bound errors when only giving one word as command
        if len(self.command_list) < 2 and not ('exit' == self.command_list[0] or 'stop' == self.command_list[0]):
            log.error(f'Commands need to have at least 2 words!')
            return

        if 'show' == self.command_list[0] and 'inventory' == self.command_list[1]:
            player.show_inventory()
        elif 'look' == self.command_list[0] and 'around' == self.command_list[1]:
            log.warning(f'You are in a {player.location.name}. {player.location.description}')
        elif 'look' == self.command_list[0] and 'at' == self.command_list[1]:
            self.look(player)
        elif 'look' == self.command_list[0] and ('north' == self.command_list[1] or 'south' == self.command_list[1] or
                                                 'west' == self.command_list[1] or 'east' == self.command_list[1]):
            self.look_cardinal(player)
        elif 'look' == self.command_list[0] and 'in' == self.command_list[1] or 'open' == self.command_list[0]:
            self.open(player)
        elif 'go' == self.command_list[0]:
            self.go(player)
        elif 'unlock' == self.command_list[0]:
            self.unlock(player)
        elif 'take' == self.command_list[0]:
            self.take(player)
        elif 'talk' == self.command_list[0] and 'to' == self.command_list[1]:
            self.talk(player)
        elif 'buy' == self.command_list[0]:
            self.buy(player)
        elif 'exit' == self.command_list[0] or 'stop' == self.command_list[0]:
            exit('Game stopped by Player')
        else:
            log.error('This game is too stupid to understand what you mean :(')

    def look(self, player):
        """Look at components or doors"""
        obj_to_look_at_name = self.get_obj_name(2, len(self.command_list))
        # retrieve item object
        obj_to_look_at = self.get_obj_from_name(obj_to_look_at_name)
        # Checks if object is in the same location as the player and outputs description.
        try:
            if self.is_correct_location(obj_to_look_at, player.location):
                log.debug('Component found at current location!')
                log.warning(obj_to_look_at.description)
            elif player.location.inventory.is_item_in_inventory(obj_to_look_at):
                log.debug('Component found at current location!')
                log.warning(obj_to_look_at.description)
            else:
                log.warning(f'There is no {obj_to_look_at.name} here.')
        # if obj_to_look_at is None
        except AttributeError:
            log.error('No such thing here.')

    def look_cardinal(self, player):
        """Look in cardinal direction and output Barrier's description"""
        direction = self.command_list[1]
        if direction == 'north':
            log.warning(f'{player.location.north_wall.description}')
        elif direction == 'south':
            log.warning(f'{player.location.south_wall.description}')
        elif direction == 'west':
            log.warning(f'{player.location.west_wall.description}')
        elif direction == 'east':
            log.warning(f'{player.location.east_wall.description}')

    def open(self, player):
        """Shows Container's inventory and opens doors. Opening doors ist just cosmetic, doesn't need to be done."""
        if 'open' == self.command_list[0]:
            obj_to_open_name = self.get_obj_name(1, len(self.command_list))
        else:
            obj_to_open_name = self.get_obj_name(2, len(self.command_list))
        obj_to_open = self.get_obj_from_name(obj_to_open_name)
        try:
            # check for correct location
            obj_is_in_location = self.is_correct_location(obj_to_open, player.location)
            assert obj_is_in_location
            # if object is container, check if it is unlocked and open it
            if isinstance(obj_to_open, inventory.Container):
                if obj_to_open.lock.is_unlocked:
                    obj_to_open.show_inventory()
                else:
                    log.warning('You need to unlock this before you can open it!')
            # if object is not a container it must be a door, so try to open that
            elif isinstance(obj_to_open, locations.Door):
                if obj_to_open.lock.is_unlocked:
                    log.warning(f'You open {obj_to_open.name}. you can go through now.')
                else:
                    log.warning(f'You need to unlock this first!')
            # This else clause should never be executed
            else:
                log.error(f'If you see this something is very weird. Ask Developer about "look at/open" function')
                raise AttributeError
        except AttributeError:
            log.warning('No such thing exists to be be opened!')
        except AssertionError:
            log.warning(f'You need to be in the same location as the object you want to open')

    def go(self, player):
        """Go in cardinal direction."""
        direction = self.command_list[1]
        player.go_direction(direction)
        log.warning(f'You are in a {player.location.name}. {player.location.description}')

    def unlock(self, player):
        """Unlock doors and containers"""
        if len(self.command_list) < 2:
            log.warning(f'Unlock what?')
            return
        # determine what object the player wants to unlock
        obj_to_unlock_name = self.get_obj_name(1, len(self.command_list))
        # get actual object
        obj_to_unlock = self.get_obj_from_name(obj_to_unlock_name, 'Container')
        if obj_to_unlock is None:
            obj_to_unlock = self.get_obj_from_name(obj_to_unlock_name, 'Door')
        if obj_to_unlock is None:
            log.error(f'"{obj_to_unlock_name.capitalize()}" is not something that can be unlocked!')
            return
        # check if the object is in the same location as the player when it is a container
        is_in_location = self.is_correct_location(obj_to_unlock, player.location)
        if is_in_location:
            try:
                # checks if key is in player's inventory
                if player.is_item_in_inventory(obj_to_unlock.lock.key):
                    obj_to_unlock.unlock(obj_to_unlock.lock.key)
                else:
                    log.warning(f'You are missing the correct key to unlock this!')
            # if obj_to_unlock is None
            except AttributeError:
                log.warning('Nothing with that name exists.')
        else:
            log.warning('You need to be in the same location to unlock this!')

    def take(self, player):
        """Take items out of a container or directly from a location"""
        # take stuff from container
        if 'from' in self.command_list:
            index_from = self.command_list.index('from')
            obj_to_take_name = self.get_obj_name(1, index_from)
            # retrieve item object
            obj_to_take = self.get_obj_from_name(obj_to_take_name)
            # get inventory name given by player
            inv_to_take_from_name = self.get_obj_name(index_from + 1, len(self.command_list))
            # get actual container(inventory) object from name provided by player
            inv_to_take_from = self.get_obj_from_name(inv_to_take_from_name, 'Container')
            # check if container is in player's location
            try:
                if self.is_correct_location(inv_to_take_from, player.location):
                    # check if container is unlocked, otherwise raise warning to player
                    if inv_to_take_from.lock.is_unlocked:
                        # check if item is in container's inventory
                        if inv_to_take_from.is_item_in_inventory(obj_to_take):
                            # do actual adding and removing of the item
                            player.add_item(obj_to_take)
                            inv_to_take_from.remove_item(obj_to_take)
                            log.warning(f'{obj_to_take.name} added to inventory.')
                        else:
                            log.warning(f'Nothing with that name can be taken from {inv_to_take_from.name}.')
                    else:
                        log.warning(f'{inv_to_take_from.name} is locked!')
                else:
                    log.warning(f'You need to be in the same location as {inv_to_take_from.name} to take from it!')
            except AttributeError:
                log.warning(f'This container does not exist')
        # take stuff directly in location
        else:
            # get object name given by player
            obj_to_take_name = self.get_obj_name(1, len(self.command_list))
            # retrieve item object
            obj_to_take = self.get_obj_from_name(obj_to_take_name)
            # check if object's location is player's location
            correct_location = False
            try:
                # go through items in locations 'inventory'
                for item_w_amount in player.location.inventory.inventory_list:
                    if item_w_amount[0] == obj_to_take:
                        correct_location = True
                # check for correct location
                if correct_location:
                    # add to player's inventory
                    player.add_item(obj_to_take)
                    # remove from location
                    player.location.inventory.remove_item(obj_to_take)
                    log.warning(f'{obj_to_take.name} added to inventory.')
                else:
                    log.warning(f'Nothing with that name can be taken from {player.location.name}.')
            # message if object could not be found in location or container
            except AttributeError:
                log.warning(f'Nothing with that name can be taken from this location.')

    def talk(self, player):
        """Talk to an NPC merchant and show their inventory to the player."""
        # get character object to talk to
        char_to_talk_name = self.get_obj_name(2, len(self.command_list))
        char_to_talk = self.get_obj_from_name(char_to_talk_name, 'Character')
        try:
            # check location
            if self.is_correct_location(char_to_talk, player.location):
                # show character 'voice lines' to player
                log.warning(f'{char_to_talk.text}')
                time.sleep(0.1)
                # show character's inventory with the prices
                char_to_talk.show_inventory(True)
            else:
                log.warning(f'You need to be in the same location as {char_to_talk.name} to talk to him!')
        except AttributeError:
            log.error(f'"{char_to_talk_name.capitalize()}" is not a valid Character name.')

    def buy(self, player):
        """Buy given item from the character in player's location. Only works with one merchant per location!"""
        obj_to_buy_name = self.get_obj_name(1, len(self.command_list))
        obj_to_buy = self.get_obj_from_name(obj_to_buy_name)
        try:
            for character in components.Component.get_all_components()['Character']:
                if self.is_correct_location(character, player.location):
                    if character.is_item_in_inventory(obj_to_buy):
                        # Checks if player has enough money, then removes the amount of money and switches item to
                        #   new inventory.
                        if player.has_enough_money(obj_to_buy.price):
                            player.money -= obj_to_buy.price
                            player.add_item(obj_to_buy)
                            character.remove_item(obj_to_buy)
                            log.warning(f'{obj_to_buy.name} added to inventory')
                        else:
                            log.warning(f'You don\'t have enough money to buy "{obj_to_buy.name}" for '
                                        f'{obj_to_buy.price} {config.CURRENCY}!')
                    else:
                        log.warning(f'{character.name} does not have "{obj_to_buy.name}" for sale!')
                return
            log.warning(f'There is no merchant here to buy this from!')
        except AttributeError:
            log.error(f'"{obj_to_buy_name.capitalize()}" is not a valid Item name!')

    def get_obj_name(self, range_start: int, range_end: int):
        """Goes through command_list. Takes start and end indexes as command and returns String from those words"""
        obj_name = ''
        for i in range(range_start, range_end):
            obj_name += f'{self.command_list[i]} '
        # make lower case and remove trailing space
        return obj_name.rstrip().lower()

    @staticmethod
    def get_obj_from_name(obj_name: str, component_type: str = None):
        """Returns component object by looking for its name. If no component type is given, it loops through all."""
        obj_name = obj_name.lower()
        # go through all existing components and doors
        if component_type is None:
            for c_type in components.Component.get_all_components():
                for obj in components.Component.get_all_components()[c_type]:
                    if obj.name.lower() == obj_name:
                        return obj
            for door in locations.Barrier.get_all_barriers():
                if door.name.lower() == obj_name:
                    return door
        # look for Barriers (doors)
        elif component_type == 'Barrier' or component_type == 'Door':
            for door in locations.Barrier.get_all_barriers():
                if door.name.lower() == obj_name:
                    return door
        # only look in given component type
        else:
            for obj in components.Component.get_all_components()[component_type]:
                if obj.name.lower() == obj_name:
                    return obj
        return None

    @staticmethod
    def is_correct_location(obj_to_check, location: locations.Location) -> bool:
        """Takes an object (component or door) and a location. Then checks if the object is in that location and
        returns boolean result."""
        try:
            if isinstance(obj_to_check, components.Component):
                assert obj_to_check.location == location
            elif isinstance(obj_to_check, locations.Door):
                assert location.north_wall == obj_to_check or location.south_wall == obj_to_check or \
                       location.west_wall == obj_to_check or location.east_wall == obj_to_check
            else:
                raise AttributeError(f'"{obj_to_check}" not a valid object to check its location!')
            log.debug(f'Correct location for {obj_to_check.internal_name} confirmed.')
            return True
        except AssertionError:
            return False
