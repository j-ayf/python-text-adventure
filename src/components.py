import logging
from .base import Base
from .locations import Location

log = logging.getLogger(__name__)


class Component(Base):
    _all_components = {
        'Item': [],
        'Key': [],
        'Character': [],
        'Player': [],
        'Container': []
    }

    def __init__(self, description=None, name=None, internal_name=None, location=None):
        """Constructor for Component"""
        super().__init__(description, name, internal_name)
        self.location = location
        Component._all_components.get(type(self).__name__).append(self)

    @property
    def location(self) -> Location:
        """Returns the current location"""
        return self._location

    @location.setter
    def location(self, new_location: Location):
        """Sets new location"""
        self._location = new_location
        if new_location is None:
            log.debug(f'No location for {self.internal_name} has been set')
        else:
            log.debug(f'New location for {self.internal_name} has been set')

    @classmethod
    def get_all_components(cls):
        """Returns list with all Locations in the game."""
        return cls._all_components


class Item(Component):

    def __init__(self, description=None, name=None, internal_name=None, price: int = 1, location=None):
        """Constructor for Item(Component)"""
        super().__init__(description, name, internal_name, location)
        self.price = price

    @property
    def price(self) -> int:
        """Returns the item's price"""
        return self._price

    @price.setter
    def price(self, price: int):
        """Sets item's new price"""
        self._price = int(price)


class Key(Item):
    pass
