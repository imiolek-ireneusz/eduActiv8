# -*- coding: utf-8 -*-

import random
import os
import sys
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 15, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        h = random.randrange(0, 225)
        h_init = h
        self.auto = False

        caption_font_color = ex.hsv_to_rgb(h, 255, 140)

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

        self.unit_mouse_over = None
        self.units = []

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

        # create table to store 'binary' solution
        self.solution_grid = [1 for x in range(data[0])]

        x = 0
        y = 4
        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")

        for i in range(len(shuffled)):
            h = random.randrange(0, 255, 5)
            caption = shuffled[i]

            number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
            font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
            fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=bg_img_src,
                                          bg_img_src=bg_img_src,
                                          dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=font_color,
                                          bg_tint_color=number_color,
                                          fg_tint_color=fg_number_color,
                                          txt_align=(0, 0), font_type=data[4], multi_color=False, alpha=True,
                                          immobilized=False, fg_as_hover=True)
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            self.units.append(self.board.ships[-1])
            x += 1
            if x >= data[0]:
                x = 0
                y += 1

        # find position of first door square
        x = (data[0] - word_len) // 2
        self.left_offset = x
        label_bg_color = (255, 255, 255)
        door_bg_tint = ex.hsv_to_rgb(h_init, self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
        if self.mainloop.scheme is None:
            bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        else:
            bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
            if self.mainloop.scheme.dark:
                bg_img_src = os.path.join('unit_bg', "universal_sq_door_no_trans.png")
                label_bg_color = (0, 0, 0)

        # add objects to the board
        for i in range(word_len):
            # add new door
            self.board.add_universal_unit(grid_x=x + i, grid_y=2, grid_w=1, grid_h=1, txt=None,
                                          fg_img_src=None,
                                          bg_img_src=bg_img_src,
                                          dc_img_src=None,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=None,
                                          bg_tint_color=door_bg_tint,
                                          fg_tint_color=None,
                                          txt_align=(0, 0), font_type=10, multi_color=False, alpha=True,
                                          immobilized=True, mode=2)
            self.board.all_sprites_list.move_to_front(self.board.units[i])

        self.board.add_unit(0, 2, x, 1, classes.board.Obstacle, "", label_bg_color)
        self.board.add_unit(x + word_len, 2, data[0] - x - word_len, 1, classes.board.Obstacle, "", label_bg_color)

        self.board.add_unit(0, 0, data[0], 1, classes.board.Letter,
                            self.d["Build the following word using the letters below."], label_bg_color, "", 3)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = caption_font_color
        self.board.ships[-1].speaker_val = self.dp["Build the following word using the letters below."]
        self.board.ships[-1].speaker_val_update = False
        self.board.add_unit(0, 1, data[0], 1, classes.board.Letter, self.word, label_bg_color, "", 0)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = caption_font_color

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.auto = True
            self.check_result()

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def auto_check(self):
        if self.board.grid[2] == self.solution_grid:
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 2:
                    self.board.ships[i].update_me = True
                    if ex.unival(self.board.ships[i].value) == ex.unival(self.word_l[self.board.ships[i].grid_x - self.left_offset]):
                        self.board.ships[i].set_display_check(True)
                    else:
                        self.board.ships[i].set_display_check(False)

    def auto_check_reset(self):
        for each in self.board.ships:
            each.update_me = True
            each.set_display_check(None)
        self.auto = False

    def check_result(self):
        result = [" " for i in range(self.data[0])]
        if self.board.grid[2] == self.solution_grid:
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 2:
                    result[self.board.ships[i].grid_x] = self.board.ships[i].value
            result_s = ''.join(result).strip()
            if ex.unival(self.word) == ex.unival(result_s):
                self.auto_check()
                self.level.next_board()
            else:
                if self.auto:
                    self.auto_check()
                else:
                    self.level.try_again()
        else:
            if self.auto:
                self.auto_check_reset()
            else:
                self.level.try_again()
