# -*- coding: utf-8 -*-

import os
import pygame


class Dialog:
    def __init__(self, game_board):
        self.game_board = game_board
        self.color = (255, 255, 255, 150)
        self.scheme = "white"
        if self.game_board.mainloop.scheme is not None:
            if self.game_board.mainloop.scheme.dark:
                self.scheme = "black"
                self.color = (0, 0, 0, 150)
        """
        if self.game_board.lang.lang in ['en_GB', 'en_US']:
            self.img_src = "congrats.png"
            self.img_src2 = "game_over_en.jpg"
        else:
            self.img_src = "congrats.png"
            self.img_src2 = "game_over.jpg"
        """

        self.img_src = "congrats.png"
        self.img_src2 = "game_over.png"
        self.layout = game_board.layout
        self.layout_update()
        self.level = game_board.level

    def layout_update(self):
        self.color = (255, 255, 255, 150)
        self.scheme = "white"
        if self.game_board.mainloop.scheme is not None:
            if self.game_board.mainloop.scheme.dark:
                self.scheme = "black"
                self.color = (0, 0, 0, 150)
        self.width = self.layout.game_w
        self.height = self.layout.game_h
        self.image = pygame.Surface([self.width, self.height], flags=pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.img = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
        self.img2 = pygame.image.load(os.path.join('res', 'images', self.img_src2)).convert_alpha()

        # img2 has the same size
        img_pos_x = self.img.get_rect(centerx=self.image.get_width() // 2)
        img_pos_y = self.img.get_rect(centery=self.image.get_height() // 2)
        self.img_pos = (img_pos_x[0], img_pos_y[1])

    def update(self, screen):
        self.image.fill(self.color)
        if self.level.dialog_type == 0:
            self.image.blit(self.img, (self.img_pos))

        elif self.level.dialog_type == 1:
            self.image.blit(self.img2, (self.img_pos))

        elif self.level.dialog_type == 2:
            pass
        screen.blit(self.image, (0, 0))
