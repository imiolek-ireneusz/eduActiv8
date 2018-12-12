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
        data = [28, 8]
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

        num3 = random.randint(2, self.level_data[0])
        num2 = random.randint(2, self.level_data[0])
        num1 = random.randint(1, num3-1)
        num4 = random.randint(1, num2-1)

        self.response = [0, 1]

        self.current_txt = ""

        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        if self.lang.lang == "gr":
            self.qm = ";"
        else:
            self.qm = "?"

        # add cross simplification fields
        self.board.add_unit(0+7, 1, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs1a = self.board.units[-1]
        self.cs1a.font_color = self.font_color2

        self.board.add_unit(0+7, 6, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs1b = self.board.units[-1]
        self.cs1b.font_color = self.font_color3

        self.board.add_unit(8-2+7, 1, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs2a = self.board.units[-1]
        self.cs2a.font_color = self.font_color3

        self.board.add_unit(8-2+7, 6, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs2b = self.board.units[-1]
        self.cs2b.font_color = self.font_color2

        # add second simplification fields
        self.board.add_unit(0+10-2+7, 1, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs1xa = self.board.units[-1]
        self.cs1xa.font_color = self.font_color6

        self.board.add_unit(0+10-2+7, 6, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs1xb = self.board.units[-1]
        self.cs1xb.font_color = self.font_color6

        self.board.add_unit(8+8-2+7, 1, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs2xa = self.board.units[-1]
        self.cs2xa.font_color = self.font_color7

        self.board.add_unit(8+8-2+7, 6, 1, 1, classes.board.Label, "", white, "", 25)
        self.cs2xb = self.board.units[-1]
        self.cs2xb.font_color = self.font_color7

        # add cross line
        mainloc = [[1+7, 2], [1+7, 4], [4+7, 2], [4+7, 4]]
        mainloc2 = [[9+7, 2], [9+7, 4], [12+7, 2], [12+7, 4]]
        f_colors = [self.font_color2, self.font_color3, self.font_color3, self.font_color2]
        f2_colors = [self.font_color4, self.font_color5, self.font_color5, self.font_color4]

        f_colors2 = [self.font_color6, self.font_color6, self.font_color7, self.font_color7]
        f2_colors2 = [self.font_color8, self.font_color8, self.font_color9, self.font_color9]

        self.divisors = []
        self.divisors2 = []

        self.cross_lines = []
        self.cross_lines2 = []
        self.cross_lines3 = []

        for i in range(4):
            unit1c = classes.universal.Universal(board=self.board, grid_x=mainloc[i][0], grid_y=mainloc[i][1],
                                               grid_w=2, grid_h=2, bg_img_src="cross_line_la.png", bg_color=transp,
                                               bg_tint_color=f_colors[i], immobilized=True)

            unit1d = classes.universal.Universal(board=self.board, grid_x=mainloc[i][0]+1, grid_y=mainloc[i][1],
                                                grid_w=1, grid_h=1, txt="", bg_color=transp, immobilized=True,
                                                font_colors=(f2_colors[i], ), font_type=2,
                                                txt_align=(2, 1))

            unit2c = classes.universal.Universal(board=self.board, grid_x=mainloc2[i][0], grid_y=mainloc2[i][1],
                                               grid_w=2, grid_h=2, bg_img_src="cross_line_la.png", bg_color=transp,
                                               bg_tint_color=f_colors2[i], immobilized=True)

            unit2d = classes.universal.Universal(board=self.board, grid_x=mainloc2[i][0] + 1, grid_y=mainloc2[i][1],
                                                grid_w=1, grid_h=1, txt="", bg_color=transp, immobilized=True,
                                                font_colors=(f2_colors2[i],), font_type=2,
                                                txt_align=(2, 1))

            unit3c = classes.universal.Universal(board=self.board, grid_x=mainloc[i][0], grid_y=mainloc[i][1],
                                                 grid_w=2, grid_h=2, bg_img_src="cross_line_la.png", bg_color=transp,
                                                 bg_tint_color=f_colors2[i], immobilized=True)

            self.cross_lines.append(unit1c)
            self.board.all_sprites_list.add(unit1c)

            self.divisors.append(unit1d)
            self.board.all_sprites_list.add(unit1d)

            self.cross_lines2.append(unit2c)
            self.board.all_sprites_list.add(unit2c)

            self.divisors2.append(unit2d)
            self.board.all_sprites_list.add(unit2d)

            self.cross_lines3.append(unit3c)
            self.board.all_sprites_list.add(unit3c)

        self.max_num = 143

        # add division labels
        self.board.add_unit(0, 2, 2, 2, classes.board.Label, str(num1), white, "", 31)
        self.dnm1a = self.board.units[-1]
        self.dnm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.dnm1a.font_color = self.font_color

        self.board.add_unit(0, 4, 2, 2, classes.board.Label, str(num3), white, "", 31)
        self.dnm1b = self.board.units[-1]
        self.dnm1b.font_color = self.font_color

        self.board.add_unit(2, 3, 1, 2, classes.board.Label, chr(247), white, "", 31)
        self.board.units[-1].font_color = self.font_color

        self.board.add_unit(3, 2, 2, 2, classes.board.Label, str(num4), white, "", 31)
        self.dnm2a = self.board.units[-1]
        self.dnm2a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.dnm2a.font_color = self.font_color

        self.board.add_unit(3, 4, 2, 2, classes.board.Label, str(num2), white, "", 31)
        self.dnm2b = self.board.units[-1]
        self.dnm2b.font_color = self.font_color

        self.board.add_unit(6, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.board.units[-1].font_color = self.font_color

        # add inversed multiplication labels
        self.board.add_unit(1+7, 2, 2, 2, classes.board.Label, str(num1), white, "", 31)
        self.nm1a = self.board.units[-1]
        self.nm1a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.nm1a.font_color = self.font_color

        self.board.add_unit(1+7, 4, 2, 2, classes.board.Label, str(num3), white, "", 31)
        self.nm1b = self.board.units[-1]
        self.nm1b.font_color = self.font_color

        self.board.add_unit(3+7, 3, 1, 2, classes.board.Label, chr(215), white, "", 31)
        self.board.units[-1].font_color = self.font_color

        self.board.add_unit(4+7, 2, 2, 2, classes.board.Label, str(num2), white, "", 31)
        self.nm2a = self.board.units[-1]
        self.nm2a.set_fraction_lines(top=False, bottom=True, color=bd_color1)
        self.nm2a.font_color = self.font_color

        self.board.add_unit(4+7, 4, 2, 2, classes.board.Label, str(num4), white, "", 31)
        self.nm2b = self.board.units[-1]
        self.nm2b.font_color = self.font_color

        self.board.add_unit(7+7, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.board.units[-1].font_color = self.font_color

        # add labels for second simplifications
        self.board.add_unit(9+7, 2, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm1xa = self.board.units[-1]
        self.nm1xa.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=100)
        self.nm1xa.font_color = self.font_color

        self.board.add_unit(9+7, 4, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm1xb = self.board.units[-1]
        self.nm1xb.font_color = self.font_color

        self.board.add_unit(11+7, 2, 1, 2, classes.board.Label, chr(215), white, "", 31)
        self.board.units[-1].font_color = self.font_color
        self.board.units[-1].set_fraction_lines(top=False, bottom=True, color=bd_color1, length=100)

        self.board.add_unit(11+7, 4, 1, 2, classes.board.Label, chr(215), white, "", 31)
        self.board.units[-1].font_color = self.font_color

        self.board.add_unit(12+7, 2, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm2xa = self.board.units[-1]
        self.nm2xa.set_fraction_lines(top=False, bottom=True, color=bd_color1, length=100)
        self.nm2xa.font_color = self.font_color

        self.board.add_unit(12+7, 4, 2, 2, classes.board.Label, "", white, "", 31)
        self.nm2xb = self.board.units[-1]
        self.nm2xb.font_color = self.font_color

        # calculations added further down
        self.board.add_unit(15+7, 3, 1, 2, classes.board.Label, "=", white, "", 31)
        self.board.units[-1].font_color = self.font_color
        self.board.add_unit(17+7, 2, 3, 2, classes.board.Label, self.qm, white, "", 31)
        self.sm1a = self.board.units[-1]
        self.sm1a.set_outline(color=self.font_color, width=1)
        self.sm1a.checkable = True
        self.sm1a.init_check_images()

        self.sm1a.font_color = self.font_color
        self.board.add_unit(17+7, 4, 3, 2, classes.board.Label, self.qm, white, "", 31)
        self.sm1b = self.board.units[-1]
        self.sm1b.set_outline(color=self.font_color, width=1)
        self.sm1b.checkable = True
        self.sm1b.init_check_images()
        self.sm1b.font_color = self.font_color

        # response numerator
        self.board.add_unit(16+7, 2, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_l_mtsd.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1alt = self.board.ships[-1]
        self.board.add_unit(20+7, 2, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1art = self.board.ships[-1]

        # response denominator
        self.board.add_unit(16+7, 4, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_l_mtsd.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1blt = self.board.ships[-1]
        self.board.add_unit(20+7, 4, 1, 2, classes.board.ImgCenteredShip, "", transp, img_src='nav_r_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(color1)
        self.nm1brt = self.board.ships[-1]
        self.text_fields = [self.sm1a, self.sm1b]
        self.initialize_numbers(num1, num2, num3, num4)

        unit_fraction_line = classes.universal.Universal(board=self.board, grid_x=17+7, grid_y=3,
                                                         grid_w=3, grid_h=2, bg_img_src="fraction_line.png",
                                                         bg_color=transp,
                                                         bg_tint_color=self.font_color, immobilized=True)

        self.board.all_sprites_list.add(unit_fraction_line)

        for each in self.board.ships:
            each.readable = False
            each.immobilize()
        if self.level_data[1]:
            for each in self.cross_lines:
                self.board.all_sprites_list.move_to_front(each)
            for each in self.cross_lines2:
                self.board.all_sprites_list.move_to_front(each)
            for each in self.cross_lines3:
                self.board.all_sprites_list.move_to_front(each)

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

    def initialize_numbers(self, num1, num2, num3, num4):
        self.numbers = [num1, num3]
        self.numbers2 = [num2, num4]

        # try cross simplification
        self.step_1_cross_simplification(num1, num2, num3, num4)

        # if none of the numbers can be cross simplified try to simplify each fraction separately
        if self.csm1 == [[None, None], [None, None]]:
            self.set_s1_vert_simp_colors()
            self.step_1_vertical_simplification(num1, num2, num3, num4)
        else:
            self.set_s1_cross_simp_colors()
            self.hide_first_simp()

        # try to simplify the resulting fractions
        self.step_2_vertical_simplification()

        if self.level_data[5]:
            self.set_all_qm()

        for each in self.board.units:
            each.update_me = True
        self.mainloop.redraw_needed[0] = True

    def set_s1_cross_simp_colors(self):
        self.divisors[0].font_colors = (self.font_color2, )
        self.divisors[3].font_colors = (self.font_color2, )
        self.divisors[1].font_colors = (self.font_color3, )
        self.divisors[2].font_colors = (self.font_color3, )
        self.cs1a.font_color = self.font_color2
        self.cs2b.font_color = self.font_color2
        self.cs1b.font_color = self.font_color3
        self.cs2a.font_color = self.font_color3
        for each in self.divisors:
            each.update_me = True
            each.update(self.board)

    def set_s1_vert_simp_colors(self):
        self.divisors[0].font_colors = (self.font_color6, )
        self.divisors[3].font_colors = (self.font_color7, )
        self.divisors[1].font_colors = (self.font_color6, )
        self.divisors[2].font_colors = (self.font_color7, )
        self.cs1a.font_color = self.font_color6
        self.cs2b.font_color = self.font_color7
        self.cs1b.font_color = self.font_color6
        self.cs2a.font_color = self.font_color7
        for each in self.divisors:
            each.update_me = True
            each.update(self.board)

    def hide_first_simp(self):
        for each in self.cross_lines3:
            each.hide()

    def show_first_simp(self):
        for each in self.cross_lines3:
            each.show()

    def s1_cross_simplify(self, num, gcf):
        if num == 1 and gcf is not None:
            self.csm1[0][0] = self.numbers[0] // gcf
            self.csm1[1][1] = self.numbers2[1] // gcf
            if self.level_data[1]:
                self.cross_lines[0].show()
                self.cross_lines[3].show()
            if self.level_data[2]:
                self.divisors[0].set_value("%s%s" % (chr(247), str(gcf)))
                self.divisors[3].set_value("%s%s" % (chr(247), str(gcf)))
            if self.level_data[3]:
                self.cs1a.set_value(str(self.csm1[0][0]))
                self.cs2b.set_value(str(self.csm1[1][1]))
        elif num == 1 and gcf is None:
            self.cross_lines[0].hide()
            self.cross_lines[3].hide()
            self.cs1a.set_value("")
            self.cs2b.set_value("")
            self.divisors[0].set_value("")
            self.divisors[3].set_value("")

        elif num == 2 and gcf is not None:
            self.csm1[0][1] = self.numbers[1] // gcf
            self.csm1[1][0] = self.numbers2[0] // gcf
            if self.level_data[1]:
                self.cross_lines[1].show()
                self.cross_lines[2].show()
            if self.level_data[2]:
                self.divisors[1].set_value("%s%s" % (chr(247), str(gcf)))
                self.divisors[2].set_value("%s%s" % (chr(247), str(gcf)))
            if self.level_data[3]:
                self.cs1b.set_value(str(self.csm1[0][1]))
                self.cs2a.set_value(str(self.csm1[1][0]))
        elif num == 2 and gcf is None:
            self.cross_lines[1].hide()
            self.cross_lines[2].hide()
            self.cs1b.set_value("")
            self.cs2a.set_value("")
            self.divisors[1].set_value("")
            self.divisors[2].set_value("")

    def s2_vert_simplify(self, num, gcf):
        if num == 1 and gcf is not None:
            self.csm3[0][0] = self.simp_numbers[0] // gcf
            self.csm3[0][1] = self.simp_numbers[1] // gcf
            if self.level_data[1]:
                self.cross_lines2[0].show()
                self.cross_lines2[1].show()
            if self.level_data[2]:
                self.divisors2[0].set_value("%s%s" % (chr(247), str(gcf)))
                self.divisors2[1].set_value("%s%s" % (chr(247), str(gcf)))
            if self.level_data[3]:
                self.cs1xa.set_value(str(self.csm3[0][0]))
                self.cs1xb.set_value(str(self.csm3[0][1]))
        elif num == 1 and gcf is None:
            self.cross_lines2[0].hide()
            self.cross_lines2[1].hide()
            self.cs1xa.set_value("")
            self.cs1xb.set_value("")
            self.divisors2[0].set_value("")
            self.divisors2[1].set_value("")

        elif num == 2 and gcf is not None:
            self.csm3[1][0] = self.simp_numbers[2] // gcf
            self.csm3[1][1] = self.simp_numbers[3] // gcf
            if self.level_data[1]:
                self.cross_lines2[2].show()
                self.cross_lines2[3].show()
            if self.level_data[2]:
                self.divisors2[2].set_value("%s%s" % (chr(247), str(gcf)))
                self.divisors2[3].set_value("%s%s" % (chr(247), str(gcf)))
            if self.level_data[3]:
                self.cs2xa.set_value(str(self.csm3[1][0]))
                self.cs2xb.set_value(str(self.csm3[1][1]))
        elif num == 2 and gcf is None:
            self.cross_lines2[2].hide()
            self.cross_lines2[3].hide()
            self.cs2xa.set_value("")
            self.cs2xb.set_value("")
            self.divisors2[2].set_value("")
            self.divisors2[3].set_value("")

    def s1_vert_simplify(self, num, gcf):
        if num == 1 and gcf is not None:
            self.csm2[0][0] = self.numbers[0] // gcf
            self.csm2[0][1] = self.numbers[1] // gcf
            if self.level_data[1]:
                self.cross_lines3[0].show()
                self.cross_lines3[1].show()
            if self.level_data[2]:
                self.divisors[0].set_value("%s%s" % (chr(247), str(gcf)))
                self.divisors[1].set_value("%s%s" % (chr(247), str(gcf)))
            if self.level_data[3]:
                self.cs1a.set_value(str(self.csm2[0][0]))
                self.cs1b.set_value(str(self.csm2[0][1]))
        elif num == 1 and gcf is None:
            self.cross_lines3[0].hide()
            self.cross_lines3[1].hide()
            self.cs1a.set_value("")
            self.cs1b.set_value("")
            self.divisors[0].set_value("")
            self.divisors[1].set_value("")

        elif num == 2 and gcf is not None:
            self.csm2[1][0] = self.numbers2[0] // gcf
            self.csm2[1][1] = self.numbers2[1] // gcf
            if self.level_data[1]:
                self.cross_lines3[2].show()
                self.cross_lines3[3].show()
            if self.level_data[2]:
                self.divisors[2].set_value("%s%s" % (chr(247), str(gcf)))
                self.divisors[3].set_value("%s%s" % (chr(247), str(gcf)))
            if self.level_data[3]:
                self.cs2a.set_value(str(self.csm2[1][0]))
                self.cs2b.set_value(str(self.csm2[1][1]))
        elif num == 2 and gcf is None:
            self.cross_lines3[2].hide()
            self.cross_lines3[3].hide()
            self.cs2a.set_value("")
            self.cs2b.set_value("")
            self.divisors[2].set_value("")
            self.divisors[3].set_value("")

    def step_1_cross_simplification(self, num1, num2, num3, num4):
        # cross simplified numbers
        self.csm1 = [[None, None], [None, None]]

        # initial cross simplification
        gcf1 = self.get_GCF((num1, num4))
        gcf2 = self.get_GCF((num2, num3))

        if gcf1 > 1:
            self.s1_cross_simplify(1, gcf1)
        else:
            self.s1_cross_simplify(1, None)
        if gcf2 > 1:
            self.s1_cross_simplify(2, gcf2)
        else:
            self.s1_cross_simplify(2, None)

        # display resulting numbers after cross simplification - change font color if necessary
        if self.csm1[0][0] is not None and self.csm1[1][0] is not None:
            self.sum_numbers = [self.csm1[0][0] * self.csm1[1][0], self.csm1[0][1] * self.csm1[1][1]]
            self.simp_numbers = [self.csm1[0][0], self.csm1[0][1], self.csm1[1][0], self.csm1[1][1]]
            if self.level_data[1]:
                self.nm1xa.set_font_color(self.font_color2)
                self.nm1xb.set_font_color(self.font_color3)
                self.nm2xa.set_font_color(self.font_color3)
                self.nm2xb.set_font_color(self.font_color2)
            if self.level_data[4]:
                self.nm1xa.set_value(str(self.csm1[0][0]))
                self.nm1xb.set_value(str(self.csm1[0][1]))
                self.nm2xa.set_value(str(self.csm1[1][0]))
                self.nm2xb.set_value(str(self.csm1[1][1]))
            else:
                self.set_all_qm()

        elif self.csm1[0][0] is not None:
            self.sum_numbers = [self.csm1[0][0] * num2, num3 * self.csm1[1][1]]
            self.simp_numbers = [self.csm1[0][0], num3, num2, self.csm1[1][1]]
            self.nm1xb.set_value(str(num3))
            self.nm1xb.set_font_color(self.font_color)
            self.nm2xa.set_value(str(num2))
            self.nm2xa.set_font_color(self.font_color)

            if self.level_data[1]:
                self.nm1xa.set_font_color(self.font_color2)
                self.nm2xb.set_font_color(self.font_color2)

            if self.level_data[4]:
                self.nm1xa.set_value(str(self.csm1[0][0]))
                self.nm2xb.set_value(str(self.csm1[1][1]))
            else:
                self.nm1xa.set_value(self.qm)
                self.nm2xb.set_value(self.qm)
                self.nm1xa.set_outline(color=self.font_color, width=1)
                self.nm2xb.set_outline(color=self.font_color, width=1)
                self.text_fields.extend([self.nm1xa, self.nm2xb])
        elif self.csm1[0][1] is not None:
            self.sum_numbers = [num1 * self.csm1[1][0], self.csm1[0][1] * num4]
            self.simp_numbers = [num1, self.csm1[0][1], self.csm1[1][0], num4]
            self.nm1xa.set_value(str(num1))
            self.nm1xa.set_font_color(self.font_color)
            self.nm2xb.set_value(str(num4))
            self.nm2xb.set_font_color(self.font_color)

            if self.level_data[1]:
                self.nm1xb.set_font_color(self.font_color3)
                self.nm2xa.set_font_color(self.font_color3)

            if self.level_data[4]:
                self.nm1xb.set_value(str(self.csm1[0][1]))
                self.nm2xa.set_value(str(self.csm1[1][0]))
            else:
                self.nm1xb.set_value(self.qm)
                self.nm2xa.set_value(self.qm)
                self.nm1xb.set_outline(color=self.font_color, width=1)
                self.nm2xa.set_outline(color=self.font_color, width=1)
                self.text_fields.extend([self.nm1xb, self.nm2xa])
        else:
            self.sum_numbers = [num1 * num2, num3 * num4]
            self.simp_numbers = [num1, num3, num2, num4]
            self.nm1xa.set_value(str(num1))
            self.nm1xa.set_font_color(self.font_color)
            self.nm1xb.set_value(str(num3))
            self.nm1xb.set_font_color(self.font_color)
            self.nm2xa.set_value(str(num2))
            self.nm2xa.set_font_color(self.font_color)
            self.nm2xb.set_value(str(num4))
            self.nm2xb.set_font_color(self.font_color)

    def step_1_vertical_simplification(self, num1, num2, num3, num4):
        # cross simplified numbers
        self.csm2 = [[None, None], [None, None]]

        # initial simplification
        gcf1 = self.get_GCF((num1, num3))
        gcf2 = self.get_GCF((num2, num4))

        if gcf1 > 1:
            self.s1_vert_simplify(1, gcf1)
        else:
            self.s1_vert_simplify(1, None)
        if gcf2 > 1:
            self.s1_vert_simplify(2, gcf2)
        else:
            self.s1_vert_simplify(2, None)

        if self.csm2[0][0] is not None and self.csm2[1][0] is not None:
            self.sum_numbers = [self.csm2[0][0] * self.csm2[1][0], self.csm2[0][1] * self.csm2[1][1]]
            self.simp_numbers = [self.csm2[0][0], self.csm2[0][1], self.csm2[1][0], self.csm2[1][1]]
            if self.level_data[1]:
                self.nm1xa.set_font_color(self.font_color6)
                self.nm1xb.set_font_color(self.font_color6)
                self.nm2xa.set_font_color(self.font_color7)
                self.nm2xb.set_font_color(self.font_color7)

            if self.level_data[4]:
                self.nm1xa.set_value(str(self.csm2[0][0]))
                self.nm1xb.set_value(str(self.csm2[0][1]))
                self.nm2xa.set_value(str(self.csm2[1][0]))
                self.nm2xb.set_value(str(self.csm2[1][1]))
            else:
                self.set_all_qm()

        elif self.csm2[0][0] is not None:
            self.sum_numbers = [self.csm2[0][0] * self.csm2[0][1], num3 * num4]
            self.simp_numbers = [self.csm2[0][0], self.csm2[0][1], num2, num4]
            self.nm2xa.set_value(str(num2))
            self.nm2xa.set_font_color(self.font_color)
            self.nm2xb.set_value(str(num4))
            self.nm2xb.set_font_color(self.font_color)

            if self.level_data[1]:
                self.nm1xa.set_font_color(self.font_color6)
                self.nm1xb.set_font_color(self.font_color6)
            if self.level_data[4]:
                self.nm1xa.set_value(str(self.csm2[0][0]))
                self.nm1xb.set_value(str(self.csm2[0][1]))
            else:
                self.nm1xa.set_value(self.qm)
                self.nm1xb.set_value(self.qm)
                self.nm1xa.set_outline(color=self.font_color, width=1)
                self.nm1xb.set_outline(color=self.font_color, width=1)
                self.text_fields.extend([self.nm1xa, self.nm1xb])
        elif self.csm2[1][1] is not None:
            self.sum_numbers = [num1 * num2, self.csm2[1][0] * self.csm2[1][1]]
            self.simp_numbers = [num1, num3, self.csm2[1][0], self.csm2[1][1]]
            self.nm1xa.set_value(str(num1))
            self.nm1xa.set_font_color(self.font_color)
            self.nm1xb.set_value(str(num3))
            self.nm1xb.set_font_color(self.font_color)

            if self.level_data[1]:
                self.nm2xa.set_font_color(self.font_color7)
                self.nm2xb.set_font_color(self.font_color7)
            if self.level_data[4]:
                self.nm2xa.set_value(str(self.csm2[1][0]))
                self.nm2xb.set_value(str(self.csm2[1][1]))
            else:
                self.nm2xa.set_value(self.qm)
                self.nm2xb.set_value(self.qm)
                self.nm2xa.set_outline(color=self.font_color, width=1)
                self.nm2xb.set_outline(color=self.font_color, width=1)
                self.text_fields.extend([self.nm2xa, self.nm2xb])
        else:
            self.sum_numbers = [num1 * num2, num3 * num4]
            self.simp_numbers = [num1, num3, num2, num4]
            self.nm1xa.set_value(str(num1))
            self.nm1xa.set_font_color(self.font_color)
            self.nm1xb.set_value(str(num3))
            self.nm1xb.set_font_color(self.font_color)
            self.nm2xa.set_value(str(num2))
            self.nm2xa.set_font_color(self.font_color)
            self.nm2xb.set_value(str(num4))
            self.nm2xb.set_font_color(self.font_color)

    def step_2_vertical_simplification(self):
        # simplify the cross simplified result if possible
        self.csm3 = [[None, None], [None, None]]

        gcf1x = self.get_GCF((self.simp_numbers[0], self.simp_numbers[1]))
        gcf2x = self.get_GCF((self.simp_numbers[2], self.simp_numbers[3]))
        if gcf1x > 1:
            self.s2_vert_simplify(1, gcf1x)
        else:
            self.s2_vert_simplify(1, None)
        if gcf2x > 1:
            self.s2_vert_simplify(2, gcf2x)
        else:
            self.s2_vert_simplify(2, None)

        # calculate new result
        if self.csm3[0][0] is not None and self.csm3[1][1] is not None:
            self.sum_numbers = [self.csm3[0][0] * self.csm3[1][0], self.csm3[0][1] * self.csm3[1][1]]
        elif self.csm3[0][0] is not None:
            self.sum_numbers = [self.csm3[0][0] * self.simp_numbers[2], self.csm3[0][1] * self.simp_numbers[3]]
        elif self.csm3[1][1] is not None:
            self.sum_numbers = [self.simp_numbers[0] * self.csm3[1][0], self.simp_numbers[1] * self.csm3[1][1]]
        else:
            self.sum_numbers = [self.simp_numbers[0] * self.simp_numbers[2], self.simp_numbers[1] * self.simp_numbers[3]]

    def set_all_qm(self):
        self.nm1xa.set_value(self.qm)
        self.nm1xb.set_value(self.qm)
        self.nm2xa.set_value(self.qm)
        self.nm2xb.set_value(self.qm)
        self.nm1xa.set_outline(color=self.font_color, width=1)
        self.nm1xb.set_outline(color=self.font_color, width=1)
        self.nm2xa.set_outline(color=self.font_color, width=1)
        self.nm2xb.set_outline(color=self.font_color, width=1)
        self.text_fields.extend([self.nm1xa, self.nm1xb, self.nm2xa, self.nm2xb])

        self.nm1a.set_value(self.qm)
        self.nm1b.set_value(self.qm)
        self.nm2a.set_value(self.qm)
        self.nm2b.set_value(self.qm)
        self.nm1a.set_outline(color=self.font_color, width=1)
        self.nm1b.set_outline(color=self.font_color, width=1)
        self.nm2a.set_outline(color=self.font_color, width=1)
        self.nm2b.set_outline(color=self.font_color, width=1)
        self.text_fields.extend([self.nm1a, self.nm1b, self.nm2a, self.nm2b])

    def update_fractions(self):
        self.sm1a.set_value(str(self.response[0]))
        self.sm1b.set_value(str(self.response[1]))

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.lang.d["To divide a fraction by a fraction..."])

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
            if ns[1] > 1:
                ns[1] -= 1

        elif n2 == 1:
            if ns[1] <= self.max_num:
                ns[1] += 1

        if n1 != 0:
            self.toggle_active_fract(self.sm1a)
        elif n2 != 0:
            self.toggle_active_fract(self.sm1b)

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
        gd.BoardGame.update(self, game)  # rest of painting done by parent

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
