# -*- coding: utf-8 -*-

import random
import sys
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 10, 8)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 15, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        # create non-movable objects
        s = 100
        v = 255
        h = random.randrange(0, 225)

        font_color = ex.hsv_to_rgb(h, 255, 140)
        if self.mainloop.scheme is not None:
            color0 = self.mainloop.scheme.u_color
        else:
            color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        font_color = ex.hsv_to_rgb(h, 255, 140)

        # data = [x_count, y_count, letter_count, top_limit, ordered]
        if self.level.lvl == 1:
            data = [15, 9, 15, 0, 1]
        elif self.level.lvl == 2:
            data = [15, 9, 15, 1, 1]
        elif self.level.lvl == 3:
            data = [15, 9, 15, 2, 1]
        elif self.level.lvl == 4:
            data = [15, 9, 15, 3, 1]
        elif self.level.lvl == 5:
            data = [15, 9, 30, 4, 2]
        elif self.level.lvl == 6:
            data = [15, 9, 30, 5, 2]
        elif self.level.lvl == 7:
            data = [15, 9, 30, 6, 3]
        elif self.level.lvl == 8:
            data = [15, 9, 30, 7, 3]
        letter_table = []
        if self.lang.lang != "lkt":
            letter_table.extend(self.lang.alphabet_lc)
            letter_table.extend(self.lang.alphabet_uc)
            letter_table.extend(self.lang.accents_lc)
            letter_table.extend(self.lang.accents_uc)
        else:
            letter_table = ['a', 'b', 'č', 'e', 'g', 'ǧ', 'h', 'ȟ', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 's', 'š', 't', 'u', 'w', 'y', 'z', 'ž', 'A', 'B', 'Č', 'E', 'G', 'Ǧ', 'H', 'Ȟ', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'S', 'Š', 'T', 'U', 'W', 'Y', 'Z', 'Ž', 'á', 'é', 'í', 'ó', 'ú', 'Á', 'ŋ']

        self.words = self.lang.di[data[3]]
        self.data = data

        self.board.set_animation_constraints(0, data[0], 2, data[1])

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        self.word = self.words[random.randrange(1, self.words[0])]
        if sys.version_info < (3, 0):
            self.wordu = unicode(self.word, "utf-8")
            word_len = len(self.wordu)
            self.word_l = []
            # dirty way of replacing the word with letters from alphabet
            for each in self.wordu:
                for i in range(len(letter_table)):
                    if each == unicode(letter_table[i], "utf-8"):
                        self.word_l.append(letter_table[i])
        else:
            word_len = len(self.word)
            self.word_l = self.word

        self.num_list = []
        if self.lang.lang != "lkt":
            choice_list = self.lang.alphabet_lc + self.lang.alphabet_uc
        else:
            choice_list = ['a', 'b', 'č', 'e', 'g', 'ǧ', 'h', 'ȟ', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 's', 'š', 't', 'u', 'w', 'y', 'z', 'ž', 'A', 'B', 'Č', 'E', 'G', 'Ǧ', 'H', 'Ȟ', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'S', 'Š', 'T', 'U', 'W', 'Y', 'Z', 'Ž']
        for i in range(data[2] - word_len):  # adding noice letters
            index = random.randrange(0, len(choice_list))
            self.num_list.append(choice_list[index])
        shuffled = self.num_list[:]
        for i in range(word_len):
            shuffled.append(self.word_l[i])
        random.shuffle(shuffled)
        color = ((255, 255, 255))

        # create table to store 'binary' solution
        self.solution_grid = [1 for x in range(data[0])]

        x = 0
        y = 4
        for i in range(len(shuffled)):
            if self.mainloop.scheme is not None:
                number_color = self.mainloop.scheme.u_font_color
            else:
                h = random.randrange(0, 255, 5)
                number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            caption = shuffled[i]
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, caption, number_color, "", 1)
            self.board.ships[-1].font_color = ex.hsv_to_rgb(h, 255, 140)
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            x += 1
            if x >= data[0]:
                x = 0
                y += 1

        # find position of first door square
        x = (data[0] - word_len) // 2
        self.left_offset = x

        # add objects to the board
        for i in range(word_len):
            self.board.add_door(x + i, 2, 1, 1, classes.board.Door, "", color, "")
            self.board.units[i].door_outline = True
            self.board.all_sprites_list.move_to_front(self.board.units[i])

        self.board.add_unit(0, 2, x, 1, classes.board.Obstacle, "", color0)
        self.board.add_unit(x + word_len, 2, data[0] - x - word_len, 1, classes.board.Obstacle, "", color0)

        self.board.add_unit(0, 0, data[0], 1, classes.board.Letter,
                            self.d["Build the following word using the letters below."], color0, "", 3)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.board.ships[-1].speaker_val = self.dp["Build the following word using the letters below."]
        self.board.ships[-1].speaker_val_update = False
        self.board.add_unit(0, 1, data[0], 1, classes.board.Letter, self.word, color0, "", 0)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.outline_all(0, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.check_result(auto=True)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check(self):
        if self.board.grid[2] == self.solution_grid:
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 2:
                    self.board.ships[i].update_me = True
                    if self.board.ships[i].value == self.word[self.board.ships[i].grid_x - self.left_offset]:
                        self.board.ships[i].set_display_check(True)
                    else:
                        self.board.ships[i].set_display_check(False)

    def auto_check_reset(self):
        for each in self.board.ships:
            each.update_me = True
            each.set_display_check(None)

    def check_result(self, auto=False):
        result = [" " for i in range(self.data[0])]
        if self.board.grid[2] == self.solution_grid:
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 2:
                    result[self.board.ships[i].grid_x] = self.board.ships[i].value
            result_s = ''.join(result).strip()
            if self.word == result_s:
                self.auto_check()
                self.level.next_board()
            else:
                if auto:
                    self.auto_check()
                else:
                    self.level.try_again()
        else:
            if auto:
                self.auto_check_reset()
            else:
                self.level.try_again()
