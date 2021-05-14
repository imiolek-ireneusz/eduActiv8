# -*- coding: utf-8 -*-

import os
import pygame
import classes.extras as ex


class BaseButton(pygame.sprite.Sprite):
    def __init__(self, panel, pos_x, pos_y, width, height, img_src_1="", img_src_2="", img_src_3="", rev=False):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.pos = [pos_x, pos_y]
        self.panel = panel
        self.color = self.panel.bg_color

        if self.panel.mainloop.scheme is not None:
            if self.panel.mainloop.scheme.dark:
                self.scheme_dir = "black"
            else:
                self.scheme_dir = "black"
        else:
            self.scheme_dir = "black"
        self.update_size(width, height)

        self.img_src_1 = img_src_1
        self.img_src_2 = img_src_2
        self.img_src_3 = img_src_3
        self.img_4 = None
        self.update_fonts()
        self.hasimg = False
        self.hover = False

        if self.btntype == "imgbtn":
            self.load_images(rev)
        elif self.btntype in ["levels", "titles"]:
            self.update_levels()

    def update_fonts(self):
        if self.btn_id in [2, 6]:
            self.font = self.panel.fonts[0]
            self.font2 = self.panel.fonts[1]
            self.font3 = self.panel.fonts[2]
            self.font4 = self.panel.fonts[3]

    def update_size(self, width, height):
        self.image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.rect.width = width

    def on_mouse_over(self):
        pass

    def on_mouse_out(self):
        pass


class Button(BaseButton):
    def __init__(self, panel, pos_x, pos_y, width, height, btntype="imgbtn", img_src_1="", img_src_2="", img_src_3="",
                 rev=False):
        self.btn_id = len(panel.btns)
        self.panel = panel
        self.btntype = btntype
        BaseButton.__init__(self, panel, pos_x, pos_y, width, height, img_src_1, img_src_2, img_src_3, rev)

    def load_images(self, rev):
        self.rev = rev
        self.img_pos = (0, 0)
        self.img_1 = pygame.image.load(os.path.join('res', 'images', "info_bar", "mask", self.img_src_1)).convert_alpha()
        self.img_1.fill(self.panel.mainloop.cl.info_buttons_col, special_flags=pygame.BLEND_ADD)
        self.img_2 = pygame.image.load(os.path.join('res', 'images', "info_bar", "mask", self.img_src_2)).convert_alpha()
        self.img_2.fill(self.panel.mainloop.cl.info_buttons_col, special_flags=pygame.BLEND_ADD)
        self.img_4 = pygame.image.load(
            os.path.join('res', 'images', "info_bar", "decor", self.img_src_2)).convert_alpha()

        if self.img_src_3 != "":
            self.img_3 = pygame.image.load(
                os.path.join('res', 'images', "info_bar", self.img_src_3)).convert_alpha()
        if rev:
            self.img_1 = pygame.transform.flip(self.img_1, 1, 0)
            self.img_2 = pygame.transform.flip(self.img_2, 1, 0)
            self.img_4 = pygame.transform.flip(self.img_4, 1, 0)

        self.img = self.img_2
        self.hasimg = True
        self.update()

    def reload_colors(self):
        self.load_images(self.rev)
        self.update_fonts()

    def on_mouse_over(self):
        if not self.hover:
            self.hover = True
            self.panel.mainloop.redraw_needed[1] = True
            if self.hasimg:
                if not (((self.btn_id == 1 or self.btn_id == 7)
                         and self.panel.level.lvl == self.panel.mainloop.game_board.min_level)
                        or ((self.btn_id == 3 or self.btn_id == 8)
                            and self.panel.level.lvl == self.panel.level.lvl_count)):
                    self.img = self.img_1

    def on_mouse_out(self):
        if self.hover:
            self.hover = False
            self.panel.mainloop.redraw_needed[1] = True
            if self.hasimg:
                self.img = self.img_2

    def update_levels(self):
        if 1 < self.panel.level.games_per_lvl != 99:
            text2 = self.font2.render("%s/%s" % (self.panel.level.game_step, self.panel.level.games_per_lvl), 1,
                                      self.panel.font_color)
            textpos2 = text2.get_rect(centerx=self.image.get_width() // 2)
            self.image.blit(text2, (textpos2[0], 40))
            lvl_lift = -9
        else:
            lvl_lift = 0

        if self.panel.level.lvl_count > 1:
            if self.panel.level.completed > 0:
                font_color = self.panel.font_color2
            else:
                font_color = self.panel.font_color3
            text = self.font.render("%s" % (self.panel.level.lvl), 1, font_color)
            textpos1 = text.get_rect(centerx=self.image.get_width() // 2)
            self.image.blit(text, (textpos1[0], lvl_lift))

    def update_title(self):
        text = self.font3.render("%s" % (self.panel.title), 1, self.panel.font_color)
        text2 = self.font4.render("%s" % (self.panel.subtitle), 1, self.panel.font_color1)
        text3 = self.font4.render("%s" % (self.panel.game_id), 1, self.panel.font_color4)
        tw1 = self.font3.size(self.panel.title)[0]
        tw2 = self.font4.size(self.panel.subtitle)[0]
        tw3 = self.font4.size(self.panel.game_id)[0]
        if self.panel.mainloop.lang.ltr_text:
            ttx = 0
            stx = 0
            idx = self.panel.title_space - tw3 - 10
        else:
            ttx = self.panel.title_space - tw1 - 10
            stx = self.panel.title_space - tw2 - 10
            idx = 0

        if self.panel.title_space == 0 or tw1 < self.panel.title_space:
            self.image.blit(text, (ttx, 2))
            if tw2 < self.panel.title_space:
                self.image.blit(text2, (stx, 39))
        self.image.blit(text3, (idx, 39))

    def update(self):
        self.image.fill(self.color)
        if self.btntype == "imgbtn":
            self.image.blit(self.img, self.img_pos)
            if self.img_4 is not None:
                self.image.blit(self.img_4, self.img_pos)
        elif self.btntype == "levels":
            self.update_levels()
        elif self.btntype == "titles":
            self.update_title()


class InfoBar:
    def __init__(self, mainloop):
        self.mainloop = mainloop
        self.mouse_over = False
        self.game_board = None
        self.home_btns_w = 50 + 66
        self.last_hover = None
        self.fonts = []
        self.create()

    def create(self):
        self.btns = []
        """
        self.font_color = (255, 75, 0, 0)
        self.font_color1 = (255, 125, 0, 0)
        self.font_color4 = (255, 175, 0, 0)
        self.font_color2 = (225, 75, 0, 0)
        self.font_color3 = (255, 175, 0, 0)
        """

        self.load_font_colors()

        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.bg_color = (0, 0, 0, 0)
            else:
                self.bg_color = (255, 255, 255, 0)
            self.font_color = self.mainloop.scheme.info_font_color0
            self.font_color1 = self.mainloop.scheme.info_font_color1

            self.font_color2 = self.mainloop.scheme.info_font_color2
            self.font_color3 = self.mainloop.scheme.info_font_color3
        else:
            self.bg_color = (255, 255, 255, 0)

        self.hidden = False
        self.close_dialog = False
        self.margin_top = 3  # 13
        self.lang = self.mainloop.lang
        self.title_space = 0
        self.title = ""
        self.subtitle = ""
        self.game_id = ""
        self.btn_list = pygame.sprite.LayeredUpdates()
        self.reset_buttons()
        self.update_fonts()

    def load_font_colors(self):
        self.font_color = ex.hsv_to_rgb(self.mainloop.cl.color_sliders[5][0] * 16, 255, 220)
        self.font_color1 = ex.hsv_to_rgb(self.mainloop.cl.color_sliders[5][0] * 16, 255, 255)
        self.font_color4 = ex.hsv_to_rgb(self.mainloop.cl.color_sliders[5][0] * 16, 150, 255)
        self.font_color2 = self.font_color
        self.font_color3 = self.font_color4

    def update_fonts(self):
        self.fonts = []
        points = int(round((60 * 72 / 96), 0))
        sizes = [points, points // 2, int(points / 1.9), int(points / 2.6)]
        for i in range(2, 4):
            sizes[i] = int(sizes[i] * self.mainloop.config.font_multiplier)

        for i in range(4):
            self.fonts.append(pygame.font.Font(
                os.path.join('res', 'fonts', self.mainloop.config.font_dir, self.mainloop.config.font_name_1),
                sizes[i]))

        for each in self.btns:
            each.update_fonts()
        self.reset_titles()

    def new_game(self, game_board, screen):
        self.game_board = game_board
        self.level = self.game_board.level
        self.screen = screen
        self.height = self.mainloop.sizer.info_bar_h
        self.height_o = self.mainloop.sizer.info_bar_offset_h
        self.width = self.mainloop.sizer.info_bar_pos[2]  # self.game_board.layout.screen_w - self.m_offset
        if len(self.btns) == 0:
            self.add_btns()
        self.layout_update()
        self.game_board.dialog.layout_update()

    def hover(self, pos, l):
        for btn in self.btns:
            if btn.rect.topleft[0] < (pos[0]) < (btn.rect.topleft[0] + btn.width) and btn.rect.topleft[
                1] < (pos[1] - l.info_bar_pos[1]) < (btn.rect.topleft[1] + btn.height):
                if btn.hasimg:
                    return btn
        return None

    def reload_colors(self):
        self.update_me = True
        self.mainloop.redraw_needed = [True, True, True]
        for each in self.btns:
            if each.btntype == "imgbtn":
                each.reload_colors()

    def handle(self, event, layout, mainloop):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
                btn = self.hover(pos, layout)
                self.mainloop.mbtndno = btn

        if event.type == pygame.MOUSEBUTTONUP:
            # Change the x/y screen coordinates to grid coordinates
            pos = event.pos
            btn = self.hover(pos, layout)
            # if left button pressed:
            if event.button == 1 and self.mainloop.mbtndno == btn:
                self.mainloop.game_board.drag = False
                if btn is not None:
                    if btn.btn_id == 0:
                        btn.img = btn.img_2
                        self.game_board.check_result()
                    elif btn.btn_id == 1:
                        if self.level.lvl > self.mainloop.game_board.min_level:
                            self.level.manual_leveldown()
                        if self.level.lvl == self.mainloop.game_board.min_level:
                            btn.img = btn.img_2
                    elif btn.btn_id == 3:
                        if self.level.lvl == self.level.lvl_count:
                            btn.img = btn.img_2
                        else:
                            self.level.manual_levelup()
                    elif btn.btn_id == 4:  # clicked on close button
                        mainloop.dialog.show_dialog(0, self.lang.d["Do you want to exit the game?"])
                    elif btn.btn_id == 5:
                        self.level.load_level()
                        self.mainloop.sfx.play(1)
                    elif btn.btn_id == 7:
                        if self.level.lvl == self.mainloop.game_board.min_level:
                            btn.img = btn.img_2
                        else:
                            self.level.chapter_down()
                    elif btn.btn_id == 8:
                        if self.level.lvl == self.level.lvl_count:
                            btn.img = btn.img_2
                        else:
                            self.level.chapter_up()
                    elif btn.btn_id == 9:
                        self.show_info_dialog()
                    elif btn.btn_id == 11:
                        self.show_menu()
            elif event.button > 1:
                if btn is not None:
                    if btn.btn_id == 11:
                        self.show_menu(True)
                    elif btn.btn_id == 3 or btn.btn_id == 8:
                        if self.level.lvl < self.level.lvl_count:
                            self.level.lvl = self.level.lvl_count
                            btn.img = btn.img_2
                            self.level.load_level()
                    elif btn.btn_id == 1 or btn.btn_id == 7:
                        if self.level.lvl > 1:
                            self.level.lvl = 1
                            btn.img = btn.img_2
                            self.level.load_level()

        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_over()
            if self.mainloop.info.title != self.mainloop.m.games[self.mainloop.m.active_game_id].title:
                self.reset_titles()
            if self.hidden:
                if not self.close_dialog:
                    self.buttons_restore()
            pos = event.pos
            btn = self.hover(pos, layout)
            if btn is not None:
                if self.last_hover is not None and self.last_hover != btn:
                    self.last_hover.on_mouse_out()
                self.last_hover = btn
                btn.on_mouse_over()
            else:
                if self.last_hover is not None:
                    self.last_hover.on_mouse_out()
                    self.last_hover = None
                self.close_dialog = False

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
        self.mouse_over = True

    def on_mouse_out(self):
        if self.mouse_over:
            self.mouse_over = False
        if self.last_hover is not None:
            self.last_hover.on_mouse_out()

    def show_menu(self, start=False):
        self.mainloop.redraw_needed = [True, True, True]
        if start:
            self.mainloop.menu_level = 0
        else:
            if self.mainloop.menu_level == 4:
                self.mainloop.menu_level = 3
            elif self.mainloop.menu_level == 3:
                if self.mainloop.m.current_inner:
                    self.mainloop.m.current_inner = False
                    self.mainloop.menu_level = 2
                else:
                    self.mainloop.m.current_inner = False
                    self.mainloop.menu_level = 1
            elif self.mainloop.menu_level == 2:
                self.mainloop.menu_level = 1
            else:
                self.mainloop.menu_level = 0
        if self.mainloop.menu_level == 0:
            self.mainloop.game_board.vis_buttons = (0, 0, 0, 0, 1, 0, 1, 0, 0)
            self.buttons_restore()
            self.mainloop.m.start_hidden_game(0)
        else:
            self.title = ""
            self.subtitle = ""
            if self.mainloop.m.game_dbid == 271:
                self.mainloop.m.start_hidden_game(272)
            else:
                self.mainloop.m.start_hidden_game(271)
        self.realign()

    def reset_titles(self):
        if not self.close_dialog:
            # book 1
            if self.mainloop.m.game_constructor != "game000.Board":
                self.title = self.mainloop.m.games[self.mainloop.m.active_game_id].title
                self.subtitle = self.mainloop.m.games[self.mainloop.m.active_game_id].subtitle
            else:
                self.title = ""
                self.subtitle = ""

            if self.mainloop.m.game_constructor not in ["game000.Board", "game001.Board", "game002.Board",
                                                        "game003.Board", "game004.Board", "game113.Board"]:
                self.game_id = "#%s/%03i" % (
                self.mainloop.m.games[self.mainloop.m.active_game_id].game_constructor[4:7],
                self.mainloop.m.games[self.mainloop.m.active_game_id].dbgameid)
            else:
                self.game_id = ""

            self.mainloop.redraw_needed[1] = True

    def resetbtns(self):
        for btn in self.btns:
            if btn.hasimg:
                btn.img = btn.img_2

    def add_btn(self, panel, pos_x, pos_y, btn_size_x, btn_size_y, btntype="imgbtn", img_src_1="", img_src_2="",
                img_src_3="", rev=False):
        new_button = Button(panel, pos_x, pos_y, btn_size_x, btn_size_y, btntype, img_src_1, img_src_2, img_src_3, rev)
        self.btns.append(new_button)
        self.btn_list.add(new_button)

    def add_btns(self):
        self.add_btn(self, self.home_btns_w + 122, 5 + self.margin_top, 84, 66, "imgbtn", "info_ok2.png", "info_ok1.png")
        self.add_btn(self, self.width - 315, 5 + self.margin_top, 66, 66, "imgbtn", "info_arrow2.png",
                     "info_arrow1.png")
        self.add_btn(self, self.width - 253, 5 + self.margin_top, 74, 66, "levels")  # level number label
        self.add_btn(self, self.width - 182, 5 + self.margin_top, 66, 66, "imgbtn", "info_arrow2.png",
                     "info_arrow1.png", "", True)
        self.add_btn(self, self.width - 71, 5 + self.margin_top, 66, 66, "imgbtn", "info_close2.png", "info_close1.png")
        self.add_btn(self, self.home_btns_w + 222, 5 + self.margin_top, 66, 66, "imgbtn", "info_refresh2.png", "info_refresh1.png")
        title_width = self.width
        self.add_btn(self, self.home_btns_w + 300, 5 + self.margin_top, title_width, 69, "titles")

        self.add_btn(self, self.width - 351, 5 + self.margin_top, 33, 66, "imgbtn", "info_lvls2.png", "info_lvls1.png")
        self.add_btn(self, self.width - 113, 5 + self.margin_top, 33, 66, "imgbtn", "info_lvls2.png", "info_lvls1.png",
                     "", True)

        self.add_btn(self, self.home_btns_w + 5, 5 + self.margin_top, 66, 66, "imgbtn", "info2.png", "info1.png") #9
        self.btns[-1].hidden = False

        # add a layer of solid colour behind right-aligned buttons
        self.add_btn(self, self.width - 323, 5 + self.margin_top, 323, 66, "btn_bg")# 13 - 10

        #self.add_btn(self, 25, -200, 66, 66, "imgbtn", "home1.png", "home2.png")  # 11
        self.add_btn(self, 25, -200, 66, 66, "imgbtn", "home2.png", "home1.png")  # 11

        self.btns[-1].hidden = False

        self.btn_list.move_to_back(self.btns[10])
        self.btn_list.move_to_back(self.btns[6])

    def layout_update(self):
        self.btns[6].update_size(self.width, self.btns[6].rect.height)
        self.btns[1].rect.left = self.width - 315
        self.btns[2].rect.left = self.width - 253
        self.btns[3].rect.left = self.width - 182
        self.btns[4].rect.left = self.width - 71
        self.btns[7].rect.left = self.width - 351
        self.btns[8].rect.left = self.width - 113
        self.btns[9].rect.left = self.home_btns_w
        self.btns[10].rect.left = self.width - 315
        self.reset_alignment()
        self.check_btn_tops()

    def title_only(self):
        self.hide_buttons(0, 0, 0, 0, 0, 0, 1, 0, 0)
        self.mainloop.redraw_needed[1] = True
        self.hidden = True
        self.btn_list.move_to_front(self.btns[6])
        self.btns[9].hidden = True
        self.layout_update()
        self.title_space = self.width - 10

    def show_info_dialog(self):
        self.mainloop.game_board.show_info_dialog()
        self.resetbtns()

    def buttons_restore(self):
        a = self.mainloop.game_board.vis_buttons
        self.hide_buttonsa(a)
        self.btns[9].hidden = False
        self.mainloop.redraw_needed[1] = True
        self.hidden = False
        self.btn_list.move_to_back(self.btns[6])
        self.layout_update()

    def realign(self):
        if self.mainloop.menu_level > 0:
            self.home_btns_w = 50 + 66
            self.btns[11].rect.top = 5 + self.margin_top
        else:
            self.home_btns_w = 0
            self.btns[11].rect.top = -200
        if self.mainloop.menu_level < 3:
            self.reset_titles()
        self.rescale_title_space()
        self.resetbtns()
        self.buttons_restore()
        self.reset_alignment()
        self.align_to_left()

    def align_to_left(self):
        self.btns[9].rect.left = self.home_btns_w
        if not self.btns[9].hidden and self.mainloop.game_board.show_info_btn:
            info_w = 66 + 10
        else:
            info_w = 0
        if self.visible_btns[8] == 0:
            if self.visible_btns[0] == 0 and self.visible_btns[5] == 1:
                self.btns[5].rect.left = self.home_btns_w + 5 + info_w
                self.btns[6].rect.left = self.home_btns_w + 78 + info_w
            elif self.visible_btns[0] == 0 and self.visible_btns[5] == 0:
                self.btns[6].rect.left = self.home_btns_w + 10 + info_w
            elif self.visible_btns[0] == 1 and self.visible_btns[5] == 0:
                self.btns[0].rect.left = self.home_btns_w + 5 + info_w
                self.btns[6].rect.left = self.home_btns_w + 105 + info_w
        else:
            if self.visible_btns[0] == 0 and self.visible_btns[5] == 1:
                self.btns[5].rect.left = self.home_btns_w + 142 + info_w - 50 # 5+117+20
                self.btns[6].rect.left = self.home_btns_w + 215 + info_w - 50  # 78+117+20
            elif self.visible_btns[0] == 0 and self.visible_btns[5] == 0:
                self.btns[6].rect.left = self.home_btns_w + 142 + info_w - 50  # 5+117+20
            elif self.visible_btns[0] == 1 and self.visible_btns[5] == 0:
                self.btns[0].rect.left = self.home_btns_w + 142 + info_w - 50  # 5+117+20
                self.btns[6].rect.left = self.home_btns_w + 242 + info_w - 50  # 105+117+20

    def reset_alignment(self):
        self.btns[9].rect.left = self.home_btns_w

        if not self.btns[9].hidden and self.mainloop.game_board.show_info_btn:
            info_w = 66 + 10
        else:
            info_w = 0
        if self.visible_btns[8] == 0:
            self.btns[0].rect.left = self.home_btns_w + 5 + info_w
            self.btns[5].rect.left = self.home_btns_w + 105 + info_w
            self.btns[6].rect.left = self.home_btns_w + 183 + info_w
        else:
            self.btns[0].rect.left = self.home_btns_w + 122 + info_w
            self.btns[5].rect.left = self.home_btns_w + 222 + info_w
            self.btns[6].rect.left = self.home_btns_w + 300 + info_w

    def align_to_right(self):
        if self.visible_btns[7] == 1:
            self.btns[1].rect.left = self.width - 315
            self.btns[2].rect.left = self.width - 253
            self.btns[3].rect.left = self.width - 182
        else:
            self.btns[1].rect.left = self.width - 288
            self.btns[2].rect.left = self.width - 223
            self.btns[3].rect.left = self.width - 148

    def hide_buttons(self, a, b, c, d, e, f, g, h, i):
        self.visible_btns = [a, b, c, d, e, f, g, h, i]

    def hide_buttonsa(self, a):
        self.visible_btns = a

    def reset_buttons(self):
        self.visible_btns = [1, 1, 1, 1, 1, 1, 1, 0, 0]

    def check_btn_tops(self):
        #                      0  1          2     3            4     5      6       7             8
        # self.visible_btns = [ok,left_arrow,levels,right_arrow,close,refresh,titles, fast forward, keyboard]
        # self.visible_btns = [1,1,1,1,1,1,1,0,0]
        # if sum(self.visible_btns) < 7:
        vb = self.visible_btns
        if self.mainloop.game_board.show_info_btn and not self.btns[9].hidden:
            self.btns[9].rect.top = 5 + self.margin_top
        else:
            self.btns[9].rect.top = -200

        for i in range(9):
            if vb[i] == 0:
                if i < 7:
                    self.btns[i].rect.top = -200
                elif i == 7:
                    self.btns[7].rect.top = -200
                    self.btns[8].rect.top = -200
                else:
                    self.btns[9].rect.top = -200
            else:
                if i < 7:
                    self.btns[i].rect.top = 5 + self.margin_top
                elif i == 7:
                    self.btns[7].rect.top = 5 + self.margin_top
                    self.btns[8].rect.top = 5 + self.margin_top
                else:
                    self.btns[9].rect.top = 5 + self.margin_top

        if vb[0] == 0 or vb[5] == 0 or vb[8] == 0:
            self.align_to_left()
        if vb[7] == 0:
            self.align_to_right()

        # adjusting the position of the background strip behind the right-aligned buttons
        if vb[1:4] == [0, 0, 0] and vb[7] == 0:
            self.btns[10].rect.left = self.width - 71 - 5
        elif vb[7] == 1:
            self.btns[10].rect.left = self.width - 351 - 5
        elif vb[1] == 1 and vb[7] == 0:
            self.btns[10].rect.left = self.width - 288 - 5
        elif vb[1] == 0 and vb[2] == 1:
            self.btns[10].rect.left = self.width - 223 - 5
        else:
            self.btns[10].rect.left = self.width - 5
        # title space
        self.rescale_title_space()

    def rescale_title_space(self):
        if self.hidden is False or self.close_dialog:
            self.title_space = self.btns[10].rect.left - self.btns[6].rect.left
        elif self.hidden is True and self.close_dialog is False:
            self.title_space = self.width - 10

    def draw(self, screen):
        # draw info bar
        color = self.font_color
        hs = 80
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                color = (255, 255, 255)
        screen.fill(self.bg_color)

        if self.mainloop.m.game_constructor != "game000.Board":
            pygame.draw.line(screen, color, [0, hs], [self.game_board.layout.screen_w, 80], 2)

        for each_item in self.btns:
            each_item.update()

        self.btn_list.draw(screen)
