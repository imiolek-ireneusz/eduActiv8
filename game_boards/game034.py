# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 36, 5)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 23, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.board.decolorable = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        if self.mainloop.scheme is None:
            s = 100
            v = 255
            h = random.randrange(0, 255, 5)
            color0 = ex.hsv_to_rgb(h, 40, 255)  # highlight 1
            color1 = ex.hsv_to_rgb(h, 70, v)  # highlight 2
            color2 = ex.hsv_to_rgb(h, s, v)  # normal color
            color3 = ex.hsv_to_rgb(h, 230, 100)
            font_color = ex.hsv_to_rgb(h, 255, 140)
        else:
            s = 150
            v = 225
            h = 170
            color0 = ex.hsv_to_rgb(h, 40, 255)  # highlight 1
            color1 = ex.hsv_to_rgb(h, 70, v)  # highlight 2
            color2 = ex.hsv_to_rgb(h, s, v)  # normal color
            color3 = ex.hsv_to_rgb(h, 230, 100)
            font_color = self.mainloop.scheme.u_font_color

        # data = [x_count, y_count, range_from, range_to, max_sum_range, image]
        if self.level.lvl == 1:
            data = [23, 9]
        elif self.level.lvl == 2:
            data = [23, 9]
            color1 = color0
        elif self.level.lvl == 3:
            data = [23, 9]
            color1 = color2 = color0
        elif self.level.lvl == 4:
            data = [23, 9]
            color1 = color2 = color0
        elif self.level.lvl == 5:
            data = [23, 9]
            color2 = color1 = color0 = font_color
            color3 = (40, 40, 40)
        self.data = data
        self.board.set_animation_constraints(10, data[0], 0, data[1])

        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        num1 = random.randrange(1, 10)
        num2 = random.randrange(1, 10)
        self.solution = [num1, num2, num1 * num2]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        unique = set()
        for i in range(1, 10):
            for j in range(1, 10):
                if i == num1 and j == num2:
                    color = color0
                elif i == num1 or j == num2:
                    color = color1
                elif self.level.lvl == 2 and (i == num2 or j == num1):
                    color = color1
                else:
                    color = color2
                mul = i * j
                unique.add(mul)
                caption = str(mul)
                self.board.add_unit(i - 1, j - 1, 1, 1, classes.board.Label, caption, color, "", 2)
                self.board.units[-1].font_color = font_color
        self.board.add_unit(9, 0, 1, 9, classes.board.Obstacle, "", color3)
        unique = sorted(unique)
        # draw outline with selectable numbers
        self.multi = dict()
        x = 11
        y = 0

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
            door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        else:
            dc_img_src = None
            door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
            if self.mainloop.scheme.dark:
                door_bg_img_src = os.path.join('unit_bg', "universal_sq_door_no_trans.png")

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        h = 7

        for i in range(9):
            x += 1
            if self.level.lvl < 2:
                number_color = ex.hsv_to_rgb(h * i, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
                fg_number_color = ex.hsv_to_rgb(h * i, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)
                font_color = [ex.hsv_to_rgb(h * i, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
            self.multi[str(unique[i])] = i
            caption = str(unique[i])
            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=fg_number_color,
                                          txt_align=(0, 0), font_type=2, multi_color=False, alpha=True,
                                          immobilized=False, fg_as_hover=True)
            self.units.append(self.board.ships[-1])
            self.board.ships[-1].audible = False
            if self.lang.lang == "he":
                sv = self.lang.n2spk(unique[i])
                self.board.ships[-1].speaker_val = sv
                self.board.ships[-1].speaker_val_update = False
        x = 14
        y = 4
        captions = [str(num1), chr(215), "=", str(num1 * num2)]
        if self.level.lvl < 2:
            number_color = self.board.ships[self.solution[1] - 1].bg_tint_color
            font_color = self.board.ships[self.solution[1] - 1].font_colors

        for i in range(4):
            if i == 2:
                x += 1
            self.board.add_universal_unit(grid_x=x + i, grid_y=y, grid_w=1, grid_h=1, txt=captions[i],
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=2, multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=1)
            if self.level.lvl < 2:
                self.board.units[-1].font_colors = self.board.ships[self.solution[1] - 1].font_colors

        self.outline_all(0, 1)

        self.board.add_universal_unit(grid_x=16, grid_y=y, grid_w=1, grid_h=1, txt="",
                                      fg_img_src=None, bg_img_src=door_bg_img_src, dc_img_src=None,
                                      bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                      bg_tint_color=number_color, fg_tint_color=None,
                                      txt_align=(0, 0), font_type=2, multi_color=False, alpha=True,
                                      immobilized=True, fg_as_hover=False, mode=2)

        self.home_square = self.board.units[86]
        self.home_square.checkable = True
        self.home_square.init_check_images()
        self.home_square.door_outline = True
        if self.level.lvl < 2:
            self.home_square.font_colors = self.board.ships[self.solution[1] - 1].font_colors

        self.board.all_sprites_list.move_to_front(self.home_square)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if self.show_msg == False:
            if event.type == pygame.KEYDOWN and (event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER):
                lhv = len(self.home_square.value)
                self.changed_since_check = True
                if event.key == pygame.K_BACKSPACE:
                    if lhv > 0:
                        self.home_square.value = self.home_square.value[0:lhv - 1]
                elif not self.board.grid[4][16]:
                    char = event.unicode
                    if len(char) > 0 and char in self.digits:
                        self.home_square.value = char
                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True
            elif event.type == pygame.MOUSEMOTION and self.drag:
                if self.board.grid[4][16]:
                    self.home_square.value = ""
                    self.home_square.update_me = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for each in self.board.units:
                    if each.is_door is True:
                        self.board.all_sprites_list.move_to_front(each)
                if self.board.grid[4][16]:
                    self.home_square.value = ""
                    self.home_square.update_me = True
                    self.check_result()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                self.check_result()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.auto_check_reset()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def auto_check_reset(self):
        self.home_square.set_display_check(None)

    def check_result(self):
        if self.board.grid[4][16]:
            sol = self.board.ships[self.solution[1] - 1]
            if sol.grid_x == 16 and sol.grid_y == 4:
                self.passed()
                self.home_square.set_display_check(True)
            else:
                self.home_square.set_display_check(False)
        else:
            if self.home_square.value != "" and (int(self.home_square.value) == self.solution[1]):
                self.passed()
                self.home_square.set_display_check(True)
            else:
                self.home_square.set_display_check(False)
        self.mainloop.redraw_needed[0] = True

    def passed(self):
        self.level.next_board(self.d["Perfect!"])

