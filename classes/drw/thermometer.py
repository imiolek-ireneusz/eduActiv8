# -*- coding: utf-8 -*-

import pygame
from math import pi


class Thermometer:
    def __init__(self, game_board, width, height, scale, color, border_color, rng, number, lbl_dist=5):
        self.size = [width * scale, height * scale]
        self.center = [self.size[0] // 2, self.size[1] // 2]
        self.game_board = game_board
        self.color = color
        self.border_color = border_color
        self.number = number
        self.lbl_dist = lbl_dist
        self.rng = rng
        self.v_margin = int(80 * self.size[0] / 500.0)
        self.marker_len10 = int(20 * self.size[0] / 150.0)
        self.marker_len5 = int(15 * self.size[0] / 150.0)
        self.marker_len = int(10 * self.size[0] / 150.0)
        self.bar_width = int(25 * self.size[0] / 150.0)
        self.bottom_r = int(30 * self.size[0] / 150.0)
        self.v_gauge_margin_t = int(120 * self.size[0] / 500.0)
        self.v_gauge_margin_b = int(120 * self.size[0] / 500.0) + self.bottom_r

        self.canvas = pygame.Surface((self.size[0], self.size[1] - 1), flags=pygame.SRCALPHA)
        self.canvas.fill((0, 0, 0, 0))
        self.draw_thermometer()

    def get_canvas(self):
        return self.canvas

    def update_colors(self, color, border_color):
        self.color = color
        self.border_color = border_color

    def update_values(self, number):
        self.number = number
        self.canvas.fill((0, 0, 0, 0))
        self.draw_thermometer()

    def draw_thermometer(self):
        # set constraints
        l = self.center[0] - self.bar_width // 2
        r = self.center[0] + self.bar_width // 2
        t = self.v_margin + self.bar_width // 2
        b = self.size[1] - self.v_margin - self.bottom_r // 2
        bw = 2  # border width

        # draw 2 vertical borders
        pygame.draw.line(self.canvas, self.border_color, [l, t], [l, b], bw)
        pygame.draw.line(self.canvas, self.border_color, [r, t], [r, b], bw)

        # draw a circle at the bottom
        pygame.draw.circle(self.canvas, self.color, (self.center[0], b), self.bottom_r, 0)
        pygame.draw.circle(self.canvas, self.border_color, (self.center[0], b), self.bottom_r, bw)

        # draw an arc at the top
        rct = pygame.Rect((l, t - self.bar_width // 2), (self.bar_width+bw, self.bar_width+bw))
        pygame.draw.arc(self.canvas, self.border_color, rct, 0, pi, bw)

        # draw markers and numbers
        line_length = self.size[1] - self.v_gauge_margin_t - self.v_gauge_margin_b
        dist = self.rng[1] - self.rng[0]
        step = line_length * 1.0 / (dist + 1)

        for i in range(dist, -1, -1):
            vl = self.rng[0] + dist - i
            if vl % 10 == 0:
                ln = self.marker_len10
            elif vl % 5 == 0:
                ln = self.marker_len5
            else:
                ln = self.marker_len
            pygame.draw.line(self.canvas, self.border_color,
                             [r, self.v_gauge_margin_t + i * step],
                             [r + ln, self.v_gauge_margin_t + i * step], 1)
            if i % self.lbl_dist == 0:
                val = str(vl)
                font_size = self.game_board.t_font.size(val)
                text = self.game_board.t_font.render(val, 1, self.border_color)
                x = r + self.marker_len10 + self.marker_len
                y = self.v_gauge_margin_t + i * step - font_size[1] // 2
                self.canvas.blit(text, (x, y))

        # draw bar fill
        bw = 2
        t2 = self.size[1] - (self.v_gauge_margin_b + step * (abs(self.rng[0] - self.number) + 1))
        pygame.draw.polygon(self.canvas, self.color, [[l+bw, b-bw], [r-bw+1, b-bw], [r-bw+1, t2], [l+bw, t2]])
