# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 14)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.decolorable = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.board.draw_grid = False
        s = 100
        v = 255
        h = random.randrange(0, 255, 5)
        white = (255, 255, 255)
        if self.mainloop.scheme is None:
            color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
            instr_font_col = ex.hsv_to_rgb(h, 255, 140)
            font_col = (0, 0, 0)
        else:
            font_col = self.mainloop.scheme.u_font_color
            if self.mainloop.scheme.dark:
                white = (0, 0, 0)
                color0 = (0, 0, 10)
            else:
                color0 = (254, 254, 255)
            instr_font_col = font_col
        # setting level variable
        # data = [x_count, y_count, number_count, top_limit, ordered]
        if self.level.lvl == 1:
            data = [13, 9, 5, 3, 2]
        elif self.level.lvl == 2:
            data = [13, 9, 8, 3, 3]
        elif self.level.lvl == 3:
            data = [12, 9, 7, 4, 2]
        elif self.level.lvl == 4:
            data = [12, 9, 11, 4, 3]
        elif self.level.lvl == 5:
            data = [12, 9, 15, 4, 4]
        elif self.level.lvl == 6:
            data = [13, 9, 9, 5, 2]
        elif self.level.lvl == 7:
            data = [13, 9, 14, 5, 3]
        elif self.level.lvl == 8:
            data = [13, 9, 19, 5, 4]
        elif self.level.lvl == 9:
            data = [13, 9, 24, 5, 5]
        elif self.level.lvl == 10:
            data = [12, 9, 11, 6, 2]
        elif self.level.lvl == 11:
            data = [12, 9, 17, 6, 3]
        elif self.level.lvl == 12:
            data = [12, 9, 23, 6, 4]
        elif self.level.lvl == 13:
            data = [12, 9, 29, 6, 5]
        elif self.level.lvl == 14:
            data = [12, 9, 35, 6, 6]

        self.chapters = [1, 3, 6, 10, 14]
        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            data[0] = self.get_x_count(data[1], even=True)
        else:
            data[0] = self.get_x_count(data[1], even=False)

        self.data = data
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.choice_list = [x for x in range(1, data[2] + 1)]
        self.shuffled = self.choice_list[:]
        random.shuffle(self.shuffled)
        """
        If the grid size is odd, then the number of inversions in a solvable situation are even.
        If the grid size is even, and the blank is on an odd row (first, third etc), then the number of inversions in a solvable situation are odd.
        If the grid size is even, and the blank is on an even row (second, fourth etc), then the number of inversions in a solvable situation are even. 
        """
        inversions = ex.inversions(self.shuffled)
        if inversions % 2 != 0:  # if number of inversions is odd it is unsolvable
            # in unsolvable combinations swapping 2 squares will make it solvable
            temp = self.shuffled[0]
            self.shuffled[0] = self.shuffled[1]
            self.shuffled[1] = temp

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4] - 1  # height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3]) // 2  # side margin width
        self.check = [h1, h2, w2]

        self.board.add_door(w2, h1, data[3], data[4], classes.board.Door, "", white, "")
        # create table to store 'binary' solution
        # find position of first door square
        x = w2
        y = h1
        self.mini_grid = []
        # add objects to the board
        line = []
        h_start = random.randrange(0, 155, 5)
        h_step = 100 // (data[2])
        for i in range(data[2]):
            if self.mainloop.scheme is None:
                h = (h_start + (self.shuffled[i] - 1) * h_step)
                number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            else:
                number_color = color0
            caption = str(self.shuffled[i])
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, caption, number_color, "", 2)

            self.board.ships[-1].readable = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            if self.mainloop.scheme is None:
                self.board.ships[-1].font_color = ex.hsv_to_rgb(h, 255, 140)
            else:
                self.board.ships[-1].font_color = font_col

            line.append(i)
            x += 1
            if x >= w2 + data[3] or i == data[2] - 1:
                x = w2
                y += 1
                self.mini_grid.append(line)
                line = []
        if self.mainloop.scheme is not None:
            self.outline_all(font_col, 1)
        instruction = self.d["Re-arrange right"]
        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, color0, "", 5)  # bottom 2
        self.board.ships[-1].font_color = instr_font_col
        self.board.ships[-1].immobilize()

        self.board.ships[-1].speaker_val = self.dp["Re-arrange right"]
        self.board.ships[-1].speaker_val_update = False
        if self.mainloop.scheme is None:
            self.outline_all(0, 1)
        # horizontal
        self.board.add_unit(0, 0, data[0], h1, classes.board.Obstacle, "", white, "", 7)  # top
        self.board.add_unit(0, h1 + data[4], data[0], h2, classes.board.Obstacle, "", white, "", 7)  # bottom 1
        # side obstacles
        self.board.add_unit(0, h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # left
        self.board.add_unit(w2 + data[3], h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # right

        self.board.all_sprites_list.move_to_front(self.board.units[0])

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        current = [x for x in range(self.data[2] + 1)]  # self.choice_list[:]
        # collect value and x position on the grid from ships list
        for i in range(len(self.board.ships) - 1):
            x = self.board.ships[i].grid_x - self.check[2]
            y = self.board.ships[i].grid_y - self.check[0]
            w = self.data[3]
            pos = x + (y * w)
            current[pos] = int(self.board.ships[i].value)
            if pos < self.data[2]:
                if self.choice_list[pos] == current[pos]:
                    self.board.ships[i].set_display_check(True)
                else:
                    self.board.ships[i].set_display_check(False)
            else:
                self.board.ships[i].set_display_check(False)

        del (current[-1])
        if self.choice_list == current:
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True


"""
If the grid size is odd, then the number of inversions in a solvable situation are even.
If the grid size is even, and the blank is on an odd row (first, third etc), then the number of inversions in a solvable situation are odd.
If the grid size is even, and the blank is on an even row (second, fourth etc), then the number of inversions in a solvable situation are even. 

Consider the following configuration in the 3 x 2 case:

4 5
1 3 2

The equivalent permutation is 4, 5, 1, 3, 2. 
The number of inversions is 3 + 3 + 1 = 7. n = 3, so n is odd. 
Therefore, the number of inversions in a legal configuration must be even. 
It's not, so this configuration is illegal.

Here's another example. Considering the following 4 x 2 case:
	
  7 2 1
4 6 3 5

The equivalent permutation is 7, 2, 1, 4, 6, 3, 5. 
The number of inversions is 6 + 1 + 1 + 2 = 10. 
In this case, n = 4, so n is even. m = 2 and i = 1, 
so m - i is odd and we are in case 1.1c of the proof -> 
the number of inversions must be odd. 
They are not, so this configuration is illegal.
"""
