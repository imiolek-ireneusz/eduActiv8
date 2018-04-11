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
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter, "", self.white, "", 0)
                fraction_canvas = self.board.ships[-1]
                fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale, self.color1, self.color2,
                                                            self.bd_color1,
                                                            self.bd_color2, self.fractions[i], 2)
                fraction.set_offset(20, 30)
                fraction_canvas.painting = fraction.get_canvas().copy()
            else:
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter,
                                    [str(self.fractions[i - switch][0]), str(self.fractions[i - switch][1])],
                                    self.white, "", 8)
                self.board.ships[-1].font_color = self.bd_color1
                canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)
                self.draw_fraction_line(canvas, self.size, self.center)
                self.board.ships[-1].painting = canvas.copy()

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
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter, "", self.white, "",
                                    0)
                fraction_canvas = self.board.ships[-1]
                fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale, self.color1, self.color2,
                                                            self.bd_color1,
                                                            self.bd_color2, self.fractions[i], 2)
                fraction.set_offset(20, 30)
                fraction_canvas.painting = fraction.get_canvas().copy()
            else:
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter,
                                    "0." + str(self.fractions[i - switch][0]), self.white, "", 8)
                self.board.ships[-1].font_color = self.bd_color1

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
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter, "", self.white, "",
                                    0)
                perc_canvas = self.board.ships[-1]
                perc = classes.drw.percentage_hq.Percentage(1, self.board.scale, self.color1, self.color2,
                                                            self.bd_color1,
                                                            self.bd_color2, self.perc[i])
                perc_canvas.painting = perc.get_canvas().copy()
            else:
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter,
                                    str(self.perc[i - switch]) + "%", self.white, "", 8)
                self.board.ships[-1].font_color = self.bd_color1

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
                self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.Letter, "", self.white, "",
                                    0)
                ratio_canvas = self.board.ships[-1]
                ratio = classes.drw.ratio_hq.Ratio(1, self.board.scale, color1, color2, color3,
                                                           self.bd_color1, self.bd_color2, self.bd_color3, self.ratios[i])
                ratio_canvas.painting = ratio.get_canvas().copy()

            else:
                if rlen == 3:
                    self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.MultiColorLetters,
                                        "<1>" + str(self.ratios[i - switch][0]) + "<4> : <2>" + str(self.ratios[i - switch][1]) + "<4> : <3>" + str(self.ratios[i - switch][2]),
                                        self.white, "", 8)
                else:
                    self.board.add_unit(self.slots[i][0], self.slots[i][1], 1, 1, classes.board.MultiColorLetters,
                                        "<1>" + str(self.ratios[i - switch][0]) + "<4> : <2>" + str(
                                            self.ratios[i - switch][1]),
                                        self.white, "", 8)
                self.board.ships[-1].set_font_colors(self.bd_color1, self.bd_color2, self.bd_color3, self.colon_color)

    def draw_fraction_line(self, canvas, size, center):
        lh = 4
        la = self.mainloop.config.font_start_at_adjustment * 60 // size
        pygame.draw.line(canvas, self.bd_color1, [center[0] - size // 7, center[1] - lh // 2 + la],
                         [center[0] + size // 7, center[1] - lh // 2 + la], lh)

    def immo(self, ship):
        ship.immobilize()
        ship.readable = False
        ship.perm_outline = True
        ship.uncovered = False

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[1] is None and self.ai_enabled is False:
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
                            self.history[0].perm_outline_color = self.bd_color2  # [50,255,50]
                            self.history[1].perm_outline_color = self.bd_color2
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

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.level.next_board()
            else:
                self.history[0].perm_outline_width = 1
                self.history[0].perm_outline_color = self.bd_color2
                self.history[1].perm_outline_width = 1
                self.history[1].perm_outline_color = self.bd_color2
                self.history[0].update_me = True
                self.history[1].update_me = True
                self.history = [None, None]
                self.ai_enabled = False
                self.disp_counter = 0

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
