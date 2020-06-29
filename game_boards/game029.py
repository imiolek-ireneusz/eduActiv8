# -*- coding: utf-8 -*-

import os
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.laby
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 3, 7)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 7)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        s = random.randrange(150, 205, 5)
        v = random.randrange(150, 205, 5)
        h = random.randrange(0, 255, 5)
        color = ex.hsv_to_rgb(h, s, v)
        scheme = "white"
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                scheme = "black"
        # data = [0:x_count, 1:y_count, 2:games_per_level, 3:bug_img, 4:level_maps]
        img1 = os.path.join("schemes", scheme, "mouse_77.png")
        img2 = os.path.join("schemes", scheme, "cheese_77.png")

        if self.level.lvl == 1:  # img_ 77x77
            data = [11, 7, 10]
        elif self.level.lvl == 2:
            data = [13, 9, 10]
        elif self.level.lvl == 3:
            data = [17, 11, 10]
        elif self.level.lvl == 4:
            data = [19, 13, 10]
        elif self.level.lvl == 5:
            data = [23, 15, 10]
        elif self.level.lvl == 6:
            data = [25, 17, 10]
        elif self.level.lvl == 7:
            data = [27, 19, 10]
        self.auto_checking = True

        # rescale the number of squares horizontally to better match the screen width
        x_count = self.get_x_count(data[1], even=False)
        if x_count > data[0]:
            data[0] = x_count

        self.data = data
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.mylaby = classes.laby.Laby((data[0] + 1) // 2, (data[1] + 1) // 2, 0, 0, scale)
        self.mylaby.generate_laby()
        laby_grid = self.mylaby.labi_to_array()
        self.solution = [data[0] - 1, data[1] - 1]
        self.board.add_door(self.solution[0], self.solution[1], 1, 1, classes.board.Door, "", (255, 255, 255), img2)
        self.board.units[0].outline = False

        x = 0
        y = 0

        for j in range(data[1]):
            for i in range(data[0]):
                if laby_grid[j][i] == 1:
                    self.board.add_unit(i, j, 1, 1, classes.board.Obstacle, "", color)
        self.ships_count = len(self.board.ships)
        self.board.add_unit(x, y, 1, 1, classes.board.ImgShipRota, "", (255, 255, 255), img1)
        self.board.ships[0].outline = False
        self.board.ships[0].draggable = True
        self.board.ships[0].audible = False
        self.board.all_sprites_list.move_to_front(self.board.ships[0])
        self.board.active_ship = 0
        self.ship_id = 0
        self.board.moved = self.check_result
        self.drag = False

    def handle(self, event):
        if not self.show_msg:
            if self.board.ships[0].grid_pos == self.solution:
                self.check_result()

        gd.BoardGame.handle(self, event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def after_keydown_move(self):
        self.changed_since_check = True
        self.check_result()

    def check_result(self):
        if self.board.ships[self.board.active_ship].grid_pos == self.solution:
            self.board.ships[0].draggable = False
            self.level.next_board()
        else:
            self.changed_since_check = False
