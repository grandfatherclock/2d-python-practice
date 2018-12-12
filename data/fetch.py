"""
FETCH contains all functions that 'fetch' something when given certain information.
"""

import pygame


class Fetch:
    def __init__(self, gameclass):
        self.gc = gameclass

    def tile_name(self, sx, sy, sz):
        """
        Returns the name of the tile in the given coords. If no tile exists, then it is created.
        """
        # Gives the name of a specific block, like 'air', 'water', or others. Does not return the tile itself,
        # but does CREATE the specific tile, if it's not in the system.
        if self.gc.fetch.tile_finder(sx, sy, sz) is None:
            return None
        else:
            return self.gc.fetch.tile_finder(sx, sy, sz).name

    def find_tile(self, location, coords=None):
        """
        Returns the tile corresponding to the given string. If the tile doesn't exist, then tile_name will create it.
        """

        if not coords:
            coords = self.gc.player.realcoords

        direction = self.gc.player.direction
        change = self.dir_2_change(direction)

        if location == 'current':
            change = [0, 0]
            extra = 0
        elif location == 'below current':
            change = [0, 0]
            extra = -1
        elif location == 'below below current':
            change = [0, 0]
            extra = -2
        elif location == 'viewing':
            extra = 0
        elif location == 'below viewing':
            extra = -1
        elif location == 'below below viewing':
            extra = -2

        return self.gc.fetch.tile_finder(coords[0] + change[0], coords[1] + change[1], coords[2] + extra)

    def crd_2_str(self, coord):
        """
        Converts given coords (x, y, z) into strings. Used when accessing created_tiles and tile_columns dicts
        """
        if len(coord) == 3:
            return str(str(coord[0]) + ',' + str(coord[1]) + ',' + str(coord[2]))
        elif len(coord) == 2:
            return str(str(coord[0]) + ',' + str(coord[1]))

    def top_tile(self, column_x, column_y):
        """
        Returns the top non-air tile of a given tile column
        """
        newlist = []
        dicto = self.gc.world.loaded_chunks[self.chunk_convert(column_x, column_y)].tiles[column_x, column_y]
        for pair in dicto:
            if dicto[pair].name != 'air':
                newlist.append(pair)
        number = (max(filter(lambda f: f <= self.gc.camera.top_layer, newlist)))
        return self.gc.world.loaded_chunks[self.chunk_convert(column_x, column_y)].tiles[column_x, column_y][number]

    def is_tile_clean(self, tile):
        """
        Returns whether a given tile has any objects on it
        """
        d = True
        for n in range(0, 5):
            if tile.object[n] is not None:
                d = False
        return d

    def how_many_turns(self, direction_start, direction_end):
        """
        Returns the amount of turns taken between 2 directions - used in calculating entranceways of placed staircases
        """
        dir_list = ['right', 'down', 'left', 'up']
        start_index = dir_list.index(direction_start)
        end_index = dir_list.index(direction_end)

        if start_index > end_index:
            final = 4 - start_index + end_index
        else:
            final = end_index - start_index
        return final

    def event_2_string(self, event):
        """
        Returns a simplified string of the given directional keypress-event
        """
        if event.key == pygame.K_DOWN:
            return 'down'
        elif event.key == pygame.K_RIGHT:
            return 'right'
        elif event.key == pygame.K_LEFT:
            return 'left'
        elif event.key == pygame.K_UP:
            return 'up'

    def dir_2_change(self, direction):
        """
        Returns the x and y change of the given direction
        """
        if direction == 'up':
            return [0, -1]
        elif direction == 'right':
            return [1, 0]
        elif direction == 'down':
            return [0, 1]
        else:
            return [-1, 0]

    def opposite_cardinal(self, direction):
        """
        Returns the exact opposite direction of the given direction
        """
        if direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'

    def current_chunk(self):
        """
        Returns the chunk the player is currently standing in
        """
        x = self.gc.player.realcoords[0]//self.gc.camera.chunk_size
        y = self.gc.player.realcoords[1]//self.gc.camera.chunk_size
        return x, y

    def update_loaded_chunks(self):
        """
        Saves and deletes unloaded chunks, and loads info from
        previously deleted ones that are now loaded
        """
        newlist = []
        for n in [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 0), (0, 1),
                  (1, -1), (1, 0), (1, 1)]:
            x = self.current_chunk()[0] + n[0]
            y = self.current_chunk()[1] + n[1]

            newlist.append((x, y))

            if (x, y) not in self.gc.world.loaded_chunks and (x, y) in self.gc.world.created_chunks:
                if self.gc.world.chunk_deletion:

                    # Check if the chunk is currently being saved (due to having been deleted)
                    if (x, y) in self.gc.updates.chunk_delete_list:
                        self.gc.world.loaded_chunks[x, y] = self.gc.updates.chunk_delete_list[x, y][0]

                    # If not, then send it to be loaded
                    elif (x, y) not in self.gc.updates.chunk_load_list:
                        self.gc.updates.chunk_load_list[x, y] = [self.gc.objects.Chunk(x, y), 0]

                else:
                    # load from existing list if chunk deletion is off
                    self.gc.world.loaded_chunks[x, y] = self.gc.world.all_chunks[x, y]

        for k in self.gc.world.loaded_chunks.copy():
            if k not in newlist:

                if self.gc.world.chunk_deletion:
                    # Make a file with this chunk and its info for later loading if chunk deletion is on
                    if k not in self.gc.updates.chunk_delete_list:
                        self.gc.updates.chunk_delete_list[k] = [self.gc.world.loaded_chunks[k], 0,
                                                                list(self.gc.world.loaded_chunks[k].tiles)]

                self.gc.world.loaded_chunks.pop(k)

    def make_tile_from_name(self, name):
        if name == "SandTile":
            newtile = self.gc.objects.SandTile()
        elif name == "GrassTile":
            newtile = self.gc.objects.SandTile()
        elif name == "StoneTile":
            newtile = self.gc.objects.StoneTile()
        elif name == "BedrockTile":
            newtile = self.gc.objects.BedrockTile()
        elif name == "DirtTile":
            newtile = self.gc.objects.DirtTile()
        elif name == "WaterTile":
            newtile = self.gc.objects.WaterTile()
        elif name == "AirTile":
            newtile = self.gc.objects.AirTile()

        return newtile

    def make_object_from_name(self, name):
        if name == "SpruceTop":
            newobject = self.gc.objects.SpruceTop()
        elif name == "SpruceBottom":
            newobject = self.gc.objects.SpruceBottom()
        elif name == "PineMiddle":
            newobject = self.gc.objects.PineMiddle()
        elif name == "PineTop":
            newobject = self.gc.objects.PineTop()
        elif name == "PineBottom":
            newobject = self.gc.objects.PineBottom()
        elif name == "Rock":
            newobject = self.gc.objects.Rock()
        elif name == "BigRock":
            newobject = self.gc.objects.BigRock()
        elif name == "Bush":
            newobject = self.gc.objects.Bush()
        elif name == "BerryBush":
            newobject = self.gc.objects.BerryBush()
        elif name == "TallGrass":
            newobject = self.gc.objects.TallGrass()
        elif name == "DarkTallGrass":
            newobject = self.gc.objects.DarkTallGrass()
        elif name == "TestObject":
            newobject = self.gc.objects.TestObject()
        elif name == "WoodWall":
            newobject = self.gc.objects.WoodWall()
        elif name == "RockWall":
            newobject = self.gc.objects.RockWall()
        elif name == "Planks":
            newobject = self.gc.objects.Planks()
        elif name == "Road":
            newobject = self.gc.objects.Road()
        elif name == "Staircase(up)":
            newobject = self.gc.objects.Staircase()
            newobject.direction = 'up'
        elif name == "Staircase(down)":
            newobject = self.gc.objects.Staircase()
            newobject.direction = 'down'
        elif name == "Staircase(right)":
            newobject = self.gc.objects.Staircase()
            newobject.direction = 'right'
        elif name == "Staircase(left)":
            newobject = self.gc.objects.Staircase()
            newobject.direction = 'left'

        return newobject

    def chunk_convert(self, x, y):
        return x//self.gc.camera.chunk_size, y//self.gc.camera.chunk_size

    def tile_finder(self, x, y, z):
        try:
            return self.gc.world.loaded_chunks[self.chunk_convert(x, y)].tiles[x, y][z]
        except KeyError:
            return 'air'


