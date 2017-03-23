# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 2, 8)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 26, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        if not self.lang.has_uc:
            self.level.lvl_count = 8

        if self.level.lvl > self.level.lvl_count:
            self.level.lvl = self.level.lvl_count
        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = random.randrange(190, 225)
        v = 255  # random.randrange(230, 255)
        h = random.randrange(0, 255)
        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        font_color = ex.hsv_to_rgb(h, 255, 140)

        self.alphabet_lc = self.lang.alphabet_lc
        self.alphabet_uc = self.lang.alphabet_uc
        self.alphabet_len = len(self.alphabet_lc)

        if self.alphabet_len % 2 == 0:
            self.alphabet_width = self.alphabet_len // 2
            self.last_block = False
        else:
            self.alphabet_width = self.alphabet_len // 2 + 1
            self.last_block = True

        # number of letters to find
        nlf = [0, 0, 0, 0]

        aw = self.alphabet_width

        nlf[1] = aw

        if aw % 2 == 0:
            if (aw // 2) % 2 == 0:
                nlf[0] = aw // 2
            else:
                nlf[0] = aw // 2 + 1
        else:
            if (aw // 2) % 2 == 0:
                nlf[0] = aw // 2 + 1
            else:
                nlf[0] = aw // 2

        nlf[2] = nlf[0] + nlf[1]
        nlf[3] = aw * 2 - 4
        if self.mainloop.m.game_variant == 0:
            if self.level.lvl == 1:
                data = [self.alphabet_width, 6, self.alphabet_lc, 0, nlf[0]]
            elif self.level.lvl == 2:
                data = [self.alphabet_width, 6, self.alphabet_lc, 0, nlf[1]]
            elif self.level.lvl == 3:
                data = [self.alphabet_width, 6, self.alphabet_lc, 0, nlf[2]]
            elif self.level.lvl == 4:
                data = [self.alphabet_width, 6, self.alphabet_lc, 0, nlf[3]]

            elif self.level.lvl == 5:
                data = [self.alphabet_width, 6, self.alphabet_lc, 1, nlf[0]]
            elif self.level.lvl == 6:
                data = [self.alphabet_width, 6, self.alphabet_lc, 1, nlf[1]]
            elif self.level.lvl == 7:
                data = [self.alphabet_width, 6, self.alphabet_lc, 1, nlf[2]]
            elif self.level.lvl == 8:
                data = [self.alphabet_width, 6, self.alphabet_lc, 1, nlf[3]]
        elif self.mainloop.m.game_variant == 1:
            if self.level.lvl == 1:
                data = [self.alphabet_width, 6, self.alphabet_uc, 0, nlf[0]]
            elif self.level.lvl == 2:
                data = [self.alphabet_width, 6, self.alphabet_uc, 0, nlf[1]]
            elif self.level.lvl == 3:
                data = [self.alphabet_width, 6, self.alphabet_uc, 0, nlf[2]]
            elif self.level.lvl == 4:
                data = [self.alphabet_width, 6, self.alphabet_uc, 0, nlf[3]]

            elif self.level.lvl == 5:
                data = [self.alphabet_width, 6, self.alphabet_uc, 1, nlf[0]]
            elif self.level.lvl == 6:
                data = [self.alphabet_width, 6, self.alphabet_uc, 1, nlf[1]]
            elif self.level.lvl == 7:
                data = [self.alphabet_width, 6, self.alphabet_uc, 1, nlf[2]]
            elif self.level.lvl == 8:
                data = [self.alphabet_width, 6, self.alphabet_uc, 1, nlf[3]]

        self.points = data[4] // 5 + (self.level.lvl + 3) // 4

        self.chapters = [1, 4, 8]
        self.data = data
        self.board.set_animation_constraints(0, data[0], 0, data[1] - 1)

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.word = self.data[2][:]
        word_len = self.alphabet_len
        if not self.lang.ltr_text:
            sx = "".join(self.word)
            sx = ex.unival(sx)
            self.word = sx[data[0] - 1:0:-1] + sx[0]
            self.word += sx[word_len:data[0] - 1:-1]
        chosen_indexes = []
        index_list_org = [x for x in range(self.alphabet_len)]
        index_list = [x for x in range(self.alphabet_len)]

        lowered = []
        for i in range(data[4]):  # picking letters to lower
            index = random.randrange(0, len(index_list))
            chosen_indexes.append(index_list[index])
            lowered.append(index_list[index])
            del (index_list[index])
        random.shuffle(lowered)
        color = ((255, 255, 255))

        # create table to store 'binary' solution
        self.solution_grid = [1 for x in range(data[0])]

        x = 0
        y = 0
        if data[4] < data[0]:
            x2 = (data[0] - len(lowered)) // 2
            x3 = 0
        else:
            x2 = 0
            x3 = (data[0] - (len(lowered) - data[0])) // 2  # (word_len-(data[0]-len(lowered)))//2
        y2 = 2
        j = 0
        h_step = 255 // self.alphabet_len
        s = 100
        idx = 0
        for i in range(self.alphabet_len):
            picked = False
            if i in lowered:
                picked = True
            if data[3] == 1:
                s = 100
            else:
                if self.lang.ltr_text:
                    if picked:
                        h = round(h_step * lowered[j])
                    else:
                        h = round(h_step * index_list_org[i])
                else:
                    if picked:
                        h = round(h_step * (self.alphabet_len - lowered[j]))
                    else:
                        h = round(h_step * (self.alphabet_len - index_list_org[i]))

            number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1

            # change y
            if picked:
                if j < data[0]:
                    xj = x2 + j
                else:
                    xj = x3 + j - data[0]
                    y2 = 3
                caption = self.word[lowered[j]]
                self.board.add_unit(xj, y2, 1, 1, classes.board.Letter, caption, number_color, "", 0)
                self.board.add_door(x, y, 1, 1, classes.board.Door, "", color, "")
                self.board.units[j].door_outline = True
                #self.board.ships[i].highlight = False
                self.board.ships[i].outline_highlight = True
                self.board.ships[i].font_color = ex.hsv_to_rgb(h, 255, 140)
                self.board.ships[i].idx = i
                j += 1
            else:
                caption = self.word[i]
                self.board.add_unit(x, y, 1, 1, classes.board.Letter, caption, number_color, "", 0)
                self.board.ships[i].font_color = ex.hsv_to_rgb(h, 255, 140)
                self.board.ships[i].idx = i
                self.board.ships[i].immobilize()
            x += 1
            if x >= data[0]:
                if not self.last_block:
                    x = 0
                else:
                    if self.lang.ltr_text:
                        x = 0
                    else:
                        x = 1
                y = data[1] - 2

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)

        if self.last_block:
            # if odd number of letters - add an empty square at the end
            if self.lang.ltr_text:
                x = data[0] - 1
            else:
                x = 0
            # red
            self.board.add_unit(x, data[1] - 2, 1, 1, classes.board.Label, "", color0, "", 0)

        instruction = self.d["Complete abc"]
        if self.alphabet_len > 30:
            size = 2
        else:
            size = 5
        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, color0, "", size)
        self.board.ships[-1].font_color = font_color
        self.board.ships[-1].immobilize()
        self.board.ships[-1].speaker_val = self.dp["Complete abc"]
        self.board.ships[-1].speaker_val_update = False
        self.outline_all(0, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        result = [" " for i in range(self.alphabet_len)]
        if self.board.grid[0] == self.board.grid[self.data[1] - 2] == self.solution_grid:
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 0:
                    result[self.board.ships[i].grid_x] = self.board.ships[i].value
                    #if self.board.ships[i].grid_x ==
                elif self.board.ships[i].grid_y == self.data[1] - 2:
                    if self.last_block and not self.lang.ltr_text:
                        result[self.data[0] + self.board.ships[i].grid_x - 1] = self.board.ships[i].value
                    else:
                        result[self.data[0] + self.board.ships[i].grid_x] = self.board.ships[i].value

            if ((self.lang.ltr_text and self.word == result) or (
                not self.lang.ltr_text and ex.unival(self.word) == ex.unival("".join(result)))):
                # self.update_score(self.points)
                self.level.next_board()
            else:
                if self.points > 0:
                    self.points -= 1
                self.level.try_again()
        else:
            self.level.try_again()
