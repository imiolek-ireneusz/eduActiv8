# -*- coding: utf-8 -*-

import pygame
from math import pi, cos, sin

from classes.simple_vector import Vector2


class Fraction:
    def __init__(self, unit_size, scale, color1, color2, border_color1, border_color2, numbers, border_width):
        self.size = unit_size * scale
        self.center = [self.size // 2, self.size // 2]

        self.color1 = color1
        self.color2 = color2
        self.border_color1 = border_color1
        self.border_color2 = border_color2
        self.numbers = numbers
        self.border_width = border_width


        self.canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)


        self.offset_selected = self.size // 30
        self.offset_unselected = self.size // 60
        self.set_offset(30, 60)

    def set_offset(self, selected, unselected):
        if selected > 0:
            self.offset_selected = self.size // selected
        else:
            self.offset_selected = 2
        if unselected > 0:
            self.offset_unselected = self.size // unselected
        else:
            self.offset_unselected = 2
        self.canvas.fill((0, 0, 0, 0))
        self.draw_circles()

    def get_canvas(self):
        return self.canvas

    def update_values(self, numbers):
        self.numbers = numbers
        self.canvas.fill((0, 0, 0, 0))
        self.draw_circles()


    def draw_circles(self):
        if self.numbers == [0, 0]:
            pass
        elif self.numbers == [1, 1]:
            #draw circle
            r = self.size // 2 - self.size // 10
            m = (self.size - r * 2) // 2
            cx = m + r
            cy = m + r
            #circle(Surface, color, pos, radius, width=0) -> Rect
            pygame.draw.circle(self.canvas, self.color1, (cx, cy), r, 0)
            pygame.draw.circle(self.canvas, self.border_color1, (cx, cy), r, 1)
        else:
            r = self.size // 2 - self.size // 10
            m = (self.size - r * 2) // 2

            angle = 360.0 / self.numbers[1]
            angle_start = int(round((self.numbers[0] * angle) / 2.0)) - 1
            for i in range(self.numbers[1]):
                if i < self.numbers[0]:
                    col = self.color1
                    bd_col = self.border_color1
                    #offset = self.size // (40 - self.numbers[1] * 2)
                    offset = self.offset_selected
                else:
                    col = self.color2
                    bd_col = self.border_color2
                    offset = self.offset_unselected
                    #offset = self.size // (80 - self.numbers[1] * 2)

                # Center and radius of pie chart
                cx = m + r
                cy = m + r

                #create vector to push the pieces away from the centre towards middle of the arch
                centre_vect = Vector2().from_points([cx, cy],
                                                    [cx + int(round(r * cos(((angle*(i+1) - angle / 2.0) - angle_start) * pi / 180))),
                                                     cy + int(round(r * sin(((angle*(i+1) - angle / 2.0) - angle_start) * pi / 180)))])

                centre_vect.normalize()
                p = [(cx + centre_vect[0] * offset, cy + centre_vect[1] * offset)]
                # Get points on arc
                for n in range(int(round(-1 + angle*i)), int(round(angle*(i+1)))):
                    x = cx + int(round(r * cos((n-angle_start) * pi / 180))) + centre_vect[0] * offset
                    y = cy + int(round(r * sin((n-angle_start) * pi / 180))) + centre_vect[1] * offset
                    p.append((x, y))
                p.append((cx + centre_vect[0] * offset, cy + centre_vect[1] * offset))

                # Draw pie segment
                if len(p) > 2:
                    pygame.draw.polygon(self.canvas, col, p)
                    pygame.draw.polygon(self.canvas, bd_col, p, self.border_width)
