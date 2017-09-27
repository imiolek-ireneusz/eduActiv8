# -*- coding: utf-8 -*-

# English Only Game

import os
import pygame
import random

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
        card_color = ex.hsv_to_rgb(h + 10, s - 25, v)

        data = [14, 10]
        # stretch width to fit the screen size
        data[0] = self.get_x_count(data[1], even=True)
        if data[0] < 14:
            data[0] = 14
        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.word_list = ['<1>A<2>nt', '<1>B<2>oat', '<1>C<2>at', '<1>D<2>uck', '<1>E<2>l<1>e<2>phant', '<1>F<2>ish',
                          '<1>G<2>rapes', '<1>H<2>ouse', '<1>I<2>gloo', '<1>J<2>ar', '<1>K<2>ey', '<1>L<2>ion',
                          '<1>M<2>ouse', '<1>N<2>otebook', '<1>O<2>wl', '<1>P<2>arrot', '<1>Q<2>ueen', '<1>R<2>abbit',
                          '<1>S<2>un', '<1>T<2>eapo<1>t', '<1>U<2>mbrella', '<1>V<2>iolin', '<1>W<2>indo<1>w',
                          '<1>X<2>ylophone', '<1>Y<2>arn', '<1>Z<2>ebra']

        self.pword_list = ['Ant', 'Boat', 'Cat', 'Duck', 'Elephant', 'Fish', 'Grapes', 'House', 'Igloo', 'Jar', 'Key',
                          'Lion', 'Mouse', 'Notebook', 'Owl', 'Parrot', 'Queen', 'Rabbit', 'Sun', 'Teapot', 'Umbrella',
                          'Violin', 'Window', 'Xylophone', 'Yarn', 'Zebra']

        self.frame_flow = [i for i in range(26)]
        if data[0] > 26:
            x = (data[0] - 26) // 2
        else:
            x = 0
        x2 = (data[0] - (26 - data[0])) // 2
        y = 0

        for i in range(26):
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, chr(i + 65) + chr(i + 97), self.letter_color, "", 2)
            self.board.ships[i].readable = False
            self.board.ships[i].set_outline(outline_color, 1)
            x += 1
            if x >= data[0]:
                x = x2
                y = data[1] - 1

        x = (data[0] - 4) // 2
        y = 1

        font_colors = ((200, 0, 0), font_color2)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                font_colors = (self.mainloop.scheme.u_font_color3, self.mainloop.scheme.u_font_color)

        # Card
        self.board.add_unit(x, y + 1, 2, 1, classes.board.Label, "A", card_color, "", 0)
        self.board.add_unit(x + 2, y + 1, 2, 1, classes.board.Label, "a", card_color, "", 0)
        self.board.add_unit(x - 2, y + 1, 2, 4, classes.board.Label, "A", card_color, "", 18)

        self.board.add_unit(x + 4, y + 1, 2, 4, classes.board.Label, "a", card_color, "", 18)
        img_src = os.path.join('fc', "fc%03i.jpg" % self.frame_flow[0])
        self.board.add_unit(x, y + 2, 4, 3, classes.board.ImgShip, self.word_list[0], card_color, img_src)

        self.board.add_unit(x - 2, y + 5, 8, 1, classes.board.MultiColorLetters, self.word_list[0], card_color, "", 2)
        self.board.ships[-1].set_font_colors(font_colors[0], font_colors[1])

        self.board.ships[-1].speaker_val = self.pword_list[0]
        self.board.ships[-1].speaker_val_update = False

        self.board.add_unit(x - 2, y + 6, 8, 1, classes.board.MultiColorLetters, self.word_list[0], card_color, "", 15)
        self.board.ships[-1].set_font_colors(font_colors[0], font_colors[1])

        self.board.ships[-1].speaker_val = self.pword_list[0]
        self.board.ships[-1].speaker_val_update = False

        self.board.add_door(x - 2, y + 1, 8, 6, classes.board.Door, "", card_color, "")
        self.board.units[4].set_outline(color=outline_color, width=2)
        self.board.all_sprites_list.move_to_front(self.board.units[4])
        self.slide = self.board.ships[26]
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
            if self.active_item.unit_id < 26:
                if self.prev_item is not None:
                    self.prev_item.color = self.letter_color2
                    self.prev_item.update_me = True
                self.active_item.color = (255, 255, 255)
                self.create_card(self.active_item)
                self.prev_item = self.active_item
                self.mainloop.redraw_needed[0] = True

    def create_card(self, active):
        self.say(active.value[0])
        self.board.units[0].value = active.value[0]
        self.board.units[1].value = active.value[1]
        self.board.units[2].value = active.value[0]
        self.board.units[3].value = active.value[1]
        self.board.ships[26].set_value(self.word_list[active.unit_id])
        self.board.ships[27].set_value(self.word_list[active.unit_id])
        self.board.ships[28].set_value(self.word_list[active.unit_id])
        self.board.ships[26].speaker_val = self.pword_list[active.unit_id]
        self.board.ships[27].speaker_val = self.pword_list[active.unit_id]
        self.board.ships[28].speaker_val = self.pword_list[active.unit_id]
        self.mainloop.redraw_needed[0] = True

        img_src = os.path.join('fc', "fc%03i.jpg" % self.frame_flow[active.unit_id])
        self.slide.change_image(img_src)

        self.board.active_ship = -1
        self.slide.update_me = True
        for i in [0, 1, 2, 3]:
            self.board.units[i].update_me = True
        for i in [26, 27, 28]:
            self.board.ships[i].update_me = True
        self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
