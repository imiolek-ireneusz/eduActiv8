# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 7, 11)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 7)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = 100
        v = 255
        h = random.randrange(0, 255)
        color1 = ex.hsv_to_rgb(h, s, v)
        color2 = ex.hsv_to_rgb(h, 150, v)
        color3 = ex.hsv_to_rgb(h, 150, 75)

        # data = [0-x_count, 1-y_count, 2-bottom_range1, 3-top_range1, 4-bottom_range2, 5-top_range2, 6-operator, 7-font_size]
        if self.mainloop.m.game_variant == 0:
            self.points = self.level.lvl
            self.level.lvl_count = 11
            if self.level.lvl == 1:  # addition - ch0
                data = [11, 7, 1, 5, 1, 5, "+", 2]
            elif self.level.lvl == 2:
                data = [11, 7, 3, 9, 1, 5, "+", 2]
            elif self.level.lvl == 3:
                data = [11, 7, 5, 15, 3, 9, "+", 2]
            elif self.level.lvl == 4:
                data = [11, 7, 5, 15, 5, 15, "+", 2]
            elif self.level.lvl == 5:
                data = [11, 7, 15, 55, 5, 35, "+", 2]
            elif self.level.lvl == 6:
                data = [11, 7, 35, 75, 15, 25, "+", 2]
            elif self.level.lvl == 7:
                data = [11, 7, 55, 99, 55, 99, "+", 2]
            elif self.level.lvl == 8:
                data = [11, 7, 100, 250, 100, 250, "+", 4]
            elif self.level.lvl == 9:
                data = [11, 7, 300, 500, 250, 499, "+", 4]
            elif self.level.lvl == 10:
                data = [11, 7, 400, 650, 150, 349, "+", 4]
            elif self.level.lvl == 11:
                data = [11, 7, 500, 850, 100, 149, "+", 4]
        elif self.mainloop.m.game_variant == 1:
            self.points = self.level.lvl
            self.level.lvl_count = 11
            if self.level.lvl == 1:  # subtraction  - ch1
                data = [11, 7, 3, 10, 1, 0, "-", 2]
            elif self.level.lvl == 2:
                data = [11, 7, 5, 10, 3, 0, "-", 2]
            elif self.level.lvl == 3:
                data = [11, 7, 10, 15, 3, 0, "-", 2]
            elif self.level.lvl == 4:
                data = [11, 7, 15, 20, 5, 0, "-", 2]
            elif self.level.lvl == 5:
                data = [11, 7, 20, 49, 9, 0, "-", 2]
            elif self.level.lvl == 6:
                data = [11, 7, 49, 99, 9, 0, "-", 2]
            elif self.level.lvl == 7:
                data = [11, 7, 100, 250, 30, 0, "-", 4]
            elif self.level.lvl == 8:
                data = [11, 7, 100, 250, 30, 0, "-", 4]
            elif self.level.lvl == 9:
                data = [11, 7, 100, 250, 30, 0, "-", 4]
            elif self.level.lvl == 10:
                data = [11, 7, 250, 499, 50, 0, "-", 4]
            elif self.level.lvl == 11:
                data = [11, 7, 499, 999, 99, 0, "-", 4]

        elif self.mainloop.m.game_variant == 2:
            self.points = self.level.lvl * 2
            self.level.lvl_count = 7
            if self.level.lvl > 7:
                self.level.lvl = 7
            if self.level.lvl == 1:  # multiplication  - ch2
                data = [11, 7, 1, 3, 1, 3, "*", 2]
            elif self.level.lvl == 2:
                data = [11, 7, 1, 9, 1, 3, "*", 2]
            elif self.level.lvl == 3:
                data = [11, 7, 2, 6, 2, 6, "*", 2]
            elif self.level.lvl == 4:
                data = [11, 7, 2, 7, 3, 7, "*", 2]
            elif self.level.lvl == 5:
                data = [11, 7, 2, 9, 2, 9, "*", 2]
            elif self.level.lvl == 6:
                data = [11, 7, 2, 15, 2, 15, "*", 4]
            elif self.level.lvl == 7:
                data = [11, 7, 2, 20, 2, 20, "*", 4]

        elif self.mainloop.m.game_variant == 3:
            self.points = self.level.lvl * 2
            self.level.lvl_count = 7
            if self.level.lvl > 7:
                self.level.lvl = 7
            if self.level.lvl == 1:  # division - ch3
                data = [11, 7, 1, 3, 1, 3, "/", 2]
            elif self.level.lvl == 2:
                data = [11, 7, 1, 9, 1, 3, "/", 2]
            elif self.level.lvl == 3:
                data = [11, 7, 2, 6, 2, 6, "/", 2]
            elif self.level.lvl == 4:
                data = [11, 7, 2, 7, 3, 7, "/", 2]
            elif self.level.lvl == 5:
                data = [11, 7, 2, 9, 2, 9, "/", 2]
            elif self.level.lvl == 6:
                data = [11, 7, 2, 15, 2, 15, "/", 4]
            elif self.level.lvl == 7:
                data = [11, 7, 2, 20, 2, 20, "/", 4]

        # stretch width to fit the screen size
        data[0] = self.get_x_count(data[1], even=False)
        if data[0] < 9:
            data[0] = 9
        self.data = data

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.num_list = []
        self.num_list2 = []
        self.solution = []

        num1 = [x for x in range(data[2], data[3] + 1)]
        num2 = [x for x in range(data[4], data[5] + 1)]

        if len(num1) < 5:
            num1 *= 2
        if len(num2) < 5:
            num2 *= 2
        random.shuffle(num1)
        random.shuffle(num2)

        for i in range(5):
            if data[6] == "+":
                first_num = num1[i]
                second_num = num2[i]
                self.solution.append(first_num + second_num)

            elif data[6] == "-":
                first_num = num1[i]
                second_num = random.randrange(data[4], first_num - 1)
                self.solution.append(first_num - second_num)

            elif data[6] == "*":
                first_num = num1[i]
                second_num = num2[i]
                self.solution.append(first_num * second_num)

            elif data[6] == "/":  # reversed multiplication - looking for the first factor
                first = num1[i]
                second_num = num2[i]
                first_num = first * second_num
                self.solution.append(first)

            self.num_list.append(first_num)
            self.num_list2.append(second_num)

        self.shuffled = self.num_list2[:]  # self.solution[:]
        random.shuffle(self.shuffled)

        # create objects
        if data[6] == "*":
            operator = chr(215)
        elif data[6] == "/":
            operator = chr(247)
        else:
            operator = data[6]

        x = (data[0] - 5) // 2
        y = 1
        for i in range(5):
            self.board.add_unit(x, y, 1, 1, classes.board.Label, str(self.num_list[i]), color1, "", data[7])
            self.board.add_unit(x + 1, y, 1, 1, classes.board.Label, operator, color1, "", data[7])
            self.board.add_door(x + 2, y, 1, 1, classes.board.Door, "", color1, "")
            self.board.units[-1].door_outline = True
            self.board.add_unit(x + 3, y, 1, 1, classes.board.Label, "=", color1, "", data[7])
            self.board.add_unit(x + 4, y, 1, 1, classes.board.Label, str(self.solution[i]), color1, "", data[7])

            self.board.add_unit(x + 6, y, 1, 1, classes.board.Letter, str(self.shuffled[i]), color2, "", data[7])
            self.board.ships[-1].audible = False
            self.board.ships[-1].readable = False
            y += 1
        self.outline_all(1, 1)
        for i in range(2, 25, 5):
            self.board.all_sprites_list.move_to_front(self.board.units[i])
        for each in self.board.units:
            each.font_color = color3
        for each in self.board.ships:
            each.font_color = color3

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        correct = True
        for i in range(5):
            if self.board.ships[i].grid_x == self.board.units[-3].grid_x and 0 < self.board.ships[i].grid_y < 6:
                # if position from the left is in line with target squares
                if self.board.ships[i].value != str(self.num_list2[self.board.ships[i].grid_y - 1]):
                    correct = False
                    break
            else:
                correct = False
                break
        if correct:
            tts = self.d["Perfect! Task solved!"]
            # self.update_score(self.points)
            self.level.next_board(tts)
        else:
            if self.points > 0:
                self.points -= 1
            self.level.try_again()
