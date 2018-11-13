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
        self.level = lc.Level(self, mainloop, 15, 3)
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
            self.font_color2 = ex.hsv_to_rgb(5, 255, 240)
            self.font_color3 = ex.hsv_to_rgb(160, 255, 240)
            self.font_color4 = ex.hsv_to_rgb(5, 150, 240)
            self.font_color5 = ex.hsv_to_rgb(160, 150, 240)
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

        self.bd_color1 = bd_color1
        transp = (0, 0, 0, 0)
        data = [19, 8]
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

        # add cross simplification fields
        self.board.add_unit(0, 1, 1, 1, classes.board.Label, "a", white, "", 25)
        self.cs1a = self.board.units[-1]
        self.cs1a.font_color = self.font_color2

        self.board.add_unit(0, 6, 1, 1, classes.board.Label, "b", white, "", 25)
        self.cs1b = self.board.units[-1]
        self.cs1b.font_color = self.font_color3

        self.board.add_unit(8, 1, 1, 1, classes.board.Label, "c", white, "", 25)
        self.cs2a = self.board.units[-1]
        self.cs2a.font_color = self.font_color3

        self.board.add_unit(8, 6, 1, 1, classes.board.Label, "d", white, "", 25)
        self.cs2b = self.board.units[-1]
        self.cs2b.font_color = self.font_color2

        # add cross line
        mainloc = [[1, 2], [1, 4], [6, 2], [6, 4]]
        images = ["cross_line_la.png", "cross_line_ra.png", "cross_line_ra.png", "cross_line_la.png"]
        f_colors = [self.font_color2, self.font_color3, self.font_color3, self.font_color2]
        f2_colors = [self.font_color4, self.font_color5, self.font_color5, self.font_color4]
        self.cross_lines = []
        self.divisors = []

        for i in range(4):
            unit = classes.universal.Universal(board=self.board, grid_x=mainloc[i][0], grid_y=mainloc[i][1],
                                               grid_w=2, grid_h=2, bg_img_src=images[i], bg_color=transp,
                                               bg_tint_color=f_colors[i], immobilized=True)

            unit2 = classes.universal.Universal(board=self.board, grid_x=mainloc[i][0]+1, grid_y=mainloc[i][1],
                                                grid_w=1, grid_h=1, txt="", bg_color=transp, immobilized=True,
                                                font_colors=(f2_colors[i], ), font_type=2,
                                                txt_align=(2, 1))

            self.cross_lines.append(unit)
            self.board.all_sprites_list.add(unit)

            self.divisors.append(unit2)
            self.board.all_sprites_list.add(unit2)

        self.calc_added = False
        self.initialize_numbers(num1, num2, num3, num4)
        self.max_num = 11

        # add labels
        self.board.add_unit(1, 2, 2, 2, classes.board.Label, str(self.numbers[0]), white, "", 31)
        self.nm1a = self.board.units[-1]
        self.nm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.nm1a.font_color = self.font_color

        self.board.add_unit(1, 4, 2, 2, classes.board.Label, str(self.numbers[1]), white, "", 31)
        self.nm1b = self.board.units[-1]
        self.nm1b.font_color = self.font_color

        self.board.add_unit(4, 3, 1, 2, classes.board.Label, chr(215), white, "", 31)
        self.board.units[-1].font_color = self.font_color

        self.board.add_unit(6, 2, 2, 2, classes.board.Label, str(self.numbers2[0]), white, "", 31)
        self.nm2a = self.board.units[-1]
        self.nm2a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.nm2a.font_color = self.font_color

        self.board.add_unit(6, 4, 2, 2, classes.board.Label, str(self.numbers2[1]), white, "", 31)
        self.nm2b = self.board.units[-1]
        self.nm2b.font_color = self.font_color

        self.board.add_unit(9, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.board.units[-1].font_color = self.font_color

        # calculations added further down

        self.board.add_unit(13, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.board.units[-1].font_color = self.font_color

        self.positions = [(14, 3), (14, 4), (16, 3), (18, 3), (18, 3), (17, 3)]

        self.board.add_unit(self.positions[0][0], self.positions[0][1], 2, 1, classes.board.Label, str(self.sum_numbers[0]),
                            white, "", 25)
        self.sm1a = self.board.units[-1]
        self.sm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.sm1a.font_color = self.font_color

        self.board.add_unit(self.positions[1][0], self.positions[1][1], 2, 1, classes.board.Label, str(self.sum_numbers[1]),
                            white, "", 25)
        self.sm1b = self.board.units[-1]
        self.sm1b.font_color = self.font_color

        #optional
        self.board.add_unit(16, 3, 1, 2, classes.board.Label, "", white, "", 31)
        self.nmeq3 = self.board.units[-1]
        self.nmeq3.font_color = self.font_color

        self.board.add_unit(17, 3, 2, 1, classes.board.Label, "", white, "", 25)
        self.sm3a = self.board.units[-1]
        self.sm3a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.sm3a.font_color = self.font_color

        self.board.add_unit(17, 4, 2, 1, classes.board.Label, "", white, "", 25)
        self.sm3b = self.board.units[-1]
        self.sm3b.font_color = self.font_color

        #num 1 numerator
        self.board.add_unit(0, 2, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1alt = self.board.ships[-1]
        self.board.add_unit(3, 2, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1art = self.board.ships[-1]

        # num 1 denominator
        self.board.add_unit(0, 4, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1blt = self.board.ships[-1]
        self.board.add_unit(3, 4, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1brt = self.board.ships[-1]

        # num 2 numerator
        self.board.add_unit(5, 2, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2alt = self.board.ships[-1]
        self.board.add_unit(8, 2, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2art = self.board.ships[-1]

        # num 2 denominator
        self.board.add_unit(5, 4, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_l_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2blt = self.board.ships[-1]
        self.board.add_unit(8, 4, 1, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm2brt = self.board.ships[-1]

        # add calculations line
        self.board.add_unit(10, 3, 3, 1, classes.board.MultiColorLetters, "", white, "", 25)
        self.calc_line_1 = self.board.ships[-1]
        self.calc_line_1.set_fraction_lines(top=False, bottom=True, color=bd_color1)

        self.board.add_unit(10, 4, 3, 1, classes.board.MultiColorLetters, "", white, "", 25)
        self.calc_line_2 = self.board.ships[-1]

        self.calc_added = True
        self.initialize_numbers(self.numbers[0], self.numbers2[0], self.numbers[1], self.numbers2[1])
        self.update_fractions()
        self.update_arrows()

        for each in self.board.ships:
            each.readable = False
            each.immobilize()

        for each in self.cross_lines:
            self.board.all_sprites_list.move_to_front(each)

        for each in self.divisors:
            self.board.all_sprites_list.move_to_front(each)

    def simplify(self, num, gcf):
        if num == 1 and gcf is not None:
            self.csm[0][0] = self.numbers[0] // gcf
            self.csm[1][1] = self.numbers2[1] // gcf
            self.cs1a.set_value(str(self.csm[0][0]))
            self.cs2b.set_value(str(self.csm[1][1]))
            self.cross_lines[0].show()
            self.cross_lines[3].show()
            self.divisors[0].set_value("%s%s" % (chr(247), str(gcf)))
            self.divisors[3].set_value("%s%s" % (chr(247), str(gcf)))
        elif num == 1 and gcf is None:
            self.cs1a.set_value("")
            self.cs2b.set_value("")
            self.cross_lines[0].hide()
            self.cross_lines[3].hide()
            self.divisors[0].set_value("")
            self.divisors[3].set_value("")

        elif num == 2 and gcf is not None:
            self.csm[0][1] = self.numbers[1] // gcf
            self.csm[1][0] = self.numbers2[0] // gcf
            self.cs1b.set_value(str(self.csm[0][1]))
            self.cs2a.set_value(str(self.csm[1][0]))
            self.cross_lines[1].show()
            self.cross_lines[2].show()
            self.divisors[1].set_value("%s%s" % (chr(247), str(gcf)))
            self.divisors[2].set_value("%s%s" % (chr(247), str(gcf)))
        elif num == 2 and gcf is None:
            self.cs1b.set_value("")
            self.cs2a.set_value("")
            self.cross_lines[1].hide()
            self.cross_lines[2].hide()
            self.divisors[1].set_value("")
            self.divisors[2].set_value("")

    def initialize_numbers(self, num1, num2, num3, num4):
        self.numbers = [num1, num3]
        self.numbers2 = [num2, num4]

        # initial cross simplification
        gcf1 = self.get_GCF((num1, num4))
        gcf2 = self.get_GCF((num2, num3))

        # cross simplified numbers
        self.csm = [[None, None], [None, None]]
        if gcf1 > 1:
            self.simplify(1, gcf1)
        else:
            self.simplify(1, None)
        if gcf2 > 1:
            self.simplify(2, gcf2)
        else:
            self.simplify(2, None)

        self.sum_numbers = [num1 * num2, num3 * num4]
        if self.csm[0][0] is not None and self.csm[1][0] is not None:
            self.sum_numbers = [self.csm[0][0] * self.csm[1][0], self.csm[0][1] * self.csm[1][1]]
            if self.calc_added:
                self.calc_line_1.set_value("<1>%d<2> %s <3>%d" % (self.csm[0][0], chr(215), self.csm[1][0]))
                self.calc_line_1.set_font_colors(self.font_color2, self.font_color, self.font_color3)
                self.calc_line_2.set_value("<1>%d<2> %s <3>%d" % (self.csm[0][1], chr(215), self.csm[1][1]))
                self.calc_line_2.set_font_colors(self.font_color3, self.font_color, self.font_color2)

        elif self.csm[0][0] is not None:
            self.sum_numbers = [self.csm[0][0] * num2, num3 * self.csm[1][1]]
            if self.calc_added:
                self.calc_line_1.set_value("<1>%d<2> %s <3>%d" % (self.csm[0][0], chr(215), num2))
                self.calc_line_1.set_font_colors(self.font_color2, self.font_color, self.font_color)
                self.calc_line_2.set_value("<1>%d<2> %s <3>%d" % (num3, chr(215), self.csm[1][1]))
                self.calc_line_2.set_font_colors(self.font_color, self.font_color, self.font_color2)

        elif self.csm[0][1] is not None:
            self.sum_numbers = [num1 * self.csm[1][0], self.csm[0][1] * num4]
            if self.calc_added:
                self.calc_line_1.set_value("<1>%d<2> %s <3>%d" % (num1, chr(215), self.csm[1][0]))
                self.calc_line_1.set_font_colors(self.font_color, self.font_color, self.font_color3)
                self.calc_line_2.set_value("<1>%d<2> %s <3>%d" % (self.csm[0][1], chr(215), num4))
                self.calc_line_2.set_font_colors(self.font_color3, self.font_color, self.font_color)
        else:
            if self.calc_added:
                self.calc_line_1.set_value("<1>%d<2> %s <3>%d" % (num1, chr(215), num2))
                self.calc_line_1.set_font_colors(self.font_color, self.font_color, self.font_color)
                self.calc_line_2.set_value("<1>%d<2> %s <3>%d" % (num3, chr(215), num4))
                self.calc_line_2.set_font_colors(self.font_color, self.font_color, self.font_color)

        self.gcf = 1
        self.res2_numbers = self.sum_numbers[:]

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
        gd.BoardGame.handle(self, event)  # send event handling up
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
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
