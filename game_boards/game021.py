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
        self.level = lc.Level(self, mainloop, 1, 1)
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

        self.history = []
        self.undo_step = 0
        self.bg_color = [255, 255, 255]
        color = [255, 255, 255]
        data = [39, 27]
        self.slider_color = [50, 50, 250]
        self.slider_bg_col = [200, 200, 255]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=None)
        if x_count > data[0]:
            data[0] = x_count
        else:
            y_count = self.get_y_count(data[0], even=None)
            data[1] = y_count - 1
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.slider_min = self.mainloop.size[0] - self.layout.game_margin - 8 * self.layout.scale
        self.slider_max = self.mainloop.size[0] - self.layout.game_margin - 2

        # canvas
        self.board.add_unit(0, 3, data[0], data[1] - 6, classes.board.Letter, "", color, "", 2)
        self.canvas_block = self.board.ships[0]
        self.canvas_block.set_outline([0, 54, 229], 1)
        # tools
        images = ["paint_pencil.png", "paint_brush.png", "paint_wide_brush.png", "paint_line.png", "paint_rect.png",
                  "paint_circle.png", "paint_eraser.png", "paint_bucket.png"]
        j = 7
        for i in range(8):
            self.board.add_unit(j, 0, 3, 3, classes.board.ImgShip, "", color, images[i])
            j += 3
        if data[0] - j - 8 > 0:
            self.board.add_unit(j, 0, data[0] - j - 8, 3, classes.board.Obstacle, "", self.bg_color, "",
                                0)  # gap filler

        self.board.add_unit(data[0] - 8, 1, 8, 2, classes.board.Letter, "", color, "", 0)
        self.size_slider = self.board.ships[-1]

        self.board.add_unit(data[0] - 8, 0, 8, 1, classes.board.Label,
                            self.d["brush size"] + ": " + str(self.brush_size), color, "", 0)
        self.size_display = self.board.units[-1]
        self.board.add_unit(0, 0, 3, 3, classes.board.ImgShip, "", color, "paint_undo.png")
        self.board.add_unit(3, 0, 3, 3, classes.board.ImgShip, "", color, "paint_redo.png")
        self.board.add_unit(6, 0, 1, 3, classes.board.Obstacle, "", self.bg_color, "", 0)  # gap filler

        self.board.add_door(7, 0, 3, 3, classes.board.Door, "", color, "")
        self.board.add_door(0, data[1] - 3, 1, 1, classes.board.Door, "", color, "")
        tool_len = len(self.board.ships)
        # color pallette
        h = 0
        s = 250
        v = 100
        # number of available color spaces minus 2 for black and white
        number_of_colors = data[0] * 3 - 2
        number_of_hues = 13
        number_of_col_per_hue = number_of_colors // number_of_hues
        if number_of_col_per_hue > 3:
            v_num = (255 - v) // (number_of_col_per_hue - 3)
        else:
            v_num = 150

        # greyscale
        grey_num = number_of_colors + 2 - number_of_hues * number_of_col_per_hue
        if grey_num > 1:
            grey_v_num = (255 // (grey_num - 1))
        else:
            grey_v_num = 0
        grey_count = 0

        self.color_start = len(self.board.ships)
        for j in range(data[1] - 3, data[1]):
            for i in range(data[0]):
                color2 = ex.hsv_to_rgb(h, s, v)
                self.board.add_unit(i, j, 1, 1, classes.board.Letter, "", color2, "", 2)
                if h < 255:
                    if v <= (255 - v_num):
                        v += v_num
                    else:
                        if s > 115:
                            s -= 70
                        else:
                            v = 100
                            s = 250
                            h += 20
                if h > 255:
                    if grey_count == 0:
                        s = 0
                        v = 0
                        grey_count += 1
                    else:
                        v += grey_v_num

        self.active_color = self.board.ships[tool_len + 1].initcolor

        self.tool_door = self.board.units[-2]
        self.color_door = self.board.units[-1]
        self.btn_down = False
        self.paint_function = [self.paint_pencil, self.paint_brush1, self.paint_brush2, self.paint_line,
                               self.paint_rect, self.paint_circle, self.paint_eraser, self.paint_bucket]

        # points
        self.p_first = [0, 0]
        self.p_last = [0, 0]
        self.p_prev = [0, 0]
        self.p_current = [0, 0]

        doors = [self.tool_door, self.color_door]
        for each in doors:
            each.door_outline = True
            self.board.all_sprites_list.move_to_front(each)

        for each in self.board.ships:
            each.outline = False
            each.immobilize()
            each.readable = False

        # set outline for tools
        for i in range(1, self.color_start):
            self.board.ships[i].set_outline([0, 54, 229], 1)

        for i in range(2):
            self.board.units[i].set_outline([0, 54, 229], 1)

        self.canvas = pygame.Surface(
            [self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1])
        self.canvas.fill(self.canvas_block.initcolor)
        self.canvas_org = self.canvas.copy()  # pygame.Surface([self.canvas_block.grid_w*self.board.scale, self.canvas_block.grid_h*self.board.scale-1])
        self.history.append(self.canvas.copy())

        self.slider_canvas = pygame.Surface(
            [self.size_slider.grid_w * self.board.scale, self.size_slider.grid_h * self.board.scale - 1])
        self.slider_bg_lines = [[0, self.board.scale], [8 * self.board.scale, 2],
                                [8 * self.board.scale, 2 * self.board.scale - 4]]
        self.draw_slider(self.brush_size)

    def draw_slider(self, size):
        x = (((self.size_slider.grid_w * self.board.scale) - 10) * size) / 100
        slider_rect = [x, 0, 10, 2 * self.board.scale]
        self.slider_canvas.fill(self.size_slider.initcolor)
        pygame.draw.polygon(self.slider_canvas, self.slider_bg_col, self.slider_bg_lines, 0)
        pygame.draw.rect(self.slider_canvas, self.slider_color, slider_rect, 0)

        self.size_slider.painting = self.slider_canvas.copy()
        self.size_slider.update_me = True
        self.mainloop.redraw_needed[0] = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change the x/y screen coordinates to grid coordinates
            pos = event.pos
            active = self.board.active_ship
            if event.button == 1:
                if active == 0:
                    self.btn_down = True
                    canvas_pos = [pos[0] - self.layout.game_left,
                                  pos[1] - self.layout.top_margin - 3 * self.layout.scale]
                    self.p_first = canvas_pos
                    self.p_prev = canvas_pos
                    self.p_current = canvas_pos
                    self.paint_function[self.active_tool](0)
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                    # start of painting done here
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
                    self.active_color = self.board.ships[active].initcolor
                    self.color_door.set_pos(self.board.active_ship_pos)

        elif event.type == pygame.MOUSEMOTION and self.btn_down == True:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
            if active == 0 and column >= 0 and 2 < row < self.data[1] - 3:
                canvas_pos = [pos[0] - self.layout.game_left, pos[1] - self.layout.top_margin - 3 * self.layout.scale]
                self.p_prev = self.p_current
                self.p_current = canvas_pos
                self.paint_function[self.active_tool](1)
            elif active == 9 and self.sizing == True and row < 3:  # column >= self.data[0]-8 and :
                self.change_size(pos, 1)
            elif active == 9:
                self.sizing = False
                self.btn_down = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
            if active == 0 and column >= 0 and 2 < row < self.data[1] - 3:
                # drop the new object onto the painting
                canvas_pos = [pos[0] - self.layout.game_left, pos[1] - self.layout.top_margin - 3 * self.layout.scale]
                self.p_last = canvas_pos
                self.paint_function[self.active_tool](2)
                self.update_history()
            elif active == 9 and self.sizing == True and row < 3:  # column >= self.data[0]-8 and :
                self.change_size(pos, 2)
            else:
                if self.btn_down:
                    self.screen_restore()
                    self.copy_to_screen()
            self.sizing == False
            self.btn_down = False

    def change_size(self, pos, stage):
        if self.slider_min < pos[0] < self.slider_max:
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
        size = int(((pos[0] - self.slider_min) * 100.0) / (self.slider_max - self.slider_min))
        self.brush_size = size
        self.size_display.value = self.d["brush size"] + ": " + str(self.brush_size)
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
            # rectangle = [self.p_first[0], self.p_first[1], self.p_last[0]-self.p_first[0],self.p_last[1]-self.p_first[1]]
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
