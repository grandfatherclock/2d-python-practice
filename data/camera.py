"""
This class contains the Camera class which takes the display made in the world gen and properly scales it to be blitted
to the screen.
"""

import pygame


class Camera:

    def __init__(self, gameclass):

        self.gc = gameclass

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.legend_display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.active_map_display = None

        # Zoom can be 128, 64, 32, 16, or 8, with 8 being furthest away from the camera
        self.zoom = 32
        # Scale can only be 8 or 16. 8 is for when the map is all zoomed out (so items aren't shown in 16 res)
        self.scale = 16
        self.chunk_size = 16
        self.chunk_sky_height = 11
        self.chunk_ground_depth = -10
        self.top_layer = 1
        self.locked_move = False

        self.previous_tile = 'air'
        self.status_surface = None
        self.screen_update = False

        # Fonts
        self.font = pygame.font.SysFont("courier", 18)
        self.fontsmall = pygame.font.SysFont("courier", 12)

    def camera_change(self):
        """
        This function is activated each time the camera moves up or down BY W OR S (NOT by stairs or autoshift)
        It checks whether the player is able to move. The player can't move when the camera isn't on the player layer.
        """
        if self.gc.player.realcoords[2] == self.top_layer:
            self.locked_move = False
        else:
            self.locked_move = True
        self.gc.updates.dir_downhold_counter = 0

    def sprite_res(self):
        """
        1 if zoom level is furthest away, 0 at any other zoom level
        """
        return self.scale//8 - 1

    def print_screen(self):
        """
        Prints the active display to the screen after zooming.
        """

        pygame.display.set_caption('Cozy Cave (%d FPS)' % self.gc.clock.get_fps())

        if self.screen_update or self.gc.world.first:
            self.screen.fill((20, 20, 20))

            # Zoom to the correct tiles, based on zoom level
            zoom_to_pixels = int(self.scale * self.gc.world.tiles_on_screenx)
            newsurf = pygame.Surface((zoom_to_pixels, zoom_to_pixels))

            if self.zoom == 128:
                newsurf.blit(self.active_map_display, (0, 0), (16*3, (self.scale*2)+16*3, zoom_to_pixels, zoom_to_pixels))
            else:
                newsurf.blit(self.active_map_display, (0, 0), (0, 0, zoom_to_pixels, zoom_to_pixels))

            # Resize everything to fit with zoom level
            newsurf = pygame.transform.scale(newsurf, (newsurf.get_size()[0]*(self.zoom//self.scale),
                                                       newsurf.get_size()[1]*(self.zoom//self.scale)))

            # Print everything on screen
            self.screen.blit(newsurf, (self.SCREEN_WIDTH/2-256, self.SCREEN_HEIGHT/2-256))

            #TEST - CHUNKS
            for chunk in self.gc.world.created_chunks:
                if self.gc.fetch.current_chunk() == chunk:
                    self.screen.fill((200,0,0), (self.chunk_size*chunk[0]+50,self.chunk_size*chunk[1]+100,self.chunk_size,self.chunk_size))

                elif chunk not in self.gc.world.loaded_chunks:
                    self.screen.fill((0,100,0), (self.chunk_size*chunk[0]+50,self.chunk_size*chunk[1]+100,self.chunk_size,self.chunk_size))

                else:
                    self.screen.fill((0,200,0), (self.chunk_size*chunk[0]+50,self.chunk_size*chunk[1]+100,self.chunk_size,self.chunk_size))

            if len(self.gc.updates.chunk_load_list) > 0:
                label1 = self.font.render('loading '+ str(len(self.gc.updates.chunk_load_list))+ ' chunks', 1, (255, 255, 255))
                self.screen.blit(label1, (300, 100))
            if len(self.gc.updates.chunk_delete_list) > 0:
                label1 = self.font.render('saving '+ str(len(self.gc.updates.chunk_delete_list))+ ' chunks', 1, (255, 255, 255))
                self.screen.blit(label1, (100, 100))

            # Debug Text
            label1 = self.font.render('Zoom: x'+str(self.zoom//8), 1, (255, 255, 255))
            self.screen.blit(label1, (25, 25))
            if self.top_layer == self.gc.player.realcoords[2]:
                label1 = self.font.render('Layer View: ' + str(self.top_layer) + ' (Player Layer)', 1, (0, 255, 255))
                self.screen.blit(label1, (self.SCREEN_WIDTH//2 - 130, self.SCREEN_HEIGHT - 50))
            else:
                label1 = self.font.render('Layer View: ' + str(self.top_layer), 1, (255, 255, 255))
                self.screen.blit(label1, (self.SCREEN_WIDTH//2 - 60, self.SCREEN_HEIGHT - 50))
            label1 = self.font.render('[D: Dig down] [X: Place stairs] [P: Place tile]', 1, (100, 100, 100))
            self.screen.blit(label1, (140, 5))
            label1 = self.font.render('[SPACE: Remove object] [S: Layer down] [W: Layer up]', 1, (100, 100, 100))
            self.screen.blit(label1, (140, 20))
            label1 = self.font.render('[C: NoClip] [V: Created tiles] [Z: Zoom] [ENTER: Reset map]', 1, (100, 100, 100))
            self.screen.blit(label1, (140, 35))
            label1 = self.font.render('[SHIFT hold + direction: Turn player]', 1, (100, 100, 100))
            self.screen.blit(label1, (140, 50))

            if self.status_surface is not None:
                self.status_surface = pygame.transform.scale(self.status_surface, (800, 800))
                self.screen.blit(self.status_surface, (0, 0))

            label = self.font.render(str(self.gc.player.realcoords), 1, (255, 255, 255))
            self.screen.blit(label, (0, self.SCREEN_HEIGHT - 50))

            self.legend_display = self.screen
            self.gc.world.first = False
            self.screen_update = False

        # MIGHT BE IMPORTANT, BUT RIGHT NOW IT ONLY SEEMS TO MAKE THE PROGRAM SLOWER
        # else:
        #    self.screen.blit(self.legend_display, (0, 0))
