# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.drw.percentage_multi_hq
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 2, 2)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 8)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = True

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color
        else:
            white = (255, 255, 255)

        data = [13, 8]
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]

        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True

        self.board.board_bg.line_color = (20, 20, 20)
        self.number_count = random.randint(2, 5)
        self.numbers = self.get_numbers(self.number_count, 5, 5)

        hues = []
        step = 255 // self.number_count
        hues.append(random.randint(5, 245))
        for i in range(1, self.number_count):
            hues.append((hues[0] + step * i) % 255)

        colors = [ex.hsv_to_rgb(hues[i], 187, 255) for i in range(self.number_count)]
        b_colors = [ex.hsv_to_rgb(hues[i], 187, 255) for i in range(self.number_count)]

        self.board.add_unit(0, 0, data[1], data[1], classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.percentage_multi_hq.Percentage(1, self.board.scale * data[1], colors, b_colors, self.numbers)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def get_numbers(self, count, dist, step):
        redraw = True
        nums = [x for x in range(dist, dist*(count+1), dist)]
        nums_total = sum(nums)
        remainder = 100 - nums_total
        if remainder > 0:
            while redraw:
                redraw = False
                l2 = nums[:]
                remainder = 100 - nums_total
                for i in range(count-1):
                    if remainder > 0:
                        a = random.randrange(0, remainder, step)
                        remainder -= a
                        l2[i] += a
                if remainder > 0:
                    l2[-1] += remainder
                l2s = sorted(l2)
                for i in range(1, count):
                    if l2s[i-1] > l2s[i] - dist:
                        redraw = True
                        break
        return l2

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #    active = self.board.active_ship

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
