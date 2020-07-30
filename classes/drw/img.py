# -*- coding: utf-8 -*-

import pygame


class Img:
    def __init__(self, unit_w, unit_h, scale, img_src, scale_factor=1, bg_color=(0, 0, 0, 0), tint_color=None):
        self.size_w = unit_w * scale
        self.size_h = unit_h * scale
        self.img_src = img_src
        self.w = int(self.size_w * scale_factor)
        self.h = int(self.size_h * scale_factor)
        self.l = (self.size_w - self.w) // 2
        self.t = (self.size_h - self.w) // 2

        self.canvas = pygame.Surface((self.size_w, self.size_h), flags=pygame.SRCALPHA)
        self.canvas.fill(bg_color)

        self.img_org = pygame.image.load(self.img_src).convert_alpha()
        self.img_rect = self.img_org.get_rect()

        self.img = self.scalled_img(self.img_org, self.w, self.h)
        self.img_pos = (self.l, self.t)

        if tint_color is not None:
            self.img = self.get_tinted_img(tint_color)

        self.canvas.blit(self.img, self.img_pos)

    def get_canvas(self):
        return self.canvas

    def scalled_img(self, image, new_w, new_h):
        """scales image depending on pygame version and bit depth using either smoothscale or scale"""
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    def get_tinted_img(self, tint_color):
        tinted_img = self.img.copy()
        tinted_img.fill(tint_color, special_flags=pygame.BLEND_ADD)
        return tinted_img
