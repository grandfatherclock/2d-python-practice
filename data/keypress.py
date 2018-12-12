"""
This is where keypresses are utilized. It's just one big function, as no internal info is really needed.
Most of the time, it just calls other classes in other files to do the processing.
"""

import pygame
import copy


def keypress(event, gc):

    # Reset map
    if event.key == pygame.K_RETURN:
        gc.world.reset_map()

    # Make map (for testing purposes)
    elif event.key == pygame.K_m:
        gc.world.make_map()

    # Zoom in
    elif event.key == pygame.K_z:
        gc.actions.zoom()

    # Go down 1 layer
    elif event.key == pygame.K_s:
        gc.camera.top_layer -= 1
        if gc.camera.top_layer < -10:
            gc.camera.top_layer = -10
        else:
            gc.world.update_all = True
        gc.camera.camera_change()

    # Go up 1 layer
    elif event.key == pygame.K_w:
        gc.camera.top_layer += 1
        if gc.camera.top_layer > 10:
            gc.camera.top_layer = 10
        else:
            gc.world.update_all = True
        gc.camera.camera_change()

    # Show status and map of created tiles
    elif event.key == pygame.K_v:
        print('created: '+str(len(gc.world.created_tiles)))
        gc.camera.status_surface = pygame.Surface((100, 100))
        gc.camera.status_surface.set_colorkey((0, 0, 0))
        for tile in gc.world.created_tiles.items():
            if tile[1].name is not 'air':
                gc.camera.status_surface.fill(tile[1].color, (tile[1].coords[0]+50, tile[1].coords[1]+50, 1, 1))

    elif event.key == pygame.K_c and not gc.camera.locked_move:
        if gc.collision.can_pass:
            gc.collision.can_pass = False
        else:
            gc.collision.can_pass = True

    # Actions

    elif event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT) and not gc.camera.locked_move:
        # See if player should be able to move - player can't move if viewing layer is not player layer
        if gc.camera.top_layer == gc.player.realcoords[2]:
            gc.player.direction = gc.fetch.event_2_string(event)
            gc.collision.turn_player(gc.fetch.event_2_string(event))

            # adds new direction to direction list (list of currently held directions)
            gc.updates.direction_list.append(copy.copy(gc.player.direction))

            # tests if player is holding shift
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                gc.world.update_map((gc.player.realcoords[0], gc.player.realcoords[1], gc.player.realcoords[2]))
            else:
                gc.collision.check_collision(gc.player.direction)
                # starts the counter for how long a button has been held down for
                gc.updates.dir_downhold_counter = 1

    elif event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
        # When shift is pressed, stop all movement - like a handbrake
        gc.updates.dir_downhold_counter = 0

    # Place grass tile in front of player
    elif event.key == pygame.K_p and not gc.camera.locked_move:
        gc.actions.place_tile(gc.objects.GrassTile())

    # Place stairs in front of the player
    elif event.key == pygame.K_x and not gc.camera.locked_move:
        gc.actions.place_object(gc.objects.Staircase())

    # Dig a hole in front of the player
    elif event.key == pygame.K_d and not gc.camera.locked_move:
        gc.actions.dig()

    # Remove object in front of player
    elif event.key == pygame.K_SPACE and not gc.camera.locked_move:
        gc.actions.remove_object(False, gc.fetch.find_tile('below viewing').coords)
