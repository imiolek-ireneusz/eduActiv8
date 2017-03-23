# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 16)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 18, 9)

    def create_game_objects(self, level=1):
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.board.decolorable = False

        white = (255, 255, 255)

        numbero = 5
        if self.level.lvl == 1:
            numbero = 6
        elif self.level.lvl == 2:
            numbero = 7
        elif self.level.lvl == 3:
            numbero = 8
        elif self.level.lvl == 4:
            numbero = 9
        elif self.level.lvl == 5:
            numbero = 10
        elif self.level.lvl == 6:
            numbero = 11
        elif self.level.lvl == 7:
            numbero = 12
        elif self.level.lvl == 8:
            numbero = 13
        elif self.level.lvl == 9:
            numbero = 14
        elif self.level.lvl == 10:
            numbero = 15
        elif self.level.lvl == 11:
            numbero = 16
        elif self.level.lvl == 12:
            numbero = 17
        elif self.level.lvl == 13:
            numbero = 18
        elif self.level.lvl == 14:
            numbero = 19
        elif self.level.lvl == 15:
            numbero = 20
        elif self.level.lvl == 16:
            numbero = 21
        self.points = 1
        self.bonus = numbero + numbero
        data = [numbero * 2, numbero]
        self.data = data
        self.layout.update_layout(data[0], data[1])

        self.board.level_start(data[0], data[1], self.layout.scale)
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.number_hat = []
        for i in range(1, data[0] + 1, 2):
            for j in range(1, data[1] + 1):
                mul = ((i + 1) // 2) * j
                if i == 1 or j == 1:
                    if i == 1 and j == 1:
                        caption = "+"
                        fs = 0
                    else:
                        fs = 1
                        caption = str(mul - 1)
                else:
                    fs = 1
                    caption = ""
                    key = "%02d%02d" % ((i + 1) // 2, j)
                    self.number_hat.append(key)
                self.board.add_unit(i - 1, j - 1, 2, 1, classes.board.Label, caption, white, "", fs)
        self.next_number()
        self.outline_all(0, 1)
        self.level.game_step = 0
        self.level.games_per_lvl = len(self.number_hat) + 1

    def next_number(self):
        if self.mainloop.scheme is None:
            s = random.randrange(150, 225, 5)
            v = random.randrange(190, 225, 5)
            h = random.randrange(0, 255, 5)
            color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
            color1 = ex.hsv_to_rgb(h, 70, v)  # highlight 2
            color2 = ex.hsv_to_rgb(h, s, v)  # normal color
            color3 = ex.hsv_to_rgb(h, 230, 100)
        else:
            s = 200  # random.randrange(150, 225, 5)
            v = 200  # random.randrange(190, 225, 5)
            h = 170  # random.randrange(0, 255, 5)
            color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
            color1 = ex.hsv_to_rgb(h, 70, v)  # highlight 2
            color2 = ex.hsv_to_rgb(h, s, v)  # normal color
            color3 = (0, 0, 0)  # ex.hsv_to_rgb(h,230,100)

        self.points = 1
        ln = len(self.number_hat)
        if ln > 0:
            index = random.randrange(0, ln)
            choice = self.number_hat[index]
            del (self.number_hat[index])
            num1 = int(choice[0:2])
            num2 = int(choice[2:])
            self.solution = [num1, num2, num1 - 1 + num2 - 1]
            for i in range(1, self.data[0] + 1, 2):
                for j in range(1, self.data[1] + 1):
                    unit_id = self.board.get_unit_id(i - 1, j - 1)
                    if (i + 1) // 2 == num1 and j == num2:
                        color = color0
                        self.board.units[unit_id].font_color = color3
                    elif (i + 1) // 2 == num1 or j == num2:
                        color = color1
                        self.board.units[unit_id].font_color = color1
                    elif (i + 1) // 2 == num2 and j == num1:  # ?
                        color = color2
                        self.board.units[unit_id].font_color = color2
                    else:
                        color = color2
                        self.board.units[unit_id].font_color = color1
                    mul = ((i + 1) // 2) + j
                    if i == 1 or j == 1:
                        if (i + 1) // 2 == num1 or j == num2:
                            self.board.units[unit_id].font_color = color3  # !
                        else:
                            self.board.units[unit_id].font_color = color1
                    else:
                        caption = ""

                    self.board.units[unit_id].color = color
                    self.board.units[unit_id].update_me = True
            self.board.units[0].font_color = color3
            self.outline_all(0, 1)

            self.home_square = self.board.units[(num1 - 1) * self.data[1] + num2 - 1]

            self.mainloop.redraw_needed[0] = True
        else:
            # self.update_score(self.bonus)
            self.level.next_board()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.show_msg == False:
            if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                lhv = len(self.home_square.value)
                self.changed_since_check = True
                if event.key == pygame.K_BACKSPACE:
                    if lhv > 0:
                        self.home_square.value = self.home_square.value[0:lhv - 1]
                else:  # if not self.board.grid[4][18]:
                    char = event.unicode
                    if char in self.digits:
                        if len(char) > 0 and lhv < 3:
                            self.home_square.value += char
                        else:
                            self.home_square.value = char
                self.home_square.update_me = True
                self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        if self.changed_since_check:
            if self.home_square.value != "" and (int(self.home_square.value) == self.solution[2]):
                # self.update_score(self.points)
                self.quick_passed()

            else:
                if self.bonus > 0:
                    self.bonus -= 1
                if self.points > 0:
                    self.points = 0
                self.failed()

    def passed(self):
        self.level.next_board(tts)

    def quick_passed(self):
        self.level.game_step += 1
        self.next_number()

    def failed(self):
        self.level.try_again()
        self.changed_since_check = False
        self.home_square.value = ""
        self.home_square.update_me = True
        self.mainloop.redraw_needed[0] = True
