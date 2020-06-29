# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.ai_enabled = True
        self.board.draw_grid = False
        white = [255, 255, 255]

        scheme = "white"
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                scheme = "black"

        if self.level.lvl == 1:
            data = [7, 5, 17, -2]
        elif self.level.lvl == 2:
            data = [7, 5, 17, -1]
        elif self.level.lvl == 3:
            data = [7, 5, 14, -2]
        elif self.level.lvl == 4:
            data = [7, 5, 14, -1]
        elif self.level.lvl == 5:
            data = [7, 5, 12, -2]
        elif self.level.lvl == 6:
            data = [7, 5, 12, -1]
        elif self.level.lvl == 7:
            data = [7, 5, 10, -2]
        elif self.level.lvl == 8:
            data = [7, 5, 10, -1]
        elif self.level.lvl == 9:
            data = [7, 5, 8, -2]
        elif self.level.lvl == 10:
            data = [7, 5, 8, -1]

        self.ai_speed = data[2]
        # stretch width to fit the screen size
        max_x_count = self.get_x_count(data[1], even=False)
        if max_x_count > 7:
            data[0] = max_x_count

        self.data = data
        self.level.game_step = 0
        self.level.games_per_lvl = 1
        self.moveable = False
        self.moves = []
        self.move_buttons = []
        self.possible_move_buttons = []
        self.sequence_counter = 0
        self.current_step = 0
        self.start_sequence = True
        self.completed_mode = False

        self.center = [data[0] // 2, data[1] // 2]

        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.add_unit(self.center[0], self.center[1], 1, 1, classes.board.MultiImgSprite, "", white,
                            os.path.join("schemes", scheme, "owl_5.png"), 0, frame_flow=[0, 1, 2, 3, 4, 3, 2, 1, 0],
                            frame_count=9, row_data=[5, 1])
        self.owl = self.board.ships[0]
        self.owl.outline = False
        self.owl.draggable = False
        self.owl.audible = True
        self.board.active_ship = 0
        self.ship_id = 0

        self.images = [os.path.join("schemes", scheme, "a_yellow_150.png"),
                       os.path.join("schemes", scheme, "a_green_150.png"),
                       os.path.join("schemes", scheme, "a_blue_150.png"),
                       os.path.join("schemes", scheme, "a_red_150.png")]
        for i in range(4):
            self.board.add_door(self.center[0], self.center[1], 1, 1, classes.board.SlidingDoor, "", white,
                                self.images[i], frame_flow=[0, 1], frame_count=2, row_data=[2, 1])

        self.update_arrows()
        self.board.all_sprites_list.move_to_front(self.board.ships[0])
        self.add_next_move()

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if self.ship_id < 0 and event.type == pygame.MOUSEBUTTONDOWN:
            # make it impossible to deselect the main character
            self.board.active_ship = 0
            self.ship_id = 0
            if self.moveable:
                pos = event.pos
                column = pos[0] // (self.layout.width)
                row = (pos[1] - self.layout.top_margin) // (self.layout.height)
                self.direction = [0, 0]
                arrow_clicked = False
                if column == self.owl_pos[0] - 1 and row == self.owl_pos[1]:
                    self.direction[0] = -1
                    arrow_clicked = True
                elif column == self.owl_pos[0] + 1 and row == self.owl_pos[1]:
                    self.direction[0] = 1
                    arrow_clicked = True
                elif column == self.owl_pos[0] and row == self.owl_pos[1] - 1:
                    self.direction[1] = -1
                    arrow_clicked = True
                elif column == self.owl_pos[0] and row == self.owl_pos[1] + 1:
                    self.direction[1] = 1
                    arrow_clicked = True

                if arrow_clicked:
                    self.check_direction_kdown()
        if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.moveable:
            self.move = False
        elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
            self.highlight_color(-1)
            self.mainloop.redraw_needed[0] = True
            self.move = False

    def update_arrows(self):
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        self.owl_pos = list(self.board.active_ship_pos)
        self.possible_moves = []
        self.possible_move_buttons = []
        for i in range(4):
            if 0 <= self.owl_pos[0] + directions[i][0] < self.data[0] and 0 <= self.owl_pos[1] + directions[i][1] < \
                    self.data[1]:
                pos = [self.owl_pos[0] + directions[i][0], self.owl_pos[1] + directions[i][1]]
                self.possible_moves.append(pos)
                self.possible_move_buttons.append(i)
            else:
                pos = self.owl_pos
            self.board.units[i].set_pos(pos)
        self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def after_keydown_move(self):
        self.update_arrows()
        if self.owl_pos == self.moves[self.current_step]:
            self.highlight_color(self.move_buttons[self.current_step])
            if self.current_step < len(self.moves) - 1:
                self.current_step += 1
                self.level.game_step = self.current_step
            else:
                self.level.game_step = self.current_step + 1
                self.ai_speed = 5
                self.completed_mode = True
                self.ai_enabled = True
            self.mainloop.redraw_needed[1] = True
            self.mainloop.redraw_needed[0] = True
        else:
            self.game_over()
        self.move = False

    def next_level(self):
        self.current_step = 0
        self.board._place_unit(0, self.center)
        self.update_arrows()

    def game_over(self):
        self.level.games_per_lvl = 1
        self.level.game_step = 0
        self.mainloop.redraw_needed[1] = True
        self.level.game_over()

    def highlight_color(self, btn_id):
        for i in range(4):
            if i == btn_id:
                self.board.units[i].set_frame(1)
                self.board.units[i].update_me = True
            else:
                self.board.units[i].set_frame(0)
                self.board.units[i].update_me = True

    def add_next_move(self):
        next, btn = self.pick_index()
        if len(self.moves) > -1 - self.data[3]:
            while btn == self.move_buttons[-1] and btn == self.move_buttons[self.data[3]]:
                next, btn = self.pick_index()
        self.moves.append(next)  # possible_moves = self.possible_moves()
        self.move_buttons.append(btn)

    def pick_index(self):
        index = random.choice(range(len(self.possible_moves)))
        next = self.possible_moves[index]
        btn = self.possible_move_buttons[index]
        return [next, btn]

    def ai_walk(self):
        if self.start_sequence:
            if self.sequence_counter < len(self.moves) * 2:
                if self.sequence_counter % 2 == 0:
                    self.highlight_color(self.move_buttons[self.sequence_counter // 2])
                else:
                    self.highlight_color(-1)
                self.sequence_counter += 1
            else:
                self.start_sequence = False
                self.ai_enabled = False
                self.sequence_counter = 0
                self.moveable = True
        elif self.completed_mode:
            if self.owl.frame < self.owl.frame_count - 1:
                self.owl.next_frame()
                self.owl.update_me = True
            else:
                self.check_result()

    def check_result(self):
        if self.current_step == len(self.moves) - 1:
            # self.update_score(len(self.moves)*2)
            self.add_next_move()
            self.next_level()
            self.level.games_per_lvl = len(self.moves)  # gpl #number of games to play in order to level up
            self.level.game_step = 0
            self.owl.set_frame(0)
            self.owl.update_me = True
            self.mainloop.redraw_needed[1] = True
            self.completed_mode = False
            self.start_sequence = True
            self.ai_enabled = True
            self.ai_speed = self.data[2]
            self.moveable = False
