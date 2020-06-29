# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.fraction_hq


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 7)

    def create_game_objects(self, level=1):
        self.board.decolorable = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.board.draw_grid = False

        if self.mainloop.scheme is None:
            h = random.randrange(0, 255, 5)
            white = (255, 255, 255)
            self.bg_col = white
            self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
            self.font_color = ex.hsv_to_rgb(h, 255, 100)
        else:
            h = 170
            self.font_color = self.mainloop.scheme.u_font_color  # ex.hsv_to_rgb(h,255,100)
            if self.mainloop.scheme.dark:
                self.bg_col = (0, 0, 1)
                self.color2 = (0, 0, 200)
            else:
                self.bg_col = (254, 254, 255)
                self.color2 = (0, 0, 200)

        if self.mainloop.scheme is not None:
            h1 = 170
            h2 = 40
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            h1 = h
            h2 = h1

            color1 = ex.hsv_to_rgb(h1, 150, 255)
            color2 = ex.hsv_to_rgb(h2, 30, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 187, 200)
            bd_color2 = ex.hsv_to_rgb(h2, 150, 225)

        data = [13, 5, 3]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        data.append(5)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        self.data = data
        self.layout.update_layout(data[0], data[1])
        self.board.set_animation_constraints(5, data[0] - 5, 0, data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        self.num_list = []
        self.num_list2 = []

        decimals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sign = "/"
        numbers = []

        # first number
        num1 = random.choice(decimals)
        num2 = 10
        numbers.append([num1, num2])
        expr = str(round(float(num1) / float(num2), 2))
        self.num_list.append(expr)
        self.num_list2.append(expr)

        # second fraction
        num1 = random.randrange(1, data[3])
        num2 = random.randrange(num1 + 1, data[3] + 1)
        numbers.append([num1, num2])
        expr = str(float(num1)) + sign + str(float(num2))
        self.num_list.append(expr)
        self.num_list2.append(["", str(num1), str(num2), ""])

        # create table to store 'binary' solution
        self.solution_grid = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.expression = [" " for x in range(data[0])]
        # find position of first door square
        xd = (data[0] - data[2]) // 2

        # add objects to the board
        self.board.add_unit(0, 0, 5, 5, classes.board.Label, "", self.bg_col, "", data[4])
        self.board.add_unit(8, 0, 5, 5, classes.board.Label, "", self.bg_col, "", data[4])

        size = self.board.scale
        center = [size // 2, size // 2]

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        door_color = ex.hsv_to_rgb(0, self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
        fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        for i in range(0, 2):
            x2 = xd + i * 2
            caption = self.num_list2[i]
            self.board.add_universal_unit(grid_x=x2, grid_y=2, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None, txt_align=(0, 0),
                                          font_type=data[4], multi_color=False, alpha=True, mode=1, immobilized=True)
            if i == 1:
                self.board.units[i + 2].init_m_painting()
                self.draw_fractions(self.board.units[i + 2].manual_painting, size, center, font_color[0])
                self.board.units[i + 2].update_me = True
            self.expression[x2] = str(self.num_list[i])
            if i < 1:
                self.solution_grid[x2 + 1] = 1

        signs = [" < ", " = ", " > "]

        for i in range(len(signs)):
            if len(signs) < data[0]:
                if i == 0 and len(signs) % 2 == 0:
                    x = data[0] // 2
                    y = 2
                else:
                    x = (data[0] - len(signs)) // 2
                    y = 0

            self.board.add_universal_unit(grid_x=x + i, grid_y=y, grid_w=1, grid_h=1, txt=signs[i],
                                          fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=fg_number_color,
                                          txt_align=(0, 0), font_type=data[4], multi_color=False, alpha=True,
                                          immobilized=False, fg_as_hover=True)
            self.units.append(self.board.ships[-1])
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()
            self.board.ships[i].readable = False

        ind = len(self.board.units)
        self.board.add_universal_unit(grid_x=xd + 1, grid_y=2, grid_w=1, grid_h=1, txt=None,
                                      fg_img_src=None, bg_img_src=bg_door_img_src, dc_img_src=None,
                                      bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                      bg_tint_color=door_color, fg_tint_color=None, txt_align=(0, 0),
                                      font_type=10, multi_color=False, alpha=True, immobilized=True, mode=2)
        self.board.all_sprites_list.move_to_front(self.board.units[ind])

        for i in range(2):
            self.fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * self.board.units[i].grid_w, color1, color2, bd_color1,
                                                             bd_color2, numbers[i], 1)
            self.board.units[i].painting = self.fraction.get_canvas().copy()

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Drag lt"])

    def draw_fractions(self, canvas, size, center, color):
        lh = max(int(size * 0.05), 2)
        la = self.mainloop.config.font_start_at_adjustment
        pygame.draw.line(canvas, self.font_color, [center[0] - size // 7, center[1] - lh // 2 + la],
                         [center[0] + size // 7, center[1] - lh // 2 + la], lh)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.check_result()

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        elif event.type == pygame.KEYUP:
            self.check_result()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill(self.bg_col)
        gd.BoardGame.update(self, game)

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def check_result(self):
        if self.board.grid[2] == self.solution_grid:
            found = None
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 2:  # if the sign is on line with expression
                    found = self.board.ships[i]
                    value = self.board.ships[i].value
                    if value == " = ":
                        value = "=="
                    self.expression[self.board.ships[i].grid_x] = value
            eval_string = ''.join(self.expression)
            eval_string.strip()
            if eval(eval_string):
                self.level.next_board()
                if found is not None:
                    found.set_display_check(True)
            else:
                if found is not None:
                    found.set_display_check(False)
        else:
            self.auto_check_reset()
        self.mainloop.redraw_needed[0] = True
