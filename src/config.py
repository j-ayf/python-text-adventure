"""Config file with global Stuff and initialization code."""
import json
import logging

import character
import components
import inventory
import locations

log = logging.getLogger(__name__)

CURRENCY = 'Gold Coin'


def welcome(player_name):
    """TODO: Comment function welcome"""
    return f"Welcome to this very simple Text Adventure, {player_name}! Find you way out of the Mansion to finish it!"


def initialize(chosen_player_name):
    """Loads all components from JSON and creates game objects"""
    f = open("init.json", "r")
    f = f.read()
    init_json = json.loads(f)

    for component in init_json:
        if component == 'Item':
            init_items(init_json['Item'])
        elif component == 'Key':
            init_keys(init_json['Key'])
        elif component == 'Door':
            init_doors(init_json['Door'])
        elif component == 'Barrier':
            init_barriers(init_json['Barrier'])
        elif component == 'Location':
            init_locations(init_json['Location'])
        elif component == 'Character':
            init_characters(init_json['Character'])
        elif component == 'Player':
            init_player(init_json['Player'], chosen_player_name)
        elif component == 'Container':
            init_containers(init_json['Container'])
        else:
            log.error(f'MISSING FUNCTION FOR INIT-OBJECT TYPE')

    set_locations(init_json)


def init_items(items):
    """Goes through all items defined in JSON and creates objects from them. Almost the same as 'init_keys', apart
    from the object type being created"""
    for item in items:
        desc = items[item]['description']
        if items[item]['name'] == 'Money':
            name = CURRENCY
        else:
            name = items[item]['name']
        internal_name = item
        price = items[item]['price']
        # Create objects without assigning them to a variable
        components.Item(desc, name, internal_name, price)


def init_keys(keys):
    """Goes through all keys defined in JSON and creates objects from them. Almost the same as 'init_items', apart
    from the object type being created"""
    for key in keys:
        desc = keys[key]['description']
        name = keys[key]['name']
        internal_name = key
        # Create objects without assigning them to a variable
        components.Key(desc, name, internal_name)


def init_doors(doors):
    """Goes through all doors defined in JSON and creates objects from them."""
    for door in doors:
        this_key = None
        if doors[door]['key'] is not None:
            for key in components.Component.get_all_components()['Key']:
                if key.internal_name == doors[door]['key']:
                    this_key = key
        desc = doors[door]['description']
        name = doors[door]['name']
        internal_name = door
        # Create objects without assigning them to a variable
        locations.Door(this_key, desc, name, internal_name)


def init_barriers(barriers):
    """Goes through all barriers defined in JSON and creates objects from them."""
    for barrier in barriers:
        desc = barriers[barrier]['description']
        internal_name = barrier
        # Create objects without assigning them to a variable
        locations.Barrier(desc, internal_name=internal_name)


def init_locations(location_list):
    """Goes through all locations defined in JSON and creates objects from them."""
    # Initialize barrier variables
    north_wall = None
    south_wall = None
    west_wall = None
    east_wall = None
    for location in location_list:
        # Check which barrier is the correct one defined in the JSON. Checks existing barriers' internal_name.
        for barrier in locations.Barrier.get_all_barriers():
            if barrier.internal_name == location_list[location]['north_wall']:
                north_wall = barrier
            if barrier.internal_name == location_list[location]['south_wall']:
                south_wall = barrier
            if barrier.internal_name == location_list[location]['west_wall']:
                west_wall = barrier
            if barrier.internal_name == location_list[location]['east_wall']:
                east_wall = barrier
        desc = location_list[location]['description']
        inv_desc = location_list[location]['inv_description']
        name = location_list[location]['name']
        internal_name = location
        # Create objects without assigning them to a variable
        new_location = locations.Location(north_wall, south_wall, west_wall, east_wall, desc, name, internal_name,
                                          inv_desc)

        fill_inventory(new_location.inventory, 'Item', location_list, location)
        fill_inventory(new_location.inventory, 'Key', location_list, location)


def init_characters(characters):
    """Goes through all characters defined in JSON and creates objects from them. Almost the same as 'init_player',
    apart from the object type being created"""
    for char in characters:
        desc = characters[char]['description']
        name = characters[char]['name']
        text = characters[char]['text']
        internal_name = char

        new_character = character.Character(desc, name, internal_name, text=text)

        fill_inventory(new_character, 'Item', characters, char)
        fill_inventory(new_character, 'Key', characters, char)


def init_player(players, chosen_player_name):
    """Goes through all characters defined in JSON and creates objects from them. Almost the same as 'init_player',
    apart from the object type being created"""
    # for-loop will only be run once because there is only one player, but who knows what happens in the future.
    for char in players:
        desc = players[char]['description']
        name = chosen_player_name
        # Optional: money can be specified as its own item and added to inventory or specifically for player
        #   initialization.
        money = int(players[char]['money'])
        internal_name = char

        new_player = character.Player(desc, name, internal_name, money=money)

        fill_inventory(new_player, 'Item', players, char)
        fill_inventory(new_player, 'Key', players, char)


def init_containers(containers):
    """Goes through all barriers defined in JSON and creates objects from them."""
    for container in containers:
        this_key = None
        for key in components.Component.get_all_components()['Key']:
            if key.internal_name == containers[container]['key']:
                this_key = key
        desc = containers[container]['description']
        name = containers[container]['name']
        internal_name = container

        new_container = inventory.Container(this_key, desc, name, internal_name)
        fill_inventory(new_container, 'Item', containers, container)
        fill_inventory(new_container, 'Key', containers, container)


def fill_inventory(inventory_obj, item_type: str, json_segment, inv_str):
    """Fills inventory with all items specified in JSON. 'inventory_obj' can also be a character because they share the
    same methods. 'item_type' parameter to distinguish between regular items and sub-items like keys. 'json_segment'
    is the characters (plural) json segment and 'inv_str' is the string of the specific character that gets their
    inventory filled."""
    for target_item in json_segment[inv_str]['inventory']:
        amount = 1
        # check if an amount has been given in json in format "item_name(amount)"
        if '(' in target_item:
            index = target_item.index('(')
            amount = int(target_item[index+1:-1])
            target_item = target_item[0:index]
        for actual_item in components.Component.get_all_components()[item_type]:
            if actual_item.internal_name == target_item:
                # add item to inventory as many times as specified. Default is 1
                for i in range(amount):
                    inventory_obj.add_item(actual_item)


def set_locations(init_json):
    """Sets locations to the objects as defined in JSON by looping through existing objects and checking corresponding
    fields in JSON"""
    # loop through component types in '_all_components' list in components.py
    for component_type in components.Component.get_all_components():
        # Items and Keys don't have a location
        if component_type == 'Item' or component_type == 'Key':
            continue
        # loop through components of component type
        for component in components.Component.get_all_components()[component_type]:
            # setting variable to make code more readable. Contains the path to the location internal_name field in
            #  JSON of the particular component
            loc_json = init_json[component_type][component.internal_name]['location']

            # checks if a locations should be set or JSON field is set to "None"
            if loc_json != 'None':
                # loops through existing locations
                for location in locations.Location.get_all_locations():
                    # checks if current location in loop is the one defined in JSON and if so, sets it on component.
                    if location.internal_name == loc_json:
                        component.location = location


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s -- %(module)s -- %(message)s')
    initialize('Janik')
