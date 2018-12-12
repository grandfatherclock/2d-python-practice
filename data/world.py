"""
This file keeps track of everything world-generation related. Make_map can be called to update one or more tiles.
"""

import random
import pygame
import data.objects as objects
from opensimplex import OpenSimplex
gen = OpenSimplex()
import os


class WorldChange:
    def __init__(self, gameclass):
        self.gc = gameclass
        self.test_world = True
        self.loaded_chunks = {}
        self.created_chunks = []
        self.new_chunk_list = [(0,0)]
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

        # Whether or not chunks should be deleted and reloaded when they go out of view
        self.chunk_deletion = True
        self.all_chunks = {}

        self.first = True
        self.local_update = None
        self.update_list = []
        self.update_all = True
        # Is true if the player has digged out the tile below them
        self.dig = False
        # Used for when looking for a solid tile in a column
        self.found_solid = False
        self.tiles_on_screenx = 16
        # There are more tiles on the Y axis so rendering large trees can't be seen when going downwards
        self.tiles_on_screeny = 16

    def reset_map(self):
        """
        Resets all variables. Keeps looping until a map is created where the player is standing on a clean tile.
        """
        iterationcount = 0

        n = True
        while n:
            # Delete all chunk text files when exiting the game
            for the_file in os.listdir('data/chunks'):
                file_path = os.path.join('data/chunks', the_file)
                os.unlink(file_path)

            self.add_object = {}
            self.loaded_chunks = {}
            self.created_chunks = []
            self.new_chunk_list = [(0,0)]
            self.first = True
            self.gc.player.realcoords = [0, 0, 1]
            self.gc.player.temporary_coords = [0, 0, 1]
            self.gc.collision.on_stairs = None

            self.gc.camera.top_layer = 1
            self.gc.camera.stairs_entrance = None
            self.gc.camera.status_surface = None
            self.gc.camera.active_map_display = None
            self.update_all = True
            self.make_map()

            iterationcount += 1
            if self.gc.fetch.tile_finder(self.gc.player.realcoords[0],
                                         self.gc.player.realcoords[1],
                                         self.gc.player.realcoords[2]-1).passable and \
               self.gc.fetch.is_tile_clean(self.gc.fetch.tile_finder(self.gc.player.realcoords[0],
                                           self.gc.player.realcoords[1],
                                           self.gc.player.realcoords[2]-1)):
                n = False

        print(iterationcount, "iterations")

    def make_map(self):
        print('mm')
        """
        Creates the world map. Is only run ONCE when creating the start of the map.
        """
        # Seedmaking
        if self.first:
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

        player = self.gc.player
        camera = self.gc.camera
        new_display = pygame.Surface((self.tiles_on_screenx*self.gc.camera.scale,
                                      self.tiles_on_screeny*self.gc.camera.scale))
        xrange = ((self.tiles_on_screenx//2*-1)+player.realcoords[0], self.tiles_on_screenx//2+player.realcoords[0])
        yrange = ((self.tiles_on_screeny//2*-1)+player.realcoords[1], self.tiles_on_screeny//2+player.realcoords[1])
        zrange = (-10, 11)

        # Creates all tiles within a certain range, and fills them with objects.
        for n in [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 0), (0, 1),
                  (1, -1), (1, 0), (1, 1)]:
            self.create_chunk(n)

        # Draws the tiles and objects created by the insertion
        '''for y in range(yrange[0], yrange[1]):
            for x in range(xrange[0], xrange[1]):
                self.draw_master(x, y, 0, new_display)'''

        # Update the area around the player

        for x in range(self.gc.player.realcoords[0] - self.gc.world.tiles_on_screenx//2,
                       self.gc.player.realcoords[0] + self.gc.world.tiles_on_screenx//2):
            for y in range(self.gc.player.realcoords[1] - self.gc.world.tiles_on_screeny//2,
                           self.gc.player.realcoords[1] + self.gc.world.tiles_on_screeny//2):
                self.draw_master(x, y, self.gc.player.realcoords[2], new_display)

        # Draw the PLAYER.
        self.draw_player(new_display)

        camera.active_map_display = new_display.copy()

    def tile_insertion(self, x, y, z, chunk, checkchunk):
        """
        Creates a tile instance with info from tile_calculation in a given x, y, z coordinate, as well as
        objects and connected objects. Checkchunk boolean decides whether or not this tile should create adjacent chunks
        if it itself is a new chunk.
        """

        fetch = self.gc.fetch

        # Fill the tile
        tile = self.tile_calculation(x, y, z)
        tile.coords = (x, y, z)

        # Create additional objects that are connected (like leaves on trees)
        # See if this tile has connected objects
        '''for n in range(5):
            try:
                for connection in tile.object[n].connected:
                    # See if the connected object's specific tile is in the system
                    
                    if home_chunk.get(fetch.crd_2_str((x + connection[1][0],
                                                               y + connection[1][1], z))) is None:            
                    
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
                continue'''

        '''# If the previous action (connected tiles being assigned to non-created tiles) happened to this
        # tile, then add the relevant connections to this tile's objects, and remove the element
        # completely from the add_object library
        if self.add_object.get(fetch.crd_2_str((x, y, z))) is not None:
            for prev_connection in self.add_object[fetch.crd_2_str((x, y, z))]:
                tile.object[prev_connection.layer] = prev_connection
            self.add_object.pop(fetch.crd_2_str((x, y, z)))'''

        # Add tiles to the 2d tile column list (used in drawing to find transparent tiles)
        if (x,y) in chunk.tiles:
            chunk.tiles[x,y][z] = tile
        else:
            chunk.tiles[x,y] = {}
            chunk.tiles[x,y][z] = tile
            if checkchunk:
                self.new_chunk_list.append((x//self.gc.camera.chunk_size, y//self.gc.camera.chunk_size))

    def tile_calculation(self, x, y, z):
        """
        The real worldgen. Takes some coords, makes a tile out of it, and returns the tile. Only makes natural tiles.
        """

        screen_width = self.gc.camera.SCREEN_WIDTH
        screen_height = self.gc.camera.SCREEN_HEIGHT

        # For the random seed that decides how the worldgen creates stuff.

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

    def create_chunk(self, chunkcoords):
        camera = self.gc.camera
        newchunk = objects.Chunk(chunkcoords[0], chunkcoords[1])
        xrange = (chunkcoords[0] * camera.chunk_size, chunkcoords[0] * camera.chunk_size + camera.chunk_size)
        yrange = (chunkcoords[1] * camera.chunk_size, chunkcoords[1] * camera.chunk_size + camera.chunk_size)
        zrange = (camera.chunk_ground_depth, camera.chunk_sky_height)

        # Creates all tiles within a certain range, and fills them with objects.
        for y in range(yrange[0], yrange[1]):
            for x in range(xrange[0], xrange[1]):
                for z in range(zrange[0], zrange[1]):
                    self.tile_insertion(x, y, z, newchunk, False)

        # Add chunk to loaded chunks
        self.created_chunks.append(chunkcoords)

        # Add chunk to list with all chunks, if chunk deletion is off
        if self.chunk_deletion is False:
            self.all_chunks[chunkcoords] = newchunk

        # If the created chunk is too far away from the player (i.e unloaded), then delete it from "loaded chunks".
        self.loaded_chunks[chunkcoords] = newchunk
        if abs(self.gc.fetch.current_chunk()[0] - chunkcoords[0]) > 1 \
                or abs(self.gc.fetch.current_chunk()[1] - chunkcoords[1]) > 1:
            del self.loaded_chunks[chunkcoords]

    def draw_master(self, x, y, z, new_display):
        """
        Takes the tiles and their coordinates from the tile_insertion, and draws them to the display,
        as well as objects and the player
        """

        fetch = self.gc.fetch
        camera = self.gc.camera

        # Go through the column this tile is a part of, and find the Z coord that is closest to the camera
        toptile = fetch.top_tile(x, y)

        # Draw TILES
        self.draw_tiles(new_display, x, y, toptile.coords[2])

        # Draw OBJECTS
        self.find_objects(new_display, self.gc.fetch.tile_finder(x, y, toptile.coords[2]), x, y,
                          camera.sprite_res(),
                          self.tiles_on_screenx//2*camera.scale - self.gc.player.realcoords[0]*camera.scale,
                          self.tiles_on_screeny//2*camera.scale - self.gc.player.realcoords[1]*camera.scale,
                          self.gc.player.realcoords)

        # Darkness / Brightness overlays depending on depth or height of the camera
        # DOESNT QUITE WORK YET - NEEDS OVERHAUL
        """alpha_overlay = pygame.Surface((camera.scale, camera.scale))
        if topz < 0:
            alpha_overlay.fill((0, 0, 0))
            alpha_overlay.set_alpha((25.5*(camera.top_layer-topz))-25.5)
        else:
            alpha_overlay.fill((255, 255, 255))
            alpha_overlay.set_alpha((25.5*(camera.top_layer-topz))-25.5)
        new_display.blit(alpha_overlay, (xcount*camera.scale, ycount*camera.scale))"""

    def draw_tiles(self, display, x, y, z):
        """
        Draws the tile of a given coord onto a given display
        """
        camera = self.gc.camera

        tile = self.gc.fetch.tile_finder(x, y, z)

        # we add these to the tile drawing, since the screen can't take negative values. Therefore everything is offset
        # by half the tiles visible on the screen (as these will be all the negative ones)
        x_add = self.tiles_on_screenx//2*camera.scale - self.gc.player.realcoords[0]*camera.scale
        y_add = self.tiles_on_screeny//2*camera.scale - self.gc.player.realcoords[1]*camera.scale

        display.fill(tile.color, (x*camera.scale+x_add,
                                  y*camera.scale+y_add +
                                  # this offsets each layer a bit towards y
                                  ((self.gc.player.realcoords[2]-1 - tile.coords[2])*camera.scale/4),
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

    def draw_player(self, new_display):
        """
        Draws the player and the object on top of him.
        """
        camera = self.gc.camera
        x_add = self.tiles_on_screenx//2*camera.scale
        y_add = self.tiles_on_screeny//2*camera.scale
        player_coords = self.gc.player.realcoords

        if self.gc.player.realcoords[2] == camera.top_layer:
            new_display.blit(self.gc.player.sprite[camera.sprite_res()], (x_add, y_add))
        else:
            # Draw ghost of player if viewing layer is below player layer
            new_display.blit(self.gc.player.ghost_sprite[camera.sprite_res()], (camera.scale, camera.scale+5))

        # Draw the objects on the player. Topz finds the highest non-air tile in a column to be drawn on screen
        x, y = self.gc.player.realcoords[0], self.gc.player.realcoords[1]
        topz = self.gc.fetch.top_tile(x, y).coords[2]

        self.find_objects(new_display, self.gc.fetch.tile_finder(x, y, topz), x, y, self.gc.camera.sprite_res(),
                          self.tiles_on_screenx//2*camera.scale - self.gc.player.realcoords[0]*camera.scale,
                          self.tiles_on_screeny//2*camera.scale - self.gc.player.realcoords[1]*camera.scale, player_coords)

        # Check if the player moved behind a tile, and if so, draw it.
        if self.gc.player.movement:
            x, y, z = self.gc.player.realcoords[0]
            if self.gc.fetch.tile_finder(x, y+1, z).passable_through is False:
                self.gc.player.movement = None

    def find_objects(self, display, tile, x, y, res, x_add, y_add, player_coords):
        """
        Checks if a given tile has any objects on it, and sends these objects to be drawn
        """

        if tile.object[0] is not None:
            self.draw_objects(display, tile, x, y, res, 0)
        if tile.object[2] is not None:
            self.draw_objects(display, tile, x, y, res, 2)
            # Draw PLAYER for the second time. This is if the player happens to occupy the same tile as a solid object
            # (like stairs) so the player is shown above the object
            if (player_coords[0], player_coords[1]) == (x, y):
                display.blit(self.gc.player.sprite[self.gc.camera.sprite_res()],
                             (player_coords[0]*self.gc.camera.scale+x_add,
                              player_coords[1]*self.gc.camera.scale+y_add))

                # put this instead if player isn't drawn correctly:
                # display.blit(player.sprite[camera.sprite_res()], (xcount*camera.scale, ycount*camera.scale))

        if tile.object[1] is not None:
            self.draw_objects(display, tile, x, y, res, 1)
        if tile.object[3] is not None:
            self.draw_objects(display, tile, x, y, res, 3)
        if tile.object[4] is not None:
            self.draw_objects(display, tile, x, y, res, 4)

    def draw_objects(self, display, tile, x, y, res, number):
        """
        Draws the given object of the given tile to the screen, and rotates any objects that are directional
        """
        x_add = self.tiles_on_screenx//2*self.gc.camera.scale - self.gc.player.realcoords[0]*self.gc.camera.scale
        y_add = self.tiles_on_screeny//2*self.gc.camera.scale - self.gc.player.realcoords[1]*self.gc.camera.scale

        if tile.object[number].vertical_sprite is not None:

            if tile.object[number].direction == 'left':
                spriten = pygame.transform.flip(tile.object[number].sprite[res], True, False)
            elif tile.object[number].direction == 'right':
                spriten = tile.object[number].sprite[res]
            elif tile.object[number].direction == 'down':
                spriten = pygame.transform.flip(tile.object[number].vertical_sprite[res], False, True)
            elif tile.object[number].direction == 'up':
                spriten = tile.object[number].vertical_sprite[res]

            display.blit(spriten, (x*self.gc.camera.scale + x_add, y*self.gc.camera.scale + y_add))
        else:
            display.blit(tile.object[number].sprite[res], (x*self.gc.camera.scale + x_add, y*self.gc.camera.scale + y_add))

    def instancer(self, _class):
        """
        Takes a class and makes it into an instance. Used in world generation when creating objects like trees
        """
        instance = _class
        return instance

    def update_map(self, update_range):
        """
        Adds coords that needs updating to a list,
        which is iterated through once a loop. The updates aren't processed here.
        """

        self.update_list.append(update_range)

