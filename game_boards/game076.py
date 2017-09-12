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
        self.font_hl = (100, 0, 250)
        self.font_hl2 = (250, 0, 200)
        self.font_hl3 = (200, 0, 250)
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
        rngs = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                     self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        if self.lang.lang == 'pl':
            self.divisor_pos = 1
        else:
            self.divisor_pos = 0

        data = [39, 25]
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

        self.top_line = self.board.scale // 2

        if self.lang.ltr_text:
            self.div_sign = "÷"
        else:
            self.div_sign = "/"
        nr1 = random.randrange(rngs[0], rngs[1])
        nr2 = random.randrange(rngs[2], rngs[3])
        self.n1 = nr1 * nr2
        self.n2 = nr1
        self.sumn1n2 = nr2  # self.n1+self.n2
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
        self.up_count = 0
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if self.divisor_pos == 0:
            r_offset = 0
            d_offset = 0
            ds_offset = 0
            d_str = "¥"
            d_h = 3
            num2_align = 2

        else:
            r_offset = 4
            d_offset = self.n1sl * 2 + 1
            ds_offset = self.n1sl * 2 - 3
            d_str = self.div_sign
            d_h = 4
            num2_align = 1

        if self.lang.lang == 'el':
            qm = ";"
        else:
            qm = "?"

        question = self.n1s + " " + self.div_sign + " " + self.n2s + " = " + qm
        # question
        self.board.add_unit(1, 0, data[0] - 1 - self.sumn1n2sl * 2 - 1 - self.n1sl * 2, 2, classes.board.Label,
                            question, self.bg_col, "", 21)
        self.board.units[-1].align = 1
        self.question = self.board.units[-1]
        j = 0
        xs = self.data[0] - self.n1sl * 2
        # first number
        for i in range(self.n1sl):
            self.board.add_unit(xs + i * 2 - r_offset, 3, 2, 2, classes.board.Label, self.n1s[i], self.bg_col, "", 21)
            self.nums1l.append(self.board.units[-1])
            self.nums1l[-1].font_color = self.grey
            self.nums1l[-1].pos_id = i
            j += 1

            # second number

        self.board.add_unit(data[0] - 4 - j * 2 + d_offset, 3, 3, 2, classes.board.Label, self.n2s, self.bg_col, "", 21)
        self.num2 = self.board.units[-1]
        self.num2.align = num2_align

        self.board.add_unit(data[0] - self.n1sl * 2 - r_offset, 2, self.n1sl * 2, 1, classes.board.Label, "",
                            self.bg_col, "", 21)
        self.line_unit = self.board.units[-1]
        self.draw_hori_line(self.line_unit)

        if self.divisor_pos == 0:
            self.board.add_unit(data[0] - self.n1sl * 2 - 1 + ds_offset, 2, 1, d_h, classes.board.Label, "",
                                self.bg_col, "", 21)
            self.vert_line = self.board.units[-1]
            self.draw_vert_line(self.vert_line)
        else:
            self.board.add_unit(data[0] - self.n1sl * 2 - 1 + ds_offset, 2, 1, d_h, classes.board.Label, d_str,
                                self.bg_col, "", 21)

        self.division_sign = self.board.units[-1]

        self.resl = []
        self.nbel = []
        self.mpll = []
        self.subl = []
        self.minl = []  # to store minus signs

        res = [0 for i in range(self.n1sl)]
        nbr = [0 for i in range(self.n1sl)]
        nbe = [0 for i in range(self.n1sl)]
        mpl = [0 for i in range(self.n1sl)]
        sub = [0 for i in range(self.n1sl)]
        # [res,nbr,mpl,sub,line]
        yp = [0, 3, 5, 8, 7]

        xp = [xs, xs, xs + 2, xs + 2, xs]
        self.activables = 0
        for i in range(self.n1sl):
            if i > 0:
                nbr[i] = sub[i - 1] * 10 + int(self.n1s[i])
                nbe[i] = int(self.n1s[i])
                self.board.add_unit(xp[1] - r_offset, yp[1], 2, 2, classes.board.Letter, "", self.bg_col, "",
                                    21)
                self.nbel.append(self.board.ships[-1])
                self.nbel[-1].pos_id = i
                self.activables += 1
            elif i == 0:
                nbr[i] = int(self.n1s[i])
                nbe[i] = int(self.n1s[i])
            res[i] = nbr[i] / self.n2
            self.board.add_unit(xp[0] - r_offset, yp[0], 2, 2, classes.board.Letter, "", self.bg_col, "",
                                21)
            self.resl.append(self.board.ships[-1])
            self.resl[-1].pos_id = i
            self.activables += 1

            mpl[i] = self.n2 * res[i]
            mpls = str(mpl[i])
            mplsl = len(mpls)
            self.board.add_unit(xp[2] - mplsl * 2 - 2 - r_offset, yp[2], 2, 2, classes.board.Label, "-", self.bg_col,
                                "", 21)
            self.minl.append(self.board.units[-1])
            self.mpll.append([])
            for j in range(mplsl):
                self.board.add_unit(xp[2] - mplsl * 2 + j * 2 - r_offset, yp[2], 2, 2, classes.board.Letter, "",
                                    self.bg_col, "", 21)
                self.mpll[i].append(self.board.ships[-1])
                self.mpll[i][-1].pos_id = i
                self.mpll[i][-1].posy_id = j
                self.activables += 1
            sub[i] = nbr[i] - mpl[i]
            subs = str(sub[i])
            subsl = len(subs)
            self.subl.append([])
            for j in range(subsl):
                self.board.add_unit(xp[3] - subsl * 2 + j * 2 - r_offset, yp[3], 2, 2, classes.board.Letter, "",
                                    self.bg_col, "", 21)
                self.subl[i].append(self.board.ships[-1])
                self.subl[i][-1].pos_id = i
                self.subl[i][-1].posy_id = j
                self.activables += 1

            self.board.add_unit(xp[4] + (2 - len(str(nbr[i])) * 2) - r_offset, yp[4], len(str(nbr[i])) * 2, 1,
                                classes.board.Label, "", self.bg_col, "", 21)
            self.draw_hori_line(self.board.units[-1])
            for i in range(5):
                xp[i] += 2
                if i > 0:
                    yp[i] += 5

        hint_offset = len(self.resl) * 2 + 6
        self.board.add_unit(0, 5, data[0] - hint_offset, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint1 = self.board.units[-1]
        self.hint1.align = 1

        self.board.add_unit(0, 7, data[0] - hint_offset, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint2 = self.board.units[-1]
        self.hint2.align = 1

        self.board.add_unit(0, 9, data[0] - hint_offset, 2, classes.board.Label, "", self.bg_col, "", 22)
        self.hint3 = self.board.units[-1]
        self.hint3.align = 1

        self.board.add_unit(0, 15, data[0] - hint_offset, 2, classes.board.Letter, self.lang.d["demo start"],
                            self.bg_col, "", 22)
        self.next_step_btn = self.board.ships[-1]
        self.next_step_btn.readable = False
        self.all_a_count = len(self.board.ships) - 1

        self.home_square = self.board.ships[0]
        self.board.active_ship = self.home_square.unit_id
        self.current_pos = self.home_square.unit_id

        for each in self.board.ships:
            each.immobilize()

        self.res = res
        self.nbr = nbr
        self.nbe = nbe
        self.mpl = mpl
        self.sub = sub
        self.sub_len = len(sub)
        self.deactivate_colors()
        self.board.units[0].font_color = self.task_str_color
        self.next_step_btn.font_color = (0, 200, 0)
        self.next_step_btn.set_outline(self.bg_col, 1)

    def draw_vert_line(self, unit):
        w = unit.grid_w * self.board.scale
        h = unit.grid_h * self.board.scale
        center = [w // 2, h // 2]

        canv = pygame.Surface([w, h - 1])
        canv.fill(self.bg_col)

        pygame.draw.line(canv, self.grey, (center[0], self.top_line), (center[0], h - self.top_line), 3)
        pygame.draw.line(canv, self.grey, (center[0] - 1, self.top_line), (w, self.top_line), 3)

        unit.painting = canv.copy()
        unit.update_me = True

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
                    if self.current_pos + 1 > self.all_a_count:
                        self.level.next_board_load()
                    else:
                        self.next_step()

    def next_step(self):
        self.next_step_btn.value = self.lang.d["demo next step"]
        self.home_sqare_switch(self.current_pos)
        self.current_pos += 1
        if self.current_pos + 1 > self.all_a_count:
            self.next_step_btn.value = self.lang.d["demo next eg"]

        self.next_step_btn.update_me = True

    def home_sqare_switch(self, activate):

        if activate >= 0 and activate < self.activables:
            self.board.active_ship = activate
            self.home_square.update_me = True
            if self.board.active_ship >= 0:
                self.home_square.set_outline(self.grey, 2)
                self.deactivate_colors()
                self.home_square = self.board.ships[self.board.active_ship]
                self.home_square.set_outline(self.activated_col, 2)
                self.reactivate_colors()
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

    def reactivate_colors(self):
        self.board.units[0].font_color = self.task_str_color
        if self.home_square in self.resl:
            if self.home_square.pos_id == 0:
                self.nums1l[0].font_color = self.font_hl3
            else:
                for each in self.subl[self.home_square.pos_id - 1]:
                    each.font_color = self.font_hl3
                    each.set_outline(self.font_hl3, 1)
                self.nbel[self.home_square.pos_id - 1].font_color = self.font_hl3
                self.nbel[self.home_square.pos_id - 1].set_outline(self.font_hl3, 1)
            self.num2.font_color = self.font_hl2
            if self.divisor_pos == 1:
                self.division_sign.font_color = self.font_hl2
        elif self.home_square in self.nbel:
            self.nums1l[self.home_square.pos_id].font_color = self.font_hl3
        else:
            f = False
            for each in self.mpll:
                for e in each:
                    if self.home_square == e:
                        f = True
                        # it's in this sublist - now highlight entire sublist
                        for e2 in each:
                            e2.font_color = self.font_hl
                            e2.set_outline(self.font_hl2, 1)
                        # highlight multiplied numbers
                        self.num2.font_color = self.font_hl2
                        self.resl[self.home_square.pos_id].font_color = self.font_hl3
                        self.resl[self.home_square.pos_id].set_outline(self.font_hl3, 1)
                        break
            if not f:
                for each in self.subl:
                    for e in each:
                        if self.home_square == e:
                            for e2 in each:
                                e2.font_color = self.font_hl
                                e2.set_outline(self.font_hl2, 1)
                            if self.home_square.pos_id == 0:
                                self.nums1l[0].font_color = self.font_hl3
                                self.mpll[0][0].font_color = self.font_hl2
                                self.mpll[0][0].set_outline(self.font_hl2, 1)
                            else:
                                # highlight all previous subtract + dropped number
                                for e2 in self.subl[self.home_square.pos_id - 1]:
                                    e2.font_color = self.font_hl3
                                    e2.set_outline(self.font_hl3, 1)
                                self.nbel[self.home_square.pos_id - 1].font_color = self.font_hl3
                                self.nbel[self.home_square.pos_id - 1].set_outline(self.font_hl3, 1)
                                # highlight previous multiplication result
                                for e2 in self.mpll[self.home_square.pos_id]:
                                    e2.font_color = self.font_hl2
                                    e2.set_outline(self.font_hl2, 1)
                            self.minl[self.home_square.pos_id].font_color = self.font_hl3
                            break

        self.hint1.font_color = self.hint1_fcol
        self.hint2.font_color = self.hint2_fcol
        self.hint3.font_color = self.hint3_fcol
        self.next_step_btn.font_color = self.font_hl
        self.auto_fill()
        self.home_square.set_outline(self.hint2_fcol, 3)
        self.home_square.font_color = self.hint2_fcol
        self.next_step_btn.set_outline(self.bg_col, 1)

    def auto_fill(self):
        self.board.units[0].font_color = self.task_str_color
        s = "0"
        self.hint1.value = ""
        self.hint2.value = ""
        self.hint3.value = ""
        multiplication_string = ""
        val = 0
        self.board.units[0].font_color = self.task_str_color
        if self.home_square in self.resl:
            if self.home_square.pos_id == 0:
                rem = ""
                if self.sub[self.home_square.pos_id] > 0:
                    if self.lang.ltr_text:
                        rem = "(%s %d)" % (self.lang.d["remainder"], self.sub[self.home_square.pos_id])
                    else:
                        rem = "(%d %s)" % (self.sub[self.home_square.pos_id], self.lang.d["remainder"])
                self.hint1.value = "%s %s %s = %s %s" % (
                self.nums1l[0].value, self.div_sign, self.num2.value, str(self.res[0]), rem)

            else:
                rem = ""
                if self.home_square.pos_id < self.sub_len - 1:
                    if self.sub[self.home_square.pos_id] > 0:
                        if self.lang.ltr_text:
                            rem = "(%s %d)" % (self.lang.d["remainder"], self.sub[self.home_square.pos_id])
                        else:
                            rem = "(%d %s)" % (self.sub[self.home_square.pos_id], self.lang.d["remainder"])
                self.hint1.value = "%d %s %s = %d %s" % (
                self.nbr[self.home_square.pos_id], self.div_sign, self.num2.value, self.res[self.home_square.pos_id],
                rem)
            if self.lang.ltr_text:
                self.hint2.value = "%s %s" % (self.lang.d["demo write"], self.res[self.home_square.pos_id])
            else:
                self.hint2.value = "%s %s" % (self.res[self.home_square.pos_id], self.lang.d["demo write"])
            self.resl[self.home_square.pos_id].value = str(self.res[self.home_square.pos_id])
        elif self.home_square in self.nbel:
            if self.lang.ltr_text:
                self.hint2.value = "%s %s" % (self.lang.d["demo rewrite"], self.nums1l[self.home_square.pos_id].value)
            else:
                self.hint2.value = "%s %s" % (self.nums1l[self.home_square.pos_id].value, self.lang.d["demo rewrite"],)

            self.nbel[self.home_square.pos_id - 1].value = str(self.nbe[self.home_square.pos_id])
        else:
            f = False
            for each in self.mpll:
                for e in each:
                    if self.home_square == e:
                        f = True
                        break
            if not f:  # sub
                self.hint1.value = "%d - %d = %d" % (
                self.nbr[self.home_square.pos_id], self.mpl[self.home_square.pos_id], self.sub[self.home_square.pos_id])
                n = str(self.sub[self.home_square.pos_id])[self.home_square.posy_id]
                self.subl[self.home_square.pos_id][self.home_square.posy_id].value = n
                if self.lang.ltr_text:
                    self.hint2.value = "%s %s" % (self.lang.d["demo write"], n)
                else:
                    self.hint2.value = "%s %s" % (n, self.lang.d["demo write"])
                if self.home_square.pos_id == self.sub_len - 1:
                    if self.lang.ltr_text:
                        self.hint3.value = "%s: %d" % (self.lang.d["demo_result"], self.sumn1n2)
                    else:
                        self.hint3.value = "%d :%s" % (self.sumn1n2, self.lang.d["demo_result"])

                    self.question.value = "%s %s %s = %d" % (self.n1s, self.div_sign, self.n2s, self.sumn1n2)
                    for each in self.resl:
                        each.set_outline(self.bg_col, 1)
                        each.font_color = self.hint3_fcol

            else:  # multi
                self.hint1.value = "%d %s %s = %d" % (
                self.res[self.home_square.pos_id], "×", self.num2.value, self.mpl[self.home_square.pos_id])
                n = str(self.mpl[self.home_square.pos_id])[self.home_square.posy_id]
                self.mpll[self.home_square.pos_id][self.home_square.posy_id].value = n
                if self.lang.ltr_text:
                    self.hint2.value = "%s %s" % (self.lang.d["demo write"], n)
                else:
                    self.hint2.value = "%s %s" % (n, self.lang.d["demo write"])

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
