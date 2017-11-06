# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 11)

    def create_game_objects(self, level=1):
        self.board.decolorable = False
        self.board.draw_grid = False
        color = (234, 218, 225)
        self.color = color
        self.grey = (200, 200, 200)
        self.font_hl = (100, 0, 250)
        self.task_str_color = ex.hsv_to_rgb(200, 200, 230)
        self.activated_col = self.font_hl
        white = (255, 255, 255)
        self.bg_col = white
        self.top_line = 3  # self.board.scale//2
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.bg_col = (0, 0, 0)

        rngs = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                     self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        data = [39, 18]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=None)
        if x_count > 39:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        n1 = random.randrange(rngs[0], rngs[1])
        n2 = random.randrange(rngs[2], rngs[3])
        self.n1 = max(n1, n2)
        self.n2 = min(n1, n2)
        self.sumn1n2 = self.n1 + self.n2
        self.n1s = str(self.n1)
        self.n2s = str(self.n2)
        self.sumn1n2s = str(self.sumn1n2)
        self.n1sl = len(self.n1s)
        self.n2sl = len(self.n2s)
        self.sumn1n2sl = len(self.sumn1n2s)
        self.cursor_pos = 0
        self.correct = False
        self.carryl = []
        self.resultl = []
        self.nums1l = []
        self.nums2l = []
        self.ship_id = 0
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if self.lang.lang == 'el':
            qm = ";"
        else:
            qm = "?"

        question = self.n1s + " + " + self.n2s + " = " + qm
        self.board.add_unit(1, 0, data[0] - 1 - self.sumn1n2sl * 3, 3, classes.board.Label, question, self.bg_col, "",
                            21)
        self.board.units[-1].align = 1

        # carry 1
        for i in range(self.sumn1n2sl - 1):
            self.board.add_unit(data[0] - 5 - i * 3, 1, 1, 1, classes.board.Letter, "", self.bg_col, "", 0)
            self.carryl.append(self.board.ships[-1])
            self.carryl[-1].set_outline(self.grey, 2)
            self.carryl[-1].pos_id = i
        # first number
        for i in range(self.n1sl):
            self.board.add_unit(data[0] - 3 - i * 3, 2, 3, 3, classes.board.Label, self.n1s[-(i + 1)], self.bg_col, "",
                                21)
            self.nums1l.append(self.board.units[-1])
            self.nums1l[-1].font_color = self.grey
            self.nums1l[-1].pos_id = i
        # second number
        i = 0
        for i in range(self.n2sl):
            self.board.add_unit(data[0] - 3 - i * 3, 5, 3, 3, classes.board.Label, self.n2s[-(i + 1)], self.bg_col, "",
                                21)
            self.nums2l.append(self.board.units[-1])
            self.nums2l[-1].pos_id = i
        i += 1
        self.board.add_unit(data[0] - 3 - i * 3, 5, 3, 3, classes.board.Label, "+", self.bg_col, "", 21)
        self.plus_label = self.board.units[-1]
        # line
        self.board.add_unit(data[0] - self.sumn1n2sl * 3, 8, self.sumn1n2sl * 3, 1, classes.board.Label, "",
                            self.bg_col, "", 21)
        self.draw_hori_line(self.board.units[-1])

        # result
        for i in range(self.sumn1n2sl):
            self.board.add_unit(data[0] - 3 - i * 3, 9, 3, 3, classes.board.Letter, "", self.bg_col, "", 21)
            self.resultl.append(self.board.ships[-1])
            self.resultl[-1].set_outline(self.grey, 2)
            self.resultl[-1].pos_id = i

            self.resultl[-1].checkable = True
            self.resultl[-1].init_check_images()


        self.resultl[0].set_outline(self.activated_col, 3)
        self.home_square = self.resultl[0]
        self.board.active_ship = self.home_square.unit_id
        for each in self.board.ships:
            each.immobilize()
        self.deactivate_colors()
        self.reactivate_colors()

    def draw_hori_line(self, unit):
        w = unit.grid_w * self.board.scale
        h = unit.grid_h * self.board.scale
        center = [w // 2, h // 2]

        canv = pygame.Surface([w, h - 1])
        canv.fill(self.bg_col)

        pygame.draw.line(canv, self.grey, (0, self.top_line), (w, self.top_line), 3)
        unit.painting = canv.copy()
        unit.update_me = True

    def auto_check_reset(self):
        for each in self.resultl:
            each.set_display_check(None)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.show_msg == False:
            if event.type == pygame.KEYDOWN:
                self.auto_check_reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.home_sqare_switch(self.board.active_ship + 1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.home_sqare_switch(self.board.active_ship - 1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.home_sqare_switch(self.board.active_ship - self.sumn1n2sl + 1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.home_sqare_switch(self.board.active_ship + self.sumn1n2sl)
            elif event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN and not self.correct:
                lhv = len(self.home_square.value)
                self.changed_since_check = True
                if event.key == pygame.K_BACKSPACE:
                    if lhv > 0:
                        self.home_square.value = self.home_square.value[0:lhv - 1]
                else:
                    char = event.unicode
                    if (len(char) > 0 and lhv < 2 and char in self.digits):

                        if self.home_square in self.resultl:
                            if lhv == 1:
                                s = self.home_square.value + char
                                if s[0] == "0":
                                    self.home_square.value = char
                                else:
                                    n = int(s)
                                    if n < 20:
                                        self.home_square.value = str(n % 10)
                                        try:
                                            self.carryl[self.home_square.pos_id].value = "1"
                                            self.carryl[self.home_square.pos_id].update_me = True
                                        except:
                                            pass

                                    else:
                                        self.home_square.value = char
                            else:
                                self.home_square.value = char
                        elif self.home_square in self.carryl:
                            if char == "1":
                                self.home_square.value = char
                            else:
                                self.home_square.value = ""

                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.home_sqare_switch(self.board.active_ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.auto_check_reset()

    def home_sqare_switch(self, activate):
        if activate < 0 or activate > self.sumn1n2sl * 2 - 1:
            activate = self.sumn1n2sl - 1

        if activate >= 0 and activate < self.sumn1n2sl * 2 - 1:
            self.board.active_ship = activate
            self.home_square.update_me = True
            if self.board.active_ship >= 0:
                self.home_square.set_outline(self.grey, 2)
                self.deactivate_colors()
                self.home_square = self.board.ships[self.board.active_ship]
                self.home_square.set_outline(self.activated_col, 3)
                self.reactivate_colors()
                self.home_square.font_color = self.font_hl
            self.home_square.update_me = True
            self.mainloop.redraw_needed[0] = True

    def deactivate_colors(self):
        for each in self.board.ships:
            each.font_color = self.grey
            each.update_me = True

        for each in self.board.units:
            each.font_color = self.grey
            each.update_me = True

    def reactivate_colors(self):
        self.plus_label.font_color = self.font_hl
        self.board.units[0].font_color = self.task_str_color
        if self.home_square.pos_id > 0:
            self.carryl[self.home_square.pos_id - 1].font_color = self.font_hl
        if (self.n1sl > self.home_square.pos_id):
            self.nums1l[self.home_square.pos_id].font_color = self.font_hl
        if (self.n2sl > self.home_square.pos_id):
            self.nums2l[self.home_square.pos_id].font_color = self.font_hl
        self.resultl[self.home_square.pos_id].font_color = self.font_hl

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        s = ""
        i = 0
        for each in reversed(self.resultl):
            s += each.value
            if each.value == self.sumn1n2s[i]:
                each.set_display_check(True)
            else:
                each.set_display_check(False)
            i += 1
        if s == self.sumn1n2s:
            self.level.next_board()
