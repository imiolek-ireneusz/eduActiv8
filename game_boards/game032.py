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
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 6)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 1, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        # data = [horizontal_number_of_units, bottom_limit, top_limit, number_count, font_size]
        data = [11, 5]
        data.extend(self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group, self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        self.data = data
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        self.num_list = []
        if self.mainloop.m.game_variant == 0:
            self.ob_count = data[5]
            for i in range(self.ob_count):
                index = random.randrange(data[3], data[4])
                self.num_list.append(str(index))
        elif self.mainloop.m.game_variant == 1:
            self.num_list2 = []

            self.ob_count = data[4]

            sign = ["+", "-"]

            for i in range(self.ob_count):
                num1 = random.randrange(1, data[3])
                rand_sign = sign[random.randrange(2)]
                if rand_sign == "+":
                    while True:
                        num2 = random.randrange(0, data[3])
                        if num1 + num2 < data[5]:
                            break
                else:
                    num2 = random.randrange(0, num1)
                expr = str(num1) + rand_sign + str(num2)
                self.num_list.append(expr)

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]
        self.expression = ["" for x in range(data[0])]

        # find position of first door square
        xd = (data[0] - data[2]) // 2

        # add objects to the board
        h = random.randrange(0, 255, 5)

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
            dc_tall_img_src = os.path.join('unit_bg', "universal_r1x3_dc.png")
        else:
            dc_img_src = None
            dc_tall_img_src = None

        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_tall_img_src = os.path.join('unit_bg', "universal_r1x3_bg.png")

        if self.mainloop.scheme is None:
            door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        else:
            door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
            if self.mainloop.scheme.dark:
                door_bg_img_src = os.path.join('unit_bg', "universal_sq_door_no_trans.png")

        for i in range(0, self.ob_count):
            x2 = xd + i * 2
            caption = self.num_list[i]
            self.board.add_universal_unit(grid_x=x2, grid_y=2, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[6], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=1)
            self.solution_grid[x2] = 1
            self.expression[x2] = str(self.num_list[i])
            if i < self.ob_count - 1:
                self.solution_grid[x2 + 1] = 1

        if h > 125:
            h = random.randrange(0, h - 25, 5)
        else:
            h = random.randrange(h + 25, 255, 5)

        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        indu = len(self.board.units)
        inds = len(self.board.ships)
        self.door_indexes = []
        for i in range(0, self.ob_count - 1):
            self.board.add_universal_unit(grid_x=xd + i * 2 + 1, grid_y=1, grid_w=1, grid_h=3, txt=[">", "=", "<"],
                                          fg_img_src=bg_tall_img_src, bg_img_src=bg_tall_img_src,
                                          dc_img_src=dc_tall_img_src, bg_color=(0, 0, 0, 0), border_color=None,
                                          font_color=font_color, bg_tint_color=number_color,
                                          fg_tint_color=fg_number_color, txt_align=(0, 0), font_type=data[6],
                                          multi_color=False, alpha=True, immobilized=False, fg_as_hover=True, mode=0)

            self.units.append(self.board.ships[-1])
            self.board.add_universal_unit(grid_x=xd + i * 2 + 1, grid_y=2, grid_w=1, grid_h=1, txt="",
                                          fg_img_src=None, bg_img_src=door_bg_img_src, dc_img_src=None,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                          bg_tint_color=(255, 0, 0), fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[6], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=2)

            self.board.units[indu + i].checkable = True
            self.board.units[indu + i].init_check_images()
            self.door_indexes.append(indu + i)
            self.board.ships[inds + i].readable = False
            self.board.all_sprites_list.move_to_front(self.board.units[indu + i])
        self.changed_since_check = True
        self.outline_all(0, 1)

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Drag the slider"])

    def auto_check_reset(self):
        for each in self.board.units:
            if each.is_door:
                each.update_me = True
                each.set_display_check(None)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        all_true = True
        for i in range(len(self.board.ships)):
            # calculate the active value based on grid_y of the slider
            value = self.board.ships[i].value[2 - self.board.ships[i].grid_y]
            if value == "=":
                value = "=="
            self.expression[self.board.ships[i].grid_x] = value
            mini_expression = self.expression[self.board.ships[i].grid_x - 1] + value + self.expression[self.board.ships[i].grid_x + 1]
            if eval(mini_expression) is True:
                self.board.units[self.door_indexes[i]].set_display_check(True)
            else:
                self.board.units[self.door_indexes[i]].set_display_check(False)
                all_true = False
        if all_true:
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True

