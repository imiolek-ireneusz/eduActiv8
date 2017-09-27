# -*- coding: utf-8 -*-

import math
import os
import pygame
import random
import sys

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.board.draw_grid = False
        s = 100
        v = 255
        h = random.randrange(0, 225)
        self.letter_color = ex.hsv_to_rgb(h, s, v)
        self.letter_color2 = ex.hsv_to_rgb(h, 50, v)
        font_color = ex.hsv_to_rgb(h, 255, 140)
        font_color2 = ex.hsv_to_rgb(h, 255, 50)
        outline_color = ex.hsv_to_rgb(h, s + 50, v - 50)

        if self.mainloop.scheme is not None:
            card_color = self.mainloop.scheme.u_color
        else:
            card_color = (255, 255, 255)

        if self.lang.lang == 'fr':
            alc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z']
            uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
        else:

            alc = self.lang.alphabet_lc
            if self.lang.has_uc:
                uc = self.lang.alphabet_uc

        self.abc_len = len(alc)
        h = int(math.ceil(self.abc_len / 3.0))

        data = [16, h]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count < 16:
            data[0] = 16
        else:
            data[0] = x_count

        self.data = data

        self.card_font_size_top = 0
        if self.mainloop.lang.lang == "lkt":
            self.card_font_size_top = 1

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.base26 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.font_size = 17
        self.word_list = self.lang.d['abc_flashcards_word_sequence']
        self.pword_list = self.lang.dp['abc_flashcards_word_sequence']
        self.frame_flow = self.lang.d['abc_flashcards_frame_sequence']
        if self.lang.lang == "el":
            self.font_size = 16
        if self.lang.ltr_text:
            x = 0
        else:
            x = data[0] - 2
        y = 0

        for i in range(self.abc_len):
            if self.lang.has_uc:
                caption = uc[i] + alc[i]
            else:
                caption = alc[i]
            self.board.add_unit(x, y, 2, 1, classes.board.Letter, caption, self.letter_color, "", 3)
            self.board.ships[i].readable = False
            self.board.ships[i].set_outline(outline_color, 1)
            y += 1
            if y >= data[1]:
                if i > 2 * data[1] - 2:
                    if self.lang.ltr_text:
                        x = 4
                    else:
                        x = data[0] - 6
                    y = 0
                else:
                    if self.lang.ltr_text:
                        x = 2
                    else:
                        x = data[0] - 4
                    y = 0
        if self.lang.ltr_text:
            x = (data[0] - 4 + 3 + 3) // 2
        else:
            x = (data[0] - 10) // 2

        if self.lang.has_cursive:
            y = 1
        else:
            y = 2

        # Card
        if self.lang.has_uc:
            w = 8
            xd = 0
        else:
            w = 6
            xd = 1
        if self.lang.has_uc:
            img_plus = 0
            self.board.add_unit(x, y, 2, 1, classes.board.Label, uc[0], card_color, "", self.card_font_size_top)
            if self.lang.has_cursive:
                self.board.add_unit(x - 2, y + 1, 2, 3, classes.board.Label, uc[0], card_color, "", self.font_size)

            self.board.add_unit(x + 2 - xd, y, 2, 1, classes.board.Label, alc[0], card_color, "", self.card_font_size_top)
            if self.lang.has_cursive:
                self.board.add_unit(x + 4 - xd, y + 1, 2, 3, classes.board.Label, alc[0], card_color, "",
                                    self.font_size)
        else:
            img_plus = 1
            if self.lang.has_cursive:
                self.board.add_unit(x + 1 - xd, y, 2, 1, classes.board.Label, alc[0], card_color, "", self.card_font_size_top)
                self.board.add_unit(x + 3 - xd, y, 2, 1, classes.board.Label, alc[0], card_color, "", self.font_size)
            else:
                self.board.add_unit(x + 2 - xd, y, 2, 1, classes.board.Label, alc[0], card_color, "", self.card_font_size_top)

        # frame size 288 x 216
        img_src = os.path.join('fc', "fc%03i.jpg" % self.frame_flow[0])
        self.board.add_unit(x - xd + img_plus, y + 1, 4, 3, classes.board.ImgShip, self.word_list[0], card_color,
                            img_src)
        self.board.ships[-1].speaker_val = self.pword_list[0]
        self.board.ships[-1].speaker_val_update = False

        # TO DO adjust for color schemes
        font_colors = ((200, 0, 0), font_color2)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                font_colors = (self.mainloop.scheme.u_font_color3, self.mainloop.scheme.u_font_color)

        if self.lang.ltr_text:
            self.board.add_unit(x - 2 + xd, y + 4, w, 1, classes.board.MultiColorLetters, self.word_list[0], card_color,
                                "", 2)
            self.board.ships[-1].set_font_colors(font_colors[0], font_colors[1])
        else:
            self.board.add_unit(x - 2 + xd, y + 4, w, 1, classes.board.Letter, self.word_list[0], card_color, "", 2)

        self.board.ships[-1].speaker_val = self.pword_list[0]
        self.board.ships[-1].speaker_val_update = False
        if self.lang.has_cursive:
            if self.lang.ltr_text:
                self.board.add_unit(x - 2 + xd, y + 5, w, 2, classes.board.MultiColorLetters, self.word_list[0],
                                    card_color, "", self.font_size)
                self.board.ships[-1].set_font_colors(font_colors[0], font_colors[1])
            else:
                self.board.add_unit(x - 2 + xd, y + 5, w, 2, classes.board.Letter, self.word_list[0], card_color, "",
                                    self.font_size)
            self.board.ships[-1].speaker_val = self.pword_list[0]
            self.board.ships[-1].speaker_val_update = False
            h = 7
        else:
            h = 5
        self.board.add_door(x - 2 + xd, y, w, h, classes.board.Door, "", card_color, "")
        self.board.units[-1].set_outline(color=outline_color, width=2)
        self.board.all_sprites_list.move_to_front(self.board.units[-1])
        self.slide = self.board.ships[self.abc_len]
        self.slide.perm_outline = True
        for each in self.board.ships:
            each.immobilize()
            each.font_color = font_color
        for each in self.board.units:
            each.font_color = font_color
        self.active_item = self.board.ships[0]
        self.active_item.color = (255, 255, 255)
        self.prev_item = self.active_item

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_item = self.board.ships[self.board.active_ship]
            if self.active_item.unit_id < self.abc_len:
                if self.prev_item is not None:
                    self.prev_item.color = self.letter_color2
                    self.prev_item.update_me = True
                self.active_item.color = (255, 255, 255)
                self.create_card(self.active_item)
                self.prev_item = self.active_item
                self.mainloop.redraw_needed[0] = True

    def create_card(self, active):
        val = ex.unival(active.value)
        if len(val) == 2:
            lcb = 0
            lce = 1
            ucb = 1
            uce = 2
        if len(val) == 4:
            lcb = 0
            lce = 2
            ucb = 2
            uce = 4

        if sys.version_info < (3, 0):
            self.say(val[0].encode("utf-8"))
        else:
            self.say(val[0])
        self.board.units[0].value = val[lcb:lce]
        if self.lang.has_cursive:
            self.board.units[1].value = val[lcb:lce]
        indx = [0, 1]
        if self.lang.has_uc:
            if self.lang.has_cursive:
                indx = [0, 1, 2, 3]
                self.board.units[2].value = val[ucb:uce]
                self.board.units[3].value = val[ucb:uce]
            else:
                self.board.units[1].value = val[ucb:uce]

        self.board.ships[self.abc_len].value = self.word_list[active.unit_id]
        self.board.ships[self.abc_len].speaker_val = self.pword_list[active.unit_id]
        self.board.ships[self.abc_len + 1].set_value(self.word_list[active.unit_id])
        self.board.ships[self.abc_len + 1].speaker_val = self.pword_list[active.unit_id]

        if self.lang.has_cursive:
            indx2 = [self.abc_len, self.abc_len + 1, self.abc_len + 2]
            self.board.ships[self.abc_len + 2].set_value(self.word_list[active.unit_id])
            self.board.ships[self.abc_len + 2].speaker_val = self.pword_list[active.unit_id]
        else:
            indx2 = [self.abc_len, self.abc_len + 1]
        img_src = os.path.join('fc', "fc%03i.jpg" % self.frame_flow[active.unit_id])
        self.slide.change_image(img_src)
        self.board.active_ship = -1
        self.slide.update_me = True
        for i in indx:
            self.board.units[i].update_me = True
        for i in indx2:
            self.board.ships[i].update_me = True
        self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
