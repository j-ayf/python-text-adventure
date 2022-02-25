from commands import Command
import config
import logging
import time

log = logging.getLogger(__name__)


def start_text_adventure():
    log.debug('Game function started.')
    time.sleep(0.1)
    player_name = input('Enter your Name: ')
    config.initialize(player_name)
    log.warning(f'Welcome Message')

    # Game Loop
    while True:
        time.sleep(0.1)  # Needed to make sure the Enter Command message is shown after log messages.
        command = enter_command()
        command.analyze()


def enter_command():
    """Returns the command object"""
    try:
        command = Command(input('Enter Command: '))
        return command
    except KeyboardInterrupt:
        exit('Game stopped by Keyboard Interrupt')


if __name__ == '__main__':
    # used for dev
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s -- %(module)s -- %(message)s')
    # used for playing as messages to the Player
    # logging.basicConfig(level=logging.INFO, format='%(message)s')
    start_text_adventure()
