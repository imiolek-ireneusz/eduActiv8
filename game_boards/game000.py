# -*- coding: utf-8 -*-

import os
import pygame

import classes.board
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 11)

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

        self.board.add_unit(data[0]-4, 0, 4, 1, classes.board.Label, ["v.%s" % self.mainloop.config.version, " ", " "],
                            color, "", 5)
        self.board.units[-1].align = 2
        self.board.units[-1].font_color = ver_color

        img_src = os.path.join("schemes", self.scheme_dir, 'home_logo.png')
        self.board.add_unit(0, 1, data[0], 3, classes.board.ImgCenteredShip, "", color, img_src)
        self.canvas = self.board.ships[-1]
        self.canvas.immobilize()
        self.canvas.outline = False
        """
        self.canvas.font = self.canvas.board.font_sizes[4]
        val = "v.%s " % self.mainloop.config.version
        text = self.canvas.font.render(val, 1, ver_color)
        y = self.canvas.img_rect.height - self.canvas.font.size(val)[1] - 1
        x = self.canvas.img_rect.width - self.canvas.font.size(val)[0]# - (self.canvas.img_rect.width//100)
        self.canvas.img.blit(text, (x, y))
        """
        if self.mainloop.android is None:
            self.board.add_unit(0, 6, data[0], 1, classes.board.Label,
                                [self.lang.d["Check for newer version..."]], color, "", 4)
            self.board.units[-1].font_color = font_color2

            self.board.add_unit(0, 7, data[0], 1, classes.board.Label, ["http://sourceforge.net/projects/eduactiv8/",
                                                                        "https://github.com/imiolek-ireneusz/eduactiv8"],
                                color, "", 4)
            self.board.units[-1].font_color = font_color

        self.board.add_unit(0, 5, data[0], 1, classes.board.Label, ["www.facebook.com/eduactiv8", ""], color, "", 4)
        self.board.units[-1].font_color = font_color

        self.board.add_unit(0, 4, data[0], 1, classes.board.Label, "www.eduactiv8.org", color, "", 2)
        self.board.units[-1].font_color = font_color
        if not self.mainloop.speaker.started and self.mainloop.android is None:
            self.board.add_unit(0, 8, data[0], 2, classes.board.Label, self.lang.d["please install espeak"], color, "",
                                5)
            self.board.units[-1].font_color = font_color

        self.board.add_unit(0, 10, data[0], 1, classes.board.Label, "Copyright (C) 2012 - 2017  Ireneusz Imiolek",
                            color, "", 6)
        self.board.units[-1].font_color = font_color
        """
        centre = data[0] // 2
        self.board.add_unit(0, 10, centre, 1, classes.board.Letter, ">> %s <<" % self.lang.d["Credits"], color2, "", 3)
        self.btn_lic = self.board.ships[-1]
        self.btn_lic.font_color = (255, 0, 0)
        self.btn_lic.highlight = False
        self.btn_lic.readable = False
        self.board.add_unit(centre + 1, 10, centre, 1, classes.board.Letter,
                            ">> %s <<" % self.lang.d["Translation Credits"], color2, "", 3)
        self.btn_tra = self.board.ships[-1]
        self.btn_tra.font_color = (255, 0, 0)
        self.btn_tra.highlight = False
        self.btn_tra.readable = False
        """

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                active = self.board.active_ship
                if active > 0:
                    if self.board.ships[active] == self.btn_lic:
                        self.start_game(1)
                    elif self.board.ships[active] == self.btn_tra:
                        self.start_game(2)
        """

    def start_game(self, gameid):
        self.mainloop.m.start_hidden_game(gameid)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
