"""
GameClass contains instances of all relevant modules, which can be accessed and modified from the modules
themselves. GameClass is like a library for data, that can be shared across all the game files.
"""

import pygame
import data.camera
import data.fetch
import data.world
import data.player
import data.water
import data.updates
import data.objects
import data.collision
import data.actions


class GameClass:

    def __init__(self):
        self.camera = data.camera.Camera(self)
        self.fetch = data.fetch.Fetch(self)
        self.world = data.world.WorldChange(self)
        self.player = data.player.Player(self)
        self.water = data.water.Water(self)
        self.updates = data.updates.Updates(self)
        self.objects = data.objects
        self.collision = data.collision.Collision(self)
        self.actions = data.actions.Actions(self)

        self.clock = pygame.time.Clock()
        self.tick = 0
        self.loop = True

    def main_loop(self):
        """
        This function contains the main loop of the game, as well as the startup procedures that only happens once,
        like the reset_map function that looks for a suitable starting tile.
        """
        self.world.reset_map()

        while self.loop:
            self.updates.check_all()
            self.camera.print_screen()

            self.tick += 1
            if self.tick == 60:
                self.tick = 0
                self.water.water_flow()

            self.clock.tick(60)
            pygame.display.flip()
