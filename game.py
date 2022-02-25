from commands import Command
import config
import logging
import time

log = logging.getLogger(__name__)


def start_text_adventure():
    log.debug('Game function started.')
    config.initialize('Janik')
    log.warning(f'Welcome Message')

    # Game Loop
    while True:
        time.sleep(0.1)
        command = enter_command()
        command.analyze()


def enter_command():
    """TODO: Currently returns the list of words within the command"""
    try:
        command = Command(input('Enter Command: '))
        return command
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    # used for dev
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s -- %(module)s -- %(message)s')
    # used for playing as messages to the Player
    # logging.basicConfig(level=logging.INFO, format='%(message)s')
    start_text_adventure()
