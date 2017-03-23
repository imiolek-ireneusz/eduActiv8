# -*- coding: utf-8 -*-

import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 5, 12)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 6)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = 100  # random.randrange(150, 190, 5)
        v = 255  # random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 40, 230)
        font_color = ex.hsv_to_rgb(h, 255, 140)

        if self.level.lvl == 1:
            data = [11, 6, 3, 9, 2, 1]
        elif self.level.lvl == 2:
            data = [11, 6, 3, 20, 2, 2]
        elif self.level.lvl == 3:
            data = [11, 6, 3, 99, 2, 2]
        elif self.level.lvl == 4:
            data = [11, 6, 5, 9, 3, 1]
        elif self.level.lvl == 5:
            data = [11, 6, 5, 20, 3, 2]
        elif self.level.lvl == 6:
            data = [11, 6, 5, 99, 3, 2]
        elif self.level.lvl == 7:
            data = [11, 6, 7, 9, 4, 1]
        elif self.level.lvl == 8:
            data = [11, 6, 7, 20, 4, 2]
        elif self.level.lvl == 9:
            data = [11, 6, 7, 99, 4, 2]
        elif self.level.lvl == 10:
            data = [11, 6, 9, 9, 5, 1]
        elif self.level.lvl == 11:
            data = [11, 6, 9, 20, 5, 2]
        elif self.level.lvl == 12:
            data = [11, 6, 9, 99, 5, 2]
        self.chapters = [1, 4, 7, 10, 12]
        self.data = data
        self.points = data[4] - 1
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        signs = ["+", " ", "-"]
        self.ship_id = -1
        self.total = 0

        while self.total < 2:
            # get random numbers until sum of all numbers is over 1 (does not prevent negative numbers in mid calculation)
            self.num_list = []
            self.sign_list = []
            expr = []
            choice_list = [x for x in range(1, data[3])]
            for i in range(data[4]):
                index = random.randrange(0, len(choice_list))
                self.num_list.append(choice_list[index])
                expr.append(str(choice_list[index]))
                if i < data[4] - 1:
                    sign_ind = random.randrange(2)
                    if sign_ind == 0:
                        p = 0
                    else:
                        p = 1
                    self.sign_list.append(signs[sign_ind+p])
                    expr.append(str(signs[sign_ind+p]))
            eval_string = ''.join(expr)
            eval_string.strip()
            self.total = eval(eval_string)

        color = ((255, 255, 255))

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]
        self.expression = [" " for x in range(data[0])]

        # find position of first door square
        xd = (data[0] - data[2]) // 2

        # add objects to the board
        h = random.randrange(0, 255, 5)
        number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1

        for i in range(0, data[4]):
            x2 = xd + i * 2 - 1
            caption = str(self.num_list[i])
            self.board.add_unit(x2, 2, 1, 1, classes.board.Label, caption, number_color, "", data[5])
            self.board.units[i].font_color = ex.hsv_to_rgb(h, 255, 140)
            self.solution_grid[x2] = 1
            self.expression[x2] = str(self.num_list[i])
            if i < data[4] - 1:
                self.solution_grid[x2 + 1] = 1
                self.expression[x2 + 1] = self.sign_list[i]

        self.board.add_unit(x2 + 1, 2, 1, 1, classes.board.Label, "=", number_color, "", data[5])
        self.board.units[-1].font_color = ex.hsv_to_rgb(h, 255, 140)
        self.board.add_unit(x2 + 2, 2, 1, 1, classes.board.Label, str(self.total), number_color, "", data[5])
        self.board.units[-1].font_color = ex.hsv_to_rgb(h, 255, 140)
        # signs = ["<","=",">"]*(data[4]-1)

        if h > 125:
            h = random.randrange(0, h - 25, 5)
        else:
            h = random.randrange(h + 25, 255, 5)
        number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1

        indu = len(self.board.units)
        inds = len(self.board.ships)
        for i in range(0, data[4] - 1):
            self.board.add_unit(xd + i * 2 + 1 - 1, 1, 1, 3, classes.board.Letter, signs, number_color, "", data[5])
            self.board.ships[i].font_color = ex.hsv_to_rgb(h, 255, 140)
            self.board.add_door(xd + i * 2 + 1 - 1, 2, 1, 1, classes.board.Door, "", color, "")
            self.board.units[indu + i].door_outline = True
            self.board.ships[inds + i].readable = False
            self.board.all_sprites_list.move_to_front(self.board.units[indu + i])

        instruction = self.d["Drag the slider"]
        self.board.add_unit(0, 5, 11, 1, classes.board.Letter, instruction, color0, "", 7)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color

        self.board.ships[-1].speaker_val = self.dp["Drag the slider"]
        self.board.ships[-1].speaker_val_update = False

        self.outline_all(0, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        err = False
        for i in range(len(self.board.ships) - 1):
            # calculate the active value based on grid_y of the slider
            if self.board.ships[i].grid_y != 1:
                value = self.board.ships[i].value[2 - self.board.ships[i].grid_y]
                self.expression[self.board.ships[i].grid_x] = value
            else:
                err = True
                break

        if err is not True:
            eval_string = ''.join(self.expression)
            eval_string.strip()
            if eval(eval_string) == self.total:  # True:
                # self.update_score(self.points)
                self.level.next_board()
            else:
                if self.points > 0:
                    self.points -= 1
                self.level.try_again()
        else:
            if self.points > 0:
                self.points -= 1
            self.level.try_again()
