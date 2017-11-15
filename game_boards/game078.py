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

        color = (255, 255, 255)
        white = (255, 255, 255)
        gray = (100, 100, 100)

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
            h_pool = range(13, 24)
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
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], self.layout.scale)

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
        for i in range(self.square_count):
            if i < switch:
                self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Ship, "", white, "", self.font_size)
                self.clock_wrapper = self.board.ships[-1]
                self.board.active_ship = self.clock_wrapper.unit_id
                self.clock = classes.drw.clock.Clock(self, self.clock_wrapper, self.size, self.time[i], self.data[2:11])
            else:
                self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Letter,
                                    "%02d:%02d" % (self.time[i - switch][0], self.time[i - switch][1]), white, "", 8)
                self.board.ships[-1].font_color = color4
            self.immo(self.board.ships[-1])
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(color4, 1)

        self.mainloop.redraw_needed[0] = True

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
                            self.history[0].perm_outline_color = self.colors2[1]  # [50,255,50]
                            self.history[1].perm_outline_color = self.colors2[1]
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
                self.history[0].perm_outline_color = self.colors2[1]
                self.history[1].perm_outline_width = 1
                self.history[1].perm_outline_color = self.colors2[1]
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
