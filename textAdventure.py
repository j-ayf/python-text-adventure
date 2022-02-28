import src.game
import logging

log = logging.getLogger(__name__)


def main():
    src.game.start_text_adventure()


if __name__ == '__main__':
    # used for playing as messages to the Player
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    main()
