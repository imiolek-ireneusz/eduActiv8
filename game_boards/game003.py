# -*- coding: utf-8 -*-

import pygame
from math import ceil

import classes.board
import classes.extras as ex
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

        self.lang_titles = self.mainloop.lang.lang_titles
        self.all_lng = self.mainloop.lang.all_lng
        self.ok_lng = self.mainloop.lang.ok_lng
        self.languages = self.ok_lng

        self.lang_count = len(self.languages)
        half = int(ceil(self.lang_count / 2.0)) - 1

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
                t = i
                self.board.add_unit(c - 6, t, 2, 1, classes.board.Label, self.lang.lang_progress[i], white, "", 3)
                self.board.units[-1].font_color = (200, 200, 200)
            else:
                c = self.center + 4
                t = i - half - 1
                self.board.add_unit(c + 4, t, 2, 1, classes.board.Label, self.lang.lang_progress[i], white, "", 3)
                self.board.units[-1].font_color = (200, 200, 200)
            self.board.add_unit(c - 4, t, 8, 1, classes.board.Letter, self.lang_titles[i], white, "", 2)
            self.board.units[-1].update_lng_font_size("def_2.0")
            if self.all_lng[i] == lang:
                lng_index = i

        self.board.add_unit(0, data[1]-1, data[0], 1, classes.board.Label, "https://www.transifex.com/eduactiv8/eduactiv8/", white, "", 3)
        self.board.units[-1].font_color = (150, 150, 150)
        self.board.units[-1].update_lng_font_size("def_2.0")


        for each in self.board.ships:
            each.immobilize()
            each.readable = False
            each.outline = False
            each.font_color = (55, 105, 5)

        self.reselect(lng_index)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            active = self.board.active_ship
            if event.button == 1:
                if active >= 0:
                    # change language
                    if self.lang.lang != self.languages[active]:
                        self.change_language(self.languages[active], self.lang_titles[active], active)
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
        self.mainloop.sb.update_fonts()
        self.mainloop.dialog.reload_fonts()
        self.reselect(lang_id)
        self.mainloop.sb.resize()
        self.mainloop.sb.update_me = True
        if lng in self.lang.tts_disabled_lngs:
            self.mainloop.sb.espeak_avail(False)
        else:
            self.mainloop.sb.espeak_avail(True)

    def reselect(self, selectid):
        for each in self.board.ships:
            if each.unit_id != selectid:
                each.font_color = (40, 40, 40)
                each.update_lng_font_size("def_1.75")
            else:
                each.font_color = ex.hsv_to_rgb(self.mainloop.cl.get_interface_hue(), 255, 200)
                each.update_lng_font_size("def_1.25")
            each.update_me = True
        """
        # Malayam language - font selector - temporarily disabled
        if selectid == self.board.ships[-2].unit_id:
            self.board.ships[-2].update_lng_font_size("ml_1.25")
        else:
            self.board.ships[-2].update_lng_font_size("ml_1.75")
        """


    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
