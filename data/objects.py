"""
OBJECTS is storage for images and classes for objects, items, and tiles.
This class should never have any calculations inside.
"""

import pygame
import os.path

# Sprite load
img_player = pygame.image.load(os.path.join('data', 'sprites', 'player.png'))
img_player8 = pygame.image.load(os.path.join('data', 'sprites', 'player8.png'))
img_playeroutline = pygame.image.load(os.path.join('data', 'sprites', 'player_outline.png'))
img_blackersquare = pygame.image.load(os.path.join('data', 'sprites', 'blackersquare.png'))
img_blackestsquare = pygame.image.load(os.path.join('data', 'sprites', 'blackestsquare.png'))
img_mistoverlay = pygame.image.load(os.path.join('data', 'sprites', 'mist.png'))
img_mistsquare = pygame.image.load(os.path.join('data', 'sprites', 'mistsquare.png'))

img_rockwall = pygame.image.load(os.path.join('data', 'sprites', 'rockwall.png'))
img_woodwall = pygame.image.load(os.path.join('data', 'sprites', 'woodwall.png'))
img_spruce = pygame.image.load(os.path.join('data', 'sprites', 'spruce.png'))
img_sprucebottom = pygame.image.load(os.path.join('data', 'sprites', 'spruce_bottom.png'))
img_sprucebottom8 = pygame.image.load(os.path.join('data', 'sprites', 'spruce_bottom8.png'))
img_sprucetop = pygame.image.load(os.path.join('data', 'sprites', 'spruce_top.png'))
img_sprucetop8 = pygame.image.load(os.path.join('data', 'sprites', 'spruce_top8.png'))
img_pinebottom = pygame.image.load(os.path.join('data', 'sprites', 'pine_bottom2.png'))
img_pinebottom8 = pygame.image.load(os.path.join('data', 'sprites', 'pine_bottom28.png'))
img_pinemiddle = pygame.image.load(os.path.join('data', 'sprites', 'pine_middle2.png'))
img_pinemiddle8 = pygame.image.load(os.path.join('data', 'sprites', 'pine_middle28.png'))
img_pinetop = pygame.image.load(os.path.join('data', 'sprites', 'pine_top.png'))
img_pinetop8 = pygame.image.load(os.path.join('data', 'sprites', 'pine_top8.png'))
img_rock = pygame.image.load(os.path.join('data', 'sprites', 'rock.png'))
img_rock8 = pygame.image.load(os.path.join('data', 'sprites', 'rock8.png'))
img_bush = pygame.image.load(os.path.join('data', 'sprites', 'bush.png'))
img_bush8 = pygame.image.load(os.path.join('data', 'sprites', 'bush8.png'))
img_berrybush = pygame.image.load(os.path.join('data', 'sprites', 'berrybush.png'))
img_berrybush8 = pygame.image.load(os.path.join('data', 'sprites', 'berrybush8.png'))
img_bigrock = pygame.image.load(os.path.join('data', 'sprites', 'bigrock.png'))
img_bigrock8 = pygame.image.load(os.path.join('data', 'sprites', 'bigrock8.png'))
img_grass = pygame.image.load(os.path.join('data', 'sprites', 'grass.png'))
img_grass8 = pygame.image.load(os.path.join('data', 'sprites', 'grass8.png'))
img_darkgrass = pygame.image.load(os.path.join('data', 'sprites', 'darkgrass.png'))
img_darkgrass8 = pygame.image.load(os.path.join('data', 'sprites', 'darkgrass8.png'))
img_road = pygame.image.load(os.path.join('data', 'sprites', 'road.png'))
img_planks = pygame.image.load(os.path.join('data', 'sprites', 'planks.png'))
img_stairs = pygame.image.load(os.path.join('data', 'sprites', 'stairs.png'))
img_stairsvertical = pygame.image.load(os.path.join('data', 'sprites', 'stairs_vertical.png'))

# Object info:
# Layer 1 (0): things on the ground that can be passed through, but doesn't cover the player (carpets, flooring)
# Layer 2 (1): things on the ground that can't be passed through (player, solid tiles)
# Layer 3 (2): things on the ground that can be passed through, that do cover the player (tall grass, flowers)
# Layer 4 (3): things 1 block off the ground (spruce top, pine middle)
# Layer 5 (4): things 2 blocks off the ground (pine top)


class Chunk:
    def __init__(self, x, y):
        self.coords = x, y
        self.tiles = {}

# Tile classes


class Tile:
    def __init__(self, name, color, passable):
        self.color = color
        self.name = name
        self.object = [None, None, None, None, None]
        self.item = []
        self.passable = passable
        self.passable_through = False
        self.coords = None
        self.visible = True
        self.loaded = 1


class SandTile(Tile):
    def __init__(self):
        Tile.__init__(self, 'sand', (255, 255, 0), True)


class GrassTile(Tile):
    def __init__(self):
        Tile.__init__(self, 'grass', (0, 255, 0), True)


class StoneTile(Tile):
    def __init__(self):
        Tile.__init__(self, 'stone', (80, 80, 80), True)


class BedrockTile(Tile):
    def __init__(self):
        Tile.__init__(self, 'bedrock', (20, 20, 20), True)


class DirtTile(Tile):
    def __init__(self):
        Tile.__init__(self, 'dirt', (100, 50, 0), True)


class WaterTile(Tile):
    def __init__(self):
        Tile.__init__(self, 'water', (0, 0, 255), False)
        self.passable_through = True


class AirTile(Tile):
    def __init__(self):
        Tile.__init__(self, 'air', None, False)
        self.passable_through = True


# Object classes


class Object:
    def __init__(self, name, sprite, passable, layer):
        self.name = name
        self.sprite = sprite
        self.passable = passable
        self.layer = layer
        self.connected = None
        self.block_sides = None
        self.vertical_sprite = None
        self.direction = None


class SpruceTop(Object):
    def __init__(self):
        Object.__init__(self, 'spruce top', (img_sprucetop8, img_sprucetop), True, 3)


class SpruceBottom(Object):
    def __init__(self):
        Object.__init__(self, 'spruce bottom', (img_sprucebottom8, img_sprucebottom), False, 2)
        self.connected = [(SpruceTop(), (0, -1))]


class PineMiddle(Object):
    def __init__(self):
        Object.__init__(self, 'pine middle', (img_pinemiddle8, img_pinemiddle), True, 3)


class PineTop(Object):
    def __init__(self):
        Object.__init__(self, 'pine top', (img_pinetop8, img_pinetop), True, 4)


class PineBottom(Object):
    def __init__(self):
        Object.__init__(self, 'pine bottom', (img_pinebottom8, img_pinebottom), False, 2)
        self.connected = [(PineMiddle(), (0, -1)), (PineTop(), (0, -2))]


class Rock(Object):
    def __init__(self):
        Object.__init__(self, 'rock', (img_rock8, img_rock), False, 2)


class BigRock(Object):
    def __init__(self):
        Object.__init__(self, 'big rock', (img_bigrock8, img_bigrock), False, 2)


class Bush(Object):
    def __init__(self):
        Object.__init__(self, 'bush', (img_bush8, img_bush), False, 2)


class BerryBush(Bush):
    def __init__(self):
        Bush.__init__(self)
        self.name = 'berry bush'
        self.sprite = (img_berrybush8, img_berrybush)


class TallGrass(Object):
    def __init__(self):
        Object.__init__(self, 'tall grass', (img_grass8, img_grass), True, 1)


class DarkTallGrass(TallGrass):
    def __init__(self):
        TallGrass.__init__(self)
        self.sprite = (img_darkgrass8, img_darkgrass)


class TestObject(Object):
    def __init__(self):
        Object.__init__(self, 'test', (img_player8, img_player), False, 4)


class WoodWall(Object):
    def __init__(self):
        Object.__init__(self, 'wood wall', (img_woodwall, img_woodwall), False, 2)


class RockWall(Object):
    def __init__(self):
        Object.__init__(self, 'rock wall', (img_rockwall, img_rockwall), False, 2)


class Planks(Object):
    def __init__(self):
        Object.__init__(self, 'planks', (img_planks, img_planks), True, 0)


class Road(Object):
    def __init__(self):
        Object.__init__(self, 'road', (img_road, img_road), True, 0)


class Staircase(Object):
    def __init__(self):
        Object.__init__(self, 'staircase', (img_stairs, img_stairs), True, 2)
        self.sprite = (img_stairs, img_stairs)
        self.vertical_sprite = (img_stairsvertical, img_stairsvertical)
        self.block_sides = ' x ' \
                           'osb' \
                           ' x '
        self.direction = 'right'



        '''# Reset xcount and ycount for object displaying
        if self.local_update is None:
            xcount = 0
            ycount = 0
        else:
            xcount = local_x - cornerx - square_rad
            ycount = local_y - cornery - square_rad'''



        '''# Some crazy stuff happens if the right and bottom edge aren't messed with here - DON'T TOUCH!
        if player.movement is not None:
            if player.movement == 'right':
                xcount = self.tiles_on_screenx-1
            elif player.movement == 'down':
                # Originally it was camera.tiles_on_screeny-1, but if you subtract 2 more, and subtract 2 from
                # movementrange_y, you get to update 2 tiles from the bottom each time you go down. Which is great for
                # when trees are being loaded the "wrong" way in.
                if self.new_tile_made:
                    ycount = self.tiles_on_screeny-3
                    movementrange_y[0] -= 2
                else:
                    ycount = self.tiles_on_screeny-1
            player.movement = None
            print('huh')'''


'''def player_update(self, new_display):
        """
        Draws the player as well as the tile(s) the player was previously at (to remove the previous player sprite).
        """
        #f = self.gc.fetch
        #p = self.gc.player
#
        #update_tiles = [[0, 0]]
        #for coord in p.last_movement:
        #    update_tiles.append([f.dir_2_change(f.opposite_cardinal(coord))[0] + update_tiles[-1][0],
        #                         f.dir_2_change(f.opposite_cardinal(coord))[1] + update_tiles[-1][1]])
        #update_tiles = [[0, 0]]
#
        #for n in update_tiles:
        #    xcount = self.tiles_on_screenx // 2 + n[0]
        #    ycount = self.tiles_on_screeny // 2 + n[1]
        #    x, y = self.gc.player.realcoords[0] + n[0], self.gc.player.realcoords[1] + n[1]
        #    topz = f.top_z(x, y)
#
        #    if n == [0, 0]:
        #        self.draw_player(new_display, xcount, ycount)
        #        print('dddddddddddd')
        #    else:
        #        self.draw_tiles(new_display, x, y, topz, xcount, ycount)

        # this replaces all the above text and was in the for-loop - might be dangerous we'll see
        self.draw_player(new_display, self.tiles_on_screenx // 2, self.tiles_on_screeny // 2)
        print('player sprite has been redrawn')

        # Draw the objects

        x, y = self.gc.player.realcoords[0], self.gc.player.realcoords[1]

        self.find_objects(new_display, self.created_tiles[self.gc.fetch.crd_2_str((x, y, self.gc.fetch.top_z(x, y)))],
                          x, y, self.tiles_on_screenx // 2, self.tiles_on_screeny // 2, self.gc.camera.sprite_res())

        # self.force_player_draw = False'''






'''house_1 = ['wwww',
           'wppw',
           'wppw',
           'wwww']

house_2 = ['wwwwwww',
           'wpppppw',
           'wpppppw',
           'wpppppw',
           'wpppppw',
           'wpppppw',
           'wwwwwww']

house_3 = ['wwwwwwwww',
           'wpppppppw',
           'wpppppppw',
           'wpppppppw',
           'wpppwwwww',
           'wpppw',
           'wpppw',
           'wpppw',
           'wwwww']

house_4 = ['wwww',
           'wppw',
           'wppw',
           'wppw',
           'wppw',
           'wppw',
           'wppw',
           'wppw',
           'wppw',
           'wwww']

house_list = [house_1,house_2,house_3,house_4]'''



'''
def direction_turner(direction, turns):
    # Finds out what direction something will face if turned 90 degrees clockwise a certain amount of times
    # - used in calculating entranceways of placed staircases

    dir_list = ['right', 'down', 'left', 'up']
    num = turns + dir_list.index(direction)
    if num > 3:
        num -= 4
    return dir_list[num]
'''


'''def make_town(x, y):
    xc = x
    yc = y
    z = 0
    # Y subtracted by 3 because the 40x40 area starts 3 tiles up from the origin tile
    yn = y-3
    camera.town_gen = (xc, yc)
    make_map()
    if not camera.town_stop:
        if player.direction == 'up':

            road_length = random.randint(5, 20)
            for n in range(road_length):
                if worldchange.created_tiles[crd_2_str((x, yn-n, z))].passable:
                    if worldchange.created_tiles[crd_2_str((x, yn-n, z))].object[1][1] is not None \
                            or worldchange.created_tiles[crd_2_str((x , yn-n, z))].object[2][1] is not None:
                        remove_object(True, (x, yn-n, z))

                    worldchange.created_tiles[crd_2_str((x, yn-n, z))].object[0][1] = road
                else:
                    break

            house_chance = random.randint(0, 3)
            #if house_chance == 0:
            house = house_list[random.randint(1,len(house_list))-1]
            nxplus = len(max(house, key=len)) * -1

            nx = 0 + nxplus
            ny = 0
            breaking = False
            for tier in house:
                for block in tier:
                    if worldchange.created_tiles[crd_2_str((x + nx, ny+yn-len(house)-road_length//2, z))].passable is False:
                        breaking = True
                        break

                    if worldchange.created_tiles[crd_2_str((x + nx, ny+yn-len(house)-road_length//2, z))].object[1][1] is not None \
                            or worldchange.created_tiles[crd_2_str((x + nx, ny+yn-len(house)-road_length//2, z))].object[2][1] is not None:
                        remove_object(True, (x+nx, ny+yn-len(house)-road_length//2, z))

                    worldchange.created_tiles[crd_2_str((x + nx, ny+yn-len(house)-road_length//2, z))].object[1][1] =\
                        structure_objects(block)
                    nx += 1
                    if nx == len(tier) + nxplus:
                        nx = 0 + nxplus
                ny += 1
                if breaking:
                    break

            # House gen
            nx = 0
            ny = 0
            house = house_list[random.randint(1,len(house_list))-1]

            for tier in house:
                for block in tier:
                    if worldchange.created_tiles[crd_2_str((x + nx, yn + ny-len(house), z))].object[1][1] is not None \
                            or worldchange.created_tiles[crd_2_str((x + nx, yn + ny-len(house), z))].object[0][1] is not None:
                        remove_object((x+nx, yn + ny-len(house), z))
                    worldchange.created_tiles[crd_2_str((x + nx, yn + ny-len(house), z))].object[1][1] =\
                        structure_objects(block)
                    nx += 1
                    if nx == len(tier):
                        nx = 0
                ny += 1

    camera.town_gen = None
    camera.town_stop = False
'''