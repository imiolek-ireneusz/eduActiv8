# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.drw.fraction_hq
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 15, 3)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 15, 10)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color
            line_color = self.mainloop.scheme.u_font_color

            h1 = 170
            h2 = 40
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            white = (255, 255, 255)
            line_color = (0, 0, 0)

            h1 = random.randrange(0, 255)
            h2 = (h1 + 128) % 255

            color1 = ex.hsv_to_rgb(h1, 150, 255)
            color2 = ex.hsv_to_rgb(h2, 40, 255)


            bd_color1 = ex.hsv_to_rgb(h1, 187, 200)
            bd_color2 = ex.hsv_to_rgb(h2, 100, 200)

        data = [22, 14]
        f_size = 10
        self.data = data

        #self.vis_buttons = [1, 0, 0, 0, 1, 1, 1, 0, 0]
        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 1]

        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True

        self.board.board_bg.line_color = (20, 20, 20)

        self.multiplier = 2

        lst = self.get_multiple_factors(80, 3)
        n = random.randint(0, len(lst)-1)
        num1 = lst[n][0]
        num2 = lst[n][1]
        self.numbers = [num1, num2]
        self.numbers2 = [num1, num2 * self.multiplier]
        self.max_num = 119

        # add first fraction
        self.board.add_unit(0, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                         bd_color2, self.numbers, 2)
        # self.fraction.set_offset(15, 10)
        self.fraction.set_offset(0, 0)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()

        self.board.add_unit(2, f_size, 2, 2, classes.board.Letter, "-", white, "", 31)
        self.board.ships[-1].font_color = bd_color1
        self.board.add_unit(4, f_size, 2, 2, classes.board.Label, str(self.numbers[0]), white, "", 31)
        self.nm1 = self.board.units[-1]
        #self.nm1.set_outline(color=[255, 0, 0], width=2)
        self.nm1.checkable = True
        self.nm1.init_check_images()
        self.nm1.set_fraction_lines(top=False, bottom=True, color=line_color)
        self.nm1.font_color = bd_color1
        self.board.add_unit(6, f_size, 2, 2, classes.board.Letter, "+", white, "", 31)
        self.board.ships[-1].font_color = bd_color1
        self.board.add_unit(2, f_size + 2, 2, 2, classes.board.Letter, "-", white, "", 31)
        self.board.ships[-1].font_color = bd_color2
        self.board.add_unit(4, f_size + 2, 2, 2, classes.board.Label, str(self.numbers[1]), white, "", 31)
        self.nm2 = self.board.units[-1]
        #self.nm2.set_outline(color=[255, 0, 0], width=2)
        self.nm2.checkable = True
        self.nm2.init_check_images()
        # self.nm2.set_fraction_lines(top=True, bottom=False, color=bd_color2)
        self.nm2.font_color = bd_color2
        self.board.add_unit(6, f_size + 2, 2, 2, classes.board.Letter, "+", white, "", 31)
        self.board.ships[-1].font_color = bd_color2

        # add second fraction
        self.board.add_unit(f_size + 2, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.fraction2_canvas = self.board.units[-1]
        self.fraction2 = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                          bd_color2, self.numbers2, 2)
        # self.fraction2.set_offset(10, 5)
        self.fraction2.set_offset(0, 0)
        self.fraction2_canvas.painting = self.fraction2.get_canvas().copy()
        self.board.add_unit(f_size + 6, f_size, 2, 2, classes.board.Label, str(self.numbers2[0]), white, "", 31)
        self.nm1a = self.board.units[-1]
        self.nm1a.checkable = True
        self.nm1a.init_check_images()
        self.nm1a.set_fraction_lines(top=False, bottom=True, color=line_color)
        self.nm1a.font_color = bd_color1

        self.board.add_unit(f_size + 6, f_size + 2, 2, 2, classes.board.Label, str(self.numbers2[1]), white, "", 31)
        self.nm2a = self.board.units[-1]
        self.nm2a.checkable = True
        self.nm2a.init_check_images()
        self.nm2a.font_color = bd_color2

        self.factorss = self.get_factors(self.numbers)
        self.factor_list = []
        for i in range(12):
            self.board.add_unit(f_size, i, 2, 1, classes.board.Letter, "", white, "", 0)
            self.board.ships[-1].font_color = bd_color1
            self.factor_list.append(self.board.ships[-1])
        self.update_factors()
        self.active_factor = self.factor_list[0]
        self.activate_factor(0)

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.lang.d["To reduce a fraction..."])

    def update_factors(self):
        self.factors = self.get_factors(self.numbers)
        ld = len(self.factors)
        for i in range(12):
            if i < ld:
                val = str(self.factors[i])
            else:
                val = ""
            self.factor_list[i].set_value(val)
        self.activate_factor(0)

    def get_multiple_factors(self, top, min_of_factors):
        """
        Get a list of tuples of numbers that have more than min_of_factors common factors
        :param top: top of the range ie. 1-120
        :param min_of_factors: minimum number of common factors
        :return: list of tuples of numbers that have more than min_of_factors number of common factors
        """
        lst = []
        for i in range(1, top + 1):
            for j in range(1, top + 1):
                if i < j:
                    if len(self.get_factors((i, j))) > min_of_factors:
                        lst.append((i, j))
        return lst

    def get_factors(self, n):
        """
        Get a list of common factors
        :param n: list/tupple of (numerator, denominator)
        :return: a list of common factors for both numbers in n
        """
        mn = min(n[0], n[1])
        mx = max(n[0], n[1])
        lst = [1]
        if mn > 3:
            for i in range(2, mn / 2 + 1):
                if mn % i == 0 and mx % i == 0:
                    lst.append(i)
        if mx % mn == 0 and mn != 1:
            lst.append(mn)
        return lst

    def activate_factor(self, active):
        if len(self.factor_list[active].value) > 0:
            self.factor_list[active].update_font_size(31)
            self.active_factor = self.factor_list[active]
            for i in range(12):
                if i != active:
                    self.factor_list[i].update_font_size(25)
                self.factor_list[i].update_me = True
            self.update_fractions()

            self.mainloop.redraw_needed[0] = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = self.board.active_ship
            if active == 0:
                self.change_fract_btn(-1, 0)
            elif active == 1:
                self.change_fract_btn(1, 0)
            elif active == 2:
                self.change_fract_btn(0, -1)
            elif active == 3:
                self.change_fract_btn(0, 1)
            elif 3 < active < 16:
                self.activate_factor(active-4)
            self.auto_check_reset()
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            self.check_result()
        elif event.type == pygame.KEYDOWN:
            self.auto_check_reset()

    def auto_check_reset(self):
        self.nm1.set_display_check(None)
        self.nm2.set_display_check(None)

    def change_mlt_btn(self, n):
        if n == 1:
            if self.multiplier < 10:
                self.multiplier += 1
        if n == -1:
            if self.multiplier > 1:
                self.multiplier -= 1

        self.update_fractions()

    def change_fract_btn(self, n1, n2):
        if n1 == -1:
            if self.numbers[0] > 1:
                self.numbers[0] -= 1
        elif n1 == 1:
            if self.numbers[0] < self.max_num:
                self.numbers[0] += 1
            if self.numbers[0] >= self.numbers[1]:
                self.numbers[1] = self.numbers[0]+1

        elif n2 == -1:
            if self.numbers[1] > 2:
                self.numbers[1] -= 1
            if self.numbers[0] >= self.numbers[1]:
                self.numbers[0] = self.numbers[1]-1

        elif n2 == 1:
            if self.numbers[1] <= self.max_num:
                self.numbers[1] += 1

        self.update_factors()
        self.update_fractions()

    def update_fractions(self):
        self.nm1.set_value(str(self.numbers[0]))
        self.nm2.set_value(str(self.numbers[1]))
        self.fraction.update_values(self.numbers)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()
        self.mainloop.redraw_needed[0] = True
        self.fraction_canvas.update_me = True
        self.nm1a.set_value(str(int(round(self.numbers[0] / float(self.active_factor.value)))))
        self.nm2a.set_value(str(int(round(self.numbers[1] / float(self.active_factor.value)))))
        self.fraction2.update_values((int(round(self.numbers[0] / float(self.active_factor.value))), int(round(self.numbers[1] / float(self.active_factor.value)))))
        self.fraction2_canvas.painting = self.fraction2.get_canvas().copy()
        self.fraction2_canvas.update_me = True
        self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass

