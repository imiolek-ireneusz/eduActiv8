# -*- coding: utf-8 -*-

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 8)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False

        self.color = (255, 255, 255)

        font_color2 = ex.hsv_to_rgb(self.mainloop.cl.get_interface_hue(), 255, 150)
        data = [23, 16]

        self.data = data
        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.initcolor = self.color
        self.board.board_bg.color = self.color
        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        self.board.add_unit(0, 0, data[0], 1, classes.board.Label, "Copyright (C) 2012 - 2025  Ireneusz Imiolek",
                            self.color, "", 1)
        self.board.add_unit(0, 1, data[0], 1, classes.board.Label, "", self.color, "", 2)
        self.board.add_unit(0, 2, data[0], 5, classes.board.Label, self.lang.d["Credits_long"], self.color, "", 2)
        self.board.units[-1].valign = 1
        if self.mainloop.android is None:
            self.board.add_unit(0, 7, data[0], 1, classes.board.Label, "", self.color, "", 2)
            self.board.add_unit(0, 8, data[0], 1, classes.board.Label, self.lang.d["Lic_title"], self.color, "", 1)
            self.board.add_unit(0, 9, data[0], 6, classes.board.Label, self.lang.d["Lic_desc"], self.color, "", 2)
            self.board.units[-1].valign = 1

        for each in self.board.units:
            each.font_color = font_color2

    def handle(self, event):
        gd.BoardGame.handle(self, event)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
