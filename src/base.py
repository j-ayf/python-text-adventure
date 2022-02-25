import logging

log = logging.getLogger(__name__)


class Base:

    def __init__(self, description=None, name=None, internal_name=None):
        """Constructor for Base"""
        self.description = description
        self.name = name
        self.internal_name = internal_name
        log.debug(f'New {type(self).__name__}({self.internal_name}) created.')

    @property
    def description(self) -> str:
        """Returns the description variable of stuff"""
        return self._description

    @description.setter
    def description(self, new_description):
        """Sets new description for stuff"""
        self._description = str(new_description)

    @property
    def name(self) -> str:
        """Returns the name variable of stuff"""
        return self._name

    @name.setter
    def name(self, new_name):
        """Allows setting new name for stuff"""
        if new_name is None:
            self._name = 'unnamed object'
        else:
            self._name = str(new_name)

    @property
    def internal_name(self) -> str:
        """Returns the internal name variable of stuff"""
        return self._internal_name

    @internal_name.setter
    def internal_name(self, new_name):
        """Allows setting new internal name for stuff"""
        if new_name is None:
            new_name = self.name.lower().replace(" ", "_")
            self._internal_name = new_name
        else:
            self._internal_name = str(new_name)

    def __repr__(self):
        """Returns the object's String."""
        return f'Name: {self.name}, Internal Name: {self.internal_name}'
