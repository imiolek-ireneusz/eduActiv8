# -*- coding: utf-8 -*-

import math
import os
import pygame
import random
import sys

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.simple_vector as sv


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)
        self.max_size = 99

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.board.decolorable = False
        self.board.draw_grid = False
        self.brush_size = 2
        self.max_points = 3
        self.prev_snap = None
        self.direction = 0

        self.color_s = random.randrange(50, 90, 5)
        self.color_v = random.randrange(230, 255, 5)

        h = random.randrange(0, 255, 1)
        self.bg_color = [255, 255, 255]
        color = [255, 255, 255]
        white = (255, 255, 255)
        self.transp = (0, 0, 0, 0)

        self.lbl_font_color = ex.hsv_to_rgb(17, 255, 175)
        self.guides_color = [200, 200, 200]
        self.axis_color = [255, 0, 0]
        scheme = "white"
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                scheme = "black"
                white = (0, 0, 0)
                self.bg_color = (0, 0, 0)
                color = (0, 0, 0)
                self.guides_color = (30, 30, 30)

        lvl_data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                         self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        data = [27, 20]

        self.data = data

        self.mainloop.info.hide_buttons(0, 0, 0, 0, 1, 1, 1, 0, 0)
        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.scale = scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.line_color = (20, 20, 20)
        self.reset()

        if self.mainloop.android is None:
            self.grid_density_div = lvl_data[0]
        else:
            self.grid_density_div = 1

        self.guide_scale = self.board.scale# // self.grid_density_div
        self.left_padding = 3
        self.px_padding = self.left_padding * scale + self.layout.game_left
        # canvas
        self.canvas_side = min(data[0] - self.left_padding, data[1])
        self.board.add_unit(self.left_padding, 0, self.canvas_side, self.canvas_side, classes.board.Letter, "", color,
                            "", 2)
        self.canvas_block = self.board.ships[-1]
        self.canvas_block.set_outline([0, 54, 229], 1)
        self.board.add_unit(0, 0, 2, 2, classes.board.ImgShip, "", white, os.path.join("symmetry", "ax_h.png"), 0, alpha=True)
        self.ax_h_btn = self.board.ships[-1]

        self.board.add_unit(0, 2, 2, 2, classes.board.ImgShip, "", white, os.path.join("symmetry", "ax_v.png"), 0, alpha=True)
        self.ax_v_btn = self.board.ships[-1]

        self.board.add_unit(0, 4, 2, 2, classes.board.ImgShip, "", white, os.path.join("symmetry", "ax_hv.png"), 0, alpha=True)
        self.ax_hv_btn = self.board.ships[-1]

        self.board.add_unit(0, 6, 2, 2, classes.board.ImgShip, "", white,os.path.join("symmetry", "ax_d1.png"), 0, alpha=True)
        self.ax_d1_btn = self.board.ships[-1]

        self.board.add_unit(0, 8, 2, 2, classes.board.ImgShip, "", white, os.path.join("symmetry", "ax_d2.png"), 0, alpha=True)
        self.ax_d2_btn = self.board.ships[-1]

        self.board.add_unit(0, 10, 2, 2, classes.board.ImgShip, "", white, os.path.join("symmetry", "ax_dd.png"), 0, alpha=True)
        self.ax_dd_btn = self.board.ships[-1]


        self.board.add_unit(0, 12, 2, 2, classes.board.ImgShip, "", white, os.path.join("symmetry", "ax_hvdd.png"), 0, alpha=True)
        self.ax_hvdd_btn = self.board.ships[-1]

        #up]

        self.board.add_unit(0, 15, 2, 1, classes.board.ImgCenteredShip, "", self.transp, img_src='nav_u.png', alpha=True)
        #self.board.add_unit(0, 8, 2, 1, classes.board.ImgShip, "", white, os.path.join("schemes", scheme, "c_circle.png"), 0)
        self.up_btn = self.board.ships[-1]

        #max points label
        self.board.add_unit(0, 16, 2, 2, classes.board.Label, str(self.max_points), white, "", 31)
        self.mpl = self.board.units[-1]
        self.mpl.font_color = self.lbl_font_color

        #down
        self.board.add_unit(0, 18, 2, 1, classes.board.ImgCenteredShip, "", self.transp, img_src='nav_dd.png', alpha=True)
        #self.board.add_unit(0, 11, 2, 1, classes.board.ImgShip, "", white, os.path.join("schemes", scheme, "c_circle.png"), 0)
        self.dn_btn = self.board.ships[-1]

        self.btn_down = False

        # add colour mixer
        # current color
        self.board.add_unit(data[1]+4, 0, 3, 1, classes.board.Obstacle, "", ex.hsv_to_rgb(0, 255, 255), "", 0)
        self.current_col_ind = self.board.units[-1]

        self.board.add_unit(data[1]+4, 1, 1, 1, classes.board.Letter, "H", color, "", 2)
        self.board.add_unit(data[1]+5, 1, 1, 1, classes.board.Letter, "S", color, "", 2)
        self.board.add_unit(data[1]+6, 1, 1, 1, classes.board.Letter, "V", color, "", 2)
        self.step = int(255 / (data[1] - 2))
        hi = random.randint(0, data[1] - 3)
        self.custom_color_hsv = [hi * self.step, ((data[1] - 2) // 2) * self.step, (data[1] - 2) * self.step]
        self.h_units = []
        self.s_units = []
        self.v_units = []

        # hue selectors
        for i in range(data[1] - 2):
            c0 = ex.hsv_to_rgb(self.step * i, 255, 255)
            self.board.add_unit(data[1] + 4, i + 2, 1, 1, classes.board.Ship, "", c0, "", 0)
            self.h_units.append(self.board.ships[-1])

        # saturation selectors
        for i in range(data[1] - 2):
            c1 = ex.hsv_to_rgb(0, self.step * i, 255)
            self.board.add_unit(data[1] + 5, i + 2, 1, 1, classes.board.Ship, "", c1, "", 0)
            self.s_units.append(self.board.ships[-1])

        # vibrance selectors
        for i in range(data[1] - 2):
            c2 = ex.hsv_to_rgb(0, 255, self.step * i)
            self.board.add_unit(data[1] + 6, i + 2, 1, 1, classes.board.Ship, "", c2, "", 0)
            self.v_units.append(self.board.ships[-1])

        for each in self.board.ships:
            each.outline = False
            each.immobilize()
            each.readable = False

        self.canvas = pygame.Surface(
            [self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1])
        self.layer = pygame.Surface(
            [self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1],
            pygame.SRCALPHA)

        self.new_screen()
        # self.vectors = []
        self.board.add_door(0, 0, 2, 2, classes.board.Door, "", color, "")
        self.tool_door = self.board.units[-1]
        self.tool_door.door_outline = True
        self.board.all_sprites_list.move_to_front(self.tool_door)

        self.board.add_door(data[1] + 4, 2 + hi, 1, 1, classes.board.Door, "", color, "")
        self.h_door = self.board.units[-1]
        self.h_door.door_outline = True
        self.h_door.perm_outline_color = (200, 0, 0)

        self.board.all_sprites_list.move_to_front(self.h_door)

        self.board.add_door(data[1] + 5, 2 + ((data[1] - 2) // 2), 1, 1, classes.board.Door, "", color, "")
        self.s_door = self.board.units[-1]
        self.s_door.door_outline = True
        self.s_door.perm_outline_color = (200, 0, 0)
        self.board.all_sprites_list.move_to_front(self.s_door)

        self.board.add_door(data[1] + 6, data[1] - 1, 1, 1, classes.board.Door, "", color, "")
        self.v_door = self.board.units[-1]
        self.v_door.door_outline = True
        self.v_door.perm_outline_color = (200, 0, 0)
        self.board.all_sprites_list.move_to_front(self.v_door)
        self.update_colors()

    def update_colors(self, h=None, s=None, v=None):
        if h is not None:
            self.custom_color_hsv[0] = h * self.step
        if s is not None:
            self.custom_color_hsv[1] = s * self.step
        if v is not None:
            self.custom_color_hsv[2] = v * self.step

        for i in range(self.data[1] - 2):
            self.h_units[i].color = ex.hsv_to_rgb(i * self.step, self.custom_color_hsv[1], self.custom_color_hsv[2])
            self.h_units[i].initcolor = self.h_units[i].color
            self.h_units[i].update_me = True

        for i in range(self.data[1] - 2):
            self.s_units[i].color = ex.hsv_to_rgb(self.custom_color_hsv[0], i * self.step, self.custom_color_hsv[2])
            self.s_units[i].initcolor = self.s_units[i].color
            self.s_units[i].update_me = True

        for i in range(self.data[1] - 2):
            self.v_units[i].color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], i * self.step)
            self.v_units[i].initcolor = self.v_units[i].color
            self.v_units[i].update_me = True
        self.current_col_ind.color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], self.custom_color_hsv[2])
        self.active_color = self.current_col_ind.color
        self.active_color.append(127)
        if self.custom_color_hsv[2] > 127:
            self.border_color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], self.custom_color_hsv[2] - 50)
        else:
            self.border_color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], self.custom_color_hsv[2] + 50)
        #self.border_color.append(127)
        self.current_col_ind.update_me = True

    def new_screen(self):
        self.layer.fill(self.transp)
        self.canvas.fill(self.canvas_block.initcolor)
        self.draw_guides(self.guide_scale)
        self.draw_axis(self.direction)
        self.canvas_org = self.canvas.copy()
        self.copy_to_screen()

    def reset(self):
        self.points = []
        self.points_count = 0
        #self.active_color = self.current_col_ind.color
        self.p_current = [0, 0]

    def layer_blit(self):
        self.canvas.blit(self.layer, (0, 0))
        self.layer.fill(self.transp)

    def fill_poli(self):
        p2 = self.get_simetrical_shape(self.direction, self.points)

        #draw shape
        self.points.append(self.points[0])
        pygame.draw.polygon(self.layer, self.active_color, self.points, 0)
        pygame.draw.polygon(self.layer, self.border_color, self.points, 3)
        self.layer_blit()

        #draw symetrical shape
        p2.append(p2[0])
        pygame.draw.polygon(self.layer, self.active_color, p2, 0)
        pygame.draw.polygon(self.layer, self.border_color, p2, 3)
        self.layer_blit()
        self.draw_axis(self.direction)

        self.reset()
        self.copy_to_screen()

    def fill_polix2(self):
        if self.direction == 4:
            a = [0, 1]
        else:
            a = [2, 3]
        p2 = self.get_simetrical_shape(a[0], self.points)
        p3 = self.get_simetrical_shape(a[1], self.points)
        p4 = self.get_simetrical_shape(a[0], p3)

        p = [self.points, p2, p3, p4]
        for each in p:
            each.append(each[0])
            pygame.draw.polygon(self.layer, self.active_color, each, 0)
            self.layer_blit()
        for each in p:
            pygame.draw.polygon(self.canvas, self.border_color, each, 3)

        self.draw_axis(self.direction)

        self.reset()
        self.copy_to_screen()
        #self.backup_canvas()

    def fill_polix4(self):
        p2 = self.get_simetrical_shape(0, self.points)
        p3 = self.get_simetrical_shape(1, self.points)
        p4 = self.get_simetrical_shape(0, p3)

        p5 = self.get_simetrical_shape(2, self.points)
        p6 = self.get_simetrical_shape(3, self.points)
        p7 = self.get_simetrical_shape(2, p2)
        p8 = self.get_simetrical_shape(2, p3)

        p = [self.points, p2, p3, p4, p5, p6, p7, p8]
        for each in p:
            each.append(each[0])
            pygame.draw.polygon(self.layer, self.active_color, each, 0)
            self.layer_blit()
        for each in p:
            pygame.draw.polygon(self.canvas, self.border_color, each, 3)

        self.draw_axis(self.direction)

        self.reset()
        self.copy_to_screen()

    def get_simetrical_shape(self, direction, points):
        hs = (self.canvas_side // 2) * self.scale
        p2 = []
        if direction == 0:
            for each in points:
                p2.append([each[0], hs + (hs-each[1])])
            return p2
        elif direction == 1:
            for each in points:
                p2.append([hs + (hs - each[0]), each[1]])
            return p2
        elif direction == 2:
            for each in points:
                p2.append([each[1], each[0]])
            return p2
        elif direction == 3:
            sd = self.canvas_side * self.scale
            for each in points:
                p2.append([sd - each[1], sd - each[0]])
            return p2

    def draw_axis(self, direction):
        hs = (self.canvas_side // 2) * self.scale
        if direction == 0: #horizontal
            points = ((0, hs), (self.canvas_side * self.scale, hs))
        elif direction == 1: #vertical
            points = ((hs, 0), (hs, self.canvas_side * self.scale))
        elif direction == 2: #diagonal top-left to bottom-right
            points = ((0, 0), (self.canvas_side * self.scale, self.canvas_side * self.scale))
        elif direction == 3: #diagonal bottom-left to top-right
            points = ((0, self.canvas_side * self.scale), (self.canvas_side * self.scale, 0))
        elif direction == 4: #horz & vert
            self.draw_axis(0)
            self.draw_axis(1)
            #points = ((0, hs), (self.canvas_side * self.scale, hs))
            #points2 = ((hs, 0), (hs, self.canvas_side * self.scale))
            #pygame.draw.line(self.canvas, self.axis_color, points2[0], points2[1], 3)
        elif direction == 5:  # both diagonal
            self.draw_axis(2)
            self.draw_axis(3)
            #points = ((0, 0), (self.canvas_side * self.scale, self.canvas_side * self.scale))
            #points2 = ((0, self.canvas_side * self.scale), (self.canvas_side * self.scale, 0))
            #pygame.draw.line(self.canvas, self.axis_color, points2[0], points2[1], 3)
        elif direction == 6:
            for i in range(4):
                self.draw_axis(i)

        if direction < 4:
            pygame.draw.line(self.canvas, self.axis_color, points[0], points[1], 3)

    def get_set_r(self):
        v = sv.Vector2.from_points(self.points[0], self.points[1])
        if v[0] != 0 or v[1] != 0:
            r = math.sqrt(v[0] * v[0] + v[1] * v[1])
        else:
            r = 0
        r = int(r)
        self.circle_r = r
        return r

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            active = self.board.active_ship
            column = (pos[0] - self.px_padding) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
            if event.button == 1 and column >= 0 and 0 <= row < self.data[1]:
                if self.points_count == 0:
                    pass  # self.new_screen()

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            active = self.board.active_ship
            column = (pos[0] - self.px_padding) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)
            if active != self.canvas_block.unit_id and active > -1:
                if active == self.ax_h_btn.unit_id:
                    self.change_axis(0)
                elif active == self.ax_v_btn.unit_id:
                    self.change_axis(1)
                elif active == self.ax_d1_btn.unit_id:
                    self.change_axis(2)
                elif active == self.ax_d2_btn.unit_id:
                    self.change_axis(3)
                elif active == self.ax_hv_btn.unit_id:
                    self.change_axis(4)
                elif active == self.ax_dd_btn.unit_id:
                    self.change_axis(5)
                elif active == self.ax_hvdd_btn.unit_id:
                    self.change_axis(6)
                elif active == self.up_btn.unit_id:
                    self.change_points_num(1)
                elif active == self.dn_btn.unit_id:
                    self.change_points_num(-1)
                elif self.board.ships[active] in self.h_units:
                    self.h_door.set_pos(self.board.active_ship_pos)
                    c = active - self.h_units[0].unit_id
                    self.update_colors(c, None, None)
                    self.mainloop.redraw_needed[0] = True
                elif self.board.ships[active] in self.s_units:
                    self.s_door.set_pos(self.board.active_ship_pos)
                    c = active - self.s_units[0].unit_id
                    self.update_colors(None, c, None)
                    self.mainloop.redraw_needed[0] = True
                elif self.board.ships[active] in self.v_units:
                    self.v_door.set_pos(self.board.active_ship_pos)
                    c = active - self.v_units[0].unit_id
                    self.update_colors(None, None, c)
                    self.mainloop.redraw_needed[0] = True

            if event.button == 1 and 0 <= column < self.data[1] and 0 <= row < self.data[1]:
                if self.points_count < self.max_points:
                    canvas_pos = self.snap_to_guide([pos[0] - self.px_padding, pos[1] - self.layout.top_margin])
                    if canvas_pos not in self.points:
                        self.points.append(canvas_pos)

                        self.p_current = canvas_pos
                        self.paint_line(0)

                        self.paint_line(2)
                        self.points_count += 1
                        if self.points_count >= self.max_points:
                            self.check_drawing()

        elif event.type == pygame.MOUSEMOTION and 0 < self.points_count < self.max_points:
            active = self.board.active_ship
            pos = event.pos
            column = (pos[0] - self.px_padding) // (self.layout.width)
            row = (pos[1] - self.layout.top_margin) // (self.layout.height)

            if 0 <= column < self.data[1] and 0 <= row < self.data[1]:
                canvas_pos = self.snap_to_guide([pos[0] - self.px_padding, pos[1] - self.layout.top_margin])

                self.p_current = canvas_pos[:]

                if self.prev_snap is None:
                    self.prev_snap = canvas_pos[:]

                if self.prev_snap != self.p_current:
                    self.prev_snap = canvas_pos[:]
                    self.paint_line(1)

    def update_arrows(self):
        # enable/dissable arrows
        if self.max_points < 4:
            if self.dn_btn.img_src != "nav_dd.png":
                self.dn_btn.change_image("nav_dd.png")
        else:
            if self.dn_btn.img_src != "nav_d.png":
                self.dn_btn.change_image("nav_d.png")


        if self.max_points > 9:
            if self.up_btn.img_src != "nav_ud.png":
                self.up_btn.change_image("nav_ud.png")
        else:
            if self.up_btn.img_src != "nav_u.png":
                self.up_btn.change_image("nav_u.png")

    def change_points_num(self, n):
        if n == 1 and self.max_points < 10 or n == -1 and self.max_points > 3:
            if self.points_count >= self.max_points - 1 and n == -1:
                n = 0

            self.max_points = self.max_points + n

            self.mpl.set_value(str(self.max_points))
            self.update_arrows()
            self.mainloop.redraw_needed[0] = True

    def change_tool(self, tool):
        self.max_points = tool
        self.reset()
        self.mainloop.redraw_needed[0] = True
        if tool < 4:
            self.tool_door.set_pos(self.board.active_ship_pos)

    def change_axis(self, axis):
        self.direction = axis
        self.new_screen()
        self.reset()
        self.mainloop.redraw_needed[0] = True
        if axis < 7:
            self.tool_door.set_pos(self.board.active_ship_pos)

    def paint_line(self, state):
        if state == 0:
            self.copy_to_screen()
            self.backup_canvas()
        elif state == 1:
            self.screen_restore()
            pygame.draw.aaline(self.canvas, self.border_color, self.points[-1], self.p_current, 1)
            if self.points_count == self.max_points - 1:

                if self.max_points == 2:
                    v = sv.Vector2.from_points(self.points[0], self.p_current)
                    if v[0] != 0 or v[1] != 0:
                        r = math.sqrt(v[0] * v[0] + v[1] * v[1])
                    else:
                        r = 0
                    r = int(r)
                    if r > 2:
                        pygame.draw.circle(self.canvas, self.border_color, self.points[0], r, 1)
                        pygame.draw.aaline(self.canvas, self.border_color, self.points[0], self.p_current, 1)
                else:
                    pygame.draw.aaline(self.canvas, self.border_color, self.points[0], self.p_current, 1)
            self.copy_to_screen()
        elif state == 2 and self.points_count > 0:
            self.screen_restore()

            self.draw_line(self.p_current, self.points[-2], 1, 1)
            if self.points_count == self.max_points - 1:
                self.draw_line(self.p_current, self.points[0], 1, 1)
                pygame.draw.circle(self.canvas, self.active_color, self.points[-2], 1, 0)
            self.copy_to_screen()
            self.backup_canvas()

    def draw_line(self, p1, p2, bs1, bs2):
        # find points for the corners of the polygon using Tales Theorem
        # and draw the polygon - rotated rectangle or trapezium and 2 circles at the ends of the 'line'
        v = sv.Vector2.from_points(p1, p2)
        if v[0] != 0 or v[1] != 0:
            bs1 = bs1 // 2
            bs2 = bs2 // 2
            # vector length
            v_len = math.sqrt(v[0] * v[0] + v[1] * v[1])
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
            pygame.draw.polygon(self.canvas, self.border_color, points)
            pygame.draw.aalines(self.canvas, self.border_color, True, points, 1)

            pygame.draw.circle(self.canvas, self.border_color, p1, bs1, 0)
            pygame.draw.circle(self.canvas, self.border_color, p2, bs2, 0)

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

    def v2_to_int(self, vector):
        integers = [int(each) for each in vector]
        return integers

    def draw_guides(self, size):
        x = size
        y = size
        while x < self.layout.game_w:
            p1 = [x, 0]
            p2 = [x, self.layout.game_h]
            pygame.draw.line(self.canvas, self.guides_color, p1, p2, 1)
            x += size
        while y < self.layout.game_h:
            p1 = [0, y]
            p2 = [self.layout.game_w, y]
            pygame.draw.line(self.canvas, self.guides_color, p1, p2, 1)
            y += size
        self.copy_to_screen()

    def snap_to_guide(self, point):
        x = point[0]
        y = point[1]
        dif = [x % self.guide_scale, y % self.guide_scale]
        if dif[0] < self.guide_scale // 2:
            x = x - dif[0]
        else:
            x = x + self.guide_scale - dif[0]

        if dif[1] < self.guide_scale // 2:
            y = y - dif[1]
        else:
            y = y + self.guide_scale - dif[1]

        return [x, y]

    def check_drawing(self):
        if self.direction < 4:
            self.fill_poli()
        elif self.direction < 6:
            self.fill_polix2()
        else:
            self.fill_polix4()
