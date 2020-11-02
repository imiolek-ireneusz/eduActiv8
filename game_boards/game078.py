# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.clock


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 3, 16)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 4, 2)

    def create_game_objects(self, level=1):
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.ai_enabled = False
        self.hand_id = 0
        self.hand_coords = [[], []]
        self.board.draw_grid = False

        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.colon_col = (255, 255, 255)
            else:
                self.colon_col = (0, 0, 0)
            self.h_col = self.mainloop.scheme.color3
            self.m_col = self.mainloop.scheme.color4
        else:
            self.colon_col = (0, 0, 0)
            self.h_col = ex.hsv_to_rgb(225, 190, 220)
            self.m_col = ex.hsv_to_rgb(170, 190, 220)

        color1 = ex.hsv_to_rgb(225, 70, 230)
        color3 = ex.hsv_to_rgb(225, 255, 255)
        color5 = ex.hsv_to_rgb(225, 180, 240)
        color7 = ex.hsv_to_rgb(225, 10, 255)

        color2 = ex.hsv_to_rgb(170, 70, 230)
        color4 = ex.hsv_to_rgb(170, 255, 255)
        color6 = ex.hsv_to_rgb(170, 180, 240)
        color8 = ex.hsv_to_rgb(170, 10, 255)

        self.colors = [color1, color2]
        self.colors2 = [color3, color4]
        self.colors3 = [color5, color6]
        self.colors4 = [color7, color8]

        if self.level.lvl == 1:
            data = [4, 2, True, True, False, False, True, False, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = [0]
        elif self.level.lvl == 2:
            data = [4, 2, True, True, False, False, True, False, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60, 15)
        elif self.level.lvl == 3:
            data = [4, 2, True, True, False, False, False, True, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60, 5)
        elif self.level.lvl == 4:
            data = [4, 2, True, True, False, False, False, True, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60, 5)
        elif self.level.lvl == 5:
            data = [4, 2, True, True, False, False, False, False, False, True, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 6:
            data = [4, 2, True, True, True, False, True, False, False, True, True, 15]
            h_pool = range(13, 24)
            m_pool = [0]
        elif self.level.lvl == 7:
            data = [4, 2, True, True, True, False, False, True, False, True, True, 15]
            h_pool = list(range(13, 24))
            h_pool.append(0)
            m_pool = range(0, 60, 5)
        elif self.level.lvl == 8:
            data = [4, 2, True, True, True, False, False, False, False, True, True, 25]
            h_pool = range(0, 24)
            m_pool = range(0, 60)
        elif self.level.lvl == 9:
            data = [4, 2, True, True, False, False, False, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 10:
            data = [4, 2, True, True, False, False, False, True, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 11:
            data = [4, 2, True, True, False, False, True, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 12:
            data = [4, 2, True, False, False, False, False, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 13:
            data = [4, 2, True, False, False, True, False, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 14:
            data = [4, 2, True, True, False, False, False, False, True, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 15:
            data = [4, 2, True, True, False, False, True, False, True, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 16:
            data = [4, 2, True, True, False, False, False, False, True, False, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60)

        # visual display properties
        self.show_outer_ring = data[2]
        self.show_minutes = data[3]
        self.show_24h = data[4]
        self.show_only_quarters_h = data[5]
        self.show_only_quarters_m = data[6]
        self.show_only_fives_m = data[7]
        self.show_roman = data[8]
        self.show_highlight = data[9]
        self.show_hour_offset = data[10]

        self.disp_counter = 0
        self.disp_len = 1
        self.found = 0
        self.clicks = 0
        self.square_count = data[0] * data[1]
        self.history = [None, None]
        self.time = []
        for i in range(4):
            tt = [random.choice(h_pool), random.choice(m_pool)]
            while tt in self.time:
                tt = [random.choice(h_pool), random.choice(m_pool)]
            self.time.append(tt)
        self.tm = self.time[0][:]

        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

        self.disp_counter = 0
        self.disp_len = 1
        self.completed_mode = False
        self.font_size = 0
        self.data = data

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.units = []
        choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        self.size = self.board.scale
        self.clock_fonts = []
        self.points = int(round((self.board.scale * 72 / 96) * 1.2, 0))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (42 * self.size / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (21 * self.size / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSans.ttf'),
                                                 (int(self.points / (self.board.scale / (21 * self.size / 500.0))))))

        slots = []
        for j in range(0, data[1]):
            for i in range(0, data[0]):
                slots.append([i, j])
        random.shuffle(slots)
        self.center = [self.size // 2, self.size // 2]
        switch = self.square_count // 2
        h = random.randint(0, 255)
        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
            img_style = "bb"
            self.default_bg_color = ex.hsv_to_rgb(h, 200, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 230, 90)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 150, 200), ]

            self.selected_color = ex.hsv_to_rgb(h, 150, 50)
            self.selected_font_color = [ex.hsv_to_rgb(h, 150, 100), ]
        else:
            img_style = "wb"
            self.default_bg_color = ex.hsv_to_rgb(h, 150, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 80, self.mainloop.cl.bg_color_v)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 200, self.mainloop.cl.font_color_v), ]

            self.selected_color = ex.hsv_to_rgb(h, 50, self.mainloop.cl.bg_color_v)
            self.selected_font_color = [ex.hsv_to_rgb(h, 50, 250), ]

        self.dc_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        if self.mainloop.m.game_variant == 4:
            self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s150.png" % img_style)
        elif self.mainloop.m.game_variant == 5:
            self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s20.png" % img_style)

        door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        for i in range(self.square_count):
            if i < switch:
                self.board.add_universal_unit(grid_x=slots[i][0], grid_y=slots[i][1], grid_w=1, grid_h=1, txt="",
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=door_bg_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=self.font_color,
                                              bg_tint_color=self.default_bg_color, fg_tint_color=self.hover_bg_color,
                                              dc_tint_color=self.default_bg_color, txt_align=(0, 0),
                                              font_type=self.font_size, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)
                self.clock_wrapper = self.board.ships[-1]
                self.clock = classes.drw.clock.Clock(self, self.clock_wrapper, self.size, self.time[i], self.data[2:11])
                self.board.ships[-1].manual_painting_layer = 1
                self.board.ships[-1].init_m_painting()
                self.board.ships[-1].manual_painting = self.clock.get_canvas().copy()
                self.board.ships[-1].update_me = True
            else:
                s = "<1>%02d<3>:<2>%02d" % (self.time[i - switch][0], self.time[i - switch][1])
                self.board.add_universal_unit(grid_x=slots[i][0], grid_y=slots[i][1], grid_w=1, grid_h=1,
                                              txt=s,
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=door_bg_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=[self.h_col, self.m_col, self.colon_col],
                                              bg_tint_color=self.default_bg_color, fg_tint_color=self.hover_bg_color,
                                              dc_tint_color=self.default_bg_color, txt_align=(0, 0), font_type=35,
                                              multi_color=True, alpha=True,
                                              immobilized=True, fg_as_hover=True)
            self.units.append(self.board.ships[-1])
            self.board.ships[i].checkable = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].init_check_images()
        self.outline_all(color4, 1)

        self.mainloop.redraw_needed[0] = True

    def immo(self, ship):
        ship.immobilize()
        ship.readable = False
        ship.perm_outline = True
        ship.uncovered = False

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[1] is None and self.ai_enabled is False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if not active.uncovered:
                    if self.history[0] is None:
                        self.history[0] = active
                        self.semi_select(active)
                        self.clicks += 1
                        active.uncovered = True
                    elif self.history[1] is None:
                        self.history[1] = active
                        self.semi_select(active)
                        self.clicks += 1
                        if self.chosen[self.history[0].unit_id] != self.chosen[self.history[1].unit_id]:
                            self.ai_enabled = True
                            self.history[0].uncovered = False
                        else:
                            self.select()
                            self.found += 2
                            if self.found == self.square_count:
                                self.completed_mode = True
                                self.ai_enabled = True

                    active.update_me = True

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.custom_hover(event)

    def semi_select(self, o):
        if self.mainloop.m.game_variant == 4:
            o.dc_tint_color = self.semi_selected_color
            o.bg_tint_color = (50, 50, 50)
        elif self.mainloop.m.game_variant == 5:
            o.dc_tint_color = self.semi_selected_color
        else:
            o.bg_tint_color = self.semi_selected_color
        o.mouse_out()
        o.update_me = True

    def select(self):
        for each in self.history:
            if self.mainloop.m.game_variant in [4, 5]:
                each.dc_tint_color = self.selected_color
                each.set_dc_img(self.dc_selected_img_src)
            else:
                each.bg_tint_color = self.selected_color
            each.uncovered = True
            each.set_display_check(True)
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]

    def deselect(self):
        for each in self.history:
            if self.mainloop.m.game_variant in [4, 5]:
                each.dc_tint_color = self.default_bg_color
                each.bg_tint_color = None
            else:
                each.bg_tint_color = self.default_bg_color
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]
        self.ai_enabled = False
        self.disp_counter = 0

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.ai_enabled = False
                self.level.next_board()
            else:
                self.deselect()

    def custom_hover(self, event):
        if not self.drag and not self.ai_enabled:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            found = False
            for each in self.units:
                if each.rect.left < pos[0] < each.rect.right and each.rect.top < pos[1] < each.rect.bottom:
                    if each != self.unit_mouse_over:
                        if self.unit_mouse_over is not None:
                            self.unit_mouse_over.mouse_out()
                        self.unit_mouse_over = each
                    found = True
                    if not each.uncovered:
                        each.handle(event)
                    break
            if not found:
                if self.unit_mouse_over is not None:
                    self.unit_mouse_over.mouse_out()
                self.unit_mouse_over = None

    def check_result(self):
        pass
