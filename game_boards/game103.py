# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.fraction_hq

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
            white = self.mainloop.scheme.u_color
            h1 = 170
            h2 = h1
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            white = (255, 255, 255)
            h1 = random.randrange(5, 255)
            h2 = h1
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 40, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 255, 200)
            bd_color2 = ex.hsv_to_rgb(h2, 100, 200)

        self.bd_color_1 = bd_color1
        self.bd_color_2 = bd_color2

        data = [4, 2]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.data = data

        self.disp_counter = 0
        self.disp_len = 1
        self.found = 0
        self.clicks = 0
        self.square_count = data[0] * data[1]
        self.history = [None, None]
        self.fractions = []
        self.fractions2 = []
        count = 0
        while True:
            d = random.randint(self.data[2], self.data[3])
            n = random.randint(1, d-1)
            fract = [n, d]
            x = float(n) / d
            add = True
            for each in self.fractions:
                if each == fract or float(each[0]) / each[1] == x:
                    add = False
                    break
            if add:
                self.fractions.append(fract)
                if d < 5:
                    m = random.randint(2, 5)
                else:
                    m = random.randint(2, 3)
                self.fractions2.append([fract[0] * m, fract[1] * m])
                count += 1
                if count == 4:
                    break

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
        switch = self.square_count // 2
        for i in range(self.square_count):
            if i < switch:
                if self.mainloop.m.game_variant == 0:
                    self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Letter, "", white, "", 0)
                    fraction_canvas = self.board.ships[-1]
                    fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale, color1, color2,
                                                                     bd_color1,
                                                                     bd_color2, self.fractions[i], 2)
                    fraction.set_offset(20, 30)
                    fraction_canvas.painting = fraction.get_canvas().copy()
                else:
                    self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Letter,
                                        [str(self.fractions[i][0]), str(self.fractions[i][1])],
                                        white, "", 8)
                    self.board.ships[-1].font_color = bd_color1
                    canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)
                    self.draw_fraction_line(canvas, self.size, self.center)
                    self.board.ships[-1].painting = canvas.copy()
            else:
                if self.mainloop.m.game_variant == 0:
                    self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Letter, "", white, "", 8)
                    fraction_canvas = self.board.ships[-1]
                    fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale, color1, color2,
                                                                bd_color1, bd_color2, self.fractions2[i - switch], 2)
                    fraction.set_offset(20, 30)
                    fraction_canvas.painting = fraction.get_canvas().copy()
                else:
                    self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Letter,
                                        [str(self.fractions2[i - switch][0]), str(self.fractions2[i - switch][1])],
                                        white, "", 8)
                    self.board.ships[-1].font_color = bd_color1
                    canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)
                    self.draw_fraction_line(canvas, self.size, self.center)
                    self.board.ships[-1].painting = canvas.copy()
            self.immo(self.board.ships[-1])
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(bd_color2, 1)

        self.mainloop.redraw_needed[0] = True

    def draw_fraction_line(self, canvas, size, center):
        lh = 4
        la = self.mainloop.config.font_start_at_adjustment * 60 // size
        pygame.draw.line(canvas, self.bd_color_1, [center[0] - size // 7, center[1] - lh // 2 + la],
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

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
