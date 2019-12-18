# -*- coding: utf-8 -*-

import os
import random
import pygame

import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 8)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        images = ["fr_apple2.png", "fr_apple1.png", "fr_pear.png", "fr_orange.png", "fr_plum.png",
                  "fr_cherry.png", "fr_wmelon.png", "fr_lemon.png", "fr_banana.png", "fr_strawberry.png"]
        h_list = [15, 61, 44, 17, 199, 253, 60, 42, 35, 5]
        index = random.randint(0, 9)
        rand_image = os.path.join("fr", images[index])
        h = h_list[index]

        data = [11, 8]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        # data = [range_from, range_to, max_sum_range, sign]
        # rescale the number of squares horizontally to better match the screen width
        x_count = self.get_x_count(data[1], even=None)
        if x_count > 11:
            data[0] = x_count
        self.data = data

        self.board.set_animation_constraints(1, data[0], 0, data[1])

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        choice_list = [x for x in range(data[2], data[3])] * data[5]
        self.num_list = []
        self.num_list2 = []
        self.solution = []

        for i in range(data[1]):
            index = random.randrange(0, len(choice_list))
            self.num_list.append(choice_list[index])
            if data[6] == "n":
                self.solution.append(choice_list[index])
                second_num = 0
            elif data[6] == "+":
                second_range = data[4] - choice_list[index]
                second_num = random.randrange(1, second_range + 1)
                self.solution.append(choice_list[index] + second_num)
            else:
                second_range = choice_list[index] - 1
                second_num = random.randrange(1, second_range + 1)
                self.solution.append(choice_list[index] - second_num)

            self.num_list2.append(second_num)
            del (choice_list[index])

        if data[6] == "n":
            total = sum(self.num_list)
        elif data[6] == "+":
            total = sum(self.num_list) + sum(self.num_list2)
        else:
            total = sum(self.num_list) - sum(self.num_list2)

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

        for i in range(data[1]):
            if data[6] == "n":
                rhs = ""
            else:
                rhs = data[6] + str(self.num_list2[i])
            caption = str(self.num_list[i]) + rhs
            self.board.add_universal_unit(grid_x=0, grid_y=i, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[7], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=1)
            self.board.units[-1].checkable = True
            self.board.units[-1].init_check_images()

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "dc_hover_wb.png")
        else:
            if self.mainloop.scheme.dark:
                dc_img_src = os.path.join('unit_bg', "dc_hover_bw.png")
            else:
                dc_img_src = os.path.join('unit_bg', "dc_hover_wb.png")
        x = data[0] - 1
        y = 0
        for i in range(1, total + 1):
            if y >= data[1]:
                y = 0
                x -= 1
            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=None,
                                          fg_img_src=None, bg_img_src=rand_image, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                          bg_tint_color=None, fg_tint_color=None, dc_tint_color=number_color,
                                          txt_align=(0, 0), font_type=0, multi_color=False, alpha=True,
                                          immobilized=False, dc_as_hover=True, mode=0)
            self.board.ships[-1].audible = False
            self.board.ships[-1].outline = False
            self.units.append(self.board.ships[-1])
            y += 1

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def auto_check_reset(self):
        for each in self.board.units:
            each.set_display_check(None)

    def check_result(self, auto=False):
        self.result = []
        j = 0
        for each_list in self.board.grid:
            total = 0
            i = 0
            for each_item in each_list:
                if i > 0:
                    total += each_item
                i += 1
            self.result.append(total)
            if self.result[j] == self.solution[j]:
                self.board.units[j].set_display_check(True)
            else:
                self.board.units[j].set_display_check(False)

            j += 1

        if self.result == self.solution:
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True
