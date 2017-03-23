# -*- coding: utf-8 -*-

import math
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
        # create non-movable objects
        self.board.draw_grid = False
        s = random.randrange(30, 80)
        v = random.randrange(200, 255)
        h = random.randrange(0, 225)
        self.letter_color = ex.hsv_to_rgb(h, s, v)
        font_color = ex.hsv_to_rgb(h, s, 75)
        font_colors = ((200, 0, 0), (20, 20, 20))
        outline_color = ex.hsv_to_rgb(h, s + 50, v - 50)

        if self.mainloop.scheme is not None:
            card_color = self.mainloop.scheme.u_color  # (0,0,0)#(255,255,255)#ex.hsv_to_rgb(h+10,s-25,v)
            if self.mainloop.scheme.dark:
                font_colors = ((200, 0, 0), (255, 255, 255))
        else:
            card_color = (255, 230, 255)

        if self.mainloop.m.game_variant == 0:
            phonics_seq = ["/a/", "/ae/", "/air/", "/ar/", "/e/", "/ee/", "/eer/", "/er/", "/i/", "/ie/", "/o/", "/oa/",
                           "/oi/", "/oo/ (short)", "/oo/ (long)", "/ou/", "/or/", "/u/", "/ue/", "/uh/", "/ur/"]
            phonics_words = [
                ["<1>sh<2>ip", "<1>sh<2>oe", "<2>je<3>lly<4>fi<1>sh", "<1>sh<2>rimp", "<1>sh<2>ark", "<1>sh<2>ore"],
                ["chimp", "church"], ["foot", "boot", "food"]]
            phonics_imgs = [
                [("transport", "ship.jpg"), ("clothes_n_accessories", "shoe.jpg"), ("animals", "jellyfish.jpg"),
                 ("animals", "shrimp.jpg"), ("animals", "shark.jpg"), ("nature", "shore.jpg")],
                [("clothes_n_accessories", "shoe.jpg"), ("clothes_n_accessories", "shoe.jpg")],
                [("clothes_n_accessories", "shoe.jpg"), ("clothes_n_accessories", "shoe.jpg"),
                 ("clothes_n_accessories", "shoe.jpg")]]
        elif self.mainloop.m.game_variant == 1:
            phonics_seq = ["/b/", "/c/, /k/", "/ch/", "/d/", "/f/", "/g/", "/h/", "/j/", "/ks/", "/l/", "/m/", "/n/",
                           "/ng/", "/p/", "/r/", "/s/", "/sh/", "/t/", "/th/", "/th/", "/v/", "/w/", "/y/", "/z/",
                           "/gz/", "/zh/"]
            phonics_words = [
                ["<1>sh<2>ip", "<1>sh<2>oe", "<2>je<3>lly<4>fi<1>sh", "<1>sh<2>rimp", "<1>sh<2>ark", "<1>sh<2>ore"],
                ["chimp", "church"], ["foot", "boot", "food"]]
            phonics_imgs = [
                [("transport", "ship.jpg"), ("clothes_n_accessories", "shoe.jpg"), ("animals", "jellyfish.jpg"),
                 ("animals", "shrimp.jpg"), ("animals", "shark.jpg"), ("nature", "shore.jpg")],
                [("clothes_n_accessories", "shoe.jpg"), ("clothes_n_accessories", "shoe.jpg")],
                [("clothes_n_accessories", "shoe.jpg"), ("clothes_n_accessories", "shoe.jpg"),
                 ("clothes_n_accessories", "shoe.jpg")]]

        self.abc_len = len(phonics_seq)
        if self.abc_len < 14:
            h = 13
            dv = 1
        elif self.abc_len < 27:
            h = 13
            dv = 2
        elif self.abc_len < 39:
            h = 13
            dv = 3
        else:
            h = int(math.ceil(self.abc_len / 3.0))
            dv = 3

        data = [16, h]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count < 16:
            data[0] = 16
        else:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        # self.prev_item = None
        # self.base26 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.font_size = 17

        if self.lang.lang == "el":
            self.font_size = 16
        if self.lang.ltr_text:
            x = 0
        else:
            x = data[0] - 3
        y = 0

        for i in range(self.abc_len):
            caption = phonics_seq[i]
            self.board.add_unit(x, y, 3, 1, classes.board.Letter, caption, self.letter_color, "", 2)
            self.board.ships[i].readable = False
            self.board.ships[i].set_outline(outline_color, 1)
            y += 1
            if y >= data[1]:
                if i > 3 * data[1] - 3:
                    if self.lang.ltr_text:
                        x = 4
                    else:
                        x = data[0] - 6
                    y = 0
                else:
                    if self.lang.ltr_text:
                        x = 3
                    else:
                        x = data[0] - 4
                    y = 0
        if self.lang.ltr_text:
            x = (data[0] - 4 + 3 + 3) // 2
        else:
            x = (data[0] - 10) // 2

        y = 1
        ln = len(phonics_words[0])

        max_w = data[0] - (dv * 3 + 3 + 1)
        l = dv * 3 + 1
        if max_w > 7:
            w = 7
            # l = l + (max_w - w) // 2
        else:
            w = max_w
        self.board.add_unit(l, 0, data[0] - l - 1, 1, classes.board.Label, "/sh/", card_color, "", 0)
        for i in range(6):
            if i < ln:
                word = phonics_words[0][i]
                img_src = os.path.join('art4apps', phonics_imgs[0][i][0], phonics_imgs[0][i][1])
            # self.board.add_unit(l,y+i*2,2,2,classes.board.Label,img_src,card_color,"",2)
            self.board.add_unit(l + 2, y + i * 2, w, 2, classes.board.MultiColorLetters, word, card_color, "", 0)
            self.board.ships[-1].align = 1
            self.board.ships[-1].set_font_colors(font_colors[0], font_colors[1])
            self.board.add_unit(l, y + i * 2, 2, 2, classes.board.ImgShip, self.board.ships[-1].value, card_color,
                                img_src)

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
            if self.abc_len > self.board.active_ship > -1:
                self.active_i = self.board.ships[self.board.active_ship]
                if self.active_i.unit_id < self.abc_len:
                    self.active_item = self.active_i
                    if self.prev_item is not None:
                        self.prev_item.color = self.letter_color
                        self.prev_item.update_me = True
                    self.active_item.color = (255, 255, 255)
                    self.create_card(self.active_item)
                    self.active_item.update_me = True
                    self.prev_item = self.active_item
                    self.mainloop.redraw_needed[0] = True
            else:
                if self.prev_item is not None:
                    self.prev_item.color = (255, 255, 255)

    def create_card(self, active):
        # val = ex.unival(active.value)
        # self.board.units[0].update_me = True
        # self.board.active_ship = -1
        self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
