# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 12, 14)

    def create_game_objects(self, level=1):
        # create non-movable objects

        self.vis_buttons = [0, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        color1 = ex.hsv_to_rgb(h, 90, 230)

        color0a = ex.hsv_to_rgb(h, 70, 230)  # highlight 1
        color1a = ex.hsv_to_rgb(h, 120, 230)

        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
        self.font_color = self.color2

        if self.lang.lang == "fi":
            w = 14
            bw = 12
        else:
            w = 10
            bw = 8
        if self.level.lvl == 1:
            data = [w, 14, 0, 10]
        elif self.level.lvl == 2:
            data = [w, 14, 10, 20]
        elif self.level.lvl == 3:
            data = [w, 14, 20, 30]
        elif self.level.lvl == 4:
            data = [w, 14, 30, 40]
        elif self.level.lvl == 5:
            data = [w, 14, 40, 50]
        elif self.level.lvl == 6:
            data = [w, 14, 50, 60]
        elif self.level.lvl == 7:
            data = [w, 14, 60, 70]
        elif self.level.lvl == 8:
            data = [w, 14, 70, 80]
        elif self.level.lvl == 9:
            data = [w, 14, 80, 90]
        elif self.level.lvl == 10:
            data = [w, 14, 90, 100]

        # rescale the number of squares horizontally to better match the screen width
        x = self.get_x_count(data[1], even=True)

        if x > data[0]:
            data[0] = x

        self.data = data

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        self.in_focus = None
        self.center = self.data[0] // 2

        x1 = self.center - w // 2
        x2 = self.center - (w // 2 - 2)

        self.board.add_unit(x1, 0, w, 1, classes.board.Label, "%d - %d" % (data[2], data[3]), color1, "", 0)
        self.board.units[-1].font_color = self.font_color

        y = 2
        for i in range(data[2], data[3] + 1):
            if self.lang.ltr_text:
                sv = str(i)
            else:
                sv = self.lang.n2spk(i)
            self.board.add_unit(x1, y, 2, 1, classes.board.Letter, str(i), color1, "", 2)
            self.board.ships[-1].speaker_val = sv
            self.board.ships[-1].speaker_val_update = False
            self.board.ships[-1].normal_cl = color1
            self.board.ships[-1].highlight_cl = color1a
            self.board.add_unit(x2, y, bw, 1, classes.board.Letter, self.lang.n2txt(i), color0, "", 2)
            self.board.ships[-1].speaker_val = sv
            self.board.ships[-1].speaker_val_update = False
            self.board.ships[-1].normal_cl = color0
            self.board.ships[-1].highlight_cl = color0a
            y += 1

        for each in self.board.ships:
            each.font_color = self.font_color
            each.immobilize()

        self.outline_all(self.color2, 1)

    def onClick(self, new_focus):
        if self.in_focus is not None:
            self.in_focus.color = self.in_focus.normal_cl
            self.in_focus.update_me = True
        if new_focus is not None:
            self.in_focus = new_focus
            self.in_focus.color = self.in_focus.highlight_cl
            self.in_focus.update_me = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # and self.start_sequence==False:
            if 0 <= self.board.active_ship < 23:
                active = self.board.ships[self.board.active_ship]
                self.onClick(active)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
