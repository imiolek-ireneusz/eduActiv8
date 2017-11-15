# -*- coding: utf-8 -*-

import os
import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.decolorable = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.board.draw_grid = False

        s = random.randrange(150, 190, 5)
        v = random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)
        white = (255, 255, 255)
        if self.mainloop.scheme is None:
            color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        else:
            color0 = self.mainloop.scheme.u_color
            if self.mainloop.scheme.dark:
                white = (0, 0, 0)
        outline_color = (150, 150, 150)
        # setting level variable
        # data = [x_count, y_count, number_count, top_limit, ordered]
        if self.level.lvl == 1:
            data = [13, 7, 5, 3, 2]
        elif self.level.lvl == 2:
            data = [13, 7, 8, 3, 3]
        elif self.level.lvl == 3:
            data = [12, 7, 7, 4, 2]
        elif self.level.lvl == 4:
            data = [12, 7, 11, 4, 3]
        elif self.level.lvl == 5:
            data = [12, 7, 15, 4, 4]
        elif self.level.lvl == 6:
            data = [13, 7, 9, 5, 2]
        elif self.level.lvl == 7:
            data = [13, 7, 14, 5, 3]
        elif self.level.lvl == 8:
            data = [13, 7, 19, 5, 4]
        elif self.level.lvl == 9:
            data = [12, 7, 11, 6, 2]
        elif self.level.lvl == 10:
            data = [12, 7, 17, 6, 3]

        self.chapters = [1, 5, 10]

        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            x_count = self.get_x_count(data[1], even=True)
        else:
            x_count = self.get_x_count(data[1], even=False)

        if x_count > data[0]:
            data[0] = x_count

        self.data = data
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        image_src = [os.path.join('memory', "n_img%da.png" % (i)) for i in range(1, 22)]
        self.choice_list = [x for x in range(1, data[2] + 1)]
        self.shuffled = self.choice_list[:]
        random.shuffle(self.shuffled)

        inversions = ex.inversions(self.shuffled)
        if inversions % 2 != 0:  # if number of inversions is odd it is unsolvable
            # in unsolvable combinations swapping 2 squares will make it solvable
            temp = self.shuffled[0]
            self.shuffled[0] = self.shuffled[1]
            self.shuffled[1] = temp

        color = ((255, 255, 255))

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4] - 1  # height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3]) // 2  # side margin width
        self.check = [h1, h2, w2]

        self.board.add_door(w2, h1, data[3], data[4], classes.board.Door, "", color, "")
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
            number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            caption = str(self.shuffled[i])
            self.board.add_unit(x, y, 1, 1, classes.board.ImgShip, caption, white, image_src[self.shuffled[i]])
            self.board.ships[-1].readable = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            line.append(i)
            x += 1
            if x >= w2 + data[3] or i == data[2] - 1:
                x = w2
                y += 1
                self.mini_grid.append(line)
                line = []
        self.outline_all(outline_color, 1)
        instruction = self.d["Re-arrange right"]
        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, color0, "", 8)  # bottom 2
        self.board.ships[-1].immobilize()
        if self.mainloop.scheme is not None:
            self.board.ships[-1].font_color = self.mainloop.scheme.u_font_color
        self.board.ships[-1].speaker_val = self.dp["Re-arrange right"]
        self.board.ships[-1].speaker_val_update = False

        # horizontal
        self.board.add_unit(0, 0, data[0], h1, classes.board.Obstacle, "", white, "", 7)  # top
        self.board.add_unit(0, h1 + data[4], data[0], h2, classes.board.Obstacle, "", white, "", 7)  # bottom 1
        # side obstacles
        self.board.add_unit(0, h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # left
        self.board.add_unit(w2 + data[3], h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # right

        self.board.all_sprites_list.move_to_front(self.board.units[0])

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        current = [x for x in range(self.data[2] + 1)]  # self.choice_list[:]
        # collect value and x position on the grid from ships list
        for i in range(len(self.board.ships) - 1):
            x = self.board.ships[i].grid_x - self.check[2]
            y = self.board.ships[i].grid_y - self.check[0]
            w = self.data[3]
            pos = x + (y * w)
            current[pos] = int(self.board.ships[i].value)
            if pos < self.data[2]:
                if self.choice_list[pos] == current[pos]:
                    self.board.ships[i].set_display_check(True)
                else:
                    self.board.ships[i].set_display_check(False)
            else:
                self.board.ships[i].set_display_check(False)

        del (current[-1])
        if self.choice_list == current:
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True
