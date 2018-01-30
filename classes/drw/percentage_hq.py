# -*- coding: utf-8 -*-

import pygame
from math import pi, cos, sin

from classes.simple_vector import Vector2


class Percentage:
    def __init__(self, unit_size, scale, color1, color2, border_color1, border_color2, number):
        self.size = unit_size * scale
        self.center = [self.size // 2, self.size // 2]

        self.color1 = color1
        self.color2 = color2
        self.border_color1 = border_color1
        self.border_color2 = border_color2
        self.number = number
        self.type = type

        self.canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)
        self.canvas.fill((0, 0, 0, 0))

        self.draw_circles()

    def get_canvas(self):
        return self.canvas

    def update_values(self, number):
        self.number = number
        self.canvas.fill((0, 0, 0, 0))
        self.draw_circles()

    def draw_circles(self):
        r = self.size // 2 - self.size // 10
        m = (self.size - r * 2) // 2

        angles = (self.number * 3.6, (100 - self.number) * 3.6)
        #angle_start = [int(angles[0]), 0] #int(round((self.number * angle) / 2.0))
        #angle_start = [int(round(angles[0] / 2.0 - angles[0])), int(round(angles[0] / 2.0)) + int(angles[0])]
        angle_start = [int(round(angles[0] / 2.0 - angles[0])) + 1, int(round(angles[0] / 2.0 - angles[0]))+int(angles[0]) + 1]
        #angle_start = [270, 270+int(angles[0])]
        for i in range(2):
            if i == 0:
                col = self.color1
                bd_col = self.border_color1
                offset = self.size // 40
            else:
                col = self.color2
                bd_col = self.border_color2
                offset = self.size // 40

            # Center and radius of pie chart
            cx = m + r
            cy = m + r

            #create vector to push the pieces away from the centre towards middle of the arch
            centre_vect = Vector2().from_points([cx, cy],
                                                [cx + int(round(r * cos(((angles[i] - angles[i] / 2.0) + angle_start[i]) * pi / 180))),
                                                 cy + int(round(r * sin(((angles[i] - angles[i] / 2.0) + angle_start[i]) * pi / 180)))])

            centre_vect.normalize()
            p = [(cx + centre_vect[0] * offset, cy + centre_vect[1] * offset)]
            # Get points on arc
            for n in range(-1 + angle_start[i], angle_start[i] + int(round(angles[i]))):
                x = cx + int(round(r * cos((n) * pi / 180))) + centre_vect[0] * offset
                y = cy + int(round(r * sin((n) * pi / 180))) + centre_vect[1] * offset
                p.append((x, y))
            p.append((cx + centre_vect[0] * offset, cy + centre_vect[1] * offset))

            # Draw pie segment
            if len(p) > 2 and angles[i] > 0:
                    pygame.draw.polygon(self.canvas, col, p)
                    if self.number not in [0, 100]:
                        pygame.draw.polygon(self.canvas, bd_col, p, 2)
                    else:
                        pygame.draw.polygon(self.canvas, bd_col, p[1:-1], 2)

