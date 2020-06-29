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
        self.hint1_fcol = (100, 0, 250)
        self.hint2_fcol = (200, 0, 0)
        self.hint3_fcol = (250, 0, 200)

        self.task_str_color = ex.hsv_to_rgb(200, 200, 230)
        self.activated_col = self.font_hl
        white = (255, 255, 255)
        self.bg_col = white
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.bg_col = (0, 0, 0)
        self.top_line = 3
        rngs = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                     self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        self.level.games_per_lvl = 99

        data = [39, 18]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=None)
        if x_count > 39:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        while True:
            n1 = random.randrange(rngs[0], rngs[1])
            n2 = random.randrange(rngs[2], rngs[3])
            if n1 != n2:
                break
        self.n1 = max(n1, n2)
        self.n2 = min(n1, n2)
        self.sumn1n2 = self.n1 - self.n2
        self.n1s = str(self.n1)
        self.n2s = str(self.n2)
        self.sumn1n2s = str(self.sumn1n2)
        self.n1sl = len(self.n1s)
        self.n2sl = len(self.n2s)
        self.sumn1n2sl = len(self.sumn1n2s)
        self.cursor_pos = 1
        self.correct = False
        self.carry1l = []
        self.carry10l = []
        self.resultl = []
        self.nums1l = []
        self.nums2l = []
        self.all_nums = []
        s = "%0" + str(self.n1sl) + "d"
        self.n1sh = s % self.n1
        self.n2sh = s % self.n2

        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if self.lang.lang == 'el':
            qm = ";"
        else:
            qm = "?"

        question = self.n1s + " - " + self.n2s + " = " + qm
        # question
        self.board.add_unit(1, 0, data[0] - 3 - (max(self.n1sl, self.n2sl)) * 3, 3, classes.board.Label, question,
                            self.bg_col, "", 21)
        self.board.units[-1].align = 1

        # borrow 1
        for i in range(self.n1sl - 1):
            self.board.add_unit(data[0] - 6 - i * 3, 0, 1, 1, classes.board.Label, "-", self.bg_col, "", 0)
            self.board.add_unit(data[0] - 5 - i * 3, 0, 1, 1, classes.board.Letter, "", self.bg_col, "", 1)
            self.carry1l.append(self.board.ships[-1])
            self.carry1l[-1].set_outline(self.grey, 2)
            self.carry1l[-1].pos_id = i
            self.board.units[-1].align = 2

        # add 10
        for i in range(self.n1sl - 1):
            self.board.add_unit(data[0] - 3 - i * 3, 1, 1, 1, classes.board.Label, "+", self.bg_col, "", 0)
            self.board.add_unit(data[0] - 2 - i * 3, 1, 1, 1, classes.board.Letter, "", self.bg_col, "", 1)
            self.carry10l.append(self.board.ships[-1])
            self.carry10l[-1].set_outline(self.grey, 2)
            self.carry10l[-1].pos_id = i
            self.board.units[-1].align = 2

        self.board.add_unit(data[0] - 2 - self.n1sl * 3, 0, 2, 1, classes.board.Label, "-1", self.bg_col, "", 0)
        self.board.add_unit(data[0] - 2 - self.n1sl * 3, 1, 2, 1, classes.board.Label, "+10", self.bg_col, "", 0)

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
        self.board.add_unit(data[0] - 3 - i * 3, 5, 3, 3, classes.board.Label, "-", self.bg_col, "", 21)
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

        self.resultl[0].set_outline(self.activated_col, 3)
        self.home_square = self.resultl[0]
        self.board.active_ship = self.home_square.unit_id

        self.activable_count = len(self.board.ships)
        self.board.add_unit(0, 9, data[0] - self.sumn1n2sl * 3 - 3, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint1 = self.board.units[-1]
        self.hint1.align = 1

        self.board.add_unit(0, 11, data[0] - self.sumn1n2sl * 3 - 3, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint2 = self.board.units[-1]
        self.hint2.align = 1

        self.board.add_unit(0, 5, data[0] - self.sumn1n2sl * 3 - 6, 3, classes.board.Label, "", self.bg_col, "", 22)
        self.hint3 = self.board.units[-1]
        self.hint3.align = 1

        self.board.add_unit(0, 15, data[0], 2, classes.board.Letter, self.lang.d["demo start"], self.bg_col, "", 22)
        self.next_step_btn = self.board.ships[-1]
        self.next_step_btn.readable = False

        self.all_nums.extend(self.carry1l)
        self.all_nums.extend(self.carry10l)
        self.all_nums.extend(self.nums1l)
        self.all_nums.extend(self.nums2l)
        self.all_nums.extend(self.resultl)

        for each in self.board.ships:
            each.immobilize()
        self.deactivate_colors()
        self.board.units[0].font_color = self.task_str_color
        self.next_step_btn.font_color = (0, 200, 0)

    def draw_hori_line(self, unit):
        w = unit.grid_w * self.board.scale
        h = unit.grid_h * self.board.scale

        canv = pygame.Surface((w, h - 1))
        canv.fill(self.bg_col)

        pygame.draw.line(canv, self.grey, (0, self.top_line), (w, self.top_line), 3)
        unit.painting = canv.copy()
        unit.update_me = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if not self.show_msg:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                self.next_step()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.board.active_ship == self.next_step_btn.unit_id:
                    if self.cursor_pos == self.sumn1n2sl + 1:
                        self.level.next_board_load()
                    else:
                        self.next_step()

    def home_sqare_switch(self, activate):
        if activate < 0 or activate > self.activable_count:
            activate = self.activable_count - self.sumn1n2sl

        if activate >= 0 and activate < self.activable_count:
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

    def next_step(self):
        self.ship_id = 0
        if 0 <= self.cursor_pos < self.sumn1n2sl + 1:
            self.hint1.value = ""
            comp = ""
            result = 0
            self.home_sqare_switch(self.cursor_pos + ((self.n1sl - 1) * 2 - 1))
            if self.carry1l[self.cursor_pos - 2].value == "1":
                first_val = int(self.n1sh[0 - self.cursor_pos]) - 1
            else:
                first_val = int(self.n1sh[0 - self.cursor_pos])

            if first_val < int(self.n2sh[0 - self.cursor_pos]):
                if self.carry1l[self.cursor_pos - 2].value == "1":
                    comp = "%s - 1 < %s" % (self.n1sh[0 - self.cursor_pos], self.n2sh[0 - self.cursor_pos])
                else:
                    comp = "%s < %s" % (self.n1sh[0 - self.cursor_pos], self.n2sh[0 - self.cursor_pos])
                self.hint3.value = [comp, self.lang.d["borrow 10"]]
                self.hint1.value = "10 + "
                result = 10
                self.carry10l[self.cursor_pos - 1].value = "10"
                self.carry10l[self.cursor_pos - 1].update_me = True
                self.carry1l[self.cursor_pos - 1].value = "1"
                self.carry1l[self.cursor_pos - 1].update_me = True
                self.carry10l[self.cursor_pos - 1].set_outline(self.hint3_fcol, 3)
                self.carry10l[self.cursor_pos - 1].font_color = self.hint3_fcol
            else:
                self.hint3.value = ""
            if self.cursor_pos == self.sumn1n2sl:
                self.next_step_btn.value = self.lang.d["demo next eg"]
                self.next_step_btn.update_me = True
            elif self.cursor_pos == 1:
                self.next_step_btn.value = self.lang.d["demo next step"]
                self.next_step_btn.update_me = True
            if self.cursor_pos >= 1 and self.cursor_pos <= self.sumn1n2sl:

                self.carry10l[self.cursor_pos - 2].set_outline(self.grey, 2)
                if self.cursor_pos > 1 and self.cursor_pos <= self.sumn1n2sl:
                    self.carry1l[self.cursor_pos - 3].set_outline(self.grey, 2)

            if first_val >= int(self.n2sh[0 - self.cursor_pos]):
                result = result + int(self.n1sh[0 - self.cursor_pos]) - int(self.n2sh[0 - self.cursor_pos])
            else:
                result = result + int(self.n1sh[0 - self.cursor_pos]) - int(self.n2sh[0 - self.cursor_pos])
            if self.cursor_pos <= self.sumn1n2sl:
                self.hint1.value += self.n1sh[0 - self.cursor_pos]
            if self.cursor_pos > 1 and self.cursor_pos <= self.sumn1n2sl:

                self.carry1l[self.cursor_pos - 2].set_outline(self.grey, 2)
                if self.carry1l[self.cursor_pos - 2].value == "1":
                    self.hint1.value += " - 1"  # self.carry1l[self.cursor_pos-2].value
                    self.carry1l[self.cursor_pos - 2].set_outline(self.font_hl, 3)
                    result -= 1
            if self.cursor_pos <= self.n2sl:
                self.hint1.value += " - " + self.n2sh[0 - self.cursor_pos]

            self.hint1.value += " = " + str(result)

            # if 1 = 1 don't display
            if len(self.hint1.value) == 5:
                self.hint1.value = ""
            if self.lang.ltr_text:
                if self.hint1.value == "":
                    self.hint2.value = self.lang.d["demo rewrite"] + str(result % 10)
                else:
                    self.hint2.value = self.lang.d["demo write"] + str(result % 10)
            else:
                if self.hint1.value == "":
                    self.hint2.value = str(result % 10) + " " + self.lang.d["demo rewrite"]
                else:
                    self.hint2.value = str(result % 10) + " " + self.lang.d["demo write"]
            self.resultl[self.cursor_pos - 1].value = str(result % 10)
            self.resultl[self.cursor_pos - 1].font_color = self.hint2_fcol
            self.resultl[self.cursor_pos - 1].set_outline(self.hint2_fcol, 3)
            self.resultl[self.cursor_pos - 1].update_me = True

            self.hint1.update_me = True
            self.hint2.update_me = True
            self.hint3.update_me = True

            self.mainloop.redraw_needed[0] = True
            self.cursor_pos += 1

    def deactivate_colors(self):
        for each in self.board.ships:
            each.font_color = self.grey
            each.update_me = True

        for each in self.board.units:
            each.font_color = self.grey
            each.update_me = True

        for each in self.all_nums:
            each.set_outline(self.grey, 2)

    def reactivate_colors(self):
        self.plus_label.font_color = self.font_hl
        self.board.units[0].font_color = self.task_str_color
        if self.home_square in self.carry1l:
            self.carry10l[self.home_square.pos_id].font_color = self.font_hl

        elif self.home_square in self.carry10l:
            self.carry1l[self.home_square.pos_id].font_color = self.font_hl

        elif self.home_square in self.resultl:
            if self.home_square.pos_id > 0:
                self.carry1l[self.home_square.pos_id - 1].font_color = self.font_hl
            if self.home_square.pos_id >= 0 and self.home_square.pos_id < self.sumn1n2sl - 1:
                self.carry10l[self.home_square.pos_id].font_color = self.font_hl
            if (self.n1sl > self.home_square.pos_id):
                self.nums1l[self.home_square.pos_id].font_color = self.font_hl
            if (self.n2sl > self.home_square.pos_id):
                self.nums2l[self.home_square.pos_id].font_color = self.font_hl
            self.resultl[self.home_square.pos_id].font_color = self.font_hl
        self.resultl[self.home_square.pos_id].font_color = self.font_hl
        self.hint1.font_color = self.hint1_fcol
        self.hint2.font_color = self.hint2_fcol
        self.hint3.font_color = self.hint3_fcol
        self.next_step_btn.font_color = self.font_hl

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
