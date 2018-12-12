"""
Currently a very empty file, this only holds the player's info. In the future this is where health, damage, and other
player attributes will be stored and calculated.
"""

import data.objects


class Player:
    def __init__(self, gameclass):
        self.gc = gameclass
        self.realcoords = [0, 0, 1]
        self.temporary_coords = [0, 0, 1]
        self.movement = None
        self.last_movement = ['up']
        self.last_chunk = (0, 0)
        self.direction = 'up'
        self.sprite = [data.objects.img_player8, data.objects.img_player]
        self.ghost_sprite = [data.objects.img_playeroutline, data.objects.img_playeroutline]
        self.can_pass = False
