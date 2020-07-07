# -*- coding: utf-8 -*-

import pygame
from math import pi, cos, sin, fsum


class Ratio:
    def __init__(self, unit_size, scale, color1, color2, color3, border_color1, border_color2, border_color3, numbers,
                 scale_factor=1):
        self.size = unit_size * scale
        self.center = [self.size // 2, self.size // 2]
        self.r = int(self.size // 2.5 * scale_factor)
        self.r2 = int(self.size // 17 * scale_factor)

        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.border_color1 = border_color1
        self.border_color2 = border_color2
        self.border_color3 = border_color3
        self.numbers = numbers
        self.type = type

        self.canvas = pygame.Surface((self.size, self.size - 1), flags=pygame.SRCALPHA)
        self.canvas.fill((0, 0, 0, 0))

        self.draw_minicircles()

    def get_canvas(self):
        return self.canvas

    def update_values(self, numbers):
        self.numbers = numbers
        self.canvas.fill((0, 0, 0, 0))
        self.draw_minicircles()

    def draw_minicircles(self):
        ttl = int(fsum(self.numbers))
        angle_step = 2 * pi / ttl
        angle_start = -pi / 2
        r = self.r #self.size // 2.5
        r2 = self.r2 #size // 17
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
