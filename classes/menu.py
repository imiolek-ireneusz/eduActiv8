# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import pygame
import ast

import time

import classes.extras as ex

"""
# games no longer imported on the start of the game but instead when the activity is selected to run
from game_boards import game000, game001, game002, game003, game004, game005, game006, game007, game008, game009, \
    game010, game011, game012, game013, game014, game015, game016, game017, game018, game019, game020, game021, game022, \
    game023, game024, game025, game026, game027, game028, game029, game031, game032, game033, game034, game035, \
    game036, game037, game038, game039, game041, game042, game043, game044, game045, game046, game047, \
    game049, game050, game051, game052, game053, game054, game055, game056, game059, game060, game061, game062, \
    game063, game064, game065, game066, game067, game068, game069, game070, game071, game072, game073, game074, \
    game075, game076, game077, game078, game079, game080, game081, game082, game083, game084, game085, game087, \
    game088, game089, game090, game091, game092, game093

#games currently not used
#game030, game040, game048, game057, game058, game083 - to keep 30, 48, 57, 58
#
#
# 40, 83, 86, 91,
"""

class MenuCategoryGroup(pygame.sprite.Sprite):
    def __init__(self, menu, unit_id, title, subtitle, w, h, img_src1):
        pygame.sprite.Sprite.__init__(self)

        self.selected = False
        self.state = 0  # 0 - normal, 1 - hover, 2 - selected
        self.categories = []
        self.initial_h = h
        self.mouse_dn = False
        self.alpha_value = 200

        self.menu = menu
        self.unit_id = unit_id
        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)
        self.w = w
        self.h = h

        # top and bottom used to detect clicks for collapsing a group
        self.t = 0
        self.b = 0
        self.th = 78
        self.bh = 40

        self.selected = False
        self.animating = False
        self.mouse_over = False

        self.image = pygame.Surface([w, h])
        self.image.set_colorkey((0, 0, 0))
        self.image.set_alpha(self.alpha_value)
        self.img = self.image
        self.img_pos = (0, 0)

        try:
            # module image - top
            self.img1 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', img_src1)).convert()
            self.img1.set_colorkey((255, 255, 255))

            # module images bottom
            self.img2 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', self.menu.cat_img_src2)).convert()
            self.img2.set_colorkey((255, 255, 255))
            self.img3 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', self.menu.cat_img_src3)).convert()
            self.img3.set_colorkey((255, 255, 255))
            self.img4 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', self.menu.cat_img_src4)).convert()
            self.img4.set_colorkey((255, 255, 255))

            # image top highlights
            self.img5 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', self.menu.cat_img_src5)).convert()
            self.img5.set_colorkey((255, 255, 255))
            self.img6 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', self.menu.cat_img_src6)).convert()
            self.img6.set_colorkey((255, 255, 255))

            # category background image
            self.img7 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', self.menu.cat_img_src7)).convert()
        except:
            pass

        self.rect = self.image.get_rect()

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            found = False
            if self.selected:
                for each in self.categories:
                    # if each.rect.topleft[0]+self.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0]+self.rect.topleft[0] and each.rect.topleft[1]+self.rect.topleft[1] + each.rect.height >= pos[1] >= each.rect.topleft[1]+self.rect.topleft[1]:
                    if each.rect.topleft[0] + self.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] + \
                            self.rect.topleft[0] and each.rect.topleft[1] + self.rect.topleft[1] + each.rect.height >= \
                            pos[1] >= each.rect.topleft[1] + self.rect.topleft[1]:
                        each.handle(event)
                        self.mouse_dn = False
            if not found:
                self.mouse_dn = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = event.pos
            found = False
            if self.selected:
                for each in self.categories:
                    # if each.rect.topleft[0]+self.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0]+self.rect.topleft[0] and each.rect.topleft[1]+self.rect.topleft[1] + each.rect.height >= pos[1] >= each.rect.topleft[1]+self.rect.topleft[1]:
                    if each.rect.topleft[0] + self.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] + \
                            self.rect.topleft[0] and each.rect.topleft[1] + self.rect.topleft[1] + each.rect.height >= \
                            pos[1] >= each.rect.topleft[1] + self.rect.topleft[1]:
                        each.handle(event)
                        # print(each.rect.topleft)
                        found = True

            if not found:
                if self.mouse_dn:
                    # collapse a group only if the mouse is over top or bottom part of the slider and not between icons
                    if self.t < pos[1] < self.t + self.th or self.b > pos[1] > self.b - self.bh:
                        self.on_click()

        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            # self.menu.mainloop.mouse_over[1] = self
            found = False
            if self.selected:
                for each in self.categories:
                    # if each.rect.topleft[0]+self.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0]+self.rect.topleft[0] and each.rect.topleft[1]+self.rect.topleft[1] + each.rect.height >= pos[1] >= each.rect.topleft[1]+self.rect.topleft[1]:
                    if each.rect.topleft[0] + self.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] + \
                            self.rect.topleft[0] and each.rect.topleft[1] + self.rect.topleft[1] + each.rect.height >= \
                            pos[1] >= each.rect.topleft[1] + self.rect.topleft[1]:

                        each.handle(event)

                        if self.menu.mainloop.mouse_over[1] is not None:
                            self.menu.mainloop.mouse_over[1].mouse_over = False
                        self.menu.mainloop.mouse_over[1] = None

                        if self.menu.mainloop.mouse_over[2] != each:
                            if self.menu.mainloop.mouse_over[2] is not None:
                                self.menu.mainloop.mouse_over[2].on_mouse_out()
                            self.menu.mainloop.mouse_over[2] = each

                        found = True
            if not found:
                if self.menu.mainloop.mouse_over[1] != self:
                    if self.menu.mainloop.mouse_over[1] is not None:
                        self.menu.mainloop.mouse_over[1].on_mouse_out()
                    self.menu.mainloop.mouse_over[1] = self
                    if self.menu.mainloop.mouse_over[2] is not None:
                        self.menu.mainloop.mouse_over[2].on_mouse_out()
                    self.menu.mainloop.mouse_over[2] = None
                # category out
                self.on_mouse_over()

    def play_sound(self, sound_id):
        self.menu.mainloop.sfx.play(sound_id)

    def on_mouse_over(self):
        if not (self.menu.lswipe_mouse_dn or self.menu.rswipe_mouse_dn):
            if not self.mouse_over:
                self.on_mouse_enter()
            if self.state < 2:
                self.state = 1
            self.mouse_over = True

    def on_mouse_enter(self):
        if self.state < 2:
            self.image.set_alpha(255)
        self.menu.mainloop.info.title = self.title
        self.menu.mainloop.info.subtitle = self.subtitle
        self.menu.mainloop.info.game_id = "#%03i" % self.unit_id

        self.menu.mainloop.redraw_needed[1] = True
        self.menu.mainloop.redraw_needed[2] = True
        if self.menu.mainloop.android is None:
            self.menu.mainloop.info.title_only()

    def on_mouse_out(self):
        if self.mouse_over:
            if self.state < 2:
                self.state = 0
                self.image.set_alpha(self.alpha_value)

            self.mouse_over = False
            self.mouse_dn = False
            self.menu.reset_titles()

    def on_click(self):
        self.toggle_select()

    def toggle_select(self):
        if not self.menu.ldrag:
            if self.selected:
                self.hide_icons()
                self.play_sound(6)
                pygame.event.post(
                    pygame.event.Event(pygame.MOUSEMOTION,
                                       {"pos": pygame.mouse.get_pos(), "rel": None, "buttons": None}))
            else:
                self.show_icons()
                self.play_sound(5)
            self.menu.update_panel_height()

    def hide_icons(self):
        self.selected = False
        self.mouse_over = False
        self.state = 0
        self.h = self.initial_h
        self.image = pygame.Surface([self.w, self.h])
        self.image.set_colorkey((0, 0, 0))
        self.image.set_alpha(self.alpha_value)
        self.rect = self.image.get_rect()
        self.menu.mainloop.redraw_needed[2] = True
        self.menu.scroll_l = 0
        self.menu.tab_l_scroll = 0

    def show_icons(self):
        self.selected = True
        self.state = 2
        self.h = self.initial_h + 15 + len(self.categories) * (self.menu.cat_icon_size + self.menu.y_margin)
        self.image = pygame.Surface([self.w, self.h])
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.menu.mainloop.redraw_needed[2] = True

        for each in self.menu.top_categories:
            if each != self:
                each.hide_icons()

    def update(self):
        i = self.h - 30

        # background image
        while i > 30:
            self.image.blit(self.img7, (6, i))
            i = i - 29

        # chose bottom image depending on state
        o = eval("self.img%s" % str(self.state + 2))
        self.image.blit(o, (0, self.h - 40))

        # top image
        self.image.blit(self.img1, (0, 0))

        # top image frame based on state
        if self.state > 0:
            o = eval("self.img%s" % str(self.state + 4))
            self.image.blit(o, (1, 1))

        if self.selected:
            i = 85
            for each in self.categories:
                each.update()
                each.rect.topleft = (11, i)
                self.image.blit(each.image, (11, i))
                i = i + each.rect.h + self.menu.y_margin


# Objects from old version
class MenuCategory(pygame.sprite.Sprite):
    def __init__(self, menu, top_id, cat_id, title, subtitle, cat_icon_size, img_src):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.menu = menu
        self.state = 0
        self.cat_id = cat_id
        self.top_id = top_id
        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)
        self.mouse_over = False
        self.mouse_dn = False
        self.alpha_value = 200
        self.color = (245, 0, 245)

        self.image = pygame.Surface([cat_icon_size, cat_icon_size])
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha_value)
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.img_pos = (0, 0)
            try:
                self.img1 = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert_alpha()
                self.img2 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', "ico_c_bgn.png")).convert()
                self.img3 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', "ico_c_bgh.png")).convert()
                self.img4 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', "ico_c_bga.png")).convert()

                self.img_pos = (0, 0)
            except:
                pass

        # Make our top-left corner the passed-in location. The +1 is the margin
        self.rect = self.image.get_rect()

    def handle(self, event):
        # TO DO
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_dn = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.mouse_dn:
            self.menu.active_cat = self.cat_id
            if self.menu.active_cat_o is not None:
                if self.menu.active_cat_o != self:
                    self.menu.active_cat_o.deactivate()
            self.activate()

            self.menu.mainloop.redraw_needed[1] = True
            self.menu.mainloop.redraw_needed[2] = True

        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_over()

    def activate(self):
        self.state = 2
        if self.menu.active_cat_o != self:
            self.menu.mainloop.sfx.play(3)
            self.menu.active_cat_o = self

    def deactivate(self):
        self.state = 0

    def on_mouse_enter(self):
        self.mouse_over = True
        self.mouse_dn = False
        if self.state != 2:
            self.state = 1
        if self.menu.mainloop.mouse_over[2] is not None:
            self.menu.mainloop.mouse_over[2].on_mouse_out()
        self.menu.mainloop.mouse_over[2] = self

        self.menu.mainloop.redraw_needed[1] = True
        self.menu.mainloop.redraw_needed[2] = True
        if self.menu.mainloop.android is None:
            self.menu.mainloop.info.title_only()

    def on_mouse_over(self):
        if not (self.menu.lswipe_mouse_dn or self.menu.rswipe_mouse_dn):
            if not self.mouse_over:
                self.on_mouse_enter()
            self.menu.mainloop.info.title = self.title
            self.menu.mainloop.info.subtitle = self.subtitle
            self.menu.mainloop.info.game_id = "#%03i" % self.cat_id
            self.mouse_over = True

    def on_mouse_out(self):
        if self.mouse_over:
            if self.state != 2:
                self.state = 0
            self.mouse_over = False
            self.menu.reset_titles()
            self.menu.mainloop.redraw_needed[1] = True

    def update(self):
        self.image.fill(self.color)
        if self.state == 0:
            self.image.blit(self.img2, self.img_pos)
            self.image.set_alpha(self.alpha_value)
        elif self.state == 1:
            self.image.blit(self.img3, self.img_pos)
            self.image.set_alpha(255)
        elif self.state == 2:
            self.image.set_alpha(255)
            self.image.blit(self.img4, self.img_pos)
        self.image.blit(self.img1, (7, 7))


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, menu, dbgameid, item_id, cat_id, title, subtitle, constructor, icon_size, img_src, img_src2,
                 variant=0, var2=0, max_age=7):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.menu = menu
        self.mouse_over = False
        self.mouse_dn = False
        self.item_id = item_id
        self.state = 0
        self.alpha_value = 200
        self.hidden = False
        self.cat_id = cat_id
        self.game_constructor = constructor
        self.variant = variant
        self.var2 = var2
        self.dbgameid = dbgameid
        self.lang_activity = False

        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)

        self.max_age = max_age

        self.color0 = (33, 121, 149)
        self.color1 = (0, 0, 0)
        self.color2 = (255, 255, 255)


        self.image = pygame.Surface([icon_size[0], icon_size[1]])
        self.image.set_alpha(self.alpha_value)
        self.img_src = img_src
        self.img_src2 = img_src2 #image on the right hand side of the icon
        if len(self.img_src) > 0:
            if len(self.img_src2) == 0:
                self.img_src2 = "eico0.png"
            # self.img = self.image
            self.img_pos = (0, 0)
            try:
                self.img1 = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert_alpha()
                self.img2 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', "ico_bgn.png")).convert_alpha()
                self.img3 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', "ico_bgh.png")).convert_alpha()
                self.img4 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', "ico_bga.png")).convert_alpha()
                self.img5 = self.img4  # pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', "ico_bgb.png")).convert_alpha()
                self.img6 = pygame.image.load(os.path.join('res', 'icons', self.img_src2)).convert_alpha()
            except:
                pass



        #self.image.set_colorkey(self.color)

        # Make our top-left corner the passed-in location. The +1 is the margin
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill(self.color0)
        if self.state == 0:
            self.image.blit(self.img2, self.img_pos)
            self.image.set_alpha(self.alpha_value)
        elif self.state == 1:
            self.image.blit(self.img3, self.img_pos)
            self.image.set_alpha(255)
        elif self.state == 2:
            self.image.set_alpha(255)
            if self.menu.mainloop.scheme is not None and self.menu.mainloop.scheme.dark:
                self.image.fill(self.color1)
                self.image.blit(self.img5, self.img_pos)
            else:
                self.image.fill(self.color2)
                self.image.blit(self.img4, self.img_pos)
        self.image.blit(self.img1, (7, 7))
        self.image.blit(self.img6, (57, 9))

    def handle(self, event):
        # TO DO
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_dn = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.mouse_dn:
            pass
            """
            self.menu.active_cat = self.cat_id
            #self.tab_l_scroll = (self.scroll_l // self.scroll_step)
            if self.menu.mainloop.config.settings["sounds"]:
                s3.play()
            self.menu.mainloop.redraw_needed[1] = True
            self.menu.mainloop.redraw_needed[2] = True
            """
        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_over()

    def on_mouse_enter(self):
        self.mouse_over = True
        self.mouse_dn = False
        if self.state != 2:
            self.state = 1
        if self.menu.mainloop.mouse_over[2] is not None:
            self.menu.mainloop.mouse_over[2].on_mouse_out()
        self.menu.mainloop.mouse_over[2] = self

        self.menu.mainloop.redraw_needed[1] = True
        self.menu.mainloop.redraw_needed[2] = True
        if self.menu.mainloop.android is None:
            self.menu.mainloop.info.title_only()

    def on_mouse_over(self):
        if not (self.menu.lswipe_mouse_dn or self.menu.rswipe_mouse_dn):
            if not self.mouse_over:
                self.on_mouse_enter()
            self.menu.mainloop.info.title = self.title
            self.menu.mainloop.info.subtitle = self.subtitle
            self.menu.mainloop.info.game_id = "#%s/%03i" % (self.game_constructor[4:7], self.dbgameid)
            self.mouse_over = True

    def on_mouse_out(self):
        if self.mouse_over:
            if self.state != 2:
                self.state = 0
            self.mouse_over = False
            self.mouse_dn = False
            self.menu.reset_titles()
            self.menu.mainloop.redraw_needed[1] = True


class MenuBookmark(pygame.sprite.Sprite):
    def __init__(self, menu, bm_id, bm_icon_width, img_src):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.menu = menu
        self.bm_id = bm_id
        self.color = (245, 0, 245)

        self.image = pygame.Surface([bm_icon_width, 78])
        self.image.fill(self.color)
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.img = self.image
            self.img_pos = (0, 0)
            try:
                self.img_org = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'icon_frames', self.img_src)).convert()
                self.img_pos = (0, 0)
                self.img = self.img_org
            except:
                pass

        # Make our top-left corner the passed-in location. The +1 is the margin
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill(self.color)
        if len(self.img_src) > 0:
            self.image.blit(self.img, self.img_pos)


class ScrollArrowItem(pygame.sprite.Sprite):
    def __init__(self, menu, imgh, imga, w, h, direction, bg_col):
        pygame.sprite.Sprite.__init__(self)
        self.menu = menu
        self.image = pygame.Surface([w, h])
        self.color = bg_col
        self.direction = direction
        self.image.fill(self.color)

        self.state = 1
        self.mouse_over = False
        self.mouse_dn = False
        self.img_pos = (0, 0)
        self.w = w
        self.h = h
        self.imgs_loaded = False

        # try:
        self.img1 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'images', 'arrows', imga)).convert()
        self.img2 = pygame.image.load(os.path.join("res", "themes", self.menu.mainloop.theme, 'images', 'arrows', imgh)).convert()
        #self.img0 = pygame.image.load(os.path.join('res', 'images', 'arrows', imgd)).convert()
        self.imgs_loaded = True
        # except:
        #    pass

        self.rect = self.image.get_rect()

    def handle(self, event):
        # TO DO
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_dn = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.mouse_dn:
            self.mouse_dn = False

        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_over()

    def on_mouse_enter(self):
        self.mouse_over = True
        self.mouse_dn = False
        if self.state != 0:
            self.state = 2
            if self.menu.mainloop.mouse_over[1] is not None:
                self.menu.mainloop.mouse_over[1].on_mouse_out()
            if self.menu.mainloop.mouse_over[2] is not None:
                self.menu.mainloop.mouse_over[2].on_mouse_out()
            self.menu.mainloop.mouse_over[2] = self

            self.menu.mainloop.redraw_needed[1] = True
            self.menu.mainloop.redraw_needed[2] = True

    def on_mouse_over(self):
        if not self.mouse_over:
            self.on_mouse_enter()
        self.mouse_over = True

    def on_mouse_out(self):
        if self.mouse_over:
            if self.state != 0:
                self.state = 1
                self.mouse_over = False
                self.mouse_dn = False
                self.menu.mainloop.redraw_needed[2] = True

    def update(self):
        if self.imgs_loaded:
            eval("self.image.blit(self.img%d, self.img_pos)" % self.state)


class Menu:
    def __init__(self, mainloop):
        self.mainloop = mainloop
        self.lang = self.mainloop.lang
        self.uage = self.mainloop.config.user_age_group
        self.create_lists()
        self.scroll_arrows = []
        self.arrow_h = 50
        self.mouseenter = -1
        self.mouseenter_cat = -1
        self.l = None
        self.active_game_id = 0
        self.active_o = None
        self.active_cat_o = None
        self.mouse_over = False
        self.game_started_id = -1
        self.active_cat = 0
        self.tab_game_id = -5
        self.prev_cat = -1
        self.lang_activity = False
        self.game_constructor = "game000.Board"
        self.game_dbid = 0
        self.game_variant = 0
        self.game_var2 = 0
        self.icon_size = [50+26+12, 50+8]
        self.cat_icon_size = 58
        self.initial_cat_h = 105
        self.x_margin = 6 + 4  # 6
        self.y_margin = 10  # 5
        self.scroll_l = 0
        self.scroll_r = 0
        self.tab_l_scroll = 0
        self.tab_r_scroll = 0
        self.scroll_direction = 0
        self.active_pane = None
        self.en_list = []  # list of games that need the speaker to be switched to English
        self.scroll_step = self.icon_size[1] + self.y_margin

        self.id2icon = dict()

        self.cat_img_src2 = "ico_tbn.png"  # bottom part normal
        self.cat_img_src3 = "ico_tbh.png"  # bottom part hover
        self.cat_img_src4 = "ico_tba.png"  # bottom part active
        self.cat_img_src5 = "ico_t_frame_hover.png"  # top hover frame
        self.cat_img_src6 = "ico_t_frame_active.png"  # top active frame
        self.cat_img_src7 = "ico_t_red_bg.png"  # category background image

        self.xml = self.mainloop.xml_conn

        # This is a list of 'sprites.' Each block in the program is
        # added to this list. The list is managed by a class called 'RenderPlain.'
        self.categories_list = pygame.sprite.LayeredUpdates()
        self.top_categories_list = pygame.sprite.LayeredUpdates()
        self.games_in_current_cat = pygame.sprite.LayeredUpdates()
        self.bookmarks_list = pygame.sprite.LayeredUpdates()
        self.larrows_list = pygame.sprite.LayeredUpdates()
        self.rarrows_list = pygame.sprite.LayeredUpdates()

        self.lswipe_mouse_dn = None
        self.lswipe_mouse_up = None
        self.lswiped = False
        self.rswipe_mouse_dn = None
        self.rswipe_mouse_up = None
        self.rswiped = False
        self.lswipe_t = 0
        self.rswipe_t = 0
        self.ldrag = False
        self.rdrag = False
        #self.game_constructors = [game000, game001, game002, game003, game004, game005, game006, game007, game008, game009, game010, game011, game012, game013, game014, game015, game016, game017, game018, game019, game020, game021, game022, game023, game024, game025, game026, game027, game028, game029, game030, game031, game032, game033, game034, game035, game036, game037, game038, game039, game040, game041, game042, game043, game044, game045, game046, game047, game048, game049, game050, game051, game052, game053, game054, game055, game056, game057, game058, game059, game060, game061, game062, game063, game064, game065, game066, game067, game068, game069, game070, game071, game072, game073, game074, game075, game076, game077, game078, game079, game080, game081, game082, game083, game084, game085, game086, game087, game088]
        self.add_arrows()
        self.create_menu()

    def add_arrows(self):
        lt = ScrollArrowItem(self, "lth.png", "lta.png", 95, 50, -1, self.mainloop.cl.menu_l)
        lb = ScrollArrowItem(self, "lbh.png", "lba.png", 95, 50, 1, self.mainloop.cl.menu_l)
        rt = ScrollArrowItem(self, "rth.png", "rta.png", 108, 50, -1, self.mainloop.cl.menu_r)
        rb = ScrollArrowItem(self, "rbh.png", "rba.png", 108, 50, 1, self.mainloop.cl.menu_r)
        self.scroll_arrows = [lt, lb, rt, rb]
        self.larrows_list.add(lt)
        self.larrows_list.add(lb)
        self.rarrows_list.add(rt)
        self.rarrows_list.add(rb)

    def update_panel_height(self):
        h = 0
        for each in self.top_categories:
            h = h + each.h + self.y_margin

        self.cat_h = h

    def swipe_reset(self):
        self.lswipe_mouse_dn = None
        self.lswipe_mouse_up = None
        self.lswiped = False
        self.rswipe_mouse_dn = None
        self.rswipe_mouse_up = None
        self.rswiped = False
        self.lswipe_t = 0
        self.rswipe_t = 0

    def load_levels(self):
        if self.mainloop.config.save_levels:
            temp = dict()
            temp = self.mainloop.db.load_all_cursors(self.mainloop.userid)
            for key in self.saved_levels.keys():
                if key not in temp.keys():
                    temp[key] = self.saved_levels[key]
            self.saved_levels = temp

    def save_levels(self):
        pass

    def commit_save(self, file_name):
        pass

    def create_lists(self):
        self.categories = []
        self.top_categories = []
        self.elements = []
        self.games = []
        self.games_current = []
        self.bookmarks = []
        self.saved_levels = dict()

    def add_categories_to_groups(self):
        for each in self.categories:
            if each.top_id > 0:
                self.top_categories[each.top_id - 1].categories.append(each)

    def create_menu(self):
        #self.add_categories()
        #self.add_top_categories()
        self.add_all()
        self.add_categories_to_groups()
        #self.add_games()
        self.add_bookmark("", "tab_l.png", 78)
        self.scroll_l = 0
        self.scroll_r = 0

        img_src = "tab_r.png"
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                img_src = "tab_r2.png"
        self.add_bookmark("", img_src, 65+26 + 12)
        self.load_levels()

    def empty_menu(self):
        self.create_lists()
        self.categories_list.empty()
        self.top_categories_list.empty()
        self.games_in_current_cat.empty()
        self.bookmarks_list.empty()

    def lang_change(self):
        self.empty_menu()
        self.create_menu()
        self.change_cat(self.active_cat)

    def reset_scroll(self):
        self.scroll_r = 0
        self.tab_r_scroll = 0
        self.scroll_l = 0
        self.tab_l_scroll = 0

    def handle_menu_l(self, event):
        self.on_mouse_over()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.scroll_menu(direction=-1, pane=0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.scroll_menu(direction=1, pane=0)

        elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            # if event.type == pygame.MOUSEBUTTONUP:
            #    self.mainloop.game_board.drag = False
            pos = [event.pos[0], event.pos[1]]
            if self.l.screen_h - self.arrow_h > pos[1] > self.l.misio_pos[3] + self.arrow_h:
                sub_category_found = False
                for each in self.elements:
                    if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and each.rect.topleft[
                        1] + each.rect.height >= pos[1] >= each.rect.topleft[1]:
                        each.handle(event)
                        sub_category_found = True

                if not sub_category_found:
                    if self.mainloop.mouse_over[1] is not None:
                        self.mainloop.mouse_over[1].on_mouse_out()
                        self.mainloop.mouse_over[1] = None
                    if self.mainloop.mouse_over[2] is not None:
                        self.mainloop.mouse_over[2].on_mouse_out()
                        self.mainloop.mouse_over[2] = None
            else:
                for each in self.larrows_list:
                    if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and each.rect.topleft[
                        1] + each.rect.height >= pos[1] >= each.rect.topleft[1]:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.scroll_menu(direction=each.direction, pane=0)
                        if event.type == pygame.MOUSEMOTION:
                            each.handle(event)

                        if self.mainloop.mouse_over[1] is not None:
                            self.mainloop.mouse_over[1].on_mouse_out()
                            self.mainloop.mouse_over[1] = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.lswipe_mouse_dn = True
                self.lswipe_t = pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                self.lswipe_mouse_dn = False
                if self.ldrag:
                    self.ldrag = False
            elif event.type == pygame.MOUSEMOTION:
                if self.lswipe_mouse_dn is True:
                    if pos[1] > self.lswipe_t + self.cat_icon_size + self.y_margin:
                        self.scroll_menu(-1, 0)
                        self.lswipe_t = pos[1]
                        self.ldrag = True
                    elif pos[1] < self.lswipe_t - (self.cat_icon_size + self.y_margin):
                        self.scroll_menu(1, 0)
                        self.lswipe_t = pos[1]
                        self.ldrag = True
        else:
            pass

    def handle_menu_r(self, event, mlw):
        try:
            if event.type == pygame.MOUSEMOTION:
                self.on_mouse_over()
                pos = [event.pos[0] - self.mainloop.layout.menu_l_w, event.pos[1]]

                if self.l.screen_h - self.arrow_h > pos[1] > self.l.misio_pos[3] + self.arrow_h:
                    for each in self.elements:
                        each.on_mouse_out()
                    if self.mainloop.info.hidden == False and pos[0] < self.l.menu_w:
                        if self.mainloop.android is None:
                            self.mainloop.info.title_only()
                    found = False
                    for each in self.games_current:
                        if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and \
                                                        each.rect.topleft[1] + each.rect.height >= pos[1] >= \
                                        each.rect.topleft[1]:
                            each.handle(event)
                            found = True
                    if not found:
                        if self.mainloop.mouse_over[2] is not None:
                            self.mainloop.mouse_over[2].on_mouse_out()

                        self.mainloop.mouse_over[2] = None
                    if self.rswipe_mouse_dn is True:
                        if pos[1] > self.rswipe_t + self.icon_size[1] + self.y_margin:
                            self.scroll_menu(-1, 1)
                            self.rswipe_t = pos[1]
                            self.rdrag = True
                        elif pos[1] < self.rswipe_t - (self.icon_size[1] + self.y_margin):
                            self.scroll_menu(1, 1)
                            self.rswipe_t = pos[1]
                            self.rdrag = True
                else:
                    for each in self.rarrows_list:
                        if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and \
                                                        each.rect.topleft[1] + each.rect.height >= pos[1] >= \
                                        each.rect.topleft[1]:
                            each.handle(event)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = [event.pos[0] - self.mainloop.layout.menu_l_w, event.pos[1]]
                if self.l.screen_h - self.arrow_h > pos[1] > self.l.misio_pos[3] + self.arrow_h:
                    for each in self.games_current:
                        if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and \
                                                        each.rect.topleft[1] + each.rect.height >= pos[1] >= \
                                        each.rect.topleft[1]:
                            each.handle(event)
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for each in self.rarrows_list:
                            if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and \
                                                            each.rect.topleft[1] + each.rect.height >= pos[1] >= \
                                            each.rect.topleft[1]:
                                self.scroll_menu(direction=each.direction, pane=1)
                                each.handle(event)
                self.rswipe_mouse_dn = True
                self.rswipe_t = pos[1]
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = [event.pos[0] - self.mainloop.layout.menu_l_w, event.pos[1]]
                if self.l.screen_h - self.arrow_h > pos[1] > self.l.misio_pos[3] + self.arrow_h:
                    self.on_mouse_up(pos, event)
                self.swipe_reset()
                self.rswipe_mouse_dn = False
                if self.rdrag:
                    self.rdrag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                self.scroll_menu(direction=-1, pane=1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                self.scroll_menu(direction=1, pane=1)
        except:
            pass

    def play_sound(self, sound_id):
        self.mainloop.sfx.play(sound_id)

    def on_mouse_up(self, pos, event=None):
        for each in self.games_current:
            if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and each.rect.topleft[
                1] + each.rect.height >= pos[1] >= each.rect.topleft[1]:
                if event is not None:
                    each.handle(event)
                if each.mouse_dn:
                    each.state = 2
                    self.active_game_id = each.item_id
                    self.mainloop.front_img.state = 0
                    if self.active_o is not None:
                        if each != self.active_o:
                            self.active_o.state = 0
                            self.play_sound(4)
                    else:
                        self.play_sound(4)
                    self.active_o = each

                    self.mainloop.config.max_age = each.max_age
                    self.game_constructor = each.game_constructor
                    self.game_dbid = each.dbgameid
                    self.game_variant = each.variant
                    self.game_var2 = each.var2
                    self.lang_activity = each.lang_activity
                    self.tab_r_scroll = (self.scroll_r // self.scroll_step)
                    row = (pos[1] - 3 - self.l.misio_pos[3] - self.arrow_h - self.scroll_r) // (
                    self.icon_size[1] + self.y_margin)
                    self.tab_game_id = row

                    self.mainloop.score = 0
                    self.mainloop.redraw_needed = [True, True, True]
                    break

    def start_hidden_game(self, gameid):
        for each in self.games:
            if each.dbgameid == gameid:
                self.active_game_id = each.item_id
                self.mainloop.front_img.state = 0
                if self.active_o is not None:
                    if each != self.active_o:
                        self.active_o.state = 0
                        self.play_sound(4)
                else:
                    self.play_sound(4)
                self.active_o = each
                self.game_constructor = each.game_constructor
                self.game_variant = each.variant
                self.game_var2 = each.var2
                self.tab_r_scroll = -1
                self.tab_game_id = -1

                self.mainloop.score = 0
                self.mainloop.redraw_needed = [True, True, True]

    def on_mouse_over(self):
        if not self.mouse_over:
            self.on_mouse_enter()

    def on_mouse_enter(self):
        if self.mainloop.mouse_over[0] is not None:
            self.mainloop.mouse_over[0].on_mouse_out()
        self.mainloop.mouse_over[0] = self
        if self.mainloop.mouse_over[1] is not None:
            self.mainloop.mouse_over[1].on_mouse_out()
        self.mainloop.mouse_over[1] = None
        if self.mainloop.mouse_over[2] is not None:
            self.mainloop.mouse_over[2].on_mouse_out()
        self.mainloop.mouse_over[2] = None

        self.update_panel_height()

        self.mouse_over = True

    def on_mouse_out(self):
        if self.mouse_over:
            self.mouse_over = False

    def scroll_menu(self, direction=0, pane=-1):
        if pane == -1:
            direction = self.scroll_direction
            pane = self.active_pane
        menu_height = self.mainloop.size[1] - (self.y_margin + self.l.misio_pos[3] + 2 * self.arrow_h)
        if direction != 0 and pane == 1:
            if self.game_h > menu_height:
                diff = self.game_h - menu_height
                if (direction == 1 and -self.scroll_r < diff) or (direction == -1 and self.scroll_r < 0):
                    self.scroll_r = self.scroll_r - self.scroll_step * direction

                self.tab_r_scroll = (self.scroll_r // self.scroll_step)
                self.mainloop.redraw_needed[2] = True
                self.mainloop.redraw_needed[1] = True
        elif direction != 0 and pane == 0:
            diff = self.cat_h - menu_height
            if (direction == 1 and -self.scroll_l < diff) or (direction == -1 and self.scroll_l < 0):
                self.scroll_l = self.scroll_l - self.scroll_step * direction
            self.tab_l_scroll = (self.scroll_l // self.scroll_step)
            self.mainloop.redraw_needed[2] = True
            self.mainloop.redraw_needed[1] = True

    def reset_titles(self):
        self.mainloop.info.title = ""
        self.mainloop.info.subtitle = ""
        self.mainloop.info.game_id = ""
        self.mainloop.redraw_needed[1] = True
        self.mainloop.redraw_needed[2] = True
        self.mouseenter = -1
        self.mouseenter_cat = -1

    def add_bookmark(self, title, img_src, width):
        new_bookmark = MenuBookmark(self, len(self.bookmarks), width, img_src)
        self.bookmarks.append(new_bookmark)

    def add_top_category(self, top_id, title, subtitle, img_src1):  # 105
        new_top_category = MenuCategoryGroup(self, top_id, title, subtitle, 80, self.initial_cat_h, img_src1)
        self.top_categories.append(new_top_category)
        self.top_categories_list.add(new_top_category)
        self.elements.append(new_top_category)

    def add_all(self):
        #t1 = time.clock()
        self.add_category(0, 0, self.lang.d["Info Category"], "", "ico_c_00.png")

        self.badge_count = self.mainloop.db.get_completion_count(self.mainloop.userid)
        # [0   1   2   3   4   5   6   7]
        # pre, y1, y2, y3, y4, y5, y6, all
        # spare game spots - 048
        # spare_ids - 119 - 130
        self.id2icon = dict()

        self.lang_customized_icons = (11, 140, 12, 13)
        c_id = 0  # Add the home screens
        self.add_game(0, c_id, 0, 7, "game000.Board", "", "", "ico_g_0000.png")
        self.games[-1].hidden = True
        if self.badge_count > 0:
            self.add_game(141, c_id, 0, 7, "game004.Board", self.lang.d["Achievements"], "", "ico_g_0004.png", "eico8.png")
        self.add_game(3, c_id, 0, 7, "game003.Board", self.lang.d["Language"], "", "ico_g_0003.png", "eico9.png")

        self.add_game(2, c_id, 0, 7, "game002.Board", self.lang.d["Translators"], "", "ico_g_0002.png", "eico7.png")
        #self.games[-1].hidden = True
        self.add_game(1, c_id, 0, 7, "game001.Board", self.lang.d["Credits"], "", "ico_g_0001.png", "eico7.png")
        #self.games[-1].hidden = True
        home_cat_icons = {0: "ico_g_0000.png", 141: "ico_g_0004.png", 3: "ico_g_0003.png", 1: "ico_g_0001.png",
                          2: "ico_g_0002.png"}
        self.id2icon.update(home_cat_icons)

        for top_cat in self.xml.menu_root:
            #add category groups
            self.add_top_category(ast.literal_eval(top_cat.attrib['id']), self.lang.d[top_cat.attrib['title']], "",
                                  top_cat.attrib['icon'])
            for cat in top_cat:
                #add categories
                cat_add = True

                if cat.attrib['visible'] == "0":
                    cat_add = False
                # check the age range if not in display all
                elif self.uage != 7:
                    if self.uage < ast.literal_eval(cat.attrib['min_age']):
                        cat_add = False
                    elif self.uage > ast.literal_eval(cat.attrib['max_age']):
                        cat_add = False

                # check for languages included/excluded
                if cat.attrib['lang_incl'] != "":
                    lin = ast.literal_eval(cat.attrib['lang_incl'])
                    if self.mainloop.lang.lang[0:2] not in lin:
                        cat_add = False
                elif cat.attrib['lang_excl'] != "":
                    lex = ast.literal_eval(cat.attrib['lang_excl'])
                    if self.mainloop.lang.lang[0:2] in lex:
                        cat_add = False
                # check if the activity requires espeak to work correctly
                if self.mainloop.speaker.started is False and ast.literal_eval(cat.attrib['listening']) is True:
                    cat_add = False

                if cat_add:
                    c_id = ast.literal_eval(cat.attrib['id'])
                    if ast.literal_eval(cat.attrib["icosuffix"]):
                        ico = cat.attrib['icon'][0:8] + self.lang.ico_suffix + cat.attrib['icon'][8:]
                        self.add_category(ast.literal_eval(top_cat.attrib['id']), c_id,
                                          self.lang.d[cat.attrib['title']], self.lang.d[cat.attrib['subtitle']],
                                          ico)
                    else:
                        self.add_category(ast.literal_eval(top_cat.attrib['id']), c_id,
                                          self.lang.d[cat.attrib['title']], self.lang.d[cat.attrib['subtitle']],
                                          cat.attrib['icon'])

                    for game in cat:
                        # add games in current category
                        add = True

                        if game.attrib['visible'] == "0":
                            add = False
                        # check the age range and display code
                        elif self.uage != 7:
                            if self.uage < int(game.attrib['min_age']):
                                add = False
                            elif self.uage > int(game.attrib['max_age']):
                                add = False

                        if add:
                            # check for languages included/excluded
                            if game.attrib['lang_incl'] != "":
                                lin = ast.literal_eval(game.attrib['lang_incl'])
                                if self.mainloop.lang.lang[0:2] not in lin:
                                    add = False
                            elif game.attrib['lang_excl'] != "":
                                lex = ast.literal_eval(game.attrib['lang_excl'])
                                if self.mainloop.lang.lang[0:2] in lex:
                                    add = False

                            # check if the game requires the alphabet to have upper case
                            if self.lang.has_uc is False and ast.literal_eval(
                                    game.attrib['require_uc']) is True:
                                add = False
                            elif self.mainloop.android is not None and ast.literal_eval(
                                    game.attrib['android']) is False:
                                add = False
                            elif self.mainloop.speaker.started is False and ast.literal_eval(
                                    game.attrib['listening']) is True:
                                add = False

                        if add:
                            # dbgameid, cat_id, min_age, max_age, constructor, title, subtitle, img_src, variant=0, var2=0
                            if ast.literal_eval(game.attrib["icosuffix"]):
                                ico = game.attrib['icon'][0:10] + self.lang.ico_suffix + game.attrib[
                                                                                             'icon'][10:]
                                self.add_game(int(game.attrib['dbid']),
                                              c_id,
                                              int(game.attrib["min_age"]),
                                              int(game.attrib["max_age"]),
                                              "game%03i.Board" % int(game.attrib["constructor_id"]),
                                              self.lang.d[game.attrib['title']],
                                              self.lang.d[game.attrib['subtitle']],
                                              ico, game.attrib['ico_group'],
                                              int(game.attrib["variant"]),
                                              int(game.attrib["var2"]))
                            else:
                                self.add_game(int(game.attrib['dbid']),
                                              c_id,
                                              int(game.attrib["min_age"]),
                                              int(game.attrib["max_age"]),
                                              "game%03i.Board" % int(game.attrib["constructor_id"]),
                                              self.lang.d[game.attrib['title']],
                                              self.lang.d[game.attrib['subtitle']],
                                              game.attrib['icon'], game.attrib['ico_group'],
                                              int(game.attrib["variant"]),
                                              int(game.attrib["var2"]))
                            self.games[-1].lang_activity = ast.literal_eval(game.attrib['lang_activity'])
                        self.id2icon[int(game.attrib['dbid'])] = game.attrib['icon']
                else:
                    for game in cat:
                        self.id2icon[int(game.attrib['dbid'])] = game.attrib['icon']
        self.update_panel_height()

    def add_category(self, top_id, cat_id, title, subtitle, img_src):
        new_category = MenuCategory(self, top_id, cat_id, title, subtitle, self.cat_icon_size, img_src)
        self.categories.append(new_category)
        self.categories_list.add(new_category)

    def add_game(self, dbgameid, cat_id, min_age, max_age, constructor, title, subtitle, img_src, img_src2="", variant=0, var2=0):
        if min_age <= self.uage <= max_age or self.uage == 7:
            new_game = MenuItem(self, dbgameid, len(self.games), cat_id, title, subtitle, constructor, self.icon_size,
                                img_src, img_src2, variant, var2, max_age)
            self.games.append(new_game)
        self.saved_levels[dbgameid] = 1

    def draw_menu(self, menu, menu_l, menu_r, l):
        mw = l.menu_r_w
        menu.fill((255, 255, 255))
        menu_l.fill(self.mainloop.cl.menu_l)
        menu_r.fill(self.mainloop.cl.menu_r)
        pygame.draw.line(menu_l, self.mainloop.cl.white, [l.menu_l_w - 1, 0], [l.menu_l_w - 1, l.screen_h], 1)

        # load games from new category if changed
        self.change_category(self.active_cat)

        x = self.x_margin - 3
        y = self.y_margin + l.misio_pos[3] + self.scroll_l + self.arrow_h

        for each_item in self.top_categories:
            each_item.rect.topleft = [x, y]
            each_item.t = y
            each_item.b = y + each_item.h
            y += each_item.h + self.y_margin

            each_item.update()

        x = self.x_margin
        y = self.y_margin + l.misio_pos[3] + self.scroll_r + self.arrow_h
        c = 5
        for each_item in self.games_current:
            each_item.rect.topleft = [x, y]
            each_item.update()
            y += self.icon_size[1] + self.y_margin
            c += 10

        # if category with current game is shown show the tab, otherwise hide it (move it off screen)
        if self.games[self.active_game_id] in self.games_in_current_cat:
            bmr_top = (self.tab_game_id + self.tab_r_scroll) * (self.icon_size[1] + self.y_margin) + 2 + l.misio_pos[
                3] + self.arrow_h
        else:
            bmr_top = -100
        bml_top = (self.active_cat + self.tab_l_scroll) * (self.icon_size[1] + self.y_margin) + 2 + l.misio_pos[
            3] + self.arrow_h
        self.bookmarks[0].rect.topleft = [19, bml_top - 2]
        self.bookmarks[1].rect.topleft = [5, bmr_top - 2]

        self.bookmarks[0].update()
        self.bookmarks[1].update()

        # Draw all spites
        # self.categories_list.draw(menu_l)
        self.bookmarks_list.draw(menu_l)
        self.top_categories_list.draw(menu_l)
        self.games_in_current_cat.draw(menu_r)
        x = 0
        y = l.misio_pos[3]
        if self.scroll_arrows:
            self.scroll_arrows[0].rect.topleft = [x, y]
            self.scroll_arrows[2].rect.topleft = [x, y]
            y = l.screen_h - 50
            self.scroll_arrows[1].rect.topleft = [x, y]
            self.scroll_arrows[3].rect.topleft = [x, y]

            for each in self.scroll_arrows:
                each.update()

            self.larrows_list.draw(menu_l)
            self.rarrows_list.draw(menu_r)

    def change_category(self, cat_id):
        if self.prev_cat != self.active_cat:
            self.change_cat(cat_id)

    def change_cat(self, cat_id):
        self.scroll_r = 0
        self.tab_r_scroll = 0
        self.games_in_current_cat.empty()
        self.games_current = []
        for each_item in self.games:
            if each_item.cat_id == cat_id:
                if not each_item.hidden:
                    self.games_in_current_cat.add(each_item)
                    self.games_current.append(each_item)
                    if self.active_o is not None:
                        if each_item.item_id == self.active_o.item_id:
                            self.active_o = each_item
                            self.active_o.state = 2
        self.games_in_current_cat.add(self.bookmarks[1])
        self.games_in_current_cat.move_to_back(self.bookmarks[1])
        self.prev_cat = self.active_cat
        self.game_h = len(self.games_current) * (self.icon_size[1] + self.y_margin)  # -self.y_margin
