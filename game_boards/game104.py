# -*- coding: utf-8 -*-

import random
import pygame
import os

import classes.board
import classes.drw.percentage_multi_hq
import classes.game_driver as gd
import classes.level_controller as lc
import classes.extras as ex


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 10, 6)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 8)

    def create_game_objects(self, level=1):
        self.max_size = 99
        self.board.draw_grid = False

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color
        else:
            white = (255, 255, 255)

        data = [12, 7]
        self.data = data

        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]

        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True

        self.unit_mouse_over = None
        self.units = []

        self.board.board_bg.line_color = (20, 20, 20)

        # level_data[start, step, count]
        if self.level.lvl == 1:
            level_data = [10, 10, 2]
        elif self.level.lvl == 2:
            level_data = [10, 10, 3]
        elif self.level.lvl == 3:
            level_data = [5, 5, 3]
        elif self.level.lvl == 4:
            level_data = [5, 5, 4]
        elif self.level.lvl == 5:
            level_data = [5, 5, 5]
        else:
            level_data = [5, 1, 5]

        self.number_count = level_data[2]
        self.numbers = self.get_numbers(self.number_count, level_data[0], level_data[1])
        self.numbers_sh = self.numbers[:]
        random.shuffle(self.numbers_sh)

        self.positions = [[2, 4], [2, 3, 4], [1, 2, 4, 5], [1, 2, 3, 4, 5]]

        hues = []
        step = 255 // self.number_count
        hues.append(random.randint(5, 245))
        for i in range(1, self.number_count):
            hues.append((hues[0] + step * i) % 255)

        colors = [ex.hsv_to_rgb(hues[i], 150, 250) for i in range(self.number_count)]
        b_colors = [ex.hsv_to_rgb(hues[i], 150, 220) for i in range(self.number_count)]

        self.board.add_unit(0, 0, data[1], data[1], classes.board.Label, "", white, "", 0)
        self.fraction_canvas = self.board.units[-1]
        self.fraction = classes.drw.percentage_multi_hq.Percentage(1, self.board.scale * data[1],
                                                                   colors, b_colors, self.numbers)
        self.fraction_canvas.painting = self.fraction.get_canvas().copy()

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
            font_color = [(0, 0, 0)]
        else:
            dc_img_src = None
            font_color = [self.mainloop.scheme.u_font_color]

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_rect_img_src = os.path.join('unit_bg', "universal_r2x1_bg_plain_color.png")
        frame_img_src = os.path.join('unit_bg', "universal_r2x1_door.png")
        bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        number_color = ex.hsv_to_rgb(self.mainloop.cl.get_interface_hue(), self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        fg_number_color = ex.hsv_to_rgb(self.mainloop.cl.get_interface_hue(), self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        for i in range(self.number_count):
            # colour label
            tint_color = ex.hsv_to_rgb(hues[i], self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
            self.board.add_universal_unit(grid_x=data[1] + 1, grid_y=self.positions[self.number_count-2][i],
                                          grid_w=2, grid_h=1, txt="", fg_img_src=frame_img_src,
                                          bg_img_src=bg_rect_img_src, dc_img_src=None, bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=None, bg_tint_color=tint_color,
                                          fg_tint_color=None, txt_align=(0, 0), font_type=10,
                                          multi_color=False, alpha=True, immobilized=True, fg_as_hover=False, mode=1)

            # response placeholder
            door_bg_tint = ex.hsv_to_rgb(hues[i], self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
            self.board.add_universal_unit(grid_x=data[1] + 3, grid_y=self.positions[self.number_count-2][i],
                                          grid_w=1, grid_h=1, txt=None, fg_img_src=None, bg_img_src=bg_door_img_src,
                                          dc_img_src=None, bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                          bg_tint_color=door_bg_tint, fg_tint_color=None, txt_align=(0, 0),
                                          font_type=10, multi_color=False, alpha=True, immobilized=True, mode=2)

            # potential response
            self.board.add_universal_unit(grid_x=data[1] + i + (data[0] - data[1] - self.number_count) // 2, grid_y=0,
                                          grid_w=1, grid_h=1, txt=str(self.numbers_sh[i]) + "%", fg_img_src=bg_img_src,
                                          bg_img_src=bg_img_src, dc_img_src=dc_img_src, bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=font_color, bg_tint_color=number_color,
                                          fg_tint_color=fg_number_color, txt_align=(0, 0), font_type=3,
                                          multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)

            self.units.append(self.board.ships[-1])
            self.board.ships[-1].solution = self.numbers_sh[i]
            self.board.ships[-1].highlight = False
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()

        for each in self.board.ships:
            each.readable = False

    def get_numbers(self, count, dist, step):
        redraw = True
        nums = [x for x in range(dist, dist*(count+1), dist)]
        nums_total = sum(nums)
        remainder = 100 - nums_total
        if remainder > 0:
            while redraw:
                redraw = False
                l2 = nums[:]
                remainder = 100 - nums_total
                for i in range(count-1):
                    if remainder > 0:
                        a = random.randrange(0, remainder, step)
                        remainder -= a
                        l2[i] += a
                if remainder > 0:
                    l2[-1] += remainder
                l2s = sorted(l2)
                for i in range(1, count):
                    if l2s[i-1] > l2s[i] - dist:
                        redraw = True
                        break
        return l2

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for each in self.board.units:
                self.board.all_sprites_list.move_to_front(each)
            self.auto_check()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def auto_check(self):
        ready = True
        for each in self.board.ships:
            if each.grid_x != self.data[1] + 3 or each.grid_y == 0 or each.grid_x == 6:
                ready = False
        if ready:
            self.check_result()

    def check_result(self):
        all_correct = True
        for each in self.board.ships:
            if each.grid_x == self.data[1] + 3 and 0 < each.grid_y < 6:
                correct = False
                for i in range(len(self.positions[self.number_count-2])):
                    if each.grid_y == self.positions[self.number_count-2][i] and each.solution == self.numbers[i]:
                        each.set_display_check(True)
                        correct = True
                if not correct:
                    each.set_display_check(False)
                    all_correct = False
            else:
                each.set_display_check(False)
                all_correct = False

        if all_correct:
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True
