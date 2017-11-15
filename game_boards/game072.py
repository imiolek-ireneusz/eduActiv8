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

        self.task_str_color = ex.hsv_to_rgb(200, 200, 230)
        self.activated_col = self.font_hl
        white = (255, 255, 255)
        self.white = white
        self.bg_col = white
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.bg_col = (0, 0, 0)

        self.auto_select = True
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

        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.top_line = self.board.scale // 2
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
            d_str = "÷"
            d_h = 4
            num2_align = 1

        if self.lang.lang == 'el':
            qm = ";"
        else:
            qm = "?"
        question = self.n1s + " ÷ " + self.n2s + " = " + qm
        # question
        self.board.add_unit(1, 0, data[0] - 1 - self.sumn1n2sl * 2 - 1 - self.n1sl * 2, 2, classes.board.Label,
                            question, self.bg_col, "", 21)
        self.board.units[-1].align = 1
        j = 0
        xs = self.data[0] - self.n1sl * 2
        # first number
        for i in range(self.n1sl):
            self.board.add_unit(xs + i * 2 - r_offset, 3, 2, 2, classes.board.Label, self.n1s[i], self.bg_col, "", 21)
            self.nums1l.append(self.board.units[-1])
            self.nums1l[-1].font_color = self.grey
            self.nums1l[-1].pos_id = i
            j += 1

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
                self.board.add_unit(xp[1] - r_offset, yp[1], 2, 2, classes.board.Letter, "", self.bg_col, "", 21)
                self.nbel.append(self.board.ships[-1])
                self.nbel[-1].checkable = True
                self.nbel[-1].init_check_images()
                self.nbel[-1].pos_id = i
                self.activables += 1
            elif i == 0:
                nbr[i] = int(self.n1s[i])
                nbe[i] = int(self.n1s[i])
            res[i] = nbr[i] / self.n2
            self.board.add_unit(xp[0] - r_offset, yp[0], 2, 2, classes.board.Letter, "", self.bg_col, "", 21)
            self.resl.append(self.board.ships[-1])
            self.resl[-1].pos_id = i
            self.resl[-1].checkable = True
            self.resl[-1].init_check_images()
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
                self.mpll[i][-1].checkable = True
                self.mpll[i][-1].init_check_images()
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
                self.subl[i][-1].checkable = True
                self.subl[i][-1].init_check_images()
                self.activables += 1

            self.board.add_unit(xp[4] + (2 - len(str(nbr[i])) * 2) - r_offset, yp[4], len(str(nbr[i])) * 2, 1,
                                classes.board.Label, "", self.bg_col, "", 21)
            self.draw_hori_line(self.board.units[-1])
            for i in range(5):
                xp[i] += 2
                if i > 0:
                    yp[i] += 5
            self.home_square = self.board.ships[0]
            self.board.active_ship = self.home_square.unit_id

        for each in self.board.ships:
            each.immobilize()

        self.deactivate_colors()
        self.reactivate_colors()

        self.nbr = nbr
        self.nbe = nbe
        self.res = res
        self.mpl = mpl
        self.sub = sub

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
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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
                        self.home_square.value = char
                        if self.auto_select:
                            self.home_sqare_switch(self.board.active_ship + 1)
                    else:
                        self.home_square.value = ""

                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.home_sqare_switch(self.board.active_ship)

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
                            # highlight subtracted numbers
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

        self.home_square.set_outline(self.font_hl, 3)
        self.home_square.font_color = self.font_hl

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check_reset(self):
        for i in range(len(self.mpll)):
            for each in self.mpll[i]:
                each.set_display_check(None)
        for i in range(len(self.subl)):
            for each in self.subl[i]:
                each.set_display_check(None)
        for each in self.nbel:
            each.set_display_check(None)
        for each in self.resl:
            each.set_display_check(None)

    def check_result(self):
        correct = True
        for i in range(len(self.mpll)):
            for j in range(len(self.mpll[i])):
                if self.mpll[i][j].value == str(self.mpl[i])[j]:
                    self.mpll[i][j].set_display_check(True)
                else:
                    self.mpll[i][j].set_display_check(False)
                    correct = False

        for i in range(len(self.nbel)):
            if self.nbel[i].value == str(self.nbe[i+1]):
                self.nbel[i].set_display_check(True)
            else:
                self.nbel[i].set_display_check(False)
                correct = False

        for i in range(len(self.subl)):
            for j in range(len(self.subl[i])):
                if self.subl[i][j].value == str(self.sub[i])[j]:
                    self.subl[i][j].set_display_check(True)
                else:
                    self.subl[i][j].set_display_check(False)
                    correct = False

        for i in range(len(self.resl)):
            if self.resl[i].value == str(self.res[i]):
                self.resl[i].set_display_check(True)
            else:
                self.resl[i].set_display_check(False)
                correct = False

        s = ""
        for each in self.resl:
            s += each.value
        if len(s) > 0:
            if int(s) == self.sumn1n2 and correct:
                self.level.next_board()
