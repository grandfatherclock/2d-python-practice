"""
The WATER module keeps track of water physics, and finds tiles that need to be updated.
This file is called every 60 frames.
"""


class Water:
    def __init__(self, gameclass):
        self.gc = gameclass
        self.updating_airtiles = []

    def water_flow(self):
        fetch = self.gc.fetch
        append_to_airtiles = []
        remove_from_airtiles = []
        if len(self.updating_airtiles) > 0:

            for air_tile in self.updating_airtiles:

                counter = 0

                # For each air tile that updates all around it, see if there are water tiles around it.
                for dr in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    if self.gc.world.created_tiles.get(fetch.crd_2_str((air_tile[0] + dr[0],
                                                                        air_tile[1] + dr[1],
                                                                        air_tile[2]))) is not None:

                        if self.gc.world.created_tiles[fetch.crd_2_str((air_tile[0] + dr[0],
                                                                        air_tile[1] + dr[1],
                                                                        air_tile[2]))].name == 'water':
                            # If there is an air tile around it, add this tile to be made into water, and see if there
                            # is air tiles around it to be added to the update list.
                            inherit_coords = self.gc.world.created_tiles[fetch.crd_2_str((air_tile[0],
                                                                                          air_tile[1],
                                                                                          air_tile[2]))].coords
                            inherit_objects = self.gc.world.created_tiles[fetch.crd_2_str((air_tile[0],
                                                                                           air_tile[1],
                                                                                           air_tile[2]))].object
                            self.gc.world.created_tiles[fetch.crd_2_str((air_tile[0], air_tile[1], air_tile[2])
                                                                        )] = self.gc.objects.WaterTile()
                            self.gc.world.created_tiles[fetch.crd_2_str((air_tile[0], air_tile[1], air_tile[2])
                                                                        )].object = inherit_objects
                            self.gc.world.created_tiles[fetch.crd_2_str((air_tile[0], air_tile[1], air_tile[2])
                                                                        )].coords = inherit_coords

                            # It's important to add the new watertile to the column since it's in contest for being top
                            self.gc.world.update_column(air_tile[0], air_tile[1], air_tile[2])

                            remove_from_airtiles.append(air_tile)
                            self.gc.world.update_map((1, air_tile[0], air_tile[1], air_tile[2], False))

                            for dr2 in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                                if self.gc.world.created_tiles[fetch.crd_2_str((air_tile[0] + dr2[0],
                                                                                air_tile[1] + dr2[1],
                                                                                air_tile[2]))].name == 'air' and\
                                                                               (air_tile[0] + dr2[0],
                                                                                air_tile[1] + dr2[1],
                                                                                air_tile[2]) not in append_to_airtiles:

                                    # Append any found air tiles to be added to the update list
                                    append_to_airtiles.append((air_tile[0] + dr2[0],
                                                               air_tile[1] + dr2[1],
                                                               air_tile[2]))
                            break
                        else:
                            counter += 1
                            if counter == 4:
                                remove_from_airtiles.append(air_tile)

                    else:
                        counter += 1
                        if counter == 4:
                            remove_from_airtiles.append(air_tile)

            for tile in remove_from_airtiles:
                self.updating_airtiles.remove(tile)

            for tile2 in append_to_airtiles:
                self.updating_airtiles.append(tile2)

