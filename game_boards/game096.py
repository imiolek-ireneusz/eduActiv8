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
            h1 = 170
            h2 = h1 #40
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
            font_color = bd_color1
        else:
            white = (255, 255, 255)
            h1 = 17
            h2 = h1
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 40, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 255, 200)
            bd_color2 = ex.hsv_to_rgb(h2, 100, 200)
            font_color = ex.hsv_to_rgb(h1, 255, 175)
            
        self.bd_color1 = bd_color1
        transp = (0, 0, 0, 0)
        data = [24, 9]
        f_size = 5
        self.data = data
        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 1]

        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True

        self.board.board_bg.line_color = (20, 20, 20)

        self.multiplier = 2
        num3 = random.randint(2, 12)
        num4 = random.randint(2, 12)
        num1 = random.randint(1, num3-1)
        num2 = random.randint(1, num4-1)

        self.initialize_numbers(num1, num2, num3, num4)
        self.max_num = 11

        # add first fraction
        self.board.add_unit(0, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                         bd_color2, self.numbers, 2)
        self.fraction.set_offset(20, 30)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()

        # add second fraction
        self.board.add_unit(f_size, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.fraction2_canvas = self.board.units[-1]
        self.fraction2 = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                          bd_color2, self.numbers2, 2)
        self.fraction2.set_offset(20, 30)
        self.fraction2_canvas.painting = self.fraction2.get_canvas().copy()

        # add initial result
        self.board.add_unit(f_size*2+2, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.res2_canvas = self.board.units[-1]
        self.res2 = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                          bd_color2, self.res2_numbers, 2)
        self.res2.set_offset(0, 0)
        self.res2_canvas.painting = self.res2.get_canvas().copy()

        # add simplified result
        self.board.add_unit(f_size * 3 + 2+2, 0, f_size, f_size, classes.board.Label, "", white, "", 0)
        self.sim2_canvas = self.board.units[-1]
        self.sim2 = classes.drw.fraction_hq.Fraction(1, self.board.scale * f_size, color1, color2, bd_color1,
                                                     bd_color2, self.sim2_numbers, 2)
        self.sim2.set_offset(0, 0)
        self.sim2_canvas.painting = self.sim2.get_canvas().copy()

        # add labels
        self.board.add_unit(f_size // 2, f_size, 1, 1, classes.board.Label, str(self.numbers[0]), white, "", 25)
        self.nm1a = self.board.units[-1]
        self.nm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.nm1a.font_color = font_color

        self.board.add_unit(f_size // 2, f_size+1, 1, 1, classes.board.Label, str(self.numbers[1]), white, "", 25)
        self.nm1b = self.board.units[-1]
        self.nm1b.font_color = font_color

        self.board.add_unit(f_size-1, f_size, 2, 2, classes.board.Label, chr(215), white, "", 31)
        self.board.units[-1].font_color = font_color

        self.board.add_unit(f_size + f_size // 2, f_size, 1, 1, classes.board.Label, str(self.numbers2[0]), white, "", 25)
        self.nm2a = self.board.units[-1]
        self.nm2a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.nm2a.font_color = font_color

        self.board.add_unit(f_size + f_size // 2, f_size + 1, 1, 1, classes.board.Label, str(self.numbers2[1]), white, "", 25)
        self.nm2b = self.board.units[-1]
        self.nm2b.font_color = font_color

        self.board.add_unit(f_size*2, f_size, 2, 2, classes.board.Label, "=", white, "", 31)
        self.board.units[-1].font_color = font_color


        self.positions = [(f_size * 2 + 2 + f_size // 2-1, f_size),
                          (f_size * 2 + 2 + f_size // 2-1, f_size + 1),
                          (f_size * 3 + 1, f_size),
                          (f_size * 3 + 3, f_size),
                          (f_size * 3 + 3, f_size + 1),
                          (f_size * 3 + 2, f_size)]

        self.board.add_unit(self.positions[0][0], self.positions[0][1], 3, 1, classes.board.Label, str(self.sum_numbers[0]),
                            white, "", 25)
        self.sm1a = self.board.units[-1]
        self.sm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.sm1a.font_color = font_color

        self.board.add_unit(self.positions[1][0], self.positions[1][1], 3, 1, classes.board.Label, str(self.sum_numbers[1]),
                            white, "", 25)
        self.sm1b = self.board.units[-1]
        self.sm1b.font_color = font_color

        #optional
        self.board.add_unit(f_size * 3 + f_size // 2, f_size, 2, 2, classes.board.Label, "", white, "", 31)
        self.nmeq3 = self.board.units[-1]
        self.nmeq3.font_color = font_color
        self.positions2 = [(f_size * 3 + f_size // 2 + 4 - 1, f_size),
                           (f_size * 3 + f_size // 2 + 4 - 1, f_size + 1),
                           (f_size * 3 + f_size // 2 + 3, f_size)]
        self.board.add_unit(self.positions2[0][0], self.positions2[0][1], 3, 1, classes.board.Label, "", white, "", 25)
        self.sm3a = self.board.units[-1]
        self.sm3a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.sm3a.font_color = font_color

        self.board.add_unit(self.positions2[1][0], self.positions2[1][1], 3, 1, classes.board.Label, "", white, "", 25)
        self.sm3b = self.board.units[-1]
        self.sm3b.font_color = font_color

        #num 1 numerator
        self.board.add_unit(f_size // 2 - 1, f_size, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1alt = self.board.ships[-1]
        self.board.add_unit(f_size // 2 + 1, f_size, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1art = self.board.ships[-1]

        # num 1 denominator
        self.board.add_unit(f_size // 2 - 1, f_size + 1, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1blt = self.board.ships[-1]
        self.board.add_unit(f_size // 2 + 1, f_size + 1, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1brt = self.board.ships[-1]

        # num 2 numerator
        self.board.add_unit(f_size + f_size // 2 - 1, f_size, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2alt = self.board.ships[-1]
        self.board.add_unit(f_size + f_size // 2 + 1, f_size, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2art = self.board.ships[-1]

        # num 2 denominator
        self.board.add_unit(f_size + f_size // 2 - 1, f_size + 1, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2blt = self.board.ships[-1]
        self.board.add_unit(f_size + f_size // 2 + 1, f_size + 1, 1, 1, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2brt = self.board.ships[-1]

        self.update_fractions()
        self.update_arrows()

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

    def initialize_numbers(self, num1, num2, num3, num4):
        self.numbers = [num1, num3]
        self.numbers2 = [num2, num4]
        self.sum_numbers = [num1 * num2, num3 * num4]
        self.gcf = 1
        self.res2_numbers = [num1 * num2, num3 * num4]
        # simplifiy if needed print
        self.gcf = self.get_GCF(self.res2_numbers)
        if self.gcf > 1:
            self.sim2_numbers = [int(round(self.res2_numbers[0] / float(self.gcf))),
                                 int(round(self.res2_numbers[1] / float(self.gcf)))]
        else:
            self.sim2_numbers = [0, 0]

        for each in self.board.units:
            each.update_me = True
        self.mainloop.redraw_needed[0] = True


    def update_fractions(self):
        self.fraction.update_values(self.numbers)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()
        self.fraction2.update_values(self.numbers2)
        self.fraction2_canvas.painting = self.fraction2.get_canvas().copy()
        self.res2.update_values(self.res2_numbers)
        self.res2_canvas.painting = self.res2.get_canvas().copy()
        self.sim2.update_values(self.sim2_numbers)
        self.sim2_canvas.painting = self.sim2.get_canvas().copy()

        self.nm1a.set_value(str(self.numbers[0]))
        self.nm1b.set_value(str(self.numbers[1]))
        self.nm2a.set_value(str(self.numbers2[0]))
        self.nm2b.set_value(str(self.numbers2[1]))
        self.sm1a.set_value(str(self.sum_numbers[0]))
        self.sm1b.set_value(str(self.sum_numbers[1]))

        #if can be simplified - is more than 1 or has gcf > 1
        if self.sum_numbers[0] >= self.sum_numbers[1] or self.gcf > 1:
            self.nmeq3.set_value("=")
        else:
            self.nmeq3.set_value("")

        if self.sim2_numbers[0] == 0:
            v0 = ""
            v1 = ""
            v2 = ""
        else:
            v0 = "="
            v1 = str(self.sim2_numbers[0])
            v2 = str(self.sim2_numbers[1])

        self.nmeq3.set_value(v0)
        self.sm3a.set_value(v1)
        self.sm3b.set_value(v2)

        if self.sim2_numbers[0] == 0:
            self.sm3a.set_fraction_lines(top=False, bottom=False, color=self.bd_color1)
        else:
            self.sm3a.set_fraction_lines(top=False, bottom=True, color=self.bd_color1)

        # reposition
        self.board.move_unit(self.sm3a.unit_id, self.positions2[0][0], self.positions2[0][1])
        self.board.move_unit(self.sm3b.unit_id, self.positions2[1][0], self.positions2[1][1])
        
    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.lang.d["To multiply two fractions..."])

    def get_GCF(self, n):
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

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = self.board.active_ship
            if active == 0:
                self.change_fract_btn(self.numbers, -1, 0)
            elif active == 1:
                self.change_fract_btn(self.numbers, 1, 0)
            elif active == 2:
                self.change_fract_btn(self.numbers, 0, -1)
            elif active == 3:
                self.change_fract_btn(self.numbers, 0, 1)

            elif active == 4:
                self.change_fract_btn(self.numbers2, -1, 0)
            elif active == 5:
                self.change_fract_btn(self.numbers2, 1, 0)
            elif active == 6:
                self.change_fract_btn(self.numbers2, 0, -1)
            elif active == 7:
                self.change_fract_btn(self.numbers2, 0, 1)

            self.auto_check_reset()
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            self.check_result()
        elif event.type == pygame.KEYDOWN:
            self.auto_check_reset()

    def auto_check_reset(self):
        pass

    def change_fract_btn(self, ns, n1, n2):
        if n1 == -1:
            if ns[0] > 1:
                ns[0] -= 1
        elif n1 == 1:
            if ns[0] < self.max_num:
                ns[0] += 1
            if ns[0] >= ns[1]:
                ns[1] = ns[0]+1

        elif n2 == -1:
            if ns[1] > 2:
                ns[1] -= 1
            if ns[0] >= ns[1]:
                ns[0] = ns[1]-1

        elif n2 == 1:
            if ns[1] <= self.max_num:
                ns[1] += 1

        self.initialize_numbers(self.numbers[0], self.numbers2[0], self.numbers[1], self.numbers2[1])
        self.update_arrows()
        self.update_fractions()

    def update_arrows(self):
        # enable/dissable arrows
        if self.numbers[0] == 1:
            if self.nm1alt.img_src != "nav_l_mtsd.png":
                self.nm1alt.change_image("nav_l_mtsd.png")
        else:
            if self.nm1alt.img_src != "nav_l_mts.png":
                self.nm1alt.change_image("nav_l_mts.png")

        if self.numbers[0] == 11:
            if self.nm1art.img_src != "nav_r_mtsd.png":
                self.nm1art.change_image("nav_r_mtsd.png")
        else:
            if self.nm1art.img_src != "nav_r_mts.png":
                self.nm1art.change_image("nav_r_mts.png")

        if self.numbers2[0] == 1:
            if self.nm2alt.img_src != "nav_l_mtsd.png":
                self.nm2alt.change_image("nav_l_mtsd.png")
        else:
            if self.nm2alt.img_src != "nav_l_mts.png":
                self.nm2alt.change_image("nav_l_mts.png")

        if self.numbers2[0] == 11:
            if self.nm2art.img_src != "nav_r_mtsd.png":
                self.nm2art.change_image("nav_r_mtsd.png")
        else:
            if self.nm2art.img_src != "nav_r_mts.png":
                self.nm2art.change_image("nav_r_mts.png")

        if self.numbers[1] == 2:
            if self.nm1blt.img_src != "nav_l_mtsd.png":
                self.nm1blt.change_image("nav_l_mtsd.png")
        else:
            if self.nm1blt.img_src != "nav_l_mts.png":
                self.nm1blt.change_image("nav_l_mts.png")

        if self.numbers[1] == 12:
            if self.nm1brt.img_src != "nav_r_mtsd.png":
                self.nm1brt.change_image("nav_r_mtsd.png")
        else:
            if self.nm1brt.img_src != "nav_r_mts.png":
                self.nm1brt.change_image("nav_r_mts.png")

        if self.numbers2[1] == 2:
            if self.nm2blt.img_src != "nav_l_mtsd.png":
                self.nm2blt.change_image("nav_l_mtsd.png")
        else:
            if self.nm2blt.img_src != "nav_l_mts.png":
                self.nm2blt.change_image("nav_l_mts.png")

        if self.numbers2[1] == 12:
            if self.nm2brt.img_src != "nav_r_mtsd.png":
                self.nm2brt.change_image("nav_r_mtsd.png")
        else:
            if self.nm2brt.img_src != "nav_r_mts.png":
                self.nm2brt.change_image("nav_r_mts.png")

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
