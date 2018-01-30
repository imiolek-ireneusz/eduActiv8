# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.drw.percentage_hq
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 2, 2)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 8)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color

            h1 = 170
            h2 = 40
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            white = (255, 255, 255)

            h1 = random.randrange(0, 255, 5)
            color1 = ex.hsv_to_rgb(h1, 150, 255)
            color2 = ex.hsv_to_rgb(h1, 40, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 187, 200)
            bd_color2 = ex.hsv_to_rgb(h1, 75, 255)

        data = [13, 8]
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

        num1 = range(5, 100, 5)[random.randint(0, 18)]
        self.number = num1


        self.board.add_unit(0, 0, data[1], data[1], classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.percentage_hq.Percentage(1, self.board.scale * data[1], color1, color2, bd_color1, bd_color2, self.number)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()

        self.board.add_unit(data[1] + 1, 5, 2, 2, classes.board.Letter, "-", white, "", 31)
        self.board.ships[-1].font_color = bd_color1
        self.board.add_unit(data[1], 3, 4, 2, classes.board.Label, str(num1) + "%", white, "", 31)
        self.nm1 = self.board.units[-1]
        self.board.units[-1].font_color = bd_color1
        self.board.add_unit(data[1] + 1, 1, 2, 2, classes.board.Letter, "+", white, "", 31)
        self.board.ships[-1].font_color = bd_color1

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = self.board.active_ship
            if active == 0:
                self.change_perc_btn(-1)
            elif active == 1:
                self.change_perc_btn(1)


    def change_perc_btn(self, n1):
        if n1 == -1:
            if self.number > 1:
                self.number -= 5
        elif n1 == 1:
            if self.number < 100:
                self.number += 5

        self.nm1.set_value(str(self.number)+"%")
        self.fraction.update_values(self.number)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()
        self.fraction_canvas.update_me = True
        self.mainloop.redraw_needed[0] = True



    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
