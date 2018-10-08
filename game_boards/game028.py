# -*- coding: utf-8 -*-

import os
import pygame

import classes.board
import classes.game_driver as gd
import classes.laby
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 5, 18)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 5, 4)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.check_laby = True
        self.auto_checking = True

        # all_grid_sizes_at_1024_768 = [[7, 4],[8, 5],[9, 6],[10, 7],[11, 7],[12, 8],[13, 9],[14, 9],[15, 10],[16, 11],[17, 11],[18, 12],[19, 13],[20, 14],[21, 14],[22, 15],[23, 16],[24, 16],[25, 17],[26, 18],[27, 19],[28, 19],[29, 20],,[30,21]]
        grid_sizes = [[5, 4], [7, 5], [8, 6], [9, 7], [11, 8], [12, 9], [14, 10], [15, 11], [17, 12], [18, 13],
                      [19, 14], [21, 15], [22, 16], [24, 17], [25, 18], [26, 19], [28, 20], [29, 21], [30, 22]]

        data = grid_sizes[self.level.lvl - 1]

        # rescale the number of squares horizontally to better match the screen width
        x_count = self.get_x_count(data[1], even=False)
        if x_count > data[0]:
            data[0] = x_count

        self.data = data

        self.points = (data[0] + data[1]) // 5

        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        bg_col = (255, 255, 255)
        line_col = (0, 150, 0)
        line_width = 3
        scheme = "white"
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                scheme = "black"
                line_col = self.mainloop.scheme.u_font_color
                bg_col = (0, 0, 0)

        img_src1 = os.path.join("schemes", scheme, "sheep.png")
        img_src2 = os.path.join("schemes", scheme, "sheep_herd.png")

        self.mylaby = classes.laby.laby(data[0], data[1], 0, 0, scale, line_col, line_width)
        self.mylaby.generate_laby()

        self.board.add_unit(0, 0, 1, 1, classes.board.ImgShip, "", bg_col, img_src1)
        self.person = self.board.ships[0]
        self.person.audible = False
        self.person.draggable = True
        self.board.add_door(data[0] - 1, data[1] - 1, 1, 1, classes.board.Door, "", bg_col, img_src2)
        self.board.units[0].outline = False
        self.board.ships[0].outline = False
        self.board.all_sprites_list.move_to_front(self.person)
        self.board.active_ship = 0
        self.ship_id = 0
        self.board.moved = self.check_result
        self.drag = False

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent
        if self.show_msg == False:
            self.mylaby.show(game)

    def after_keydown_move(self):
        pass
        # self.changed_since_check = True
        # self.check_result()

    def check_result(self):
        target = pygame.sprite.spritecollide(self.board.units[0], self.board.ship_list, False, collided=None)
        if len(target) > 0:
            # self.update_score(self.points)
            self.level.next_board()
