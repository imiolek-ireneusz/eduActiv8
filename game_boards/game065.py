# -*- coding: utf-8 -*-

import pygame
import random
from math import pi, cos, acos, sin, sqrt

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.simple_vector as sv


# REMOVED GAME
class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 12, 8)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 19, 10)

    def create_game_objects(self, level=1):
        pass

    def handle(self, event):
        pass

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
