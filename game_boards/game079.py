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

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
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
        trans_color = (0, 0, 0, 0)

        if self.lang.lang == "fi":
            w = 18
            bw = 12
        else:
            w = 14
            bw = 8

        data = [w, 14, 0, 10]

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

        self.board.add_unit(x1+2, 0, w-4, 1, classes.board.Label, "%d - %d" % (data[2], data[3]), color1, "", 0)
        self.range_label = self.board.units[-1]
        self.range_label.font_color = self.font_color

        y = 2
        for i in range(data[2], data[3] + 1):
            if self.lang.ltr_text:
                sv = str(i)
            else:
                sv = self.lang.n2spk(i)
            self.board.add_unit(x1+2, y, 2, 1, classes.board.Letter, str(i), color1, "", 2)
            self.board.ships[-1].speaker_val = sv
            self.board.ships[-1].speaker_val_update = False
            self.board.ships[-1].normal_cl = color1
            self.board.ships[-1].highlight_cl = color1a
            self.board.add_unit(x2+2, y, bw, 1, classes.board.Letter, self.lang.n2txt(i), color0, "", 2)
            self.board.ships[-1].speaker_val = sv
            self.board.ships[-1].speaker_val_update = False
            self.board.ships[-1].normal_cl = color0
            self.board.ships[-1].highlight_cl = color0a
            y += 1

        self.outline_all(self.color2, 1)

        self.board.add_unit(x1, 2, 2, 11, classes.board.ImgCenteredShip, "", trans_color, img_src='nav_l.png',
                            alpha=True)
        self.lt = self.board.ships[-1]
        self.lt.outline = False
        self.board.add_unit(x2+bw+2, 2, 2, 11, classes.board.ImgCenteredShip, "", trans_color, img_src='nav_r.png',
                            alpha=True)
        self.rt = self.board.ships[-1]
        self.rt.outline = False

        for each in self.board.ships:
            each.font_color = self.font_color
            each.immobilize()

        self.page_number = 0

    def next_slide(self, n):
        if n == 1:
            if self.page_number < 9:
                self.page_number += 1
            else:
                self.page_number = 0
        else:
            if self.page_number > 0:
                self.page_number -= 1
            else:
                self.page_number = 9

        self.create_card()
        self.mainloop.redraw_needed[0] = True

    def create_card(self):
        for i in range(0, 22, 2):
            n = self.page_number * 10 + i // 2
            if self.lang.ltr_text:
                sv = str(n)
            else:
                sv = self.lang.n2spk(n)
            self.board.ships[i].set_value(str(n))
            self.board.ships[i+1].set_value(self.lang.n2txt(n))

            self.board.ships[i].speaker_val = sv
            self.board.ships[i].speaker_val_update = False
            self.board.ships[i+1].speaker_val = sv
            self.board.ships[i+1].speaker_val_update = False

            self.board.ships[i].update_me = True
            self.board.ships[i+1].update_me = True
        self.range_label.set_value("%d - %d" % (self.page_number * 10, self.page_number * 10 + 10))
        self.range_label.update_me = True

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
            if 0 <= self.board.active_ship < 22:
                active = self.board.ships[self.board.active_ship]
                self.onClick(active)
            else:
                pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
                if self.lt.rect.topleft[0] < pos[0] < self.lt.rect.topleft[0] + self.lt.rect.width and \
                                        self.lt.rect.topleft[1] < pos[1] < self.lt.rect.topleft[
                            1] + self.lt.rect.height:
                    self.next_slide(-1)
                elif self.rt.rect.topleft[0] < pos[0] < self.rt.rect.topleft[0] + self.rt.rect.width and \
                                        self.rt.rect.topleft[1] < pos[1] < self.rt.rect.topleft[
                            1] + self.rt.rect.height:
                    self.next_slide(1)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
