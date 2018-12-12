# -*- coding: utf-8 -*-

import pygame
from math import sqrt

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.simple_vector as sv


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 2)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)
        self.max_size = 99
        self.history_capacity = 25

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.board.decolorable = False
        self.board.draw_grid = False
        self.active_tool = 0
        self.brush_size = 5
        self.brush_height = 4  # used by brush2 only
        self.var_brush = 1
        self.sizing = False
        if self.level.lvl == 1:
            self.horizontal = True
        else:
            self.horizontal = False

        self.history = []
        self.undo_step = 0
        font_color = (0, 54, 229)
        if self.mainloop.scheme is not None:
            font_color = self.mainloop.scheme.u_font_color
            if self.mainloop.scheme.dark:
                self.bg_color = [0, 0, 0]
                color = [0, 0, 0]
            else:
                self.bg_color = [255, 255, 255]
                color = [255, 255, 255]
        else:
            self.bg_color = [255, 255, 255]
            color = [255, 255, 255]
        if self.horizontal:
            data = [38, 27]
        else:
            data = [20, 38]
        self.slider_color = [50, 50, 250]
        self.slider_bg_col = [200, 200, 255]

        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=None)
        if x_count > data[0]:
            data[0] = x_count
        self.data = data

        self.vis_buttons = [0, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        if self.horizontal:
            txt = self.d["brush size"] + ": " + str(self.brush_size)
            canvas_pos = [0, 3, data[0], data[1] - 6]
            self.slider_min = self.mainloop.size[0] - self.layout.game_margin - 8 * self.layout.scale
            self.slider_max = self.mainloop.size[0] - self.layout.game_margin - 2
        else:
            txt = str(self.brush_size)
            canvas_pos = [3, 0, data[0] - 6, data[1]]
            self.slider_max = self.layout.game_pos[1] + self.layout.game_pos[3]
            self.slider_min = self.slider_max - 7 * self.layout.scale

        self.board.add_unit(canvas_pos[0], canvas_pos[1], canvas_pos[2], canvas_pos[3],
                            classes.board.Letter, "", color, "", 2)
        self.canvas_block = self.board.ships[0]
        self.canvas_block.set_outline([0, 54, 229], 1)
        # tools
        images = ["paint_pencil.png", "paint_brush.png", "paint_wide_brush.png", "paint_line.png", "paint_rect.png",
                  "paint_circle.png", "paint_eraser.png", "paint_bucket.png"]
        if self.horizontal:
            j = 7
            for i in range(8):
                self.board.add_unit(j, 0, 3, 3, classes.board.ImgShip, "", color, images[i], alpha=True)
                j += 3

            size_disp_pos = [[data[0] - 8, 1, 8, 2], [data[0] - 8, 0, 8, 1]]
        else:
            j = 6
            for i in range(8):
                self.board.add_unit(0, j, 3, 3, classes.board.ImgShip, "", color, images[i], alpha=True)
                j += 3
            size_disp_pos = [[0, data[1] - 7, 3, 7], [0, data[1] - 8, 3, 1]]

        self.board.add_unit(size_disp_pos[0][0], size_disp_pos[0][1], size_disp_pos[0][2], size_disp_pos[0][3],
                            classes.board.Letter, "", color, "", 0)
        self.size_slider = self.board.ships[-1]

        self.board.add_unit(size_disp_pos[1][0], size_disp_pos[1][1], size_disp_pos[1][2], size_disp_pos[1][3],
                            classes.board.Label, txt, color, "", 0)
        self.board.units[-1].font_color = font_color

        self.size_display = self.board.units[-1]
        self.board.add_unit(0, 0, 3, 3, classes.board.ImgShip, "", color, "paint_undo.png", alpha=True)
        if self.horizontal:
            self.board.add_unit(3, 0, 3, 3, classes.board.ImgShip, "", color, "paint_redo.png", alpha=True)
            self.board.add_door(7, 0, 3, 3, classes.board.Door, "", color, "")

            self.step = 256.0 / (self.data[0] - 1)
            self.custom_color_hsv = [data[0] // 2 * self.step, (data[0] - 1) * self.step, (data[0] - 1) * self.step]
        else:
            self.board.add_unit(0, 3, 3, 3, classes.board.ImgShip, "", color, "paint_redo.png", alpha=True)
            self.board.add_door(0, 6, 3, 3, classes.board.Door, "", color, "")

            self.step = 256.0 / (self.data[1] - 1)
            self.custom_color_hsv = [data[1] // 2 * self.step, (data[1] - 1) * self.step, (data[1] - 1) * self.step]

        self.tool_door = self.board.units[-1]
        self.color_start = len(self.board.ships)

        self.h_units = []
        self.s_units = []
        self.v_units = []

        if self.horizontal:
            door_loc = [[data[0] // 2, data[1] - 3], [data[0] - 1, data[1] - 2], [data[0] - 1, data[1] - 1]]
            self.board.add_unit(0, data[1] - 3, 1, 1, classes.board.Label, "H", color, "", 0)
            self.board.add_unit(0, data[1] - 2, 1, 1, classes.board.Label, "S", color, "", 0)
            self.board.add_unit(0, data[1] - 1, 1, 1, classes.board.Label, "V", color, "", 0)

            # hue selectors
            for i in range(0, self.data[0]-1):
                c0 = ex.hsv_to_rgb(self.step * i, 255, 255)
                self.board.add_unit(i + 1, data[1] - 3, 1, 1, classes.board.Ship, "", c0, "", 0)
                self.h_units.append(self.board.ships[-1])

            # saturation selectors
            for i in range(0, self.data[0]-1):
                c1 = ex.hsv_to_rgb(0, self.step * i, 255)
                self.board.add_unit(i + 1, data[1] - 2, 1, 1, classes.board.Ship, "", c1, "", 0)
                self.s_units.append(self.board.ships[-1])

            # vibrance selectors
            for i in range(0, self.data[0]-1):
                c2 = ex.hsv_to_rgb(0, 255, self.step * i)
                self.board.add_unit(i + 1, data[1] - 1, 1, 1, classes.board.Ship, "", c2, "", 0)
                self.v_units.append(self.board.ships[-1])
        else:
            door_loc = [[data[0] - 3, data[1] // 2], [data[0] - 2, data[1] - 1], [data[0] - 1, data[1] - 1]]
            self.board.add_unit(data[0] - 3, 0, 1, 1, classes.board.Label, "H", color, "", 0)
            self.board.add_unit(data[0] - 2, 0, 1, 1, classes.board.Label, "S", color, "", 0)
            self.board.add_unit(data[0] - 1, 0, 1, 1, classes.board.Label, "V", color, "", 0)

            # hue selectors
            for i in range(0, self.data[1] - 1):
                c0 = ex.hsv_to_rgb(self.step * i, 255, 255)
                self.board.add_unit(data[0] - 3, i + 1, 1, 1, classes.board.Ship, "", c0, "", 0)
                self.h_units.append(self.board.ships[-1])

            # saturation selectors
            for i in range(0, self.data[1] - 1):
                c1 = ex.hsv_to_rgb(0, self.step * i, 255)
                self.board.add_unit(data[0] - 2, i + 1, 1, 1, classes.board.Ship, "", c1, "", 0)
                self.s_units.append(self.board.ships[-1])

            # vibrance selectors
            for i in range(0, self.data[1] - 1):
                c2 = ex.hsv_to_rgb(0, 255, self.step * i)
                self.board.add_unit(data[0] - 1, i + 1, 1, 1, classes.board.Ship, "", c2, "", 0)
                self.v_units.append(self.board.ships[-1])

        for i in range(1, 4):
            self.board.units[-i].font_color = font_color

        for each in self.board.ships:
            each.outline = False
            each.immobilize()
            each.readable = False

        self.board.add_door(door_loc[0][0], door_loc[0][1], 1, 1, classes.board.Door, "", color, "")
        self.h_door = self.board.units[-1]
        self.h_door.door_outline = True
        self.h_door.perm_outline_color = (200, 0, 0)
        self.board.all_sprites_list.move_to_front(self.h_door)

        self.board.add_door(door_loc[1][0], door_loc[1][1], 1, 1, classes.board.Door, "", color, "")
        self.s_door = self.board.units[-1]
        self.s_door.door_outline = True
        self.s_door.perm_outline_color = (200, 0, 0)
        self.board.all_sprites_list.move_to_front(self.s_door)

        self.board.add_door(door_loc[2][0], door_loc[2][1], 1, 1, classes.board.Door, "", color, "")
        self.v_door = self.board.units[-1]
        self.v_door.door_outline = True
        self.v_door.perm_outline_color = (200, 0, 0)
        self.board.all_sprites_list.move_to_front(self.v_door)

        self.btn_down = False
        self.paint_function = [self.paint_pencil, self.paint_brush1, self.paint_brush2, self.paint_line,
                               self.paint_rect, self.paint_circle, self.paint_eraser, self.paint_bucket]
        # points
        self.p_first = [0, 0]
        self.p_last = [0, 0]
        self.p_prev = [0, 0]
        self.p_current = [0, 0]

        self.tool_door.door_outline = True
        self.board.all_sprites_list.move_to_front(self.tool_door)

        for each in self.board.ships:
            each.outline = False
            each.immobilize()
            each.readable = False

        """
        # set outline for tools
        for i in range(1, self.color_start):
            self.board.ships[i].set_outline([0, 54, 229], 1)

        for i in range(2):
            self.board.units[i].set_outline([0, 54, 229], 1)
        """

        self.canvas = pygame.Surface(
            [self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1])

        self.canvas.fill(self.canvas_block.initcolor)
        self.canvas_org = self.canvas.copy()
        self.history.append(self.canvas.copy())

        self.slider_canvas = pygame.Surface(
            [self.size_slider.grid_w * self.board.scale, self.size_slider.grid_h * self.board.scale - 1])

        if self.horizontal:
            self.slider_bg_lines = [[0, self.board.scale], [8 * self.board.scale, 2],
                                    [8 * self.board.scale, 2 * self.board.scale - 4]]
            self.update_color_choosers(self.data[0] // 2 - 1, self.data[0]-1, self.data[0]-1)
        else:
            self.slider_bg_lines = [[2, 2], [3 * self.board.scale - 2, 2],
                                    [1.5 * self.board.scale, self.size_slider.grid_h * self.board.scale - 2]]
            self.update_color_choosers(self.data[1] // 2 - 1, self.data[1]-1, self.data[1]-1)

        self.draw_slider(self.brush_size)

    def draw_slider(self, size):
        if self.horizontal:
            x = (((self.size_slider.grid_w * self.board.scale) - 10) * size) / 100
            slider_rect = [x, 0, 10, 2 * self.board.scale]
        else:
            size = 99 - size
            y = (((self.size_slider.grid_h * self.board.scale) - 10) * size) / 100
            slider_rect = [0, y, 3 * self.board.scale, 10]
        self.slider_canvas.fill(self.size_slider.initcolor)
        pygame.draw.polygon(self.slider_canvas, self.slider_bg_col, self.slider_bg_lines, 0)
        pygame.draw.rect(self.slider_canvas, self.slider_color, slider_rect, 0)

        self.size_slider.painting = self.slider_canvas.copy()
        self.size_slider.update_me = True
        self.mainloop.redraw_needed[0] = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            active = self.board.active_ship
            if event.button == 1:
                if active == 0:
                    self.btn_down = True
                    canvas_pos = [pos[0] - self.layout.game_left - self.canvas_block.grid_x * self.layout.scale,
                                  pos[1] - self.layout.top_margin - self.canvas_block.grid_y * self.layout.scale]
                    self.p_first = canvas_pos
                    self.p_prev = canvas_pos
                    self.p_current = canvas_pos
                    self.paint_function[self.active_tool](0)
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                elif 0 < active < 9:
                    self.active_tool = active - 1
                    self.tool_door.set_pos(self.board.active_ship_pos)
                elif active == 9:
                    self.change_size(pos, 0)
                elif active == 10:
                    self.undo()
                elif active == 11:
                    self.redo()
                elif active >= self.color_start:
                    if self.board.ships[active] in self.h_units:
                        self.h_door.set_pos(self.board.active_ship_pos)
                        c = active - self.h_units[0].unit_id
                        self.update_color_choosers(c, None, None)
                        self.mainloop.redraw_needed[0] = True
                    elif self.board.ships[active] in self.s_units:
                        self.s_door.set_pos(self.board.active_ship_pos)
                        c = active - self.s_units[0].unit_id
                        self.update_color_choosers(None, c, None)
                        self.mainloop.redraw_needed[0] = True
                    elif self.board.ships[active] in self.v_units:
                        self.v_door.set_pos(self.board.active_ship_pos)
                        c = active - self.v_units[0].unit_id
                        self.update_color_choosers(None, None, c)
                        self.mainloop.redraw_needed[0] = True

        elif event.type == pygame.MOUSEMOTION and self.btn_down:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
            if active == 0 and ((self.horizontal and column >= 0 and 2 < row < self.data[1] - 3) or (not self.horizontal and row >= 0 and 2 < column < self.data[0] - 3)):
                canvas_pos = [pos[0] - self.layout.game_left - self.canvas_block.grid_x * self.layout.scale,
                              pos[1] - self.layout.top_margin - self.canvas_block.grid_y * self.layout.scale]
                self.p_prev = self.p_current
                self.p_current = canvas_pos
                self.paint_function[self.active_tool](1)
            elif active == 9 and self.sizing and ((self.horizontal and row < 3) or (not self.horizontal and column < 3)):  # column >= self.data[0]-8 and :
                self.change_size(pos, 1)
            elif active == 9:
                self.sizing = False
                self.btn_down = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
            if active == 0 and ((self.horizontal and column >= 0 and 2 < row < self.data[1] - 3) or (not self.horizontal and row >= 0 and 2 < column < self.data[0] - 3)):
                canvas_pos = [pos[0] - self.layout.game_left - self.canvas_block.grid_x * self.layout.scale,
                              pos[1] - self.layout.top_margin - self.canvas_block.grid_y * self.layout.scale]
                self.p_last = canvas_pos
                self.paint_function[self.active_tool](2)
                self.update_history()
            elif active == 9 and self.sizing and ((self.horizontal and row < 3) or (not self.horizontal and column < 3)):  # column >= self.data[0]-8 and :
                self.change_size(pos, 2)
            else:
                if self.btn_down:
                    self.screen_restore()
                    self.copy_to_screen()
            self.sizing = False
            self.btn_down = False

    def update_color_choosers(self, h=None, s=None, v=None):
        if h is not None:
            self.custom_color_hsv[0] = h * self.step
        if s is not None:
            self.custom_color_hsv[1] = s * self.step
        if v is not None:
            self.custom_color_hsv[2] = v * self.step

        if self.horizontal:
            ind = 0
        else:
            ind = 1

        for i in range(0, self.data[ind]-1):
            self.h_units[i].color = ex.hsv_to_rgb(i * self.step, self.custom_color_hsv[1], self.custom_color_hsv[2])
            self.h_units[i].initcolor = self.h_units[i].color
            self.h_units[i].update_me = True

        for i in range(0, self.data[ind]-1):
            self.s_units[i].color = ex.hsv_to_rgb(self.custom_color_hsv[0], i * self.step, self.custom_color_hsv[2])
            self.s_units[i].initcolor = self.s_units[i].color
            self.s_units[i].update_me = True

        for i in range(0, self.data[ind]-1):
            self.v_units[i].color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], i * self.step)
            self.v_units[i].initcolor = self.v_units[i].color
            self.v_units[i].update_me = True

        self.active_color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], self.custom_color_hsv[2])

    def change_size(self, pos, stage):
        if self.horizontal:
            ind = 0
        else:
            ind = 1
        if self.slider_min < pos[ind] < self.slider_max:
            if stage == 0:
                self.sizing = True
                self.btn_down = True
                self.apply_size(pos)
            elif stage == 1:
                self.apply_size(pos)
            elif stage == 2:
                self.apply_size(pos)
                self.btn_down = False
                self.sizing = False
            self.size_slider.update_me = True
            self.size_display.update_me = True
            self.mainloop.redraw_needed[0] = True

    def apply_size(self, pos):
        if self.horizontal:
            size = int(((pos[0] - self.slider_min) * 100.0) / (self.slider_max - self.slider_min))
            self.brush_size = size
            self.size_display.value = self.d["brush size"] + ": " + str(self.brush_size)
        else:
            size = 99 - int(((pos[1] - self.slider_min) * 100.0) / (self.slider_max - self.slider_min))
            self.brush_size = size
            self.size_display.value = str(self.brush_size)
        self.draw_slider(size)

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
                        r = self.brush_size // 2  # - 1
                        width = self.brush_size + 2
                    pygame.draw.circle(self.canvas, self.active_color, self.p_current, r, 0)
                if self.brush_size > 3:
                    self.draw_line(self.p_prev, self.p_current, self.brush_size, self.brush_size)
                else:
                    pygame.draw.line(self.canvas, self.active_color, self.p_prev, self.p_current, width)
                self.copy_to_screen()

    def paint_brush1(self, state):
        if self.brush_size > 0:
            if state == 0:
                self.backup_canvas()
                self.copy_to_screen()
            elif state == 1:
                if self.var_brush < self.brush_size:
                    self.var_brush += 1
                self.draw_line(self.p_prev, self.p_current, self.var_brush - 1, self.var_brush)
                self.copy_to_screen()
            elif state == 2:
                self.var_brush = 1

    def paint_brush2(self, state):
        if self.brush_size > 0:
            if state == 0:
                if self.brush_size % 2 != 0:
                    self.brush_size += 1
                    self.size_display.value = str(self.brush_size)
                    self.size_display.update_me = True
                self.backup_canvas()
                rectangle = [self.p_first[0] - self.brush_size // 2, self.p_first[1] - self.brush_height // 2,
                             self.brush_size, self.brush_height]
                pygame.draw.rect(self.canvas, self.active_color, rectangle, 0)
                self.copy_to_screen()
            elif state == 1:
                rectangle = [self.p_current[0] - self.brush_size // 2, self.p_current[1] - self.brush_height // 2,
                             self.brush_size, self.brush_height]
                pygame.draw.rect(self.canvas, self.active_color, rectangle, 0)
                points = self.get_corners()
                pygame.draw.polygon(self.canvas, self.active_color, points)
                pygame.draw.aalines(self.canvas, self.active_color, True, points, 1)
                self.copy_to_screen()
            elif state == 2:
                rectangle = [self.p_last[0] - self.brush_size // 2, self.p_last[1] - self.brush_height // 2,
                             self.brush_size, self.brush_height]
                pygame.draw.rect(self.canvas, self.active_color, rectangle, 0)
                self.copy_to_screen()

    def get_corners(self):
        r1 = [self.p_prev[0] - self.brush_size // 2, self.p_prev[1] - self.brush_height // 2, self.brush_size,
              self.brush_height]
        r2 = [self.p_current[0] - self.brush_size // 2, self.p_current[1] - self.brush_height // 2, self.brush_size,
              self.brush_height]

        p1 = [[r1[0], r1[1]], [r1[0] + r1[2], r1[1]], [r1[0] + r1[2] - 1, r1[1] + r1[3] - 1], [r1[0], r1[1] + r1[3]]]
        p2 = [[r2[0], r2[1]], [r2[0] + r2[2], r2[1]], [r2[0] + r2[2] - 1, r2[1] + r2[3] - 1], [r2[0], r2[1] + r2[3]]]

        dist = sv.Vector2.from_points(self.p_prev, self.p_current)
        if (dist[0] >= 0 and dist[1] <= 0) or (dist[0] <= 0 and dist[1] >= 0):
            cr = [p1[0], p2[0], p2[2], p1[2]]
        else:
            cr = [p1[1], p2[1], p2[3], p1[3]]
        return cr

    def paint_line(self, state):
        if state == 0:
            self.backup_canvas()
        elif state == 1:
            self.screen_restore()
            pygame.draw.aaline(self.canvas, self.active_color, self.p_first, self.p_current, 1)
            self.copy_to_screen()
        elif state == 2:
            if self.brush_size > 0:
                self.screen_restore()
                if self.brush_size > 3:
                    self.draw_line(self.p_first, self.p_last, self.brush_size, self.brush_size)
                else:
                    pygame.draw.line(self.canvas, self.active_color, self.p_first, self.p_current, self.brush_size)
                self.copy_to_screen()

    def draw_line(self, p1, p2, bs1, bs2):
        # find points for the corners of the polygon using Tales Theorem
        # and draw the polygon - rotated rectangle or trapezium and 2 circles at the ends of the 'line'
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

    def paint_rect(self, state):
        if state == 0:
            self.backup_canvas()
        elif state == 1:
            lt = [min(self.p_first[0], self.p_current[0]), min(self.p_first[1], self.p_current[1])]
            rb = [max(self.p_first[0], self.p_current[0]), max(self.p_first[1], self.p_current[1])]
            rectangle = [lt[0], lt[1], rb[0] - lt[0], rb[1] - lt[1]]
            dist = sv.Vector2.from_points(lt, rb)
            if min(dist) > 2:
                self.screen_restore()
                pygame.draw.rect(self.canvas, self.active_color, rectangle, 1)
                self.copy_to_screen()
        elif state == 2:
            lt = [min(self.p_first[0], self.p_last[0]), min(self.p_first[1], self.p_last[1])]
            rb = [max(self.p_first[0], self.p_last[0]), max(self.p_first[1], self.p_last[1])]
            rectangle = [lt[0], lt[1], rb[0] - lt[0], rb[1] - lt[1]]
            if self.brush_size > 0:
                self.screen_restore()
                dist = sv.Vector2.from_points(lt, rb)
                dist = self.v2_to_int(dist)
                if min(dist) // 2 > self.brush_size:
                    border_width = self.brush_size
                    if border_width > 4:
                        if border_width % 2 == 0:
                            bw2 = border_width // 2 - 1
                        else:
                            bw2 = border_width // 2
                        border_rects = []
                        # top
                        border_rects.append([lt[0] - bw2, lt[1] - bw2, dist[0] + border_width - 1, border_width])
                        # bottom
                        border_rects.append(
                            [rb[0] - dist[0] - bw2, rb[1] - bw2, dist[0] + border_width - 1, border_width])
                        for each in border_rects:
                            pygame.draw.rect(self.canvas, self.active_color, each, 0)

                else:
                    border_width = 0
            else:
                border_width = 0
            pygame.draw.rect(self.canvas, self.active_color, rectangle, border_width)
            self.copy_to_screen()

    def paint_circle(self, state):
        if state == 0:
            self.backup_canvas()
        elif state == 1:
            lt = [min(self.p_first[0], self.p_current[0]), min(self.p_first[1], self.p_current[1])]
            rb = [max(self.p_first[0], self.p_current[0]), max(self.p_first[1], self.p_current[1])]
            rectangle = [lt[0], lt[1], rb[0] - lt[0], rb[1] - lt[1]]
            dist = sv.Vector2.from_points(lt, rb)
            if min(dist) > 2:
                self.screen_restore()
                pygame.draw.rect(self.canvas, self.active_color, rectangle, 1)
                pygame.draw.ellipse(self.canvas, self.active_color, rectangle, 1)
                self.copy_to_screen()
        elif state == 2:
            lt = [min(self.p_first[0], self.p_last[0]), min(self.p_first[1], self.p_last[1])]
            rb = [max(self.p_first[0], self.p_last[0]), max(self.p_first[1], self.p_last[1])]
            rectangle = [lt[0], lt[1], rb[0] - lt[0], rb[1] - lt[1]]
            if self.brush_size > 0:
                dist = sv.Vector2.from_points(lt, rb)
                if min(dist) // 2 > self.brush_size + 2:
                    border_width = self.brush_size
                else:
                    border_width = 0
            else:
                border_width = 0
            self.screen_restore()
            pygame.draw.ellipse(self.canvas, self.active_color, rectangle, border_width)
            if border_width > 4:
                fillup_rect1 = [lt[0] + 1, lt[1] + 1, rb[0] - lt[0] - 0.5, rb[1] - lt[1] - 0.5]
                fillup_rect2 = [lt[0] + 1, lt[1] + 0.5, rb[0] - lt[0] - 1, rb[1] - lt[1] - 0.5]
                pygame.draw.ellipse(self.canvas, self.active_color, fillup_rect1, border_width - 1)
                pygame.draw.ellipse(self.canvas, self.active_color, fillup_rect2, border_width)
                pygame.draw.ellipse(self.canvas, self.active_color, fillup_rect2, border_width)
            self.copy_to_screen()

    def paint_eraser(self, state):
        if self.brush_size > 0:
            if state == 0:
                self.backup_canvas()
                pygame.draw.circle(self.canvas, self.bg_color, self.p_current, self.brush_size // 2, 0)
                self.copy_to_screen()
            elif state == 1:
                pygame.draw.line(self.canvas, self.bg_color, self.p_prev, self.p_current, self.brush_size)
                pygame.draw.circle(self.canvas, self.bg_color, self.p_current, self.brush_size // 2, 0)
                self.copy_to_screen()

    def paint_bucket(self, state):
        if state == 0:
            self.backup_canvas()
            self.canvas.fill(self.active_color)
            self.bg_color = self.active_color
            self.copy_to_screen()

    def backup_canvas(self):
        self.canvas_org = self.canvas_block.painting.copy()

    def copy_to_screen(self):
        self.canvas_block.painting = self.canvas.copy()
        self.canvas_block.update_me = True
        self.mainloop.redraw_needed[0] = True

    def screen_restore(self):
        self.canvas = self.canvas_org.copy()
        self.var_brush = 1

    def undo(self):
        hist_len = len(self.history)
        if self.undo_step < hist_len - 1:
            self.undo_step += 1
            self.canvas = self.history[-self.undo_step - 1].copy()
            self.copy_to_screen()

    def redo(self):
        if self.undo_step > 0:
            self.undo_step -= 1
            self.canvas = self.history[-self.undo_step - 1].copy()
            self.copy_to_screen()

    def update_history(self):
        if self.undo_step != 0:
            for i in range(self.undo_step):
                del (self.history[-1])
            self.undo_step = 0
        if len(self.history) > self.history_capacity:
            del self.history[0]
        self.history.append(self.canvas.copy())

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def v2_to_int(self, vector):
        integers = [int(each) for each in vector]
        return integers

    def check_result(self):
        pass
