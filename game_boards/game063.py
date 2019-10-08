# -*- coding: utf-8 -*-

import os
import pygame
import random
from math import pi, cos, sin

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 12, 13)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 19, 10)

    def create_game_objects(self, level=1):
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = True
        self.ai_speed = 18
        self.correct = False
        self.board.draw_grid = False
        if self.mainloop.scheme is not None:
            color1 = self.mainloop.scheme.color1  # bright side of short hand
            color3 = self.mainloop.scheme.color3  # inner font color
            color5 = self.mainloop.scheme.color5  # dark side of short hand
            color7 = self.mainloop.scheme.color7  # inner circle filling

            color2 = self.mainloop.scheme.color2  # bright side of long hand
            color4 = self.mainloop.scheme.color4  # ex.hsv_to_rgb(170,255,255)#outer font color
            color6 = self.mainloop.scheme.color6  # dark side of long hand
            color8 = self.mainloop.scheme.color8  # outer circle filling
            self.h_col = color5
            self.m_col = color6

            white = self.mainloop.scheme.u_color
            gray = (100, 100, 100)
        else:
            color1 = ex.hsv_to_rgb(225, 70, 230)
            color3 = ex.hsv_to_rgb(225, 255, 255)
            color5 = ex.hsv_to_rgb(225, 180, 240)
            color7 = ex.hsv_to_rgb(225, 10, 255)

            color2 = ex.hsv_to_rgb(170, 70, 230)
            color4 = ex.hsv_to_rgb(170, 255, 255)
            color6 = ex.hsv_to_rgb(170, 180, 240)
            color8 = ex.hsv_to_rgb(170, 10, 255)

            self.h_col = ex.hsv_to_rgb(225, 190, 220)
            self.m_col = ex.hsv_to_rgb(170, 190, 220)

            white = (255, 255, 255)
            gray = (100, 100, 100)

        transp = (0, 0, 0, 0)
        self.color3 = color3
        self.color4 = color4

        self.colors = [color1, color2]
        self.colors2 = [color3, color4]
        self.colors3 = [color5, color6]
        self.colors4 = [color7, color8]

        self.h_col = ex.hsv_to_rgb(225, 190, 220)
        self.m_col = ex.hsv_to_rgb(170, 190, 220)

        if self.level.lvl == 1:
            data = [19, 10, True, True, False, False, True, False, False, True, True, 15]
            h_pool = [i for i in range(1, 13)]
            m_pool = [0]
        elif self.level.lvl == 2:
            data = [19, 10, True, True, False, False, True, False, False, True, True, 15]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60, 15)]
        elif self.level.lvl == 3:
            data = [19, 10, True, True, False, False, False, True, False, True, True, 15]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60, 5)]
        elif self.level.lvl == 4:
            data = [19, 10, True, True, False, False, False, True, False, True, True, 15]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60, 5)]
        elif self.level.lvl == 5:
            data = [19, 10, True, True, False, False, False, False, False, True, True, 25]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60)]
        elif self.level.lvl == 6:
            data = [19, 10, True, True, True, False, True, False, False, True, True, 15]
            h_pool = [i for i in range(13, 24)]
            m_pool = [0]
        elif self.level.lvl == 7:
            data = [19, 10, True, True, True, False, False, True, False, True, True, 15]
            h_pool = [i for i in range(13, 24)]
            h_pool.append(0)
            m_pool = [i for i in range(0, 60, 5)]
        elif self.level.lvl == 8:
            data = [19, 10, True, True, True, False, False, False, False, True, True, 25]
            h_pool = [i for i in range(0, 24)]
            m_pool = [i for i in range(0, 60)]
        elif self.level.lvl == 9:
            data = [19, 10, True, True, False, False, False, False, False, False, True, 25]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60)]
        elif self.level.lvl == 10:
            data = [19, 10, True, True, False, False, False, True, False, False, True, 25]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60)]
        elif self.level.lvl == 11:
            data = [19, 10, True, True, False, False, True, False, False, False, True, 25]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60)]
        elif self.level.lvl == 12:
            data = [19, 10, True, False, False, False, False, False, False, False, True, 25]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60)]
        elif self.level.lvl == 13:
            data = [19, 10, True, False, False, True, False, False, False, False, True, 25]
            h_pool = [i for i in range(1, 13)]
            m_pool = [i for i in range(0, 60)]

        # visual display properties
        self.show_outer_ring = data[2]
        self.show_minutes = data[3]
        self.show_24h = data[4]
        self.show_only_quarters_h = data[5]
        self.show_only_quarters_m = data[6]
        self.show_only_fives_m = data[7]
        self.show_only_spare_variable = data[8]
        self.show_highlight = data[9]
        self.show_hour_offset = data[10]
        self.show_roman = False

        self.level.games_per_lvl = data[11]

        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        x_count = self.get_x_count(data[1], even=False)
        if x_count > data[0]:
            data[0] = x_count

        self.font_size = 0
        self.data = data

        self.layout.update_layout(data[0], data[1])

        self.board.level_start(data[0], data[1], self.layout.scale)

        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        size = self.board.scale * 10
        self.size = size
        ans_offset = 10 + (data[0] - 15) // 2
        self.board.add_unit(10, 0, data[0] - 10, 2, classes.board.Label, self.lang.d["What time"], white, "", 2)
        self.board.units[-1].font_color = gray
        self.board.add_unit(ans_offset, 4, 2, 2, classes.board.Letter, "00", white, "", 34)
        self.ans_h = self.board.ships[-1]
        self.ans_h.checkable = True
        self.ans_h.init_check_images()
        self.board.active_ship = self.ans_h.unit_id
        self.home_square = self.ans_h

        self.board.add_unit(ans_offset + 2, 4, 1, 2, classes.board.Label, ":", white, "", 34)
        self.board.add_unit(ans_offset + 3, 4, 2, 2, classes.board.Letter, "00", white, "", 34)
        self.ans_m = self.board.ships[-1]
        self.ans_m.checkable = True
        self.ans_m.init_check_images()

        self.ans_h.set_outline(color3, 5)
        self.ans_m.set_outline(color4, 5)

        self.ans_h.immobilize()
        self.ans_m.immobilize()

        self.ans_h.readable = False
        self.ans_m.readable = False

        self.ans_h.font_color = color3
        self.ans_m.font_color = color4

        # add up/down buttons
        self.board.add_unit(ans_offset, 2, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)

        self.board.add_unit(ans_offset, 6, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.h_col)

        self.board.add_unit(ans_offset + 3, 2, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_u_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        self.board.add_unit(ans_offset + 3, 6, 2, 2, classes.board.ImgCenteredShip, "", transp,
                            img_src='nav_d_mts.png', alpha=True)
        self.board.ships[-1].set_tint_color(self.m_col)

        self.buttons = []

        for i in range(4):
            self.buttons.append(self.board.ships[-4 + i])
            self.buttons[-1].immobilize()

        self.center = [size // 2, size // 2]
        self.board.add_unit(0, 0, 10, 10, classes.board.Ship, "", white, "", self.font_size)
        self.clock_canvas = self.board.ships[-1]
        self.clock_canvas.font = self.clock_canvas.board.font_sizes[2]
        self.clock_canvas.font2 = self.clock_canvas.board.font_sizes[7]
        self.clock_canvas.font3 = self.clock_canvas.board.font_sizes[26]
        self.clock_canvas.immobilize()
        self.canvas = pygame.Surface([size, size - 1])
        if self.mainloop.scheme is not None:
            self.canvas.fill(self.mainloop.scheme.u_color)
        else:
            self.canvas.fill((255, 255, 255))
        self.time = [random.choice(h_pool), random.choice(m_pool)]  # [random.randrange(0,23),random.randrange(0,60)]

        tint_h = self.colors3[0]
        tint_m = self.colors3[1]

        shrink = 0.72
        self.whs = int(self.size * shrink)
        self.hand_h = self.scalled_img(
            pygame.image.load(os.path.join('res', 'images', "clock_h.png")).convert_alpha(), self.whs, self.whs)
        self.hand_h.fill(tint_h, special_flags=pygame.BLEND_ADD)

        self.hand_m = self.scalled_img(
            pygame.image.load(os.path.join('res', 'images', "clock_m.png")).convert_alpha(), self.whs, self.whs)
        self.hand_m.fill(tint_m, special_flags=pygame.BLEND_ADD)
        self.pivot = [self.whs // 2, self.whs // 2]
        self.hands = [self.hand_h, self.hand_m]

        self.hands_vars()
        self.draw_hands()
        #self.draw_hands(self.time, canvas, size, center, [color1, color2], [color3, color4], [color5, color6],
        #                [color7, color8])  # data[7](data, canvas, i)

        self.clock_canvas.hidden_value = [2, 3]  # numbers[i]
        self.clock_canvas.font_color = color2
        self.clock_canvas.painting = self.canvas.copy()

    def auto_check_reset(self):
        self.ans_h.set_display_check(None)
        self.ans_m.set_display_check(None)

        self.ans_h.set_outline(self.color3, 5)
        self.ans_m.set_outline(self.color4, 5)

    def hands_vars(self):
        self.angle_step_12 = 2 * pi / 12
        self.angle_step_60 = 2 * pi / 60
        self.angle_start = -pi / 2
        r = self.size // 3 + self.size // 10
        self.r = r
        if self.show_24h:
            self.rs = [r * 0.54, r * 0.85, r * 0.6]
        else:
            self.rs = [r * 0.6, r * 0.85, r * 0.6]

    def draw_hands(self):
        self.clock_wrapper = self.clock_canvas
        if self.show_hour_offset:
            a1 = self.angle_start + (2 * pi / 12) * self.time[0] + \
                 (self.angle_step_12 * (2 * pi / 60) * self.time[1]) / (2 * pi)
        else:
            a1 = self.angle_start + (2 * pi / 12) * self.time[0]
        a2 = self.angle_start + (2 * pi / 60) * self.time[1]
        self.angles = [a1, a2]

        rs = self.rs
        time = self.time

        if self.show_outer_ring:
            pygame.draw.circle(self.canvas, self.colors4[1], self.center, int(rs[1] + 10 * self.layout.scale / 62), 0)
            pygame.draw.circle(self.canvas, self.colors2[1], self.center, int(rs[1] + 10 * self.layout.scale / 62), 1)

        pygame.draw.circle(self.canvas, self.colors4[0], self.center, int(rs[2] + 10 * self.layout.scale / 62), 0)
        pygame.draw.circle(self.canvas, self.colors2[0], self.center, int(rs[2] + 10 * self.layout.scale / 62), 1)

        if self.show_outer_ring:
            for i in range(60):
                val = str(i + 1)
                if self.show_only_quarters_m:
                    if (i + 1) % 15 != 0:
                        val = ""
                elif self.show_only_fives_m:
                    if (i + 1) % 5 != 0:
                        val = ""
                if i == 59:
                    val = "0"
                a = self.angle_start + self.angle_step_60 * (i + 1)
                if self.show_minutes:
                    font_size = self.clock_wrapper.font3.size(val)
                    if not self.show_highlight or (i + 1 == time[1] or (time[1] == 0 and i == 59)):
                        text = self.clock_wrapper.font3.render("%s" % (val), 1, self.colors2[1])
                    else:
                        text = self.clock_wrapper.font3.render("%s" % (val), 1, self.colors[1])
                    offset3 = rs[1] + 10 + 15 * self.size / 500.0 + font_size[1] // 2
                    x3 = offset3 * cos(a) + self.center[0] - int(font_size[0] / 2.0)
                    y3 = offset3 * sin(a) + self.center[1] - int(font_size[1] / 2.0)

                    self.canvas.blit(text, (x3, y3))
                    if self.show_only_quarters_m or self.show_only_fives_m:
                        if (i + 1) % 15 == 0:
                            marklen = 10 + 15 * self.size / 500.0
                        elif (i + 1) % 5 == 0:
                            marklen = 10 + 10 * self.size / 500.0
                        else:
                            marklen = 10 + 5 * self.size / 500.0
                    else:
                        marklen = 10 + 10 * self.size / 500.0
                else:
                    if (i + 1) % 15 == 0:
                        marklen = 10 + 15 * self.size / 500.0
                    elif (i + 1) % 5 == 0:
                        marklen = 10 + 10 * self.size / 500.0
                    else:
                        marklen = 10 + 5 * self.size / 500.0
                if self.show_outer_ring:
                    x1 = (rs[1] + 10) * cos(a) + self.center[0]
                    y1 = (rs[1] + 10) * sin(a) + self.center[1]

                    x2 = (rs[1] + marklen) * cos(a) + self.center[0]
                    y2 = (rs[1] + marklen) * sin(a) + self.center[1]

                    pygame.draw.aaline(self.canvas, self.colors2[1], [x1, y1], [x2, y2])

        for i in range(12):
            val = str(i + 1)
            if self.show_only_quarters_h:
                if (i + 1) % 3 != 0:
                    val = ""

            a = self.angle_start + self.angle_step_12 * (i + 1)
            x1 = (rs[2] + 10) * cos(a) + self.center[0]
            y1 = (rs[2] + 10) * sin(a) + self.center[1]

            x2 = (rs[2] + 10 + 10 * self.size / 500.0) * cos(a) + self.center[0]
            y2 = (rs[2] + 10 + 10 * self.size / 500.0) * sin(a) + self.center[1]

            pygame.draw.aaline(self.canvas, self.colors2[0], [x1, y1], [x2, y2])

            font_size = self.clock_wrapper.font.size(val)
            if not self.show_highlight or i + 1 == time[0]:
                text = self.clock_wrapper.font.render("%s" % (val), 1, self.colors2[0])
            else:
                text = self.clock_wrapper.font.render("%s" % (val), 1, self.colors[0])
            if self.show_roman:
                text_angle = -(360 / 12.0) * (i + 1)
                text = pygame.transform.rotate(text, text_angle)
                rect = text.get_rect()
                x3 = (rs[2] + 10 + 7 * self.size / 500.0 + font_size[1] // 2) * cos(a) + self.center[0] - rect.width / 2
                y3 = (rs[2] + 10 + 7 * self.size / 500.0 + font_size[1] // 2) * sin(a) + \
                     self.center[1] - rect.height / 2

            else:
                x3 = (rs[2] + 10 + 7 * self.size / 500.0 +
                      font_size[1] / 2) * cos(a) + self.center[0] - font_size[0] / 2
                y3 = (rs[2] + 10 + 7 * self.size / 500.0 +
                      font_size[1] / 2) * sin(a) + self.center[1] - font_size[1] / 2
            self.canvas.blit(text, (x3, y3))

            if self.show_24h:
                if i + 13 == 24:
                    val = "0"
                    v = 0
                else:
                    val = str(i + 13)
                    v = i + 13
                font_size = self.clock_wrapper.font2.size(val)
                if not self.show_highlight or v == time[0]:
                    text = self.clock_wrapper.font2.render("%s" % (val), 1, self.colors2[0])
                else:
                    text = self.clock_wrapper.font2.render("%s" % (val), 1, self.colors[0])

                x3 = (rs[0] + font_size[1] // 4) * cos(a) + self.center[0] - font_size[0] / 2
                y3 = (rs[0] + font_size[1] // 4) * sin(a) + self.center[1] - font_size[1] / 2
                self.canvas.blit(text, (x3, y3))
        hand_width = [self.r // 14, self.r // 18]
        start_offset = [self.size // 10, self.size // 12]

        for i in range(2):
            # angle for line
            angle = self.angles[i]  # angle_start + angle_step*i

            x0 = self.center[0] - start_offset[i] * cos(angle)
            y0 = self.center[1] - start_offset[i] * sin(angle)

            # Calculate the x,y for the end point
            x1 = rs[i] * cos(angle) + self.center[0]
            y1 = rs[i] * sin(angle) + self.center[1]
            x2 = hand_width[i] * cos(angle - pi / 2) + self.center[0]
            y2 = hand_width[i] * sin(angle - pi / 2) + self.center[1]

            x3 = hand_width[i] * cos(angle + pi / 2) + self.center[0]
            y3 = hand_width[i] * sin(angle + pi / 2) + self.center[1]

            points = [[x0, y0], [x2, y2], [x1, y1], [x3, y3]]
            #self.hand_coords[i] = points
        self.clock_wrapper.update_me = True

        for i in range(0, 2):
            angle = 360 - ((self.angles[i] + pi / 2) * 180 / pi)
            img = self.rotatePivoted(self.hands[i], angle, self.pivot)
            self.canvas.blit(img[0], ((self.size - self.whs) // 2 + img[1][0], (self.size - self.whs) // 2 + img[1][1]))

        #self.update_text_time()
        self.clock_canvas.update_me = True
        self.mainloop.redraw_needed[0] = True

    def scalled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    def rotatePivoted(self, img, angle, pivot):
        image = pygame.transform.rotate(img, angle)
        rect = image.get_rect()
        rect.center = pivot
        return image, rect

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.show_msg == False:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.auto_check_reset()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    active = self.board.active_ship
                    for i in range(4):
                        if self.buttons[i].unit_id == active:
                            self.on_btn_click(i)
                            break
            if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN and not self.correct:
                lhv = len(self.home_square.value)
                self.changed_since_check = True
                if event.key == pygame.K_BACKSPACE:
                    if lhv > 0:
                        self.home_square.value = self.home_square.value[0:lhv - 1]
                else:
                    char = event.unicode
                    if (len(char) > 0 and lhv < 3 and char in self.digits):
                        if lhv == 0:
                            self.home_square.value += char
                        elif lhv == 1:
                            if self.home_square == self.ans_h:
                                if self.show_24h:
                                    n = int(self.home_square.value + char)
                                    if n > 23:
                                        self.home_square.value = char
                                    else:
                                        self.home_square.value += char
                                else:
                                    n = int(self.home_square.value + char)
                                    if n > 12:
                                        self.home_square.value = char
                                    else:
                                        self.home_square.value += char
                            if self.home_square == self.ans_m:
                                n = int(self.home_square.value + char)
                                if n > 59:
                                    self.home_square.value = char
                                else:
                                    self.home_square.value += char
                        elif lhv == 2:
                            self.home_square.value = char
                    if len(self.ans_h.value.strip()) > 0:
                        if self.home_square == self.ans_h and self.time[0] == int(self.ans_h.value):
                            self.next_field()
                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True
            elif event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and self.board.active_ship == self.ans_h.unit_id:
                if len(self.ans_h.value.strip()) > 0 and self.time[0] == int(self.ans_h.value):
                    self.next_field()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.home_square.update_me = True
                if self.board.active_ship == self.ans_h.unit_id:
                    self.home_square.perm_outline_width = 5
                    self.home_square = self.ans_h
                    self.board.active_ship = self.ans_h.unit_id
                elif self.board.active_ship == self.ans_m.unit_id:
                    self.home_square.perm_outline_width = 5
                    self.home_square = self.ans_m
                    self.board.active_ship = self.ans_m.unit_id
                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True

    def next_field(self):
        self.home_square.update_me = True
        self.home_square.perm_outline_width = 5
        self.home_square = self.ans_m
        self.board.active_ship = self.ans_m.unit_id
        self.home_square.update_me = True
        self.mainloop.redraw_needed[0] = True

    def ai_walk(self):
        if self.home_square.perm_outline_width == 1:
            self.home_square.perm_outline_width = 5
        else:
            self.home_square.perm_outline_width = 1
        self.home_square.update_me = True
        self.mainloop.redraw_needed[0] = True

    def on_btn_click(self, active_id):
        if active_id == 0:
            self.change_time(1, 0)
        elif active_id == 1:
            self.change_time(-1, 0)
        elif active_id == 2:
            self.change_time(0, 1)
        elif active_id == 3:
            self.change_time(0, -1)

    def change_time(self, h, m):
        if h == 1:
            if self.show_24h and self.ans_h.value == "23":
                self.ans_h.value = "00"
            elif not self.show_24h and self.ans_h.value == "12":
                self.ans_h.value = "01"
            else:
                self.ans_h.value = "%02d" % (int(self.ans_h.value) + 1)
        elif h == -1:
            if self.show_24h and int(self.ans_h.value) == 0:
                self.ans_h.value = "23"
            elif not self.show_24h and int(self.ans_h.value) <= 1:
                self.ans_h.value = "12"
            else:
                self.ans_h.value = "%02d" % (int(self.ans_h.value) - 1)
        elif m == 1:
            if self.ans_m.value == "59":
                self.ans_m.value = "00"
            else:
                self.ans_m.value = "%02d" % (int(self.ans_m.value) + 1)
        elif m == -1:
            if int(self.ans_m.value) == 0:
                self.ans_m.value = "59"
            else:
                self.ans_m.value = "%02d" % (int(self.ans_m.value) - 1)

        self.ans_m.update_me = True
        self.ans_h.update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        if not self.correct:
            correct = 0
            if len(self.ans_h.value.strip()) > 0 and self.time[0] == int(self.ans_h.value):
                self.ans_h.set_outline((0, 255, 0), 5)
                self.ans_h.set_display_check(True)
                correct += 1
            else:
                self.ans_h.set_display_check(False)
                self.ans_h.set_outline((255, 0, 0), 5)

            if len(self.ans_m.value.strip()) > 0 and self.time[1] == int(self.ans_m.value):
                self.ans_m.set_outline((0, 255, 0), 5)
                self.ans_m.set_display_check(True)
                correct += 1
            else:
                self.ans_m.set_outline((255, 0, 0), 5)
                self.ans_m.set_display_check(False)

            self.ans_m.update_me = True
            self.ans_h.update_me = True
            self.mainloop.redraw_needed[0] = True

            if correct == 2:
                self.correct = True
                self.ai_enabled = False
                self.level.next_board()
