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
        self.level = lc.Level(self, mainloop, 7, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.vis_buttons = [0, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        s = random.randrange(100, 150, 5)
        v = random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)
        bg_col = (255, 255, 255)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                bg_col = (0, 0, 0)
        if self.mainloop.m.game_variant > 3:
            h = 116
        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
        self.font_color = self.color2

        white = (255, 255, 255)

        self.disp_counter = 0
        self.disp_len = 1
        lvl = 0

        if self.mainloop.m.game_variant in [4, 5]:
            lvl = -2
            self.level.lvl_count = 8
        elif self.mainloop.m.game_variant in [0, 2]:
            self.level.lvl_count = 7
        elif self.mainloop.m.game_variant in [1, 3]:
            self.level.lvl_count = 6

        if self.level.lvl > self.level.lvl_count:
            self.level.lvl = self.level.lvl_count

        if self.mainloop.m.game_variant < 4:
            if self.level.lvl == lvl + 1:
                data = [4, 2, 3, 4, 2]
            elif self.level.lvl == lvl + 2:
                data = [5, 2, 3, 5, 2]
            """
            if self.mainloop.m.game_variant == 3:
                if self.uage == 3 and self.level.lvl < 3:
                    self.level.lvl = self.min_level = 3
            """

        if self.level.lvl == lvl + 3:
            data = [4, 3, 3, 4, 3]
        elif self.level.lvl == lvl + 4:
            data = [6, 3, 3, 6, 3]
        elif self.level.lvl == lvl + 5:
            data = [5, 4, 3, 5, 4]
        elif self.level.lvl == lvl + 6:
            data = [6, 4, 3, 6, 4]
        elif self.level.lvl == lvl + 7:
            data = [7, 4, 3, 7, 4]
        elif self.level.lvl == lvl + 8:
            data = [6, 5, 3, 6, 5]
        elif self.level.lvl == lvl + 9:
            data = [6, 6, 3, 6, 6]
        elif self.level.lvl == lvl + 10:
            data = [7, 6, 3, 7, 6]
        if self.mainloop.m.game_variant == 3:
            if self.level.lvl == 4:
                data = [4, 3, 3, 4, 3]
            elif self.level.lvl == 5:
                data = [5, 3, 3, 5, 3]
            elif self.level.lvl == 6:
                data = [5, 3, 3, 5, 3]
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
        self.points = self.square_count // 2

        self.history = [None, None]

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        texts1 = []
        texts2 = []
        if self.mainloop.m.game_variant == 4:
            if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
                image_src1 = [os.path.join('memory', "m_img%da.png" % (i)) for i in range(1, 22)]
            else:
                image_src1 = [os.path.join('schemes', "black", "match_animals", "m_img%da.png" % (i)) for i in
                              range(1, 22)]
            image_src2 = image_src1

        elif self.mainloop.m.game_variant == 5:
            if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
                image_src1 = [os.path.join('memory', "m_img%da.png" % (i)) for i in range(1, 22)]
                image_src2 = [os.path.join('memory', "m_img%db.png" % (i)) for i in range(1, 22)]
            else:
                image_src1 = [os.path.join('schemes', "black", "match_animals", "m_img%da.png" % (i)) for i in
                              range(1, 22)]
                image_src2 = [os.path.join('schemes', "black", "match_animals", "m_img%db.png" % (i)) for i in
                              range(1, 22)]

        elif self.mainloop.m.game_variant == 0:
            if self.level.lvl == 1:  # addition
                draw_data = [1, 5, 1, 5, 6]
            elif self.level.lvl == 2:
                draw_data = [3, 9, 1, 5, 6]
            elif self.level.lvl == 3:
                draw_data = [5, 15, 3, 9, 7]
            elif self.level.lvl == 4:
                draw_data = [5, 15, 5, 15, 8]
            elif self.level.lvl == 5:
                draw_data = [15, 55, 5, 35, 9]
            elif self.level.lvl == 6:
                draw_data = [35, 75, 15, 25, 9]
            elif self.level.lvl == 7:
                draw_data = [55, 99, 55, 99, 9]
            while len(texts1) < self.square_count // 2:
                first_num = random.randrange(draw_data[0], draw_data[1] + 1)
                second_num = random.randrange(draw_data[2], draw_data[3] + 1)
                my_sum = str(first_num + second_num)
                if my_sum not in texts1:
                    texts1.append(str(my_sum))
                    texts2.append("%d + %d" % (first_num, second_num))

        elif self.mainloop.m.game_variant == 1:
            if self.level.lvl == 1:  # subtraction  - ch1
                draw_data = [3, 10, 1, 0, 6]
            elif self.level.lvl == 2:
                draw_data = [5, 10, 3, 0, 6]
            elif self.level.lvl == 3:
                draw_data = [10, 15, 3, 0, 7]
            elif self.level.lvl == 4:
                draw_data = [15, 20, 5, 0, 7]
            elif self.level.lvl == 5:
                draw_data = [20, 49, 9, 0, 8]
            elif self.level.lvl == 6:
                draw_data = [49, 99, 9, 0, 9]
            while len(texts1) < self.square_count // 2:
                first_num = random.randrange(draw_data[0], draw_data[1] + 1)
                second_num = random.randrange(draw_data[2], first_num - 1)
                my_sum = str(first_num - second_num)
                if my_sum not in texts1:
                    texts1.append(str(my_sum))
                    texts2.append("%d - %d" % (first_num, second_num))

        elif self.mainloop.m.game_variant == 2:
            if self.level.lvl == 1:  # multiplication  - ch2
                draw_data = [1, 3, 1, 3, 6]
            elif self.level.lvl == 2:
                draw_data = [1, 9, 1, 2, 6]
            elif self.level.lvl == 3:
                draw_data = [2, 6, 2, 6, 6]
            elif self.level.lvl == 4:
                draw_data = [2, 7, 3, 7, 6]
            elif self.level.lvl == 5:
                draw_data = [2, 9, 2, 9, 6]
            elif self.level.lvl == 6:
                draw_data = [2, 15, 2, 15, 8]
            elif self.level.lvl == 7:
                draw_data = [2, 20, 2, 20, 8]
            while len(texts1) < self.square_count // 2:
                first_num = random.randrange(draw_data[0], draw_data[1] + 1)
                second_num = random.randrange(draw_data[2], draw_data[3] + 1)
                my_sum = str(first_num * second_num)
                if my_sum not in texts1:
                    texts1.append(str(my_sum))
                    texts2.append("%d %s %d" % (first_num, chr(215), second_num))
        elif self.mainloop.m.game_variant == 3:
            if self.level.lvl == 1:  # division - ch3
                draw_data = [1, 4, 1, 4, 6]
            elif self.level.lvl == 2:
                draw_data = [1, 9, 1, 4, 6]
            elif self.level.lvl == 3:
                draw_data = [1, 6, 1, 6, 6]
            elif self.level.lvl == 4:
                draw_data = [1, 9, 1, 9, 8]
            elif self.level.lvl == 5:
                draw_data = [1, 15, 1, 15, 9]
            elif self.level.lvl == 6:
                draw_data = [2, 20, 2, 20, 9]
            while len(texts1) < self.square_count // 2:
                first = random.randrange(draw_data[0], draw_data[1] + 1)
                second_num = random.randrange(draw_data[2], draw_data[3] + 1)
                first_num = first * second_num

                my_sum = str(first)  # str(first_num * second_num)
                if my_sum not in texts1:
                    texts1.append(my_sum)
                    texts2.append("%d %s %d" % (first_num, chr(247), second_num))
        elif self.mainloop.m.game_variant == 6:
            pass

        self.completed_mode = False
        if self.mainloop.m.game_variant in [4, 5]:
            choice = [x for x in range(0, 21)]
        else:
            choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4]  # -1 #height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3]) // 2  # side margin width

        slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2, w2 + data[3]):
                slots.append([i, j])
        random.shuffle(slots)

        switch = self.square_count // 2
        for i in range(self.square_count):
            if self.mainloop.m.game_variant in [4, 5]:
                if i < switch:
                    src = image_src1[self.chosen[i]]
                else:
                    src = image_src2[self.chosen[i - switch]]
                self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.ImgShip, "", white, src)
            else:
                if i < switch:
                    caption = texts1[self.chosen[i]]
                else:
                    caption = texts2[self.chosen[i - switch]]
                self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Letter, caption, color0, "",
                                    draw_data[4])
                self.board.ships[-1].font_color = self.font_color

            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
        self.outline_all(self.color2, 1)

        #self.board.add_door(0, data[1] - 1, data[0], 1, classes.board.Door, "0/0", bg_col, "", font_size=3)
        #self.counter = self.board.units[-1]
        #self.counter.font_color = (80, 80, 80)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[
            1] == None and self.ai_enabled == False:  # and self.start_sequence==False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if active.uncovered == False:
                    if self.history[0] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[0] = active
                        self.clicks += 1
                        active.uncovered = True
                    elif self.history[1] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[1] = active
                        self.clicks += 1
                        if self.chosen[self.history[0].unit_id] != self.chosen[self.history[1].unit_id]:
                            self.ai_enabled = True
                            self.history[0].uncovered = False
                            if self.points > 0:
                                self.points -= 1
                        else:
                            self.history[0].uncovered = True
                            self.history[1].uncovered = True
                            self.history[0].perm_outline_color = self.color2  # [50,255,50]
                            self.history[1].perm_outline_color = self.color2
                            self.history[0].image.set_alpha(50)
                            self.history[1].image.set_alpha(50)
                            self.history[0].update_me = True
                            self.history[1].update_me = True
                            self.found += 2
                            if self.found == self.square_count:
                                # self.update_score(self.points)
                                self.completed_mode = True
                                self.ai_enabled = True
                            self.history = [None, None]
                    active.update_me = True
                    #self.counter.value = "%i/%i" % (self.found, self.clicks)
                    #self.counter.update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.ai_enabled = False
                self.level.next_board()
            else:
                self.history[0].perm_outline_width = 1
                self.history[0].perm_outline_color = self.color2
                self.history[1].perm_outline_width = 1
                self.history[1].perm_outline_color = self.color2
                self.history[0].update_me = True
                self.history[1].update_me = True
                self.history = [None, None]
                self.ai_enabled = False
                self.disp_counter = 0

    def check_result(self):
        pass
