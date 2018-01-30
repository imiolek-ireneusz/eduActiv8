# -*- coding: utf-8 -*-

import os
import pygame
from game_boards import game000


class LogoImg(pygame.sprite.Sprite):
    """holds the logo in top left corner - also used as a home category button"""

    def __init__(self, mainloop):
        pygame.sprite.Sprite.__init__(self)
        self.mainloop = mainloop
        self.state = 2
        self.mouse_over = False
        self.image = pygame.Surface([204, 146])
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.img_pos = (0, 0)
        try:
            self.img1 = pygame.image.load(os.path.join('res', 'images', "logo_n.png")).convert()
            self.img2 = pygame.image.load(os.path.join('res', 'images', "logo_h.png")).convert()
            self.img3 = pygame.image.load(os.path.join('res', 'images', "logo_a.png")).convert()
        except:
            pass
        self.update()

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            # check if cursor is not in the top right corner as it would happen on mobile after finger up
            if event.pos[0] + event.pos[1] > 0:
                self.on_mouse_over()
            else:
                self.deselect_all()
                self.mainloop.info.buttons_restore()
                self.mainloop.info.reset_titles()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if not (self.mainloop.m.ldrag or self.mainloop.m.rdrag):
                if self.mainloop.m.active_o is not None:
                    self.mainloop.m.active_o.state = 0
                    self.mainloop.m.active_o = None
                if self.mainloop.m.active_cat_o is not None:
                    self.mainloop.m.active_cat_o.deactivate()
                    self.mainloop.m.active_cat_o = None
                if self.state < 2:
                    self.mainloop.sfx.play(4)
                self.state = 2
                self.mainloop.m.active_cat = 0
                self.mainloop.m.game_constructor = "game000.Board"
                self.mainloop.m.game_variant = 0
                self.mainloop.m.active_game_id = 0
                self.mainloop.m.game_started_id = -1
                self.mainloop.m.tab_game_id = -5
                self.mainloop.m.tab_r_scroll = 0
                self.mainloop.redraw_needed = [True, True, True]

    def on_mouse_over(self):
        if not self.mouse_over:
            self.on_mouse_enter()

    def deselect_all(self):
        if self.mainloop.mouse_over[0] is not None:
            self.mainloop.mouse_over[0].on_mouse_out()
        self.mainloop.mouse_over[0] = self
        if self.mainloop.mouse_over[1] is not None:
            self.mainloop.mouse_over[1].on_mouse_out()
        self.mainloop.mouse_over[1] = None
        if self.mainloop.mouse_over[2] is not None:
            self.mainloop.mouse_over[2].on_mouse_out()
        self.mainloop.mouse_over[2] = None

    def on_mouse_enter(self):
        self.deselect_all()
        if self.state != 2:
            self.state = 1
        self.mouse_over = True
        self.update()
        self.mainloop.redraw_needed[2] = True

    def on_mouse_out(self):
        if self.mouse_over:
            self.mouse_over = False
            if self.state != 2:
                self.state = 0
            self.update()
            self.mainloop.redraw_needed[2] = True

    def update(self):
        img = eval("self.img%i" % (self.state + 1))
        self.image.blit(img, self.img_pos)
