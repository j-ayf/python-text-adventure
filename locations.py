import logging
from base import Base

log = logging.getLogger(__name__)


class Barrier(Base):
    # Class variable that contains all barriers in a list for easy referencing
    _all_barriers = []

    def __init__(self, description=None, name=None, internal_name=None):
        super().__init__(description, name, internal_name)

        Barrier._all_barriers.append(self)

    @classmethod
    def get_all_barriers(cls):
        """Returns list with all Barriers in the game."""
        return cls._all_barriers


class Lock:

    def __init__(self, key=None):
        """Constructor for Lock. Initialize with the Key-Item needed to unlock."""
        from components import Key
        if key is not None:
            assert isinstance(key, Key)

        self.key = key

        if key is None:
            self.is_unlocked = True
        else:
            self.is_unlocked = False

    @property
    def is_unlocked(self):
        """Returns locked state of the lock"""
        return self._is_unlocked

    @is_unlocked.setter
    def is_unlocked(self, unlocked_bool):
        """TODO: Comment function is_unlocked"""
        self._is_unlocked = unlocked_bool

    def unlock(self, key):
        """Attempts to unlock a lock with a specific key."""
        from components import Key
        assert isinstance(key, Key)

        if self.is_unlocked:
            log.info(f'{type(self).__name__} is already unlocked')
        else:
            # Check if the correct key is being used
            if self.key is key:
                self.is_unlocked = True
                log.info(f'{type(self).__name__} has been unlocked.')
            else:
                log.warning(f'Wrong Key. {type(self).__name__} stays locked.')


class Door(Barrier):

    def __init__(self, key=None, description=None, name=None, internal_name=None):
        """Constructor for Door(Barrier). Initialize with the Key-Item needed to unlock."""
        Barrier.__init__(self, description, name, internal_name)
        self.lock = Lock(key)

    def is_unlocked(self):
        """Returns locked state of the lock"""
        return self.lock.is_unlocked

    def unlock(self, key):
        """Simply forwards to the 'Lock' class' method of the same name. Takes a key as parameter."""
        log.debug('Attempting to unlock door.')
        self.lock.unlock(key)


class Location(Base):
    # Class variable that contains all locations in a list. It is used to determine which location is adjacent to the
    # current one, when a character goes through a door to provide the correct new location.
    _all_locations = []

    def __init__(self, north_wall: Barrier, south_wall: Barrier, west_wall: Barrier, east_wall: Barrier,
                 description=None, name=None, internal_name=None):
        super().__init__(description, name, internal_name)
        assert isinstance(north_wall, Barrier)  # if one is a Barrier, the others should be, too #goodEnough
        self.north_wall = north_wall
        self.south_wall = south_wall
        self.west_wall = west_wall
        self.east_wall = east_wall

        Location._all_locations.append(self)

    def get_adjacent_location(self, wall_in_direction) -> 'Location':
        """Goes through the cls list-variable with all locations and checks which of those shares the passed
        wall-parameter on its 'opposite' side."""

        for loc in Location._all_locations:
            if wall_in_direction == self.north_wall:
                if wall_in_direction == loc.south_wall:
                    return loc
            elif wall_in_direction == self.south_wall:
                if wall_in_direction == loc.north_wall:
                    return loc
            elif wall_in_direction == self.west_wall:
                if wall_in_direction == loc.east_wall:
                    return loc
            else:
                if wall_in_direction == loc.west_wall:
                    return loc

        log.error('No location found!')

    @classmethod
    def get_all_locations(cls):
        """Returns list with all Locations in the game."""
        return cls._all_locations
