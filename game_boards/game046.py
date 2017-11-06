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
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        #self.level = lc.Level(self, mainloop, 3, 5)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 8)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = random.randrange(100, 121, 5)
        v = random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)

        color = ex.hsv_to_rgb(h, s, v)
        outline_color = ex.hsv_to_rgb(h, 255, 140)
        self.font_color = outline_color
        apple_bg = [255, 255, 255, 0]

        images = ["fr_apple2.png", "fr_apple1.png", "fr_pear.png", "fr_orange.png", "fr_plum.png", "fr_cherry.png", "fr_wmelon.png", "fr_lemon.png", "fr_banana.png", "fr_strawberry.png"]
        rand_image = os.path.join("fr", images[random.randint(0, 9)])

        data = [11, 8]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        # data = [range_from, range_to, max_sum_range, sign]
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
            if data[6] == "n":
                self.solution.append(choice_list[index])
                second_num = 0
            elif data[6] == "+":
                second_range = data[4] - choice_list[index]
                second_num = random.randrange(1, second_range + 1)
                self.solution.append(choice_list[index] + second_num)
            else:
                second_range = choice_list[index] - 1
                second_num = random.randrange(1, second_range + 1)
                self.solution.append(choice_list[index] - second_num)

            self.num_list2.append(second_num)
            del (choice_list[index])

        if data[6] == "n":
            total = sum(self.num_list)  # +sum(self.num_list2)
        elif data[6] == "+":
            total = sum(self.num_list) + sum(self.num_list2)
        else:
            total = sum(self.num_list) - sum(self.num_list2)

        for i in range(data[1]):
            if data[6] == "n":
                rhs = ""
            else:
                rhs = data[6] + str(self.num_list2[i])
            caption = str(self.num_list[i]) + rhs
            self.board.add_unit(0, i, 1, 1, classes.board.Label, caption, color, "", data[7])
            self.board.units[i].set_outline(outline_color, 1)
            self.board.units[i].font_color = self.font_color
            self.board.units[-1].checkable = True
            self.board.units[-1].init_check_images()
        x = data[0] - 1
        y = 0
        for i in range(1, total + 1):
            if y >= data[1]:
                y = 0
                x -= 1
            self.board.add_unit(x, y, 1, 1, classes.board.ImgShip, "", apple_bg, rand_image, alpha=True)
            self.board.ships[-1].audible = False
            self.board.ships[-1].outline = False
            y += 1

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            pass
            #self.check_result(auto=True)
            #self.auto_check_reset()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check_reset(self):
        for each in self.board.units:
            each.set_display_check(None)

    def check_result(self, auto=False):
        self.result = []
        j = 0
        for each_list in self.board.grid:
            total = 0
            i = 0
            for each_item in each_list:
                if i > 0:
                    total += each_item
                i += 1
            self.result.append(total)
            if self.result[j] == self.solution[j]:
                self.board.units[j].set_display_check(True)
            else:
                self.board.units[j].set_display_check(False)

            j += 1

        if self.result == self.solution:
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True
        #else:
            #self.level.try_again()
        #    self.auto_check_reset()
