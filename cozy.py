import sys
import pygame
import data.game
pygame.init()


def main():
    """
    This is where the whole shabang starts! Even though not much actually happens here.
    """
    gameclass = data.game.GameClass()
    gameclass.main_loop()


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
