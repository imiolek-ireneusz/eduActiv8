# -*- coding: utf-8 -*-

import pygame
import random
import os

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.clock


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 3, 13)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 12, 6)

    def create_game_objects(self, level=1):
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        h = random.randrange(150, 240, 5)
        color0 = ex.hsv_to_rgb(h, 1, 255)  # highlight 1
        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
        self.font_color = self.color2

        clock_size = 3

        self.disp_counter = 0
        self.disp_len = 1

        self.hand_id = 0
        self.hand_coords = [[], []]
        self.board.draw_grid = False

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
            data2 = [12, 6, True, True, False, False, True, False, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = [0]
        elif self.level.lvl == 2:
            data2 = [12, 6, True, True, False, False, True, False, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60, 15)
        elif self.level.lvl == 3:
            data2 = [12, 6, True, True, False, False, False, True, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60, 5)
        elif self.level.lvl == 4:
            data2 = [12, 6, True, True, False, False, False, True, False, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60, 5)
        elif self.level.lvl == 5:
            data2 = [12, 6, True, True, False, False, False, False, False, True, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 6:
            data2 = [12, 6, True, True, False, False, False, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 7:
            data2 = [12, 6, True, True, False, False, False, True, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 8:
            data2 = [12, 6, True, True, False, False, True, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 9:
            data2 = [12, 6, True, False, False, False, False, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 10:
            data2 = [12, 6, True, False, False, True, False, False, False, False, True, 25]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 11:
            data2 = [12, 6, True, True, False, False, False, False, True, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 12:
            data2 = [12, 6, True, True, False, False, True, False, True, True, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60)
        elif self.level.lvl == 13:
            data2 = [12, 6, True, True, False, False, False, False, True, False, True, 15]
            h_pool = range(1, 13)
            m_pool = range(0, 60)

        self.pointsx = self.level.lvl // 4 + 4

        # visual display properties
        self.show_outer_ring = data2[2]
        self.show_minutes = data2[3]
        self.show_24h = data2[4]
        self.show_only_quarters_h = data2[5]
        self.show_only_quarters_m = data2[6]
        self.show_only_fives_m = data2[7]
        self.show_roman = data2[8]
        self.show_highlight = data2[9]
        self.show_hour_offset = data2[10]

        self.disp_counter = 0
        self.disp_len = 1
        self.found = 0
        self.clicks = 0
        self.square_count = data2[0] * data2[1]
        self.history = [None, None]
        self.time = []
        for i in range(6):
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
        self.data2 = data2

        self.layout.update_layout(data2[0], data2[1])
        self.board.level_start(data2[0], data2[1], self.layout.scale)

        choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        self.size = self.board.scale
        self.clock_fonts = []
        self.points = int(round((self.board.scale * 72 / 96) * 1.2, 0))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (42 * self.size * clock_size / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (21 * self.size * clock_size / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSans.ttf'),
                                                 (int(self.points / (self.board.scale / (21 * self.size * clock_size / 500.0))))))

        slots = []
        for j in range(0, data2[1]):
            for i in range(0, data2[0]):
                slots.append([i, j])
        random.shuffle(slots)
        self.center = [self.size // 2, self.size // 2]
        self.mainloop.redraw_needed[0] = True

        if self.level.lvl > self.level.lvl_count:
            self.level.lvl = self.level.lvl_count
        data = [12, 6, 3, 2, 3]
        self.data = data

        self.found = 0
        self.clicks = 0

        self.squares = self.data[3] * self.data[4]

        self.square_count = self.squares * 2  # self.data[3]*self.data[4]
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
        for i in range(self.square_count):
            if i < switch:
                position_list = small_slots
                pos = i
                xw = clock_size
                self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, xw, classes.board.Ship, "", color0, "", self.font_size)
                self.clock_wrapper = self.board.ships[-1]
                self.board.active_ship = self.clock_wrapper.unit_id
                self.clock = classes.drw.clock.Clock(self, self.clock_wrapper, self.size*xw, self.time[i], self.data2[2:11])

            else:
                if self.mainloop.m.game_var2 == 0:
                    caption = self.lang.time2str(self.time[i - switch][0], self.time[i - switch][1])
                else:
                    caption = self.lang.time2str_short(self.time[i - switch][0], self.time[i - switch][1])
                position_list = wide_slots
                pos = i - switch
                xw = 3
                self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, 1, classes.board.Letter, caption,
                                    color0, "", text_font_size)
                self.board.ships[-1].font_color = self.font_color

            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(self.color2, 1)

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
                            self.history[0].perm_outline_color = self.color2  # [50,255,50]
                            self.history[1].perm_outline_color = self.color2
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
                self.history[0].perm_outline_color = self.color2
                self.history[1].perm_outline_width = 1
                self.history[1].perm_outline_color = self.color2
                self.history[0].update_me = True
                self.history[1].update_me = True
                self.history = [None, None]
                self.ai_enabled = False
                self.disp_counter = 0

    def check_result(self):
        pass
