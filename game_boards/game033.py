# -*- coding: utf-8 -*-

import random
import pygame
from math import fsum

import classes.board
import classes.drw.ratio_hq
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 2, 2)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 18, 10)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color

            h1 = 170
            h2 = 40
            h3 = 0
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 157, 255)
            color3 = ex.hsv_to_rgb(h2, 57, 255)
            self.bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            self.bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
            self.bd_color3 = ex.hsv_to_rgb(h3, 57, 155)
        else:
            white = (255, 255, 255)

            h1 = random.randrange(0, 255, 5)
            h2 = h1
            h3 = h1
            while (abs(max(h2, h1) - min(h2, h1)) < 30) or (abs(max(h3, h1) - min(h3, h1)) < 30) or (abs(max(h3, h2) - min(h3, h2)) < 30):
                h1 = random.randrange(0, 255, 5)
                h2 = random.randrange(0, 255, 5)
                h3 = random.randrange(0, 255, 5)

            color1 = ex.hsv_to_rgb(h1, 127, 255)
            color2 = ex.hsv_to_rgb(h2, 127, 255)
            color3 = ex.hsv_to_rgb(h3, 127, 255)
            self.bd_color1 = ex.hsv_to_rgb(h1, 187, 200)
            self.bd_color2 = ex.hsv_to_rgb(h2, 187, 200)
            self.bd_color3 = ex.hsv_to_rgb(h3, 187, 200)

        self.disabled_font_color = (200, 200, 200)

        data = [18, 10]
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]

        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        # self.board.board_bg.initcolor = color
        # self.board.board_bg.color = color
        self.board.board_bg.update_me = True

        self.board.board_bg.line_color = (20, 20, 20)

        self.max_total = 20

        num1 = num2 = num3 = 11
        while num1 + num2 + num3 > self.max_total:
            num1 = random.randint(1, 3)
            num2 = random.randint(1, 3)
            num3 = random.randint(1, 3)
        self.numbers = [num1, num2, num3]

        if self.numbers[2] == 0:
            offset = 2
        else:
            offset = 0



        self.board.add_unit(0, 0, data[1], data[1], classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.ratio_hq.Ratio(1, self.board.scale * data[1], color1, color2, color3, self.bd_color1, self.bd_color2, self.bd_color3, self.numbers)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()

        self.board.add_unit(data[1], 2, 2, 2, classes.board.Letter, "+", white, "", 31)
        self.board.ships[-1].font_color = self.bd_color1
        self.board.add_unit(data[1], 4, 2, 2, classes.board.Label, str(num1), white, "", 31)
        self.nm1 = self.board.units[-1]
        self.board.units[-1].font_color = self.bd_color1
        self.board.add_unit(data[1], 6, 2, 2, classes.board.Letter, "-", white, "", 31)
        self.board.ships[-1].font_color = self.bd_color1

        self.board.add_unit(data[1] + 2, 4, 1, 2, classes.board.Label, ":", white, "", 31)

        self.board.add_unit(data[1] + 3, 2, 2, 2, classes.board.Letter, "+", white, "", 31)
        self.board.ships[-1].font_color = self.bd_color2
        self.board.add_unit(data[1] + 3, 4, 2, 2, classes.board.Label, str(num2), white, "", 31)
        self.nm2 = self.board.units[-1]
        self.board.units[-1].font_color = self.bd_color2
        self.board.add_unit(data[1] + 3, 6, 2, 2, classes.board.Letter, "-", white, "", 31)
        self.board.ships[-1].font_color = self.bd_color2

        self.board.add_unit(data[1] + 5, 4, 1, 2, classes.board.Label, ":", white, "", 31)

        self.board.add_unit(data[1] + 6, 2, 2, 2, classes.board.Letter, "+", white, "", 31)
        self.board.ships[-1].font_color = self.bd_color3
        self.board.add_unit(data[1] + 6, 4, 2, 2, classes.board.Label, str(num3), white, "", 31)
        self.nm3 = self.board.units[-1]
        self.board.units[-1].font_color = self.bd_color3
        self.board.add_unit(data[1] + 6, 6, 2, 2, classes.board.Letter, "-", white, "", 31)
        self.board.ships[-1].font_color = self.bd_color3


        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = self.board.active_ship
            if active == 0:
                self.change_fract_btn(1, 0, 0)
            elif active == 1:
                self.change_fract_btn(-1, 0, 0)
            elif active == 2:
                self.change_fract_btn(0, 1, 0)
            elif active == 3:
                self.change_fract_btn(0, -1, 0)
            elif active == 4:
                self.change_fract_btn(0, 0, 1)
            elif active == 5:
                self.change_fract_btn(0, 0, -1)


    def change_fract_btn(self, n1, n2, n3):
        if n1 == 1:
            if fsum(self.numbers) < self.max_total:
                self.numbers[0] += 1
                if self.numbers[0] > 1:
                    self.board.ships[1].font_color = self.bd_color1
        if n1 == -1:
            if self.numbers[0] > 1:
                self.numbers[0] -= 1
                if self.numbers[0] == 1:
                    self.board.ships[1].font_color = self.disabled_font_color
        if n2 == 1:
            if fsum(self.numbers) < self.max_total:
                self.numbers[1] += 1
                if self.numbers[1] > 1:
                    self.board.ships[3].font_color = self.bd_color2
        if n2 == -1:
            if self.numbers[1] > 1:
                self.numbers[1] -= 1
                if self.numbers[1] == 1:
                    self.board.ships[3].font_color = self.disabled_font_color
        if n3 == 1:
            if fsum(self.numbers) < self.max_total:
                self.numbers[2] += 1
                if self.numbers[2] > 1:
                    self.board.ships[5].font_color = self.bd_color3
        if n3 == -1:
            if self.numbers[2] > 1:
                self.numbers[2] -= 1
                if self.numbers[2] == 1:
                    self.board.ships[5].font_color = self.disabled_font_color
        if fsum(self.numbers) == self.max_total:
            self.board.ships[0].font_color = self.disabled_font_color
            self.board.ships[2].font_color = self.disabled_font_color
            self.board.ships[4].font_color = self.disabled_font_color
        else:
            self.board.ships[0].font_color = self.bd_color1
            self.board.ships[2].font_color = self.bd_color2
            self.board.ships[4].font_color = self.bd_color3
        for each in self.board.ships:
            each.update_me = True

        self.nm1.set_value(str(self.numbers[0]))
        self.nm2.set_value(str(self.numbers[1]))
        self.nm3.set_value(str(self.numbers[2]))
        self.fraction.update_values(self.numbers)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()
        self.fraction_canvas.update_me = True
        self.mainloop.redraw_needed[0] = True



    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
