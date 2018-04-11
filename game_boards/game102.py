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
            white = self.mainloop.scheme.u_color
            h1 = 170
            h2 = h1
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            white = (255, 255, 255)
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
                    self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, xw, classes.board.Ship, "", white, "", self.font_size)

                    fraction_canvas = self.board.ships[-1]
                    fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * xw, color1, color2,
                                                                bd_color1,
                                                                bd_color2, self.fractions[i], 2)
                    fraction.set_offset(20, 30)
                    fraction_canvas.painting = fraction.get_canvas().copy()
                else:
                    caption = self.lang.fract2str(self.fractions[i - switch][0], self.fractions[i - switch][1])
                    position_list = wide_slots
                    pos = i - switch
                    xw = 3
                    self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, 1, classes.board.Letter, caption,
                                        white, "", text_font_size)
                    self.board.ships[-1].font_color = bd_color1
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
                    self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, xw, classes.board.Ship, "",
                                        white, "", self.font_size)

                    fraction_canvas = self.board.ships[-1]
                    """
                    fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * xw, color1, color2,
                                                                bd_color1,
                                                                bd_color2, self.fractions[i], 2)
                    """
                    fraction = classes.drw.ratio_hq.Ratio(1, self.board.scale * xw, color1, color2, color3,
                                               self.bd_color1, self.bd_color2, self.bd_color3, self.ratios[i])
                    #fraction.set_offset(20, 30)
                    fraction_canvas.painting = fraction.get_canvas().copy()
                else:
                    position_list = wide_slots
                    pos = i - switch
                    xw = 3
                    if rlen == 3:
                        self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, 1, classes.board.MultiColorLetters,
                                            "<1>" + str(self.ratios[i - switch][0]) + "<4> : <2>" + str(
                                                self.ratios[i - switch][1]) + "<4> : <3>" + str(self.ratios[i - switch][2]),
                                            white, "", 2)
                    else:
                        self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, 1,
                                            classes.board.MultiColorLetters,
                                            "<1>" + str(self.ratios[i - switch][0]) + "<4> : <2>" + str(
                                                self.ratios[i - switch][1]), white, "", 2)
                    # self.board.ships[-1].font_color = self.bd_color1
                    self.board.ships[-1].set_font_colors(self.bd_color1, self.bd_color2, self.bd_color3,
                                                         self.colon_color)

                    self.board.ships[-1].font_color = bd_color1

        for i in range(self.square_count):
            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(self.bd_color_2, 1)

    """
    def add_ratios(self, rlen=3):
        #recreate colours
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
            step = 255 // 3
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
            n1 = random.randint(1, 5)
            n2 = random.randint(1, 5)

            if rlen == 2:
                rt = [n1, n2]
            else:
                n3 = random.randint(1, 5)
                rt = [n1, n2, n3]
                
            if rt not in self.ratios:
                self.ratios.append(rt)
                count += 1
                if count == 4:
                    break

        switch = self.square_count // 2
        for i in range(self.square_count):
            if i < switch:
                #position_list = small_slots
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter, "", self.white, "",
                                    0)
                ratio_canvas = self.board.ships[-1]
                #ratio = classes.drw.ratio_hq.Ratio(1, self.board.scale, self.color1, self.color2, self.bd_color1, self.bd_color2, self.perc[i])
                ratio = classes.drw.ratio_hq.Ratio(1, self.board.scale, color1, color2, color3,
                                                           self.bd_color1, self.bd_color2, self.bd_color3, self.ratios[i])
                #fraction.set_offset(20, 30)
                ratio_canvas.painting = ratio.get_canvas().copy()

            else:
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.MultiColorLetters,
                                    "<1>" + str(self.ratios[i - switch][0]) + "<4> : <2>" + str(self.ratios[i - switch][1]) + "<4> : <3>" + str(self.ratios[i - switch][2]),
                                    self.white, "", 8)
                #self.board.ships[-1].font_color = self.bd_color1
                self.board.ships[-1].set_font_colors(self.bd_color1, self.bd_color2, self.bd_color3, self.colon_color)
    """

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[
            1] == None and self.ai_enabled == False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if active.uncovered == False:
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

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.level.next_board()
            else:
                self.history[0].perm_outline_width = 1
                self.history[0].perm_outline_color = self.bd_color_2
                self.history[1].perm_outline_width = 1
                self.history[1].perm_outline_color = self.bd_color_2
                self.history[0].update_me = True
                self.history[1].update_me = True
                self.history = [None, None]
                self.ai_enabled = False
                self.disp_counter = 0

    def check_result(self):
        pass
