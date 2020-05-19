# -*- coding: utf-8 -*-

import pygame
import copy

import classes.extras as ex


class Clock:
    def __init__(self, game_board, wrapper, width, height, times, prefs):
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
        self.black = (0, 0, 0)

        #diff colours
        self.colors = [color1, color2]
        self.colors2 = [color3, color4]
        self.colors3 = [color5, color6]
        self.colors4 = [color7, color8]

        self.hand_coords = [[], []]
        self.size = [width, height]
        self.times = times

        self.clock_wrapper = wrapper  # self.board.ships[-1]
        self.clock_wrapper.font = game_board.clock_fonts[0]
        self.clock_wrapper.font2 = game_board.clock_fonts[1]
        self.clock_wrapper.font3 = game_board.clock_fonts[2]

        self.clock_wrapper.hidden_value = [2, 3]
        self.clock_wrapper.font_color = color2

        self.margin = 30 * self.size[0] / 500.0
        self.h_marker_len = 15 * self.size[1] / 150.0
        self.h_marker_len15 = 7 * self.size[1] / 150.0
        self.m_marker_len15 = 20 * self.size[1] / 150.0
        self.m_marker_len5 = 15 * self.size[1] / 150.0
        self.m_marker_len = 10 * self.size[1] / 150.0
        self.centre_margin = 35 * self.size[1] / 150.0
        self.diff_h = 25 * self.size[1] / 150.0

        self.draw_all(times)

    def draw_all(self, times):
        self.times = times
        self.diff_solution = self.get_diff()
        self.canvas = pygame.Surface((self.size[0], self.size[1] - 1))
        if self.game_board.mainloop.scheme is not None:
            self.canvas.fill(self.game_board.mainloop.scheme.u_color)
        else:
            self.canvas.fill((255, 255, 255))
        self.draw_linear_clock()
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

    def draw_linear_clock(self):
        if self.show_24h:
            wrap = 24
        else:
            wrap = 12

        # scale the view to only the hours that need to be visible - not 1- 24, but time[0][0] - time[1][0] + 1
        line_length = self.size[0] - 2.0 * self.margin

        # draw markers and numbers for all hours displayed
        if self.times[0][0] != self.times[1][0]:
            if self.times[1][0] < self.times[0][0]:
                dist = self.times[1][0] + wrap - self.times[0][0]
            else:
                dist = self.times[1][0] - self.times[0][0]
        else:
            if self.times[1][1] < self.times[0][1]:
                dist = wrap
            else:
                dist = 0
        if dist > 0 and self.times[0] != self.times[1] and self.times[1][1] == 0:
            dist -= 1
        h_step = line_length * 1.0 / (dist + 1)
        hours = []

        for i in range(0, dist+2):
            pygame.draw.line(self.canvas, self.colors2[0],
                             [self.margin + i * h_step, self.size[1]//2 - self.centre_margin],
                             [self.margin + i * h_step, self.size[1]//2 - self.centre_margin - self.h_marker_len], 1)
            if (self.times[0][0] + i) % wrap != 0:
                val = str((self.times[0][0] + i) % wrap)
                hours.append((self.times[0][0] + i) % wrap)
            else:
                val = str(self.times[0][0] + i % wrap)
                hours.append(self.times[0][0] + i % wrap)
            font_size = self.clock_wrapper.font3.size(val)
            text = self.clock_wrapper.font3.render(val, 1, self.colors2[0])
            x = self.margin + i * h_step - int(font_size[0] / 2.0)
            y = self.size[1] // 2 - self.centre_margin - self.h_marker_len - font_size[1]
            self.canvas.blit(text, (x, y))

        # draw markers every 15 minutes
        for i in range(0, (dist+1) * 4):
            if i % 4 != 0:
                pygame.draw.line(self.canvas, self.colors2[0],
                                 [self.margin + i * h_step / 4.0, self.size[1] // 2 - self.centre_margin],
                                 [self.margin + i * h_step / 4.0, self.size[1] // 2 - self.centre_margin - self.h_marker_len15], 1)

        if self.times[0] != self.times[1]:
            # draw hour difference
            l = self.margin + self.times[0][1] * h_step / 60.0
            if self.times[1][1] == 0:
                r = self.size[0] - self.margin
            else:
                r = self.size[0] - (self.margin + (60 - self.times[1][1]) * h_step / 60.0)
            t = self.size[1]//2 - self.centre_margin + 1
            b = self.size[1]//2 - self.centre_margin + self.diff_h

            p = [[l, t], [r, t], [r, b], [l, b], [l, t]]

            pygame.draw.polygon(self.canvas, self.diff_h_col, p, 0)
            pygame.draw.polygon(self.canvas, self.diff_h_bcol, p, 1)

            # recolour the remainder of last hour
            if self.times[0][1] != self.times[1][1]:
                if self.times[0][1] < self.times[1][1] or self.times[1][1] == 0:
                    d = dist
                else:
                    d = (dist - 1)
                l2 = l + d * h_step
                p = [[l2, t], [r, t], [r, b], [l2, b], [l2, t]]
                pygame.draw.polygon(self.canvas, self.diff_hr_col, p, 0)
                pygame.draw.polygon(self.canvas, self.diff_h_bcol, p, 1)

                if self.show_result:
                    #display number of minutes inside remainder
                    val = "%sm" % self.diff_solution[1]
                    font_size = self.clock_wrapper.font3.size(val)
                    x = l2 + (r - l2) / 2 - font_size[0] / 2
                    y = self.size[1] // 2 - self.centre_margin + (self.diff_h - font_size[1]) / 2
                    if font_size[0] < (r - l2) - 5:
                        x = l2 + (r - l2) / 2 - font_size[0] / 2
                        text = self.clock_wrapper.font3.render(val, 1, self.white)
                    else:
                        x = r + 5
                        text = self.clock_wrapper.font3.render(val, 1, self.colors2[1])
                    self.canvas.blit(text, (x, y))

            # draw white lines - divide hours
            if dist > 0:
                for i in range(1, dist + 1):
                    if l + i * h_step < r:
                        pygame.draw.line(self.canvas, self.white, [l + i * h_step, t], [l + i * h_step, b], 1)

            if self.show_result:
                d = self.diff_solution[0]
                for i in range(0, d):
                    if i < d:
                        l = self.margin + h_step * i + self.times[0][1] * h_step / 60.0
                        r = self.margin + h_step * (i + 1) + self.times[0][1] * h_step / 60.0

                        val = "%sh" % (i + 1)
                        font_size = self.clock_wrapper.font3.size(val)
                        x = l + (r - l) / 2 - font_size[0] / 2
                        y = self.size[1] // 2 - self.centre_margin + (self.diff_h - font_size[1]) / 2
                        text = self.clock_wrapper.font3.render(val, 1, self.white)
                        self.canvas.blit(text, (x, y))

        # draw markers and numbers for all minutes
        m_step = line_length * 1.0 / 60
        for i in range(0, 61):
            if i % 15 == 0:
                m_len = self.m_marker_len15
            elif i % 5 == 0:
                m_len = self.m_marker_len5
            else:
                m_len = self.m_marker_len

            if i % 5 == 0:
                font_size = self.clock_wrapper.font3.size(str(i))
                text = self.clock_wrapper.font3.render(str(i), 1, self.colors2[1])
                x = self.margin + i * m_step - int(font_size[0] / 2.0)
                y = self.size[1] // 2 + self.centre_margin + self.m_marker_len15
                self.canvas.blit(text, (x, y))

            pygame.draw.line(self.canvas, self.colors2[1],
                             [self.margin + i * m_step, self.size[1]//2 + self.centre_margin],
                             [self.margin + i * m_step, self.size[1]//2 + self.centre_margin + m_len], 1)

        # draw minutes difference
        if self.times[0][1] < self.times[1][1]: #if first time is smaller than second time - all minutes in one hour
            l = self.margin + self.times[0][1] * m_step
            r = self.margin + self.times[1][1] * m_step
            t = self.size[1] // 2 + self.centre_margin - 1
            b = self.size[1] // 2 + self.centre_margin - self.diff_h

            p = [[l, t], [r, t], [r, b], [l, b], [l, t]]

            pygame.draw.polygon(self.canvas, self.diff_m_col, p, 0)
            pygame.draw.polygon(self.canvas, self.diff_m_bcol, p, 1)

            if self.show_result:
                val = "%sm" % (self.times[1][1] - self.times[0][1])
                font_size = self.clock_wrapper.font3.size(val)
                y = self.size[1] // 2 + self.centre_margin - self.diff_h + (self.diff_h - font_size[1]) / 2
                if font_size[0] < (r - l) - 5:
                    x = l + (r - l) / 2 - font_size[0] / 2
                    text = self.clock_wrapper.font3.render(val, 1, self.white)
                else:
                    x = r + 5
                    text = self.clock_wrapper.font3.render(val, 1, self.colors2[1])
                self.canvas.blit(text, (x, y))

        elif self.times[0][1] > self.times[1][1]:
            t = self.size[1] // 2 + self.centre_margin - 1
            b = self.size[1] // 2 + self.centre_margin - self.diff_h

            l1 = self.margin + self.times[0][1] * m_step
            r1 = self.size[0] - self.margin
            p1 = [[l1, t], [r1, t], [r1, b], [l1, b], [l1, t]]
            pygame.draw.polygon(self.canvas, self.diff_m_col, p1, 0)
            pygame.draw.polygon(self.canvas, self.diff_m_bcol, p1, 1)

            if self.show_result:
                val = "%sm" % (60 - self.times[0][1])
                font_size = self.clock_wrapper.font3.size(val)
                y = self.size[1] // 2 + self.centre_margin - self.diff_h + (self.diff_h - font_size[1]) / 2
                if font_size[0] < (r1 - l1) - 5:
                    x = l1 + (r1 - l1) / 2 - font_size[0] / 2
                    text = self.clock_wrapper.font3.render(val, 1, self.white)
                else:
                    x = r1 + 5
                    text = self.clock_wrapper.font3.render(val, 1, self.colors2[1])
                self.canvas.blit(text, (x, y))

            if self.times[1][1] != 0:
                l2 = self.margin
                r2 = self.margin + self.times[1][1] * m_step
                p2 = [[l2, t], [r2, t], [r2, b], [l2, b], [l2, t]]
                pygame.draw.polygon(self.canvas, self.diff_m_col, p2, 0)
                pygame.draw.polygon(self.canvas, self.diff_m_bcol, p2, 1)
                if self.show_result:
                    val = "%sm" % self.times[1][1]
                    font_size = self.clock_wrapper.font3.size(val)
                    y = self.size[1] // 2 + self.centre_margin - self.diff_h + (self.diff_h - font_size[1]) / 2
                    if font_size[0] < (r2 - l2) - 5:
                        x = l2 + (r2 - l2) / 2 - font_size[0] / 2
                        text = self.clock_wrapper.font3.render(val, 1, self.white)
                    else:
                        x = l2 - font_size[0] - 5
                        text = self.clock_wrapper.font3.render(val, 1, self.colors2[1])
                    self.canvas.blit(text, (x, y))

        # draw a horizontal lines through the centre of the view
        pygame.draw.line(self.canvas, self.colors2[0],
                         [self.margin, self.size[1]//2 - self.centre_margin],
                         [self.size[0]-self.margin, self.size[1]//2 - self.centre_margin], 2)

        pygame.draw.line(self.canvas, self.colors2[1],
                         [self.margin, self.size[1]//2 + self.centre_margin],
                         [self.size[0]-self.margin, self.size[1]//2 + self.centre_margin], 2)

        self.clock_wrapper.update_me = True


