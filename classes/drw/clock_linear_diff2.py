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
        self.centre_margin = 25 * self.size[1] / 150.0
        self.diff_h = 30 * self.size[1] / 150.0
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
                dist = 12
            else:
                dist = 0

        if dist > 0 and self.times[0] != self.times[1] and self.times[1][1] == 0:
            dist -= 1

        h_step = line_length * 1.0 / (dist + 1)

        hours = []

        for i in range(0, dist + 2):
            pygame.draw.line(self.canvas, self.colors2[0],
                             [self.margin + i * h_step, self.size[1] // 2 + self.centre_margin],
                             [self.margin + i * h_step, self.size[1] // 2 + self.centre_margin + self.h_marker_len], 1)
            if (self.times[0][0] + i) % wrap != 0:
                val = str((self.times[0][0] + i) % wrap)
                hours.append((self.times[0][0] + i) % wrap)
            else:
                val = str(self.times[0][0] + i % wrap)
                hours.append(self.times[0][0] + i % wrap)
            font_size = self.clock_wrapper.font3.size(val)
            text = self.clock_wrapper.font3.render(val, 1, self.colors2[0])
            x = self.margin + i * h_step - int(font_size[0] / 2.0)
            y = self.size[1] // 2 + self.centre_margin + self.m_marker_len15  # + font_size[1]
            self.canvas.blit(text, (x, y))

        # draw markers every 15 minutes
        if dist != 0:
            for i in range(0, (dist + 1) * 4):
                if i % 4 != 0:
                    pygame.draw.line(self.canvas, self.colors2[0],
                                     [self.margin + i * h_step / 4.0, self.size[1] // 2 + self.centre_margin],
                                     [self.margin + i * h_step / 4.0,
                                      self.size[1] // 2 + self.centre_margin + self.h_marker_len15], 1)
        else: #draw markers every 5 minutes as well
            m_step = line_length * 1.0 / 60
            for i in range(0, 61):
                if i % 15 == 0:
                    m_len = self.m_marker_len15
                elif i % 5 == 0:
                    m_len = self.m_marker_len5
                else:
                    m_len = self.m_marker_len

                pygame.draw.line(self.canvas, self.colors2[0],
                                 [self.margin + i * m_step, self.size[1] // 2 + self.centre_margin],
                                 [self.margin + i * m_step, self.size[1] // 2 + self.centre_margin + m_len], 1)


        t = self.size[1] // 2 + self.centre_margin - self.diff_h
        b = self.size[1] // 2 + self.centre_margin - 1

        if self.times[0] != self.times[1]:
            #draw minute difference before first full hour
            #if there's exactly 1 hour difference on the hours ie 10:00 - 11:00
            if self.times[0][0] != self.times[1][0] and self.times[0][1] == 0 and self.times[1][1] == 0:
                l = self.margin
                r = self.size[0] - self.margin
                p = [[l, t], [r, t], [r, b], [l, b], [l, t]]

                pygame.draw.polygon(self.canvas, self.diff_h_col, p, 0)
                pygame.draw.polygon(self.canvas, self.diff_h_bcol, p, 1)
            elif dist == 0:
                if self.times[0][0] == self.times[1][0]:
                    l = self.margin + self.times[0][1] * h_step / 60.0
                    r = self.size[0] - (self.margin + (60 - self.times[1][1]) * h_step / 60.0)
                else: #case of ie. 3:45 - 4:00
                    l = self.margin + self.times[0][1] * h_step / 60.0
                    r = self.size[0] - self.margin
                p = [[l, t], [r, t], [r, b], [l, b], [l, t]]

                pygame.draw.polygon(self.canvas, self.diff_m_col, p, 0)
                pygame.draw.polygon(self.canvas, self.diff_m_bcol, p, 1)
            elif self.times[0][1] != 0:
                l = self.margin + self.times[0][1] * h_step / 60.0
                r = self.margin + h_step

                p = [[l, t], [r, t], [r, b], [l, b], [l, t]]

                pygame.draw.polygon(self.canvas, self.diff_m_col, p, 0)
                pygame.draw.polygon(self.canvas, self.diff_m_bcol, p, 1)
            if self.show_result:
                if self.times[0][1] != 0 or (dist == 0 and not (self.times[0][1] == 0 and self.times[1][1] == 0)):
                    # display partial difference
                    if dist == 0 and self.times[0][0] == self.times[1][0]:
                        val = "%sm" % (self.times[1][1] - self.times[0][1])
                    else:
                        val = "%sm" % (60 - self.times[0][1])
                    font_size = self.clock_wrapper.font3.size(val)
                    x = l + (r - l) / 2 - font_size[0] / 2
                    if font_size[0] < (r - l) - 5:
                        y = self.size[1] // 2 + self.centre_margin - self.diff_h + (self.diff_h - font_size[1]) / 2
                        text = self.clock_wrapper.font3.render(val, 1, self.white)
                    else:
                        if dist == 1:
                            x = r - font_size[0] - 5
                        y = self.size[1] // 2 + self.centre_margin - self.diff_h - font_size[1]
                        text = self.clock_wrapper.font3.render(val, 1, self.colors2[1])
                    self.canvas.blit(text, (x, y))

            #draw hour difference if more than 1
            if dist > 0:
                if self.times[0][1] == 0:
                    l = self.margin
                else:
                    l = self.margin + h_step

                if self.times[1][1] == 0:
                    r = self.size[0] - self.margin
                else:
                    r = self.size[0] - self.margin - h_step
                p = [[l, t], [r, t], [r, b], [l, b], [l, t]]

                pygame.draw.polygon(self.canvas, self.diff_h_col, p, 0)
                pygame.draw.polygon(self.canvas, self.diff_h_bcol, p, 1)



            #draw minute difference after last full hour
            if dist > 0:
                if self.times[1][1] > 0:
                    l = self.size[0] - self.margin - h_step
                    r = self.size[0] - (self.margin + (60 - self.times[1][1]) * h_step / 60.0)
                    p = [[l, t], [r, t], [r, b], [l, b], [l, t]]

                    pygame.draw.polygon(self.canvas, self.diff_m_col, p, 0)
                    pygame.draw.polygon(self.canvas, self.diff_m_bcol, p, 1)

                    #display partial difference
                    if self.show_result:
                        val = "%sm" % self.times[1][1]
                        font_size = self.clock_wrapper.font3.size(val)
                        x = l + (r - l) / 2 - font_size[0] / 2
                        if font_size[0] < (r - l) - 5:
                            y = self.size[1] // 2 + self.centre_margin - self.diff_h + (self.diff_h - font_size[1]) / 2
                            text = self.clock_wrapper.font3.render(val, 1, self.white)
                        else:
                            if dist == 1:
                                x = l + 5
                            y = self.size[1] // 2 + self.centre_margin - self.diff_h - font_size[1]
                            text = self.clock_wrapper.font3.render(val, 1, self.colors2[1])
                        self.canvas.blit(text, (x, y))

            # draw white lines - divide hours
            if dist > 0:
                for i in range(1, dist + 1):
                    pygame.draw.line(self.canvas, self.white, [self.margin + i * h_step, t], [self.margin + i * h_step, b], 1)

            if self.show_result:
                for i in range(1, dist + 2):
                    if i < dist or \
                            (i < dist + 1 and self.times[0][1] == 0) or \
                            (i < dist + 1 and self.times[1][1] == 0) or \
                            (self.times[0][1] == 0 and self.times[1][1] == 0):
                        if self.times[0][1] == 0:
                            l = self.margin + h_step * (i - 1)
                        else:
                            l = self.margin + h_step * i

                        if self.times[0][1] == 0:
                            r = self.margin + h_step * i
                        else:
                            r = self.margin + h_step * (i + 1)
                        val = "%sh" % i
                        font_size = self.clock_wrapper.font3.size(val)
                        x = l + (r - l) / 2 - font_size[0] / 2
                        y = self.size[1] // 2 + self.centre_margin - self.diff_h + (self.diff_h - font_size[1]) / 2
                        text = self.clock_wrapper.font3.render(val, 1, self.white)
                        self.canvas.blit(text, (x, y))

        # draw a horizontal line
        pygame.draw.line(self.canvas, self.colors2[0],
                         [self.margin, self.size[1] // 2 + self.centre_margin],
                         [self.size[0] - self.margin, self.size[1] // 2 + self.centre_margin], 2)

        self.clock_wrapper.update_me = True
