# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 99, 17)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.board.decolorable = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 0]
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
        self.level.game_step = 1
        self.start_sequence = True
        self.completed_mode = False
        self.game_over_mode = False
        self.disp_counter = 0
        self.disp_len = 3
        self.found = set()
        # setting level variable
        # data = [x_count, y_count, number_count, top_limit, ordered]
        if self.level.lvl == 1:
            data = [13, 9, 5, 3, 3]
        elif self.level.lvl == 2:
            data = [13, 9, 8, 3, 4]
        elif self.level.lvl == 3:
            data = [12, 9, 8, 4, 4]
        elif self.level.lvl == 4:
            data = [12, 9, 7, 4, 5]
        elif self.level.lvl == 5:
            data = [13, 9, 7, 5, 5]
        elif self.level.lvl == 6:
            data = [13, 9, 11, 5, 6]
        elif self.level.lvl == 7:
            data = [12, 9, 11, 6, 6]
        elif self.level.lvl == 8:
            data = [12, 9, 15, 6, 7]
        elif self.level.lvl == 9:
            data = [13, 9, 15, 7, 7]
        elif self.level.lvl == 10:
            data = [13, 9, 9, 7, 8]
        elif self.level.lvl == 11:
            data = [12, 9, 9, 8, 8]
        elif self.level.lvl == 12:
            data = [12, 9, 14, 8, 9]
        elif self.level.lvl == 13:
            data = [13, 9, 14, 9, 9]
        elif self.level.lvl == 14:
            data = [12, 9, 14, 10, 9]
        elif self.level.lvl == 15:
            data = [13, 9, 14, 11, 9]
        elif self.level.lvl == 16:
            data = [12, 9, 14, 12, 9]
        elif self.level.lvl == 17:
            data = [13, 9, 14, 13, 9]
        self.chapters = [1, 3, 5, 7, 9, 11, 13, 15, 17]
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

        self.level.games_per_lvl = self.max_games
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        self.current_count = 1
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
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and not self.show_msg and not self.start_sequence:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if active.unit_id in self.chosen:
                    active.initcolor = self.highlight_color
                    active.color = active.initcolor
                    self.found.add(active.unit_id)
                    if len(self.found) == self.current_count:
                        self.completed_mode = True
                        self.ai_enabled = True
                else:
                    active.initcolor = (255, 0, 0)
                    active.color = active.initcolor
                    self.game_over_mode = True  # self.game_over()
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
        self.current_step = 0
        self.current_count += 1
        self.found = set()
        self.level.game_step = self.current_count
        self.mainloop.redraw_needed[1] = True
        if self.current_count <= self.max_games:
            self.draw_nums()
            self.reset_colors()
            self.start_sequence = True
            self.ai_enabled = True
        else:
            # self.update_score(self.level.lvl + self.max_games)
            self.mainloop.db.update_completion(self.mainloop.userid, self.active_game.dbgameid, self.level.lvl)
            self.level.levelup()

    def game_over(self):
        self.level.game_step = 0
        self.current_count = 0
        self.next_level()

    def highlight_colors(self):
        for each in self.board.ships:
            if each.unit_id in self.chosen:
                each.initcolor = self.highlight_color
                each.color = each.initcolor
                each.update_me = True
        self.mainloop.redraw_needed[0] = True
        self.mainloop.redraw_needed[1] = True

    def reset_colors(self):
        for each in self.board.ships:
            each.initcolor = self.color
            each.color = each.initcolor
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
            if self.disp_counter > 1:  # self.disp_len:
                self.completed_mode = False
                self.disp_counter = 0
                self.next_level()
        elif self.game_over_mode:
            self.disp_counter += 1
            self.highlight_colors()
            if self.disp_counter > 2:  # self.disp_len:
                self.game_over_mode = False
                self.disp_counter = 0
                self.game_over()

    def check_result(self):
        pass
