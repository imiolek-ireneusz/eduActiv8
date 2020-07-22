# -*- coding: utf-8 -*-

import pygame
import random
import os

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.fraction_hq
import classes.drw.ratio_hq


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 12, 6)

    def create_game_objects(self, level=1):
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.ai_enabled = False
        self.board.draw_grid = False
        if self.mainloop.scheme is not None:
            h1 = 170
            h2 = h1
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            h1 = random.randrange(5, 255, 5)
            h2 = h1
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 40, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 255, 200)
            bd_color2 = ex.hsv_to_rgb(h2, 100, 200)

        self.bd_color_1 = bd_color1
        self.bd_color_2 = bd_color2

        data = [12, 6, 2, 3]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.data = data

        rlen = self.data[4]

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
        self.data = data

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2
        self.size = self.board.scale

        slots = []
        for j in range(0, data[1]):
            for i in range(0, data[0]):
                slots.append([i, j])
        random.shuffle(slots)
        self.center = [self.size // 2, self.size // 2]
        self.mainloop.redraw_needed[0] = True

        if self.level.lvl > self.level.lvl_count:
            self.level.lvl = self.level.lvl_count

        self.found = 0
        self.clicks = 0
        fract_size = 3

        self.squares = self.data[2] * self.data[3]

        self.square_count = self.squares * 2
        self.history = [None, None]

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.units = []
        self.completed_mode = False

        choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        small_slots = [[0, 3], [0, 0], [3, 0], [6, 0], [9, 0], [9, 3]]
        wide_slots = [[3, 3], [6, 3], [3, 4], [6, 4], [3, 5], [6, 5]]

        random.shuffle(wide_slots)
        switch = self.square_count // 2
        if self.lang.lang == "lkt":
            text_font_size = 10
        else:
            text_font_size = 8

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
        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        self.dc_img_src_label = os.path.join('unit_bg', "universal_r3x1_dc.png")
        bg_img_src_label = os.path.join('unit_bg', "universal_r3x1_bg.png")
        door_bg_img_src_label = os.path.join('unit_bg', "universal_r3x1_door.png")

        if self.mainloop.m.game_variant == 0:
            self.fractions = []
            count = 0
            while True:
                d = random.randint(self.data[4], self.data[5])
                n = random.randint(1, d - 1)

                fract = [n, d]
                if fract not in self.fractions:
                    self.fractions.append(fract)
                    count += 1
                    if count == 6:
                        break
            for i in range(self.square_count):
                if i < switch:
                    position_list = small_slots
                    pos = i
                    xw = fract_size
                    self.board.add_universal_unit(grid_x=position_list[pos][0], grid_y=position_list[pos][1], grid_w=xw,
                                                  grid_h=xw, txt="",
                                                  fg_img_src=bg_img_src, bg_img_src=bg_img_src,
                                                  dc_img_src=door_bg_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=self.font_color,
                                                  bg_tint_color=self.default_bg_color,
                                                  fg_tint_color=self.hover_bg_color,
                                                  dc_tint_color=self.default_bg_color, txt_align=(0, 0),
                                                  font_type=self.font_size, multi_color=False, alpha=True,
                                                  immobilized=True, fg_as_hover=True)

                    fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * xw, color1, color2,
                                                                bd_color1, bd_color2, self.fractions[i], 2, 0.9)

                    fraction.set_offset(20, 30)
                    self.board.ships[-1].manual_painting_layer = 1
                    self.board.ships[-1].init_m_painting()
                    self.board.ships[-1].manual_painting = fraction.get_canvas().copy()
                    self.board.ships[-1].update_me = True

                else:
                    caption = self.lang.fract2str(self.fractions[i - switch][0], self.fractions[i - switch][1])
                    position_list = wide_slots
                    pos = i - switch
                    xw = 3
                    self.board.add_universal_unit(grid_x=position_list[pos][0], grid_y=position_list[pos][1],
                                                  grid_w=xw, grid_h=1, txt=caption,
                                                  fg_img_src=bg_img_src_label, bg_img_src=bg_img_src_label,
                                                  dc_img_src=door_bg_img_src_label,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=self.font_color,
                                                  bg_tint_color=self.default_bg_color,
                                                  fg_tint_color=self.hover_bg_color,
                                                  dc_tint_color=self.default_bg_color, txt_align=(0, 0),
                                                  font_type=text_font_size, multi_color=False, alpha=True,
                                                  immobilized=True, fg_as_hover=True)

                self.units.append(self.board.ships[-1])

        else:
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
            self.ratios = []
            count = 0
            while True:
                n1 = random.randint(self.data[5], self.data[6])
                n2 = random.randint(self.data[5], self.data[6])

                if rlen == 2:
                    rt = [n1, n2]
                else:
                    n3 = random.randint(self.data[5], self.data[6])
                    rt = [n1, n2, n3]

                if rt not in self.ratios:
                    self.ratios.append(rt)
                    count += 1
                    if count == 6:
                        break

            for i in range(self.square_count):
                if i < switch:
                    position_list = small_slots
                    pos = i
                    xw = fract_size
                    self.board.add_universal_unit(grid_x=position_list[pos][0], grid_y=position_list[pos][1], grid_w=xw,
                                                  grid_h=xw, txt="",
                                                  fg_img_src=bg_img_src, bg_img_src=bg_img_src,
                                                  dc_img_src=door_bg_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=self.font_color,
                                                  bg_tint_color=self.default_bg_color,
                                                  fg_tint_color=self.hover_bg_color,
                                                  dc_tint_color=self.default_bg_color, txt_align=(0, 0),
                                                  font_type=self.font_size, multi_color=False, alpha=True,
                                                  immobilized=True, fg_as_hover=True)

                    fraction = classes.drw.ratio_hq.Ratio(1, self.board.scale * xw, color1, color2, color3,
                                                          self.bd_color1, self.bd_color2, self.bd_color3,
                                                          self.ratios[i], 0.92)
                    self.board.ships[-1].manual_painting_layer = 1
                    self.board.ships[-1].init_m_painting()
                    self.board.ships[-1].manual_painting = fraction.get_canvas().copy()
                    self.board.ships[-1].update_me = True
                else:
                    position_list = wide_slots
                    pos = i - switch
                    xw = 3
                    font_colors = [self.bd_color1, self.bd_color2, self.bd_color3, self.colon_color]
                    if rlen == 3:
                        caption = "<1>" + str(self.ratios[i - switch][0]) + \
                                  "<4> : <2>" + str(self.ratios[i - switch][1]) + \
                                  "<4> : <3>" + str(self.ratios[i - switch][2])
                    else:
                        caption = "<1>" + str(self.ratios[i - switch][0]) + \
                                  "<4> : <2>" + str(self.ratios[i - switch][1])

                    self.board.add_universal_unit(grid_x=position_list[pos][0], grid_y=position_list[pos][1],
                                                  grid_w=xw, grid_h=1, txt=caption,
                                                  fg_img_src=bg_img_src_label, bg_img_src=bg_img_src_label,
                                                  dc_img_src=door_bg_img_src_label,
                                                  bg_color=(0, 0, 0, 0), border_color=None,
                                                  font_color=font_colors,
                                                  bg_tint_color=self.default_bg_color,
                                                  fg_tint_color=self.hover_bg_color,
                                                  dc_tint_color=self.default_bg_color, txt_align=(0, 0),
                                                  font_type=2, multi_color=True, alpha=True,
                                                  immobilized=True, fg_as_hover=True)

                self.units.append(self.board.ships[-1])

        for i in range(self.square_count):
            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(self.bd_color_2, 1)

    def handle_old(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[1] is None and not self.ai_enabled:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if not active.uncovered:
                    if self.history[0] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[0] = active
                        self.clicks += 1
                        active.uncovered = True
                    elif self.history[1] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[1] = active
                        self.clicks += 1
                        if self.chosen[self.history[0].unit_id] != self.chosen[self.history[1].unit_id]:
                            self.ai_enabled = True
                            self.history[0].uncovered = False
                        else:
                            self.history[0].uncovered = True
                            self.history[1].uncovered = True
                            self.history[0].perm_outline_color = self.bd_color_2  # [50,255,50]
                            self.history[1].perm_outline_color = self.bd_color_2
                            self.history[0].image.set_alpha(50)
                            self.history[1].image.set_alpha(50)
                            self.history[0].update_me = True
                            self.history[1].update_me = True
                            self.history[0].set_display_check(True)
                            self.history[1].set_display_check(True)
                            self.found += 2
                            if self.found == self.square_count:
                                self.completed_mode = True
                                self.ai_enabled = True
                            self.history = [None, None]
                    active.update_me = True

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
