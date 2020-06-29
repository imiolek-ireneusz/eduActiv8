# -*- coding: utf-8 -*-

import random
import pygame
import os

import classes.board
import classes.drw.thermometer
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 2, 2)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 15, 9)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False

        # self.rng = (random.randrange(-30, -5, 5), random.randrange(5, 30, 5))
        self.rng = [-30, 30]
        self.number = random.randint(self.rng[0], self.rng[1])

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color
            h1 = 170
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
        else:
            white = (255, 255, 255)
            color1 = self.temp2col(self.number)
            hsv_col = ex.rgb_to_hsv(color1[0], color1[1], color1[2])
            bd_color1 = ex.hsv_to_rgb(hsv_col[0], 187, 200)
        transp = (0, 0, 0, 0)

        data = [7, 10]
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]

        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True

        self.board.board_bg.line_color = (20, 20, 20)
        self.points = int(round((self.board.scale * 72 / 96) * 1.2, 0))
        self.t_font = pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSans.ttf'),
                                       (int(self.points / (self.board.scale / (60 * self.board.scale * 3 / 500.0)))))

        self.board.add_unit(0, 0, 3, data[1], classes.board.Label, "", white, "", 0)
        self.ther_canvas = self.board.units[-1]

        self.thermometer = classes.drw.thermometer.Thermometer(self, 3, self.data[1], self.board.scale,
                                                               color1, bd_color1, self.rng, self.number, 5)
        self.ther_canvas.painting = self.thermometer.get_canvas().copy()

        self.board.add_unit(4, 6, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(bd_color1)

        self.board.add_unit(3, 4, 4, 2, classes.board.Label, str(self.number)+"°C", white, "", 31)
        self.nm1 = self.board.units[-1]
        self.board.units[-1].font_color = bd_color1

        self.board.add_unit(4, 2, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(bd_color1)

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def temp2col(self, number):
        if number > 5:
            return self.get_color_on_gradient((253, 215, 37), (199, 2, 2), 5, 35, number)
        elif number > 0:
            return self.get_color_on_gradient((120, 243, 251), (253, 215, 37), 0, 5, number)
        else:
            return self.get_color_on_gradient((0, 47, 193), (120, 243, 251), -35, 0, number)

    def get_color_on_gradient(self, color_start, color_end, range_start, range_end, number):
        x1, x2 = range_start, range_end

        h = x2 - x1
        a, b = color_start, color_end

        rate = (
            float(b[0] - a[0]) / h,
            float(b[1] - a[1]) / h,
            float(b[2] - a[2]) / h
        )

        color = (
            int(min(max(a[0] + (rate[0] * (number - x1)), 0), 255)),
            int(min(max(a[1] + (rate[1] * (number - x1)), 0), 255)),
            int(min(max(a[2] + (rate[2] * (number - x1)), 0), 255))
        )
        return color

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = self.board.active_ship
            if active == 0:
                self.change_num_btn(-1)
            elif active == 1:
                self.change_num_btn(1)

    def change_num_btn(self, n1):
        if n1 == -1:
            if self.number > self.rng[0]:
                self.number -= 1
        elif n1 == 1:
            if self.number < self.rng[1]:
                self.number += 1

        color1 = self.temp2col(self.number)
        hsv_col = ex.rgb_to_hsv(color1[0], color1[1], color1[2])
        bd_color1 = ex.hsv_to_rgb(hsv_col[0], 187, 200)

        self.thermometer.update_colors(color1, bd_color1)
        self.nm1.set_value(str(self.number)+"°C")
        self.thermometer.update_values(self.number)
        self.ther_canvas.painting = self.thermometer.get_canvas().copy()
        self.ther_canvas.update_me = True

        for each in self.board.ships:
            each.set_tint_color(bd_color1)
            each.update_me = True

        self.nm1.font_color = bd_color1
        self.nm1.update_me = True

        self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
