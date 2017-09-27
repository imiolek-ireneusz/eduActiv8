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
        self.max_points = 4
        self.prev_snap = None

        self.color_s = random.randrange(50, 90, 5)
        self.color_v = random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 1)
        self.bg_color = [255, 255, 255]
        color = [255, 255, 255]
        white = (255, 255, 255)
        self.guides_color = [200, 200, 200]
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

        data = [15, 12]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=None)
        if x_count > data[0]:
            data[0] = x_count
        else:
            y_count = self.get_y_count(data[0], even=None)
            data[1] = y_count - 1
        self.data = data

        self.mainloop.info.hide_buttons(0, 0, 0, 0, 1, 1, 1, 0, 0)
        self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.reset()

        if self.mainloop.android is None:
            self.grid_density_div = lvl_data[0]
        else:
            self.grid_density_div = 1

        self.guide_scale = self.board.scale // self.grid_density_div
        self.left_padding = 2
        self.px_padding = self.left_padding * scale + self.layout.game_left
        # canvas
        self.board.add_unit(self.left_padding, 0, data[0] - self.left_padding, data[1], classes.board.Letter, "", color,
                            "", 2)
        self.canvas_block = self.board.ships[-1]
        self.canvas_block.set_outline([0, 54, 229], 1)
        self.board.add_unit(0, 0, 2, 2, classes.board.ImgShip, "", white,
                            os.path.join("schemes", scheme, "c_quati.png"), 0)
        self.poli_btn = self.board.ships[-1]

        self.board.add_unit(0, 2, 2, 2, classes.board.ImgShip, "", white, os.path.join("schemes", scheme, "c_tria.png"),
                            0)
        self.tria_btn = self.board.ships[-1]

        self.board.add_unit(0, 4, 2, 2, classes.board.ImgShip, "", white,
                            os.path.join("schemes", scheme, "c_circle.png"), 0)
        self.circle_btn = self.board.ships[-1]

        self.btn_down = False

        for each in self.board.ships:
            each.outline = False
            each.immobilize()
            each.readable = False
        self.figures = [0, 1, 2, 3, 4, 5, 6]
        self.names = [self.lang.d["trapezium"], self.lang.d["square"], self.lang.d["parallelogram"],
                      self.lang.d["rectangle"], self.lang.d["right_trapezium"], self.lang.d["iso_trapezium"],
                      self.lang.d["rhombus"]]
        self.sides = [[True, True, True], [True, False, False], [True, True, True], [True, True, False],
                      [True, True, True], [True, True, True], [True, False, False]]

        self.canvas = pygame.Surface(
            [self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1])
        self.new_screen()
        # self.vectors = []
        self.board.add_door(0, 0, 2, 2, classes.board.Door, "", color, "")

        self.tool_door = self.board.units[-1]
        self.tool_door.door_outline = True
        self.board.all_sprites_list.move_to_front(self.tool_door)

    def new_screen(self):
        self.canvas.fill(self.canvas_block.initcolor)
        self.draw_guides(self.guide_scale)
        self.canvas_org = self.canvas.copy()
        self.copy_to_screen()

    def reset(self):
        self.points = []
        self.points_count = 0
        self.active_color = [255, 0, 0]
        self.p_current = [0, 0]

    def fill_poli(self, point_count):
        self.points.append(self.points[0])
        pygame.draw.polygon(self.canvas, self.active_color, self.points, 0)
        pygame.draw.polygon(self.canvas, self.canvas_block.font_color, self.points, 3)
        if self.name != "":
            h_min = min([self.points[i][0] for i in range(point_count)])
            h_max = max([self.points[i][0] for i in range(point_count)])
            v_max = max([self.points[i][1] for i in range(point_count)])

            self.draw_name(self.name, h_min + (h_max - h_min) // 2, v_max)
        self.reset()
        self.copy_to_screen()
        self.backup_canvas()

    def get_set_r(self):
        v = sv.Vector2.from_points(self.points[0], self.points[1])
        if v[0] != 0 or v[1] != 0:
            r = math.sqrt(v[0] * v[0] + v[1] * v[1])
        else:
            r = 0
        r = int(r)
        self.circle_r = r
        return r

    def fill_circle(self):
        self.get_set_r()
        r = self.circle_r
        pygame.draw.circle(self.canvas, self.active_color, self.points[0], r, 0)
        pygame.draw.circle(self.canvas, self.canvas_block.font_color, self.points[0], r, 3)
        pygame.draw.aaline(self.canvas, self.canvas_block.font_color, self.points[0], self.points[1], 1)
        self.get_set_r()

        h_min = self.points[0][0] - self.circle_r
        h_max = self.points[0][0] + self.circle_r
        v_max = self.points[0][1] + self.circle_r

        self.draw_name(self.name, h_min + (h_max - h_min) // 2, v_max)
        self.reset()
        self.copy_to_screen()
        self.backup_canvas()

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
            if active != self.canvas_block.unit_id:
                if active == self.poli_btn.unit_id:
                    self.change_tool(4)
                elif active == self.tria_btn.unit_id:
                    self.change_tool(3)
                elif active == self.circle_btn.unit_id:
                    self.change_tool(2)

            if event.button == 1 and column >= 0 and 0 <= row < self.data[1]:
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

            if column >= 0 and 0 <= row < self.data[1]:
                canvas_pos = self.snap_to_guide([pos[0] - self.px_padding, pos[1] - self.layout.top_margin])

                self.p_current = canvas_pos[:]

                if self.prev_snap is None:
                    self.prev_snap = canvas_pos[:]

                if self.prev_snap != self.p_current:
                    self.prev_snap = canvas_pos[:]
                    self.paint_line(1)

    def change_tool(self, tool):
        self.max_points = tool
        self.reset()
        self.mainloop.redraw_needed[0] = True
        self.tool_door.set_pos(self.board.active_ship_pos)

    def paint_line(self, state):
        if state == 0:
            self.copy_to_screen()
            self.backup_canvas()
        elif state == 1:
            self.screen_restore()
            pygame.draw.aaline(self.canvas, self.active_color, self.points[-1], self.p_current, 1)
            if self.points_count == self.max_points - 1:

                if self.max_points == 2:
                    v = sv.Vector2.from_points(self.points[0], self.p_current)
                    if v[0] != 0 or v[1] != 0:
                        r = math.sqrt(v[0] * v[0] + v[1] * v[1])
                    else:
                        r = 0
                    r = int(r)
                    if r > 2:
                        pygame.draw.circle(self.canvas, self.active_color, self.points[0], r, 1)
                        pygame.draw.aaline(self.canvas, self.active_color, self.points[0], self.p_current, 1)
                else:
                    pygame.draw.aaline(self.canvas, self.active_color, self.points[0], self.p_current, 1)
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
            pygame.draw.polygon(self.canvas, self.active_color, points)
            pygame.draw.aalines(self.canvas, self.active_color, True, points, 1)

            pygame.draw.circle(self.canvas, self.active_color, p1, bs1, 0)
            pygame.draw.circle(self.canvas, self.active_color, p2, bs2, 0)

    def draw_name(self, name, x, y):
        val = name
        if sys.version_info < (3, 0):
            try:
                val = unicode(name, "utf-8")
            except UnicodeDecodeError:
                val = name
            except TypeError:
                val = name

        text = self.canvas_block.font.render("%s" % (val), 1, self.canvas_block.font_color)
        offset = self.canvas_block.font.size(val)[0] // 2
        if x < offset + 5:
            pos_x = 5
        elif x + offset > self.canvas_block.rect.width:
            pos_x = self.canvas_block.rect.width - offset * 2 - 5
        else:
            pos_x = x - offset

        if y > self.canvas_block.rect.height - self.canvas_block.font.size(val)[1]:
            y = self.canvas_block.rect.height - self.canvas_block.font.size(val)[1] - 5

        self.canvas.blit(text, (pos_x, y))

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
        h = random.randrange(0, 255, 1)
        if self.mainloop.scheme is None:
            self.canvas_block.font_color = ex.hsv_to_rgb(h, self.color_s + 100, self.color_v - 100)
            self.active_color = ex.hsv_to_rgb(h, self.color_s, self.color_v)
        else:
            self.canvas_block.font_color = self.mainloop.scheme.u_font_color
            self.active_color = self.mainloop.scheme.shape_color
        if self.max_points == 4:
            self.check_quadrilateral(self.points)
            self.fill_poli(4)
        elif self.max_points == 3:
            self.check_triangle(self.points)
            self.fill_poli(3)
        elif self.max_points == 2:
            self.check_circle(self.points)
            self.fill_circle()

    def scalar_product(self, v1, v2):
        return sum([v1[i] * v2[i] for i in range(len(v1))])

    def side_len(self, v):
        x = max(v[0][0], v[1][0]) - min(v[0][0], v[1][0])
        y = max(v[0][1], v[1][1]) - min(v[0][1], v[1][1])
        return math.sqrt(x ** 2 + y ** 2)

    def vector_len(self, v):
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    def is_orthogonal(self, v1, v2):
        epsilon = 0.00001
        return abs(self.scalar_product(v1, v2) / (self.vector_len(v1) * self.vector_len(v2))) < epsilon

    def angle(self, v1, v2):
        return self.scalar_product(v1, v2) / (self.vector_len(v1) * self.vector_len(v2))

    def is_parallel(self, v1, v2):
        epsilon = 0.00001
        return abs(self.scalar_product(v1, v2) / (self.vector_len(v1) * self.vector_len(v2))) > 1 - epsilon

    def not_intersecting(self, A, B, C, D):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    def crossing(self, A, B, C, D):
        return self.not_intersecting(A, C, B, D) or self.not_intersecting(B, C, D, A)

    def collinear(self, p0, p1, p2):
        x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
        x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
        return x1 * y2 - x2 * y1 == 0  # 1e-12

    def collinear4(self, p):
        if self.collinear(p[0], p[1], p[2]) or self.collinear(p[1], p[2], p[3]) or self.collinear(p[2], p[3], p[
            0]) or self.collinear(p[3], p[0], p[1]):
            return True
        else:
            return False

    def collinear_all(self, p):
        if self.collinear(p[0], p[1], p[2]) and self.collinear(p[1], p[2], p[3]) and self.collinear(p[2], p[3], p[
            0]) and self.collinear(p[3], p[0], p[1]):
            return True
        else:
            return False

    def points_to_vectors(self, points):
        vectors = []
        l = len(points)
        for i in range(l):
            p1 = points[i]
            if i < l - 1:
                p2 = points[i + 1]
            else:
                p2 = points[0]
            v = [p2[0] - p1[0], p2[1] - p1[1]]
            self.vectors.append([p1, p2])
            vectors.append(v)
        return vectors

    def check_quadrilateral(self, points):
        self.vectors = []
        v = self.points_to_vectors(points)
        if self.crossing(points[1], points[3], points[0], points[2]):
            self.name = ""
        else:
            self.name = self.lang.d["quadrilateral"]
        if (self.is_parallel(v[0], v[2]) and self.not_intersecting(points[1], points[3], points[0], points[2])) or (
            self.is_parallel(v[1], v[3]) and self.not_intersecting(points[0], points[2], points[1], points[3])):
            self.name = self.lang.d["trapezium"]
            if self.is_parallel(v[0], v[2]) and self.is_parallel(v[1], v[3]):
                self.name = self.lang.d["parallelogram"]
                if abs(self.side_len(self.vectors[0]) - self.side_len(self.vectors[1])) < 0.01:
                    self.name = self.lang.d["rhombus"]
                    if self.is_orthogonal(v[0], v[1]):
                        self.name = self.lang.d["square"]
                elif self.is_orthogonal(v[0], v[1]):
                    self.name = self.lang.d["rectangle"]
            elif self.is_orthogonal(v[0], v[1]) or self.is_orthogonal(v[1], v[2]) or self.is_orthogonal(v[2], v[
                3]) or self.is_orthogonal(v[3], v[0]):
                self.name = self.lang.d["right_trapezium"]
            elif abs(self.side_len(self.vectors[0]) - self.side_len(self.vectors[2])) < 0.01 or abs(
                            self.side_len(self.vectors[1]) - self.side_len(self.vectors[3])) < 0.01:
                self.name = self.lang.d["iso_trapezium"]
        elif self.collinear4(points) and not self.collinear_all(points):
            self.name = self.lang.d["triangle_not_really"]
        elif self.collinear_all(points):
            self.name = self.lang.d["squished_quadi"] + " :)"

    def check_triangle(self, points):
        self.vectors = []
        v = self.points_to_vectors(points)
        self.name = self.lang.d["triangle"]

        if self.collinear(v[0], v[1], v[2]):
            self.name = self.lang.d["squished_tria"] + " :)"
        else:
            self.name = self.lang.d["triangle"]
            if self.t_right(v):
                if self.t_iso():
                    self.name = self.lang.d["right_iso_tria"]
                else:
                    self.name = self.lang.d["right_tria"]
            elif self.t_acute(v):
                if self.t_equi(v):
                    self.name = self.lang.d["equi_tria"]
                elif self.t_iso():
                    self.name = self.lang.d["acute_iso_tria"]
                else:
                    self.name = self.lang.d["acute_tria"]
            else:  # if self.t_obtuse(v):
                if self.t_iso():
                    self.name = self.lang.d["obtuse_iso_tria"]
                else:
                    self.name = self.lang.d["obtuse_tria"]

    def t_right(self, v):
        return self.is_orthogonal(v[0], v[1]) or self.is_orthogonal(v[1], v[2]) or self.is_orthogonal(v[2], v[0])

    def t_iso(self):
        return abs(self.side_len(self.vectors[0]) - self.side_len(self.vectors[1])) < 0.01 or abs(
            self.side_len(self.vectors[1]) - self.side_len(self.vectors[2])) < 0.01 or abs(
            self.side_len(self.vectors[2]) - self.side_len(self.vectors[0])) < 0.01

    def t_acute(self, v):
        return self.angle(v[0], v[1]) < 0 and self.angle(v[1], v[2]) < 0 and self.angle(v[2], v[0]) < 0

    def t_obtuse(self, v):
        return not self.t_acute * (v)

    def t_equi(self, v):
        return self.vector_len(v[0]) == self.vector_len(v[1]) == self.vector_len(v[2])

    def check_circle(self, points):
        self.name = self.lang.d["circle"]
