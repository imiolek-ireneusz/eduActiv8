# -*- coding: utf-8 -*-

import pygame
from math import pi, cos, sin

from classes.simple_vector import Vector2


class Percentage:
    def __init__(self, unit_size, scale, colors, b_colors, numbers):
        self.size = unit_size * scale
        self.center = [self.size // 2, self.size // 2]
        self.numbers = numbers
        self.type = type

        self.canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)
        self.set_colors(colors, b_colors)
        self.redraw()

    def get_canvas(self):
        return self.canvas

    def set_colors(self, colors, b_colors):
        self.colors = colors
        self.b_colors = b_colors

    def redraw(self):
        self.canvas.fill((0, 0, 0, 0))
        self.draw_circles()

    def update_values(self, numbers):
        self.numbers = numbers
        self.canvas.fill((0, 0, 0, 0))
        self.draw_circles()

    def draw_circles(self):
        r = self.size // 2 - self.size // 10
        m = (self.size - r * 2) // 2
        angles = []
        angle_start = []
        angle_start_float = []
        for i in range(len(self.numbers)):
            angles.append(self.numbers[i] * 3.6)
            if i == 0:
                angle_start.append(0)
                angle_start_float.append(0)
            else:
                angle_start.append(int(angle_start_float[-1] - angles[i]))
                angle_start_float.append(angle_start_float[-1] - angles[i])

        for i in range(len(self.numbers)):
            offset = 0

            # Center and radius of pie chart
            cx = m + r
            cy = m + r

            #create vector to push the pieces away from the centre towards middle of the arch
            centre_vect = Vector2().from_points([cx, cy],
                                                [cx + int(round(r * cos(((angles[i] - angles[i] / 2.0) + angle_start_float[i]) * pi / 180))),
                                                 cy + int(round(r * sin(((angles[i] - angles[i] / 2.0) + angle_start_float[i]) * pi / 180)))])

            centre_vect.normalize()
            p = [(cx + centre_vect[0] * offset, cy + centre_vect[1] * offset)]

            # Get points on arc
            for n in range(-1 + angle_start[i], 1 + int(round(angle_start_float[i] + angles[i]))):
                x = cx + int(round(r * cos((n) * pi / 180))) + centre_vect[0] * offset
                y = cy + int(round(r * sin((n) * pi / 180))) + centre_vect[1] * offset
                p.append((x, y))
            p.append((cx + centre_vect[0] * offset, cy + centre_vect[1] * offset))

            # Draw pie segment
            if len(p) > 2 and angles[i] > 0:
                    pygame.draw.polygon(self.canvas, self.colors[i], p)

                    if self.numbers[i] not in [0, 100]:
                        pygame.draw.polygon(self.canvas, self.b_colors[i], p, 2)
                    else:
                        pygame.draw.polygon(self.canvas, self.b_colors[i], p[1:-1], 2)
