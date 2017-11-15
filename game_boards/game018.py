# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 3, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 30, 230)  # highlight 1
        self.color = color0
        self.highlight_color = ex.hsv_to_rgb(h, 230, 150)
        white = (255, 255, 255)
        bg_col = (255, 255, 255)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                bg_col = (0, 0, 0)
        self.disp_counter = 0
        self.disp_len = 1
        # data = [x_count, y_count, number_count, top_limit, ordered]

        if self.level.lvl == 1:
            data = [4, 2, 3, 4, 2]
        elif self.level.lvl == 2:
            data = [5, 2, 3, 5, 2]
        elif self.level.lvl == 3:
            data = [4, 3, 3, 4, 3]
        elif self.level.lvl == 4:
            data = [6, 3, 3, 6, 3]
        elif self.level.lvl == 5:
            data = [5, 4, 3, 5, 4]
        elif self.level.lvl == 6:
            data = [6, 4, 3, 6, 4]
        elif self.level.lvl == 7:
            data = [7, 4, 3, 7, 4]
        elif self.level.lvl == 8:
            data = [6, 5, 3, 6, 5]
        elif self.level.lvl == 9:
            data = [6, 6, 3, 6, 6]
        elif self.level.lvl == 10:
            data = [7, 6, 3, 7, 6]

        self.chapters = [1, 5, 10]

        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            x = self.get_x_count(data[1], even=True)
        else:
            x = self.get_x_count(data[1], even=False)

        if x > data[0]:
            data[0] = x

        self.data = data
        self.found = 0
        self.clicks = 0
        self.square_count = self.data[3] * self.data[4]
        self.history = [None, None]

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        if self.mainloop.m.game_variant == 0:
            image_src = [os.path.join('memory', "m_img%da.png" % (i)) for i in range(1, 22)]
            self.back_img_src = os.path.join('memory', "m_img22a.png")
        elif self.mainloop.m.game_variant == 1:
            image_src = [os.path.join('memory', "f_img%da.png" % (i)) for i in range(1, 22)]
            self.back_img_src = os.path.join('memory', "m_img22a.png")
        elif self.mainloop.m.game_variant == 2:
            image_src = [os.path.join('memory', "v_img%da.png" % (i)) for i in range(1, 22)]
            self.back_img_src = os.path.join('memory', "m_img22a.png")
        elif self.mainloop.m.game_variant == 3:
            image_src = [os.path.join('memory', "n_img%da.png" % (i)) for i in range(1, 22)]
            self.back_img_src = os.path.join('memory', "m_img22a.png")

        self.card_fronts = []
        self.completed_mode = False
        # pick images - half the square_count
        if self.mainloop.m.game_variant == 3:
            if self.level.lvl < 6:
                choice = [x for x in range(0, 10)]
            else:
                choice = [x for x in range(0, self.square_count // 2)]
        else:
            choice = [x for x in range(0, 21)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2
        random.shuffle(self.chosen)

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        w2 = (data[0] - data[3]) // 2  # side margin width

        x = w2
        y = h1
        self.card_back = classes.board.ImgSurf(self.board, 1, 1, white, self.back_img_src)

        for i in range(self.square_count):
            self.board.add_unit(x, y, 1, 1, classes.board.ImgShip, "", white, self.back_img_src)
            self.card_fronts.append(classes.board.ImgSurf(self.board, 1, 1, white, image_src[self.chosen[i]]))
            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            if x >= w2 + data[3] - 1:
                x = w2
                y += 1
            else:
                x += 1
        self.outline_all([200, 200, 200], 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[
            1] == None and self.ai_enabled == False:  # and self.start_sequence==False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if active.uncovered == False:
                    if self.history[0] is None:
                        active.img = self.card_fronts[active.unit_id].img.copy()
                        self.history[0] = active
                        self.clicks += 1
                        active.uncovered = True
                    elif self.history[1] is None:
                        active.img = self.card_fronts[active.unit_id].img.copy()
                        self.history[1] = active
                        self.clicks += 1
                        if self.chosen[self.history[0].unit_id] != self.chosen[self.history[1].unit_id]:
                            self.ai_enabled = True
                            self.history[0].uncovered = False
                        else:
                            self.history[0].uncovered = True
                            self.history[1].uncovered = True
                            self.history[0].set_display_check(True)
                            self.history[1].set_display_check(True)
                            self.found += 2
                            if self.found == self.square_count:
                                self.completed_mode = True
                                self.ai_enabled = True
                            self.history = [None, None]
                    active.update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.level.next_board()
            else:
                self.history[0].img = self.card_back.img.copy()
                self.history[1].img = self.card_back.img.copy()
                self.history[0].update_me = True
                self.history[1].update_me = True
                self.history = [None, None]
                self.ai_enabled = False
                self.disp_counter = 0

    def check_result(self):
        pass
