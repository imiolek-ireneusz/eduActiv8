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
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        if self.mainloop.m.game_variant > 3:
            h = 116
        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
        self.font_color = self.color2

        white = (255, 255, 255)

        self.disp_counter = 0
        self.disp_len = 1

        texts1 = []
        texts2 = []
        data = [4, 2]
        data.extend(self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                     self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        if self.mainloop.m.game_variant < 4:
            data[0] = data[9]
            data[1] = data[10]
        else:
            data[0] = data[2]
            data[1] = data[3]
        self.square_count = data[0] * data[1]

        if self.mainloop.m.game_variant == 0:
            while len(texts1) < self.square_count // 2:
                first_num = random.randrange(data[2], data[3] + 1)
                second_num = random.randrange(data[4], data[5] + 1)
                my_sum = str(first_num + second_num)
                if my_sum not in texts1:
                    texts1.append(str(my_sum))
                    if second_num < 0:
                        n2 = "(%d)" % second_num
                    else:
                        n2 = str(second_num)
                    texts2.append("%d + %s" % (first_num, n2))

        elif self.mainloop.m.game_variant == 1:
            while len(texts1) < self.square_count // 2:
                first_num = random.randrange(data[2], data[3] + 1)
                if first_num - 1 <= data[4] and self.mainloop.m.game_var2 == 0:
                    continue
                else:
                    if self.mainloop.m.game_var2 == 0:
                        second_num = random.randint(data[4], first_num - 1)
                    else:
                        second_num = random.randint(data[4], data[5])
                    my_sum = str(first_num - second_num)
                    if my_sum not in texts1:
                        texts1.append(str(my_sum))
                        if second_num < 0:
                            n2 = "(%d)" % second_num
                        else:
                            n2 = str(second_num)
                        texts2.append("%d - %s" % (first_num, n2))

        elif self.mainloop.m.game_variant == 2:
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)

            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(texts1) < self.square_count // 2:
                if data[3] == 0:
                    first_num = int(l1[random.randint(0, l1l-1)])
                else:
                    first_num = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l-1)])
                else:
                    second_num = random.randint(data[4], data[5])
                my_sum = str(first_num * second_num)
                if my_sum not in texts1:
                    texts1.append(str(my_sum))
                    texts2.append("%d %s %d" % (first_num, chr(215), second_num))

        elif self.mainloop.m.game_variant == 3:
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)

            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(texts1) < self.square_count // 2:
                if data[3] == 0:
                    first = int(l1[random.randint(0, l1l - 1)])
                else:
                    first = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l - 1)])
                else:
                    second_num = random.randint(data[4], data[5])
                first_num = first * second_num
                my_sum = str(first)
                if my_sum not in texts1:
                    texts1.append(my_sum)
                    texts2.append("%d %s %d" % (first_num, chr(247), second_num))

        elif self.mainloop.m.game_variant == 4:
            #data = [4, 2]
            if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
                image_src1 = [os.path.join('memory', "m_img%da.png" % i) for i in range(1, 22)]
            else:
                image_src1 = [os.path.join('schemes', "black", "match_animals", "m_img%da.png" % i) for i in range(1, 22)]
            image_src2 = image_src1

        elif self.mainloop.m.game_variant == 5:
            #data = [4, 2]
            if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
                image_src1 = [os.path.join('memory', "m_img%da.png" % i) for i in range(1, 22)]
                image_src2 = [os.path.join('memory', "m_img%db.png" % i) for i in range(1, 22)]
            else:
                image_src1 = [os.path.join('schemes', "black", "match_animals", "m_img%da.png" % i) for i in range(1, 22)]
                image_src2 = [os.path.join('schemes', "black", "match_animals", "m_img%db.png" % i) for i in range(1, 22)]

        self.data = data
        self.found = 0
        self.clicks = 0
        self.history = [None, None]
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        self.completed_mode = False

        if self.mainloop.m.game_variant in [4, 5]:
            choice = [x for x in range(0, 21)]
        else:
            choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        h1 = (data[1] - data[1]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[1]  # -1 #height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[0]) // 2  # side margin width

        slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2, w2 + data[0]):
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
                self.board.add_unit(slots[i][0], slots[i][1], 1, 1, classes.board.Letter, caption, color0, "", data[8])
                self.board.ships[-1].font_color = self.font_color

            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(self.color2, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[1] is None and self.ai_enabled is False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if not active.uncovered:
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
                        else:
                            self.history[0].uncovered = True
                            self.history[1].uncovered = True
                            self.history[0].perm_outline_color = self.color2  # [50,255,50]
                            self.history[1].perm_outline_color = self.color2
                            self.history[0].image.set_alpha(50)
                            self.history[1].image.set_alpha(50)
                            self.history[0].update_me = True
                            self.history[1].update_me = True
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
