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
        self.level = lc.Level(self, mainloop, 1, 20)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.decolorable = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.board.draw_grid = False

        outline_color = (150, 150, 150)
        white = (255, 255, 255)
        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
            white = (0, 0, 0)
        # setting level variable
        # data = [x_count, y_count, number_count, top_limit, ordered]
        data = [7, 6, 8, 3, 3]
        self.chapters = [1, 5, 10, 15, 20]

        # rescale the number of squares horizontally to better match the screen width
        data[0] = self.get_x_count(data[1], even=False)

        self.data = data

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        if self.mainloop.m.game_variant == 0:
            if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
                image_src = [os.path.join('memory', "m_img%da.png" % (i)) for i in range(1, 21)]
                grey_image_src = [os.path.join('memory', "m_img%db.png" % (i)) for i in range(1, 22)]
            else:
                image_src = [os.path.join('schemes', "black", "match_animals", "m_img%da.png" % (i)) for i in
                             range(1, 21)]
                grey_image_src = [os.path.join('schemes', "black", "match_animals", "m_img%db.png" % (i)) for i in
                                  range(1, 22)]

        elif self.mainloop.m.game_variant == 1:
            image_src = [os.path.join('memory', "f_img%da.png" % (i)) for i in range(1, 21)]
            grey_image_src = [os.path.join('memory', "m_img22b.png")]
        elif self.mainloop.m.game_variant == 2:
            image_src = [os.path.join('memory', "n_img%da.png" % (i)) for i in range(2, 22)]
            grey_image_src = [os.path.join('memory', "m_img22b.png")]

        self.bg_img_src = image_src[self.level.lvl - 1]  # os.path.join('memory', "m_img13a.png")
        if len(grey_image_src) > 1:
            self.bg_img_grey_src = grey_image_src[self.level.lvl - 1]  # os.path.join('memory', "m_img13b.png")
        else:
            self.bg_img_grey_src = ""  # grey_image_src[0]
        self.bg_img = classes.board.ImgSurf(self.board, 3, 3, white, self.bg_img_src)

        self.finished = False
        self.choice_list = [x for x in range(1, data[2] + 1)]
        self.shuffled = self.choice_list[:]
        random.shuffle(self.shuffled)

        inversions = ex.inversions(self.shuffled)
        if inversions % 2 != 0:  # if number of inversions is odd it is unsolvable
            # in unsolvable combinations swapping 2 squares will make it solvable
            temp = self.shuffled[0]
            self.shuffled[0] = self.shuffled[1]
            self.shuffled[1] = temp

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4] - 1  # height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3]) // 2  # side margin width
        self.check = [h1, h2, w2]
        self.board.add_door(w2, h1, data[3], data[4], classes.board.Door, "", white, self.bg_img_grey_src)

        self.board.units[0].image.set_colorkey((1, 2, 3))
        # create table to store 'binary' solution
        # find position of first door square
        x = w2
        y = h1
        self.mini_grid = []
        # add objects to the board
        line = []
        h_start = random.randrange(0, 155, 5)
        h_step = 100 // (data[2])

        for i in range(data[2]):
            h = (h_start + (self.shuffled[i] - 1) * h_step)
            caption = str(self.shuffled[i])
            self.board.add_unit(x, y, 1, 1, classes.board.ImgShip, caption, white, self.bg_img_src)
            self.board.ships[-1].img = self.bg_img.img.copy()
            self.board.ships[-1].readable = False
            offset_x = 0
            offset_y = 0
            if self.shuffled[i] in [2, 5, 8]:
                offset_x = self.board.scale - 0
            elif self.shuffled[i] in [3, 6]:
                offset_x = (self.board.scale - 0) * 2

            if self.shuffled[i] in [4, 5, 6]:
                offset_y = self.board.scale - 0
            elif self.shuffled[i] in [7, 8]:
                offset_y = (self.board.scale - 0) * 2

            self.board.ships[-1].img_pos = (-offset_x, -offset_y)

            line.append(i)
            x += 1
            if x >= w2 + data[3] or i == data[2] - 1:
                x = w2
                y += 1
                self.mini_grid.append(line)
                line = []

        # mini img below game
        self.board.add_unit(w2 + data[3] - 2, data[1] - 1, 1, 1, classes.board.ImgShip, "", white, self.bg_img_src)
        self.preview = self.board.ships[-1]
        self.preview.immobilize()
        self.preview.outline = False
        # draw 4 lines on the mini preview
        step = self.board.scale // 3
        pygame.draw.line(self.preview.img, outline_color, [step, 0], [step, step * 3], 1)
        pygame.draw.line(self.preview.img, outline_color, [step * 2, 0], [step * 2, step * 3], 1)
        pygame.draw.line(self.preview.img, outline_color, [0, step], [step * 3, step], 1)
        pygame.draw.line(self.preview.img, outline_color, [0, step * 2], [step * 3, step * 2], 1)

        self.preview.update_me = True
        self.outline_all(outline_color, 1)

        # horizontal
        self.board.add_unit(0, 0, data[0], 1, classes.board.Obstacle, "", white, "", 7)  # top
        self.board.add_unit(0, h1 + data[4], data[0], 1, classes.board.Obstacle, "", white, "", 7)  # bottom 1
        # side obstacles
        self.board.add_unit(0, h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # left
        self.board.add_unit(w2 + data[3], h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # right

        # self.board.all_sprites_list.move_to_front(self.board.units[0])
        self.board.all_sprites_list.move_to_back(self.board.units[0])
        self.board.all_sprites_list.move_to_back(self.board.board_bg)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            self.check_result()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        if self.changed_since_check and self.finished == False:
            ships = []
            current = [x for x in range(self.data[2] + 1)]  # self.choice_list[:]
            # collect value and x position on the grid from ships list
            for i in range(len(self.board.ships) - 1):
                x = self.board.ships[i].grid_x - self.check[2]
                y = self.board.ships[i].grid_y - self.check[0]
                w = self.data[3]
                h = self.data[4]
                pos = x + (y * w)
                current[pos] = int(self.board.ships[i].value)
            del (current[-1])
            if self.choice_list == current:
                self.mainloop.db.update_completion(self.mainloop.userid, self.active_game.dbgameid, self.level.lvl)
                self.level.update_level_dictx()
                self.mainloop.redraw_needed[1] = True
                self.finished = True
                self.board.units[0].img = self.bg_img.img.copy()
                self.board.all_sprites_list.move_to_front(self.board.units[0])
                self.board.units[0].update_me = True
                # copied from level controller:
                index = random.randrange(0, len(self.dp["Great job!"]))
                praise = self.dp["Great job!"][index]
                self.say(praise, 6)
                self.board.units[2].value = praise
                self.board.units[2].update_me = True
