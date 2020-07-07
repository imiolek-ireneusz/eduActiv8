# -*- coding: utf-8 -*-

import pygame
from math import pi, cos, sin

from classes.simple_vector import Vector2


class Fraction:
    def __init__(self, unit_size, scale, color1, color2, border_color1, border_color2, numbers, border_width, scale_factor = 1):
        self.size = unit_size * scale
        self.center = [self.size // 2, self.size // 2]
        self.r_base = self.size // 2 - self.size // 10
        self.r = int(self.r_base * scale_factor)

        self.color1 = color1
        self.color2 = color2
        self.border_color1 = border_color1
        self.border_color2 = border_color2
        self.numbers = numbers
        self.border_width = border_width

        self.canvas = pygame.Surface((self.size, self.size - 1), flags=pygame.SRCALPHA)

        self.offset_selected = self.size // 30
        self.offset_unselected = self.size // 60
        self.set_offset(30, 60)

    def set_offset(self, selected, unselected):
        if selected > 0:
            self.offset_selected = self.size // selected
        else:
            self.offset_selected = 0
        if unselected > 0:
            self.offset_unselected = self.size // unselected
        else:
            self.offset_unselected = 0
        self.canvas.fill((0, 0, 0, 0))

        if self.offset_selected == 0:
            self.draw_fraction_no_offset()
        else:
            self.draw_fraction()

    def get_canvas(self):
        return self.canvas

    def update_values(self, numbers):
        self.numbers = numbers
        self.canvas.fill((0, 0, 0, 0))
        if self.offset_selected == 0:
            self.draw_fraction_no_offset()
        else:
            self.draw_fraction()

    def draw_fraction(self):
        r = self.r
        m = (self.size - r * 2) // 2
        if self.numbers == [0, 0]:
            pass
        elif self.numbers == [1, 1]:
            cx = m + r
            cy = m + r
            pygame.draw.circle(self.canvas, self.color1, (cx, cy), r, 0)
            pygame.draw.circle(self.canvas, self.border_color1, (cx, cy), r, 1)
        else:
            if self.numbers[1] < 48:
                step = 5
            else:
                step = 2

            angle = 360.0 / self.numbers[1]
            angle_start_f = (self.numbers[0] * angle) / 2.0
            for i in range(self.numbers[1]):
                if i < self.numbers[0] and self.numbers[0] > 0:
                    col = self.color1
                    bd_col = self.border_color1
                    offset = self.offset_selected
                else:
                    col = self.color2
                    bd_col = self.border_color2
                    offset = self.offset_unselected

                # Center and radius of pie chart
                cx = m + r
                cy = m + r

                #create vector to push the pieces away from the centre towards middle of the arch
                centre_vect = Vector2().from_points([cx, cy],
                                                    [cx + (r * cos(((angle*(i+1) - angle / 2.0) -
                                                                    angle_start_f) * pi / 180.0)),
                                                     cy + (r * sin(((angle*(i+1) - angle / 2.0) -
                                                                    angle_start_f) * pi / 180.0))])

                centre_vect.normalize()
                #first point
                p = [(cx + centre_vect[0] * offset, cy + centre_vect[1] * offset)]

                # Get points on arc
                for n in range(int(round(angle*i)), int(round(angle*(i+1))), step):
                    x = cx + int(round(r * cos((n-angle_start_f) * pi / 180) + centre_vect[0] * offset))
                    y = cy + int(round(r * sin((n-angle_start_f) * pi / 180) + centre_vect[1] * offset))
                    p.append((x, y))

                # final point on arc
                n = angle * (i + 1)
                x = cx + int(round(r * cos((n-angle_start_f) * pi / 180) + centre_vect[0] * offset))
                y = cy + int(round(r * sin((n-angle_start_f) * pi / 180) + centre_vect[1] * offset))
                p.append((x, y))

                # last point - same as the first one
                p.append((cx + centre_vect[0] * offset, cy + centre_vect[1] * offset))

                # Draw pie segment
                if len(p) > 2:
                    pygame.draw.polygon(self.canvas, col, p)
                    pygame.draw.polygon(self.canvas, bd_col, p, self.border_width)

    def draw_fraction_no_offset(self):
        if self.numbers[1] != 0:
            a = 360.0 * self.numbers[0] / self.numbers[1]
            nums = [a, 360 - a]
            cols = [self.color1, self.color2]
            bd_cols = [self.border_color1, self.border_color2]

            self.draw_background(nums, cols, bd_cols)
            self.draw_lines()

    def draw_lines(self):
        r = self.size // 2 - self.size // 10
        m = (self.size - r * 2) // 2

        angle = 360.0 / self.numbers[1]
        angle_start_f = (self.numbers[0] * angle) / 2.0

        for i in range(self.numbers[1]):
            if i < self.numbers[0]:
                bd_col = self.border_color1
            else:
                bd_col = self.border_color2

            # Center and radius of pie chart
            cx = m + r
            cy = m + r

            #first point
            p = [(cx, cy)]

            # second point (on arc)
            n = angle * (i + 1)
            x = cx + int(round(r * cos((n-angle_start_f) * pi / 180)))
            y = cy + int(round(r * sin((n-angle_start_f) * pi / 180)))
            p.append((x, y))

            if i < self.numbers[1]-1:
                pygame.draw.line(self.canvas, bd_col, p[0], p[1], 2)

            if i == self.numbers[1]-1 or i == self.numbers[0]-1:
                pygame.draw.line(self.canvas, self.border_color1, p[0], p[1], 3)


    def draw_background(self, num, cols, bd_cols):
        r = self.size // 2 - self.size // 10
        m = (self.size - r * 2) // 2
        angles = []
        angle_start_float = []

        for i in range(len(num)):
            angles.append(num[i])
            if i == 0:
                angle_start_float.append(360-num[0] / 2.0)
            else:
                angle_start_float.append(angle_start_float[-1] + angles[i - 1])

        for i in range(len(num)):
            if i == 0:
                w = 3
            else:
                w = 2

            # Center and radius of pie chart
            cx = m + r
            cy = m + r

            # first point
            p = [(cx, cy)]

            # Get points on arc
            for n in range(int(round(angle_start_float[i])), int(round(angle_start_float[i] + angles[i])), 3):
                x = cx + int(round(r * cos(n * pi / 180)))
                y = cy + int(round(r * sin(n * pi / 180)))
                p.append((x, y))

            # final point on arc
            n = int(round(angle_start_float[i] + angles[i]))
            x = cx + int(round(r * cos(n * pi / 180)))
            y = cy + int(round(r * sin(n * pi / 180)))
            p.append((x, y))

            # last point
            p.append((cx, cy))

            # Draw pie segment
            if len(p) > 2 and angles[i] > 0:
                pygame.draw.polygon(self.canvas, cols[i], p)
                pygame.draw.lines(self.canvas, bd_cols[i], False,  p[1:-1], w)
