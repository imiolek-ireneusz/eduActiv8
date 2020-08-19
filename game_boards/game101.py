# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.fraction_hq
import classes.drw.percentage_hq
import classes.drw.ratio_hq


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 4, 2)

    def create_game_objects(self, level=1):
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.ai_enabled = False
        self.hand_id = 0
        self.hand_coords = [[], []]
        self.board.draw_grid = False

        if self.mainloop.scheme is not None:
            self.white = self.mainloop.scheme.u_color
            h1 = 170
            h2 = h1
            self.color1 = ex.hsv_to_rgb(h1, 255, 255)
            self.color2 = ex.hsv_to_rgb(h2, 75, 255)
            self.bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            self.bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            self.white = (255, 255, 255)

            h1 = random.randint(5, 255)
            h2 = h1
            self.color1 = ex.hsv_to_rgb(h1, 255, 255)
            self.color2 = ex.hsv_to_rgb(h2, 40, 255)

            self.bd_color1 = ex.hsv_to_rgb(h1, 255, 200)
            self.bd_color2 = ex.hsv_to_rgb(h2, 100, 200)

        data = [4, 2]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.data = data
        rlen = self.data[2]

        self.disp_counter = 0
        self.disp_len = 1
        self.found = 0
        self.clicks = 0
        self.square_count = data[0] * data[1]
        self.history = [None, None]

        self.disp_counter = 0
        self.disp_len = 1
        self.completed_mode = False
        self.font_size = 0

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.units = []
        choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        self.size = self.board.scale

        self.slots = []
        for j in range(0, data[1]):
            for i in range(0, data[0]):
                self.slots.append([i, j])
        random.shuffle(self.slots)
        self.center = [self.size // 2, self.size // 2]

        h = (h1 + 85) % 255
        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
            self.default_bg_color = ex.hsv_to_rgb(h, 200, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 230, 90)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 150, 200), ]

            self.selected_color = ex.hsv_to_rgb(h, 150, 50)
            self.selected_font_color = [ex.hsv_to_rgb(h, 150, 100), ]
        else:
            self.default_bg_color = ex.hsv_to_rgb(h, 150, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 80, self.mainloop.cl.bg_color_v)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 200, self.mainloop.cl.font_color_v), ]

            self.selected_color = ex.hsv_to_rgb(h, 50, self.mainloop.cl.bg_color_v)
            self.selected_font_color = [ex.hsv_to_rgb(h, 50, 250), ]

        self.dc_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        self.bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        self.door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        if self.mainloop.m.game_variant == 0:
            self.add_fractions()
        elif self.mainloop.m.game_variant == 1:
            self.add_decimals()
        elif self.mainloop.m.game_variant == 2:
            self.add_percentages()
        elif self.mainloop.m.game_variant == 3:
            self.add_ratios(rlen)

        for i in range(self.square_count):
            self.immo(self.board.ships[i])
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()

        self.outline_all(self.bd_color2, 1)

        self.mainloop.redraw_needed[0] = True

    def add_fractions(self):
        self.fractions = []
        count = 0
        while True:
            d = random.randint(self.data[2], self.data[3])
            n = random.randint(1, d - 1)

            fract = [n, d]
            if fract not in self.fractions:
                self.fractions.append(fract)
                count += 1
                if count == 4:
                    break

        switch = self.square_count // 2
        for i in range(self.square_count):
            if i < switch:
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt="", fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=self.font_color, bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color, dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=self.font_size, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)

                fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale, self.color1, self.color2,
                                                            self.bd_color1, self.bd_color2, self.fractions[i], 2, 0.9)
                fraction.set_offset(20, 30)
                self.board.ships[-1].manual_painting_layer = 1
                self.board.ships[-1].init_m_painting()
                self.board.ships[-1].manual_painting = fraction.get_canvas().copy()
                self.board.ships[-1].update_me = True
            else:
                s = [str(self.fractions[i - switch][0]), str(self.fractions[i - switch][1])]
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt=s, fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=self.font_color, bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color, dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=8, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)
                canvas = pygame.Surface((self.size, self.size - 1), flags=pygame.SRCALPHA)
                self.draw_fraction_line(canvas, self.size, self.center)
                self.board.ships[-1].manual_painting_layer = 1
                self.board.ships[-1].init_m_painting()
                self.board.ships[-1].manual_painting = canvas.copy()
                self.board.ships[-1].update_me = True
            self.units.append(self.board.ships[-1])

    def add_decimals(self):
        self.fractions = []
        count = 0
        while True:
            d = 10
            n = random.randint(self.data[2], d - 1)

            fract = [n, d]
            if fract not in self.fractions:
                self.fractions.append(fract)
                count += 1
                if count == 4:
                    break

        switch = self.square_count // 2
        for i in range(self.square_count):
            if i < switch:
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt="", fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=self.font_color, bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color, dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=self.font_size, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)
                fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale, self.color1, self.color2,
                                                            self.bd_color1, self.bd_color2, self.fractions[i], 2, 0.9)
                fraction.set_offset(20, 30)
                self.board.ships[-1].manual_painting_layer = 1
                self.board.ships[-1].init_m_painting()
                self.board.ships[-1].manual_painting = fraction.get_canvas().copy()
                self.board.ships[-1].update_me = True
            else:
                s = "0." + str(self.fractions[i - switch][0])
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt=s, fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=self.font_color, bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color, dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=8, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)
            self.units.append(self.board.ships[-1])

    def add_percentages(self):
        self.perc = []
        count = 0
        while True:
            n = random.randrange(self.data[3], self.data[4] + 1, self.data[2])
            suff_margin = True
            for each in self.perc:
                if not (n < each - 5 or n > each + 5):
                    suff_margin = False
                    break
            if suff_margin:
                self.perc.append(n)
                count += 1
                if count == 4:
                    break

        switch = self.square_count // 2
        for i in range(self.square_count):
            if i < switch:
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt="", fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=self.font_color, bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color, dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=self.font_size, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)
                perc = classes.drw.percentage_hq.Percentage(1, self.board.scale, self.color1, self.color2,
                                                            self.bd_color1, self.bd_color2, self.perc[i], 0.95)
                self.board.ships[-1].manual_painting_layer = 1
                self.board.ships[-1].init_m_painting()
                self.board.ships[-1].manual_painting = perc.get_canvas().copy()
                self.board.ships[-1].update_me = True
            else:
                s = str(self.perc[i - switch]) + "%"
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt=s, fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=self.font_color, bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color, dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=8, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)

            self.units.append(self.board.ships[-1])

    def add_ratios(self, rlen=3):
        if self.mainloop.scheme is not None:
            h1 = 170
            h2 = 40
            h3 = 0
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 157, 255)
            color3 = ex.hsv_to_rgb(h2, 57, 255)
            self.bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            self.bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
            self.bd_color3 = ex.hsv_to_rgb(h3, 57, 155)

            self.colon_color = self.mainloop.scheme.u_font_color
        else:
            step = 255 // rlen
            h1 = random.randrange(0, 255)
            h2 = (h1 + step) % 255
            h3 = (h1 + step * 2) % 255

            color1 = ex.hsv_to_rgb(h1, 197, 255)
            color2 = ex.hsv_to_rgb(h2, 197, 255)
            color3 = ex.hsv_to_rgb(h3, 197, 255)
            self.bd_color1 = ex.hsv_to_rgb(h1, 187, 200)
            self.bd_color2 = ex.hsv_to_rgb(h2, 187, 200)
            self.bd_color3 = ex.hsv_to_rgb(h3, 187, 200)
            self.colon_color = (0, 0, 0)
        ratio_font_colors = [self.bd_color1, self.bd_color2, self.bd_color3, self.colon_color]
        self.ratios = []
        count = 0
        while True:
            n1 = random.randint(self.data[3], self.data[4])
            n2 = random.randint(self.data[3], self.data[4])
            if rlen == 2:
                rt = [n1, n2]
            else:
                n3 = random.randint(self.data[3], self.data[4])
                rt = [n1, n2, n3]
            if rt not in self.ratios:
                self.ratios.append(rt)
                count += 1
                if count == 4:
                    break

        switch = self.square_count // 2
        for i in range(self.square_count):
            if i < switch:
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt="", fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=self.font_color, bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color, dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=self.font_size, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)
                ratio = classes.drw.ratio_hq.Ratio(1, self.board.scale, color1, color2, color3, self.bd_color1,
                                                   self.bd_color2, self.bd_color3, self.ratios[i], 0.92)
                self.board.ships[-1].manual_painting_layer = 1
                self.board.ships[-1].init_m_painting()
                self.board.ships[-1].manual_painting = ratio.get_canvas().copy()
                self.board.ships[-1].update_me = True

            else:
                if rlen == 3:
                    caption = "<1>" + str(self.ratios[i - switch][0]) + \
                              "<4> : <2>" + str(self.ratios[i - switch][1]) + \
                              "<4> : <3>" + str(self.ratios[i - switch][2])
                else:
                    caption = "<1>" + str(self.ratios[i - switch][0]) + \
                              "<4> : <2>" + str(self.ratios[i - switch][1])
                self.board.add_universal_unit(grid_x=self.slots[i][0], grid_y=self.slots[i][1], grid_w=1, grid_h=1,
                                              txt=caption, fg_img_src=self.bg_img_src, bg_img_src=self.bg_img_src,
                                              dc_img_src=self.door_bg_img_src, bg_color=(0, 0, 0, 0),
                                              border_color=None, font_color=ratio_font_colors,
                                              bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color,
                                              dc_tint_color=self.default_bg_color,
                                              txt_align=(0, 0), font_type=8, multi_color=True, alpha=True,
                                              immobilized=True, fg_as_hover=True)
                self.units.append(self.board.ships[-1])

    def draw_fraction_line(self, canvas, size, center):
        lh = 4
        la = self.mainloop.config.font_start_at_adjustment * 60 // size
        pygame.draw.line(canvas, self.font_color[0], [center[0] - size // 7, center[1] - lh // 2 + la],
                         [center[0] + size // 7, center[1] - lh // 2 + la], lh)

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
        o.bg_tint_color = self.semi_selected_color
        o.mouse_out()
        o.update_me = True

    def select(self):
        for each in self.history:
            each.bg_tint_color = self.selected_color
            each.uncovered = True
            each.set_display_check(True)
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]

    def deselect(self):
        for each in self.history:
            each.bg_tint_color = self.default_bg_color
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]
        self.ai_enabled = False
        self.disp_counter = 0

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

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
