# -*- coding: utf-8 -*-

import pygame
from math import pi, cos, sin


class Fraction:
    def __init__(self, unit_size, scale, color1, color2, numbers, fract_type):
        self.size = unit_size * scale
        self.center = [self.size // 2, self.size // 2]

        self.color1 = color1
        self.color2 = color2
        self.numbers = numbers

        self.canvas = pygame.Surface([self.size, self.size - 1], flags=pygame.SRCALPHA)
        self.canvas.fill((0, 0, 0, 0))

        self.drawing_f = [self.draw_circles, self.draw_minicircles, self.draw_polygons, self.draw_petals]
        self.drawing_f[fract_type]()

    def get_canvas(self):
        return self.canvas

    def draw_circles(self):
        angle_step = 2 * pi / self.numbers[1]
        angle_start = -pi / 2
        angle_arc_start = -pi / 2
        r = self.size // 2 - self.size // 10
        m = (self.size - r * 2) // 2
        angle = angle_start
        angle_e = angle_arc_start + self.numbers[0] * 2 * pi / self.numbers[1]

        i = 0
        while angle < angle_e:  # maximum of 158 lines per pi
            x = (r - 2) * cos(angle) + self.center[0]
            y = (r - 2) * sin(angle) + self.center[1]
            pygame.draw.line(self.canvas, self.color1, [self.center[0], self.center[1]], [x, y], 3)
            i += 1
            angle = angle_start + 0.02 * (i)

        pygame.draw.ellipse(self.canvas, self.color2, (m, m, self.size - m*2, self.size - m*2), 1)
        #pygame.draw.ellipse(self.canvas, self.color2, (11, 11, self.size - 22, self.size - 22), 1)
        r = r - 1
        for i in range(self.numbers[1]):
            # angle for line
            angle = angle_start + angle_step * i
            # Calculate the x,y for the end point
            x = r * cos(angle) + self.center[0]
            y = r * sin(angle) + self.center[1]

            # Draw the line from the self.center to the calculated end point
            pygame.draw.line(self.canvas, self.color2, [self.center[0], self.center[1]], [x, y], 1)

    def draw_polygons(self):
        half = False
        self.numbers = self.numbers[:]
        if self.numbers[1] == 2:
            self.numbers[1] = 4
            half = True
        angle_step = 2 * pi / self.numbers[1]
        angle_start = -pi / 2
        r = self.size // 2 - self.size // 10
        angle = angle_start

        r = r - 1
        x = r * cos(angle) + self.center[0]
        y = r * sin(angle) + self.center[1]
        prev = [self.center[0], self.center[1]]

        lines = []
        multilines = []
        points = []
        points.append(prev)

        for i in range(self.numbers[1] + 1):
            # angle for line
            angle = angle_start + angle_step * i
            # Calculate the x,y for the end point
            if i > 0:
                x = r * cos(angle) + self.center[0]
            else:
                x = self.center[0]

            y = r * sin(angle) + self.center[1]
            # Draw the line from the self.center to the calculated end point

            if half is False or (half is True and i % 2 == 0):
                multilines.append([[self.center[0], self.center[1]], [x, y]])

            lines.append(prev)
            prev = [x, y]
            if (half is False and i < self.numbers[0] + 1) or (half is True and i < 3):
                points.append(prev)

        points.append(self.center)
        pygame.draw.polygon(self.canvas, self.color1, points, 0)

        lines.append([x, y])
        # pygame.draw.aalines(self.canvas, self.color2, True, lines, True)
        pygame.draw.lines(self.canvas, self.color2, True, lines, 1)
        for each in multilines:
            pygame.draw.line(self.canvas, self.color2, each[0], each[1], 1)

    def draw_minicircles(self):
        angle_step = 2 * pi / self.numbers[1]
        angle_start = -pi / 2
        r = self.size // 3.5
        # manually draw the arc - the 100% width of the arc does not impress

        for i in range(self.numbers[1]):
            # angle for line
            angle = angle_start + angle_step * i

            # Calculate the x,y for the end point
            x = r * cos(angle) + self.center[0]
            y = r * sin(angle) + self.center[1]
            if i < self.numbers[0]:
                pygame.draw.circle(self.canvas, self.color1, [int(x), int(y)], self.size // 7, 0)
            pygame.draw.circle(self.canvas, self.color2, [int(x), int(y)], self.size // 7, 1)
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