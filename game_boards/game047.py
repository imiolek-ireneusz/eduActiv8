# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, lvlc[0], lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 6)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = 70
        v = 230
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 40, 230)
        font_color = ex.hsv_to_rgb(h, 255, 140)

        # data = [x_count, y_count, letter_count, ordered]
        data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group, self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group)  # [1, 3, 5, 7, 9, 10]
        """
        if self.level.lvl == 1:
            data = [11, 6, 3, True, 1]
        elif self.level.lvl == 2:
            data = [11, 6, 3, False, 1]
        elif self.level.lvl == 3:
            data = [11, 6, 5, True, 1]
        elif self.level.lvl == 4:
            data = [11, 6, 5, False, 1]
        elif self.level.lvl == 5:
            data = [11, 6, 7, True, 1]
        elif self.level.lvl == 6:
            data = [11, 6, 7, False, 1]
        elif self.level.lvl == 7:
            data = [11, 6, 9, True, 1]
        elif self.level.lvl == 8:
            data = [11, 6, 9, False, 1]
        elif self.level.lvl == 9:
            data = [11, 6, 11, True, 1]
        elif self.level.lvl == 10:
            data = [11, 6, 11, False, 1]
        """

        self.points = (data[2] + 2) // 3 + self.level.lvl // 4

        self.data = data
        self.board.set_animation_constraints(0, data[0], 0, data[1] - 1)
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        if self.mainloop.m.game_variant == 0:
            if self.lang.ltr_text:
                self.alphabet = self.lang.alphabet_lc
            else:
                ts = "".join(self.lang.alphabet_lc)
                ts = ex.unival(ts)
                self.alphabet = ts[::-1]
        elif self.mainloop.m.game_variant == 1:
            self.alphabet = self.lang.alphabet_uc

        self.alph_len = len(self.alphabet)

        self.num_list = []
        self.indexes = []
        self.choice_indexes = [x for x in range(self.alph_len)]

        if data[3] == True:
            choice_list = [x for x in range(self.alph_len - data[2])]
            index = random.randrange(0, len(choice_list))
            n = 0
            for i in range(data[2]):
                self.num_list.append(choice_list[index] + n)
                self.indexes.append(index + n)
                n += 1
        else:
            choice_list = [x for x in range(self.alph_len)]
            for i in range(data[2]):
                index = random.randrange(0, len(choice_list))
                self.num_list.append(choice_list[index])
                self.indexes.append(choice_list[index])
                del (choice_list[index])

        self.indexes.sort()
        shuffled = self.num_list[:]
        random.shuffle(shuffled)

        color = (255, 255, 255)

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]

        # find position of first door square
        x = (data[0] - data[2]) // 2

        # add objects to the board
        for i in range(data[2]):
            self.board.add_door(x + i, 0, 1, 1, classes.board.Door, "", color, "")
            self.board.units[i].door_outline = True
            y = random.randrange(1, 5)
            number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            caption = self.alphabet[shuffled[i]]
            self.board.add_unit(x + i, y, 1, 1, classes.board.Letter, caption, number_color, "", data[4])
            self.board.ships[-1].font_color = font_color
            # self.board.ships[i].highlight = False
            self.board.ships[i].outline_highlight = True
            self.solution_grid[x + i] = 1

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)
        instruction = self.d["Re-arrange alphabetical"]
        self.board.add_unit(0, 5, 11, 1, classes.board.Letter, instruction, color0, "", 7)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.board.ships[-1].speaker_val = self.dp["Re-arrange alphabetical"]
        self.board.ships[-1].speaker_val_update = False
        self.outline_all(0, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

    def update(self, game):
        game.fill((0, 0, 0))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        if self.board.grid[0] == self.solution_grid:
            ships = []

            # collect value and x position on the grid from ships list
            for i in range(self.data[2]):
                ships.append([self.board.ships[i].grid_x, self.board.ships[i].value])
            ships_sorted = sorted(ships)
            correct = True
            for i in range(self.data[2]):
                if i < self.data[2] - 1:
                    if ships_sorted[i][1] != self.alphabet[self.indexes[i]]:
                        correct = False
            if correct == True:
                # self.update_score(self.points)
                self.level.next_board()
            else:
                if self.points > 0:
                    self.points -= 1
                self.level.try_again()
        else:
            self.level.try_again()
