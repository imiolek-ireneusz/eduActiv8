# -*- coding: utf-8 -*-

import os
import pygame

import classes.board
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 17, 11)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False
        if self.mainloop.m.badge_count == 0:
            self.mainloop.m.lang_change()

        #ver_color = (55, 0, 90)
        ver_color = (33, 121, 149)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.scheme_dir = "black"
                color = (0, 0, 0)
                ver_color = (255, 255, 0)
            else:
                self.scheme_dir = "white"
                color = (255, 255, 255)
        else:
            self.scheme_dir = "white"
            color = (255, 255, 255)

        # (234,218,225) #ex.hsv_to_rgb(225,15,235)
        self.color = color
        font_color = (33, 121, 149)
        font_color2 = (20, 75, 92)
        data = [17, 11]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=False)
        if x_count > 17:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.initcolor = color
        self.board.board_bg.color = color
        self.board.board_bg.update_me = True
        if self.mainloop.config.update_available:
            txt = self.d["upd8 available"] % (self.mainloop.config.version, self.mainloop.config.avail_version)
            align = 0
        else:
            txt = self.d["upd8 no update"] % self.mainloop.config.version
            align = 2
        self.board.add_unit(0, 0, data[0], 1, classes.board.Label, [txt, " ", " "], color, "", 5)
        self.board.units[-1].align = align
        self.board.units[-1].font_color = ver_color

        img_src = os.path.join("schemes", self.scheme_dir, 'home_logo.png')
        self.board.add_unit(0, 1, data[0], 3, classes.board.ImgCenteredShip, "", color, img_src)
        self.canvas = self.board.ships[-1]
        self.canvas.immobilize()
        self.canvas.outline = False

        if self.mainloop.android is None:
            self.board.add_unit(0, 6, data[0], 1, classes.board.Label, self.lang.d["Check for newer version..."], color, "", 6)
            self.board.units[-1].font_color = font_color
            self.board.add_unit(0, 7, data[0], 1, classes.board.Label, "www.sourceforge.net/projects/eduactiv8   |   www.github.com/imiolek-ireneusz/eduactiv8",
                                color, "", 6)
            self.board.units[-1].font_color = font_color

            # self.board.add_unit(0, 7, data[0], 1, classes.board.Label, ["http://sourceforge.net/projects/eduactiv8/",
            #                                                            "https://github.com/imiolek-ireneusz/eduactiv8"],color, "", 6)
            self.board.units[-1].font_color = font_color

        self.board.add_unit(0, 5, data[0], 1, classes.board.Label, ["www.facebook.com/eduactiv8", ""], color, "", 4)
        self.board.units[-1].font_color = font_color2

        self.board.add_unit(0, 4, data[0], 1, classes.board.Label, "www.eduactiv8.org", color, "", 1)
        self.board.units[-1].font_color = font_color2

        self.board.add_unit(0, 9, data[0], 1, classes.board.Label,
                            "info%seduactiv8%sorg   |   bugs%seduactiv8%sorg" % ("@", ".", "@", "."), color, "", 6)
        self.board.units[-1].font_color = font_color

        self.board.add_unit(0, 10, data[0], 1, classes.board.Label, "Copyright (C) 2012 - 2018  Ireneusz Imiolek",
                            color, "", 6)
        self.board.units[-1].font_color = font_color

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up

    def start_game(self, gameid):
        self.mainloop.m.start_hidden_game(gameid)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
