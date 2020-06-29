# -*- coding: utf-8 -*-

import os
import random
import pygame
import copy

import classes.board
import classes.drw.clock
import classes.drw.clock_linear_diff
import classes.drw.clock_linear_diff2
import classes.drw.clock_circular_diff
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 8)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False
        self.ai_enabled = True
        self.ai_speed = 18
        self.correct = False

        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                colon_col = (255, 255, 255)
            else:
                colon_col = (0, 0, 0)
            white = self.mainloop.scheme.u_color
            color3 = self.mainloop.scheme.color3
            color4 = self.mainloop.scheme.color4
        else:
            white = (255, 255, 255)
            colon_col = (0, 0, 0)
            color3 = ex.hsv_to_rgb(225, 255, 255)
            color4 = ex.hsv_to_rgb(170, 255, 255)

        self.color3 = color3
        self.color4 = color4

        self.h_col = ex.hsv_to_rgb(225, 190, 220)
        self.m_col = ex.hsv_to_rgb(170, 190, 220)
        transp = (0, 0, 0, 0)

        h = random.randrange(150, 240, 5)
        self.font_color = ex.hsv_to_rgb(h, 255, 170)
        if self.mainloop.m.game_variant < 4:
            data = [18, 10, 25]
        elif self.mainloop.m.game_variant == 4:
            data = [18, 7, 25]
        else:
            data = [23, 11, 60]

        self.data = data

        self.lvl_data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid,
                                                              self.mainloop.config.user_age_group, self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True

        self.board.board_bg.line_color = (20, 20, 20)

        self.size = self.board.scale

        self.data2 = [None, None, True, True, False, False, False, True, False, True, True, True]
        # self.lvl_data = [0 - h1_range_start, 1 - h1_range_end, 2 - h2_range_start_from_h1 [0/1], 3 - h2_range_start,
        # 4 - h2_range_end, 5 - m1_range_start, 6 - m1_range_end, 7 - m2_range_start_from_m1, 8 - m2_range_start,
        # 9 - m2_range_end, 10 - minute range step (ie. 1, 5, 15, etc) 11 - show_24, 12 - show_numbers_on_diff]

        self.data2[4] = self.lvl_data[11]
        self.data2[11] = self.lvl_data[12]

        th1 = random.randint(self.lvl_data[0], self.lvl_data[1])
        if self.lvl_data[2] == 3:
            th2 = th1 + 1
        elif self.lvl_data[2] == 2:
            th2 = th1
        elif self.lvl_data[2] == 1:
            th2 = random.randint(th1 + 1, self.lvl_data[4])
        else:
            th2 = random.randint(self.lvl_data[3], self.lvl_data[4])
        if self.lvl_data[7] == 2:
            tm1 = 0
            tm2 = 0
        else:
            tm1 = random.randrange(self.lvl_data[5], self.lvl_data[6], self.lvl_data[10])
            if self.lvl_data[7] == 1:
                tm2 = random.randrange(tm1 + self.lvl_data[10], self.lvl_data[9], self.lvl_data[10])
            elif self.lvl_data[7] == 3:
                tm2 = random.randrange(self.lvl_data[8], tm1 - self.lvl_data[10]+1, self.lvl_data[10])
            else:
                tm2 = random.randrange(self.lvl_data[8], self.lvl_data[9], self.lvl_data[10])

        self.show_24h = self.data2[4]
        self.times = [[th1, tm1], [th2, tm2]]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.clock_fonts = []
        self.points = int(round((self.board.scale * 72 / 96) * 1.2, 0))
        xw = [6, 0]
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             42 * self.size * xw[0] / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             data[2] * self.size * xw[0] / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSans.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             30 * self.size * xw[0] / 500.0))))))

        #loc = [diff, hours, mins, h-, h+, m-, m+, h, m, diff_clock]
        if self.mainloop.m.game_variant < 5:
            loc = [[xw[0] * 2, 0, 6], [xw[0] * 2, 3], [xw[0] * 2, 6], [xw[0] * 2, 1], [xw[0] * 2 + 4, 1], [xw[0] * 2, 4],
                   [xw[0] * 2 + 4, 4], [xw[0] * 2 + 2, 1], [xw[0] * 2 + 2, 4], [0, xw[0] + 1, data[0], 3]]
        else:
            loc = [[0, 7, 12], [0, 10], [6, 10], [0, 8], [4, 8], [6, 8],
                   [10, 8], [2, 8], [8, 8], [data[0]-11, 0, 11, 11]]

        self.board.add_unit(0, 0, xw[0], 1, classes.board.Letter, self.lang.d["start_time"], white, "", 3)
        self.board.ships[-1].font_color = self.font_color

        self.board.add_unit(xw[0], 0, xw[0], 1, classes.board.Letter, self.lang.d["end_time"], white, "", 3)
        self.board.ships[-1].font_color = self.font_color

        self.board.add_unit(loc[0][0], loc[0][1], loc[0][2], 1, classes.board.Letter, self.lang.d["difference"], white, "", 3)
        self.board.ships[-1].font_color = self.font_color

        self.diff = self.get_diff()

        self.board.add_unit(loc[1][0], loc[1][1], 6, 1, classes.board.Letter,
                            [self.lang._n("hour", 0), ""], white, "", 4)
        self.board.ships[-1].font_color = color3
        self.h_caption = self.board.ships[-1]

        self.board.add_unit(loc[2][0], loc[2][1], 6, 1, classes.board.Letter,
                            [self.lang._n("minute", 0), ""], white, "", 4)
        self.board.ships[-1].font_color = color4
        self.m_caption = self.board.ships[-1]

        self.buttons = []

        self.board.add_unit(loc[3][0], loc[3][1], 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(loc[4][0], loc[4][1], 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(loc[5][0], loc[5][1], 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)
        self.board.add_unit(loc[6][0], loc[6][1], 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)
        for i in range(4):
            self.buttons.append(self.board.ships[-4 + i])

        self.board.add_unit(loc[7][0], loc[7][1], 2, 2, classes.board.Letter, "0", white, "", 31)
        self.ans_h = self.board.ships[-1]
        self.ans_h.checkable = True
        self.ans_h.init_check_images()
        self.board.active_ship = self.ans_h.unit_id
        self.home_square = self.ans_h

        self.board.add_unit(loc[8][0], loc[8][1], 2, 2, classes.board.Letter, "0", white, "", 31)
        self.ans_m = self.board.ships[-1]
        self.ans_m.checkable = True
        self.ans_m.init_check_images()

        self.ans_h.set_outline(color3, 5)
        self.ans_m.set_outline(color4, 5)
        self.ans_h.immobilize()
        self.ans_m.immobilize()
        self.ans_h.readable = False
        self.ans_m.readable = False
        self.ans_h.font_color = color3
        self.ans_m.font_color = color4

        # add first clock
        if self.mainloop.m.game_variant == 1 or self.mainloop.m.game_variant == 3:
            a = random.randint(0, 1)
            if a == 0:
                b = 1
            else:
                b = random.randint(0, 1)
            clock_types = (a, b)
        elif self.mainloop.m.game_variant == 4:
            clock_types = (random.randint(0, 1), random.randint(0, 1))
        else:
            clock_types = [0, 0]

        if clock_types[0] == 0:
            self.board.add_unit(0, 1, xw[0], xw[0], classes.board.Ship, "", white, "", 0)
            self.clock_wrapper1 = self.board.ships[-1]
            self.board.active_ship = self.clock_wrapper1.unit_id
            self.clock1 = classes.drw.clock.Clock(self, self.clock_wrapper1, self.size * xw[0], self.times[0],
                                                  self.data2[2:11])
        else:
            self.board.add_unit(0, 1, xw[0], xw[0], classes.board.MultiColorLetters,
                                "<1>%02d<3>:<2>%02d" % (self.times[0][0], self.times[0][1]), white, "", 34)
            self.board.ships[-1].set_font_colors(color3, color4, colon_col)

        # add second clock
        if clock_types[1] == 0:
            self.board.add_unit(0 + xw[0], 1, xw[0], xw[0], classes.board.Ship, "", white, "", 0)
            self.clock_wrapper2 = self.board.ships[-1]
            self.board.active_ship = self.clock_wrapper2.unit_id
            self.clock2 = classes.drw.clock.Clock(self, self.clock_wrapper2, self.size * xw[0], self.times[1],
                                                  self.data2[2:11])
        else:
            self.board.add_unit(0 + xw[0], 1, xw[0], xw[0], classes.board.MultiColorLetters,
                                "<1>%02d<3>:<2>%02d" % (self.times[1][0], self.times[1][1]), white, "", 34)
            self.board.ships[-1].set_font_colors(color3, color4, colon_col)

        # linear diff
        if self.lvl_data[13]:
            self.board.add_unit(loc[9][0], loc[9][1], loc[9][2], loc[9][3], classes.board.Ship, "", white, "", 0)
            self.clock_wrapper3 = self.board.ships[-1]
            self.board.active_ship = self.clock_wrapper3.unit_id
            if self.mainloop.m.game_variant == 0 or self.mainloop.m.game_variant == 1:
                self.clock3 = classes.drw.clock_linear_diff.Clock(self, self.clock_wrapper3, self.size * data[0],
                                                                  self.size * 3, self.times, self.data2[2:12])
            elif self.mainloop.m.game_variant == 2 or self.mainloop.m.game_variant == 3:
                self.clock3 = classes.drw.clock_linear_diff2.Clock(self, self.clock_wrapper3, self.size * data[0],
                                                                   self.size * 3, self.times, self.data2[2:12])
            elif self.mainloop.m.game_variant == 5:
                self.clock3 = classes.drw.clock_circular_diff.Clock(self, self.clock_wrapper3, self.size * 11,
                                                                    self.times, self.data2[2:12])

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def get_diff(self):
        t = copy.deepcopy(self.times)

        # calculate minutes
        if t[1][1] >= t[0][1]:
            m = t[1][1] - t[0][1]
        else:
            m = 60 + t[1][1] - t[0][1]
            t[1][0] -= 1

        # calculate hours
        if t[1][0] >= t[0][0]:
            h = t[1][0] - t[0][0]
        else:
            if self.show_24h:
                h = 24 + t[1][0] - t[0][0]
            else:
                h = 12 + t[1][0] - t[0][0]
        return [h, m]

    def next_field(self):
        self.home_square.update_me = True
        self.home_square.perm_outline_width = 5
        self.home_square = self.ans_m
        self.board.active_ship = self.ans_m.unit_id
        self.home_square.update_me = True
        self.mainloop.redraw_needed[0] = True

    def ai_walk(self):
        if self.home_square.perm_outline_width == 1:
            self.home_square.perm_outline_width = 5
        else:
            self.home_square.perm_outline_width = 1
        self.home_square.update_me = True
        self.mainloop.redraw_needed[0] = True

    def auto_check_reset(self):
        self.ans_h.set_display_check(None)
        self.ans_m.set_display_check(None)

        self.ans_h.set_outline(self.color3, 5)
        self.ans_m.set_outline(self.color4, 5)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if not self.show_msg:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.auto_check_reset()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    active = self.board.active_ship
                    for i in range(4):
                        if self.buttons[i].unit_id == active:
                            self.on_btn_click(i)
                            break
            if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN and not self.correct:
                lhv = len(self.home_square.value)
                self.changed_since_check = True
                if event.key == pygame.K_BACKSPACE:
                    if lhv > 0:
                        self.home_square.value = self.home_square.value[0:lhv - 1]
                else:
                    char = event.unicode
                    if len(char) > 0 and lhv < 3 and char in self.digits:
                        if lhv == 0:
                            self.home_square.value += char
                        elif lhv == 1:
                            if self.home_square.value == "0":
                                self.home_square.value = char
                            else:
                                if self.home_square == self.ans_h:
                                    if self.show_24h:
                                        n = int(self.home_square.value + char)
                                        if n > 23:
                                            self.home_square.value = char
                                        else:
                                            self.home_square.value += char
                                    else:
                                        n = int(self.home_square.value + char)
                                        if n > 12:
                                            self.home_square.value = char
                                        else:
                                            self.home_square.value += char
                                if self.home_square == self.ans_m:
                                    n = int(self.home_square.value + char)
                                    if n > 59:
                                        self.home_square.value = char
                                    else:
                                        self.home_square.value += char
                        elif lhv == 2:
                            self.home_square.value = char
                    if len(self.ans_h.value.strip()) > 0:
                        if self.home_square == self.ans_h and self.diff[0] == int(self.ans_h.value):
                            self.next_field()
                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True
            elif event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.board.active_ship == self.ans_h.unit_id:
                if len(self.ans_h.value.strip()) > 0 and self.diff[0] == int(self.ans_h.value):
                    self.next_field()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.home_square.update_me = True
                if self.board.active_ship == self.ans_h.unit_id:
                    self.home_square.perm_outline_width = 5
                    self.home_square = self.ans_h
                    self.board.active_ship = self.ans_h.unit_id
                elif self.board.active_ship == self.ans_m.unit_id:
                    self.home_square.perm_outline_width = 5
                    self.home_square = self.ans_m
                    self.board.active_ship = self.ans_m.unit_id
                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True

    def on_btn_click(self, active_id):
        if active_id == 0:
            self.change_time(-1, 0)
        elif active_id == 1:
            self.change_time(1, 0)
        elif active_id == 2:
            self.change_time(0, -1)
        elif active_id == 3:
            self.change_time(0, 1)

    def change_time(self, h, m):
        if h == 1:
            if self.data2[4] and self.ans_h.value == "23":
                self.ans_h.value = "0"
            elif not self.data2[4] and self.ans_h.value == "12":
                self.ans_h.value = "0"
            else:
                self.ans_h.value = str(int(self.ans_h.value) + 1)
        elif h == -1:
            if self.data2[4] and self.ans_h.value == "0":
                self.ans_h.value = "23"
            elif not self.data2[4] and self.ans_h.value == "0":
                self.ans_h.value = "12"
            else:
                self.ans_h.value = str(int(self.ans_h.value) - 1)
        elif m == 1:
            if self.ans_m.value == "59":
                self.ans_m.value = "0"
                self.change_time(1, 0)
            else:
                self.ans_m.value = str(int(self.ans_m.value) + 1)
        elif m == -1:
            if self.ans_m.value == "0":
                self.ans_m.value = "59"
                self.change_time(-1, 0)
            else:
                self.ans_m.value = str(int(self.ans_m.value) - 1)

        # update captions
        self.h_caption.set_value([self.lang._n("hour", int(self.ans_h.value)), ""])
        self.m_caption.set_value([self.lang._n("minute", int(self.ans_m.value)), ""])

        self.ans_m.update_me = True
        self.ans_h.update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        if not self.correct:
            correct = 0
            if len(self.ans_h.value.strip()) > 0 and self.diff[0] == int(self.ans_h.value):
                self.ans_h.set_outline((0, 255, 0), 5)
                self.ans_h.set_display_check(True)
                correct += 1
            else:
                self.ans_h.set_display_check(False)
                self.ans_h.set_outline((255, 0, 0), 5)

            if len(self.ans_m.value.strip()) > 0 and self.diff[1] == int(self.ans_m.value):
                self.ans_m.set_outline((0, 255, 0), 5)
                self.ans_m.set_display_check(True)
                correct += 1
            else:
                self.ans_m.set_outline((255, 0, 0), 5)
                self.ans_m.set_display_check(False)

            self.ans_m.update_me = True
            self.ans_h.update_me = True
            self.mainloop.redraw_needed[0] = True

            if correct == 2:
                self.correct = True
                self.ai_enabled = False
                self.level.next_board()
