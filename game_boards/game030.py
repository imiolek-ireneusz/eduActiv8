# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 15, 6)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 12, 7)

    def create_game_objects(self, level=1):
        self.change_count = 0
        self.ai_enabled = True
        self.ai_speed = 3
        self.frame_tick = 8
        self.frame_flow = 0
        self.points = 0
        self.hit_ = 0
        self.total_ = 0
        self.active_mole = None

        self.grass_bg = [51, 128, 0]
        self.score_bg = (255, 255, 255)  # [219,255,187]

        # data = [x_count, y_count, games per lvl, time on surface, 1/x minimum to pass]
        if self.level.lvl == 1:
            data = [6, 3, 15, 4, 12]
        elif self.level.lvl == 2:
            data = [6, 3, 25, 3, 22]
        elif self.level.lvl == 3:
            data = [6, 3, 30, 2, 25]
        elif self.level.lvl == 4:
            data = [6, 3, 40, 1, 33]
        elif self.level.lvl == 5:
            data = [6, 3, 50, 0, 42]
        elif self.level.lvl == 6:
            data = [6, 3, 50, -1, 45]

        self.data = data

        self.level.games_per_lvl = data[2]

        self.vis_buttons = [0, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.board.add_unit(0, 0, 2, 2, classes.board.Label, "0", self.score_bg, "", 3)
        self.board.add_unit(0, 2, 2, 1, classes.board.Label, str(self.mainloop.score), self.score_bg, "", 3)
        self.hit_miss = self.board.units[0]
        self.score = self.board.units[1]
        self.max_escape = self.data[2] - self.data[4] + 1
        x = 2
        y = 0
        for i in range(12):  # 222x222
            self.board.add_unit(x, y, 1, 1, classes.board.MultiImgSprite, "", self.grass_bg, "mole_sprites.png", 0,
                                frame_flow=[0, 1, 2, 3, 2, 1], frame_count=6, row_data=[4, 1])
            x = x + 1
            if x > data[0] - 1:
                x = 2
                y += 1

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.show_msg == False:
            self.hit()

    def update(self, game):
        game.fill(self.grass_bg)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def ai_walk(self):
        if self.frame_flow == 0:
            self.activate()
            self.frame_flow = [0, 1, 2, 3, 2, 1]  # self.board.ships[self.active_mole_id].frame_flow
        if self.frame_tick < 3:
            self.active_mole.next_frame()
            self.active_mole.update_me = True
        elif 4 + self.data[3] < self.frame_tick < 8 + self.data[3]:  # 4 -> 8
            self.active_mole.next_frame()
            self.active_mole.update_me = True

        self.frame_tick += 1
        if self.frame_tick > 14 + self.data[3]:
            self.frame_tick = 0
            self.active_mole.reset()
            self.activate()
            self.check_result()

    def activate(self):
        self.active_mole_id = random.randrange(0, 12)
        self.active_mole = self.board.ships[self.active_mole_id]
        self.active_mole.reset()
        self.frame_tick = 0
        y = self.active_mole_id // 4
        x = self.active_mole_id - (y * 4) + 2
        self.active_mole_pos = (x, y)

        self.total_ += 1
        if self.total_ == self.data[2] + 1:
            pass  # self.check_result()
        else:
            self.level.game_step = self.total_
            self.hit_miss.value = str(self.hit_)

        self.mainloop.redraw_needed[1] = True

    def reset(self):
        self.active_mole.reset()
        self.frame_tick = 8 + self.data[3]

    def game_reset(self):
        self.reset()
        self.points = 0
        self.hit_ = 0
        self.total_ = 1
        self.score.value = str(self.mainloop.score)
        self.hit_miss.value = str(self.hit_)

    def hit(self):
        if self.active_mole is not None and self.frame_tick < 8 + self.data[
            3] and self.board.active_ship_pos == self.active_mole_pos:
            self.points += self.active_mole.frame_flow[self.active_mole.frame] * 10
            self.score.value = str(self.mainloop.score + self.points)
            self.active_mole_pos = (-1, -1)
            self.hit_ += 1
            self.reset()
            self.mainloop.sfx.play(12)
            self.hit_miss.value = str(self.hit_)
            self.hit_miss.update_me = True
            self.score.update_me = True

    def game_over(self):
        tts = self.dp["work harder"]
        self.level.game_step = self.total_
        self.level.game_over(tts)

    def check_result(self):
        if self.total_ < self.data[2]:
            if self.total_ - self.hit_ > self.max_escape:
                self.game_over()
        elif self.total_ >= self.data[2] + 1:
            tts = ""
            if self.hit_ < self.data[4]:
                self.game_over()
            else:
                self.mainloop.score += self.points
                self.level.game_step = self.total_ - 1
                self.level.next_board(tts)
