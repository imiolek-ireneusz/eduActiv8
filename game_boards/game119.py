# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.drw.fraction_hq
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex
import classes.universal


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 15, 10)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color
            h1 = 170
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            self.font_color = bd_color1
        else:
            white = (255, 255, 255)
            h1 = 17
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 255, 200)
            self.font_color = ex.hsv_to_rgb(h1, 255, 175)

        self.font_color2 = ex.hsv_to_rgb(5, 255, 240)
        self.font_color3 = ex.hsv_to_rgb(160, 255, 240)
        self.font_color4 = ex.hsv_to_rgb(5, 150, 240)
        self.font_color5 = ex.hsv_to_rgb(160, 150, 240)

        self.font_color6 = ex.hsv_to_rgb(60, 255, 220)
        self.font_color7 = ex.hsv_to_rgb(195, 255, 240)
        self.font_color8 = ex.hsv_to_rgb(60, 150, 220)
        self.font_color9 = ex.hsv_to_rgb(195, 150, 240)

        self.bd_color1 = bd_color1
        transp = (0, 0, 0, 0)
        if self.mainloop.m.game_variant == 0:
            data = [26, 8]
            if self.mainloop.m.game_var2 == 0:
                data[0] = data[0] - 0
        else:
            data = [23, 8]
            if self.mainloop.m.game_var2 == 0:
                data[0] = data[0] - 0

        self.data = data

        self.level_data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid,
                                                               self.mainloop.config.user_age_group,
                                                               self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)
        self.hidden_sim = [False, False]
        self.shift = False

        if self.mainloop.m.game_variant == 0:
            self.sign = "+"
            num3 = random.randint(2, self.level_data[0])
            num4 = num3
            if self.mainloop.m.game_var2 == 1:
                while num4 == num3:
                    num4 = random.randint(2, self.level_data[0])
            num1 = random.randint(1, num3 - 1)
            num2 = random.randint(1, num4 - 1)

        else:
            self.sign = "-"
            sm = 0
            # make sure the numbers are not equal to 0 when subtracting
            while (-0.001 < sm < 0.001):
                num3 = random.randint(2, self.level_data[0])
                num4 = num3
                if self.mainloop.m.game_var2 == 1:
                    while num4 == num3:
                        num4 = random.randint(2, self.level_data[0])
                num1 = random.randint(1, num3 - 1)
                num2 = random.randint(1, num4 - 1)
                sm = float(num1) / num3 - float(num2) / num4

        self.response = [0, 1]
        self.current_txt = ""

        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if self.lang.lang == "gr":
            self.qm = ";"
        else:
            self.qm = "?"

        mainloc = [[0, 2], [0, 4], [3, 2], [3, 4]]
        mainloc2 = [[6, 2], [6, 4], [9, 2], [9, 4]]
        f2_colors = [self.font_color4, self.font_color4, self.font_color5, self.font_color5]
        f2_colors2 = [self.font_color8, self.font_color8, self.font_color9, self.font_color9]

        self.divisors = []
        self.divisors2 = []

        for i in range(4):
            unit1d = classes.universal.Universal(board=self.board, grid_x=mainloc[i][0] + 1, grid_y=mainloc[i][1],
                                                 grid_w=1, grid_h=1, txt="", bg_color=transp, immobilized=True,
                                                 font_colors=(f2_colors[i],), font_type=2,
                                                 txt_align=(2, 1))

            unit2d = classes.universal.Universal(board=self.board, grid_x=mainloc2[i][0] + 1, grid_y=mainloc2[i][1],
                                                 grid_w=1, grid_h=1, txt="", bg_color=transp, immobilized=True,
                                                 font_colors=(f2_colors2[i],), font_type=2,
                                                 txt_align=(2, 1))

            self.divisors.append(unit1d)
            self.board.all_sprites_list.add(unit1d)

            self.divisors2.append(unit2d)
            self.board.all_sprites_list.add(unit2d)

        self.max_num = 143

        # add labels
        self.board.add_unit(0, 2, 2, 2, classes.board.Label, str(num1), white, "", 31)
        self.nm1a = self.board.units[-1]
        self.nm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1)

        self.board.add_unit(0, 4, 2, 2, classes.board.Label, str(num3), white, "", 31)
        self.nm1b = self.board.units[-1]

        self.board.add_unit(2, 3, 1, 2, classes.board.Label, self.sign, white, "", 31)
        self.board.units[-1].font_color = self.font_color

        self.board.add_unit(3, 2, 2, 2, classes.board.Label, str(num2), white, "", 31)
        self.nm2a = self.board.units[-1]
        self.nm2a.set_fraction_lines(top=False, bottom=True, color=bd_color1)

        self.board.add_unit(3, 4, 2, 2, classes.board.Label, str(num4), white, "", 31)
        self.nm2b = self.board.units[-1]

        self.board.add_unit(5, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.eq1 = self.board.units[-1]

        # add labels for simplification

        self.board.add_unit(6, 2, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm1xa = self.board.units[-1]
        self.nm1xa.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=80)

        self.board.add_unit(6, 4, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm1xb = self.board.units[-1]

        self.board.add_unit(8, 3, 1, 2, classes.board.Label, self.sign, white, "", 31)
        self.pl1 = self.board.units[-1]

        self.board.add_unit(9, 2, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm2xa = self.board.units[-1]
        self.nm2xa.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=80)

        self.board.add_unit(9, 4, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm2xb = self.board.units[-1]

        # add labels for calculation with common denominators
        self.board.add_unit(11, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.eq2 = self.board.units[-1]

        self.board.add_unit(12, 2, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm1xa2 = self.board.units[-1]
        self.nm1xa2.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=80)

        self.board.add_unit(12, 4, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm1xb2 = self.board.units[-1]

        self.board.add_unit(14, 3, 1, 2, classes.board.Label, self.sign, white, "", 31)
        self.pl2 = self.board.units[-1]

        self.board.add_unit(15, 2, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm2xa2 = self.board.units[-1]
        self.nm2xa2.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=80)

        self.board.add_unit(15, 4, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm2xb2 = self.board.units[-1]

        # final calculation
        self.board.add_unit(17, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.eq3 = self.board.units[-1]
        self.board.add_unit(18, 2, 2, 2, classes.board.Label, self.qm, white, "", 31)
        self.sm1a = self.board.units[-1]

        self.sm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=80)
        self.sm1a.set_outline(color=self.font_color, width=1)
        self.sm1a.checkable = True
        self.sm1a.font_color = self.font_color
        self.sm1a.init_check_images()

        self.board.add_unit(18, 4, 2, 2, classes.board.Label, self.qm, white, "", 31)
        self.sm1b = self.board.units[-1]
        self.sm1b.set_outline(color=self.font_color, width=1)
        self.sm1b.checkable = True
        self.sm1b.font_color = self.font_color
        self.sm1b.init_check_images()

        # final simplification if over 1
        if self.mainloop.m.game_variant == 0:
            self.board.add_unit(20, 3, 1, 2, classes.board.Label, "=", white, "", 31)
            self.eq4 = self.board.units[-1]

            self.board.add_unit(21, 3, 1, 2, classes.board.Label, "", white, "", 36)
            self.sm_one = self.board.units[-1]

            self.board.add_unit(22, 2, 2, 2, classes.board.Label, "", white, "", 31)
            self.sm2a = self.board.units[-1]
            self.sm2a.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=80)

            self.board.add_unit(22, 4, 2, 2, classes.board.Label, "", white, "", 31)
            self.sm2b = self.board.units[-1]
        else:

            self.board.add_unit(21, 3, 1, 2, classes.board.Label, "=", white, "", 31)
            self.eq4 = self.board.units[-1]

            self.board.add_unit(20, 0, 1, 2, classes.board.Label, "-", white, "", 36)
            self.minus = self.board.units[-1]

        # arrows for numerator 1
        self.board.add_unit(0, 0, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1alt = self.board.ships[-1]
        self.board.add_unit(3, 0, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1art = self.board.ships[-1]

        # arrows for denominator 1
        self.board.add_unit(0, 6, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1blt = self.board.ships[-1]
        self.board.add_unit(3, 6, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1brt = self.board.ships[-1]

        self.text_fields = [self.sm1a, self.sm1b]
        self.initialize_numbers(num1, num2, num3, num4)
        self.update_arrows()

        unit_fraction_line = classes.universal.Universal(board=self.board, grid_x=self.sm1a.grid_x,
                                                         grid_y=self.sm1a.grid_y + 1, grid_w=2, grid_h=2,
                                                         bg_img_src="fraction_line.png", bg_color=transp,
                                                         bg_tint_color=self.font_color, immobilized=True)

        self.board.all_sprites_list.add(unit_fraction_line)

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

        if self.level_data[1]:
            for each in self.divisors:
                self.board.all_sprites_list.move_to_front(each)

            for each in self.divisors2:
                self.board.all_sprites_list.move_to_front(each)

        self.prev_activ = self.sm1a
        self.active_fract = self.sm1a
        self.toggle_active_fract(self.sm1a)

    def toggle_active_fract(self, o1):
        if self.prev_activ != o1:
            self.prev_activ.set_outline(color=self.font_color, width=1)
            self.prev_activ.update_me = True
            self.prev_activ = o1
        o1.set_outline(color=self.font_color, width=5)
        self.active_fract = o1
        o1.update_me = True
        self.current_txt = ""
        self.mainloop.redraw_needed[0] = True

    def reset_font_colors(self):
        for each in self.board.units:
            each.font_color = self.font_color
            each.update_me = True

    def initialize_numbers(self, num1, num2, num3, num4):
        self.numbers = [num1, num3]
        self.numbers2 = [num2, num4]

        self.hidden_sim = [False, False]
        self.reset_font_colors()
        self.reset_minus()

        if num3 == num4:  # if denominators are the same add numerators
            if self.mainloop.m.game_variant == 0:
                self.sum_numbers = [num1 + num2, num3]
            else:
                # self.sum_numbers = [num1 + num2, num3]
                self.get_difference(num1, num2, num3)
            self.show(step=1, display=False)
            self.show(step=2, display=False)
            self.set_s1_colors()
            self.hidden_sim = [True, True]
        else:
            # check if simplifying fractions helps in finding lower common factor
            f_sim = [None, None, None, None]
            f_com = [None, None, None, None]
            simplified_1 = False
            simplified_2 = False

            # simplify none
            f_com[0] = self.lcd_fractions(num1, num3, num2, num4)
            f_sim[0] = self.lcd_fractions(num1, num3, num2, num4)

            # simplify first only
            gcf1 = self.gcf((num1, num3))
            if gcf1 > 1:
                num1x = int(num1 / gcf1)
                num3x = int(num3 / gcf1)
                f_com[1] = self.lcd_fractions(num1x, num3x, num2, num4)
                f_sim[1] = [[num1x, num3x], [num2, num4]]

            # simplify second only
            gcf2 = self.gcf((num2, num4))
            if gcf2 > 1:
                num2x = int(num2 / gcf2)
                num4x = int(num4 / gcf2)
                f_com[2] = self.lcd_fractions(num1, num3, num2x, num4x)
                f_sim[2] = [[num1, num3], [num2x, num4x]]

            # simplify both
            if gcf1 > 1 and gcf2 > 1:
                f_com[3] = self.lcd_fractions(num1x, num3x, num2x, num4x)
                f_sim[3] = [[num1x, num3x], [num2x, num4x]]

            # find the best option
            if f_com[3] is not None:
                # check for redundancies
                if f_com[3] == f_com[2]:
                    # simplify second only
                    num2 = num2x
                    num4 = num4x
                    simplified_2 = True
                elif f_com[3] == f_com[1]:
                    # simplify first only
                    num1 = num1x
                    num3 = num3x
                    simplified_1 = True
                else:
                    # simplify both
                    num1 = num1x
                    num3 = num3x
                    num2 = num2x
                    num4 = num4x
                    simplified_1 = True
                    simplified_2 = True
            elif f_com[2] is not None:
                # check if second simplification is needed
                if f_com[2] != f_com[0]:
                    # simplify second
                    num2 = num2x
                    num4 = num4x
                    simplified_2 = True
            elif f_com[1] is not None:
                # check if first simplification is needed
                if f_com[1] != f_com[0]:
                    # simplify first
                    num1 = num1x
                    num3 = num3x
                    simplified_1 = True

            # display simplification helpers
            if simplified_1:
                self.divisors[0].set_value("%s%s" % (chr(247), str(gcf1)))
                self.divisors[1].set_value("%s%s" % (chr(247), str(gcf1)))
                self.nm1xa.set_font_color(self.font_color2)
                self.nm1xb.set_font_color(self.font_color2)
            else:
                self.divisors[0].set_value("")
                self.divisors[1].set_value("")

            if simplified_2:
                self.divisors[2].set_value("%s%s" % (chr(247), str(gcf2)))
                self.divisors[3].set_value("%s%s" % (chr(247), str(gcf2)))
                self.nm2xa.set_font_color(self.font_color3)
                self.nm2xb.set_font_color(self.font_color3)
            else:
                self.divisors[2].set_value("")
                self.divisors[3].set_value("")

            # set correct simplification colours
            if simplified_1 or simplified_2:
                self.set_s1_colors()
                self.show(step=1, display=True)
            else:
                self.set_s2_colors()
                self.hidden_sim[0] = True
                self.show(step=1, display=False)

            #show simplified numbers
            self.step_1_simplify(num1, num2, num3, num4)

            # find common denominator
            self.display_common_den(num1, num3, num2, num4, simplified_1, simplified_2)

        if self.mainloop.m.game_variant == 0:
            self.show_simp()

        self.move_result()
        self.move_2_add_minus()
        self.move_arrows()

        if self.level_data[2] and self.level_data[3]:
            self.set_all_qm(True, True)
        elif self.level_data[2]:
            self.set_all_qm(True, False)
        elif self.level_data[3]:
            self.set_all_qm(False, True)

        for each in self.board.units:
            each.update_me = True
        self.mainloop.redraw_needed[0] = True

    def show_simp(self, force_hide=False):
        if force_hide:
            self.sm2a.hide()
            self.eq4.set_value("")
            self.sm_one.set_value("")
            self.sm2a.set_value("")
            self.sm2b.set_value("")
        else:
            if self.response[0] == self.response[1]:
                self.sm2a.hide()
                self.eq4.set_value("=")
                self.sm_one.set_value("1")
                self.sm2a.set_value("")
                self.sm2b.set_value("")
            elif self.response[0] > self.response[1] and self.response[0] < self.response[1] * 2:
                self.sm2a.show()
                self.eq4.set_value("=")
                self.sm_one.set_value("1")
                self.sm2a.set_value(str(self.response[0] - self.response[1]))
                self.sm2b.set_value(str(self.response[1]))
            else:
                self.sm2a.hide()
                self.eq4.set_value("")
                self.sm_one.set_value("")
                self.sm2a.set_value("")
                self.sm2b.set_value("")

    def update_fractions(self):
        self.nm1a.set_value(str(self.numbers[0]))
        self.nm1b.set_value(str(self.numbers[1]))
        self.nm2a.set_value(str(self.numbers2[0]))
        self.nm2b.set_value(str(self.numbers2[1]))
        self.sm1a.set_value(str(self.response[0]))
        self.sm1b.set_value(str(self.response[1]))
        if self.mainloop.m.game_variant == 0:
            self.show_simp()

    def set_all_qm(self, first=False, second=False):
        if first:
            self.nm1xa.set_value(self.qm)
            self.nm1xb.set_value(self.qm)
            self.nm2xa.set_value(self.qm)
            self.nm2xb.set_value(self.qm)
            self.nm1xa.set_outline(color=self.font_color, width=1)
            self.nm1xb.set_outline(color=self.font_color, width=1)
            self.nm2xa.set_outline(color=self.font_color, width=1)
            self.nm2xb.set_outline(color=self.font_color, width=1)
            self.text_fields.extend(
                [self.nm1xa, self.nm1xb, self.nm2xa, self.nm2xb])

        if second:
            self.nm1xa2.set_value(self.qm)
            self.nm1xb2.set_value(self.qm)
            self.nm2xa2.set_value(self.qm)
            self.nm2xb2.set_value(self.qm)
            self.nm1xa2.set_outline(color=self.font_color, width=1)
            self.nm1xb2.set_outline(color=self.font_color, width=1)
            self.nm2xa2.set_outline(color=self.font_color, width=1)
            self.nm2xb2.set_outline(color=self.font_color, width=1)
            self.text_fields.extend([self.nm1xa2, self.nm1xb2, self.nm2xa2, self.nm2xb2])

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.lang.d["Add and subtract with unlike denom. - instr"])

    def gcf(self, n):
        """
        Get the Greatest Common Factor
        :param n: list/tupple of (numerator, denominator)
        :return: a list of common factors for both numbers in n
        """
        mn = int(min(n[0], n[1]))
        mx = int(max(n[0], n[1]))
        gcf = 1
        if mx % mn == 0:
            return mn
        else:
            if mn > 3:
                start = int(mn / 2 + 1)
            else:
                start = 3
            for i in range(start, 1, -1):
                if mn % i == 0 and mx % i == 0 and i > gcf:
                    return i
        return gcf

    def gcd(self, a, b):
        if a == 0:
            return b
        return self.gcd(b % a, a)

    def lcm(self, a, b):
        return (a * b) / self.gcd(a, b)

    def lcd_fractions(self, num1, den1, num2, den2):
        lcd = self.lcm(den1, den2)
        num1 *= (lcd / den1)
        num2 *= (lcd / den2)

        return [[num1, lcd], [num2, lcd]]

    def display_common_den(self, num1, den1, num2, den2, simplified_1, simplified_2):
        lcd = self.lcm(den1, den2)
        num1 *= (lcd / den1)
        num2 *= (lcd / den2)

        if simplified_1 or simplified_2:
            if lcd > den1:
                self.divisors2[0].set_value("%s%s" % (chr(215), str(int(lcd/den1))))
                self.divisors2[1].set_value("%s%s" % (chr(215), str(int(lcd/den1))))

                self.nm1xa2.set_font_color(self.font_color6)
                self.nm1xb2.set_font_color(self.font_color6)
            else:
                self.divisors2[0].set_value("")
                self.divisors2[1].set_value("")

                if simplified_1:
                    self.nm1xa2.set_font_color(self.font_color2)
                    self.nm1xb2.set_font_color(self.font_color2)

            if lcd > den2:
                self.divisors2[2].set_value("%s%s" % (chr(215), str(int(lcd/den2))))
                self.divisors2[3].set_value("%s%s" % (chr(215), str(int(lcd/den2))))

                self.nm2xa2.set_font_color(self.font_color7)
                self.nm2xb2.set_font_color(self.font_color7)
            else:
                self.divisors2[2].set_value("")
                self.divisors2[3].set_value("")

                if simplified_2:
                    self.nm2xa2.set_font_color(self.font_color3)
                    self.nm2xb2.set_font_color(self.font_color3)
        else:
            if lcd > den1:
                self.divisors[0].set_value("%s%s" % (chr(215), str(int(lcd / den1))))
                self.divisors[1].set_value("%s%s" % (chr(215), str(int(lcd / den1))))

                self.nm1xa2.set_font_color(self.font_color6)
                self.nm1xb2.set_font_color(self.font_color6)
            else:
                self.divisors[0].set_value("")
                self.divisors[1].set_value("")

            if lcd > den2:
                self.divisors[2].set_value("%s%s" % (chr(215), str(int(lcd / den2))))
                self.divisors[3].set_value("%s%s" % (chr(215), str(int(lcd / den2))))

                self.nm2xa2.set_font_color(self.font_color7)
                self.nm2xb2.set_font_color(self.font_color7)
            else:
                self.divisors[2].set_value("")
                self.divisors[3].set_value("")

            self.divisors2[0].set_value("")
            self.divisors2[1].set_value("")
            self.divisors2[2].set_value("")
            self.divisors2[3].set_value("")

        if lcd > den1 or lcd > den2:
            self.show(step=2, display=True, simplified=simplified_1 or simplified_2)
        else:
            self.show(step=2, display=False, simplified=simplified_1 or simplified_2)
            self.hidden_sim[1] = True

        self.step_2_common_den(int(num1), int(num2), int(lcd))
        if self.mainloop.m.game_variant == 0:
            self.sum_numbers = [int(num1 + num2), int(lcd)]
        else:
            self.get_difference(num1, num2, lcd)

    def get_difference(self, num1, num2, den):
        self.sum_numbers = [int(abs(num1 - num2)), int(den)]
        if num1 > num2:
            self.sm1a.show()
            self.sm1b.show()
            self.minus.set_value("")
            self.shift = True
        elif num1 == num2:
            self.sm1a.hide()
            self.sm1b.hide()
            self.shift = True
            self.minus.set_value("0")
        else:
            self.sm1a.show()
            self.sm1b.show()
            self.shift = True
            self.minus.set_value("-")

    def step_1_simplify(self, num1, num2, den1, den2):
        self.nm1xa.set_value(str(num1))
        self.nm1xb.set_value(str(den1))
        self.nm2xa.set_value(str(num2))
        self.nm2xb.set_value(str(den2))

    def step_2_common_den(self, num1, num2, den):
        self.nm1xa2.set_value(str(num1))
        self.nm1xb2.set_value(str(den))
        self.nm2xa2.set_value(str(num2))
        self.nm2xb2.set_value(str(den))

    def set_s1_colors(self):
        self.divisors[0].font_colors = (self.font_color2, )
        self.divisors[1].font_colors = (self.font_color2, )
        self.divisors[2].font_colors = (self.font_color3, )
        self.divisors[3].font_colors = (self.font_color3, )
        for each in self.divisors:
            each.update_me = True
            each.update(self.board)

    def set_s2_colors(self):
        self.divisors[0].font_colors = (self.font_color6, )
        self.divisors[1].font_colors = (self.font_color6, )
        self.divisors[2].font_colors = (self.font_color7, )
        self.divisors[3].font_colors = (self.font_color7, )
        for each in self.divisors:
            each.update_me = True
            each.update(self.board)

    def show(self, step=1, display=True, simplified=False):
        if step == 1:
            if display:
                self.nm1xa.show()
                self.nm1xb.show()
                self.nm2xa.show()
                self.nm2xb.show()
                self.board.move_unit(self.eq1.unit_id, 5, 3)
                self.board.move_unit(self.nm1xa.unit_id, 6, 2)
                self.board.move_unit(self.nm1xb.unit_id, 6, 4)
                self.board.move_unit(self.pl1.unit_id, 8, 3)
                self.board.move_unit(self.nm2xa.unit_id, 9, 2)
                self.board.move_unit(self.nm2xb.unit_id, 9, 4)
                self.pl1.set_value(self.sign)
                self.eq1.set_value("=")
            else:
                self.nm1xa.hide()
                self.nm1xb.hide()
                self.nm2xa.hide()
                self.nm2xb.hide()
                self.board.move_unit(self.eq1.unit_id, 5, 0)
                self.board.move_unit(self.nm1xa.unit_id, 6, 0)
                self.board.move_unit(self.nm1xb.unit_id, 6, 6)
                self.board.move_unit(self.pl1.unit_id, 8, 0)
                self.board.move_unit(self.nm2xa.unit_id, 9, 0)
                self.board.move_unit(self.nm2xb.unit_id, 9, 6)
                self.pl1.set_value("")
                self.eq1.set_value("")
                self.divisors[0].set_value("")
                self.divisors[1].set_value("")
                self.divisors[2].set_value("")
                self.divisors[3].set_value("")
        else:
            if display:
                self.nm1xa2.show()
                self.nm1xb2.show()
                self.nm2xa2.show()
                self.nm2xb2.show()
                if simplified:
                    self.board.move_unit(self.eq2.unit_id, 11, 3)
                    self.board.move_unit(self.nm1xa2.unit_id, 12, 2)
                    self.board.move_unit(self.nm1xb2.unit_id, 12, 4)
                    self.board.move_unit(self.pl2.unit_id, 14, 3)
                    self.board.move_unit(self.nm2xa2.unit_id, 15, 2)
                    self.board.move_unit(self.nm2xb2.unit_id, 15, 4)
                else:
                    self.board.move_unit(self.eq2.unit_id, 5, 3)
                    self.board.move_unit(self.nm1xa2.unit_id, 6, 2)
                    self.board.move_unit(self.nm1xb2.unit_id, 6, 4)
                    self.board.move_unit(self.pl2.unit_id, 8, 3)
                    self.board.move_unit(self.nm2xa2.unit_id, 9, 2)
                    self.board.move_unit(self.nm2xb2.unit_id, 9, 4)
                self.pl2.set_value(self.sign)
                self.eq2.set_value("=")
            else:
                self.nm1xa2.hide()
                self.nm1xb2.hide()
                self.nm2xa2.hide()
                self.nm2xb2.hide()
                self.board.move_unit(self.eq2.unit_id, 11, 0)
                self.board.move_unit(self.nm1xa2.unit_id, 12, 0)
                self.board.move_unit(self.nm1xb2.unit_id, 12, 6)
                self.board.move_unit(self.pl2.unit_id, 14, 0)
                self.board.move_unit(self.nm2xa2.unit_id, 15, 0)
                self.board.move_unit(self.nm2xb2.unit_id, 15, 6)
                self.pl2.set_value("")
                self.eq2.set_value("")
                self.divisors2[0].set_value("")
                self.divisors2[1].set_value("")
                self.divisors2[2].set_value("")
                self.divisors2[3].set_value("")

    def move_2_add_minus(self):
        if self.mainloop.m.game_variant == 1 and self.shift:
            self.board.move_unit(self.sm1a.unit_id, self.sm1a.grid_x, 2)
            self.board.move_unit(self.sm1b.unit_id, self.sm1b.grid_x, 4)
            self.board.move_unit(self.minus.unit_id, self.sm1a.grid_x - 1, 3)

    def reset_minus(self):
        if self.mainloop.m.game_variant == 1:
            self.board.move_unit(self.minus.unit_id, self.sm1b.grid_x + 3, 3)
            self.minus.set_value("")
            self.eq4.set_value("")

    def move_result(self):
        if self.hidden_sim[0] and self.hidden_sim[1]:
            self.board.move_unit(self.eq3.unit_id, 5, 3)
            self.board.move_unit(self.sm1a.unit_id, 7, 2)
            self.board.move_unit(self.sm1b.unit_id, 7, 4)
            if self.mainloop.m.game_variant == 0:
                self.board.move_unit(self.eq4.unit_id, 10, 3)
                self.board.move_unit(self.sm_one.unit_id, 11, 3)
                self.board.move_unit(self.sm2a.unit_id, 12, 2)
                self.board.move_unit(self.sm2b.unit_id, 12, 4)
        elif self.hidden_sim[0] or self.hidden_sim[1]:
            self.board.move_unit(self.eq3.unit_id, 11, 3)
            self.board.move_unit(self.sm1a.unit_id, 13, 2)
            self.board.move_unit(self.sm1b.unit_id, 13, 4)
            if self.mainloop.m.game_variant == 0:
                self.board.move_unit(self.eq4.unit_id, 16, 3)
                self.board.move_unit(self.sm_one.unit_id, 17, 3)
                self.board.move_unit(self.sm2a.unit_id, 18, 2)
                self.board.move_unit(self.sm2b.unit_id, 18, 4)
        else:
            self.board.move_unit(self.eq3.unit_id, 17, 3)
            self.board.move_unit(self.sm1a.unit_id, 19, 2)
            self.board.move_unit(self.sm1b.unit_id, 19, 4)
            if self.mainloop.m.game_variant == 0:
                self.board.move_unit(self.eq4.unit_id, 22, 3)
                self.board.move_unit(self.sm_one.unit_id, 23, 3)
                self.board.move_unit(self.sm2a.unit_id, 24, 2)
                self.board.move_unit(self.sm2b.unit_id, 24, 4)

    def move_arrows(self):
        self.board.move_unit(self.nm1alt.unit_id, self.sm1a.grid_x-1, 2, True)
        self.board.move_unit(self.nm1blt.unit_id, self.sm1a.grid_x-1, 4, True)
        self.board.move_unit(self.nm1art.unit_id, self.sm1a.grid_x+2, 2, True)
        self.board.move_unit(self.nm1brt.unit_id, self.sm1a.grid_x+2, 4, True)
        if self.mainloop.m.game_variant == 1:
            self.board.move_unit(self.eq4.unit_id, self.sm1a.grid_x+2, 3)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            for each in self.text_fields:
                if each.rect.topleft[0] < pos[0] < each.rect.topleft[0] + each.rect.width and \
                        each.rect.topleft[1] < pos[1] < each.rect.topleft[1] + each.rect.height:
                    self.toggle_active_fract(each)
            active = self.board.active_ship
            if active == 0:
                self.change_fract_btn(self.response, -1, 0)
            elif active == 1:
                self.change_fract_btn(self.response, 1, 0)
            elif active == 2:
                self.change_fract_btn(self.response, 0, -1)
            elif active == 3:
                self.change_fract_btn(self.response, 0, 1)
            self.auto_check_reset()
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            self.check_result()
        elif event.type == pygame.KEYDOWN:
            self.auto_check_reset()
            lhv = len(self.current_txt)
            self.changed_since_check = True
            if event.key == pygame.K_BACKSPACE:
                if lhv > 0:
                    self.current_txt = self.current_txt[0:lhv - 1]
                    self.active_fract.value = self.current_txt
                self.active_fract.update_me = True
                if len(self.current_txt) > 0:
                    if self.active_fract == self.sm1a:
                        self.response[0] = int(self.active_fract.value)
                    elif self.active_fract == self.sm1b:
                        self.response[1] = int(self.active_fract.value)
                else:
                    if self.active_fract == self.sm1a:
                        self.response[0] = 0
                    elif self.active_fract == self.sm1b:
                        self.response[1] = 0

                if self.mainloop.m.game_variant == 0:
                    if self.sm1a.value != "" and self.sm2a.value != "":
                        self.show_simp()
                    else:
                        self.show_simp(force_hide=True)

            elif event.key == pygame.K_TAB:
                if self.active_fract == self.sm1a:
                    self.toggle_active_fract(self.sm1b)
                else:
                    self.toggle_active_fract(self.sm1a)
            else:
                char = event.unicode
                if char in self.digits:
                    if len(char) > 0 and lhv < 3 and self.active_fract.value != self.qm:
                        self.current_txt += char
                    else:
                        self.current_txt = char

                    self.active_fract.value = self.current_txt

                    if self.active_fract == self.sm1a:
                        self.response[0] = int(self.active_fract.value)
                        if self.response[0] == self.sum_numbers[0]:
                            self.toggle_active_fract(self.sm1b)
                    elif self.active_fract == self.sm1b:
                        self.response[1] = int(self.active_fract.value)
                    self.active_fract.update_me = True
                    if self.mainloop.m.game_variant == 0:
                        self.show_simp()

            self.mainloop.redraw_needed[0] = True

    def auto_check_reset(self):
        self.sm1a.set_display_check(None)
        self.sm1b.set_display_check(None)

    def change_fract_btn(self, ns, n1, n2):
        self.current_txt = ""

        if n1 == -1:
            if ns[0] > 1:
                ns[0] -= 1
        elif n1 == 1:
            if ns[0] < self.max_num:
                ns[0] += 1

        elif n2 == -1:
            if ns[1] > 2:
                ns[1] -= 1

        elif n2 == 1:
            if ns[1] <= self.max_num:
                ns[1] += 1

        if n1 != 0:
            self.toggle_active_fract(self.sm1a)
        elif n2 != 0:
            self.toggle_active_fract(self.sm1b)

        self.initialize_numbers(self.numbers[0], self.numbers2[0], self.numbers[1], self.numbers2[1])
        self.update_arrows()
        self.update_fractions()

    def update_arrows(self):
        # enable/dissable arrows
        if self.response[0] <= 1:
            if self.nm1alt.img_src != "nav_l_mtsd.png":
                self.nm1alt.change_image("nav_l_mtsd.png")
        else:
            if self.nm1alt.img_src != "nav_l_mts.png":
                self.nm1alt.change_image("nav_l_mts.png")

        if self.response[0] > self.max_num - 1:
            if self.nm1art.img_src != "nav_r_mtsd.png":
                self.nm1art.change_image("nav_r_mtsd.png")
        else:
            if self.nm1art.img_src != "nav_r_mts.png":
                self.nm1art.change_image("nav_r_mts.png")

        if self.response[1] <= 2:
            if self.nm1blt.img_src != "nav_l_mtsd.png":
                self.nm1blt.change_image("nav_l_mtsd.png")
        else:
            if self.nm1blt.img_src != "nav_l_mts.png":
                self.nm1blt.change_image("nav_l_mts.png")

        if self.response[1] > self.max_num:
            if self.nm1brt.img_src != "nav_r_mtsd.png":
                self.nm1brt.change_image("nav_r_mtsd.png")
        else:
            if self.nm1brt.img_src != "nav_r_mts.png":
                self.nm1brt.change_image("nav_r_mts.png")

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        if self.response[0] == self.sum_numbers[0]:
            self.sm1a.set_display_check(True)
        else:
            self.sm1a.set_display_check(False)

        if self.response[1] == self.sum_numbers[1]:
            self.sm1b.set_display_check(True)
        else:
            self.sm1b.set_display_check(False)

        if self.response == self.sum_numbers:
            self.level.next_board()

        self.mainloop.redraw_needed[0] = True
