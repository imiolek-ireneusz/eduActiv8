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
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
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

        transp = (0, 0, 0, 0)

        self.lvl_data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid,
                                                              self.mainloop.config.user_age_group, self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        data = [20, 14]
        f_size = 10
        self.data = data

        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.typed = False

        # reduce or extend
        if self.mainloop.m.game_variant == 0:
            re = 0
        elif self.mainloop.m.game_variant == 1:
            re = 1
        else:
            re = random.randint(0, 1)

        if re == 0: # reduce
            #lst = self.get_multiple_factors(80, 3)
            lst = self.get_multiple_factors(self.lvl_data[1] * self.lvl_data[1], 3)
            n = random.randint(0, len(lst) - 1)
            num1 = lst[n][0]
            num2 = lst[n][1]
            self.numbers = [num1, num2]
            self.factors = self.get_factors(self.numbers)
            if self.mainloop.m.game_variant == 2:
                self.active_factor = random.randrange(1, len(self.factors))
            else:
                self.active_factor = -1
            self.numbers2 = [num1 // self.factors[self.active_factor], num2 // self.factors[self.active_factor]]
            self.max_num = 119
        else:
            self.multiplier = random.randint(2, 9)
            #num2 = random.randint(2, 10)
            num2 = random.randint(self.lvl_data[0], self.lvl_data[1])
            num1 = random.randint(1, num2 - 1)
            self.numbers = [num1, num2]
            self.numbers2 = [num1 * self.multiplier, num2 * self.multiplier]
            self.max_num = 119

        self.missing_number = random.randint(1, 2)
        self.result = [1, 0]

        # add first fraction - graphic
        if self.level.lvl < 3:
            x = 0
        else:
            x = 5
        self.board.add_unit(x, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                         bd_color2, self.numbers, 2)
        self.fraction.set_offset(0, 0)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()

        # add second fraction - graphic
        if self.level.lvl < 3:
            self.board.add_unit(f_size, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
            self.fraction2_canvas = self.board.units[-1]
            self.fraction2 = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                              bd_color2, self.numbers2, 2)
            self.fraction2.set_offset(0, 0)
            self.fraction2_canvas.painting = self.fraction2.get_canvas().copy()

        # add first fraction
        self.board.add_unit(4, f_size, 2, 2, classes.board.Label, str(self.numbers[0]), white, "", 31)
        self.nm1 = self.board.units[-1]
        self.nm1.checkable = True
        self.nm1.init_check_images()

        #else:
        #    self.nm1.set_fraction_lines(top=False, bottom=True, color=line_color)
        self.nm1.font_color = bd_color1

        self.board.add_unit(4, f_size + 2, 2, 2, classes.board.Label, str(self.numbers[1]), white, "", 31)
        self.nm2 = self.board.units[-1]
        self.nm2.checkable = True
        self.nm2.init_check_images()
        self.nm2.font_color = bd_color2
        if self.missing_number == 1:
            self.nm2.set_fraction_lines(top=True, bottom=False, color=line_color)
            nm1as = "1"
            nm2as = str(self.numbers2[1])
            self.numbers_disp = 0
        else:
            self.nm1.set_fraction_lines(top=False, bottom=True, color=line_color)
            nm2as = str(self.numbers2[0])
            nm1as = str(self.numbers2[0])
            self.result[1] = self.numbers2[0]
            self.numbers_disp = self.numbers2[0]

        # add second fraction
        self.board.add_unit(f_size + 4, f_size, 2, 2, classes.board.Label, nm1as, white, "", 31)
        self.nm1a = self.board.units[-1]
        self.nm1a.font_color = bd_color1

        if self.missing_number == 1:
            self.active_num = self.nm1a
            self.board.add_unit(f_size + 2, f_size, 2, 2, classes.board.ImgCenteredShip, "", transp,
                                img_src='nav_l_mtsd.png', alpha=True)
            self.board.ships[-1].set_tint_color(bd_color1)

            self.board.add_unit(f_size + 6, f_size, 2, 2, classes.board.ImgCenteredShip, "", transp,
                                img_src='nav_r_mts.png', alpha=True)
            self.board.ships[-1].set_tint_color(bd_color1)
        else:
            self.nm1a.set_fraction_lines(top=False, bottom=True, color=line_color)


        self.board.add_unit(f_size + 4, f_size + 2, 2, 2, classes.board.Label, nm2as, white, "", 31)
        self.nm2a = self.board.units[-1]
        self.nm2a.font_color = bd_color2
        if self.missing_number == 2:
            self.active_num = self.nm2a
            self.board.add_unit(f_size + 2, f_size + 2, 2, 2, classes.board.ImgCenteredShip, "", transp,
                                img_src='nav_l_mtsd.png', alpha=True)
            self.board.ships[-1].set_tint_color(bd_color2)

            self.board.add_unit(f_size + 6, f_size + 2, 2, 2, classes.board.ImgCenteredShip, "", transp,
                                img_src='nav_r_mts.png', alpha=True)
            self.board.ships[-1].set_tint_color(bd_color2)
        else:
            self.nm2a.set_fraction_lines(top=True, bottom=False, color=line_color)
        self.active_num.set_outline(color=[255, 0, 0], width=2)
        self.active_num.checkable = True
        self.active_num.init_check_images()
        """
        self.multiplier = 2

        lst = self.get_multiple_factors(80, 3)
        n = random.randint(0, len(lst)-1)
        num1 = lst[n][0]
        num2 = lst[n][1]
        
        self.numbers = [num1, num2]
        self.numbers2 = [num1 * self.multiplier, num2 * self.multiplier]
        self.max_num = 119

        # add first fraction
        self.board.add_unit(0, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                         bd_color2, self.numbers, 2)
        self.fraction.set_offset(0, 0)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()



        self.board.add_unit(4, f_size, 2, 2, classes.board.Label, str(self.numbers[0]), white, "", 31)
        self.nm1 = self.board.units[-1]
        self.nm1.checkable = True
        self.nm1.init_check_images()
        self.nm1.set_fraction_lines(top=False, bottom=True, color=line_color)
        self.nm1.font_color = bd_color1

        self.board.add_unit(4, f_size + 2, 2, 2, classes.board.Label, str(self.numbers[1]), white, "", 31)
        self.nm2 = self.board.units[-1]
        self.nm2.checkable = True
        self.nm2.init_check_images()
        self.nm2.font_color = bd_color2

        # add second fraction
        self.board.add_unit(f_size + 2, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.fraction2_canvas = self.board.units[-1]
        self.fraction2 = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                          bd_color2, self.numbers2, 2)
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

        self.board.add_unit(f_size + 4, f_size, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(bd_color1)

        self.board.add_unit(f_size + 8, f_size, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(bd_color1)

        self.board.add_unit(f_size + 4, f_size + 2, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(bd_color2)

        self.board.add_unit(f_size + 8, f_size + 2, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(bd_color2)

        #self.factorss = self.get_factors(self.numbers)
        self.factor_list = []
        for i in range(12):
            self.board.add_unit(f_size, i, 2, 1, classes.board.Letter, "", white, "", 0)
            self.board.ships[-1].font_color = bd_color1
            self.factor_list.append(self.board.ships[-1])
        self.update_factors()
        self.active_factor = self.factor_list[0]
        self.activate_factor(0)
        """

        #self.change_fract_btn(0, 0)
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
            for i in range(2, int(mn / 2 + 1)):
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
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = self.board.active_ship
            if self.missing_number == 1:
                if active == 0:
                    self.change_fract_btn(-1, 0)
                elif active == 1:
                    self.change_fract_btn(1, 0)
            else:
                if active == 0:
                    self.change_fract_btn(0, -1)
                elif active == 1:
                    self.change_fract_btn(0, 1)
            self.auto_check_reset()
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            self.check_result()
        elif event.type == pygame.KEYDOWN:
            lhv = len(self.active_num.value)
            self.changed_since_check = True
            if event.key == pygame.K_BACKSPACE:
                if lhv > 0:
                    self.active_num.value = self.active_num.value[0:lhv - 1]
            else:
                char = event.unicode
                if self.typed and len(char) > 0 and lhv < 3 and char in self.digits:
                    self.active_num.value += char
                elif char in self.digits:
                    self.active_num.value = char
                    self.typed = True
            if len(self.active_num.value) > 0:
                self.result[self.missing_number - 1] = int(self.active_num.value)
            else:
                self.result[self.missing_number - 1] = 0

            self.active_num.update_me = True
            self.mainloop.redraw_needed[0] = True
            self.auto_check_reset()


    def auto_check_reset(self):
        self.active_num.set_display_check(None)
        self.mainloop.redraw_needed[0] = True

    def change_fract_btn(self, n1, n2):
        if n1 == -1:
            if self.result[0] > 1:
                self.result[0] -= 1
        elif n1 == 1:
            if self.result[0] < self.numbers2[1]:
                self.result[0] += 1
            #if self.result[0] >= self.result[1]:
            #    self.result[1] = self.result[0]+1

        elif n2 == -1:
            if self.result[1] > self.numbers2[0]:
                self.result[1] -= 1
            #if self.result[0] >= self.result[1]:
            #    self.result[0] = self.result[1]-1

        elif n2 == 1:
            if self.result[1] <= self.max_num:
                self.result[1] += 1
        if self.missing_number == 1:
            if self.result[0] == 1:
                self.board.ships[0].change_image("nav_l_mtsd.png")
            elif self.result[0] == self.numbers2[1]:
                self.board.ships[1].change_image("nav_r_mtsd.png")
            else:
                self.board.ships[0].change_image("nav_l_mts.png")
                self.board.ships[1].change_image("nav_r_mts.png")
        else:

            if self.result[1] == self.numbers2[0]:
                self.board.ships[0].change_image("nav_l_mtsd.png")
            elif self.result[1] == self.max_num + 1:
                self.board.ships[1].change_image("nav_r_mtsd.png")
            else:
                self.board.ships[0].change_image("nav_l_mts.png")
                self.board.ships[1].change_image("nav_r_mts.png")

        #self.update_factors()
        self.update_fractions()

    def update_fractions(self):
        if self.missing_number == 1:
            self.nm1a.set_value(str(self.result[0]))
        else:
            self.nm2a.set_value(str(self.result[1]))
        #self.fraction.update_values(self.numbers)
        #self.fraction_canvas.painting = self.fraction.get_canvas().copy()
        #self.mainloop.redraw_needed[0] = True
        #self.fraction_canvas.update_me = True
        #self.nm1a.set_value(str(int(round(self.numbers[0] / float(self.active_factor.value)))))
        #self.nm2a.set_value(str(int(round(self.numbers[1] / float(self.active_factor.value)))))
        #self.fraction2.update_values((int(round(self.numbers[0] / float(self.active_factor.value))), int(round(self.numbers[1] / float(self.active_factor.value)))))
        #self.fraction2_canvas.painting = self.fraction2.get_canvas().copy()
        #self.fraction2_canvas.update_me = True
        self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        correct = False
        if self.missing_number == 1:
            if self.result[0] == self.numbers2[0]:
                self.nm1a.set_display_check(True)
                correct = True
            else:
                self.nm1a.set_display_check(False)
        else:

            if self.result[1] == self.numbers2[1]:
                self.nm2a.set_display_check(True)
                correct = True
            else:
                self.nm2a.set_display_check(False)
        self.typed = False

        if correct:
            self.level.next_board()

        self.mainloop.redraw_needed[0] = True
