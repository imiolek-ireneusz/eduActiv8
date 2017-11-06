# -*- coding: utf-8 -*-

import os
import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc

# TODO Reuse this game - this one has been integrated with 82

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 10, 4)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 40, 30)

    def create_game_objects(self, level=1):
        pass

    def handle(self, event):
        pass

    def update(self, game):
        pass

    def check_result(self):
        pass
