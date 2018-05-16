# -*- coding: utf-8 -*-

import pygame
import copy

from math import pi, cos, sin

import classes.extras as ex


class Clock:
    def __init__(self, game_board, wrapper, size, times, prefs):
        self.game_board = game_board
        self.show_outer_ring = prefs[0]
        self.show_minutes = prefs[1]
        self.show_24h = prefs[2]
        self.show_only_quarters_h = prefs[3]
        self.show_only_quarters_m = prefs[4]
        self.show_only_fives_m = prefs[5]
        self.show_roman = prefs[6]
        self.show_highlight = prefs[7]
        self.show_hour_offset = prefs[8]
        self.show_result = prefs[9]

        self.roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

        if self.game_board.mainloop.scheme is not None:
            color1 = self.game_board.mainloop.scheme.color1  # bright side of short hand
            color3 = self.game_board.mainloop.scheme.color3  # inner font color
            color5 = self.game_board.mainloop.scheme.color5  # dark side of short hand
            color7 = self.game_board.mainloop.scheme.color7  # inner circle filling

            color2 = self.game_board.mainloop.scheme.color2  # bright side of long hand
            color4 = self.game_board.mainloop.scheme.color4  # ex.hsv_to_rgb(170,255,255)#outer font color
            color6 = self.game_board.mainloop.scheme.color6  # dark side of long hand
            color8 = self.game_board.mainloop.scheme.color8  # outer circle filling
        else:
            color1 = ex.hsv_to_rgb(225, 70, 230)
            color3 = ex.hsv_to_rgb(225, 255, 255)
            color5 = ex.hsv_to_rgb(225, 180, 240)
            color7 = ex.hsv_to_rgb(225, 10, 255)

            color2 = ex.hsv_to_rgb(170, 70, 230)
            color4 = ex.hsv_to_rgb(170, 255, 255)
            color6 = ex.hsv_to_rgb(170, 180, 240)
            color8 = ex.hsv_to_rgb(170, 10, 255)

        self.diff_h_col = ex.hsv_to_rgb(225, 150, 200)
        self.diff_hr_col = ex.hsv_to_rgb(225, 100, 210)
        self.diff_m_col = ex.hsv_to_rgb(170, 150, 200)
        self.diff_h_bcol = ex.hsv_to_rgb(225, 150, 170)
        self.diff_m_bcol = ex.hsv_to_rgb(170, 150, 170)
        self.white = (255, 255, 255)

        #diff colours
        self.colors = [color1, color2]
        self.colors2 = [color3, color4]
        self.colors3 = [color5, color6]
        self.colors4 = [color7, color8]

        self.hand_coords = [[], []]
        self.size = size
        self.times = times
        self.center = [self.size // 2, self.size // 2]

        self.clock_wrapper = wrapper  # self.board.ships[-1]
        self.clock_wrapper.font = game_board.clock_fonts[0]
        self.clock_wrapper.font2 = game_board.clock_fonts[1]
        self.clock_wrapper.font3 = game_board.clock_fonts[2]
        self.clock_wrapper.hidden_value = [2, 3]
        self.clock_wrapper.font_color = color2

        self.draw_all(times)

    def draw_all(self, times):
        self.times = times
        self.diff_solution = self.get_diff()
        self.canvas = pygame.Surface([self.size, self.size - 1])
        if self.game_board.mainloop.scheme is not None:
            self.canvas.fill(self.game_board.mainloop.scheme.u_color)
        else:
            self.canvas.fill((255, 255, 255))
        self.hands_vars()
        self.draw_clock()
        self.clock_wrapper.painting = self.canvas.copy()

    def get_diff(self):
        t = copy.deepcopy(self.times)

        # calculate minutes
        if t[1][1] >= t[0][1]:
            m = t[1][1] - t[0][1]
        else:
            m = 60 + t[1][1] - t[0][1]
            t[1][0] -= 1

        # calculate hours
        if t[1][0] >= t[0][0]:
            h = t[1][0] - t[0][0]
        else:
            if self.show_24h:
                h = 24 + t[1][0] - t[0][0]
            else:
                h = 12 + t[1][0] - t[0][0]
        return [h, m]

    def hands_vars(self):
        self.angle_step_12 = 2 * pi / 12
        self.angle_step_60 = 2 * pi / 60
        self.angle_start = -pi / 2
        self.r = self.size // 3 + self.size // 10
        self.rs = [int(70 * self.size / 500.0), int(180 * self.size / 500.0), int(110 * self.size / 500.0)]

    def draw_clock(self):
        time = self.times[0]
        if self.show_hour_offset:
            a1 = self.angle_start + (2 * pi / 12) * time[0] + (self.angle_step_12 * (2 * pi / 60) * time[1]) / (2 * pi)
        else:
            a1 = self.angle_start + (2 * pi / 12) * time[0]
        a2 = self.angle_start + (2 * pi / 60) * time[1]
        self.angles = [a1, a2]
        rs = self.rs

        if self.show_outer_ring:
            pygame.draw.circle(self.canvas, self.colors4[1], self.center, int(rs[1] + 10), 0)
            pygame.draw.circle(self.canvas, self.colors2[1], self.center, int(rs[1] + 10), 1)

        pygame.draw.circle(self.canvas, self.colors4[0], self.center, int(rs[2] + 10), 0)
        pygame.draw.circle(self.canvas, self.colors2[0], self.center, int(rs[2] + 10), 1)

        if self.show_outer_ring:
            for i in range(60):
                val = str(i + 1)
                if self.show_only_quarters_m:
                    if (i + 1) % 15 != 0:
                        val = ""
                elif self.show_only_fives_m:
                    if (i + 1) % 5 != 0:
                        val = ""
                if i == 59:
                    val = "0"
                a = self.angle_start + self.angle_step_60 * (i + 1)
                if self.show_minutes:
                    font_size = self.clock_wrapper.font3.size(val)
                    text = self.clock_wrapper.font3.render("%s" % (val), 1, self.colors2[1])
                    offset3 = rs[1] + 15 + 15 * self.size / 500.0 + font_size[1] // 2
                    x3 = offset3 * cos(a) + self.center[0] - int(font_size[0] / 2.0)
                    y3 = offset3 * sin(a) + self.center[1] - int(font_size[1] / 2.0)

                    self.canvas.blit(text, (x3, y3))
                    if self.show_only_quarters_m or self.show_only_fives_m:
                        if (i + 1) % 15 == 0:
                            marklen = 10 + 20 * self.size / 500.0
                        elif (i + 1) % 5 == 0:
                            marklen = 10 + 15 * self.size / 500.0
                        else:
                            marklen = 10 + 10 * self.size / 500.0
                    else:
                        marklen = 10 + 10 * self.size / 500.0
                else:
                    if (i + 1) % 15 == 0:
                        marklen = 10 + 20 * self.size / 500.0
                    elif (i + 1) % 5 == 0:
                        marklen = 10 + 15 * self.size / 500.0
                    else:
                        marklen = 10 + 10 * self.size / 500.0
                if self.show_outer_ring:
                    x1 = (rs[1] + 10) * cos(a) + self.center[0]
                    y1 = (rs[1] + 10) * sin(a) + self.center[1]

                    x2 = (rs[1] + marklen) * cos(a) + self.center[0]
                    y2 = (rs[1] + marklen) * sin(a) + self.center[1]

                    pygame.draw.aaline(self.canvas, self.colors2[1], [x1, y1], [x2, y2])

        for i in range(12):
            val = str(i + 1)
            if self.show_only_quarters_h:
                if (i + 1) % 3 != 0:
                    val = ""

            a = self.angle_start + self.angle_step_12 * (i + 1)
            x1 = (rs[2] + 10) * cos(a) + self.center[0]
            y1 = (rs[2] + 10) * sin(a) + self.center[1]

            x2 = (rs[2] + 10 + 10 * self.size / 500.0) * cos(a) + self.center[0]
            y2 = (rs[2] + 10 + 10 * self.size / 500.0) * sin(a) + self.center[1]

            pygame.draw.aaline(self.canvas, self.colors2[0], [x1, y1], [x2, y2])

            font_size = self.clock_wrapper.font.size(val)
            text = self.clock_wrapper.font.render("%s" % (val), 1, self.colors2[0])

            x3 = (rs[2] + 15 + 7 * self.size / 500.0 + font_size[1] / 2) * cos(a) + self.center[0] - font_size[0] / 2
            y3 = (rs[2] + 15 + 7 * self.size / 500.0 + font_size[1] / 2) * sin(a) + self.center[1] - font_size[1] / 2
            self.canvas.blit(text, (x3, y3))

            if self.show_24h:
                if i + 13 == 24:
                    val = "0"
                    v = 0
                else:
                    val = str(i + 13)
                    v = i + 13
                font_size = self.clock_wrapper.font2.size(val)
                if not self.show_highlight or v == time[0]:
                    text = self.clock_wrapper.font2.render("%s" % (val), 1, self.colors2[0])
                else:
                    text = self.clock_wrapper.font2.render("%s" % (val), 1, self.colors[0])

                x3 = (rs[0] + font_size[1] // 2) * cos(a) + self.center[0] - font_size[0] / 2
                y3 = (rs[0] + font_size[1] // 2) * sin(a) + self.center[1] - font_size[1] / 2
                self.canvas.blit(text, (x3, y3))

        if self.show_result:
            # draw difference solution
            val = "%s h" % self.diff_solution[0]
            font_size = self.clock_wrapper.font2.size(val)
            text = self.clock_wrapper.font2.render(val, 1, self.colors2[0])
            x = self.center[0] - font_size[0] // 2
            y = self.center[1] - font_size[1] * 1.2
            self.canvas.blit(text, (x, y))

            val = "%s m" % self.diff_solution[1]
            font_size = self.clock_wrapper.font2.size(val)
            text = self.clock_wrapper.font2.render(val, 1, self.colors2[1])
            x = self.center[0] - font_size[0] // 2
            y = self.center[1] + font_size[1] * 0.2
            self.canvas.blit(text, (x, y))


        self.draw_minute_diff()
        self.draw_hour_diff()

        self.clock_wrapper.update_me = True

    def draw_hour_diff(self):
        if self.times[0] != self.times[1]:
            r = self.rs[2] + 10
            r2 = r * 0.75
            m = (self.size - r * 2) // 2
            cx = m + r
            cy = m + r

            if self.times[0][0] != self.times[1][0]:
                if self.times[1][0] < self.times[0][0]:
                    dist = self.times[1][0] + 12 - self.times[0][0]
                else:
                    dist = self.times[1][0] - self.times[0][0]
            else:
                if self.times[1][1] < self.times[0][1]:
                    dist = 12
                else:
                    dist = 1

            # get angle of first hour
            a = (self.times[0][0] * 360 / 12.0 + self.times[0][1] * 0.5 - 90 + 360) % 360

            #get angle of the second hour
            b = (self.times[1][0] * 360 / 12.0 + self.times[1][1] * 0.5 - 90 + 360) % 360
            if a > b:
                b += 360

            # get points on circle at the above angles
            p = []
            p2 = []

            # add points along the ring
            for n in range(int(a), int(b)+1):
                x = cx + int(round(r * cos(n * pi / 180)))
                y = cy + int(round(r * sin(n * pi / 180)))
                p.append((x, y))

                x = cx + int(round(r2 * cos(n * pi / 180)))
                y = cy + int(round(r2 * sin(n * pi / 180)))
                p2.append((x, y))

            # add reversed points on the inner ring
            p.extend(reversed(p2))

            # finish off - close off the polygon
            p.append(p[0])

            pygame.draw.polygon(self.canvas, self.diff_h_col, p, 0)
            pygame.draw.polygon(self.canvas, self.diff_h_bcol, p, 2)

            # recolour the remainder of last hour
            if self.times[0][1] != self.times[1][1]:
                a2 = (self.times[0][0] * 360 / 12.0 + self.times[0][1] * 0.5 - 90 + 360) % 360 + 30 * dist
                if a2 > b:
                    a2 = (self.times[0][0] * 360 / 12.0 + self.times[0][1] * 0.5 - 90 + 360) % 360 + 30 * (dist - 1)
                p = []
                p2 = []

                # add points along the ring
                for n in range(int(a2), int(b) + 1):
                    x = cx + int(round(r * cos(n * pi / 180)))
                    y = cy + int(round(r * sin(n * pi / 180)))
                    p.append((x, y))

                    x = cx + int(round(r2 * cos(n * pi / 180)))
                    y = cy + int(round(r2 * sin(n * pi / 180)))
                    p2.append((x, y))

                # add reversed points on the inner ring
                p.extend(reversed(p2))

                # finish off - close off the polygon
                if len(p) > 0:
                    p.append(p[0])

                    pygame.draw.polygon(self.canvas, self.diff_hr_col, p, 0)
                    pygame.draw.polygon(self.canvas, self.diff_h_bcol, p, 2)

            # draw lines separating hours on difference arc
            if b - a > 30:
                for n in range(int(a)+30, int(b), 30):
                    x = cx + int(round(r * cos(n * pi / 180)))
                    y = cy + int(round(r * sin(n * pi / 180)))
                    pt1 = (x, y)

                    x = cx + int(round(r2 * cos(n * pi / 180)))
                    y = cy + int(round(r2 * sin(n * pi / 180)))
                    pt2 = (x, y)
                    pygame.draw.aaline(self.canvas, self.white, pt1, pt2)

    def draw_minute_diff(self):
        if self.times[0][1] != self.times[1][1]:
            r = self.rs[1] + 10
            r2 = r * 0.85
            m = (self.size - r * 2) // 2
            cx = m + r
            cy = m + r

            # get angle of first minute
            a = (self.times[0][1] * 360 / 60.0 - 90 + 360) % 360

            #get angle of the second minute
            b = (self.times[1][1] * 360 / 60.0 - 90 + 360) % 360
            if a > b:
                b += 360

            # get points on circle at the above angles
            p = []
            p2 = []

            # add points along the ring
            for n in range(int(a), int(b)+1):
                x = cx + int(round(r * cos(n * pi / 180)))
                y = cy + int(round(r * sin(n * pi / 180)))
                p.append((x, y))

                x = cx + int(round(r2 * cos(n * pi / 180)))
                y = cy + int(round(r2 * sin(n * pi / 180)))
                p2.append((x, y))

            # add reversed points on the inner ring
            p.extend(reversed(p2))

            # finish off - close off the polygon
            p.append(p[0])

            pygame.draw.polygon(self.canvas, self.diff_m_col, p, 0)
            pygame.draw.polygon(self.canvas, self.diff_m_bcol, p, 2)
