from components import Item, Component
from locations import Lock
import config
import logging

log = logging.getLogger(__name__)


class Inventory:

    def __init__(self):
        """Constructor for Inventory. Inventory list contains lists of length 2, each with an Item Object and the
        stored amount."""
        self.inventory_list = []

    @property
    def inventory_list(self) -> list:
        """Returns the Inventory Object's Inventory list with dictionaries."""
        return self._inventory

    @inventory_list.setter
    def inventory_list(self, inventory):
        """Initializes new empty list on object creation."""
        self._inventory = inventory

    def show_inventory(self, needs_price=False, component=None):
        """Returns an inventory as readable String. Takes Boolean as argument if Price should be added."""
        # Get the list from the Inventory object
        if len(self.inventory_list) > 0:
            # Create the String to be returned
            print(self.__build_inv_string(self.inventory_list, needs_price, component))
        else:
            print(f'{component.name}\'s inventory is empty :(')

    def add_item(self, item_obj: Item, amount=1):
        """Adds an item to the Inventory or increases an existing item's counter. Takes Item-Object and Amount as
        Integer as arguments."""
        is_in_inventory = False
        # go through the inventory list and look at the individual dictionaries
        for existing_item in self.inventory_list:
            if existing_item[0].internal_name == item_obj.internal_name:
                pass
            if existing_item[0].internal_name == item_obj.internal_name:
                is_in_inventory = True
                existing_item[1] += amount
                log.debug(f'{item_obj.internal_name} is already in inventory. '
                          f'Increasing counter to {existing_item[1]}.')

        if not is_in_inventory and amount > 0:
            # Inserting new item at the position determined by "__sort_inventory" method
            new_item_w_amount = [item_obj, amount]
            index = self.__sort_inventory(self.inventory_list, item_obj.internal_name)
            self.inventory_list.insert(index, new_item_w_amount)
            log.debug(f'Added {item_obj.internal_name} to inventory.')
        elif amount <= 0:
            log.error(f'Cannot add less than 1 {item_obj.internal_name}')
            Inventory.error_inventory(f'Cannot add less than 1 {item_obj.internal_name}')

    def remove_item(self, item_obj: Item, amount=1):
        """Reduces an Inventory item's amount by specified amount, or removes it completely when exact amount exists.
        If too many items are to be removed, an Error is shown to the User. Takes Item-Object and Amount as Integer
        as arguments."""
        # this list will contain the integer index that needs to be removed from _inventory
        index_to_remove = []
        item_names = []
        for i in range(len(self.inventory_list)):
            item_w_amount = self.inventory_list[i]
            item_names.append(self.inventory_list[i][0].internal_name)
            if item_w_amount[0].internal_name == item_obj.internal_name:
                # Check if inventory contains enough items to remove, otherwise print error to user and break out.
                if item_w_amount[1] - amount < 0:
                    Inventory.error_inventory(f'Not enough {item_w_amount[0].internal_name} available!\n')
                    log.info(f'Not enough {item_w_amount[0].internal_name} ro remove {amount}! Only '
                             f'{item_w_amount[1]} available.')
                    break
                # If inventory contains exact amount of items, add item to local list to be removed from inventory
                if item_w_amount[1] - amount < 1:
                    log.debug(f'{item_w_amount[0].internal_name} marked for removal from inventory.')
                    # Mark item for removal. Don't remove here or missing Index error might appear for following items
                    index_to_remove.append(i)
                # Remove the specified amount from inventory
                else:
                    item_w_amount[1] -= amount
                    log.debug(f'Reducing counter of {item_w_amount[0].internal_name} by {amount} to '
                              f'{item_w_amount[1]}.')

        if item_names.count(item_obj.internal_name) < 1:
            log.error(f'Cannot remove {item_obj.internal_name} from inventory, it does not exist.')

        # Remove items that were marked for removal
        if len(index_to_remove) > 0:
            for i in index_to_remove:
                log.debug(f'Removing {self.inventory_list[i][0].internal_name} from inventory.')
                self.inventory_list.pop(i)

    def __build_inv_string(self, inv_list, needs_price, component) -> str:
        """Create the String, that shows the stored items to the Player. Takes Inventory's List-variable and Boolean
        for the price as arguments."""
        inventory_string = f'{component.name}\'s inventory:\n'
        amount_str_length = 1
        for inv in inv_list:
            if len(str(inv[1])) > amount_str_length:
                amount_str_length = len(str(inv[1]))
        for i in range(len(inv_list)):
            # Calculate number of blanks to be added at beginning of each line to make it look nice
            blanks = ' ' * (len(str(len(inv_list))) - len(str(i+1)))
            # Calculate number of blanks to be added before "Amount" to make it look nice
            blanks2 = ' ' * (amount_str_length - len(str(inv_list[i][1])))
            # Create new line for each item
            line = ''
            line += f'{blanks}{i + 1}) {blanks2}{inv_list[i][1]}x {inv_list[i][0].name}'
            # Add price after a few blank spaces
            if needs_price:
                line = self.__add_price_str(line, inv_list[i])
            # Add new Line at the end
            inventory_string += f'{line}\n'
        return inventory_string

    @staticmethod
    def __add_price_str(line, item_w_amount) -> str:
        """Adds the price to each item in the inventory-return-String. Takes the String of a prepared line and one
        component of the Inventory's List-variable (which is also a list) as arguments."""
        # Length defined to align prices neatly underneath each other
        length = 25 - len(str(item_w_amount[0].price))
        while len(line) < length:
            # Adding required amount of blank spaces, afterwards adding actual price
            line += '_'
        line += f'{item_w_amount[0].price} {config.CURRENCY}/piece'
        return line

    @staticmethod
    def __sort_inventory(inventory, new_item_name) -> int:
        """Returns the inventory index where a new item should be inserted for alphabetical order. Takes Inventory's
        List-variable and the name of a new Item as arguments."""
        names = [new_item_name]
        for item_w_amount in inventory:
            names.append(item_w_amount[0].internal_name)
        names.sort()
        # log.debug(f'Inventory sorted after insert of {new_item_name}')
        return names.index(new_item_name)

    @staticmethod
    def error_inventory(message):
        """Prints an error message to the player"""
        print(message)

    def is_item_in_inventory(self, item) -> bool:
        """Go through items in inventory. Can't check directly because inventory is a 2-dimensional list"""
        for item_plus_amount in self.inventory_list:
            if item in item_plus_amount:
                return True
        return False


class Container(Inventory, Component):

    def __init__(self, key=None, description=None, name=None, internal_name=None, location=None):
        """Create a new Container with the needed key to unlock it"""
        Inventory.__init__(self)
        Component.__init__(self, description, name, internal_name, location)
        self.lock = Lock(key)

    def unlock(self, key):
        """Simply forwards to the 'Lock' class' method of the same name. Takes a key as parameter."""
        log.debug('Attempting to unlock Container.')
        self.lock.unlock(key)
    
    def show_inventory(self, needs_price=False, component=None):
        """Sets container as the component for name-calling, then calls parent class's method."""
        component = self
        super(Container, self).show_inventory(needs_price, component)
