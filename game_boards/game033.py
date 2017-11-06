# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc

# REMOVED GAME
class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 10, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        data = [11, 6]

        self.data = data

        self.board.set_animation_constraints(0, data[0], 0, data[1] - 1)
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

    def handle(self, event):
        pass

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
