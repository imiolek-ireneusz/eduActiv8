# -*- coding: utf-8 -*-

import math
import os
import pygame
import random

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
        self.active_color = ex.hsv_to_rgb(h, 127, 255)
        self.border_color = ex.hsv_to_rgb(h, 200, 205)

        self.lbl_font_color = ex.hsv_to_rgb(h, 200, 255)
        self.guides_color = [200, 200, 200]
        self.axis_color = [255, 0, 0]
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                white = (0, 0, 0)
                self.bg_color = (0, 0, 0)
                color = (0, 0, 0)
                self.guides_color = (30, 30, 30)


        lvl_data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                         self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        self.data = data = lvl_data

        if lvl_data[2] == 0:
            self.data[2] = random.randint(2, 4)
        if lvl_data[3] == 0:
            self.data[3] = random.randint(0, 3)
        if lvl_data[4] == 0:
            self.data[4] = random.randint(1, 2)

        self.recursion_depth = 0
        self.max_points = self.data[2] + 2
        self.direction = self.data[3]
        self.half_only = self.data[4]
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 1]
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

        self.selected = [0, 0, 0, 0]

        # add mid selectors
        # --
        self.board.add_unit(0, self.data[1]//2 - 1, 1, 2, classes.board.ImgCenteredShip, "", white, os.path.join("symmetry", "shl.png"), 0, alpha=True)
        self.board.add_unit(self.data[1] - 1, self.data[1]//2 - 1, 1, 2, classes.board.ImgCenteredShip, "", white, os.path.join("symmetry", "shr.png"), 0, alpha=True)

        # |
        self.board.add_unit(self.data[1]//2 - 1, 0, 2, 1, classes.board.ImgCenteredShip, "", white, os.path.join("symmetry", "svt.png"), 0, alpha=True)
        self.board.add_unit(self.data[1]//2 - 1, self.data[1]-1, 2, 1, classes.board.ImgCenteredShip, "", white, os.path.join("symmetry", "svb.png"), 0, alpha=True)

        #add corner selectors
        # \
        self.board.add_unit(0, 0, 1, 1, classes.board.ImgShip, "", white, os.path.join("symmetry", "stl.png"), 0, alpha=True)
        self.board.add_unit(self.data[1]-1, self.data[1]-1, 1, 1, classes.board.ImgShip, "", white, os.path.join("symmetry", "sbr.png"), 0, alpha=True)

        # /
        self.board.add_unit(self.data[1]-1, 0, 1, 1, classes.board.ImgShip, "", white, os.path.join("symmetry", "str.png"), 0, alpha=True)
        self.board.add_unit(0, self.data[1]-1, 1, 1, classes.board.ImgShip, "", white, os.path.join("symmetry", "sbl.png"), 0, alpha=True)

        self.selectors = self.board.ships[:]

        for each in self.selectors:
            each.img_src_org = each.img_src[:]
            each.checkable = True
            each.init_check_images(align=1, shrink=1)

        for i in range(8):
            sh = 1
            if i < 2:
                sh = 2
            self.selectors[i].img_src_org = self.selectors[i].img_src[:]
            self.selectors[i].checkable = True
            self.selectors[i].init_check_images(align=1, shrink=sh)

        self.guide_scale = self.board.scale  # // self.grid_density_div
        self.left_padding = 0  # 3
        self.px_padding = self.left_padding * scale + self.layout.game_left
        # canvas
        self.canvas_side = min(data[0] - self.left_padding - 2, data[1] - 2)
        self.canvas_half_size = self.canvas_side // 2
        self.board.add_unit(self.left_padding + 1, 1, self.canvas_side, self.canvas_side, classes.board.Letter, "",
                            color, "", 2)
        self.canvas_block = self.board.ships[-1]

        for each in self.board.ships:
            each.outline = False
            each.highlight = False
            each.immobilize()
            each.readable = False

        self.canvas_block.set_outline([0, 54, 229], 1)
        self.canvas = pygame.Surface(
            [self.canvas_block.grid_w * self.board.scale, self.canvas_block.grid_h * self.board.scale - 1])
        self.new_screen()
        self.reset()

        if self.data[4] == 1:
            self.random_points = self.pick_random_shape()
        else:
            self.random_points = self.pick_duosimm_shape()

        self.draw_random_shape()

    def new_screen(self):
        self.canvas.fill(self.canvas_block.initcolor)
        self.draw_guides(self.guide_scale)
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

    def fill_poli(self):
        p2 = self.get_simetrical_shape(self.direction, self.points)

        #draw shape
        self.points.append(self.points[0])
        pygame.draw.polygon(self.canvas, self.active_color, self.points, 0)

        #draw symetrical shape
        p2.append(p2[0])
        pygame.draw.polygon(self.canvas, self.active_color, p2, 0)

        #redraw outlines
        pygame.draw.polygon(self.canvas, self.border_color, p2, 3)
        pygame.draw.polygon(self.canvas, self.border_color, self.points, 3)

        #drow the task shape outline
        pygame.draw.polygon(self.canvas, self.border_color, self.random_points, 3)

        self.reset()
        self.copy_to_screen()

    def pick_duosimm_shape(self):
        """Generate a shape that has at least 2 lines of symmetry."""
        points = []
        invalid_shape = False
        n = 0
        if self.direction < 2:
            #draw 2 points one on x and one on y axis
            p1 = [random.randrange(1, self.canvas_side // 2 - 1) * self.guide_scale,
                  (self.canvas_side // 2) * self.guide_scale]
            p2 = [(self.canvas_side // 2) * self.guide_scale,
                  random.randrange(1, self.canvas_side // 2 - 1) * self.guide_scale]

            #if more points needed select them as well
            points.append(p1)

            # add remaining points
            while n < self.data[2]:
                pn = [random.randrange(1, self.canvas_side // 2 - 1) * self.guide_scale,
                      random.randrange(1, self.canvas_side // 2 - 1) * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    n += 1
            points.append(p2)

            #copy quarter to the right
            lp = len(points)
            for i in range(lp - 2, -1, -1):
                x = (self.canvas_side // 2) * self.guide_scale + (self.canvas_side // 2) * self.guide_scale - points[i][0]
                y = points[i][1]
                points.append([x, y])

            #copy all to the bottom
            lp = len(points)
            for i in range(lp - 2, 0, -1):
                x = points[i][0]
                y = (self.canvas_side // 2) * self.guide_scale + (self.canvas_side // 2) * self.guide_scale - \
                    points[i][1]
                points.append([x, y])
        else: #diagonal
            # draw 2 points one on x and one on y axis
            x = random.randrange(1, self.canvas_side // 2 - 1)
            p1 = [x * self.guide_scale, x * self.guide_scale]
            x = random.randrange(self.canvas_side // 2 + 1, self.canvas_side - 1)
            y = self.canvas_side - x
            p2 = [x * self.guide_scale, y * self.guide_scale]

            # if more points needed select them as well
            points.append(p1)

            # add remaining points
            while n < self.data[2]:
                x = random.randrange(2, self.canvas_side - 1)
                y = random.randrange(1, min(x, self.canvas_side - x))
                pn = [x * self.guide_scale, y * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    n += 1

            points.append(p2)

            # copy quarter to the bottom right
            lp = len(points)
            for i in range(lp - 2, -1, -1):
                x = self.canvas_side * self.guide_scale - points[i][1]  # (self.canvas_side // 2) * self.guide_scale + (self.canvas_side // 2) * self.guide_scale - points[i][0]
                y = self.canvas_side * self.guide_scale - points[i][0]
                points.append([x, y])

            # copy all to the bottom
            lp = len(points)
            for i in range(lp - 2, 0, -1):
                points.append([points[i][1], points[i][0]])

        v = self.points_to_vectors(points)
        a_total = 0  # sum of all angles - used to make sure all angles are not square - too many lines of symmetry
        for i in range(len(v)):
            sl = self.side_len((points[i - 1], points[i]))
            a = self.angle(v[i - 1], v[i])
            a_total += a
            if sl < self.scale - 1 or not -0.99 < a < 0.99:
                invalid_shape = True
                break

        if (self.max_points > 3 and self.intersecting(points)) or -0.2 < a_total < 0.2:
            invalid_shape = True

        if invalid_shape:
            self.recursion_depth += 1
            if self.recursion_depth < 15: #retry up to 15 times and display
                points = self.pick_duosimm_shape()

        return points


    def pick_random_shape(self):
        """Generate a random shape that has at least one line of symmetry"""
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

            #find mirrored points
            for i in range(self.max_points - 2, 0, -1):
                d = self.canvas_half_size * self.guide_scale - points[i][1]
                pn = [points[i][0], self.canvas_half_size * self.guide_scale + d]
                points.append(pn)
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

            #find mirrored points
            for i in range(self.max_points - 2, 0, -1):
                d = self.canvas_half_size * self.guide_scale - points[i][0]
                pn = [self.canvas_half_size * self.guide_scale + d, points[i][1]]
                points.append(pn)
        elif self.direction == 2:
            while inner:
                x1 = random.randrange(1, self.canvas_side)
                p1 = [x1 * self.guide_scale, x1 * self.guide_scale]
                x2 = random.randrange(1, self.canvas_side)
                p2 = [x2 * self.guide_scale, x2 * self.guide_scale]
                if abs(x1 - x2) > 2:
                    inner = False
            points.append(p1)

            mirrored = []
            # add remaining points
            while n < self.max_points - 2:
                x = random.randrange(2, self.canvas_side - 1)
                y = random.randrange(1, x)
                pn = [x * self.guide_scale, y * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    mirrored.append([pn[1], pn[0]])
                    n += 1

            points.append(p2)
            mirrored.reverse()

            #add mirrored points
            for i in range(len(mirrored)):
                points.append(mirrored[i])

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

            mirrored = []
            # add remaining points
            while n < self.max_points - 2:
                x = random.randrange(1, self.canvas_side - 2)
                y = random.randrange(1, self.canvas_side - x)
                pn = [x * self.guide_scale, y * self.guide_scale]
                if pn not in points:
                    points.append(pn)
                    mirrored.append([(self.canvas_side - y) * self.guide_scale, (self.canvas_side - x) * self.guide_scale])
                    n += 1

            points.append(p2)
            mirrored.reverse()

            #add mirrored points
            for i in range(len(mirrored)):
                points.append(mirrored[i])

        v = self.points_to_vectors(points)
        a_total = 0  #sum of all angles - used to make sure all angles are not square - too many lines of symmetry
        for i in range(len(v)):
            sl = self.side_len((points[i - 1], points[i]))
            a = self.angle(v[i - 1], v[i])
            a_total += a
            if sl < self.scale - 1 or not -0.99 < a < 0.99:
                invalid_shape = True
                break

        if (self.max_points > 3 and self.intersecting(points)) or -0.2 < a_total < 0.2:
            invalid_shape = True

        if invalid_shape:
            self.recursion_depth += 1
            if self.recursion_depth < 15:
                points = self.pick_random_shape()

        return points

    def draw_random_shape(self):
        # draw shape
        points = self.random_points[:]
        points.append(points[0])
        pygame.draw.polygon(self.canvas, self.active_color, points, 0)

        # redraw outlines
        pygame.draw.polygon(self.canvas, self.border_color, points, 3)
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
            if pos[0] > self.layout.game_margin and pos[1] > self.layout.top_margin:
                if -1 < active < 8 and active != self.canvas_block.unit_id:
                    if active % 2 != 0:
                        a = 1
                    else:
                        a = -1
                    if self.selected[active // 2] == 0:
                        self.selectors[active].change_image(self.selectors[active].img_src_org[0:12] + "a" +
                                                            self.selectors[active].img_src_org[12:])
                        self.selected[active // 2] = 1
                        self.selectors[active - a].change_image(self.selectors[active - a].img_src_org[0:12] + "a" +
                                                                self.selectors[active - a].img_src_org[12:])
                    else:
                        self.selectors[active].change_image(self.selectors[active].img_src_org)
                        self.selectors[active - a].change_image(self.selectors[active - a].img_src_org)
                        self.selected[active // 2] = 0

                    self.draw_multi_axis()
                    self.mainloop.redraw_needed[0] = True

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

    def draw_multi_axis(self):
        self.redraw_task_shape()
        for i in range(4):
            if self.selected[i] == 1:
                self.draw_axis(i)
        self.copy_to_screen()

    def change_points_num(self, n):
        if n == 1 and self.max_points < 10 or n == -1 and self.max_points > 3:
            if self.points_count >= self.max_points - 1 and n == -1:
                n = 0
            self.max_points = self.max_points + n
            self.mainloop.redraw_needed[0] = True

    def change_axis(self, axis):
        self.direction = axis
        self.new_screen()
        self.reset()
        self.mainloop.redraw_needed[0] = True

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

    def check_drawing(self):
        if self.direction < 4:
            self.fill_poli()

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Lines of symmetry - instruction"])

    def auto_check_reset(self):
        self.correct = False
        for each in self.selectors:
            each.set_display_check(None)

    def symmetrical(self, p1, p2):
        #check if all points match
        for each in p1:
            if each not in p2:
                return False
        l = []
        #find indexes in the list of points
        for i in range(len(p1)):
            l.append(p2.index(p1[i]))

        #shift the list - align with 0
        zero = l.index(0)
        l2 = l[zero:] + l[:zero]

        #check if the difference in points' locations is only 1
        for i in range(2, len(l2)):
            if l2[i-1] - l2[i] != 1:
                return False
        return True

    def check_result(self):
        if sum(self.selected) > 0:
            all_ok = True
            for i in range(4):
                p2 = self.get_simetrical_shape(i, self.random_points)

                #check if all points match
                symm = self.symmetrical(p2, self.random_points)

                if (self.selected[i] == 1 and symm) or (self.selected[i] == 0 and not symm):
                    self.selectors[i*2].set_display_check(True)
                    self.selectors[i*2+1].set_display_check(True)
                else:
                    self.selectors[i*2].set_display_check(False)
                    self.selectors[i*2+1].set_display_check(False)
                    all_ok = False
            if all_ok:
                self.level.next_board()

            self.mainloop.redraw_needed[0] = True

    """
    def draw_tmp_shape(self, points):
        # draw shape
        #points = self.random_points[:]
        points.append(points[0])
        pygame.draw.polygon(self.canvas, self.active_color, points, 0)

        # redraw outlines
        pygame.draw.polygon(self.canvas, self.border_color, points, 3)
        self.reset()
        self.copy_to_screen()
    """
