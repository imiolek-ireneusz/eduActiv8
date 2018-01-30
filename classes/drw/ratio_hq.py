# -*- coding: utf-8 -*-

import pygame
from math import pi, cos, sin, fsum

from classes.simple_vector import Vector2


class Ratio:
    def __init__(self, unit_size, scale, color1, color2, color3, border_color1, border_color2, border_color3, numbers):
        self.size = unit_size * scale
        self.center = [self.size // 2, self.size // 2]

        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.border_color1 = border_color1
        self.border_color2 = border_color2
        self.border_color3 = border_color3
        self.numbers = numbers
        self.type = type

        self.canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)
        self.canvas.fill((0, 0, 0, 0))

        self.draw_minicircles()

    def get_canvas(self):
        return self.canvas

    def update_values(self, numbers):
        self.numbers = numbers
        self.canvas.fill((0, 0, 0, 0))
        self.draw_minicircles()


    def draw_circles(self):
        r = self.size // 2 - self.size // 10
        m = (self.size - r * 2) // 2

        angle = 360.0 / self.numbers[1]
        angle_start = int(round((self.numbers[0] * angle) / 2.0))
        for i in range(self.numbers[1]):
            if i < self.numbers[0]:
                col = self.color1
                bd_col = self.border_color1
                offset = self.size // (40 - self.numbers[1] * 2)
            else:
                col = self.color2
                bd_col = self.border_color2
                offset = self.size // (80 - self.numbers[1] * 2)

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
                pygame.draw.polygon(self.canvas, bd_col, p, 2)

    def draw_minicircles(self):
        ttl = int(fsum(self.numbers))
        angle_step = 2 * pi / ttl
        angle_start = -pi / 2
        r = self.size // 2.5
        r2 = self.size // 17
        # manually draw the arc - the 100% width of the arc does not impress

        for i in range(ttl):
            # angle for line
            angle = angle_start + angle_step * i

            # Calculate the x,y for the end point
            x = r * cos(angle) + self.center[0]
            y = r * sin(angle) + self.center[1]
            if i < self.numbers[0]:
                pygame.draw.circle(self.canvas, self.color1, [int(x), int(y)], r2, 0)
                pygame.draw.circle(self.canvas, self.border_color1, [int(x), int(y)], r2, 2)
            elif i < self.numbers[0] + self.numbers[1]:
                pygame.draw.circle(self.canvas, self.color2, [int(x), int(y)], r2, 0)
                pygame.draw.circle(self.canvas, self.border_color2, [int(x), int(y)], r2, 2)
            else:
                pygame.draw.circle(self.canvas, self.color3, [int(x), int(y)], r2, 0)
                pygame.draw.circle(self.canvas, self.border_color3, [int(x), int(y)], r2, 2)
            # Draw the line from the self.center to the calculated end point

    def draw_petals(self):
        angle_step = 2 * pi / self.numbers[1]
        angle_start = -pi / 2
        r = self.size // 3 + self.size // 10

        multilines = []
        for i in range(self.numbers[1]):
            # angle for line
            angle = angle_start + angle_step * i

            # Calculate the x,y for the end point
            x = r * cos(angle) + self.center[0]
            y = r * sin(angle) + self.center[1]

            x2 = (r - self.size // 10) * cos(angle - 0.3) + self.center[0]
            y2 = (r - self.size // 10) * sin(angle - 0.3) + self.center[1]

            x3 = (r - self.size // 10) * cos(angle + 0.3) + self.center[0]
            y3 = (r - self.size // 10) * sin(angle + 0.3) + self.center[1]

            points = [self.center, [x2, y2], [x, y], [x3, y3]]

            if i < self.numbers[0]:
                pygame.draw.polygon(self.canvas, self.color1, points, 0)
            # Draw the line from the self.center to the calculated end point
            multilines.extend(points)
        pygame.draw.lines(self.canvas, self.color2, True, multilines, 1)