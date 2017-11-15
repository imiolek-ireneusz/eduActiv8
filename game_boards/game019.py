# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 7)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = 100
        v = 255
        h = random.randrange(0, 255)
        color1 = ex.hsv_to_rgb(h, s, v)
        color2 = ex.hsv_to_rgb(h, 150, v)
        color3 = ex.hsv_to_rgb(h, 150, 75)

        # data = [0-x_count, 1-y_count, 2-bottom_range1, 3-top_range1, 4-bottom_range2, 5-top_range2, 6-operator, 7-font_size]
        data = [11, 7]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        if self.mainloop.m.game_variant == 2:
            data[6] = "*"
        elif self.mainloop.m.game_variant == 3:
            data[6] = "/"

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

        if data[6] == "+":
            while len(self.solution) < 5:
                first_num = random.randint(data[2], data[3])
                second_num = random.randint(data[4], data[5])
                sm = first_num + second_num
                if sm not in self.solution:
                    self.num_list.append(first_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)
        elif data[6] == "-":
            while len(self.solution) < 5:
                first_num = random.randint(data[2], data[3])
                if self.mainloop.m.game_var2 == 0:
                    second_num = random.randint(data[4], first_num - 1)
                else:
                    second_num = random.randint(data[4], data[5])
                sm = first_num - second_num
                if sm not in self.solution:
                    self.num_list.append(first_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)
        elif data[6] == "*":
            # if list:
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)

            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(self.solution) < 5:
                if data[3] == 0:
                    first_num = int(l1[random.randint(0, l1l-1)])
                else:
                    first_num = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l-1)])
                else:
                    second_num = random.randint(data[4], data[5])
                sm = first_num * second_num
                if sm not in self.solution:
                    self.num_list.append(first_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)

        elif data[6] == "/":
            # if list:
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)
            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(self.solution) < 5:
                if data[3] == 0:
                    first = int(l1[random.randint(0, l1l - 1)])
                else:
                    first = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l - 1)])
                else:
                    second_num = random.randint(data[4], data[5])
                sm = first
                if first * second_num not in self.num_list:
                    self.num_list.append(first * second_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)

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
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()
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
            self.auto_check()

    def auto_check_reset(self):
        for each in self.board.ships:
            each.set_display_check(None)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check(self):
        count = 0
        for i in range(5):
            if self.board.ships[i].grid_x == self.board.units[-3].grid_x and 0 < self.board.ships[i].grid_y < 6:
                count += 1
        if count == 5:
            self.check_result()
        else:
            self.auto_check_reset()

    def check_result(self):
        correct = True
        for i in range(5):
            if self.board.ships[i].grid_x == self.board.units[-3].grid_x and 0 < self.board.ships[i].grid_y < 6:
                # if position from the left is in line with target squares
                if self.board.ships[i].value != str(self.num_list2[self.board.ships[i].grid_y - 1]):
                    correct = False
                    self.board.ships[i].set_display_check(False)
                else:
                    self.board.ships[i].set_display_check(True)
            else:
                correct = False
                self.board.ships[i].set_display_check(None)
        if correct:
            tts = self.d["Perfect! Task solved!"]
            self.level.next_board(tts)

        self.mainloop.redraw_needed[0] = True
