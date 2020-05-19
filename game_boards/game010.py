# -*- coding: utf-8 -*-

import pygame
import random
import sys
import os
from math import sqrt

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.simple_vector as sv


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

        self.max_size = 99
        self.board.draw_grid = False

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.active_tool = 0
        self.active_letter = "A"
        self.active_word = "Apple"
        self.word_pos_y = 0
        self.var_brush = 1
        v = 255
        h = random.randrange(0, 255)
        self.letter_color2 = ex.hsv_to_rgb(h, 50, v)
        if self.mainloop.scheme is not None:
            self.bg_color = self.mainloop.scheme.u_color
            color = self.mainloop.scheme.u_color
        else:
            self.bg_color = [255, 255, 255]
            color = [255, 255, 255]

        llc = self.lang.alphabet_lc
        luc = self.lang.alphabet_uc
        l = len(llc)

        if l % 2 == 0:
            lh = l // 2
        else:
            lh = l // 2 + 1
        hue_step = 255 // (lh * 2)

        self.count = l * 2 + lh

        data = [35, l, 0, 8]
        if self.mainloop.m.game_variant == 0:
            font_size = 12
        elif self.mainloop.m.game_variant == 1:
            font_size = 20
        elif self.mainloop.m.game_variant == 2:
            font_size = 13
        elif self.mainloop.m.game_variant == 3:
            font_size = 13

        font_size2 = 14

        # stretch width to fit the screen size
        max_x_count = self.get_x_count(data[1], even=None)
        if max_x_count > 35:
            data[0] = max_x_count
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.unit_mouse_over = None
        self.units = []

        self.brush_size = scale // 2

        # canvas
        self.board.add_unit(10, 0, data[0] - 16, data[1], classes.board.Letter, "", color, "", font_size)
        self.canvas_block = self.board.ships[0]
        self.canvas_block.set_outline([0, 54, 229], 1)

        self.canvas_block.font3 = self.board.font_sizes[font_size2]

        label_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_tint_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        self.bg_color_active = ex.hsv_to_rgb(h, 200, 255)
        self.bg_color_done = ex.hsv_to_rgb(h, 50, 255)

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None
            if self.mainloop.scheme.dark:
                self.bg_color_active = ex.hsv_to_rgb(h, 255, 200)
                self.bg_color_done = ex.hsv_to_rgb(h, 255, 55)

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        x = 0
        y = 0

        for i in range(0, l):
            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=2, grid_h=2, txt=luc[i], alpha=True,
                                          fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=label_color, fg_tint_color=fg_tint_color, txt_align=(0, 0),
                                          font_type=25, multi_color=False, immobilized=True, fg_as_hover=True)
            self.units.append(self.board.ships[-1])
            self.board.add_universal_unit(grid_x=x + 4, grid_y=y, grid_w=2, grid_h=2, txt=llc[i], alpha=True,
                                          fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=label_color, fg_tint_color=fg_tint_color, txt_align=(0, 0),
                                          font_type=25, multi_color=False, immobilized=True, fg_as_hover=True)
            self.units.append(self.board.ships[-1])

            if i < lh:
                self.board.add_universal_unit(grid_x=x + 8, grid_y=y, grid_w=2, grid_h=2, txt=str(i), alpha=True,
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                              bg_tint_color=label_color, fg_tint_color=fg_tint_color, txt_align=(0, 0),
                                              font_type=25, multi_color=False, immobilized=True, fg_as_hover=True)
                self.units.append(self.board.ships[-1])

            y += 2

            if y >= l:
                x = 2
                y = 0

        # add new door
        self.board.add_universal_unit(grid_x=0, grid_y=0, grid_w=2, grid_h=2, txt=None, fg_img_src=None,
                                      bg_img_src=bg_door_img_src, dc_img_src=None, bg_color=(0, 0, 0, 0), alpha=True,
                                      border_color=None, font_color=None, bg_tint_color=font_color[0], immobilized=True,
                                      fg_tint_color=None, txt_align=(0, 0), font_type=10, multi_color=False, mode=2)

        self.board.add_door(data[0] - 1, 17, 1, 1, classes.board.Door, "", color, "")

        # color pallette
        h = 0
        s = 250
        v = 70
        # number of available color spaces minus 2 for black and white
        number_of_col_per_hue = 6  # number_of_colors // number_of_hues
        v_num = (255 - v) // number_of_col_per_hue
        # greyscale
        grey_v_num = 255 // 5

        grey_count = 0
        for j in range(0, data[1]):
            for i in range(data[0] - 6, data[0]):
                color2 = ex.hsv_to_rgb(h, s, v)
                self.board.add_unit(i, j, 1, 1, classes.board.Ship, "", color2, "", 2)
                if h < 249:
                    if i < data[0] - 1:
                        v += v_num
                    else:
                        v = 70
                        s = 250
                        h += hue_step
                else:
                    if grey_count == 0:
                        s = 0
                        v = 0
                        grey_count += 1
                    else:
                        v += grey_v_num

        self.prev_item = self.board.ships[1]
        self.active_letter = self.board.ships[1].value

        self.active_color = self.board.ships[173].initcolor
        self.board.ships[1].bg_tint_color = self.bg_color_active
        self.board.ships[1].update_me = True
        self.size_display = self.board.units[0]
        self.tool_door = self.board.units[-2]
        self.color_door = self.board.units[-1]
        self.btn_down = False

        # points
        self.p_first = [0, 0]
        self.p_last = [0, 0]
        self.p_prev = [0, 0]
        self.p_current = [0, 0]

        self.outline_all(1, 1)

        doors = [self.tool_door, self.color_door]
        for each in doors:
            each.door_outline = True
            each.perm_outline_color = [255, 0, 0]
            self.board.all_sprites_list.move_to_front(each)

        for each in self.board.ships:
            each.outline = False
            each.font_color = font_color
            each.immobilize()

        self.canvas = pygame.Surface(
            (self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1))
        self.canvas.fill(self.canvas_block.initcolor)
        self.paint_bg_letter()
        self.canvas_org = self.canvas.copy()

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change the x/y screen coordinates to grid coordinates
            pos = event.pos
            active = self.board.active_ship
            if event.button == 1:
                if self.prev_item is not None:
                    self.prev_item.bg_tint_color = self.bg_color_done
                    self.prev_item.update_me = True

                if active == 0:
                    self.btn_down = True
                    canvas_pos = [pos[0] - self.layout.game_left - 10 * self.layout.scale,
                                  pos[1] - self.layout.top_margin]
                    self.p_first = canvas_pos
                    self.p_prev = canvas_pos
                    self.p_current = canvas_pos
                    self.paint_pencil(0)
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                elif 0 < active < self.count + 1:
                    self.active_letter = self.board.ships[self.board.active_ship].value
                    self.board.ships[self.board.active_ship].bg_tint_color = self.bg_color_active
                    self.prev_item = self.board.ships[self.board.active_ship]

                    self.tool_door.set_pos(self.board.active_ship_pos)
                    self.paint_bg_letter()
                elif active > self.count:
                    self.active_color = self.board.ships[active].initcolor
                    self.color_door.set_pos(self.board.active_ship_pos)

        elif event.type == pygame.MOUSEMOTION and self.btn_down:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // self.layout.width
            row = (pos[1] - self.layout.top_margin) // self.layout.height
            if active == 0 and self.data[0] - 6 > column > 9 and row < self.data[1]:
                canvas_pos = [pos[0] - self.layout.game_left - 10 * self.layout.scale, pos[1] - self.layout.top_margin]
                self.p_prev = self.p_current
                self.p_current = canvas_pos
                self.paint_pencil(1)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // self.layout.width
            row = (pos[1] - self.layout.top_margin) // self.layout.height
            if active == 0 and self.data[0] - 6 > column > 9 and row < self.data[1]:
                # drop the new object onto the painting
                canvas_pos = [pos[0] - self.layout.game_left - 10 * self.layout.scale, pos[1] - self.layout.top_margin]
                self.p_last = canvas_pos
                self.paint_pencil(2)
            else:
                if self.btn_down:
                    self.screen_restore()
                    self.copy_to_screen()
            self.btn_down = False

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def paint_bg_letter(self):
        if sys.version_info < (3, 0):
            txt = self.active_letter
        else:
            txt = self.active_letter
        try:
            text = self.canvas_block.font.render("%s" % (txt), 1, (220, 220, 220, 0))

            font_x = ((self.board.scale * self.canvas_block.grid_w - self.canvas_block.font.size(txt)[0]) // 2)
            if self.mainloop.m.game_variant == 0:
                font_y = ((self.board.scale * self.canvas_block.grid_h - self.canvas_block.font.size(txt)[
                    1]) // 2) - 3 * self.board.scale
            else:
                font_y = (self.board.scale * self.canvas_block.grid_h - self.canvas_block.font.size(txt)[1]) // 2

            self.canvas.fill(self.bg_color)

            self.canvas.blit(text, (font_x, font_y))
            self.copy_to_screen()
        except:
            pass

    # states => mouse states => 0 - mouse_btn_down, 1 - mouse_move, 2 - mouse_btn_up

    def paint_pencil(self, state):
        if self.brush_size > 0:
            if state == 0:
                self.backup_canvas()
                pygame.draw.circle(self.canvas, self.active_color, self.p_current, self.brush_size // 2, 0)
                self.copy_to_screen()
            elif state == 1:
                width = self.brush_size
                if self.brush_size > 2:
                    if self.brush_size % 2 == 0:
                        r = self.brush_size // 2
                        width = self.brush_size + 3
                    else:
                        r = self.brush_size // 2
                        width = self.brush_size + 2
                    pygame.draw.circle(self.canvas, self.active_color, self.p_current, r, 0)
                if self.brush_size > 3:
                    self.draw_line(self.p_prev, self.p_current, self.brush_size, self.brush_size)
                else:
                    pygame.draw.line(self.canvas, self.active_color, self.p_prev, self.p_current, width)
                self.copy_to_screen()

    def draw_line(self, p1, p2, bs1, bs2):
        """Find points for the corners of the polygon using Tales Theorem
        and draw the polygon - rotated rectangle or trapezium and 2 circles at the ends of the 'line' """
        v = sv.Vector2.from_points(p1, p2)
        if v[0] != 0 or v[1] != 0:
            bs1 = bs1 // 2
            bs2 = bs2 // 2
            # vector length
            v_len = sqrt(v[0] * v[0] + v[1] * v[1])
            x1 = v[1] * bs1 / v_len
            y1 = v[0] * bs1 / v_len
            if bs1 != bs2:
                x2 = v[1] * bs2 / v_len
                y2 = v[0] * bs2 / v_len
            else:
                x2 = x1
                y2 = y1
            points = []
            points.append([int(p1[0] - x1), int(p1[1] + y1)])
            points.append([int(p1[0] + x1), int(p1[1] - y1)])

            points.append([int(p2[0] + x2), int(p2[1] - y2)])
            points.append([int(p2[0] - x2), int(p2[1] + y2)])
            pygame.draw.polygon(self.canvas, self.active_color, points)
            pygame.draw.aalines(self.canvas, self.active_color, True, points, 1)

            pygame.draw.circle(self.canvas, self.active_color, p1, bs1, 0)
            pygame.draw.circle(self.canvas, self.active_color, p2, bs2, 0)

    def backup_canvas(self):
        self.canvas_org = self.canvas_block.painting.copy()

    def copy_to_screen(self):
        self.canvas_block.painting = self.canvas.copy()
        self.canvas_block.update_me = True
        self.mainloop.redraw_needed[0] = True

    def screen_restore(self):
        self.canvas = self.canvas_org.copy()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
