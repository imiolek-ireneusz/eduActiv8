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
        self.prev_snap = None

        self.correct = False

        self.color_s = random.randrange(50, 90, 5)
        self.color_v = random.randrange(230, 255, 5)

        h = random.randrange(0, 255, 1)
        self.bg_color = [255, 255, 255]
        color = [255, 255, 255]
        white = (255, 255, 255)
        self.transp = (0, 0, 0, 0)

        self.active_color = ex.hsva_to_rgba(h, 127, 255, 127)
        self.border_color = ex.hsv_to_rgb(h, 200, 205)

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


        #data = [27, 20, random.randint(3, 5), random.randint(0, 3)]
        #data = [27, 20, random.randint(3, 5), random.randint(0, 3), True]

        #[19, 14, random.randint(3, 5), random.randint(0, 3), half]
        if lvl_data[2] == 0:
            data = [18, 14, random.randint(3, 5), random.randint(0, 3), lvl_data[-1]]
        else:
            data = lvl_data

        self.data = data

        self.max_points = self.data[2]
        self.direction = self.data[3]
        self.half_only = self.data[4]

        #self.images = ["ax_h.png", "ax_v.png", "ax_d1.png", "ax_d2.png"]

        #self.mainloop.info.hide_buttons(0, 0, 0, 0, 1, 1, 1, 0, 0)
        #self.vis_buttons = [0, 0, 0, 0, 1, 1, 1, 0, 0]
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.scale = scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.line_color = (20, 20, 20)

        if self.mainloop.android is None:
            self.grid_density_div = lvl_data[0]
        else:
            self.grid_density_div = 1

        self.guide_scale = self.board.scale# // self.grid_density_div
        self.left_padding = 2#3
        self.px_padding = self.left_padding * scale + self.layout.game_left
        # canvas
        self.canvas_side = min(data[0] - self.left_padding, data[1])
        self.canvas_half_size = self.canvas_side // 2
        self.board.add_unit(self.left_padding, 0, self.canvas_side, self.canvas_side, classes.board.Letter, "", color,
                            "", 2)
        self.canvas_block = self.board.ships[-1]
        self.canvas_block.set_outline([0, 54, 229], 1)

        #self.board.add_unit(0, 0, 2, 2, classes.board.ImgShip, "", white, os.path.join("symmetry", self.images[self.direction]), 0, alpha=True)

        self.board.add_unit(data[1]+self.left_padding, 0, 2, 2, classes.board.Letter, "", white, "", 0)
        self.check_btn = self.board.ships[-1]
        self.check_btn.checkable = True
        self.check_btn.init_check_images(align=1, shrink=1)
        self.btn_down = False

        self.board.add_unit(data[1]+self.left_padding, 6, 2, 2, classes.board.ImgCenteredShip, "", white, img_src='nav_refreshd.png', alpha=True)
        self.rt_btn = self.board.ships[-1]

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

        self.reset()
        if self.mainloop.m.game_variant == 0:
            self.random_points = self.pick_half_shape()
        elif self.mainloop.m.game_variant == 1:
            self.random_points = self.pick_random_shape()

        self.draw_random_shape()

    def new_screen(self):
        self.canvas.fill(self.canvas_block.initcolor)
        self.draw_guides(self.guide_scale)
        self.draw_axis(self.direction)
        self.canvas_org = self.canvas.copy()
        self.copy_to_screen()

    def reset(self):
        self.points = []
        self.points_count = 0
        self.p_current = [0, 0]

    def redraw_task_shape(self):
        self.reset()
        self.new_screen()
        self.draw_random_shape()
        self.auto_check_reset()

    def layer_blit(self):
        self.canvas.blit(self.layer, (0, 0))
        self.layer.fill(self.transp)

    def fill_poli(self):
        p2 = self.get_simetrical_shape(self.direction, self.points)

        #draw shape
        self.points.append(self.points[0])
        pygame.draw.polygon(self.layer, self.active_color, self.points, 0)
        pygame.draw.polygon(self.layer, self.border_color, self.points, 3)
        self.check_symmetry(p2)
        self.layer_blit()

        #draw symetrical shape if not correct
        if not self.correct:
            p2.append(p2[0])
            pygame.draw.polygon(self.layer, self.active_color, p2, 0)

            #redraw outlines
            pygame.draw.polygon(self.layer, self.border_color, p2, 3)
            self.layer_blit()

        #draw the task shape outline
        #pygame.draw.polygon(self.layer, self.border_color, self.random_points, 3)

        self.draw_axis(self.direction)

        self.reset()
        self.copy_to_screen()


    def check_symmetry(self, p2):
        #check if the drawn shape has points in the same place
        symmetrical = True
        for each in p2:
            if each not in self.random_points:
                symmetrical = False
                break

        if symmetrical:
            #check if angles and lengths are the same
            lst = [self.random_points, p2]
            a_total = [0, 0]
            l_total = [0, 0]
            for j in range(2):
                v = self.points_to_vectors(lst[j])
                for i in range(len(v)):
                    sl = self.side_len((lst[j][i - 1], lst[j][i]))
                    a = self.angle(v[i - 1], v[i])
                    a_total[j] += a
                    l_total[j] += sl
            if abs(a_total[0] - a_total[1]) > 0.1 or abs(l_total[0] - l_total[1]) > 0.1:
                symmetrical = False

        if symmetrical:
            self.check_btn.set_display_check(True)
            self.correct = True
        else:
            self.check_btn.set_display_check(False)
            self.correct = False

        #if self.correct:
        #pygame.time.delay(1000)
        #self.level.next_board()
        if not self.correct:
            if self.rt_btn.img_src != "nav_refresh.png":
                self.rt_btn.change_image("nav_refresh.png")
        else:
            if self.rt_btn.img_src != "nav_r.png":
                self.rt_btn.change_image("nav_r.png")

        self.mainloop.redraw_needed[0] = True


    def pick_random_shape(self):
        if self.half_only:
            corners = self.max_points
            side = random.randint(0, 1)
            if self.direction == 0:
                minx = 1
                maxx = self.canvas_side - 1
                if side == 0:
                    miny = 1
                    maxy = self.canvas_side / 2 - 1
                else:
                    miny = self.canvas_side / 2 + 1
                    maxy = self.canvas_side - 1
            elif self.direction == 1:
                miny = 1
                maxy = self.canvas_side - 1
                if side == 0:
                    minx = 1
                    maxx = self.canvas_side / 2 - 1
                else:
                    minx = self.canvas_side / 2 + 1
                    maxx = self.canvas_side - 1

            invalid_shape = False
            points = []
            l = 0
            while l < corners:
                if self.direction < 2:
                    x = random.randint(minx, maxx)
                    y = random.randint(miny, maxy)
                elif self.direction == 2:
                    if side == 0:
                        x = random.randrange(2, self.canvas_side - 1)
                        y = random.randrange(1, x)
                    else:
                        x = random.randint(1, self.canvas_side - 2)
                        y = random.randint(x + 1, self.canvas_side - 1)

                elif self.direction == 3:
                    if side == 0:
                        x = random.randint(1, self.canvas_side - 2)
                        y = random.randint(1, self.canvas_side - x - 1)
                    else:
                        x = random.randint(2, self.canvas_side - 1)
                        y = random.randint(self.canvas_side - x + 1, self.canvas_side - 1)

                p = [x * self.guide_scale, y * self.guide_scale]
                if p not in points:
                    if l < 2:
                        points.append(p)
                        l += 1
                    else:
                        if not self.p_collinear_with(p, points):
                            points.append(p)
                            l += 1
            v = self.points_to_vectors(points)
            for i in range(len(v)):
                sl = self.side_len((points[i - 1], points[i]))
                a = self.angle(v[i-1], v[i])
                if sl < self.scale * 3 - 1 or not -0.95 < a < 0.95:
                    invalid_shape = True
                    break
            if self.max_points > 3 and self.intersecting(points):
                invalid_shape = True

            if invalid_shape:
                points = self.pick_random_shape()

            return points
        else:
            corners = self.max_points
            mn = 1
            mx = self.canvas_side - 1
            invalid_shape = False
            points = []
            l = 0
            while l < corners:
                x = random.randint(mn, mx)
                y = random.randint(mn, mx)

                p = [x * self.guide_scale, y * self.guide_scale]
                if p not in points:
                    if l < 2:
                        points.append(p)
                        l += 1
                    else:
                        if not self.p_collinear_with(p, points):
                            points.append(p)
                            l += 1
            v = self.points_to_vectors(points)
            for i in range(len(v)):
                sl = self.side_len((points[i - 1], points[i]))
                a = self.angle(v[i - 1], v[i])
                if sl < self.scale * 3 - 1 or not -0.95 < a < 0.95:
                    invalid_shape = True
                    break
            if self.max_points > 3 and self.intersecting(points):
                invalid_shape = True

            if invalid_shape:
                points = self.pick_random_shape()

            return points

    def pick_half_shape(self):
        points = []
        invalid_shape = False
        n = 0
        p1 = [0, 0]
        p2 = [0, 0]
        inner = True
        if self.direction == 0:
            # add 2 points on a line and one outside
            while inner:
                p1 = [random.randrange(1, self.canvas_side - 1) * self.guide_scale, (self.canvas_side // 2) * self.guide_scale]
                p2 = [random.randrange(1, self.canvas_side - 1) * self.guide_scale, (self.canvas_side // 2) * self.guide_scale]
                if abs(p1[0] - p2[0]) > 2 * self.guide_scale:
                    inner = False
            points.append(p1)

            # add remaining points
            while n < self.max_points - 2:
                pn = [random.randrange(1, self.canvas_side - 1) * self.guide_scale, random.randrange(1, self.canvas_side // 2 - 2) * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    n += 1
            points.append(p2)

        elif self.direction == 1:
            # add 2 points on a line and one outside
            while inner:
                p1 = [(self.canvas_side // 2) * self.guide_scale, random.randrange(1, self.canvas_side - 1) * self.guide_scale]
                p2 = [(self.canvas_side // 2) * self.guide_scale, random.randrange(1, self.canvas_side - 1) * self.guide_scale]
                if abs(p1[1] - p2[1]) > 2 * self.guide_scale:
                    inner = False
            points.append(p1)

            # add remaining points
            while n < self.max_points - 2:
                pn = [random.randrange(1, self.canvas_side // 2 - 2) * self.guide_scale, random.randrange(1, self.canvas_side - 1) * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    n += 1
            points.append(p2)

        elif self.direction == 2:
            while inner:
                x1 = random.randrange(1, self.canvas_side)
                p1 = [x1 * self.guide_scale, x1 * self.guide_scale]
                x2 = random.randrange(1, self.canvas_side)
                p2 = [x2 * self.guide_scale, x2 * self.guide_scale]
                if abs(x1 - x2) > 2:
                    inner = False
            points.append(p1)

            # add remaining points
            while n < self.max_points - 2:
                x = random.randrange(2, self.canvas_side - 1)
                y = random.randrange(1, x)
                pn = [x * self.guide_scale, y * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    n += 1
            points.append(p2)

        elif self.direction == 3:
            # add 2 points on a line and one outside
            while inner:
                x1 = random.randrange(1, self.canvas_side - 1)
                y1 = self.canvas_side - x1
                p1 = [x1 * self.guide_scale, y1 * self.guide_scale]
                x2 = random.randrange(1, self.canvas_side - 1)
                y2 = self.canvas_side - x2
                p2 = [x2 * self.guide_scale, y2 * self.guide_scale]
                if abs(x1 - x2) > 2:
                    inner = False
            points.append(p1)

            # add remaining points
            while n < self.max_points - 2:
                x = random.randrange(1, self.canvas_side - 2)
                y = random.randrange(1, self.canvas_side - x)
                pn = [x * self.guide_scale, y * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    n += 1

            points.append(p2)

        v = self.points_to_vectors(points)
        a_total = 0  #sum of all angles - used to make sure all angles are not square - too many lines of symmetry
        for i in range(len(v)):
            sl = self.side_len((points[i - 1], points[i]))
            a = self.angle(v[i - 1], v[i])
            a_total += a
            if sl < self.scale * 3 - 1 or not -0.95 < a < 0.95:
                invalid_shape = True
                break
        if self.max_points > 3 and self.intersecting(points):
            invalid_shape = True

        if invalid_shape:
            points = self.pick_half_shape()

        return points

    def draw_random_shape(self):
        # draw shape
        points = self.random_points[:]
        points.append(points[0])
        pygame.draw.polygon(self.layer, self.active_color, points, 0)

        # redraw outlines
        pygame.draw.polygon(self.layer, self.border_color, points, 3)
        self.layer_blit()
        #self.draw_guides(self.guide_scale)
        self.draw_axis(self.direction)
        self.reset()
        self.copy_to_screen()

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
            vectors.append(v)
        return vectors

    def side_len(self, v):
        x = max(v[0][0], v[1][0]) - min(v[0][0], v[1][0])
        y = max(v[0][1], v[1][1]) - min(v[0][1], v[1][1])
        return math.sqrt(x ** 2 + y ** 2)

    def scalar_product(self, v1, v2):
        return sum([v1[i] * v2[i] for i in range(len(v1))])

    def vector_len(self, v):
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    def angle(self, v1, v2):
        return self.scalar_product(v1, v2) / (self.vector_len(v1) * self.vector_len(v2))

    def intersecting(self, p):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        l = len(p)
        b = False
        for i in range(l):
            b = b or (ccw(p[i-0], p[i-2], p[i-3]) != ccw(p[i-1], p[i-2], p[i-3]) and ccw(p[i-0], p[i-1], p[i-2]) != ccw(p[i-0], p[i-1], p[i-3]))
        return b

    def collinear(self, p0, p1, p2):
        x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
        x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
        return x1 * y2 - x2 * y1 == 0  # 1e-12

    def collinear_poli(self, p_list):
        for i in range(len(p_list)):
            if self.collinear(p_list[i], p_list[i-1], p_list[i-2]):
                return True
        return False

    def p_collinear_with(self, p, p_list):
        pl = p_list[:]
        pl.append(p)
        return self.collinear_poli(pl)


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
                if self.board.ships[active] == self.rt_btn:
                    if self.correct:
                        self.level.next_board()
                        self.mainloop.redraw_needed[0] = True
                    else:
                        self.redraw_task_shape()

            if event.button == 1 and 0 <= column < self.data[1] and 0 <= row < self.data[1]:
                if self.points_count == 0:
                    self.redraw_task_shape()
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

    def change_points_num(self, n):
        if n == 1 and self.max_points < 10 or n == -1 and self.max_points > 3:
            if self.points_count >= self.max_points - 1 and n == -1:
                n = 0
            self.max_points = self.max_points + n
            self.mainloop.redraw_needed[0] = True

    def change_tool(self, tool):
        self.max_points = tool
        self.reset()
        self.mainloop.redraw_needed[0] = True
        #if tool < 4:
        #    self.tool_door.set_pos(self.board.active_ship_pos)

    def change_axis(self, axis):
        self.direction = axis
        self.new_screen()
        self.reset()
        self.mainloop.redraw_needed[0] = True
        #if axis < 7:
        #    self.tool_door.set_pos(self.board.active_ship_pos)

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

    def auto_check_reset(self):
        self.check_btn.set_display_check(None)
        self.correct = False
        if self.rt_btn.img_src != "nav_refreshd.png":
            self.rt_btn.change_image("nav_refreshd.png")

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Draw symmetrical shape - instruction"])
