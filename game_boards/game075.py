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
        self.greyoutline = (190, 190, 190)
        self.grey2 = (150, 150, 150)
        self.font_hl = (100, 0, 250)
        self.font_hl2 = (250, 0, 200)
        self.hint1_fcol = (100, 0, 250)
        self.hint2_fcol = (200, 0, 0)
        self.hint3_fcol = (250, 0, 200)

        self.task_str_color = ex.hsv_to_rgb(200, 200, 230)
        self.activated_col = self.font_hl
        white = (255, 255, 255)
        self.white = white
        self.bg_col = white
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.bg_col = (0, 0, 0)
        self.top_line = 3
        rngs = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                     self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        data = [39, 24]
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
        self.n1 = random.randrange(rngs[0], rngs[1])
        self.n2 = random.randrange(rngs[2], rngs[3])
        self.sumn1n2 = self.n1 * self.n2
        self.n1s = str(self.n1)
        self.n2s = str(self.n2)
        self.sumn1n2s = str(self.sumn1n2)
        self.n1sl = len(self.n1s)
        self.n2sl = len(self.n2s)
        self.sumn1n2sl = len(self.sumn1n2s)

        self.cursor_pos = 0
        self.correct = False
        self.carryl = []
        self.carrylall = []
        self.carrysuml = []
        self.semiresultl = []
        self.semiresultlall = []
        self.semiresultlengths = []

        self.resultl = []
        self.all_count = 0
        for i in range(self.n2sl):
            self.carryl.append([])
            self.semiresultl.append([])
            if int(self.n2s[self.n2sl - 1 - i]) == 0:
                self.semiresultlengths.append(self.n1sl)
            else:
                self.semiresultlengths.append(len(str(int(self.n2s[self.n2sl - 1 - i]) * self.n1)))
        self.semi_count = sum(self.semiresultlengths)
        self.nums1l = []
        self.nums2l = []
        self.ship_id = 0
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if self.lang.lang == 'el':
            qm = ";"
        else:
            qm = "?"

        question = self.n1s + " × " + self.n2s + " = " + qm
        # question
        self.board.add_unit(1, 0, data[0] - 1 - self.sumn1n2sl * 3, 3, classes.board.Label, question, self.bg_col, "",
                            21)
        self.board.units[-1].align = 1

        # carry 1
        for i in range(self.n2sl):
            for j in range(self.n1sl):
                self.board.add_unit(data[0] - 5 - j * 3, 2 - i, 1, 1, classes.board.Letter, "", self.bg_col, "", 0)
                self.carryl[i].append(self.board.ships[-1])
                self.carryl[i][-1].set_outline(self.grey, 1)
                self.carryl[i][-1].pos_id = j
                self.carryl[i][-1].posy_id = i
                self.carrylall.append(self.carryl[i][-1])

        # first number
        for i in range(self.n1sl):
            self.board.add_unit(data[0] - 3 - i * 3, 3, 3, 3, classes.board.Label, self.n1s[-(i + 1)], self.bg_col, "",
                                21)
            self.nums1l.append(self.board.units[-1])
            self.nums1l[-1].font_color = self.grey
            self.nums1l[-1].pos_id = i
        # second number
        i = 0
        for i in range(self.n2sl):
            self.board.add_unit(data[0] - 3 - i * 3, 6, 3, 3, classes.board.Label, self.n2s[-(i + 1)], self.bg_col, "",
                                21)
            self.nums2l.append(self.board.units[-1])
            self.nums2l[-1].pos_id = i
        i += 1
        self.board.add_unit(data[0] - 3 - i * 3, 6, 3, 3, classes.board.Label, "×", self.bg_col, "", 21)
        self.plus_label = self.board.units[-1]
        # line
        self.board.add_unit(data[0] - self.sumn1n2sl * 3, 9, self.sumn1n2sl * 3, 1, classes.board.Label, "",
                            self.bg_col, "", 21)
        self.draw_hori_line(self.board.units[-1])
        for i in range(self.sumn1n2sl - 2):
            self.board.add_unit(data[0] - 8 - i * 3, 10, 1, 1, classes.board.Letter, "", self.bg_col, "", 0)
            self.carrysuml.append(self.board.ships[-1])
            self.carrysuml[-1].set_outline(self.grey, 1)
            self.carrysuml[-1].pos_id = i

        for j in range(self.n2sl):
            for i in range(self.semiresultlengths[j]):
                self.board.add_unit(data[0] - 3 - i * 3 - j * 3, 11 + j * 3, 3, 3, classes.board.Letter, "",
                                    self.bg_col, "", 21)
                self.semiresultl[j].append(self.board.ships[-1])
                self.semiresultl[j][-1].set_outline(self.grey, 1)
                self.semiresultl[j][-1].pos_id = i
                self.semiresultl[j][-1].posy_id = j
                self.semiresultlall.append(self.semiresultl[j][-1])

        self.board.add_unit(data[0] - self.sumn1n2sl * 3, 10 + self.n2sl * 3 + 1, self.sumn1n2sl * 3, 1,
                            classes.board.Label, "", self.bg_col, "", 21)
        self.draw_hori_line(self.board.units[-1])
        self.board.add_unit(data[0] - (self.sumn1n2sl + 1) * 3, 7 + self.n2sl * 3 + 1, 3, 3, classes.board.Label, " + ",
                            self.bg_col, "", 21)
        self.plus2_label = self.board.units[-1]
        for i in range(self.sumn1n2sl):
            self.board.add_unit(data[0] - 3 - i * 3, 10 + self.n2sl * 3 + 2, 3, 3, classes.board.Letter, "",
                                self.bg_col, "", 21)
            self.resultl.append(self.board.ships[-1])
            self.resultl[-1].set_outline(self.grey, 1)
            self.resultl[-1].pos_id = i
        self.resultl[0].set_outline(self.activated_col, 1)
        self.home_square = self.semiresultl[0][0]
        self.board.active_ship = self.home_square.unit_id
        self.current_pos = self.home_square.unit_id
        self.first_step_taken = False
        self.all_count = sum(self.semiresultlengths) + self.n1sl + self.n2sl + self.sumn1n2sl * 2 - 2 + (
                                                                                                        self.sumn1n2sl - 1) * self.n2sl
        self.all_a_count = len(self.board.ships)  # self.all_count - self.n1sl - self.n2sl

        self.board.add_unit(0, 5, data[0] - self.sumn1n2sl * 3 - 3, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint1 = self.board.units[-1]
        self.hint1.align = 1

        self.board.add_unit(0, 9, data[0] - self.sumn1n2sl * 3 - 3, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint2 = self.board.units[-1]
        self.hint2.align = 1

        self.board.add_unit(0, 7, data[0] - self.sumn1n2sl * 3 - 6, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint3 = self.board.units[-1]
        self.hint3.align = 1

        self.board.add_unit(0, 15, data[0] - self.sumn1n2sl * 3 - 6, 2, classes.board.Letter, self.lang.d["demo start"],
                            self.bg_col, "", 22)
        self.next_step_btn = self.board.ships[-1]
        self.next_step_btn.readable = False
        for each in self.board.ships:
            each.immobilize()

        self.deactivate_colors()
        self.board.units[0].font_color = self.task_str_color
        self.next_step_btn.font_color = (0, 200, 0)
        self.next_step_btn.set_outline(self.bg_col, 1)

    def next_step(self):
        self.next_step_btn.value = self.lang.d["demo next step"]
        self.home_sqare_switch(self.current_pos)
        self.current_pos += 1
        if self.current_pos + 1 > self.all_a_count:
            self.next_step_btn.value = self.lang.d["demo next eg"]

        self.next_step_btn.update_me == True

    def draw_hori_line(self, unit):
        w = unit.grid_w * self.board.scale
        h = unit.grid_h * self.board.scale
        center = [w // 2, h // 2]

        canv = pygame.Surface([w, h - 1])
        canv.fill(self.bg_col)

        pygame.draw.line(canv, self.grey, (0, self.top_line), (w, self.top_line), 3)
        unit.painting = canv.copy()
        unit.update_me = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.show_msg == False:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                self.next_step()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.board.active_ship == self.next_step_btn.unit_id:
                    if self.current_pos + 1 > self.all_a_count:  # if self.cursor_pos == self.sumn1n2sl+1:
                        self.level.next_board_load()
                    else:
                        self.next_step()

    def home_sqare_switch(self, activate):
        if activate < 0 or activate > self.all_a_count:  # self.sumn1n2sl * 2 - 1:
            activate = self.all_a_count

        if activate >= 0 and activate < self.all_a_count:  # self.sumn1n2sl * 2 - 1:
            self.board.active_ship = activate
            self.home_square.update_me = True
            if self.board.active_ship >= 0:
                self.home_square.set_outline(self.grey, 1)
                self.deactivate_colors()
                self.home_square = self.board.ships[self.board.active_ship]
                self.home_square.set_outline(self.activated_col, 2)
                self.reactivate_colors()
                self.home_square.font_color = self.font_hl
            self.home_square.update_me = True
            self.mainloop.redraw_needed[0] = True

    def deactivate_colors(self):
        for each in self.board.ships:
            each.font_color = self.grey
            each.set_outline(self.greyoutline, 1)
            each.update_me = True

        for each in self.board.units:
            each.font_color = self.grey
            each.update_me = True
        self.next_step_btn.perm_outline_color = (255, 255, 255)

    def reactivate_colors(self):
        self.plus_label.font_color = self.font_hl
        self.board.units[0].font_color = self.task_str_color
        if self.home_square in self.carrylall:
            self.nums1l[self.home_square.pos_id].font_color = self.font_hl
            self.nums2l[self.home_square.posy_id].font_color = self.font_hl
            self.semiresultl[self.home_square.posy_id][self.home_square.pos_id].font_color = self.font_hl
            self.semiresultl[self.home_square.posy_id][self.home_square.pos_id].set_outline(self.font_hl2, 2)
            if self.home_square.pos_id + 1 < self.semiresultlengths[self.home_square.posy_id]:
                self.semiresultl[self.home_square.posy_id][self.home_square.pos_id + 1].font_color = self.grey2
                self.semiresultl[self.home_square.posy_id][self.home_square.pos_id + 1].set_outline(self.grey2, 2)
        elif self.home_square in self.semiresultlall:
            if self.home_square.pos_id < self.n1sl:
                self.nums1l[self.home_square.pos_id].font_color = self.font_hl
                self.nums2l[self.home_square.posy_id].font_color = self.font_hl
            if self.home_square.pos_id > 0:  # self.n1sl:
                self.carryl[self.home_square.posy_id][self.home_square.pos_id - 1].font_color = self.font_hl
                self.carryl[self.home_square.posy_id][self.home_square.pos_id - 1].set_outline(self.grey2, 2)
            if self.home_square.pos_id < self.n1sl:
                self.semiresultl[self.home_square.posy_id][self.home_square.pos_id].font_color = self.grey2
                self.carryl[self.home_square.posy_id][self.home_square.pos_id].set_outline(self.font_hl2, 2)
        elif self.home_square in self.resultl:
            for i in range(self.n2sl):
                if self.semiresultlengths[i] > self.home_square.pos_id - i >= 0:
                    self.semiresultl[i][self.home_square.pos_id - i].font_color = self.font_hl
                    self.semiresultl[i][self.home_square.pos_id - i].set_outline(self.grey2, 2)
            if self.home_square.pos_id > 1:
                self.carrysuml[self.home_square.pos_id - 2].font_color = self.font_hl
                self.carrysuml[self.home_square.pos_id - 2].set_outline(self.grey2, 2)
            if self.home_square.pos_id > 0 and self.home_square.pos_id < self.sumn1n2sl - 1:
                self.carrysuml[self.home_square.pos_id - 1].font_color = self.grey2
                self.carrysuml[self.home_square.pos_id - 1].set_outline(self.font_hl2, 2)
            self.plus_label.font_color = self.grey
            self.plus2_label.font_color = self.font_hl

        elif self.home_square in self.carrysuml:
            for i in range(self.n2sl):
                if self.semiresultlengths[i] > self.home_square.pos_id - i + 1 >= 0:
                    self.semiresultl[i][self.home_square.pos_id - i + 1].font_color = self.font_hl
                    self.semiresultl[i][self.home_square.pos_id - i + 1].set_outline(self.grey2, 2)
            self.resultl[self.home_square.pos_id + 1].font_color = self.font_hl
            self.resultl[self.home_square.pos_id + 1].set_outline(self.grey2, 2)
            self.plus_label.font_color = self.grey
            self.plus2_label.font_color = self.font_hl
        self.hint1.font_color = self.hint1_fcol
        self.hint2.font_color = self.hint2_fcol
        self.hint3.font_color = self.hint3_fcol
        self.next_step_btn.font_color = self.font_hl
        self.next_step_btn.set_outline(self.bg_col, 1)
        self.auto_fill()

    def auto_fill(self):
        self.plus_label.font_color = self.font_hl
        self.board.units[0].font_color = self.task_str_color
        s = "0"
        self.hint1.value = ""
        self.hint2.value = ""
        self.hint3.value = ""
        val = 0
        if self.home_square in self.semiresultlall:

            if self.home_square.pos_id < self.n1sl:
                self.nums1l[self.home_square.pos_id].font_color = self.font_hl
                self.nums2l[self.home_square.posy_id].font_color = self.font_hl
                val = (
                int(self.nums1l[self.home_square.pos_id].value) * int(self.nums2l[self.home_square.posy_id].value))
                self.hint1.value = self.nums2l[self.home_square.posy_id].value + " × " + self.nums1l[
                    self.home_square.pos_id].value
            if self.home_square.pos_id > 0:  # self.n1sl:
                self.carryl[self.home_square.posy_id][self.home_square.pos_id - 1].font_color = self.font_hl
                self.carryl[self.home_square.posy_id][self.home_square.pos_id - 1].set_outline(self.grey2, 2)
                s = self.carryl[self.home_square.posy_id][self.home_square.pos_id - 1].value
                if s == "":
                    s = "0"
                else:
                    if self.hint1.value != "":
                        self.hint1.value += " + %s" % s

                val += int(s)

            if self.home_square.pos_id < self.n1sl:
                self.semiresultl[self.home_square.posy_id][self.home_square.pos_id].font_color = self.grey2
                self.carryl[self.home_square.posy_id][self.home_square.pos_id].set_outline(self.font_hl2, 2)
                if val / 10 > 0:
                    self.carryl[self.home_square.posy_id][self.home_square.pos_id].value = str(val / 10)
                    if self.lang.ltr_text:
                        self.hint3.value = "%s %s" % (self.lang.d["carry"], str(val / 10))
                    else:
                        self.hint3.value = "%s %s" % (str(val / 10), self.lang.d["carry"])

            if self.hint1.value != "":
                self.hint1.value += " = %d" % val
            self.home_square.value = str(val % 10)
            if self.lang.ltr_text:
                if self.hint1.value == "":
                    self.hint2.value = "%s %s" % (self.lang.d["demo rewrite"], str(val % 10))
                else:
                    self.hint2.value = "%s %s" % (self.lang.d["demo write"], str(val % 10))
            else:
                if self.hint1.value == "":
                    self.hint2.value = "%s %s" % (str(val % 10), self.lang.d["demo rewrite"])
                else:
                    self.hint2.value = "%s %s" % (str(val % 10), self.lang.d["demo write"])
        elif self.home_square in self.resultl:
            if self.home_square.pos_id > 1:
                self.carrysuml[self.home_square.pos_id - 2].font_color = self.font_hl
                self.carrysuml[self.home_square.pos_id - 2].set_outline(self.grey2, 2)
                if self.carrysuml[self.home_square.pos_id - 2].value != "":
                    if self.hint1.value != "":
                        self.hint1.value += " + "
                    self.hint1.value += self.carrysuml[self.home_square.pos_id - 2].value
                    val += int(self.carrysuml[self.home_square.pos_id - 2].value)
            for i in range(self.n2sl):
                if self.semiresultlengths[i] > self.home_square.pos_id - i >= 0:
                    self.semiresultl[i][self.home_square.pos_id - i].font_color = self.font_hl
                    self.semiresultl[i][self.home_square.pos_id - i].set_outline(self.grey2, 2)
                    if self.semiresultl[i][self.home_square.pos_id - i].value != "":
                        if self.hint1.value != "":
                            self.hint1.value += " + "
                        self.hint1.value += self.semiresultl[i][self.home_square.pos_id - i].value
                        val += int(self.semiresultl[i][self.home_square.pos_id - i].value)
            if self.hint1.value != "":
                self.hint1.value += " = %s" % val
            self.home_square.value = str(val % 10)
            if self.home_square.pos_id > 0 and self.home_square.pos_id < self.sumn1n2sl - 1:
                self.carrysuml[self.home_square.pos_id - 1].font_color = self.grey2
                self.carrysuml[self.home_square.pos_id - 1].set_outline(self.font_hl2, 2)
                if val / 10 > 0:
                    self.carrysuml[self.home_square.pos_id - 1].value = str(val / 10)
                    if self.lang.ltr_text:
                        self.hint3.value = "%s %s" % (self.lang.d["carry"], str(val / 10))
                    else:
                        self.hint3.value = "%s %s" % (str(val / 10), self.lang.d["carry"])
            # if hint1 is something like 1 = 1, don't show it
            if len(self.hint1.value) < 6:
                self.hint1.value = ""
            if self.lang.ltr_text:
                if self.hint1.value == "":
                    self.hint2.value = "%s %s" % (self.lang.d["demo rewrite"], str(val % 10))
                else:
                    self.hint2.value = "%s %s" % (self.lang.d["demo write"], str(val % 10))
            else:
                if self.hint1.value == "":
                    self.hint2.value = "%s %s" % (str(val % 10), self.lang.d["demo rewrite"])
                else:
                    self.hint2.value = "%s %s" % (str(val % 10), self.lang.d["demo write"])
            self.plus_label.font_color = self.grey
            self.plus2_label.font_color = self.font_hl

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
