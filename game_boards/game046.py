# -*- coding: utf-8 -*-

import os
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 3, 5)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 8)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = random.randrange(100, 121, 5)
        v = random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)

        color = ex.hsv_to_rgb(h, s, v)
        outline_color = ex.hsv_to_rgb(h, 255, 140)
        self.font_color = outline_color
        apple_bg = [255, 255, 255, 0]

        # data = [x_count, y_count, range_from, range_to, max_sum_range, image, sign]
        if self.mainloop.m.game_variant == 0:
            if self.level.lvl == 1:
                data = [11, 8, 1, 5, 5, 3, os.path.join("fr", "fr_apple2.png"), "n", 0]
            elif self.level.lvl == 2:
                data = [11, 8, 1, 6, 6, 2, os.path.join("fr", "fr_apple1.png"), "n", 0]
            elif self.level.lvl == 3:
                data = [11, 8, 2, 6, 6, 3, os.path.join("fr", "fr_pear.png"), "n", 0]
            elif self.level.lvl == 4:
                data = [11, 8, 3, 7, 7, 3, os.path.join("fr", "fr_orange.png"), "n", 0]
            elif self.level.lvl == 5:
                data = [11, 8, 3, 8, 8, 2, os.path.join("fr", "fr_plum.png"), "n", 0]
            self.points = self.level.lvl // 2 + 1
        elif self.mainloop.m.game_variant == 1:
            if self.level.lvl == 1:
                data = [11, 8, 1, 6, 6, 2, os.path.join("fr", "fr_cherry.png"), "+", 2]
            elif self.level.lvl == 2:
                data = [11, 8, 1, 7, 7, 2, os.path.join("fr", "fr_wmelon.png"), "+", 2]
            elif self.level.lvl == 3:
                data = [11, 8, 1, 8, 8, 2, os.path.join("fr", "fr_lemon.png"), "+", 2]
            elif self.level.lvl == 4:
                data = [11, 8, 1, 9, 9, 2, os.path.join("fr", "fr_banana.png"), "+", 2]
            elif self.level.lvl == 5:
                data = [11, 8, 1, 10, 10, 2, os.path.join("fr", "fr_strawberry.png"), "+", 2]
            self.points = self.level.lvl
        elif self.mainloop.m.game_variant == 2:
            if self.level.lvl == 1:
                data = [11, 8, 2, 6, 6, 2, os.path.join("fr", "fr_tomato.png"), "-", 2]
            elif self.level.lvl == 2:
                data = [11, 8, 2, 7, 7, 2, os.path.join("fr", "fr_pepper.png"), "-", 2]
            elif self.level.lvl == 3:
                data = [11, 8, 2, 8, 8, 2, os.path.join("fr", "fr_carrot.png"), "-", 2]
            elif self.level.lvl == 4:
                data = [11, 8, 2, 9, 9, 2, os.path.join("fr", "fr_onion.png"), "-", 2]
            elif self.level.lvl == 5:
                data = [11, 8, 2, 10, 10, 2, os.path.join("fr", "fr_broccoli.png"), "-", 2]
            self.points = self.level.lvl
        # rescale the number of squares horizontally to better match the screen width
        x_count = self.get_x_count(data[1], even=None)
        if x_count > 11:
            data[0] = x_count
        self.data = data

        self.board.set_animation_constraints(1, data[0], 0, data[1])

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        choice_list = [x for x in range(data[2], data[3])] * data[5]
        self.num_list = []
        self.num_list2 = []
        self.solution = []

        for i in range(data[1]):
            index = random.randrange(0, len(choice_list))
            self.num_list.append(choice_list[index])
            if data[7] == "n":
                self.solution.append(choice_list[index])
                second_num = 0
            elif data[7] == "+":
                second_range = data[4] - choice_list[index]
                second_num = random.randrange(1, second_range + 1)
                self.solution.append(choice_list[index] + second_num)
            else:
                second_range = choice_list[index] - 1
                second_num = random.randrange(1, second_range + 1)
                self.solution.append(choice_list[index] - second_num)

            self.num_list2.append(second_num)
            del (choice_list[index])

        if data[7] == "n":
            total = sum(self.num_list)  # +sum(self.num_list2)
        elif data[7] == "+":
            total = sum(self.num_list) + sum(self.num_list2)
        else:
            total = sum(self.num_list) - sum(self.num_list2)

        for i in range(data[1]):
            if data[7] == "n":
                rhs = ""
            else:
                rhs = data[7] + str(self.num_list2[i])
            caption = str(self.num_list[i]) + rhs
            self.board.add_unit(0, i, 1, 1, classes.board.Label, caption, color, "", data[8])
            self.board.units[i].set_outline(outline_color, 1)
            self.board.units[i].font_color = self.font_color
        x = data[0] - 1
        y = 0
        for i in range(1, total + 1):
            if y >= data[1]:
                y = 0
                x -= 1
            self.board.add_unit(x, y, 1, 1, classes.board.ImgShip, "", apple_bg, data[6], alpha=True)
            self.board.ships[-1].audible = False
            self.board.ships[-1].outline = False
            y += 1

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        self.result = []
        for each_list in self.board.grid:
            total = 0
            i = 0
            for each_item in each_list:
                if i > 0:
                    total += each_item
                i += 1
            self.result.append(total)

        if self.result == self.solution:
            # self.update_score(self.points)
            self.level.next_board()
        else:
            if self.points > 0:
                self.points -= 1
            self.level.try_again()
