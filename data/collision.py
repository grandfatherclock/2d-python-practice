"""
This file is called every time the player goes in a direction. It finds out whether the tile or object the player tries
to go to is passable. It also keeps track of how stairs work when entered and exited.
"""

import pygame


class Collision:
    def __init__(self, gameclass):
        self.gc = gameclass
        self.on_stairs = None
        self.can_pass = False

    def check_collision(self, direction):
        """
        Checks whether or not the player can move in the desired direction. If it can, then move the player. If not,
        then change the player's direction to the new direction, but do not move.
        """
        # Change player's sprite's direction

        cant_pass = False
        test_for_obstruction = False

        if self.on_stairs is not None:
            # TODO: you can't go down 2 sets of stairs right after eachother if they both go in the same direction
            if direction == self.gc.fetch.opposite_cardinal(self.on_stairs[0]):
                # If the player is on stairs and want to go back from the way they came
                cant_pass = False
                if self.on_stairs[1] == 'down':

                    self.gc.player.temporary_coords[2] += 1
                    self.gc.player.realcoords[2] += 1

                elif self.on_stairs[1] == 'up':
                    self.gc.player.temporary_coords[2] -= 1
                    self.gc.player.realcoords[2] -= 1

                self.gc.camera.top_layer = self.gc.player.temporary_coords[2]
                self.gc.world.update_all = True
                self.on_stairs = None
            elif direction is not self.on_stairs[0]:
                self.gc.world.update_map((self.gc.player.temporary_coords[0],
                                         self.gc.player.temporary_coords[1],
                                         self.gc.player.temporary_coords[2]))
                return
            else:
                # If the player continues on
                test_for_obstruction = True

        # Check if the tile itself is passable
        if self.gc.fetch.tile_finder(self.gc.player.temporary_coords[0]+self.gc.fetch.dir_2_change(direction)[0],
                                     self.gc.player.temporary_coords[1]+self.gc.fetch.dir_2_change(direction)[1],
                                     self.gc.player.temporary_coords[2]).passable_through is False or \
            self.gc.fetch.tile_finder(self.gc.player.temporary_coords[0]+self.gc.fetch.dir_2_change(direction)[0],
                                      self.gc.player.temporary_coords[1]+self.gc.fetch.dir_2_change(direction)[0],
                                      self.gc.player.temporary_coords[2]-1).passable is False:
            cant_pass = True

        # Check if that tile has an object, and if that object is passable
        for n in range(0, 3):

            # Check the tile right in front of the player (really the tile below that one)
            if self.gc.fetch.find_tile('below viewing', self.gc.player.temporary_coords).object[n] is not None:

                if self.gc.fetch.find_tile('below viewing', self.gc.player.temporary_coords).object[n].passable is False:
                    cant_pass = True

                elif self.gc.fetch.find_tile('below viewing', self.gc.player.temporary_coords).object[n].passable:

                    # tests if there is a passable object below, but which can only be passed from certain directions
                    # (right now this is only relevant for stairs)
                    if self.gc.fetch.find_tile('below viewing', self.gc.player.temporary_coords).object[n].block_sides is not None:
                        if self.is_blocked_sides_passable(
                                     self.gc.fetch.find_tile('below viewing', self.gc.player.temporary_coords).object[n].block_sides,
                                     self.gc.fetch.find_tile('below viewing', self.gc.player.temporary_coords).coords[2]):
                            cant_pass = False
                            # Do this if you're entering an UP staircase
                            if self.gc.fetch.find_tile('below viewing', self.gc.player.temporary_coords).object[n].name == 'staircase':
                                self.on_stairs = (direction, 'up')
                                self.gc.player.realcoords[2] += 1
                                self.gc.camera.top_layer = self.gc.player.realcoords[2]
                                self.gc.world.update_map('all')
                                if test_for_obstruction:
                                    test_for_obstruction = False
                        else:
                            cant_pass = True
                    else:
                        cant_pass = False
        # Do this if you're entering a DOWN staircase
        if self.gc.fetch.find_tile('below below viewing',
                                   self.gc.player.temporary_coords).object[2] is not None:
            if self.gc.fetch.find_tile('below below viewing',
                                       self.gc.player.temporary_coords).object[2].name == 'staircase':

                if self.is_blocked_sides_passable(self.gc.fetch.find_tile('below below viewing',
                                                  self.gc.player.temporary_coords).object[2].block_sides,
                                                  self.gc.fetch.find_tile('below below viewing',
                                                  self.gc.player.temporary_coords).coords[2]):
                    cant_pass = False
                    self.on_stairs = (direction, 'down')
                    self.gc.player.realcoords[2] -= 1
                    self.gc.camera.top_layer = self.gc.player.realcoords[2]
                    self.gc.world.update_map('all')
                    if test_for_obstruction:
                        test_for_obstruction = False

        # The player can clip into solid objects while pressing 2 directions, so here's a small delay to stop it
        if len(self.gc.updates.direction_list) > 1 and self.gc.updates.dir_downhold_counter < 2:
            cant_pass = True

        if not cant_pass or self.can_pass:
            if test_for_obstruction is True:
                self.on_stairs = None
            # Check if the player is underneath a solid tile (underground or in a house)
            self.top_layer_calculator(self.gc.fetch.find_tile('viewing', self.gc.player.temporary_coords))

            self.gc.player.last_movement.append(direction)
            self.gc.updates.move = direction

        else:
            self.gc.world.update_map((self.gc.player.temporary_coords[0],
                                      self.gc.player.temporary_coords[1],
                                      self.gc.player.realcoords[2]))

    def turn_player(self, direction):
        """
        Turns the player sprite to a given direction
        """
        turns = self.gc.fetch.how_many_turns('up', direction)

        self.gc.player.sprite[self.gc.camera.sprite_res()] = \
            pygame.transform.rotate(self.gc.objects.img_player, - 90 * turns)
        self.gc.player.ghost_sprite[self.gc.camera.sprite_res()] = \
            pygame.transform.rotate(self.gc.objects.img_playeroutline, - 90 * turns)

    def is_blocked_sides_passable(self, system, object_layer):
        """
        Finds out whether an object can be passed through. If a side is marked X then it is not passable.
        If a side is marked O then it is. If a side is marked B then it can only be accessed if it's below the player.
        """
        direction = self.gc.player.direction

        if direction == 'right':
            relevant_index = 3
        elif direction == 'down':
            relevant_index = 1
        elif direction == 'left':
            relevant_index = 5
        else:
            relevant_index = 7

        if system[relevant_index] in ['x']:
            return False
        elif system[relevant_index] in ['o']:
            return True
        elif system[relevant_index] in ['b']:
            if self.gc.player.realcoords[2] - 2 == object_layer:
                return True
            else:
                return False

    def top_layer_calculator(self, p_t):
        """
        Calculates whether the height of the camera should be lowered or raised, based on whether the player is "under"
        anything else than an air tile.
        """
        if self.gc.fetch.tile_name(p_t.coords[0], p_t.coords[1], p_t.coords[2]+1) is not 'air' \
                and self.gc.camera.previous_tile == 'air':
            self.gc.camera.top_layer = p_t.coords[2]
            self.gc.world.update_all = True

        self.gc.camera.previous_tile = self.gc.fetch.tile_name(p_t.coords[0], p_t.coords[1], p_t.coords[2] + 1)
