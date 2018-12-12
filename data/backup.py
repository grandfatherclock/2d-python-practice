"""
This file keeps track of everything world-generation related. Make_map can be called to update one or more tiles.
"""

import random
import pygame
import data.objects as objects
from opensimplex import OpenSimplex
gen = OpenSimplex()


class WorldChange:
    def __init__(self, gameclass):
        self.gc = gameclass
        self.test_world = True
        self.created_tiles = {}
        self.tile_columns = {}
        self.add_object = {}
        self.seedbank = {'sx': None,
                         'sy': None,
                         'sx2': None,
                         'sy2': None,
                         'sx3': None,
                         'sy3': None,
                         'sx_coal1': None,
                         'sy_coal1': None,
                         'sx_coal2': None,
                         'sy_coal2': None,
                         'sx_coal3': None,
                         'sy_coal3': None,
                         'sx_coal4': None,
                         'sy_coal4': None,
                         'sx_coal5': None,
                         'sy_coal5': None,
                         'sx_coal6': None,
                         'sy_coal6': None,
                         'sx_coal7': None,
                         'sy_coal7': None,
                         'sx_coal8': None,
                         'sy_coal8': None,
                         'sx_coal9': None,
                         'sy_coal9': None,
                         'sx_coal10': None,
                         'sy_coal10': None,
                         'sx_gold8': None,
                         'sy_gold8': None,
                         'sx_gold9': None,
                         'sy_gold9': None,
                         'sx_gold10': None,
                         'sy_gold10': None,
                         'sx_copper4': None,
                         'sy_copper4': None,
                         'sx_copper5': None,
                         'sy_copper5': None,
                         'sx_copper6': None,
                         'sy_copper6': None,
                         'sx_copper7': None,
                         'sy_copper7': None,
                         'sx_copper8': None,
                         'sy_copper8': None,
                         'sx_crystal9': None,
                         'sy_crystal9': None,
                         'sx_crystal10': None,
                         'sy_crystal10': None,
                         'sx_silver8': None,
                         'sy_silver8': None,
                         'sx_silver9': None,
                         'sy_silver9': None,
                         'sx_silver10': None,
                         'sy_silver10': None}
        self.first = True
        self.local_update = None
        self.update_list = []
        self.map_update = True
        self.new_tile_made = False
        # Is true if the player has digged out the tile below them
        self.dig = False
        # Used for when looking for a solid tile in a column
        self.found_solid = False
        self.tiles_on_screenx = 20
        # There are more tiles on the Y axis so rendering large trees can't be seen when going downwards
        self.tiles_on_screeny = 24

    def reset_map(self):
        """
        Resets all variables. Keeps looping until a map is created where the player is standing on a clean tile.
        """
        iterationcount = 0

        n = True
        while n:

            self.created_tiles = {}
            self.tile_columns = {}
            self.add_object = {}
            self.first = True

            self.gc.player.realcoords = [0, 0, 1]
            self.gc.player.temporary_coords = [0, 0, 1]
            self.gc.collision.on_stairs = None

            self.gc.camera.top_layer = 1
            self.gc.camera.stairs_entrance = None
            self.gc.camera.status_surface = None
            self.gc.camera.active_map_display = None

            self.make_map()

            iterationcount += 1
            if self.gc.fetch.find_tile('below current').passable and \
               self.gc.fetch.is_tile_clean(self.gc.fetch.find_tile('below current')):
                n = False

        print(iterationcount, "iterations")

    def make_map(self):
        """
        The most important function in the game. Creates and updates the world map.
        """
        player = self.gc.player
        camera = self.gc.camera
        new_display = pygame.Surface((640, 640 + 4*camera.zoom))
        self.new_tile_made = False
        self.map_update = True

        # Xcount = 10 and ycount = 20 means that the update takes place at 10 X, 20 Y
        ycount = 0
        xcount = 0

        # Stops are very important. They stop the xcount and ycount from increasing.
        xcount_stop = False
        ycount_stop = False

        # Movementrange determines the tiles that are to be updated, in real coordinates
        movementrange_x = [player.realcoords[0]-self.tiles_on_screenx // 2,
                           player.realcoords[0] + self.tiles_on_screenx // 2]
        movementrange_y = [player.realcoords[1]-self.tiles_on_screeny // 2,
                           player.realcoords[1] + self.tiles_on_screeny // 2]

        # These variables are only relevant when there's a local update, but they still need to be assigned to something
        local_x = None
        cornerx = None
        square_rad = None

        if self.first:
            # Seedmaking
            self.seedbank['sx'] = random.uniform(0.00000000001, 1.0)*5000
            self.seedbank['sy'] = random.uniform(0.00000000001, 1.0)*5000
            self.seedbank['sx2'] = random.uniform(0.00000000001, 1.0)*5000
            self.seedbank['sy2'] = random.uniform(0.00000000001, 1.0)*5000
            self.seedbank['sx3'] = random.uniform(0.00000000001, 1.0)*5000
            self.seedbank['sy3'] = random.uniform(0.00000000001, 1.0)*5000

            self.seedbank['sx_coal1'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal1'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal2'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal2'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal3'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal3'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal4'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal4'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal5'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal5'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal6'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal6'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal7'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal7'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal8'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal8'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_coal10'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_coal10'] = random.uniform(0.00000000001, 1.0)*1000

            self.seedbank['sx_gold8'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_gold8'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_gold9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_gold9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_gold10'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_gold10'] = random.uniform(0.00000000001, 1.0)*1000

            self.seedbank['sx_copper4'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_copper4'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_copper5'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_copper5'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_copper6'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_copper6'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_copper7'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_copper7'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_copper8'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_copper8'] = random.uniform(0.00000000001, 1.0)*1000

            self.seedbank['sx_crystal9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_crystal9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_crystal10'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_crystal10'] = random.uniform(0.00000000001, 1.0)*1000

            self.seedbank['sx_silver9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_silver9'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sx_silver10'] = random.uniform(0.00000000001, 1.0)*1000
            self.seedbank['sy_silver10'] = random.uniform(0.00000000001, 1.0)*1000

        if player.movement is not None:
            moving_display = camera.active_map_display.copy()

            # Find out what tiles need to be loaded when going in a certain direction, and unload the old ones.
            # There is some weird interactions and +'s and -'s, but it should work as it is here.
            # If some of the objects don't render properly, try to add ycountstop = True to UP and DOWN

            if player.movement == 'up':
                movementrange_y = [player.realcoords[1]-self.tiles_on_screeny//2,
                                   player.realcoords[1]+4-self.tiles_on_screeny//2]
                new_display.blit(moving_display, (0, camera.scale))

            elif player.movement == 'down':
                ycount = self.tiles_on_screeny-1
                movementrange_y = [player.realcoords[1]-1+self.tiles_on_screeny//2,
                                   player.realcoords[1]+self.tiles_on_screeny//2]
                new_display.blit(moving_display, (0, camera.scale*-1))

            elif player.movement == 'left':
                xcount_stop = True
                movementrange_x = [player.realcoords[0]-self.tiles_on_screenx//2,
                                   player.realcoords[0]+1-self.tiles_on_screenx//2]
                new_display.blit(moving_display, (camera.scale, 0))

            elif player.movement == 'right':
                xcount_stop = True
                xcount = self.tiles_on_screenx-1
                movementrange_x = [player.realcoords[0]-1+self.tiles_on_screenx//2,
                                   player.realcoords[0]+self.tiles_on_screenx//2]
                new_display.blit(moving_display, (camera.scale*-1, 0))

        if self.local_update is not None:
            z = self.local_update[3]
            if camera.zoom is not 128:
                # Takes a number as a radius (square_rad) and only updates the tiles in that radius around the player.
                new_display.blit(camera.active_map_display, (0, 0))
                square_rad = self.local_update[0]
                local_x = self.local_update[1]
                local_y = self.local_update[2]

                movementrange_x = [local_x-square_rad, local_x+square_rad+1]
                movementrange_y = [local_y-square_rad, local_y+square_rad+1]
                if self.local_update[4]:
                    self.dig = True

                cornerx = player.realcoords[0] - self.tiles_on_screenx // 2
                cornery = player.realcoords[1] - self.tiles_on_screeny // 2
                xcount = local_x - cornerx - square_rad
                ycount = local_y - cornery - square_rad

            else:
                self.local_update = None

        else:
            # Create tiles and objects (Worldgen)
            self.tile_insertion_loop(movementrange_x, movementrange_y, xcount, ycount, xcount_stop, ycount_stop,
                                      local_x, cornerx, square_rad)

        # Draw the stuff that was created in the Worldgen.

        for y in range(movementrange_y[0], movementrange_y[1]):
            for x in range(movementrange_x[0], movementrange_x[1]):
                self.draw_master(movementrange_x, movementrange_y, xcount, ycount, xcount_stop, ycount_stop, new_display,
                                 local_x, cornerx, square_rad)
                # Control the x's
                if not xcount_stop:
                    xcount += 1

            # Increase Y and reset X
            if not ycount_stop:
                ycount += 1
            if not xcount_stop:
                if self.local_update is None:
                    xcount = 0
                else:
                    xcount = local_x - cornerx - square_rad

        # Draw the player.
        self.player_update(new_display, True)

        # Check if the player moved behind a tile, and if so, draw it.
        if player.movement:
            x, y, z = player.realcoords[0]

            if self.created_tiles[self.gc.fetch.crd_2_str((x, y+1, z))].passable_through is False:
                print('yehaaaaaaa')

            #self.draw_master([x, x+1], [y, y+1], xcount, ycount, xcount_stop, ycount_stop, new_display,
                             #local_x, cornerx, square_rad)

            player.movement = None

        self.local_update = None

        camera.active_map_display = new_display.copy()

    def tile_insertion_loop(self, movementrange_x, movementrange_y, xcount, ycount, xcount_stop, ycount_stop,
                            local_x, cornerx, square_rad):
        """
        Worldgen - Creates all tiles within a certain range, and fills them with objects.
        """

        for y in range(movementrange_y[0], movementrange_y[1]):
            for x in range(movementrange_x[0], movementrange_x[1]):

                # We loop the tile creation until a solid tile is found
                self.found_solid = False
                # TODO: This z overrides the z from local updates
                z = self.gc.camera.top_layer

                while self.found_solid is False:

                    self.tile_insertion(x, y, z)

                    # We subtract 1 from z which increases the depth at which the program searches for a solid tile
                    z -= 1

                # Increase X
                if not xcount_stop:
                    xcount += 1

            # Increase Y and reset X
            if not ycount_stop:
                ycount += 1
            if not xcount_stop:
                if self.local_update is None:
                    xcount = 0
                else:
                    xcount = local_x - cornerx - square_rad

    def tile_insertion(self, x, y, z):
        fetch = self.gc.fetch

        # Create new tiles. Only happens when loading brand new terrain
        if self.created_tiles.get(fetch.crd_2_str((x, y, z))) is None:

            # Indicates that a new tile has been made
            self.new_tile_made = True
            tile = self.tile_calculation(x, y, z)

            # Index the tile
            tile.coords = (x, y, z)
            self.created_tiles[fetch.crd_2_str((x, y, z))] = tile

            # Add non-air tiles to the 2d tile column list (used in drawing to find transparent tiles)
            if tile.name is not 'air':
                self.update_column(x, y, z)
                self.found_solid = True

            # If the tile below this one is already in the system, then stop trying to find a solid

            if self.created_tiles.get(fetch.crd_2_str((x, y, z - 1))) is not None:
                self.found_solid = True

            # Create additional objects that are connected (like leaves on trees)
            # See if this tile has connected objects
            for n in range(5):
                try:
                    for connection in tile.object[n].connected:
                        # See if the connected object's specific tile is in the system
                        if self.created_tiles.get(fetch.crd_2_str((x + connection[1][0],
                                                                   y + connection[1][1], z))) is None:
                            # If it isn't, then add the connected object to a dictionary list that will make
                            # sure to add the connected object when its tile is loaded in the future
                            if self.add_object.get(fetch.crd_2_str((x + connection[1][0],
                                                                    y + connection[1][1], z))) is None:
                                self.add_object[fetch.crd_2_str((x + connection[1][0],
                                                                 y + connection[1][1],
                                                                 z))] = [connection[0]]
                            else:
                                # add the object to a list, if there are multiple items to be drawn
                                self.add_object[fetch.crd_2_str((x + connection[1][0],
                                                                 y + connection[1][1],
                                                                 z))].append(connection[0])
                        else:
                            # If the tile is in the system, just add this connection to that tile's objects
                            self.created_tiles[fetch.crd_2_str((x + connection[1][0],
                                                                y + connection[1][1],
                                                                z))].object[connection[0].layer] =\
                                                                connection[0]
                except (AttributeError, TypeError):
                    continue

            # If the previous action (connected tiles being assigned to non-created tiles) happened to this
            # tile, then add the relevant connections to this tile's objects, and remove the element
            # completely from the add_object library
            if self.add_object.get(fetch.crd_2_str((x, y, z))) is not None:
                for prev_connection in self.add_object[fetch.crd_2_str((x, y, z))]:
                    tile.object[prev_connection.layer] = prev_connection
                self.add_object.pop(fetch.crd_2_str((x, y, z)))

        else:
            self.found_solid = True

    def tile_calculation(self, x, y, z):
        """
        The real worldgen. Takes some coords, makes a tile out of it, and returns the tile. Only makes natural tiles.
        """

        screen_width = self.gc.camera.SCREEN_WIDTH
        screen_height = self.gc.camera.SCREEN_HEIGHT

        if self.test_world is False:

            if z > 0:
                # Create a new tile
                tile = objects.AirTile()

            elif z == 0:
                # Create a new tile
                # Get the correct noise
                nx = x/screen_width * 100
                ny = y/screen_height * 100
                nx2 = x/screen_width * 32
                ny2 = y/screen_height * 32
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                # Generate noisemaps of different scales
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = (((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                            (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                            (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255) - 90

                # Make sure that the big noisemap has a color limit
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Assign tiles and objects based on altitude of noisemap
                if 199 < rand_n3 < 240:
                    tile = objects.GrassTile()
                    tile.color = (0, 200, 0)
                    if random.randint(1, 3) is not 1:
                        tile.object[2] = self.instancer(objects.SpruceBottom())
                    if random.randint(1, 8) == 1:
                        tile.object[1] = self.instancer(objects.DarkTallGrass())

                elif 239 < rand_n3 < 256:
                    tile = objects.GrassTile()
                    tile.color = (0, 150, 0)
                    if random.randint(1, 2) == 1:
                        tile.object[1] = self.instancer(objects.DarkTallGrass())
                    if random.randint(1, 8) is not 1:
                        tile.object[2] = self.instancer(objects.PineBottom())
                    else:
                        if random.randint(1, 3) == 1:
                            tile.object[2] = self.instancer(objects.Rock())

                elif rand_n3 < 200:
                    tile = objects.GrassTile()
                    tile.color = (0, 230, 0)
                    if random.randint(1, 8) == 1:
                        tile.object[1] = self.instancer(objects.TallGrass())
                    if random.randint(1, 30) == 1:
                        self.instancer(objects.SpruceBottom())
                    elif random.randint(1, 50) == 1:
                        tile.object[2] = self.instancer(objects.Rock())
                    elif random.randint(1, 70) == 1:
                        tile.object[2] = self.instancer(objects.BerryBush())
                        tile.object[1] = None

                if rand_n2 < 70 and rand_n3 < 170:
                    tile = objects.SandTile()
                    if random.randint(1, 10) == 1:
                        tile.object[2] = self.instancer(objects.Rock())
                if rand_n3 < 150:
                    tile = objects.SandTile()
                    if random.randint(1, 5) == 1:
                        tile.object[2] = self.instancer(objects.Rock())
                if rand_n3 < 140:
                    tile = objects.WaterTile()
                    tile.color = (0, 0, rand_n3 + 115)

            elif z == -1:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 32
                ny2 = y/screen_height * 32
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal1'], self.seedbank['sy_coal1'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()
                if rand_n2 < 80 and rand_n3 < 180:
                    tile = objects.SandTile()

                if rand_n > 210 and rand_n3 > 150:
                    tile = objects.StoneTile()
                    # Ore check
                    if rand_coal > 200:
                        tile.color = (40, 40, 40)

                if rand_n3 < 140:
                    tile = objects.SandTile()
                if rand_n3 < 120:
                    tile = objects.WaterTile()
                    tile.color = (0, 0, rand_n3 + 40)

            elif z == -2:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 32
                ny2 = y/screen_height * 32
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal2'], self.seedbank['sy_coal2'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()

                if rand_n > 180 and rand_n3 > 130:
                    tile = objects.StoneTile()

                    # Ore check
                    if rand_coal > 200:
                        tile.color = (40, 40, 40)

                if rand_n3 < 110:
                    tile = objects.SandTile()

                if rand_n3 < 90:
                    tile = objects.WaterTile()
                    tile.color = (0, 0, rand_n3 + 50)

            elif z == -3:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 32
                ny2 = y/screen_height * 32
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal3'], self.seedbank['sy_coal3'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()

                if rand_n > 150 and rand_n3 > 120:
                    tile = objects.StoneTile()
                    # Ore check
                    if rand_coal > 220:
                        tile.color = (40, 40, 40)
                    if rand_coal < 40:
                        tile.color = (226, 160, 82)

                if rand_n3 < 85:
                    tile = objects.SandTile()

                if rand_n3 < 50:
                    tile = objects.WaterTile()
                    tile.color = (0, 0, rand_n3 + 50)

            elif z == -4:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 200
                ny2 = y/screen_height * 200
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal4'], self.seedbank['sy_coal4'])) * 255

                copper_1 = x/screen_width * 200
                copper_2 = y/screen_height * 200
                rand_copper = (self.noise(copper_1, copper_2, self.seedbank['sx_copper4'],
                                          self.seedbank['sy_copper4'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()

                if rand_n > 120 and rand_n3 > 110:
                    tile = objects.StoneTile()

                    # coal
                    if rand_coal > 220:
                        tile.color = (40, 40, 40)

                    # iron
                    if rand_coal < 40:
                        tile.color = (226, 160, 82)
                    # copper
                    if rand_copper < 30:
                        tile.color = (255, 137, 29)

                if rand_n3 < 40:
                    tile = objects.SandTile()

                if rand_n3 < 20:
                    tile = objects.WaterTile()
                    tile.color = (0, 0, rand_n3 + 80)

            elif z == -5:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 200
                ny2 = y/screen_height * 200
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal5'], self.seedbank['sy_coal5'])) * 255

                copper_1 = x/screen_width * 200
                copper_2 = y/screen_height * 200
                rand_copper = (self.noise(copper_1, copper_2, self.seedbank['sx_copper5'],
                                          self.seedbank['sy_copper5'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()

                if rand_n > 100 and rand_n3 > 40:
                    tile = objects.StoneTile()
                    # coal
                    if rand_coal > 220:
                        tile.color = (40, 40, 40)
                    # iron
                    if rand_coal < 30:
                        tile.color = (226, 160, 82)
                    # copper
                    if rand_copper < 30:
                        tile.color = (255, 137, 29)

                if rand_n3 < 15:
                    tile = objects.SandTile()

                if rand_n3 < 10:
                    tile = objects.WaterTile()
                    tile.color = (0, 0, rand_n3 + 80)

            elif z == -6:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 200
                ny2 = y/screen_height * 200
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal6'], self.seedbank['sy_coal6'])) * 255

                copper_1 = x/screen_width * 200
                copper_2 = y/screen_height * 200
                rand_copper = (self.noise(copper_1, copper_2, self.seedbank['sx_copper6'],
                                          self.seedbank['sy_copper6'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()

                if rand_n > 70 and rand_n3 > 20:
                    tile = objects.StoneTile()
                    # coal
                    if rand_coal > 220:
                        tile.color = (40, 40, 40)
                    # iron
                    if rand_coal < 35:
                        tile.color = (226, 160, 82)
                    # copper
                    if rand_copper < 30:
                        tile.color = (255, 137, 29)
                    # silver
                    if rand_copper > 230:
                        tile.color = (240, 240, 240)

                if rand_n3 < 8:
                    tile = objects.SandTile()

                if rand_n3 < 5:
                    tile = objects.WaterTile()
                    tile.color = (0, 0, rand_n3 + 80)

            elif z == -7:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 200
                ny2 = y/screen_height * 200
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal7'], self.seedbank['sy_coal7'])) * 255

                copper_1 = x/screen_width * 100
                copper_2 = y/screen_height * 100
                rand_copper = (self.noise(copper_1, copper_2, self.seedbank['sx_copper7'],
                                          self.seedbank['sy_copper7'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()

                if rand_n > 30 and rand_n3 > 10:
                    tile = objects.StoneTile()
                    # coal
                    if rand_coal > 220:
                        tile.color = (40, 40, 40)
                    # iron
                    if rand_coal < 35:
                        tile.color = (226, 160, 82)
                    # copper
                    if rand_copper < 25:
                        tile.color = (255, 137, 29)
                    # silver
                    if rand_copper > 230:
                        tile.color = (240, 240, 240)

                if rand_n3 < 3:
                    tile = objects.SandTile()

            elif z == -8:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 200
                ny2 = y/screen_height * 200
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal8'], self.seedbank['sy_coal8'])) * 255

                copper_1 = x/screen_width * 100
                copper_2 = y/screen_height * 100
                rand_copper = (self.noise(copper_1, copper_2, self.seedbank['sx_copper8'],
                                          self.seedbank['sy_copper8'])) * 255

                gold_1 = x/screen_width * 100
                gold_2 = y/screen_height * 100
                rand_gold = (self.noise(gold_1, gold_2, self.seedbank['sx_gold8'], self.seedbank['sy_gold8'])) * 255

                if rand_n3 < 256:
                    tile = objects.DirtTile()

                if rand_n3 > 5:
                    tile = objects.StoneTile()
                    # coal
                    if rand_coal > 220:
                        tile.color = (40, 40, 40)
                    # iron
                    if rand_coal < 30:
                        tile.color = (226, 160, 82)
                    # copper
                    if rand_copper < 25:
                        tile.color = (255, 137, 29)
                    # silver
                    if rand_copper > 227:
                        tile.color = (240, 240, 240)
                    # gold
                    if rand_gold < 25:
                        tile.color = (255, 235, 46)

            elif z == -9:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 200
                ny2 = y/screen_height * 200
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal9'], self.seedbank['sy_coal9'])) * 255

                silver_1 = x/screen_width * 200
                silver_2 = y/screen_height * 200
                rand_silver = (self.noise(silver_1, silver_2, self.seedbank['sx_silver9'],
                                          self.seedbank['sy_silver9'])) * 255

                gold_1 = x/screen_width * 100
                gold_2 = y/screen_height * 100
                rand_gold = (self.noise(gold_1, gold_2, self.seedbank['sx_gold9'], self.seedbank['sy_gold9'])) * 255

                crystal_1 = x/screen_width * 500
                crystal_2 = y/screen_height * 500
                rand_crystal = (self.noise(crystal_1, crystal_2, self.seedbank['sx_crystal9'], self.seedbank['sy_crystal9'])) * 255

                tile = objects.StoneTile()
                tile.color = (60, 60, 60)
                # coal
                if rand_coal > 220:
                    tile.color = (40, 40, 40)
                # iron
                if rand_coal < 30:
                    tile.color = (226, 160, 82)
                # silver
                if rand_silver > 227:
                    tile.color = (240, 240, 240)
                # gold
                if rand_gold < 25:
                    tile.color = (255, 235, 46)
                # crystal
                if rand_crystal > 227:
                    tile.color = (0, 255, 255)

            elif z == -10:
                nx = x/screen_width * 64
                ny = y/screen_height * 64
                nx2 = x/screen_width * 200
                ny2 = y/screen_height * 200
                nx3 = x/screen_width * 32
                ny3 = y/screen_height * 32

                rand_n = (self.noise(nx, ny, self.seedbank['sx'], self.seedbank['sy'])) * 255
                rand_n2 = (self.noise(nx2, ny2, self.seedbank['sx2'], self.seedbank['sy2'])) * 255
                rand_n3 = ((self.noise(nx3, ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.5 * self.noise(2 * nx3, 2 * ny3, self.seedbank['sx3'], self.seedbank['sy3'])) +
                           (0.25 * self.noise(4 * nx3, 4 * ny3, self.seedbank['sx3'], self.seedbank['sy3']))) * 255
                rand_n3 -= 90
                if rand_n3 > 255:
                    rand_n3 = 255
                elif rand_n3 < 0:
                    rand_n3 = 0

                # Ore calc
                coal_1 = x/screen_width * 200
                coal_2 = y/screen_height * 200
                rand_coal = (self.noise(coal_1, coal_2, self.seedbank['sx_coal10'], self.seedbank['sy_coal10'])) * 255

                silver_1 = x/screen_width * 200
                silver_2 = y/screen_height * 200
                rand_silver = (self.noise(silver_1, silver_2, self.seedbank['sx_silver10'],
                                          self.seedbank['sy_silver10'])) * 255

                gold_1 = x/screen_width * 100
                gold_2 = y/screen_height * 100
                rand_gold = (self.noise(gold_1, gold_2, self.seedbank['sx_gold10'], self.seedbank['sy_gold10'])) * 255

                crystal_1 = x/screen_width * 500
                crystal_2 = y/screen_height * 500
                rand_crystal = (self.noise(crystal_1, crystal_2, self.seedbank['sx_crystal10'],
                                           self.seedbank['sy_crystal10'])) * 255

                tile = objects.StoneTile()
                tile.color = (60, 60, 60)
                # coal
                if rand_coal > 220:
                    tile.color = (40, 40, 40)
                # iron
                if rand_coal < 30:
                    tile.color = (226, 160, 82)
                # silver
                if rand_silver > 227:
                    tile.color = (240, 240, 240)
                # gold
                if rand_gold < 25:
                    tile.color = (255, 235, 46)
                # crystal
                if rand_crystal > 225:
                    tile.color = (0, 255, 255)

            elif z < -10:
                tile = objects.BedrockTile()
        else:
            if z > 0:
                # Create a new tile
                tile = objects.AirTile()

            elif z == 0:
                tile = objects.GrassTile()
                if x % 2 == 0 and y % 2 == 0 or x % 2 != 0 and y % 2 != 0:
                    tile.color = (0, 220, 0)
                else:
                    tile.color = (0, 190, 0)
                if random.randint(1, 20) is 1:
                    tile.object[2] = self.instancer(objects.SpruceBottom())
                elif random.randint(1, 20) is 1:
                    tile.object[2] = self.instancer(objects.PineBottom())

            elif z == -1:
                tile = objects.DirtTile()
                if x % 2 == 0 and y % 2 == 0 or x % 2 != 0 and y % 2 != 0:
                    tile.color = (160, 70, 0)

            elif z < -1:
                tile = objects.StoneTile()
                if x % 2 == 0 and y % 2 == 0 or x % 2 != 0 and y % 2 != 0:
                    tile.color = (120, 120, 120)

        return tile

    def noise(self, nx, ny, seedx, seedy):
        """
        Takes a seed, and creates perlin noise to be used in world generation
        """
        return gen.noise2d(nx+seedx, ny+seedy) / 2.0 + 0.5

    def draw_master(self, x, y, xcount, ycount, new_display):
        """
        Draws the tiles, objects, and the player within a given xrange and yrange coords.
        """
        fetch = self.gc.fetch
        camera = self.gc.camera

        # TODO: Find out how to draw 2 tiles from the same column on top of eachother (when digging a hole)

        # Go through the column this tile is a part of, and find the Z coord that is closest to the camera
        topz = fetch.top_z(x, y)

        # Draw TILES
        self.draw_tiles(new_display, x, y, topz)

        # Draw OBJECTS
        self.find_objects(new_display, self.created_tiles[fetch.crd_2_str((x, y, topz))], x, y,
                          camera.sprite_res())

        # Darkness / Brightness overlays depending on depth or height of the camera
        # TODO: Make sure the darkness overlays are only for objects that don't have roots in non-low tiles
        # TODO: Treetops think they belong on the tile they are on, not the tile their wood is on
        # DOESNT QUITE WORK YET - NEEDS OVERHAUL
        """alpha_overlay = pygame.Surface((camera.scale, camera.scale))
        if topz < 0:
            alpha_overlay.fill((0, 0, 0))
            alpha_overlay.set_alpha((25.5*(camera.top_layer-topz))-25.5)
        else:
            alpha_overlay.fill((255, 255, 255))
            alpha_overlay.set_alpha((25.5*(camera.top_layer-topz))-25.5)
        new_display.blit(alpha_overlay, (xcount*camera.scale, ycount*camera.scale))"""


    def draw_tiles(self, display, x, y, z, xcount, ycount):
        """
        Draws the tile of a given coord onto a given display
        """
        camera = self.gc.camera
        if self.gc.fetch.crd_2_str((x, y, z)) not in self.created_tiles:
            self.tile_insertion(x, y, z)

        tile = self.created_tiles[self.gc.fetch.crd_2_str((x, y, z))]

        display.fill(tile.color, (xcount*camera.scale,
                              ycount*camera.scale+((self.gc.player.realcoords[2]-1 - tile.coords[2])*camera.scale/4),
                              camera.scale, camera.scale))



        # Make the wicked cool edges on tiles that have adjacent walls


        #try:
        #    if self.created_tiles[self.gc.fetch.crd_2_str((x, y-1, z+1))].name is not 'air' and \
        #       self.created_tiles[self.gc.fetch.crd_2_str((x, y, z+1))].name is 'air':

            #        display.fill(self.created_tiles[self.gc.fetch.crd_2_str((x, y-1, z+1))].color,
            #                     (xcount*camera.scale, ycount*camera.scale,
            #                      camera.scale, camera.scale/3))
    #
            #        display.blit(objects.img_blackersquare, (xcount*camera.scale, ycount*camera.scale),
            #                     (0, 0, camera.scale, camera.scale/3))
            #except KeyError:
            #    pass

    def player_update(self, new_display, draw_objects=None):
        """
        Draws the player and the object on top of him.
        """
        xcount = self.tiles_on_screenx // 2
        ycount = self.tiles_on_screeny // 2
        camera = self.gc.camera

        if self.gc.player.realcoords[2] == camera.top_layer:
            new_display.blit(self.gc.player.sprite[camera.sprite_res()], (xcount*camera.scale,
                                                                          ycount*camera.scale -
                                                                          (self.gc.player.realcoords[2]-1) *
                                                                          (camera.scale // 3)))
        else:
            # Draw ghost of player if viewing layer is below player layer
            new_display.blit(self.gc.player.ghost_sprite[camera.sprite_res()], (xcount*camera.scale, ycount*camera.scale+5))

        # Draw the objects on the player
        if draw_objects:
            x, y = self.gc.player.realcoords[0], self.gc.player.realcoords[1]
            self.find_objects(new_display, self.created_tiles[self.gc.fetch.crd_2_str((x, y, self.gc.fetch.top_z(x, y)))],
                              x, y, xcount, ycount, self.gc.camera.sprite_res())

    def find_objects(self, display, tile, x, y, res):
        """
        Checks if a given tile has any objects on it, and sends these objects to be drawn
        """

        if tile.object[0] is not None:
            self.draw_objects(display, tile, xcount, ycount, res, 0)
        if tile.object[2] is not None:
            self.draw_objects(display, tile, xcount, ycount, res, 2)
            # Draw PLAYER for the second time. This is if the player happens to occupy the same tile as a solid object
            # (like stairs) so the player is shown above the object
            if x == self.gc.fetch.find_tile('current').coords[0] and y == self.gc.fetch.find_tile('current').coords[1]:
                self.player_update(display)

                # put this instead if player isn't drawn correctly:
                # display.blit(player.sprite[camera.sprite_res()], (xcount*camera.scale, ycount*camera.scale))

        if tile.object[1] is not None:
            self.draw_objects(display, tile, xcount, ycount, res, 1)
        if tile.object[3] is not None:
            self.draw_objects(display, tile, xcount, ycount, res, 3)
        if tile.object[4] is not None:
            self.draw_objects(display, tile, xcount, ycount, res, 4)

    def draw_objects(self, display, tile2, x, y, res, number):
        """
        Draws the given object of the given tile to the screen, and rotates any objects that are directional
        """
        if tile2.object[number].vertical_sprite is not None:

            if tile2.object[number].direction == 'left':
                spriten = pygame.transform.flip(tile2.object[number].sprite[res], True, False)
            elif tile2.object[number].direction == 'right':
                spriten = tile2.object[number].sprite[res]
            elif tile2.object[number].direction == 'down':
                spriten = pygame.transform.flip(tile2.object[number].vertical_sprite[res], False, True)
            elif tile2.object[number].direction == 'up':
                spriten = tile2.object[number].vertical_sprite[res]

            display.blit(spriten, (x*self.gc.camera.scale, y*self.gc.camera.scale))
        else:
            display.blit(tile2.object[number].sprite[res], (x*self.gc.camera.scale, y*self.gc.camera.scale))

    def update_column(self, x, y, z):
        """
        Takes a coord, and adds the tile of that coord to the column-list. If no list exists, it creates one.
        This doesn't affect what columns are highest.
        """

        if self.tile_columns.get(self.gc.fetch.crd_2_str((x, y))) is None:
            self.tile_columns[self.gc.fetch.crd_2_str((x, y))] = [z]
        else:
            self.tile_columns[self.gc.fetch.crd_2_str((x, y))].append(z)

    def instancer(self, _class):
        """
        Takes a class and makes it into an instance. Used in world generation when creating objects like trees
        """
        instance = _class
        return instance

    def update_map(self, update_range, movement=None):
        """
        Adds coords that needs updating to a list,
        which is iterated through once a loop. The updates aren't processed here.
        """

        self.update_list.append(update_range)

