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
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 8)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False

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
        transp = (0, 0, 0, 0)

        self.h_col = ex.hsv_to_rgb(225, 190, 220)
        self.m_col = ex.hsv_to_rgb(170, 190, 220)

        h = random.randrange(150, 240, 5)
        self.font_color = ex.hsv_to_rgb(h, 255, 170)
        data = [20, 11, 25]
        self.data = data

        self.lvl_data = [1, 11, 1, 0, 12, 0, 0, 2, 0, 0, 5, False, True, True]

        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]
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
        th2 = th1
        if self.lvl_data[7] == 2:
            tm1 = 0
            tm2 = 0
        else:
            tm1 = random.randrange(self.lvl_data[5], self.lvl_data[6], self.lvl_data[10])
            tm2 = tm1

        self.addition = True

        self.show_24h = self.data2[4]
        self.times = [[th1, tm1], [th2, tm2]]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.clock_fonts = []
        self.points = int(round((self.board.scale * 72 / 96) * 1.2, 0))
        xw = [7, 0]
        top_margin = xw[0] + 1
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             42 * self.size * xw[0] / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             data[2] * self.size * xw[0] / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSans.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             20 * self.size * xw[0] / 500.0))))))

        # add buttons for first clock
        self.board.add_unit(2, top_margin + 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(2, top_margin + 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(4, top_margin + 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)
        self.board.add_unit(4, top_margin + 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        # add buttons for second clock
        self.board.add_unit(xw[0] + 8, top_margin + 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(xw[0] + 8, top_margin + 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(xw[0] + 10, top_margin + 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)
        self.board.add_unit(xw[0] + 10, top_margin + 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        self.board.add_unit(1, 0, xw[0] - 2, 1, classes.board.Letter, self.lang.d["start_time"], white, "", 3)
        self.board.ships[-1].font_color = self.font_color

        self.board.add_unit(xw[0] + 7, 0, xw[0] - 2, 1, classes.board.Letter, self.lang.d["end_time"], white, "", 3)
        self.board.ships[-1].font_color = self.font_color

        self.board.add_unit(xw[0], 0, 6, 1, classes.board.Letter, self.lang.d["difference"], white, "", 2)
        self.board.ships[-1].font_color = self.font_color

        self.diff = self.get_diff()

        self.board.add_unit(xw[0], 4, 6, 1, classes.board.Letter,
                            [self.lang._n("hour", 0), ""], white, "", 4)
        self.board.ships[-1].font_color = color3
        self.h_caption = self.board.ships[-1]

        self.board.add_unit(xw[0], 7, 6, 1, classes.board.Letter,
                            [self.lang._n("minute", 0), ""], white, "", 4)
        self.board.ships[-1].font_color = color4
        self.m_caption = self.board.ships[-1]

        self.buttons = []

        self.board.add_unit(xw[0] + 1, 2, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)

        self.board.add_unit(xw[0] + 4, 2, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)

        self.board.add_unit(xw[0] + 1, 5, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        self.board.add_unit(xw[0] + 4, 5, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        for i in range(4):
            self.buttons.append(self.board.ships[-4 + i])

        self.board.add_unit(xw[0] + 2, 2, 2, 2, classes.board.Letter, "0", white, "", 31)
        self.ans_h = self.board.ships[-1]
        self.board.active_ship = self.ans_h.unit_id
        self.home_square = self.ans_h

        self.board.add_unit(xw[0] + 2, 5, 2, 2, classes.board.Letter, "0", white, "", 31)
        self.ans_m = self.board.ships[-1]

        self.ans_h.immobilize()
        self.ans_m.immobilize()
        self.ans_h.readable = False
        self.ans_m.readable = False
        self.ans_h.font_color = color3
        self.ans_m.font_color = color4

        self.digi_clocks = []

        # add first time in digital form
        top_margin = xw[0] + 1
        self.board.add_unit(2, top_margin + 1, 1, 1, classes.board.Letter, "%02d" % self.times[0][0], white, "", 0)
        self.board.ships[-1].font_color = self.h_col
        self.digi_clocks.append(self.board.ships[-1])
        self.board.add_unit(3, top_margin + 1, 1, 1, classes.board.Letter, ":", white, "", 0)
        self.board.ships[-1].font_color = colon_col
        self.board.add_unit(4, top_margin + 1, 1, 1, classes.board.Letter, "%02d" % self.times[0][1], white, "", 0)
        self.board.ships[-1].font_color = self.m_col
        self.digi_clocks.append(self.board.ships[-1])

        # add second time in digital form
        self.board.add_unit(xw[0] + 8, top_margin + 1, 1, 1, classes.board.Letter,
                            "%02d" % self.times[1][0], white, "", 0)
        self.board.ships[-1].font_color = self.h_col
        self.digi_clocks.append(self.board.ships[-1])
        self.board.add_unit(xw[0] + 9, top_margin + 1, 1, 1, classes.board.Letter, ":", white, "", 0)
        self.board.ships[-1].font_color = colon_col
        self.board.add_unit(xw[0] + 10, top_margin + 1, 1, 1, classes.board.Letter,
                            "%02d" % self.times[1][1], white, "", 0)
        self.board.ships[-1].font_color = self.m_col
        self.digi_clocks.append(self.board.ships[-1])

        # add first clock
        self.board.add_unit(0, 1, xw[0], xw[0], classes.board.Ship, "", white, "", 0)
        self.clock_wrapper1 = self.board.ships[-1]
        self.board.active_ship = self.clock_wrapper1.unit_id
        self.clock1 = classes.drw.clock.Clock(self, self.clock_wrapper1, self.size * xw[0], self.times[0],
                                              self.data2[2:11])

        # add second clock
        self.board.add_unit(6 + xw[0], 1, xw[0], xw[0], classes.board.Ship, "", white, "", 0)
        self.clock_wrapper2 = self.board.ships[-1]
        self.board.active_ship = self.clock_wrapper2.unit_id
        self.clock2 = classes.drw.clock.Clock(self, self.clock_wrapper2, self.size * xw[0], self.times[1],
                                                  self.data2[2:11])

        # linear diff
        if self.lvl_data[13]:
            self.board.add_unit(xw[0]-2, xw[0] + 1, 10, 3, classes.board.Ship, "", white, "", 0)
            self.clock_wrapper3 = self.board.ships[-1]
            self.board.active_ship = self.clock_wrapper3.unit_id
            if self.mainloop.m.game_variant == 0:
                self.clock3 = classes.drw.clock_linear_diff.Clock(self, self.clock_wrapper3,
                                                                  self.size * 10,
                                                                  self.size * 3, self.times, self.data2[2:12])
            elif self.mainloop.m.game_variant == 1:
                self.clock3 = classes.drw.clock_linear_diff2.Clock(self, self.clock_wrapper3,
                                                                   self.size * 10,
                                                                   self.size * 3, self.times, self.data2[2:12])

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

    def time_with_diff(self, diff):
        t = copy.deepcopy(self.times)
        if self.show_24h:
            mod = 24
        else:
            mod = 12

        #calculate minutes
        if self.addition:
            m = t[0][1] + diff[1]
            if m < 60:
                h = (t[0][0] + diff[0]) % mod
            else:
                m = m % 60
                h = (t[0][0] + 1 + diff[0]) % mod
        else:
            m = t[0][1] - diff[1]
            if m < 0:
                m = 60 + m
                h = t[0][0] - diff[0] - 1
            else:
                h = t[0][0] - diff[0]
            if h < 0:
                h = mod + h

        if not self.show_24h and h == 0:
            h = 12
        return [h, m]

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.show_msg == False:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                active = self.board.active_ship
                if True:
                    found = False
                    for i in range(4):
                        if self.buttons[i].unit_id == active:
                            self.on_btn_click(i)
                            found = True
                            break
                        elif self.board.ships[i].unit_id == active:
                            self.on_btn2_click(i)
                            found = True
                    if not found:
                        for i in range(4, 8):
                            if self.board.ships[i].unit_id == active:
                                self.on_btn2_click(i-4)
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

    def on_btn2_click(self, active_id):
        if active_id == 0:  # h1 + 1
            self.change_first_time(1, 0)
        elif active_id == 1:  # h1 - 1
            self.change_first_time(-1, 0)
        elif active_id == 2:  # m1 + 1
            self.change_first_time(0, 1)
        elif active_id == 3:  # m1 - 1
            self.change_first_time(0, -1)

    def change_first_time(self, h, m):
        i = 0
        if h == 1:
            if self.data2[4] and self.times[i][0] == 23:
                self.times[i][0] = 0
            elif not self.data2[4] and self.times[i][0] == 12:
                self.times[i][0] = 1
            else:
                self.times[i][0] += 1
        elif h == -1:
            if self.data2[4] and self.times[i][0] == 0:
                self.times[i][0] = 23
            elif not self.data2[4] and self.times[i][0] == 1:
                self.times[i][0] = 12
            else:
                self.times[i][0] -= 1
        elif m == 1:
            if self.times[i][1] == 59:
                self.times[i][1] = 0
                self.change_first_time(1, 0)
            else:
                self.times[i][1] += 1
        elif m == -1:
            if self.times[i][1] == 0:
                self.times[i][1] = 59
                self.change_first_time(-1, 0)
            else:
                self.times[i][1] -= 1
        self.times[1] = self.time_with_diff([int(self.ans_h.value), int(self.ans_m.value)])
        self.update_clocks()

    def change_time(self, h, m):
        if h == 1:
            if self.data2[4] and self.ans_h.value == "23":
                self.ans_h.value = "0"
            elif not self.data2[4] and self.ans_h.value == "11":
                self.ans_h.value = "0"
            else:
                self.ans_h.value = str(int(self.ans_h.value) + 1)
        elif h == -1:
            if self.data2[4] and self.ans_h.value == "0":
                self.ans_h.value = "23"
            elif not self.data2[4] and self.ans_h.value == "0":
                self.ans_h.value = "11"
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

        #update second clock
        self.times[1] = self.time_with_diff([int(self.ans_h.value), int(self.ans_m.value)])

        # update captions
        self.h_caption.set_value([self.lang._n("hour", int(self.ans_h.value)), ""])
        self.m_caption.set_value([self.lang._n("minute", int(self.ans_m.value)), ""])
        self.ans_m.update_me = True
        self.ans_h.update_me = True

        self.update_clocks()

    def update_clocks(self, clock_id=None):
        if clock_id is None or clock_id == 0:
            self.digi_clocks[0].set_value("%02d" % self.times[0][0])
            self.digi_clocks[1].set_value("%02d" % self.times[0][1])
            self.clock1.draw_all(self.times[0])
        if clock_id is None or clock_id == 1:
            self.digi_clocks[2].set_value("%02d" % self.times[1][0])
            self.digi_clocks[3].set_value("%02d" % self.times[1][1])
            self.clock2.draw_all(self.times[1])

        if self.addition:
            self.clock3.draw_all(self.times)
        else:
            self.clock3.draw_all(self.times[::-1])

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
