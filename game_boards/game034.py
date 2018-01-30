# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 36, 5)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 23, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.board.decolorable = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        if self.mainloop.scheme is None:
            s = 100
            v = 255
            h = random.randrange(0, 255, 5)
            color0 = ex.hsv_to_rgb(h, 40, 255)  # highlight 1
            color1 = ex.hsv_to_rgb(h, 70, v)  # highlight 2
            color2 = ex.hsv_to_rgb(h, s, v)  # normal color
            color3 = ex.hsv_to_rgb(h, 230, 100)
            task_bg_color = (255, 255, 255)
            font_color = ex.hsv_to_rgb(h, 255, 140)
            task_font_color = (0, 0, 0)
        else:
            s = 150
            v = 225
            h = 170
            color0 = ex.hsv_to_rgb(h, 40, 255)  # highlight 1
            color1 = ex.hsv_to_rgb(h, 70, v)  # highlight 2
            color2 = ex.hsv_to_rgb(h, s, v)  # normal color
            color3 = ex.hsv_to_rgb(h, 230, 100)
            task_bg_color = self.mainloop.scheme.u_color
            task_font_color = self.mainloop.scheme.u_font_color
            font_color = self.mainloop.scheme.u_font_color
        white = (255, 255, 255)

        # data = [x_count, y_count, range_from, range_to, max_sum_range, image]
        if self.level.lvl == 1:
            data = [23, 9]
        elif self.level.lvl == 2:
            data = [23, 9]
            color1 = color0
        elif self.level.lvl == 3:
            data = [23, 9]
            color1 = color2 = color0
        elif self.level.lvl == 4:
            data = [23, 9]
            color1 = color2 = color0
        elif self.level.lvl == 5:
            data = [23, 9]
            color2 = color1 = color0 = font_color
            color3 = (40, 40, 40)
        self.data = data
        self.board.set_animation_constraints(10, data[0], 0, data[1])

        self.board.level_start(data[0], data[1], self.layout.scale)

        num1 = random.randrange(1, 10)
        num2 = random.randrange(1, 10)
        self.solution = [num1, num2, num1 * num2]
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        unique = set()
        for i in range(1, 10):
            for j in range(1, 10):
                if i == num1 and j == num2:
                    color = color0
                elif i == num1 or j == num2:
                    color = color1
                elif self.level.lvl == 2 and (i == num2 or j == num1):
                    color = color1
                else:
                    color = color2
                mul = i * j
                unique.add(mul)
                caption = str(mul)
                self.board.add_unit(i - 1, j - 1, 1, 1, classes.board.Label, caption, color, "", 2)
                self.board.units[-1].font_color = font_color
        self.board.add_unit(9, 0, 1, 9, classes.board.Obstacle, "", color3)
        unique = sorted(unique)
        # draw outline with selectable numbers
        self.multi = dict()
        if self.mainloop.scheme is None:
            s = 140
        else:
            s = 80
        v = 255
        h = 7

        x = 11
        y = 0
        for i in range(9):
            x += 1
            color = ex.hsv_to_rgb(h * i, s, v)
            self.multi[str(unique[i])] = i
            caption = str(unique[i])
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, caption, color, "", 2)
            self.board.ships[-1].font_color = ex.hsv_to_rgb(h * i, 255, 140)
            self.board.ships[-1].audible = False
            if self.lang.lang == "he":
                sv = self.lang.n2spk(unique[i])
                self.board.ships[-1].speaker_val = sv
                self.board.ships[-1].speaker_val_update = False
        x = 14
        y = 4
        captions = [str(num1), chr(215), "=", str(num1 * num2)]
        if self.level.lvl < 4:
            color = self.board.ships[self.solution[1] - 1].initcolor
        else:
            color = (255, 255, 255)
        for i in range(4):
            if i == 2:
                x += 1
            self.board.add_unit(x + i, y, 1, 1, classes.board.Label, captions[i], color, "", 2)
            if self.level.lvl < 4:
                self.board.units[-1].font_color = self.board.ships[self.solution[1] - 1].font_color

        self.outline_all(0, 1)

        self.board.add_door(16, y, 1, 1, classes.board.Door, "", task_bg_color, "", font_size=2)
        self.home_square = self.board.units[86]
        self.home_square.checkable = True
        self.home_square.init_check_images()
        self.home_square.door_outline = True
        if self.level.lvl < 4:
            self.home_square.font_color = self.board.ships[self.solution[1] - 1].font_color
        else:
            self.home_square.font_color = task_font_color
        self.board.all_sprites_list.move_to_front(self.home_square)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.show_msg == False:
            if event.type == pygame.KEYDOWN and (event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER):
                lhv = len(self.home_square.value)
                self.changed_since_check = True
                if event.key == pygame.K_BACKSPACE:
                    if lhv > 0:
                        self.home_square.value = self.home_square.value[0:lhv - 1]
                elif not self.board.grid[4][16]:
                    char = event.unicode
                    if len(char) > 0 and char in self.digits:
                        self.home_square.value = char
                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True
            elif event.type == pygame.MOUSEMOTION and self.drag:
                if self.board.grid[4][16]:
                    self.home_square.value = ""
                    self.home_square.update_me = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for each in self.board.units:
                    if each.is_door is True:
                        self.board.all_sprites_list.move_to_front(each)
                if self.board.grid[4][16]:
                    self.home_square.value = ""
                    self.home_square.update_me = True
                    self.check_result()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                self.check_result()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.auto_check_reset()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check_reset(self):
        self.home_square.set_display_check(None)

    def check_result(self):
        if self.board.grid[4][16]:
            sol = self.board.ships[self.solution[1] - 1]
            if sol.grid_x == 16 and sol.grid_y == 4:
                self.passed()
                self.home_square.set_display_check(True)
            else:
                self.home_square.set_display_check(False)
        else:
            if self.home_square.value != "" and (int(self.home_square.value) == self.solution[1]):
                self.passed()
                self.home_square.set_display_check(True)
            else:
                self.home_square.set_display_check(False)
        self.mainloop.redraw_needed[0] = True

    def passed(self):
        self.level.next_board(self.d["Perfect!"])

