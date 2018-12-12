"""
This module is where things that are checked every loop is placed.
This includes normal event checks, map update checks, and key-press checks.
"""

import pygame
import data.keypress
import copy
import os
import random


class Updates:
    def __init__(self, gameclass):
        self.gc = gameclass
        self.dir_downhold_counter = 0
        self.direction_list = []
        self.method_list = []
        # Is a direction if the player has moved this frame
        self.move = None
        # Lists for chunks that need saving or loading incrementally
        self.chunk_load_list = {}
        self.chunk_delete_list = {}

        # How many tiles should be loaded each frame when loading in a chunk? 1 - 5376 (higher number means more lag)
        self.chunk_load_increments = 1
        # How many columns should be saved each frame when saving a chunk? 1 - 256 (higher number means more lag)
        self.chunk_save_increments = 50

    def check_all(self):
        """
        These are the updates and checks that are being made every loop.
        """
        self.gc.world.map_update = False
        self.event_checker()
        if self.gc.loop:
            self.downhold_checker()
            if len(self.chunk_load_list) > 0 and self.gc.tick % 59 == 0:
                self.chunk_incremental_load()
            if len(self.chunk_delete_list) > 0 and self.gc.tick == 0:
                print('g')
                self.chunk_incremental_save()
            self.map_update_checker()
            self.move_checker()
            self.new_chunk_checker()

    def downhold_checker(self):
        """
        When a directional button is pressed, add 1 to the time counter.
        This determines whether the player should keep going in one direction if the button is held
        """
        if self.dir_downhold_counter > 0:
            self.dir_downhold_counter += 1
            # If a directional button is held down for 10 frames, then move the player in that direction again
            if self.dir_downhold_counter > 10:
                self.gc.collision.check_collision(self.gc.player.direction)
                self.dir_downhold_counter = 1

    def event_checker(self):
        """
        Goes through all events in the pygame event handler and checks for keypresses
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # Delete all chunk text files when exiting the game
                for the_file in os.listdir('data/chunks'):
                    file_path = os.path.join('data/chunks', the_file)
                    os.unlink(file_path)
                self.gc.loop = False
            elif event.type == pygame.KEYDOWN:
                data.keypress.keypress(event, self.gc)
            elif event.type == pygame.KEYUP and event.key in\
                    (pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT):

                # remove the key that was lifted from the direction list
                if len(self.direction_list) > 0 and \
                       self.gc.fetch.event_2_string(event) in self.direction_list:
                    self.direction_list.remove(self.gc.fetch.event_2_string(event))

                if len(self.direction_list) > 0:
                    # if there are more directions being held, make the last one pressed into the new direction.
                    # update the map to update the player sprite. This makes the player direction seem a bit more
                    # "wobbly" when going in two directions at once (up/right, right/down, down/left, left/up), but it
                    # is barely noticeable unless you know it's there. It's also very rare someone presses 2 directions
                    # at the same time without keeping one of them held down.
                    self.gc.player.direction = self.direction_list[-1]
                    self.gc.collision.turn_player(self.direction_list[-1])
                    self.gc.world.update_map((self.gc.player.realcoords[0],
                                             self.gc.player.realcoords[1],
                                             self.gc.player.realcoords[2]))
                else:
                    # set the key-holding counter to 0 if there are no directions being held anymore
                    self.dir_downhold_counter = 0

            elif event.type == pygame.KEYUP and event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
                # When shift is released, resume forward movement if a direction is being held
                if self.gc.camera.top_layer == self.gc.player.realcoords[2] and len(self.direction_list) > 0:
                    self.gc.collision.check_collision(self.gc.player.direction)
                    self.dir_downhold_counter = 1

    def map_update_checker(self):
        """
        Call the make_map function only if the map has been updated this game loop.
        Go through the update_list and see if any updates are ALL (the whole map) or an x-range / y-range tuple
        (map portion). Player coord changes happens here. Force_player_draw updates the player position on the map.
        """

        # Sorts update coords after their Z and Y coords
        if len(self.gc.world.update_list) > 0:
            self.gc.world.update_list.sort(key=lambda x: x[2])
            chunkedlist = [[self.gc.world.update_list[0]]]
            n = 0
            for i in self.gc.world.update_list[1:]:
                if i[2] != chunkedlist[n][0][2]:
                    chunkedlist.append([i])
                    n+=1
                else:
                    chunkedlist[n].append(i)
            for chunk in chunkedlist:
                chunk.sort(key=lambda x: x[1], reverse=True)

            # Update each tile on the given coord
            for coordchunk in chunkedlist:
                for coord in coordchunk:
                    self.gc.world.draw_master(coord[0], coord[1], coord[2], self.gc.camera.active_map_display)
                    self.gc.world.draw_player(self.gc.camera.active_map_display)

            self.gc.camera.screen_update = True

        self.gc.player.last_movement = []
        self.gc.world.update_list = []
        self.gc.player.temporary_coords = copy.copy(self.gc.player.realcoords)

    def add_action_to_update_list(self, method):
        self.method_list.append(method)

    def move_checker(self):
        world = self.gc.world

        if self.move is not None:

            # Change player coords according to the direction the player has moved
            self.gc.player.realcoords[0] += self.gc.fetch.dir_2_change(self.gc.player.direction)[0]
            self.gc.player.realcoords[1] += self.gc.fetch.dir_2_change(self.gc.player.direction)[1]

            # Update the area around the player
            for x in range(self.gc.player.realcoords[0] - self.gc.world.tiles_on_screenx//2,
                           self.gc.player.realcoords[0] + self.gc.world.tiles_on_screenx//2):
                for y in range(self.gc.player.realcoords[1] - self.gc.world.tiles_on_screeny//2,
                               self.gc.player.realcoords[1] + self.gc.world.tiles_on_screeny//2):
                    world.draw_master(x, y, self.gc.player.realcoords[2], self.gc.camera.active_map_display)
            world.draw_player(self.gc.camera.active_map_display)

           # # Add more of the map on the edge of the screen
           # xrange = (world.tiles_on_screenx // 2 * -1, world.tiles_on_screenx // 2)
           # yrange = (world.tiles_on_screeny // 2, world.tiles_on_screeny // 2 + 1)
           # xrange = (-10, -10)
           # yrange = (-11, 9)
           # for y in range(yrange[0], yrange[1]):
           #     for x in range(xrange[0], xrange[1]):
           #         world.tile_insertion(x, y, 0)
#
           # for y in range(yrange[0], yrange[1]):
           #     for x in range(xrange[0], xrange[1]):
           #         world.draw_master(x, y, 0, self.gc.camera.active_map_display)
#
            self.gc.camera.screen_update = True
            self.move = None

    def new_chunk_checker(self):
        world = self.gc.world
        fetch = self.gc.fetch
        player = self.gc.player

        # Chunk shift
        if fetch.current_chunk() != player.last_chunk:
            world.new_chunk_list.append(fetch.current_chunk())
            player.last_chunk = fetch.current_chunk()
            fetch.update_loaded_chunks()

        if len(world.new_chunk_list) > 0:
            for chunk in world.new_chunk_list:

                adjacent_list = (chunk,
                                 (chunk[0] + 1, chunk[1] - 1),
                                 (chunk[0] - 1, chunk[1] + 1),
                                 (chunk[0] - 1, chunk[1] - 1),
                                 (chunk[0] + 1, chunk[1] + 1),
                                 (chunk[0], chunk[1] - 1),
                                 (chunk[0], chunk[1] + 1),
                                 (chunk[0] - 1, chunk[1]),
                                 (chunk[0] + 1, chunk[1]))

                for adjacent in adjacent_list:
                    if adjacent not in world.created_chunks:
                        world.create_chunk(adjacent)

            # Draw the PLAYER.
            world.draw_player(self.gc.camera.active_map_display)
            world.new_chunk_list = []

    def chunk_incremental_load(self):
        done_chunks = []
        for chunk_info in self.chunk_load_list:
            chunk_info = self.chunk_load_list[chunk_info]
            # chunk_info = [chunk, 0]:
            # [0] = chunk instace
            # [1] = current line

            file = open('data/chunks/%s.txt' % str(chunk_info[0].coords), 'r')
            contents = file.readlines()
            file.close()

            # Finds the right line to read from
            for increment_counter in range(self.chunk_load_increments):
                line = contents[chunk_info[1]].split('_')
                # Creates the tile
                tile = self.gc.fetch.make_tile_from_name(line[1])

                # INFO BEING STORED INTO THE TILE
                tile.coords = int(line[0].split(',')[0]), int(line[0].split(',')[1]), int(line[0].split(',')[2])
                if line[2] == 'None':
                    tile.color = None
                else:
                    tile.color = int(line[2].split(',')[0]), int(line[2].split(',')[1]), int(line[2].split(',')[2])
                objects = line[3].split(',')[0], line[3].split(',')[1], line[3].split(',')[2],\
                          line[3].split(',')[3], line[3].split(',')[4]
                tile.object = [None, None, None, None, None]
                n = 0
                for i in objects:
                    if i != 'None':
                        tile.object[n] = self.gc.fetch.make_object_from_name(i)
                    n += 1
                tile.item = line[4]
                if line[5] == 'False':
                    tile.passable = False
                else:
                    tile.passable = True
                if line[6] == 'False':
                    tile.passable_through = False
                else:
                    tile.passable_through = True
                if line[7] == 'False':
                    tile.visible = False
                else:
                    tile.visible = True
                tile.loaded = int(line[8])

                # Lastly, put the tile in the new chunk's dictionary.
                try:
                    chunk_info[0].tiles[tile.coords[0],tile.coords[1]][tile.coords[2]] = tile
                except KeyError:
                    chunk_info[0].tiles[tile.coords[0],tile.coords[1]] = {}
                    chunk_info[0].tiles[tile.coords[0],tile.coords[1]][tile.coords[2]] = tile

                # LASTLY, increase the counter that is used for linecounting by 1
                chunk_info[1] += 1

                # If count is bigger than the amount of tiles there are in a chunk, then the chunk has been fully loaded
                cam = self.gc.camera
                if chunk_info[1] >= (cam.chunk_size * cam.chunk_size * (cam.chunk_sky_height + abs(cam.chunk_ground_depth))):

                    # When all lines have been written, insert the completed chunk into the "loaded tiles" dict.
                    self.gc.world.loaded_chunks[chunk_info[0].coords] = chunk_info[0]

                    # add chunk to be removed
                    done_chunks.append(chunk_info[0].coords)

                    # Update the screen
                    cam.screen_update = True

                    break

        # Delete saved chunks from the chunk_delete_list
        for chunk_coords in done_chunks:
            self.chunk_load_list.pop(chunk_coords)

    def chunk_incremental_save(self):
        done_chunks = []
        chunk_info = self.chunk_delete_list[random.choice(list(self.chunk_delete_list))]

        # This method will save the chunk one column at a time. (that's around 21 tiles a frame)

        # chunk_info = [chunk, 0, list]:
        # [0] = chunk instace
        # [1] = current line
        # [2] = list of all columns in chunk, which need to be saved

        # Open relevant file, and start writing in it
        if chunk_info[1] == 0:
            if os.path.isfile('data/chunks/%s.txt' % str(chunk_info[0].coords)):
                os.remove('data/chunks/%s.txt' % str(chunk_info[0].coords))
        file = open('data/chunks/%s.txt' % str(chunk_info[0].coords), 'a')

        for n in range(self.chunk_save_increments):

            # Look through the XY list (by the Count) to find a column, and write down the tiles of that column
            for tile in chunk_info[0].tiles[chunk_info[2][chunk_info[1]]].values():

                # This will just output a Z value, since the X and Y are the same

                # Write shit
                file.write('%i,%i,%i_' % (tile.coords[0], tile.coords[1], tile.coords[2]))
                file.write('%s_' % str(type(tile).__name__))
                if tile.color is None:
                    file.write('None_')
                else:
                    file.write('%i,%i,%i_' % (tile.color[0], tile.color[1], tile.color[2]))
                for item in tile.object:
                    if item is None:
                        file.write('None,')
                    elif item.name is 'staircase':
                        file.write('Staircase(%s)' % str(item.direction))
                    else:
                        file.write('%s,' % str(type(item).__name__))
                file.write('_%s_' % str(tile.item))
                file.write('%s_' % str(tile.passable))
                file.write('%s_' % str(tile.passable_through))
                file.write('%s_' % str(tile.visible))
                file.write('%s_\n' % str(tile.loaded))

            # After the column is done, increase the counter by 1
            chunk_info[1] += 1

            # If count is bigger than the amount of columns in a chunk then the chunk has been fully saved
            if chunk_info[1] >= self.gc.camera.chunk_size * self.gc.camera.chunk_size:

                # add chunk to be removed
                done_chunks.append(chunk_info[0].coords)
                break

        file.close()

        # Delete saved chunks from the chunk_delete_list
        for chunk_coords in done_chunks:
            self.chunk_delete_list.pop(chunk_coords)

            # Update the screen
            self.gc.camera.screen_update = True

