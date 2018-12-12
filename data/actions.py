"""
ACTIONS contains all functions that are relevant when the player does something EXCEPT moving - that is in COLLISION.
"""

import copy


class Actions:
    def __init__(self, gameclass):
        self.gc = gameclass

    def dig(self):
        """
        Digs a hole in front of the player, and removes any item on the removed tile.
        """
        fetch = self.gc.fetch
        remove_tile = None

        # Dig the tile right in front of you on the same layer
        if fetch.find_tile('viewing').name not in ('air', 'water', 'bedrock'):
            remove_tile = fetch.find_tile('viewing')
            # Create the tile below the removing tile (other functions don't work if it doesn't exist)
            fetch.find_tile('below viewing')

        # Dig a hole right in front of you on the layer below
        elif fetch.find_tile('below viewing').name not in ('air', 'water', 'bedrock'):
            remove_tile = fetch.find_tile('below viewing')
            # Create the tile below the removing tile (other functions don't work if it doesn't exist)
            fetch.find_tile('below below viewing')

        if remove_tile is not None:

            # Remove objects on tile that is being digged out
            self.remove_object(True, remove_tile.coords)

            # Save the objects (the ones that weren't directly on the removed tile) and the coords of the old tile
            inherit_objects = remove_tile.object
            inherit_coords = remove_tile.coords

            # Make the old tile into an AirTile
            self.gc.world.created_tiles[self.gc.fetch.crd_2_str(remove_tile.coords)] = self.gc.objects.AirTile()

            # Make the new AirTile inherit the coords of the old tile
            self.gc.world.created_tiles[self.gc.fetch.crd_2_str(remove_tile.coords)].coords = inherit_coords

            # Remove old tile from column list (it's no longer in contest of being top tile since it's now seethrough)
            self.gc.world.tile_columns[self.gc.fetch.crd_2_str((remove_tile.coords[0],
                                                                remove_tile.coords[1])
                                                               )].remove(remove_tile.coords[2])

            # Make the tile below inherit the objects of the old tile (since objects can only be shown on solid tiles)
            topz = self.gc.fetch.top_z(remove_tile.coords[0], remove_tile.coords[1])
            self.gc.world.created_tiles[self.gc.fetch.crd_2_str((remove_tile.coords[0],
                                                                 remove_tile.coords[1],
                                                                 topz))].object = inherit_objects

            # Add these coordinates to be checked for water updates
            self.gc.water.updating_airtiles.append(remove_tile.coords)

            # Update the map
            self.gc.world.update_map((remove_tile.coords[0], remove_tile.coords[1], remove_tile.coords[2]))

    def place_tile(self, tile):
        """
        Places a tile in right front of the player, or in a hole in front of the player.
        """
        fetch = self.gc.fetch
        position = None

        if fetch.find_tile('below viewing').name in ('air', 'water'):
            position = 'below viewing'
        elif fetch.find_tile('viewing').name in ('air', 'water'):
            position = 'viewing'
        else:
            print("Can't place ", tile.name, " here!")

        # position check is to stop game from crashing if object can't be placed
        if position is not None:
            x = fetch.find_tile(position).coords[0]
            y = fetch.find_tile(position).coords[1]
            z = fetch.find_tile(position).coords[2]

            self.remove_object(True, (x, y))
            self.gc.world.created_tiles[fetch.crd_2_str((x, y, z))] = tile
            self.gc.world.created_tiles[fetch.crd_2_str((x, y, z))].coords = (x, y, z)
            self.gc.world.update_column(x, y, z)
            self.gc.world.update_map((x, y, z))

    def place_object(self, obj_class):
        """
        Places an object in front of the player. Only stairs can be placed in a hole in front of the player.
        """
        fetch = self.gc.fetch
        obj = obj_class
        diro = None

        if fetch.find_tile('below viewing').name == 'air':
            tile = fetch.find_tile('below below viewing')
            diro = fetch.opposite_cardinal(self.gc.player.direction)
            opp = True
        elif fetch.find_tile('viewing').name == 'air':
            tile = fetch.find_tile('below viewing')
            diro = self.gc.player.direction
            opp = False
        else:
            print("Can't place ", obj.name, " here!")

        # diro check is to stop game from crashing if object can't be placed
        if diro is not None:
            self.remove_object(True, (tile.coords[0], tile.coords[1]))

            tile.object[2] = copy.copy(obj)
            tile.object[2].direction = diro
            if diro is not obj.direction:
                tile.object[2].block_sides = self.rotate_blocked_sides(tile.object[2].block_sides,
                                                                       obj.direction,
                                                                       self.gc.player.direction, opp)

            self.gc.world.update_map((tile.coords[0], tile.coords[1], tile.coords[2]))

    def rotate_blocked_sides(self, system, startdir, newdir, opposite):
        """
        Rotates the blocked side-list of an object into a new direction. This is only used in this file.
        """
        oldsystem = list(system)
        newsystem = [' ', ' ', ' ',
                     ' ', 's', ' ',
                     ' ', ' ', ' ']
        turns = self.gc.fetch.how_many_turns(startdir, newdir)

        for n in range(turns):
            newsystem[5] = oldsystem[1]
            newsystem[7] = oldsystem[5]
            newsystem[3] = oldsystem[7]
            newsystem[1] = oldsystem[3]
            oldsystem = newsystem.copy()

        if opposite:
            newsystem[1] = oldsystem[7]
            newsystem[7] = oldsystem[1]
            newsystem[5] = oldsystem[3]
            newsystem[3] = oldsystem[5]

        return "".join(newsystem)

    def remove_object(self, remove_all, tilen):
        """
        Removes objects on a given tile - either everything is removed, or 1 item is removed. Also removes connections.
        """
        fetch = self.gc.fetch

        tile_iq = self.gc.world.created_tiles[fetch.crd_2_str((tilen[0], tilen[1], tilen[2]))]

        stop = False
        for n in range(3):
            if tile_iq.object[n] is not None:
                self.gc.world.update_map((tile_iq.coords[0], tile_iq.coords[1], tile_iq.coords[2]))
                # Check for connected objects, and remove those as well
                if tile_iq.object[n].connected is not None:
                    for connected_obj in tile_iq.object[n].connected:
                        # Remove the object, now that we know its x, y, and z coords
                        self.gc.world.created_tiles[fetch.crd_2_str((tile_iq.coords[0] + connected_obj[1][0],
                                                                     tile_iq.coords[1] + connected_obj[1][1],
                                                                     tile_iq.coords[2])
                                                                    )].object[connected_obj[0].layer] = None
                        # Add the tile to the update list
                        self.gc.world.update_map((tile_iq.coords[0] + connected_obj[1][0],
                                                  tile_iq.coords[1] + connected_obj[1][1],
                                                  tile_iq.coords[2]))

                # Remove the original object
                tile_iq.object[n] = None
                # Stop removing stuff if remove_all is False
                if not remove_all:
                    stop = True
            if stop:
                break

    def zoom(self):
        """
        When the player zoom in, this function calculates the new map dimensions
        """
        c = self.gc.camera

        c.zoom *= 2
        c.scale = 16
        if c.zoom > 128:
            c.zoom = 8
            c.scale = 8
        elif c.zoom == 128:
            c.zoom = 64
            self.gc.world.tiles_on_screenx = 640 // c.zoom
            self.gc.world.tiles_on_screeny = (640 // c.zoom) + 2 + 2
            c.zoom = 128
        else:
            self.gc.world.tiles_on_screenx = 640 // c.zoom
            self.gc.world.tiles_on_screeny = (640 // c.zoom) + 2 + 2

        self.gc.world.update_all = True
