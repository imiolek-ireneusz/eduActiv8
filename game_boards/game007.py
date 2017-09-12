# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 99, 27)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.board.decolorable = False
        self.vis_buttons = [0, 1, 1, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = True
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 30, 230)  # highlight 1
        self.color = color0
        self.highlight_color = ex.hsv_to_rgb(h, 230, 150)
        font_color = ex.hsv_to_rgb(h, 70, 230)
        white = (255, 255, 255)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                white = (0, 0, 0)
        self.level.game_step = 0
        self.start_sequence = True
        self.completed_mode = False
        self.game_over_mode = False
        self.disp_counter = 0
        self.disp_len = 3
        self.found = set()
        # setting level variable
        # data = [x_count, y_count, number_count, top_limit, ordered]
        if self.level.lvl == 1:
            data = [13, 9, 0, 3, 3, 1]
        elif self.level.lvl == 2:
            data = [13, 9, 0, 3, 3, 2]
        elif self.level.lvl == 3:
            data = [13, 9, 0, 3, 3, 3]
        elif self.level.lvl == 4:
            data = [13, 9, 0, 3, 4, 4]
        elif self.level.lvl == 5:
            data = [13, 9, 0, 3, 4, 5]
        elif self.level.lvl == 6:
            data = [13, 9, 0, 3, 4, 6]
        elif self.level.lvl == 7:
            data = [12, 9, 0, 4, 4, 7]
        elif self.level.lvl == 8:
            data = [12, 9, 0, 4, 4, 8]
        elif self.level.lvl == 9:
            data = [12, 9, 0, 4, 4, 9]
        elif self.level.lvl == 10:
            data = [12, 9, 0, 4, 5, 10]
        elif self.level.lvl == 11:
            data = [12, 9, 0, 4, 5, 11]
        elif self.level.lvl == 12:
            data = [12, 9, 0, 4, 5, 12]
        elif self.level.lvl == 13:
            data = [13, 9, 0, 5, 5, 13]
        elif self.level.lvl == 14:
            data = [13, 9, 0, 5, 5, 14]
        elif self.level.lvl == 15:
            data = [13, 9, 0, 5, 5, 15]
        elif self.level.lvl == 16:
            data = [13, 9, 0, 5, 6, 16]
        elif self.level.lvl == 17:
            data = [13, 9, 0, 5, 6, 17]
        elif self.level.lvl == 18:
            data = [13, 9, 0, 5, 6, 18]
        elif self.level.lvl == 19:
            data = [12, 9, 0, 6, 6, 19]
        elif self.level.lvl == 20:
            data = [12, 9, 0, 6, 6, 20]
        elif self.level.lvl == 21:
            data = [12, 9, 0, 6, 6, 21]
        elif self.level.lvl == 22:
            data = [12, 9, 0, 6, 7, 22]
        elif self.level.lvl == 23:
            data = [12, 9, 0, 6, 7, 23]
        elif self.level.lvl == 24:
            data = [12, 9, 0, 6, 7, 24]
        elif self.level.lvl == 25:
            data = [13, 9, 0, 7, 7, 25]
        elif self.level.lvl == 26:
            data = [13, 9, 0, 7, 7, 26]
        elif self.level.lvl == 27:
            data = [13, 9, 0, 7, 7, 27]

        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            data[0] = self.get_x_count(data[1], even=True)
        else:
            data[0] = self.get_x_count(data[1], even=False)

        self.data = data

        self.square_count = self.data[3] * self.data[4]

        if self.square_count % 2 == 0:
            a = 0
        else:
            a = 1

        self.max_games = self.square_count // 2 + a
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.current_count = data[5]
        self.level.games_per_lvl = self.current_count

        self.choice_list = [x for x in range(1, data[2] + 1)]
        self.shuffled = self.choice_list[:]
        random.shuffle(self.shuffled)

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4]  # -1 #height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3]) // 2  # side margin width

        self.board.add_door(w2, h1, data[3], data[4], classes.board.Door, "", white, "")

        x = w2
        y = h1

        for i in range(self.square_count):
            caption = str(i + 1)
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, caption, color0, "", 3)
            self.board.ships[i].highlight = False
            self.board.ships[i].readable = False
            self.board.ships[i].font_color = font_color
            if x >= w2 + data[3] - 1:
                x = w2
                y += 1
            else:
                x += 1
        self.outline_all(0, 1)

        # horizontal
        if data[4] < 8:
            self.board.add_unit(0, 0, data[0], h1, classes.board.Obstacle, "", white, "", 7)  # top

        if data[4] < 9:
            self.board.add_unit(0, h1 + data[4], data[0], h2, classes.board.Obstacle, "", white, "", 7)  # bottom 1
        # side obstacles
        if data[3] < 12:
            self.board.add_unit(0, h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # left
            self.board.add_unit(w2 + data[3], h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # right

        self.board.all_sprites_list.move_to_front(self.board.units[0])

        self.draw_nums()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.show_msg == False and self.start_sequence == False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if active.unit_id in self.chosen:
                    active.initcolor = self.highlight_color
                    active.color = self.highlight_color
                    len1 = len(self.found)
                    self.found.add(active.unit_id)
                    len2 = len(self.found)
                    if len2 > len1:
                        self.level.game_step += 1
                        self.mainloop.redraw_needed[1] = True

                    if len(self.found) == self.current_count:
                        self.completed_mode = True
                        self.ai_enabled = True
                else:
                    active.initcolor = (255, 0, 0)
                    active.color = (255, 0, 0)
                    self.game_over_mode = True
                    self.ai_enabled = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def draw_nums(self):
        choice = [x for x in range(self.square_count)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.current_count]

    def next_level(self):
        self.level.levelup(record=False)

    def game_over(self):
        self.level.game_restart()

    def highlight_colors(self):
        for each in self.board.ships:
            if each.unit_id in self.chosen:
                each.initcolor = self.highlight_color
                each.color = self.highlight_color
                each.update_me = True
        self.mainloop.redraw_needed[0] = True
        self.mainloop.redraw_needed[1] = True

    def reset_colors(self):
        for each in self.board.ships:
            each.initcolor = self.color
            each.color = self.color
            each.update_me = True
        self.mainloop.redraw_needed[0] = True

    def ai_walk(self):
        if self.start_sequence:
            if self.disp_counter < self.disp_len:
                if self.disp_counter == 0:
                    self.highlight_colors()
                self.disp_counter += 1
            else:
                self.reset_colors()
                self.start_sequence = False
                self.ai_enabled = False
                self.disp_counter = 0
        elif self.completed_mode:
            self.disp_counter += 1
            if self.disp_counter > 1:
                self.completed_mode = False
                self.mainloop.db.update_completion(self.mainloop.userid, self.active_game.dbgameid, self.level.lvl)
                self.disp_counter = 0
                self.next_level()
        elif self.game_over_mode:
            self.disp_counter += 1
            self.highlight_colors()
            if self.disp_counter > 2:
                self.game_over_mode = False
                self.disp_counter = 0
                self.game_over()

    def check_result(self):
        pass
