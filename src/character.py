from . import config
from . import inventory
from .components import Component, Item
from .locations import Door
import logging

log = logging.getLogger(__name__)


class Character(Component):

    def __init__(self, description=None, name=None, internal_name=None, location=None, text=None):
        """Constructor for NPC"""
        super().__init__(description, name, internal_name, location)
        self.inventory = inventory.Inventory()
        self.text = text

    @property
    def inventory(self):
        """Returns character's inventory as inventory object."""
        return self._inventory

    @inventory.setter
    def inventory(self, new_inventory):
        """Sets character's inventory as new inventory object during initialization."""
        self._inventory = new_inventory

    @property
    def text(self):
        """Returns 'Voice Line' of the character"""
        return self._text

    @text.setter
    def text(self, new_text):
        """Sets new 'Voice Line' of the character"""
        self._text = new_text

    def show_inventory(self, needs_price=False):
        """This method simply returns the result of the Inventory object's method of the same name."""
        self._inventory.show_inventory(needs_price, self)

    def add_item(self, item_obj: Item, amount=1):
        """This method simply forwards to the Inventory object's method of the same name. Takes Item object and amount
        integer as parameters."""
        log.debug(f'Item({item_obj.internal_name}) about to be added to inventory of {self.internal_name}')
        self._inventory.add_item(item_obj, amount)

    def remove_item(self, item_obj: Item, amount=1):
        """This method simply forwards to the Inventory object's method of the same name. Takes Item object and amount
        integer as parameters."""
        log.debug(f'Item({item_obj.internal_name}) about to be removed from inventory of {self.internal_name}')
        self._inventory.remove_item(item_obj, amount)

    def is_item_in_inventory(self, item) -> bool:
        """This method simply forwards to the Inventory object's method of the same name. Takes Item object as
        parameter. Returns True or False."""
        return self.inventory.is_item_in_inventory(item)


class Player(Character):

    def __init__(self, description=None, name=None, internal_name=None, location=None, money: int = 0):
        super().__init__(description, name, internal_name, location)
        self.money = money

    @property
    def money(self):
        """Returns player's money-amount"""
        return self._money

    @money.setter
    def money(self, money):
        """Sets new money amount"""
        self._money = int(money)
    
    def has_enough_money(self, cost) -> bool:
        """Checks if the player has enough money to make a purchase"""
        new_amount = self.money - cost
        if new_amount < 0:
            return False
        return True

    def go_direction(self, direction):
        """Takes direction as parameter, checks if you can go that direction and then goes there."""
        # Setting local variable as the Barrier that you attempt to go through depending on direction.
        if direction == 'north':
            wall_in_direction = self.location.north_wall
        elif direction == 'south':
            wall_in_direction = self.location.south_wall
        elif direction == 'west':
            wall_in_direction = self.location.west_wall
        elif direction == 'east':
            wall_in_direction = self.location.east_wall
        else:
            log.warning('This is not a valid direction!')
            wall_in_direction = None

        # checks if the Barrier you want to go through is a Door
        if isinstance(wall_in_direction, Door):
            if wall_in_direction.is_unlocked():
                # Sets the new location that is determined to be adjacent depending on the current location and the
                # Barrier that is shared with the location in the direction you're going.
                log.debug(f'Current Location: {self.location.internal_name}; Going through Door')
                self.location = self.location.get_adjacent_location(wall_in_direction)
                log.debug(f'New Location: {self.location.internal_name}')
                log.warning(f'You go through {wall_in_direction.name}')
            else:
                log.warning(f"'{wall_in_direction.name}' is locked.")
        elif wall_in_direction is None:
            pass
        else:
            log.warning('You cannot go there!')

    def show_inventory(self, needs_price=False):
        """Prints the current amount of money the player has, then calls super class's method."""
        print(f'Current money: {self.money} {config.CURRENCY}s')
        super(Player, self).show_inventory(needs_price)

    def add_item(self, item_obj: Item, amount=1):
        """This method simply forwards to the Inventory object's method of the same name. Takes Item object and amount
        integer as parameters."""
        log.debug(f'Item({item_obj.internal_name}) about to be added to inventory of {self.internal_name}')
        if item_obj.internal_name == 'money':
            self.money += amount
        else:
            super(Player, self).add_item(item_obj, amount)
