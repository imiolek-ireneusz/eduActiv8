# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import pygame
import ast

import time

import classes.extras as ex
from game_boards import game000, game001, game002, game003, game004, game005, game006, game007, game008, game009, \
    game010, game011, game012, game013, game015, game016, game017, game018, game019, game020, game021, game022, \
    game023, game024, game025, game026, game027, game028, game029, game031, game032, game033, game034, game035, \
    game036, game037, game038, game039, game040, game041, game042, game043, game044, game045, game046, game047, game049, game050, game051, game052, game053, game054, game055, game056, \
    game059, game060, game061, \
    game062, game063, game064, game065, game066, game067, game068, game069, game070, game071, game072, game073, game074, \
    game075, game076, game077, game078, game079, game080, game081, game082, game084, game085, game086, game087, \
    game088, game089, game090


class MenuCategoryGroup(pygame.sprite.Sprite):
    def __init__(self, menu, unit_id, title, subtitle, w, h, img_src1):
        pygame.sprite.Sprite.__init__(self)

        self.selected = False
        self.state = 0  # 0 - normal, 1 - hover, 2 - selected
        self.categories = []
        self.initial_h = h
        self.mouse_dn = False
        self.alpha_value = 170

        self.menu = menu
        self.unit_id = unit_id
        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)
        self.w = w
        self.h = h

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
            self.img1 = pygame.image.load(os.path.join('res', 'icons', img_src1)).convert()
            self.img1.set_colorkey((255, 255, 255))

            # module images bottom
            self.img2 = pygame.image.load(os.path.join('res', 'icons', self.menu.cat_img_src2)).convert()
            self.img2.set_colorkey((255, 255, 255))
            self.img3 = pygame.image.load(os.path.join('res', 'icons', self.menu.cat_img_src3)).convert()
            self.img3.set_colorkey((255, 255, 255))
            self.img4 = pygame.image.load(os.path.join('res', 'icons', self.menu.cat_img_src4)).convert()
            self.img4.set_colorkey((255, 255, 255))

            # image top highlights
            self.img5 = pygame.image.load(os.path.join('res', 'icons', self.menu.cat_img_src5)).convert()
            self.img5.set_colorkey((255, 255, 255))
            self.img6 = pygame.image.load(os.path.join('res', 'icons', self.menu.cat_img_src6)).convert()
            self.img6.set_colorkey((255, 255, 255))

            # category background image
            self.img7 = pygame.image.load(os.path.join('res', 'icons', self.menu.cat_img_src7)).convert()
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

        self.menu.mainloop.redraw_needed[1] = True
        self.menu.mainloop.redraw_needed[2] = True
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
            if self.selected == True:
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
        self.alpha_value = 170
        self.color = (245, 0, 245)

        self.image = pygame.Surface([cat_icon_size, cat_icon_size])
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha_value)
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.img_pos = (0, 0)
            try:
                self.img1 = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert()
                self.img2 = pygame.image.load(os.path.join('res', 'icons', "ico_c_bgn.png")).convert()
                self.img3 = pygame.image.load(os.path.join('res', 'icons', "ico_c_bgh.png")).convert()
                self.img4 = pygame.image.load(os.path.join('res', 'icons', "ico_c_bga.png")).convert()

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
        self.menu.mainloop.info.title_only()

    def on_mouse_over(self):
        if not self.mouse_over:
            self.on_mouse_enter()

        self.menu.mainloop.info.title = self.title
        self.menu.mainloop.info.subtitle = self.subtitle
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
    def __init__(self, menu, dbgameid, item_id, cat_id, title, subtitle, constructor, icon_size, img_src, variant=0,
                 var2=0):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.menu = menu
        self.mouse_over = False
        self.mouse_dn = False
        self.item_id = item_id
        self.state = 0
        self.alpha_value = 170
        self.hidden = False
        self.cat_id = cat_id
        self.game_constructor = constructor
        self.variant = variant
        self.var2 = var2
        self.dbgameid = dbgameid

        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)

        self.color = (245, 0, 245)

        self.image = pygame.Surface([icon_size, icon_size])
        self.image.set_alpha(self.alpha_value)
        self.img_src = img_src
        if len(self.img_src) > 0:
            # self.img = self.image
            self.img_pos = (0, 0)
            try:
                self.img1 = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert()
                self.img2 = pygame.image.load(os.path.join('res', 'icons', "ico_bgn.png")).convert()
                self.img3 = pygame.image.load(os.path.join('res', 'icons', "ico_bgh.png")).convert()
                self.img4 = pygame.image.load(os.path.join('res', 'icons', "ico_bga.png")).convert()
                self.img5 = pygame.image.load(os.path.join('res', 'icons', "ico_bgb.png")).convert()
                self.img_pos = (0, 0)
            except:
                pass

        self.image.set_colorkey(self.color)

        # Make our top-left corner the passed-in location. The +1 is the margin
        self.rect = self.image.get_rect()

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
            if self.menu.mainloop.scheme is not None and self.menu.mainloop.scheme.dark:
                self.image.blit(self.img5, self.img_pos)
            else:
                self.image.blit(self.img4, self.img_pos)
        self.image.blit(self.img1, (6, 6))

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
        self.menu.mainloop.info.title_only()

    def on_mouse_over(self):
        if not self.mouse_over:
            self.on_mouse_enter()

        self.menu.mainloop.info.title = self.title
        self.menu.mainloop.info.subtitle = self.subtitle
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
    def __init__(self, bm_id, bm_icon_width, img_src):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.bm_id = bm_id
        self.color = (245, 0, 245)

        self.image = pygame.Surface([bm_icon_width, 70])
        self.image.fill(self.color)
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.img = self.image
            self.img_pos = (0, 0)
            try:
                self.img_org = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert()
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
    def __init__(self, menu, imgh, imga, imgd, w, h, direction, bg_col):
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
        self.img1 = pygame.image.load(os.path.join('res', 'images', 'arrows', imga)).convert()
        self.img2 = pygame.image.load(os.path.join('res', 'images', 'arrows', imgh)).convert()
        self.img0 = pygame.image.load(os.path.join('res', 'images', 'arrows', imgd)).convert()
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
        self.game_constructor = game000.Board
        self.game_dbid = 0
        self.game_variant = 0
        self.game_var2 = 0
        self.icon_size = 50
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
        self.scroll_step = self.icon_size + self.y_margin

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
        lt = ScrollArrowItem(self, "lth.png", "lta.png", "ltd.png", 95, 50, -1, self.mainloop.cl.menu_l)
        lb = ScrollArrowItem(self, "lbh.png", "lba.png", "lbd.png", 95, 50, 1, self.mainloop.cl.menu_l)
        rt = ScrollArrowItem(self, "rth.png", "rta.png", "rtd.png", 70, 50, -1, self.mainloop.cl.menu_r)
        rb = ScrollArrowItem(self, "rbh.png", "rba.png", "rbd.png", 70, 50, 1, self.mainloop.cl.menu_r)
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
        self.add_bookmark("", img_src, 65)
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
                        if pos[1] > self.rswipe_t + self.icon_size + self.y_margin:
                            self.scroll_menu(-1, 1)
                            self.rswipe_t = pos[1]
                            self.rdrag = True
                        elif pos[1] < self.rswipe_t - (self.icon_size + self.y_margin):
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
                    self.game_constructor = each.game_constructor
                    self.game_dbid = each.dbgameid
                    self.game_variant = each.variant
                    self.game_var2 = each.var2
                    self.tab_r_scroll = (self.scroll_r // self.scroll_step)
                    row = (pos[1] - 3 - self.l.misio_pos[3] - self.arrow_h - self.scroll_r) // (
                    self.icon_size + self.y_margin)
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
        self.mainloop.redraw_needed[1] = True
        self.mainloop.redraw_needed[2] = True
        self.mouseenter = -1
        self.mouseenter_cat = -1

    def add_bookmark(self, title, img_src, width):
        new_bookmark = MenuBookmark(len(self.bookmarks), width, img_src)
        self.bookmarks.append(new_bookmark)

    def add_top_category(self, top_id, title, subtitle, img_src1):  # 105
        new_top_category = MenuCategoryGroup(self, top_id, title, subtitle, 80, self.initial_cat_h, img_src1)
        self.top_categories.append(new_top_category)
        self.top_categories_list.add(new_top_category)
        self.elements.append(new_top_category)

    def add_all(self):
        #t1 = time.clock()
        self.add_category(0, self.lang.d["Info Category"], "", "ico_c_00.png")

        self.badge_count = self.mainloop.db.get_completion_count(self.mainloop.userid)
        # [0   1   2   3   4   5   6   7]
        # pre, y1, y2, y3, y4, y5, y6, all
        # spare game spots - 048
        # spare_ids - 119 - 130
        self.id2icon = dict()
        """
        self.id2icon = {0: 'ico_g_0000.png', 1: 'ico_g_0001.png', 2: 'ico_g_0001.png', 3: 'ico_g_0003.png',
                        4: 'ico_g_0101.png', 5: 'ico_g_0100.png', 11: 'ico_g_0103.png', 12: 'ico_g_0105.png',
                        13: 'ico_g_0106.png', 14: 'ico_g_0107.png', 15: 'ico_g_0107.png', 17: 'ico_g_0200.png',
                        18: 'ico_g_0201.png', 19: 'ico_g_0202.png', 20: 'ico_g_0300.png', 21: 'ico_g_0323.png',
                        22: 'ico_g_0301.png', 23: 'ico_g_0317.png', 24: 'ico_g_0318.png', 25: 'ico_g_0302.png',
                        26: 'ico_g_0303.png', 27: 'ico_g_0306.png', 28: 'ico_g_0307.png', 29: 'ico_g_0308.png',
                        30: 'ico_g_0324.png', 31: 'ico_g_0319.png', 32: 'ico_g_0320.png', 33: 'ico_g_0321.png',
                        34: 'ico_g_0322.png', 35: 'ico_g_0309.png', 36: 'ico_g_0310.png', 37: 'ico_g_0311.png',
                        38: 'ico_g_0312.png', 39: 'ico_g_0313.png', 40: 'ico_g_0314.png', 41: 'ico_g_0315.png',
                        42: 'ico_g_0316.png', 43: 'ico_g_0400.png', 44: 'ico_g_0405.png', 45: 'ico_g_0401.png',
                        46: 'ico_g_0402.png', 47: 'ico_g_0403.png', 48: 'ico_g_0404.png', 49: 'ico_g_0406.png',
                        50: 'ico_g_0407.png', 51: 'ico_g_0408.png', 52: 'ico_g_0409.png', 53: 'ico_g_0410.png',
                        54: 'ico_g_1100.png', 55: 'ico_g_1101.png', 56: 'ico_g_1102.png', 57: 'ico_g_1103.png',
                        58: 'ico_g_1104.png', 59: 'ico_g_1105.png', 60: 'ico_g_1106.png', 61: 'ico_g_1107.png',
                        62: 'ico_g_0500.png', 63: 'ico_g_0501.png', 64: 'ico_g_0502.png', 65: 'ico_g_0503.png',
                        66: 'ico_g_1000.png', 67: 'ico_g_1001.png', 68: 'ico_g_1002.png', 69: 'ico_g_1003.png',
                        70: 'ico_g_1004.png', 71: 'ico_g_0600.png', 72: 'ico_g_0601.png', 73: 'ico_g_0602.png',
                        74: 'ico_g_0603.png', 75: 'ico_g_0605.png', 76: 'ico_g_0607.png', 77: 'ico_g_0604.png',
                        78: 'ico_g_0606.png', 79: 'ico_g_0700.png', 80: 'ico_g_0701.png', 81: 'ico_g_0702.png',
                        82: 'ico_g_0703.png', 83: 'ico_g_0704.png', 84: 'ico_g_0705.png', 85: 'ico_g_0706.png',
                        86: 'ico_g_0800.png', 87: 'ico_g_0801.png', 88: 'ico_g_0811.png', 89: 'ico_g_0812.png',
                        90: 'ico_g_0813.png', 91: 'ico_g_0803.png', 92: 'ico_g_0802.png', 93: 'ico_g_0806.png',
                        94: 'ico_g_0804.png', 95: 'ico_g_0807.png', 96: 'ico_g_0808.png', 97: 'ico_g_0809.png',
                        98: 'ico_g_0810.png', 102: 'ico_g_0325.png', 103: 'ico_g_0326.png', 107: 'ico_g_0203.png',
                        108: 'ico_g_0204.png', 109: 'ico_g_0205.png', 110: 'ico_g_0206.png', 111: 'ico_g_0209.png',
                        112: 'ico_g_0210.png', 113: 'ico_g_0211.png', 114: 'ico_g_0212.png', 115: 'ico_g_0208.png',
                        116: 'ico_g_0213.png', 117: 'ico_g_0214.png', 118: 'ico_g_0207.png', 135: 'ico_g_1008.png',
                        140: 'ico_g_0104.png', 141: 'ico_g_0004.png', 142: "ico_g_1000.png", 143: 'ico_g_0327.png',
                        144: "ico_g_0328.png", 145: "ico_g_0329.png", 146: "ico_g_0107.png", 147: "ico_g_1008.png",
                        148: "ico_g_1000.png", 149: "ico_g_1000.png", 150: "ico_g_1001.png", 151: "ico_g_1002.png",
                        152: "ico_g_1003.png", 153: "ico_g_1004.png", 154: "ico_g_1004.png"}
        """

        # a dictionary of unique icons (ie. language specific) for use in achievements - only those activities that are graded
        # unique_ico = {15: "ico_g_0107.png", 106: "ico_g_1007.png"}
        # self.id2icon.update(unique_ico)

        self.lang_customized_icons = (11, 140, 12, 13)
        c_id = 0  # Add the home screens
        self.add_game(0, c_id, 0, 7, game000.Board, self.lang.d["About."], self.lang.d["Game info..."],
                      "ico_g_0000.png")
        self.games[-1].hidden = True
        # if self.badge_count > 0:
        self.add_game(141, c_id, 0, 7, game084.Board, self.lang.d["Achievements"], "", "ico_g_0004.png")
        self.add_game(3, c_id, 0, 7, game003.Board, self.lang.d["Language"], "", "ico_g_0003.png")

        self.add_game(2, c_id, 0, 7, game002.Board, self.lang.d["Translators"], "", "ico_g_0002.png")
        #self.games[-1].hidden = True
        self.add_game(1, c_id, 0, 7, game001.Board, self.lang.d["Credits"], "", "ico_g_0001.png")
        #self.games[-1].hidden = True
        home_cat_icons = {0: "ico_g_0000.png", 141: "ico_g_0004.png", 3: "ico_g_0003.png", 1: "ico_g_0001.png",
                          2: "ico_g_0002.png"}
        self.id2icon.update(home_cat_icons)

        for top_cat in self.xml.root:
            #add category groups
            self.add_top_category(ast.literal_eval(top_cat.attrib['id']), self.lang.d[top_cat.attrib['title']], "",
                                  top_cat.attrib['icon'])
            for cat in top_cat:
                #add categories
                cat_add = True

                # check for languages included/excluded
                if cat.attrib['lang_incl'] != "":
                    lin = ast.literal_eval(cat.attrib['lang_incl'])
                    if self.mainloop.lang.lang[0:2] not in lin:
                        cat_add = False
                elif cat.attrib['lang_excl'] != "":
                    lex = ast.literal_eval(cat.attrib['lang_excl'])
                    if self.mainloop.lang.lang[0:2] in lex:
                        cat_add = False

                # check the age range
                if self.uage < ast.literal_eval(cat.attrib['min_age']):
                    cat_add = False
                if self.uage > ast.literal_eval(cat.attrib['max_age']):
                    cat_add = False

                if cat_add:
                    if ast.literal_eval(cat.attrib["icosuffix"]):
                        ico = cat.attrib['icon'][0:8] + self.lang.ico_suffix + cat.attrib['icon'][8:]
                        self.add_category(ast.literal_eval(top_cat.attrib['id']), self.lang.d[cat.attrib['title']],
                                          self.lang.d[cat.attrib['subtitle']], ico)
                    else:
                        self.add_category(ast.literal_eval(top_cat.attrib['id']), self.lang.d[cat.attrib['title']],
                                          self.lang.d[cat.attrib['subtitle']], cat.attrib['icon'])
                    c_id += 1
                    for game in cat:
                        # add games in current category
                        add = True

                        # check for languages included/excluded
                        if game.attrib['lang_incl'] != "":
                            lin = ast.literal_eval(game.attrib['lang_incl'])
                            if self.mainloop.lang.lang[0:2] not in lin:
                                add = False
                        elif game.attrib['lang_excl'] != "":
                            lex = ast.literal_eval(game.attrib['lang_excl'])
                            if self.mainloop.lang.lang[0:2] in lex:
                                add = False

                        # check the age range
                        if self.uage < int(game.attrib['min_age']):
                            add = False
                        elif self.uage > int(game.attrib['max_age']):
                            add = False
                        # check if the game requires the alphabet to have upper case
                        elif self.lang.has_uc is False and ast.literal_eval(
                                game.attrib['require_uc']) is True:
                            add = False
                        elif self.mainloop.android is not None and ast.literal_eval(
                                game.attrib['android']) is False:
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
                                              eval("game%03i.Board" % int(game.attrib["constructor_id"])),
                                              self.lang.d[game.attrib['title']],
                                              self.lang.d[game.attrib['subtitle']],
                                              ico,
                                              int(game.attrib["variant"]),
                                              int(game.attrib["var2"]))
                            else:
                                self.add_game(int(game.attrib['dbid']),
                                              c_id,
                                              int(game.attrib["min_age"]),
                                              int(game.attrib["max_age"]),
                                              eval("game%03i.Board" % int(game.attrib["constructor_id"])),
                                              self.lang.d[game.attrib['title']],
                                              self.lang.d[game.attrib['subtitle']],
                                              game.attrib['icon'],
                                              int(game.attrib["variant"]),
                                              int(game.attrib["var2"]))
                        self.id2icon[int(game.attrib['dbid'])] = game.attrib['icon']
                else:
                    for game in cat:
                        self.id2icon[int(game.attrib['dbid'])] = game.attrib['icon']

        # print(time.clock() - t1)


        self.update_panel_height()

    def add_top_categoriesx(self):
        cat_groups = self.xml.get_cat_groups()
        for each in cat_groups:
            self.add_top_category(ast.literal_eval(each.attrib['id']), self.lang.d[each.attrib['title']], "", each.attrib['icon'])
        # self.add_top_category(1, self.lang.d["Language arts"], "", "ico_t_00.png")
        # self.add_top_category(2, self.lang.d["Maths"], "", "ico_t_01.png")
        # self.add_top_category(4, self.lang.d["Other"], "", "ico_t_03.png")

    def add_category(self, top_id, title, subtitle, img_src):
        new_category = MenuCategory(self, top_id, len(self.categories), title, subtitle, self.cat_icon_size, img_src)
        self.categories.append(new_category)
        self.categories_list.add(new_category)

    def add_categoriesx(self):
        self.add_category(0, self.lang.d["Info Category"], "", "ico_c_00.png")

        # id="" title="" subtitle="" icon="" min_age="" max_age="" android="True" lang_incl="" lang_excl=""

        for top_cat in self.xml.root:
            for cat in top_cat:
                add = True

                #check for languages included/excluded


                if cat.attrib['lang_incl'] != "":
                    lin = ast.literal_eval(cat.attrib['lang_incl'])
                    if self.mainloop.lang.lang[0:2] not in lin:
                        add = False
                elif cat.attrib['lang_excl'] != "":
                    lex = ast.literal_eval(cat.attrib['lang_excl'])
                    if self.mainloop.lang.lang[0:2] in lex:
                        add = False

                #check the age range
                if self.uage < ast.literal_eval(cat.attrib['min_age']):
                    add = False
                if self.uage > ast.literal_eval(cat.attrib['max_age']):
                    add = False

                if add:
                    if ast.literal_eval(cat.attrib["icosuffix"]):
                        ico = cat.attrib['icon'][0:8] + self.lang.ico_suffix + cat.attrib['icon'][8:]
                        self.add_category(ast.literal_eval(top_cat.attrib['id']), self.lang.d[cat.attrib['title']],
                                          self.lang.d[cat.attrib['subtitle']], ico)
                    else:
                        self.add_category(ast.literal_eval(top_cat.attrib['id']), self.lang.d[cat.attrib['title']],
                                          self.lang.d[cat.attrib['subtitle']], cat.attrib['icon'])




        """
        self.add_category(1, self.lang.d["Discover Letters"], "", "ico_c_01%s.png" % self.lang.ico_suffix)

        if self.mainloop.lang.lang[0:2] not in ["ar", "he"]:
            self.add_category(1, self.lang.d["Learn Words"], "", "ico_c_02.png")

        if self.uage < 4 or self.uage == 7:
            self.add_category(2, self.lang.d["Learn to Count"], "", "ico_c_03.png")
        self.add_category(2, self.lang.d["Addition"], "", "ico_c_04.png")
        self.add_category(2, self.lang.d["Subtraction"], "", "ico_c_05.png")
        if self.uage > 1:
            self.add_category(2, self.lang.d["Multiplication"], "", "ico_c_06.png")
            self.add_category(2, self.lang.d["Division"], "", "ico_c_07.png")
        if self.uage > 0:
            if self.uage < 4:
                lbl = self.lang.d["Fractions"]
            elif self.uage < 5:
                lbl = self.lang.d["Decimals and Fractions"]
            elif self.uage < 6:
                lbl = self.lang.d["Decimals, fractions and percentages"]
            else:
                lbl = self.lang.d["Decimals, fractions, ratios and percentages"]
            self.add_category(2, lbl, "", "ico_c_10.png")
            self.add_category(2, self.lang.d["Shapes and Solids"], "", "ico_c_14.png")

        if self.mainloop.lang.lang == 'sr':
            self.add_category(2, self.lang.d["Clock_cat"], self.lang.d["long form"], "ico_c_15.png")
            self.add_category(2, self.lang.d["Clock_cat"], self.lang.d["short form"], "ico_c_15.png")
        else:
            self.add_category(2, self.lang.d["Clock_cat"], "", "ico_c_15.png")

        self.add_category(3, self.lang.d["Art"], "", "ico_c_16.png")
        self.add_category(3, self.lang.d["Memory"], "", "ico_c_17.png")
        self.add_category(3, self.lang.d["Games & Mazes"], "", "ico_c_18.png")
        """

        self.update_panel_height()

    def add_game(self, dbgameid, cat_id, min_age, max_age, constructor, title, subtitle, img_src, variant=0, var2=0):
        if min_age <= self.uage <= max_age or self.uage == 7:
            new_game = MenuItem(self, dbgameid, len(self.games), cat_id, title, subtitle, constructor, self.icon_size,
                                img_src, variant, var2)
            self.games.append(new_game)
        self.saved_levels[dbgameid] = 1

        # TO DO - uncomment this when recreating the list
        # self.id2icon[dbgameid] = img_src

    def add_gamesx(self):
        'creates all menu buttons'
        """

        self.badge_count = self.mainloop.db.get_completion_count(self.mainloop.userid)
        # [0   1   2   3   4   5   6   7]
        # pre, y1, y2, y3, y4, y5, y6, all
        # spare game spots - 048
        # max id 153
        # spare_ids - 119 - 130
        # TO DO !!!!!!!!!!!!!!!!!!!!!!
        # when adding new game regenerate this list and add extra games that are only used in a specific language
        self.id2icon = {0: 'ico_g_0000.png', 1: 'ico_g_0001.png', 2: 'ico_g_0001.png', 3: 'ico_g_0003.png',
                        4: 'ico_g_0101.png', 5: 'ico_g_0100.png', 11: 'ico_g_0103.png', 12: 'ico_g_0105.png',
                        13: 'ico_g_0106.png', 14: 'ico_g_0107.png', 15: 'ico_g_0107.png', 17: 'ico_g_0200.png',
                        18: 'ico_g_0201.png', 19: 'ico_g_0202.png', 20: 'ico_g_0300.png', 21: 'ico_g_0323.png',
                        22: 'ico_g_0301.png', 23: 'ico_g_0317.png', 24: 'ico_g_0318.png', 25: 'ico_g_0302.png',
                        26: 'ico_g_0303.png', 27: 'ico_g_0306.png', 28: 'ico_g_0307.png', 29: 'ico_g_0308.png',
                        30: 'ico_g_0324.png', 31: 'ico_g_0319.png', 32: 'ico_g_0320.png', 33: 'ico_g_0321.png',
                        34: 'ico_g_0322.png', 35: 'ico_g_0309.png', 36: 'ico_g_0310.png', 37: 'ico_g_0311.png',
                        38: 'ico_g_0312.png', 39: 'ico_g_0313.png', 40: 'ico_g_0314.png', 41: 'ico_g_0315.png',
                        42: 'ico_g_0316.png', 43: 'ico_g_0400.png', 44: 'ico_g_0405.png', 45: 'ico_g_0401.png',
                        46: 'ico_g_0402.png', 47: 'ico_g_0403.png', 48: 'ico_g_0404.png', 49: 'ico_g_0406.png',
                        50: 'ico_g_0407.png', 51: 'ico_g_0408.png', 52: 'ico_g_0409.png', 53: 'ico_g_0410.png',
                        54: 'ico_g_1100.png', 55: 'ico_g_1101.png', 56: 'ico_g_1102.png', 57: 'ico_g_1103.png',
                        58: 'ico_g_1104.png', 59: 'ico_g_1105.png', 60: 'ico_g_1106.png', 61: 'ico_g_1107.png',
                        62: 'ico_g_0500.png', 63: 'ico_g_0501.png', 64: 'ico_g_0502.png', 65: 'ico_g_0503.png',
                        66: 'ico_g_1000.png', 67: 'ico_g_1001.png', 68: 'ico_g_1002.png', 69: 'ico_g_1003.png',
                        70: 'ico_g_1004.png', 71: 'ico_g_0600.png', 72: 'ico_g_0601.png', 73: 'ico_g_0602.png',
                        74: 'ico_g_0603.png', 75: 'ico_g_0605.png', 76: 'ico_g_0607.png', 77: 'ico_g_0604.png',
                        78: 'ico_g_0606.png', 79: 'ico_g_0700.png', 80: 'ico_g_0701.png', 81: 'ico_g_0702.png',
                        82: 'ico_g_0703.png', 83: 'ico_g_0704.png', 84: 'ico_g_0705.png', 85: 'ico_g_0706.png',
                        86: 'ico_g_0800.png', 87: 'ico_g_0801.png', 88: 'ico_g_0811.png', 89: 'ico_g_0812.png',
                        90: 'ico_g_0813.png', 91: 'ico_g_0803.png', 92: 'ico_g_0802.png', 93: 'ico_g_0806.png',
                        94: 'ico_g_0804.png', 95: 'ico_g_0807.png', 96: 'ico_g_0808.png', 97: 'ico_g_0809.png',
                        98: 'ico_g_0810.png', 102: 'ico_g_0325.png', 103: 'ico_g_0326.png', 107: 'ico_g_0203.png',
                        108: 'ico_g_0204.png', 109: 'ico_g_0205.png', 110: 'ico_g_0206.png', 111: 'ico_g_0209.png',
                        112: 'ico_g_0210.png', 113: 'ico_g_0211.png', 114: 'ico_g_0212.png', 115: 'ico_g_0208.png',
                        116: 'ico_g_0213.png', 117: 'ico_g_0214.png', 118: 'ico_g_0207.png', 135: 'ico_g_1008.png',
                        140: 'ico_g_0104.png', 141: 'ico_g_0004.png', 142: "ico_g_1000.png", 143: 'ico_g_0327.png',
                        144: "ico_g_0328.png", 145: "ico_g_0329.png", 146: "ico_g_0107.png", 147: "ico_g_1008.png",
                        148: "ico_g_1000.png", 149: "ico_g_1000.png", 150: "ico_g_1001.png", 151: "ico_g_1002.png",
                        152: "ico_g_1003.png", 153: "ico_g_1004.png"}

        # a dictionary of unique icons (ie. language specific) for use in achievements - only those activities that are graded
        unique_ico = {15: "ico_g_0107.png", 106: "ico_g_1007.png"}
        self.id2icon.update(unique_ico)

        self.lang_customized_icons = (11, 140, 12, 13)
        c_id = 0  # Add the home screens
        self.add_game(0, c_id, 0, 7, game000.Board, self.lang.d["About."], self.lang.d["Game info..."],
                      "ico_g_0000.png")
        self.games[-1].hidden = True
        #if self.badge_count > 0:
        self.add_game(141, c_id, 0, 7, game084.Board, self.lang.d["Achievements"], "", "ico_g_0004.png")
        self.add_game(3, c_id, 0, 7, game003.Board, self.lang.d["Language"], "", "ico_g_0003.png")
        self.add_game(1, c_id, 0, 7, game001.Board, self.lang.d["Credits"], "", "ico_g_0001.png")
        self.games[-1].hidden = True
        self.add_game(2, c_id, 0, 7, game002.Board, self.lang.d["Translators"], "", "ico_g_0001.png")
        self.games[-1].hidden = True
        """




        """
        c_id = 1  # alphabet games
        # if self.mainloop.lang.lang in ['en_gb','en_us','el','ru']:
        self.add_game(5, c_id, 0, 1, game017.Board, self.lang.d["Your Alphabet"], self.lang.d["Letter Flashcards"],
                      "ico_g_0100%s.png" % self.lang.ico_suffix)
        if self.mainloop.lang.lang[0:2] == "en":
            self.add_game(4, c_id, 0, 1, game037.Board, self.lang.d["English Alphabet"],
                          self.lang.d["Letter Flashcards"], "ico_g_0101.png")
        if self.mainloop.lang.lang[0:2] in ["en", "it", "pt", "de"]:
            # hardcoded label below since it only appears in English version of the game
            self.add_game(6, c_id, 0, 2, game068.Board, self.lang.d["Learn to Write"] + " - 1",
                          self.lang.d["Trace Letters"], "ico_g_0109.png")
            self.add_game(7, c_id, 0, 2, game010.Board, self.lang.d["Learn to Write"] + " - 2",
                          self.lang.d["Trace Letters"], "ico_g_0110.png")
        if self.mainloop.lang.lang == 'ru':
            self.add_game(8, c_id, 0, 2, game022.Board, self.lang.d["Learn to Write"], self.lang.d["local_kbrd"],
                          "ico_g_0111.png")
        if self.mainloop.lang.lang == 'el':
            self.add_game(9, c_id, 0, 2, game067.Board, self.lang.d["Learn to Write"], self.lang.d["local_kbrd"],
                          "ico_g_0112.png")
        # if self.mainloop.lang.lang not in self.lang.alphabet_26:
        # if self.mainloop.lang.lang[0:2] == "en":
        #    self.add_game(10,c_id, 0, 7, game014.Board,self.lang.d["Complete the ABC"]+ " - " + self.lang.d["English"],self.lang.d["Complete abc"],"ico_g_0103.png")
        self.add_game(11, c_id, 0, 1, game049.Board, self.lang.d["Complete the ABC"], self.lang.d["Lowercase Letters"],
                      "ico_g_0103%s.png" % self.lang.ico_suffix, variant=0)
        if self.lang.has_uc:
            self.add_game(140, c_id, 0, 1, game049.Board, self.lang.d["Complete the ABC"],
                          self.lang.d["Uppercase Letters"], "ico_g_0104%s.png" % self.lang.ico_suffix, variant=1)




        self.add_game(12, c_id, 0, 3, game047.Board, self.lang.d["Sorting Letters"], self.lang.d["Lowercase Letters"],
                      "ico_g_0105%s.png" % self.lang.ico_suffix, variant=0)
        if self.lang.has_uc:
            self.add_game(13, c_id, 0, 3, game047.Board, self.lang.d["Sorting Letters"] + " ",
                          self.lang.d["Uppercase Letters"], "ico_g_0106%s.png" % self.lang.ico_suffix, variant=1)



        if self.mainloop.lang.lang in ["en_GB", "en_US", "pl", "ru", "uk", "de"] and self.mainloop.fs_size[1] > 440:
            self.add_game(14, c_id, 0, 7, game016.Board, self.lang.d["Keyboard Skills"], self.lang.d["Touch Typing"],
                          "ico_g_0107.png")
        elif self.mainloop.fs_size[1] > 440:  # and self.mainloop.lang.lang not in ["en_gb","en_us","pl","ru"]:
            if self.mainloop.lang.lang == 'el':
                self.add_game(15, c_id, 0, 7, game077.Board, self.lang.d["Keyboard Skills"],
                              self.lang.d["Touch Typing"], "ico_g_0107.png")
            elif self.mainloop.lang.lang == "fr":
                self.add_game(146, c_id, 0, 7, game088.Board, self.lang.d["Keyboard Skills"],
                              self.lang.d["Touch Typing"], "ico_g_0107.png")

        if self.mainloop.lang.lang[0:2] not in ["ar", "he"]:
            c_id = 2  # word games
            self.add_game(17, c_id, 0, 1, game013.Board, self.lang.d["Word Builder"], "", "ico_g_0200.png")
            self.add_game(18, c_id, 0, 7, game023.Board, self.lang.d["Word Maze"], self.lang.d["Collect all"],
                          "ico_g_0201.png")
            self.add_game(19, c_id, 0, 7, game025.Board, self.lang.d["Word Maze + 4"], self.lang.d["Collect all"],
                          "ico_g_0202.png")
            if self.mainloop.lang.lang[0:2] in ["en", "pl", "uk", "ru", "fr", "de", "el", "sr"]:
                self.add_game(107, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Animals"],
                              self.lang.d["Complete the word"], "ico_g_0203.png", variant=0)
                self.add_game(110, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - People"],
                              self.lang.d["Complete the word"], "ico_g_0206.png", variant=3)
                self.add_game(114, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Jobs"],
                              self.lang.d["Complete the word"], "ico_g_0212.png", variant=7)
                self.add_game(109, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Body"],
                              self.lang.d["Complete the word"], "ico_g_0205.png", variant=2)
                self.add_game(115, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Clothes and Accessories"],
                              self.lang.d["Complete the word"], "ico_g_0208.png", variant=8)
                self.add_game(108, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Sports"],
                              self.lang.d["Complete the word"], "ico_g_0204.png", variant=1)
                self.add_game(111, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Actions"],
                              self.lang.d["Complete the word"], "ico_g_0209.png", variant=4)
                self.add_game(113, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Nature"],
                              self.lang.d["Complete the word"], "ico_g_0211.png", variant=6)
                self.add_game(116, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Fruits and Vegetables"],
                              self.lang.d["Complete the word"], "ico_g_0213.png", variant=9)
                self.add_game(118, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Food"],
                              self.lang.d["Complete the word"], "ico_g_0207.png", variant=11)
                self.add_game(117, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Transport"],
                              self.lang.d["Complete the word"], "ico_g_0214.png", variant=10)
                self.add_game(112, c_id, 0, 7, game082.Board, self.lang.d["Word Builder - Constructions"],
                              self.lang.d["Complete the word"], "ico_g_0210.png", variant=5)

        # tmpd = {17:"ico_g_0200.png",18:"ico_g_0201.png",19:"ico_g_0202.png",107:"ico_g_0203.png",110:"ico_g_0206.png"}
        # self.id2icon.update(tmpd)

        # "Learn to count"
        if self.uage < 4 or self.uage == 7:
            c_id += 1
            self.add_game(20, c_id, 0, 1, game038.Board, self.lang.d["Numbers"], self.lang.d["Number Flashcards"],
                          "ico_g_0300.png")
            self.add_game(22, c_id, 0, 1, game046.Board, self.lang.d["Learn to Count"], "", "ico_g_0301.png", variant=0)
            self.add_game(25, c_id, 0, 1, game027.Board, self.lang.d["Shopping List"], "", "ico_g_0302.png")
            self.add_game(43, c_id, 0, 3, game005.Board, self.lang.d["Sorting Numbers"], "", "ico_g_0400.png")
            self.add_game(45, c_id, 0, 3, game032.Board, self.lang.d["Number Comparison"], "", "ico_g_0401.png")
            self.add_game(44, c_id, 0, 2, game011.Board, self.lang.d["Even or Odd"], "", "ico_g_0405.png")
            self.add_game(102, c_id, 0, 3, game079.Board, self.lang.d["Number Spelling"], "", "ico_g_0325.png")
            self.add_game(21, c_id, 0, 3, game061.Board, self.lang.d["Number Spelling"],
                          self.lang.d["Match numbers to their spelling"], "ico_g_0323.png", variant=0)

        # "Addition"
        c_id += 1
        self.add_game(23, c_id, 0, 1, game046.Board, self.lang.d["Learn to Count"], self.lang.d["Basic Addition"],
                      "ico_g_0317.png", variant=1)
        self.add_game(35, c_id, 0, 5, game039.Board, self.lang.d["Find solution"], "", "ico_g_0309.png", variant=0)
        self.add_game(39, c_id, 0, 5, game019.Board, self.lang.d["Find missing number"], "", "ico_g_0313.png",
                      variant=0)
        self.add_game(31, c_id, 0, 6, game060.Board, self.lang.d["Maths Matching Game"], "", "ico_g_0319.png",
                      variant=0)  # 2
        self.add_game(26, c_id, 1, 4, game036.Board, self.lang.d["Plus or Minus"], "", "ico_g_0303.png")
        self.add_game(46, c_id, 1, 2, game033.Board, self.lang.d["Addition & Subtraction"], self.lang.d["Comparison"],
                      "ico_g_0402.png")
        self.add_game(103, c_id, 0, 7, game080.Board, self.lang.d["Addition Table"] + "  ", self.lang.d["answer_enter"],
                      "ico_g_0326.png")
        self.add_game(54, c_id, 3, 7, game073.Board, self.lang.d["Columnar addition"], self.lang.d["Demonstration"],
                      "ico_g_1100.png")
        self.add_game(55, c_id, 3, 7, game069.Board, self.lang.d["Columnar addition"], self.lang.d["DIY"],
                      "ico_g_1101.png")

        # "Subtraction"
        c_id += 1
        self.add_game(24, c_id, 0, 1, game046.Board, self.lang.d["Learn to Count"], self.lang.d["Basic Subtraction"],
                      "ico_g_0318.png", variant=2)
        self.add_game(36, c_id, 0, 7, game039.Board, self.lang.d["Find solution"], "", "ico_g_0310.png", variant=1)
        self.add_game(40, c_id, 0, 7, game019.Board, self.lang.d["Find missing number"], "", "ico_g_0314.png",
                      variant=1)
        self.add_game(32, c_id, 0, 7, game060.Board, self.lang.d["Maths Matching Game"], "", "ico_g_0320.png",
                      variant=1)  # 3
        self.add_game(26, c_id, 1, 4, game036.Board, self.lang.d["Plus or Minus"], "", "ico_g_0303.png")
        self.add_game(46, c_id, 1, 2, game033.Board, self.lang.d["Addition & Subtraction"], self.lang.d["Comparison"],
                      "ico_g_0402.png")
        self.add_game(56, c_id, 3, 7, game074.Board, self.lang.d["Columnar subtraction"], self.lang.d["Demonstration"],
                      "ico_g_1102.png")
        self.add_game(57, c_id, 3, 7, game070.Board, self.lang.d["Columnar subtraction"], self.lang.d["DIY"],
                      "ico_g_1103.png")

        # "Multiplication"
        if self.uage > 1:
            c_id += 1
        self.add_game(143, c_id, 2, 7, game085.Board, self.lang.d["Multiplication Table"],
                      self.lang.d["Find the product"], "ico_g_0327.png")
        self.add_game(27, c_id, 2, 7, game004.Board, self.lang.d["Multiplication Table"],
                      self.lang.d["Find the product"], "ico_g_0306.png")
        self.add_game(28, c_id, 2, 7, game034.Board, self.lang.d["Multiplication Table"] + " ",
                      self.lang.d["Find the multiplier"], "ico_g_0307.png")
        self.add_game(37, c_id, 2, 7, game039.Board, self.lang.d["Find solution"], "", "ico_g_0311.png", variant=2)
        self.add_game(41, c_id, 2, 7, game019.Board, self.lang.d["Find missing number"], "", "ico_g_0315.png",
                      variant=2)
        self.add_game(33, c_id, 2, 7, game060.Board, self.lang.d["Maths Matching Game"], "", "ico_g_0321.png",
                      variant=2)  # 4
        self.add_game(30, c_id, 2, 7, game031.Board, self.lang.d["Multiplication Table"] + "  ",
                      self.lang.d["answer_enter"], "ico_g_0324.png")
        self.add_game(144, c_id, 2, 7, game086.Board, self.lang.d["Multiplication Table"] + "  ",
                      self.lang.d["answer_enter"], "ico_g_0328.png")
        self.add_game(58, c_id, 3, 7, game075.Board, self.lang.d["Long multiplication"], self.lang.d["Demonstration"],
                      "ico_g_1104.png")
        self.add_game(59, c_id, 3, 7, game071.Board, self.lang.d["Long multiplication"], self.lang.d["DIY"],
                      "ico_g_1105.png")

        # "Division"
        if self.uage > 1:
            c_id += 1
        self.add_game(145, c_id, 2, 7, game087.Board, self.lang.d["Division"], " ", "ico_g_0329.png")
        self.add_game(29, c_id, 2, 7, game035.Board, self.lang.d["Division"], "", "ico_g_0308.png")
        self.add_game(38, c_id, 2, 7, game039.Board, self.lang.d["Find solution"], "", "ico_g_0312.png", variant=3)
        self.add_game(42, c_id, 2, 7, game019.Board, self.lang.d["Find missing number"], "", "ico_g_0316.png",
                      variant=3)
        self.add_game(34, c_id, 2, 7, game060.Board, self.lang.d["Maths Matching Game"], "", "ico_g_0322.png",
                      variant=3)  # 5
        self.add_game(60, c_id, 3, 7, game076.Board, self.lang.d["Long division"], self.lang.d["Demonstration"],
                      "ico_g_1106.png")
        self.add_game(61, c_id, 3, 7, game072.Board, self.lang.d["Long division"], self.lang.d["DIY"], "ico_g_1107.png")

        # "Decimals and fractions"
        if self.uage > 0:
            c_id += 1
        self.add_game(47, c_id, 1, 7, game026.Board, self.lang.d["Fractions"], self.lang.d["Comparison"],
                      "ico_g_0403.png")
        self.add_game(48, c_id, 4, 7, game020.Board, self.lang.d["Decimal Fractions"], self.lang.d["Comparison"],
                      "ico_g_0404.png")
        self.add_game(49, c_id, 1, 7, game056.Board, self.lang.d["Fraction Groups"], "", "ico_g_0406.png",
                      variant=0)  # new game
        self.add_game(50, c_id, 1, 7, game056.Board, self.lang.d["Fraction Groups"], "", "ico_g_0407.png",
                      variant=1)  # new game
        self.add_game(51, c_id, 1, 7, game056.Board, self.lang.d["Fraction Groups"], "", "ico_g_0408.png",
                      variant=2)  # new game

        self.add_game(53, c_id, 6, 7, game056.Board, self.lang.d["Ratios"], "", "ico_g_0410.png", variant=4)  # new game

        self.add_game(52, c_id, 5, 7, game056.Board, self.lang.d["Percentages"], "", "ico_g_0409.png",
                      variant=3)  # new game

        # "Shapes and Solids"
        if self.uage > 0:
            c_id += 1
        self.add_game(62, c_id, 1, 7, game009.Board, self.lang.d["Shapes"], self.lang.d["Shape Flashcards"],
                      "ico_g_0500.png")
        self.add_game(63, c_id, 1, 7, game043.Board, self.lang.d["Solids"], self.lang.d["Solid Flashcards"],
                      "ico_g_0501.png")
        self.add_game(64, c_id, 1, 7, game059.Board, self.lang.d["ShapeMaker"], self.lang.d["lets_see_what_you_draw"],
                      "ico_g_0502.png")
        self.add_game(65, c_id, 1, 7, game024.Board, self.lang.d["ShapeMaker"], self.lang.d["test_yourself"],
                      "ico_g_0503.png")

        # "Clock games"
        c_id += 1
        if self.mainloop.lang.lang == 'ca':
            self.add_game(104, c_id, 0, 7, game081.Board, "Rellotge amb horari en català", self.lang.d["Play_w_clock"],
                          "ico_g_1005.png")
        else:
            self.add_game(135, c_id, 0, 7, game081.Board, self.lang.d["Clock0"], self.lang.d["Play_w_clock"],
                          "ico_g_1008.png")
        self.add_game(66, c_id, 0, 7, game066.Board, self.lang.d["Clock0"], self.lang.d["Play_w_clock"],
                      "ico_g_1000.png", variant=0)
        self.add_game(142, c_id, 0, 7, game066.Board, self.lang.d["Clock0"], self.lang.d["Play_w_clock"],
                      "ico_g_1000.png", variant=2)
        self.add_game(67, c_id, 0, 7, game063.Board, self.lang.d["Clock1"] + " - " + self.lang.d["Read time"], "",
                      "ico_g_1001.png")
        self.add_game(68, c_id, 0, 7, game064.Board, self.lang.d["Clock2"] + " - " + self.lang.d["Set time"], "",
                      "ico_g_1002.png")
        self.add_game(69, c_id, 0, 7, game065.Board, self.lang.d["Clock2"] + " - " + self.lang.d["Set time"],
                      self.lang.d["txt_only"], "ico_g_1003.png", variant=0)

        self.add_game(70, c_id, 0, 7, game078.Board, self.lang.d["TimeMatching"], "", "ico_g_1004.png")

        if self.mainloop.lang.lang == 'ru':
            self.add_game(105, c_id, 0, 7, game066.Board, self.lang.d["Clock0 - Russian official time"],
                          self.lang.d["Russian official - subtitle"], "ico_g_1006.png", variant=1)
            self.add_game(106, c_id, 0, 7, game065.Board, self.lang.d["Clock2 - Russian official time"],
                          self.lang.d["Russian official - txt_only"], "ico_g_1007.png", variant=1)

        if self.mainloop.lang.lang == 'sr':
            c_id += 1
            self.add_game(147, c_id, 0, 7, game081.Board, self.lang.d["Clock0"], self.lang.d["Play_w_clock"],
                          "ico_g_1008.png", var2=1)
            self.add_game(148, c_id, 0, 7, game066.Board, self.lang.d["Clock0"], self.lang.d["Play_w_clock"],
                          "ico_g_1000.png", variant=0, var2=1)
            self.add_game(149, c_id, 0, 7, game066.Board, self.lang.d["Clock0"], self.lang.d["Play_w_clock"],
                          "ico_g_1000.png", variant=2, var2=1)
            self.add_game(150, c_id, 0, 7, game063.Board, self.lang.d["Clock1"] + " - " + self.lang.d["Read time"], "",
                          "ico_g_1001.png", var2=1)
            self.add_game(151, c_id, 0, 7, game064.Board, self.lang.d["Clock2"] + " - " + self.lang.d["Set time"], "",
                          "ico_g_1002.png", var2=1)
            self.add_game(152, c_id, 0, 7, game065.Board, self.lang.d["Clock2"] + " - " + self.lang.d["Set time"],
                          self.lang.d["txt_only"], "ico_g_1003.png", variant=0, var2=1)

            self.add_game(153, c_id, 0, 7, game078.Board, self.lang.d["TimeMatching"], "", "ico_g_1004.png")

        # "Art"
        c_id += 1
        self.add_game(71, c_id, 0, 7, game021.Board, self.lang.d["Paint"], "", "ico_g_0600.png")
        self.add_game(72, c_id, 0, 7, game042.Board, self.lang.d["Colour Matching"], self.lang.d["label the colours"],
                      "ico_g_0601.png")

        self.add_game(73, c_id, 0, 7, game062.Board, self.lang.d["Colour Matching"], "", "ico_g_0602.png")
        self.add_game(74, c_id, 0, 7, game051.Board, self.lang.d["Paint Mixer"], self.lang.d["Mixing RYB"],
                      "ico_g_0603.png")
        self.add_game(75, c_id, 2, 7, game052.Board, self.lang.d["Ink Mixer"], self.lang.d["Mixing CMY"],
                      "ico_g_0605.png")
        self.add_game(76, c_id, 2, 7, game055.Board, self.lang.d["Find the colour of the circle"],
                      self.lang.d["Adjust CMY"], "ico_g_0607.png")
        self.add_game(77, c_id, 2, 7, game053.Board, self.lang.d["Light Mixer"], self.lang.d["Mixing RGB"],
                      "ico_g_0604.png")
        self.add_game(78, c_id, 2, 7, game054.Board, self.lang.d["Find the colour of the circle"],
                      self.lang.d["Adjust RGB"], "ico_g_0606.png")

        # "Memory"
        c_id += 1
        self.add_game(79, c_id, 0, 7, game012.Board, self.lang.d["Follow the Arrows"],
                      self.lang.d["remember the directions"], "ico_g_0700.png")
        self.add_game(80, c_id, 0, 7, game006.Board, self.lang.d["Photographic Memory"], self.lang.d["Training"],
                      "ico_g_0701.png")
        self.add_game(81, c_id, 0, 7, game007.Board, self.lang.d["Photographic Memory"] + " ",
                      self.lang.d["Automatic Levels"], "ico_g_0702.png")
        self.add_game(82, c_id, 0, 7, game018.Board, self.lang.d["Match Animals Memory"], self.lang.d["Find pairs"],
                      "ico_g_0703.png", variant=0)
        self.add_game(83, c_id, 0, 7, game018.Board, self.lang.d["Match Fruits"], self.lang.d["Find pairs"],
                      "ico_g_0704.png", variant=1)
        self.add_game(84, c_id, 0, 7, game018.Board, self.lang.d["Match Vegetables"], self.lang.d["Find pairs"],
                      "ico_g_0705.png", variant=2)
        self.add_game(85, c_id, 0, 7, game018.Board, self.lang.d["Match Numbers"], self.lang.d["Find pairs"],
                      "ico_g_0706.png", variant=3)

        # "Games & Mazes"
        c_id += 1
        self.add_game(86, c_id, 0, 7, game029.Board, self.lang.d["Mouse Maze"], self.lang.d["Let's have some cheese"],
                      "ico_g_0800.png")
        self.add_game(87, c_id, 0, 7, game028.Board, self.lang.d["Sheep Maze"], self.lang.d["Find the rest"],
                      "ico_g_0801.png")

        self.add_game(88, c_id, 0, 7, game060.Board, self.lang.d["Match Animals"],
                      self.lang.d["Find all matching animals"], "ico_g_0811.png", variant=4)  # 0
        self.add_game(89, c_id, 0, 7, game060.Board, self.lang.d["Match Animals"] + " 2",
                      self.lang.d["Match animals to their shadows"], "ico_g_0812.png", variant=5)  # 1
        self.add_game(90, c_id, 0, 7, game008.Board, self.lang.d["Match Animals"] + " 3",
                      self.lang.d["help me find my shadow"], "ico_g_0813.png")

        self.add_game(91, c_id, 0, 7, game041.Board, self.lang.d["Connect"] + " ", self.lang.d["Balloons with threads"],
                      "ico_g_0803.png")
        self.add_game(92, c_id, 0, 7, game040.Board, self.lang.d["Connect"], self.lang.d["Numbers"], "ico_g_0802.png")
        self.add_game(93, c_id, 0, 7, game050.Board, self.lang.d["Connect"], self.lang.d["Numbers"] + " 2",
                      "ico_g_0806.png")
        self.add_game(94, c_id, 0, 7, game015.Board, self.lang.d["Fifteen"], self.lang.d["With a Twist"],
                      "ico_g_0804.png")
        self.add_game(95, c_id, 0, 7, game045.Board, self.lang.d["Fifteen"], self.lang.d["With a Twist"],
                      "ico_g_0807.png")

        self.add_game(96, c_id, 0, 7, game044.Board, self.lang.d["Sliced Images"], self.lang.d["Sliced Animals"],
                      "ico_g_0808.png", variant=0)
        self.add_game(97, c_id, 0, 7, game044.Board, self.lang.d["Sliced Images"], self.lang.d["Sliced Fruits"],
                      "ico_g_0809.png", variant=1)
        self.add_game(98, c_id, 0, 7, game044.Board, self.lang.d["Sliced Images"], self.lang.d["Sliced Numbers"],
                      "ico_g_0810.png", variant=2)

        # self.find_duplicates()
        """

    def find_duplicates(self):
        mx = 0
        for each in self.games:
            if each.dbgameid > mx:
                mx = each.dbgameid
            for every in self.games:
                if each.dbgameid == every.dbgameid:
                    if each != every:
                        print(each.dbgameid)
        print("max = %i" % mx)

        # new_game = MenuItem(self,dbgameid,len(self.games),cat_id,title,subtitle,constructor,self.icon_size,img_src,variant)
        # self.games.append(new_game)

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
            y += each_item.h + self.y_margin

            each_item.update()

        x = self.x_margin
        y = self.y_margin + l.misio_pos[3] + self.scroll_r + self.arrow_h
        c = 5
        for each_item in self.games_current:
            each_item.rect.topleft = [x, y]
            each_item.update()
            y += self.icon_size + self.y_margin
            c += 10

        # if category with current game is shown show the tab, otherwise hide it (move it off screen)
        if self.games[self.active_game_id] in self.games_in_current_cat:
            bmr_top = (self.tab_game_id + self.tab_r_scroll) * (self.icon_size + self.y_margin) + 2 + l.misio_pos[
                3] + self.arrow_h
        else:
            bmr_top = -100
        bml_top = (self.active_cat + self.tab_l_scroll) * (self.icon_size + self.y_margin) + 2 + l.misio_pos[
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
        self.game_h = len(self.games_current) * (self.icon_size + self.y_margin)  # -self.y_margin
