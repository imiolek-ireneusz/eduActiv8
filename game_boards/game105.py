# -*- coding: utf-8 -*-

import os
import random
import pygame

import classes.board
import classes.drw.clock
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
            white = self.mainloop.scheme.u_color
        else:
            white = (255, 255, 255)

        self.h_col = ex.hsv_to_rgb(225, 190, 220)
        self.m_col = ex.hsv_to_rgb(170, 190, 220)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        transp = (0, 0, 0, 0)

        h = random.randrange(150, 240, 5)
        self.font_color = ex.hsv_to_rgb(h, 255, 170)

        data = [21, 11]
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]

        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True

        self.board.board_bg.line_color = (20, 20, 20)

        self.size = self.board.scale
        th1 = random.randint(1, 12)
        th2 = random.randint(1, 12)
        self.times = [[th1, 0], [th2, random.randrange(5, 55, 5)]]
        self.data2 = [12, 6, True, True, False, False, False, True, False, True, True, True]

        self.clock_fonts = []
        self.points = int(round((self.board.scale * 72 / 96) * 1.2, 0))
        xw = [5, 11]
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             42 * self.size * xw[0] / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             60 * self.size * xw[0] / 500.0))))))
        self.clock_fonts.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSans.ttf'),
                                                 (int(self.points / (self.board.scale / (
                                                             30 * self.size * xw[0] / 500.0))))))

        self.digi_clocks = []
        self.board.add_unit(1, 1, 1, 1, classes.board.Letter, "%02d" % self.times[0][0], white, "", 0)
        self.board.ships[-1].font_color = self.h_col
        self.digi_clocks.append(self.board.ships[-1])
        self.board.add_unit(2, 1, 1, 1, classes.board.Letter, ":", white, "", 0)
        self.board.ships[-1].font_color = self.black
        self.board.add_unit(3, 1, 1, 1, classes.board.Letter, "%02d" % self.times[0][1], white, "", 0)
        self.board.ships[-1].font_color = self.m_col
        self.digi_clocks.append(self.board.ships[-1])

        self.board.add_unit(0, 3, xw[0], xw[0], classes.board.Ship, "", white, "", 0)
        self.clock_wrapper = self.board.ships[-1]
        self.board.active_ship = self.clock_wrapper.unit_id
        self.clock1 = classes.drw.clock.Clock(self, self.clock_wrapper, self.size * xw[0], self.times[0],
                                              self.data2[2:11])

        self.board.add_unit(0, xw[0]+3, xw[0], 1, classes.board.Letter, self.lang.d["start_time"], white, "", 2)
        self.board.ships[-1].font_color = self.font_color

        self.board.add_unit(xw[0] + 1, 1, 1, 1, classes.board.Letter, "%02d" % self.times[1][0], white, "", 0)
        self.board.ships[-1].font_color = self.h_col
        self.digi_clocks.append(self.board.ships[-1])
        self.board.add_unit(xw[0] + 2, 1, 1, 1, classes.board.Letter, ":", white, "", 0)
        self.board.ships[-1].font_color = self.black
        self.board.add_unit(xw[0] + 3, 1, 1, 1, classes.board.Letter, "%02d" % self.times[1][1], white, "", 0)
        self.board.ships[-1].font_color = self.m_col
        self.digi_clocks.append(self.board.ships[-1])

        self.board.add_unit(xw[0], 3, xw[0], xw[0], classes.board.Ship, "", white, "", 0)
        self.clock_wrapper = self.board.ships[-1]
        self.board.active_ship = self.clock_wrapper.unit_id
        self.clock2 = classes.drw.clock.Clock(self, self.clock_wrapper, self.size * xw[0], self.times[1],
                                              self.data2[2:11])

        self.board.add_unit(xw[0], xw[0]+3, xw[0], 1, classes.board.Letter, self.lang.d["end_time"], white, "", 2)
        self.board.ships[-1].font_color = self.font_color

        # circular diff
        self.board.add_unit(xw[0] * 2, 0, xw[1], xw[1], classes.board.Ship, "", white, "", 0)
        self.clock_wrapper = self.board.ships[-1]
        self.board.active_ship = self.clock_wrapper.unit_id
        self.clock3 = classes.drw.clock_circular_diff.Clock(self, self.clock_wrapper, self.size * xw[1],
                                                            self.times, self.data2[2:12])

        self.buttons = []
        # add buttons for first clock
        self.board.add_unit(1, 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(1, 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(3, 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)
        self.board.add_unit(3, 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        # add buttons for second clock
        self.board.add_unit(xw[0] + 1, 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(xw[0] + 1, 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)
        self.board.add_unit(xw[0] + 3, 0, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)
        self.board.add_unit(xw[0] + 3, 2, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        for i in range(8):
            self.buttons.append(self.board.ships[-8 + i])

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = self.board.active_ship
            for i in range(8):
                if self.buttons[i].unit_id == active:
                    self.on_btn_click(i)
                    break

    def on_btn_click(self, active_id):
        if active_id == 0:  # h1 + 1
            self.change_time(0, 1, 0)
        elif active_id == 1:  # h1 - 1
            self.change_time(0, -1, 0)
        elif active_id == 2:  # m1 + 1
            self.change_time(0, 0, 1)
        elif active_id == 3:  # m1 - 1
            self.change_time(0, 0, -1)
        elif active_id == 4:  # h2 + 1
            self.change_time(1, 1, 0)
        elif active_id == 5:  # h2 - 1
            self.change_time(1, -1, 0)
        elif active_id == 6:  # m2 + 1
            self.change_time(1, 0, 1)
        elif active_id == 7:  # m2 - 1
            self.change_time(1, 0, -1)

    def change_time(self, clock_id, h, m):
        for i in range(2):
            if clock_id == i:
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
                        self.change_time(clock_id, 1, 0)
                    else:
                        self.times[i][1] += 1
                elif m == -1:
                    if self.times[i][1] == 0:
                        self.times[i][1] = 59
                        self.change_time(clock_id, -1, 0)
                    else:
                        self.times[i][1] -= 1
                break
        self.update_clocks(clock_id)

    def update_clocks(self, clock_id):
        if clock_id == 0:
            self.digi_clocks[0].set_value("%02d" % self.times[0][0])
            self.digi_clocks[1].set_value("%02d" % self.times[0][1])
            self.clock1.draw_all()
        else:
            self.digi_clocks[2].set_value("%02d" % self.times[1][0])
            self.digi_clocks[3].set_value("%02d" % self.times[1][1])
            self.clock2.draw_all()

        self.clock3.draw_all(self.times)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
