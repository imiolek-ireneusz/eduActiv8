# -*- coding: utf-8 -*-

import pygame

from math import pi, cos, acos, sin, sqrt
import classes.simple_vector as sv
import classes.extras as ex


class Clock:
    def __init__(self, game_board, wrapper, size, time, prefs):
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

        self.colors = [color1, color2]
        self.colors2 = [color3, color4]
        self.colors3 = [color5, color6]
        self.colors4 = [color7, color8]

        self.hand_coords = [[], []]
        self.size = size
        self.time = time
        self.center = [self.size // 2, self.size // 2]

        self.clock_wrapper = wrapper  # self.board.ships[-1]
        self.clock_wrapper.font = game_board.clock_fonts[0]
        self.clock_wrapper.font2 = game_board.clock_fonts[1]
        self.clock_wrapper.font3 = game_board.clock_fonts[2]

        self.canvas = pygame.Surface([self.size, self.size - 1])
        if self.game_board.mainloop.scheme is not None:
            self.canvas.fill(self.game_board.mainloop.scheme.u_color)
        else:
            self.canvas.fill((255, 255, 255))
        self.hands_vars()
        self.draw_hands()

        self.clock_wrapper.hidden_value = [2, 3]
        self.clock_wrapper.font_color = color2
        self.clock_wrapper.painting = self.canvas.copy()

    def hands_vars(self):
        numbers = [2, 2]
        self.angle_step_12 = 2 * pi / 12
        self.angle_step_60 = 2 * pi / 60

        self.angle_start = -pi / 2
        angle_arc_start = -pi / 2
        self.r = self.size // 3 + self.size // 10

        self.rs = [int(90 * self.size / 500.0), int(170 * self.size / 500.0), int(110 * self.size / 500.0)]

    def draw_hands(self):
        if self.show_hour_offset:
            a1 = self.angle_start + (2 * pi / 12) * self.time[0] + (self.angle_step_12 * (2 * pi / 60) * self.time[
                1]) / (2 * pi)
        else:
            a1 = self.angle_start + (2 * pi / 12) * self.time[0]
        a2 = self.angle_start + (2 * pi / 60) * self.time[1]
        self.angles = [a1, a2]

        rs = self.rs
        time = self.time

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
                    if not self.show_highlight or (i + 1 == time[1] or (time[1] == 0 and i == 59)):
                        text = self.clock_wrapper.font3.render("%s" % (val), 1, self.colors2[1])
                    else:
                        text = self.clock_wrapper.font3.render("%s" % (val), 1, self.colors[1])
                    offset3 = rs[1] + 10 + 15 * self.size / 500.0 + font_size[1] // 2
                    x3 = offset3 * cos(a) + self.center[0] - int(font_size[0] / 2.0)
                    y3 = offset3 * sin(a) + self.center[1] - int(font_size[1] / 2.0)

                    self.canvas.blit(text, (x3, y3))
                    if self.show_only_quarters_m or self.show_only_fives_m:
                        if (i + 1) % 15 == 0:
                            marklen = 10 + 15 * self.size / 500.0
                        elif (i + 1) % 5 == 0:
                            marklen = 10 + 10 * self.size / 500.0
                        else:
                            marklen = 10 + 5 * self.size / 500.0
                    else:
                        marklen = 10 + 10 * self.size / 500.0
                else:
                    if (i + 1) % 15 == 0:
                        marklen = 10 + 15 * self.size / 500.0
                    elif (i + 1) % 5 == 0:
                        marklen = 10 + 10 * self.size / 500.0
                    else:
                        marklen = 10 + 5 * self.size / 500.0
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
            if self.show_roman:
                val = self.hour_to_roman(val)
            if not self.show_highlight or i + 1 == time[0]:
                text = self.clock_wrapper.font.render("%s" % (val), 1, self.colors2[0])
            else:
                text = self.clock_wrapper.font.render("%s" % (val), 1, self.colors[0])
            if self.show_roman:
                text_angle = -(360 / 12.0) * (i + 1)
                text = pygame.transform.rotate(text, text_angle)
                rect = text.get_rect()
                x3 = (rs[2] + 10 + 7 * self.size / 500.0 + font_size[1] // 2) * cos(a) + self.center[0] - rect.width / 2
                y3 = (rs[2] + 10 + 7 * self.size / 500.0 + font_size[1] // 2) * sin(a) + self.center[
                    1] - rect.height / 2

            else:
                x3 = (rs[2] + 10 + 7 * self.size / 500.0 + font_size[1] / 2) * cos(a) + self.center[0] - font_size[
                                                                                                             0] / 2
                y3 = (rs[2] + 10 + 7 * self.size / 500.0 + font_size[1] / 2) * sin(a) + self.center[1] - font_size[
                                                                                                             1] / 2
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
        hand_width = [self.r // 14, self.r // 18]
        start_offset = [self.size // 10, self.size // 12]

        for i in range(2):
            # angle for line
            angle = self.angles[i]  # angle_start + angle_step*i

            x0 = self.center[0] - start_offset[i] * cos(angle)
            y0 = self.center[1] - start_offset[i] * sin(angle)

            # Calculate the x,y for the end point
            x1 = rs[i] * cos(angle) + self.center[0]
            y1 = rs[i] * sin(angle) + self.center[1]
            x2 = hand_width[i] * cos(angle - pi / 2) + self.center[0]
            y2 = hand_width[i] * sin(angle - pi / 2) + self.center[1]

            x3 = hand_width[i] * cos(angle + pi / 2) + self.center[0]
            y3 = hand_width[i] * sin(angle + pi / 2) + self.center[1]

            points = [[x0, y0], [x2, y2], [x1, y1], [x3, y3]]
            shadow = [[x0, y0], [x2, y2], [x1, y1]]
            self.hand_coords[i] = points
            pygame.draw.polygon(self.canvas, self.colors[i], points, 0)
            pygame.draw.polygon(self.canvas, self.colors3[i], shadow, 0)
            # Draw the line from the center to the calculated end point
            line_through = [[x0, y0], [x1, y1]]

            pygame.draw.aalines(self.canvas, self.colors2[i], True, points)
            pygame.draw.aalines(self.canvas, self.colors2[i], True, line_through)
        pygame.draw.circle(self.canvas, self.colors[0], self.center, self.size // 50, 0)
        pygame.draw.circle(self.canvas, self.colors2[0], self.center, self.size // 50, 1)
        pygame.draw.circle(self.canvas, self.colors2[0], self.center, self.size // 70, 1)
        self.clock_wrapper.update_me = True

    def hour_to_roman(self, val):
        val = int(val)
        return self.roman[val - 1]

    def vector_len(self, v):
        return sqrt(v[0] ** 2 + v[1] ** 2)

    def scalar_product(self, v1, v2):
        return sum([v1[i] * v2[i] for i in range(len(v1))])

    def angle(self, v1, v2):
        return self.scalar_product(v1, v2) / (self.vector_len(v1) * self.vector_len(v2))

    def is_contained(self, pos, coords_id=0):
        v0 = sv.Vector2.from_points(self.hand_coords[coords_id][2], self.hand_coords[coords_id][1])
        v1 = sv.Vector2.from_points(self.hand_coords[coords_id][0], self.hand_coords[coords_id][1])

        v2 = sv.Vector2.from_points(self.hand_coords[coords_id][2], self.hand_coords[coords_id][3])
        v3 = sv.Vector2.from_points(self.hand_coords[coords_id][0], self.hand_coords[coords_id][3])

        v4 = sv.Vector2.from_points(pos, self.hand_coords[coords_id][1])
        v5 = sv.Vector2.from_points(pos, self.hand_coords[coords_id][3])

        a1 = 1 - self.angle(v0, v1)  # corner 1
        a2 = 1 - self.angle(v2, v3)  # corner 2

        a3 = 1 - self.angle(v0, v4)  # point to arm1 of corner1
        a4 = 1 - self.angle(v1, v4)  # point to arm2 of corner1

        a5 = 1 - self.angle(v2, v5)  # point to arm1 of corner2
        a6 = 1 - self.angle(v3, v5)  # point to arm2 of corner2

        if (a3 + a4) < a1 and (a5 + a6) < a2:
            return True
        return False

    def current_angle(self, pos, r):

        cosa = (pos[0] - self.center[0]) / r
        sina = (pos[1] - self.center[1]) / r

        if 0 <= cosa <= 1 and -1 <= sina <= 0:
            angle = pi / 2 - acos(cosa)
        elif 0 <= cosa <= 1 and 0 <= sina <= 1:
            angle = acos(cosa) + pi / 2  # ok

        elif -1 <= cosa <= 0 and 0 <= sina <= 1:
            angle = acos(cosa) + pi / 2  # ok
        elif -1 <= cosa <= 0 and -1 <= sina <= 0:
            angle = 2 * pi + pi / 2 - acos(cosa)
        return angle