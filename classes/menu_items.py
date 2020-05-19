# -*- coding: utf-8 -*-

import os
import pygame
from math import pi, cos, sin, sqrt


class TopCategory(pygame.sprite.Sprite):
    """basic class for all on-board objects"""

    def __init__(self, board, cat_obj, grid_x=0, grid_y=0, grid_w=1, grid_h=1, item_id="", color=(0, 0, 0, 0),
                 img_src='', decor=0, sequence_id=0):
        pygame.sprite.Sprite.__init__(self)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.item_id = item_id
        self.board = board
        self.cat_obj = cat_obj
        self.sequence_id = sequence_id
        self.bg_style = self.board.mainloop.cl.menu_shapes[self.board.mainloop.cl.color_sliders[6][2]]
        self.decor_style = decor
        self.double_icon = False

        self.color = color
        self.update_me = True
        self.hover = False

        self.image = pygame.Surface((grid_w * board.scale - 1, grid_h * board.scale - 1))
        self.rect = self.image.get_rect()
        self.rect.topleft = [grid_x * board.scale + 1, grid_y * board.scale + 1]

        self.change_image(img_src)
        self.update()

    def set_styles(self, bg_style, decor_style):
        self.bg_style = bg_style
        self.decor_style = decor_style

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.update_me = True
            self.img = self.image
            self.img_pos = (0, 0)

            if self.sequence_id > 0:
                prev = self.board.units[-1]
            else:
                prev = None

            try:
                self.img1_org = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert_alpha()
                self.img1_rect = self.img1_org.get_rect()
                inner_w = int(self.rect.w * 0.8)
                self.img1 = self.scaled_img(self.img1_org, inner_w, inner_w)
                self.img1.fill(self.board.mainloop.cl.c_fg_tint_color, special_flags=pygame.BLEND_ADD)
                self.img1_rect = self.img1.get_rect()
                pos_x = ((self.board.scale * self.grid_w - inner_w) // 2)
                pos_y = ((self.board.scale * self.grid_h - inner_w) // 2)
                self.img1_pos = (pos_x, pos_y)

            except:
                pass

            if prev is None:
                try:
                    self.img2_org = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_c_bg.png")).convert_alpha()
                    self.img2_org_h = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_c_bg_h.png")).convert_alpha()
                    if self.decor_style == 1:
                        self.img2_org_decor = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_c_decor.png")).convert_alpha()
                        self.img2d = self.scaled_img(self.img2_org_decor, self.rect.w, self.rect.h)
                    self.img2 = self.scaled_img(self.img2_org, self.rect.w, self.rect.h)
                    self.img2h = self.scaled_img(self.img2_org_h, self.rect.w, self.rect.h)
                    self.img2.fill(self.board.mainloop.cl.c_bg_tint_color, special_flags=pygame.BLEND_ADD)
                    self.img2h.fill(self.board.mainloop.cl.c_bg_tint_color, special_flags=pygame.BLEND_ADD)

                except:
                    pass
            else:
                self.img2 = prev.img2
                self.img2h = prev.img2h
                if self.decor_style == 1:
                    self.img2d = prev.img2d

            self.img2_rect = self.img2.get_rect()
            pos2_x = ((self.board.scale * self.grid_w - self.img2_rect.w) // 2)
            pos2_y = ((self.board.scale * self.grid_h - self.img2_rect.h) // 2)
            self.img2_pos = (pos2_x, pos2_y)


    def resize_unit(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h
        self.image = pygame.Surface((self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1))
        self.image.fill(self.color)

    def pos_update(self):
        if self.grid_w > 0 and self.grid_h > 0:
            self.image = pygame.Surface((self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]
        else:
            self.image = pygame.Surface((1, 1))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

    def scaled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    @property
    def grid_pos(self):
        return [self.grid_x, self.grid_y]

    def set_grid_pos(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_update()

    def set_color(self, color):
        self.color = color

    def set_tint_color(self, color):
        self.tint_color = color

    def update(self, **kwargs):
        if self.update_me:
            self.update_me = False
            self.image.fill(self.color)
            if self.hover:
                self.image.blit(self.img2h, self.img2_pos)
            else:
                self.image.blit(self.img2, self.img2_pos)
            if self.decor_style == 1:
                self.image.blit(self.img2d, self.img2_pos)
            self.image.blit(self.img1, self.img1_pos)
            if self.double_icon:
                self.image.blit(self.img1, self.img1_pos)

    def mouse_out(self):
        self.board.mainloop.m.reset_titles()
        self.hover = False
        self.update_me = True
        self.update()

    def mouse_click(self):
        self.board.mainloop.menu_group = self.item_id + 1
        self.board.mainloop.menu_level = 1
        self.board.mainloop.info.realign()
        self.board.mainloop.m.start_hidden_game(271)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            if not self.hover:
                self.board.mainloop.redraw_needed[1] = True
                self.hover = True
                self.update_me = True
                self.update()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_click()


class Category(pygame.sprite.Sprite):
    """basic class for all on-board objects"""

    def __init__(self, board, cat_obj, grid_x=0, grid_y=0, grid_w=1, grid_h=1, item_id="", color=(0, 0, 0, 0),
                 img_src='', decor=0, sequence_id=0):
        pygame.sprite.Sprite.__init__(self)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.item_id = item_id
        self.sequence_id = sequence_id
        self.board = board
        self.cat_obj = cat_obj
        self.color = color
        self.update_me = True
        self.hover = False
        self.show_titles_on_hover = True

        self.bg_style = self.board.mainloop.cl.menu_shapes[self.board.mainloop.cl.color_sliders[6][2]]
        self.decor_style = decor
        self.double_icon = False

        self.image = pygame.Surface((grid_w * board.scale - 1, grid_h * board.scale - 1))
        self.rect = self.image.get_rect()
        self.rect.topleft = [grid_x * board.scale + 1, grid_y * board.scale + 1]

        self.change_image(img_src)
        self.update()

    def redraw_image(self):
        self.bg_style = self.board.mainloop.cl.menu_shapes[self.board.mainloop.cl.color_sliders[6][2]]
        self.change_image(self.img_src)
        self.update_me = True
        self.update()

    def set_styles(self, bg_style, decor_style):
        self.bg_style = bg_style
        self.decor_style = decor_style

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.update_me = True
            self.img = self.image
            self.img_pos = (0, 0)
            if self.sequence_id > 0:
                prev = self.board.units[-1]
            else:
                prev = None

            try:
                self.img1_org = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert_alpha()
                self.img1_rect = self.img1_org.get_rect()
                inner_w = int(sqrt(pow(self.rect.w / 2, 2) * 2) * 0.8)
                self.img1 = self.scaled_img(self.img1_org, inner_w, inner_w)
                self.img1.fill(self.board.mainloop.cl.c_fg_tint_color, special_flags=pygame.BLEND_ADD)
                self.img1_rect = self.img1.get_rect()
                pos_x = ((self.board.scale * self.grid_w - inner_w) // 2)
                pos_y = ((self.board.scale * self.grid_h - inner_w) // 2)
                self.img1_pos = (pos_x, pos_y)
            except:
                pass

            if prev is None:
                try:
                    self.img2_org = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_c_bg.png")).convert_alpha()
                    self.img2_org_h = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_c_bg_h.png")).convert_alpha()
                    if self.decor_style == 1:
                        self.img2_org_decor = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_c_decor.png")).convert_alpha()
                        self.img2d = self.scaled_img(self.img2_org_decor, self.rect.w, self.rect.h)
                    self.img2 = self.scaled_img(self.img2_org, self.rect.w, self.rect.h)
                    self.img2h = self.scaled_img(self.img2_org_h, self.rect.w, self.rect.h)
                    self.img2.fill(self.board.mainloop.cl.c_bg_tint_color, special_flags=pygame.BLEND_ADD)
                    self.img2h.fill(self.board.mainloop.cl.c_bg_tint_color, special_flags=pygame.BLEND_ADD)
                except:
                    pass
            else:
                self.img2 = prev.img2
                self.img2h = prev.img2h
                if self.decor_style == 1:
                    self.img2d = prev.img2d

            self.img2_rect = self.img2.get_rect()
            pos2_x = ((self.board.scale * self.grid_w - self.img2_rect.w) // 2)
            pos2_y = ((self.board.scale * self.grid_h - self.img2_rect.h) // 2)
            self.img2_pos = (pos2_x, pos2_y)

    def resize_unit(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h
        self.image = pygame.Surface((self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1))
        self.image.fill(self.color)

    def pos_update(self):
        if self.grid_w > 0 and self.grid_h > 0:
            self.image = pygame.Surface((self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]
        else:
            self.image = pygame.Surface((1, 1))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

    def scaled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    @property
    def grid_pos(self):
        return [self.grid_x, self.grid_y]

    def set_grid_pos(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_update()

    def set_color(self, color):
        self.color = color

    def set_tint_color(self, color):
        self.tint_color = color

    def update(self, **kwargs):
        if self.update_me:
            self.update_me = False
            self.board.mainloop.redraw_needed[0] = True
            self.image.fill(self.color)
            if self.hover:
                self.image.blit(self.img2h, self.img2_pos)
            else:
                self.image.blit(self.img2, self.img2_pos)
            if self.decor_style == 1:
                self.image.blit(self.img2d, self.img2_pos)
            self.image.blit(self.img1, self.img1_pos)
            if self.double_icon:
                self.image.blit(self.img1, self.img1_pos)

    def mouse_out(self):
        if self.show_titles_on_hover:
            self.board.mainloop.m.reset_titles()
        self.hover = False
        self.update_me = True
        self.update()

    def mouse_click(self):
        a = []
        if self.board.mainloop.menu_level == 1:
            if self.board.mainloop.m.categories_dict[self.item_id].has_inner:
                self.board.mainloop.m.current_inner = True
                self.board.mainloop.menu_inner_cat = self.item_id + 1
                self.board.mainloop.menu_level = 2
            else:
                self.board.mainloop.m.current_inner = False
                self.board.mainloop.menu_category = self.item_id + 1
                self.board.mainloop.menu_level = 3

            self.board.mainloop.m.change_cat(self.item_id)
        elif self.board.mainloop.menu_level == 2:
            self.board.mainloop.m.current_inner = True
            self.board.mainloop.menu_level = 3
            self.board.mainloop.menu_category = self.item_id + 1
            self.board.mainloop.m.change_cat(self.item_id)

        if self.board.mainloop.m.game_dbid == 271:
            self.board.mainloop.m.start_hidden_game(272)
        else:
            self.board.mainloop.m.start_hidden_game(271)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            if not self.hover:
                if self.show_titles_on_hover:
                    self.board.mainloop.redraw_needed[1] = True
                    self.board.mainloop.info.title = self.cat_obj.title
                    self.board.mainloop.info.subtitle = self.cat_obj.subtitle
                    self.board.mainloop.info.game_id = "#%03i" % self.cat_obj.cat_id
                self.hover = True
                self.update_me = True
                self.update()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_click()


class GameIcon(pygame.sprite.Sprite):
    """basic class for all on-board objects"""

    def __init__(self, board, game_obj, grid_x=0, grid_y=0, grid_w=1, grid_h=1, color=(0, 0, 0, 0),
                 lvl_count=None, completions=None, img_src=None, decor=0, sequence_id=0):
        pygame.sprite.Sprite.__init__(self)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.game_obj = game_obj
        self.item_id = game_obj.dbgameid
        self.sequence_id = sequence_id
        if img_src is None:
            self.img_src = game_obj.img_src
        else:
            self.img_src = img_src
        self.completions = completions
        self.level_count = lvl_count
        self.board = board
        self.challenge_completed = False
        if self.completions is not None:
            if self.completions and 0 not in self.completions:
                self.challenge_completed = True

        self.color = color
        self.lvl_not_compl_col = self.board.mainloop.cl.lvl_not_compl_col

        if self.board.mainloop.scheme is not None:
            self.canvas_color = self.board.mainloop.scheme.u_color
            if self.board.mainloop.scheme.dark:
                self.lvl_not_compl_col = self.board.mainloop.cl.lvl_not_compl_col_dark
        else:
            self.canvas_color = (255, 255, 255)

        self.lvl_completed_col = self.board.mainloop.cl.lvl_completed_col

        self.update_me = True
        self.hover = False
        self.show_titles_on_hover = True
        self.size = 256

        if self.game_obj.img_src2 == "":
            self.challenge = True
        else:
            self.challenge = False

        #add object to the dictionary to reuse its images
        if self.board.template_units is not None:
            if self.challenge and not self.challenge_completed and self.board.template_units[0] is None:
                self.board.template_units[0] = self
            elif self.challenge and self.challenge_completed and self.board.template_units[1] is None:
                self.board.template_units[1] = self
            elif not self.challenge and self.board.template_units[2] is None:
                self.board.template_units[2] = self

        self.bg_style = "game_bg"
        self.decor_style = decor
        self.double_icon = False

        self.image = pygame.Surface((grid_w * board.scale - 1, grid_h * board.scale - 1))
        self.rect = self.image.get_rect()
        self.rect.topleft = [grid_x * board.scale + 1, grid_y * board.scale + 1]

        if self.challenge and not self.challenge_completed:
            self.canvas = pygame.Surface((self.size, self.size))
            self.canvas.fill(self.canvas_color)
            self.draw_levels()
            self.canvas2 = self.scaled_img(self.canvas, self.rect.w, self.rect.h)

        self.change_image(self.img_src)
        self.update()

    def redraw_image(self):
        self.lvl_not_compl_col = self.board.mainloop.cl.lvl_not_compl_col

        if self.board.mainloop.scheme is not None:
            self.canvas_color = self.board.mainloop.scheme.u_color
            if self.board.mainloop.scheme.dark:
                self.lvl_not_compl_col = self.board.mainloop.cl.lvl_not_compl_col_dark
        self.lvl_completed_col = self.board.mainloop.cl.lvl_completed_col

        self.image = pygame.Surface((self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

        if self.challenge and not self.challenge_completed:  # not completed
            self.canvas = pygame.Surface((self.size, self.size))
            self.canvas.fill(self.canvas_color)
            self.draw_levels()
            self.canvas2 = self.scaled_img(self.canvas, self.rect.w, self.rect.h)

        self.change_image(self.img_src)
        self.update_me = True
        self.update()

    def set_styles(self, bg_style, decor_style):
        self.bg_style = bg_style
        self.decor_style = decor_style

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.update_me = True
            self.img = self.image
            self.img_pos = (0, 0)
            if self.sequence_id > 0:
                prev2 = self.board.units[-1]
            else:
                prev2 = None
            if self.board.template_units is not None:
                if self.challenge and not self.challenge_completed and self.board.template_units[0] is not None \
                        and self.board.template_units[0] != self:
                    prev3 = self.board.template_units[0]
                elif self.challenge and self.challenge_completed and self.board.template_units[1] is not None \
                        and self.board.template_units[1] != self:
                    prev3 = self.board.template_units[1]
                elif not self.challenge and self.board.template_units[2] is not None \
                        and self.board.template_units[2] != self:
                    prev3 = self.board.template_units[2]
                else:
                    prev3 = None
            else:
                prev3 = None

            try:
                self.img1_org = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert_alpha()
                self.img1_rect = self.img1_org.get_rect()
                self.img1 = self.scaled_img(self.img1_org, self.rect.w // 2, self.rect.h // 2)
                self.img1.fill(self.board.mainloop.cl.g_fg_tint_color, special_flags=pygame.BLEND_ADD)
                self.img1_rect = self.img1.get_rect()
                pos_x = ((self.board.scale * self.grid_w - self.img1_rect.w) // 2)
                pos_y = ((self.board.scale * self.grid_h - self.img1_rect.h) // 2)
                self.img1_pos = (pos_x, pos_y)
            except:
                pass

            if prev2 is None:
                try:
                    self.img2_org = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_bg_n.png")).convert_alpha()
                    self.img2_org_h = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_bg_h.png")).convert_alpha()
                    if self.decor_style == 1:
                        self.img2_org_decor = pygame.image.load(os.path.join('res', 'icons', "schemes", self.bg_style, "menu_bg_decor.png")).convert_alpha()
                    self.img2 = self.scaled_img(self.img2_org, self.rect.w, self.rect.h)
                    self.img2h = self.scaled_img(self.img2_org_h, self.rect.w, self.rect.h)
                    if self.decor_style == 1:
                        self.img2d = self.scaled_img(self.img2_org_decor, self.rect.w, self.rect.h)
                    self.img2.fill(self.board.mainloop.cl.g_bg_tint_color, special_flags=pygame.BLEND_ADD)
                    self.img2h.fill(self.board.mainloop.cl.g_bg_tint_color, special_flags=pygame.BLEND_ADD)
                except:
                    pass
            else:
                self.img2 = prev2.img2
                if self.decor_style == 1:
                    self.img2d = prev2.img2d
                self.img2h = prev2.img2h
            self.img2_rect = self.img2.get_rect()
            pos2_x = ((self.board.scale * self.grid_w - self.img2_rect.w) // 2)
            pos2_y = ((self.board.scale * self.grid_h - self.img2_rect.h) // 2)
            self.img2_pos = (pos2_x, pos2_y)

            if prev3 is None:
                try:
                    if not self.challenge:
                        self.img3_org = pygame.image.load(os.path.join('res', 'icons', "menu_ring_demo_n.png")).convert_alpha()
                        self.img3_org_h = pygame.image.load(os.path.join('res', 'icons', "menu_ring_demo_h.png")).convert_alpha()
                        self.img3 = self.scaled_img(self.img3_org, self.rect.w, self.rect.h)
                        self.img3h = self.scaled_img(self.img3_org_h, self.rect.w, self.rect.h)
                        self.img3_org_d = pygame.image.load(os.path.join('res', 'icons', "menu_ring_demo_decor.png")).convert_alpha()
                        self.img3d = self.scaled_img(self.img3_org_d, self.rect.w, self.rect.h)
                    elif self.challenge_completed:
                        self.img3_org = pygame.image.load(os.path.join('res', 'icons', "menu_ring_comp_n.png")).convert_alpha()
                        self.img3_org_h = pygame.image.load(
                            os.path.join('res', 'icons', "menu_ring_comp_h.png")).convert_alpha()
                        self.img3 = self.scaled_img(self.img3_org, self.rect.w, self.rect.h)
                        self.img3h = self.scaled_img(self.img3_org_h, self.rect.w, self.rect.h)
                        self.img3_org_d = pygame.image.load(
                            os.path.join('res', 'icons', "menu_ring_comp_decor.png")).convert_alpha()
                        self.img3d = self.scaled_img(self.img3_org_d, self.rect.w, self.rect.h)
                    else:
                        self.img3_org = pygame.image.load(os.path.join('res', 'icons', "menu_ring_03.png")).convert_alpha()
                        self.img3_org_h = pygame.image.load(
                            os.path.join('res', 'icons', "menu_ring_03h.png")).convert_alpha()
                        self.img3 = self.scaled_img(self.img3_org, self.rect.w, self.rect.h)
                        self.img3h = self.scaled_img(self.img3_org_h, self.rect.w, self.rect.h)
                        self.img3d = None
                    if self.img3d is not None:
                        self.img3.fill(self.lvl_completed_col, special_flags=pygame.BLEND_ADD)
                        self.img3h.fill(self.lvl_completed_col, special_flags=pygame.BLEND_ADD)
                except:
                    pass
            else:
                self.img3 = prev3.img3
                self.img3h = prev3.img3h
                self.img3d = prev3.img3d

    def resize_unit(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h
        self.image = pygame.Surface((self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1), flags=pygame.SRCALPHA)
        self.image.fill(self.color)

    def pos_update(self):
        if self.grid_w > 0 and self.grid_h > 0:
            self.image = pygame.Surface((self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]
        else:
            self.image = pygame.Surface((1, 1))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

    def scaled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    @property
    def grid_pos(self):
        return [self.grid_x, self.grid_y]

    def set_grid_pos(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_update()

    def set_color(self, color):
        self.color = color

    def set_tint_color(self, color):
        self.tint_color = color

    def draw_levels(self):
        r = 127
        r2 = r * 0.78
        m = (self.size - r * 2) // 2
        cx = m + r
        cy = m + r
        if self.level_count is not None:
            levels = self.level_count[1]
            padding = 4
            w = ((360.0 - (levels * padding)) / levels)
            for i in range(levels):
                a = (i * w + i * padding + 2 - 90) % 360
                b = ((i + 1) * w + (i) * padding + 2 - 90) % 360
                if a > b:
                    b += 360
                p = []
                p2 = []
                for n in range(int(a), int(b)+1):
                    x = cx + int(round(r * cos(n * pi / 180)))
                    y = cy + int(round(r * sin(n * pi / 180)))
                    p.append((x, y))

                    x = cx + int(round(r2 * cos(n * pi / 180)))
                    y = cy + int(round(r2 * sin(n * pi / 180)))
                    p2.append((x, y))
                p.extend(reversed(p2))
                p.append(p[0])
                if self.completions is not None:
                    if self.completions[i] > 0:
                        pygame.draw.polygon(self.canvas, self.lvl_completed_col, p, 0)
                    else:
                        pygame.draw.polygon(self.canvas, self.lvl_not_compl_col, p, 0)

    def update(self, **kwargs):
        if self.update_me:
            self.update_me = False
            self.board.mainloop.redraw_needed[0] = True
            self.image.fill(self.color)
            if self.challenge and not self.challenge_completed:
                self.image.blit(self.canvas2, self.img2_pos)
            if self.hover:
                self.image.blit(self.img2h, self.img2_pos)
            else:
                self.image.blit(self.img2, self.img2_pos)
            if self.decor_style == 1:
                self.image.blit(self.img2d, self.img2_pos)
            self.image.blit(self.img1, self.img1_pos)
            if self.double_icon:
                self.image.blit(self.img1, self.img1_pos)
            if self.hover:
                self.image.blit(self.img3h, self.img2_pos)
            else:
                self.image.blit(self.img3, self.img2_pos)
            if self.img3d is not None:
                self.image.blit(self.img3d, self.img2_pos)

    def mouse_out(self):
        if self.show_titles_on_hover:
            self.board.mainloop.m.reset_titles()
        self.update_me = True
        self.hover = False
        self.update()

    def mouse_click(self):
        self.board.mainloop.menu_level = 4
        self.board.mainloop.completions = self.completions
        self.board.mainloop.m.start_hidden_game(self.item_id)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            if not self.hover:
                self.hover = True
                if self.show_titles_on_hover:
                    self.board.mainloop.redraw_needed[1] = True
                    self.board.mainloop.info.title = self.game_obj.title
                    self.board.mainloop.info.subtitle = self.game_obj.subtitle
                    self.board.mainloop.info.game_id = "#%s/%03i" % (self.game_obj.game_constructor[4:7], self.game_obj.dbgameid)
                self.update_me = True
                self.update()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_click()
