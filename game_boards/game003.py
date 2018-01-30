# -*- coding: utf-8 -*-
from __future__ import with_statement

import pygame
from math import ceil

import classes.board
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 2, 2)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False

        white = (255, 255, 255)
        color = white

        self.lang_titles = self.mainloop.lang.lang_titles
        self.all_lng = self.mainloop.lang.all_lng
        self.ok_lng = self.mainloop.lang.ok_lng
        """
        if self.mainloop.config.google_trans_languages == True:
            self.languages = self.all_lng
        else:
        """
        self.languages = self.ok_lng

        self.lang_count = len(self.languages)
        half = int(ceil(self.lang_count / 2))

        data = [20, half + 3]

        max_x_count = self.get_x_count(data[1], even=True)
        if max_x_count > self.lang_count * 2 and max_x_count > 24:
            data[0] = max_x_count
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])

        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.center = self.data[0] // 2

        lang = self.mainloop.config.settings["lang"]
        lng_index = 0

        for i in range(self.lang_count):
            if i <= half:
                c = self.center - 4
                t = i + 0
            else:
                c = self.center + 4
                t = i - half - 1 + 0
            self.board.add_unit(c - 4, t, 8, 1, classes.board.Letter, self.lang_titles[i], white, "", 2)

            if self.all_lng[i] == lang:
                lng_index = i

        for each in self.board.ships:
            each.immobilize()
            each.readable = False
            each.outline = False
            each.font_color = (55, 105, 5)

        self.reselect(lng_index)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN:
            active = self.board.active_ship
            if event.button == 1:
                toggle = False
                if active >= 0:
                    # change language
                    if self.lang.lang != self.languages[active]:
                        self.change_language(self.languages[active], self.lang_titles[active], active)
                    if toggle:
                        self.mainloop.fullscreen_toggle(self.mainloop.info)
                    else:
                        self.level.load_level()

    def change_language(self, lng, lng_title, lang_id):
        self.mainloop.db.save_user_lang(lng)
        self.mainloop.config.settings["lang"] = lng
        self.lang.lang = lng
        self.mainloop.xml_conn.load_xml_files()
        self.lang.get_lang_attr()
        self.d = self.lang.d
        self.mainloop.speaker.restart_server()
        self.mainloop.m.lang_change()
        self.mainloop.redraw_needed = [True, True, True]

        if lng == "he":
            sv = self.lang.dp["Hebrew"]
        else:
            sv = lng_title
        self.say(sv)
        self.mainloop.info.update_fonts()
        self.reselect(lang_id)
        self.mainloop.sb.resize()
        self.mainloop.sb.update_me = True

    def reselect(self, selectid):
        for each in self.board.ships:
            if each.unit_id != selectid:
                each.font_color = (40, 40, 40)
                each.font = self.board.font_sizes[2]
            else:
                each.font_color = (130, 0, 180)
                each.font = self.board.font_sizes[0]
            each.update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
