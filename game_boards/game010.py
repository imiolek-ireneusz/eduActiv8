# -*- coding: utf-8 -*-

import pygame
import random
import sys
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
        s = 100
        v = 255
        h = random.randrange(0, 255)
        letter_color = ex.hsv_to_rgb(h, s, v)
        font_color = ex.hsv_to_rgb(h, 255, 140)
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
        if self.mainloop.m.game_variant == 0: #10
            font_size = 12
        elif self.mainloop.m.game_variant == 1: #68
            font_size = 20
        elif self.mainloop.m.game_variant == 2: #67
            font_size = 13
        elif self.mainloop.m.game_variant == 3: #22
            font_size = 13

        font_size2 = 14
        self.brush_size = data[3]

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

        # canvas
        self.board.add_unit(10, 0, data[0] - 16, data[1], classes.board.Letter, "", color, "", font_size)
        self.canvas_block = self.board.ships[0]
        self.canvas_block.set_outline([0, 54, 229], 1)

        self.canvas_block.font3 = self.board.font_sizes[font_size2]
        x = 0
        y = 0
        # i_chr = 65

        for i in range(0, l):
            self.board.add_unit(x, y, 2, 2, classes.board.Letter, luc[i], letter_color, "", 25)
            self.board.add_unit(x + 4, y, 2, 2, classes.board.Letter, llc[i], letter_color, "", 25)

            if i < lh:
                self.board.add_unit(x + 8, y, 2, 2, classes.board.Letter, str(i), letter_color, "", 25)

            y += 2

            if y >= l:
                x = 2
                y = 0

        self.board.add_door(0, 0, 2, 2, classes.board.Door, "", color, "")
        self.board.add_door(data[0] - 1, 17, 1, 1, classes.board.Door, "", color, "")
        tool_len = len(self.board.ships)

        # color pallette
        h = 0
        s = 250
        v = 70
        # number of available color spaces minus 2 for black and white
        number_of_col_per_hue = 6  # number_of_colors // number_of_hues
        v_num = (255 - v) // (number_of_col_per_hue)
        # greyscale
        grey_num = 6
        if grey_num > 1:
            grey_v_num = (255 // (grey_num - 1))
        else:
            grey_v_num = 0
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

        self.board.ships[1].color = self.letter_color2
        self.board.ships[1].initcolor = self.letter_color2
        self.prev_item = self.board.ships[1]

        self.active_letter = self.board.ships[1].value

        self.active_color = self.board.ships[173].initcolor
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
            [self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1])
        self.canvas.fill(self.canvas_block.initcolor)
        self.paint_bg_letter()
        self.canvas_org = self.canvas.copy()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change the x/y screen coordinates to grid coordinates
            pos = event.pos
            active = self.board.active_ship
            if event.button == 1:
                if self.prev_item is not None:
                    self.prev_item.color = self.letter_color2
                    self.prev_item.update_me = True

                if active == 0:
                    self.btn_down = True
                    canvas_pos = [pos[0] - self.layout.game_left - 10 * self.layout.scale,
                                  pos[1] - self.layout.top_margin]
                    self.p_first = canvas_pos
                    self.p_prev = canvas_pos
                    self.p_current = canvas_pos
                    self.brush_size = self.data[3]
                    self.paint_pencil(0)
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                elif 0 < active < self.count + 1:
                    self.active_letter = self.board.ships[self.board.active_ship].value
                    self.board.ships[self.board.active_ship].color = self.letter_color2
                    self.prev_item = self.board.ships[self.board.active_ship]

                    self.tool_door.set_pos(self.board.active_ship_pos)
                    self.paint_bg_letter()
                elif active > self.count:
                    self.active_color = self.board.ships[active].initcolor
                    self.color_door.set_pos(self.board.active_ship_pos)

        elif event.type == pygame.MOUSEMOTION and self.btn_down == True:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
            if active == 0 and self.data[0] - 6 > column > 9 and row < self.data[1]:
                canvas_pos = [pos[0] - self.layout.game_left - 10 * self.layout.scale, pos[1] - self.layout.top_margin]
                self.p_prev = self.p_current
                self.p_current = canvas_pos
                self.paint_pencil(1)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.layout.game_left) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
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

    def paint_bg_letter(self):
        if sys.version_info < (3, 0):
            txt = unicode(self.active_letter, "utf-8")
        else:
            txt = self.active_letter
        try:
            text = self.canvas_block.font.render("%s" % (txt), 1, (220, 220, 220, 0))

            font_x = ((self.board.scale * self.canvas_block.grid_w - self.canvas_block.font.size(txt)[0]) // 2)
            if self.mainloop.m.game_variant == 0:
                font_y = ((self.board.scale * self.canvas_block.grid_h - self.canvas_block.font.size(txt)[
                    1]) // 2) - 3 * self.board.scale
            else:
                font_y = ((self.board.scale * self.canvas_block.grid_h - self.canvas_block.font.size(txt)[1]) // 2)

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
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
