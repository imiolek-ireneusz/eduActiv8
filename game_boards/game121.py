# -*- coding: utf-8 -*-

import os
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.word_lists as wl


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 20, 10)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        color = (234, 218, 225)
        self.color = color
        h = self.mainloop.cl.get_interface_hue()
        arrow_color = ex.hsv_to_rgb(h, 200, 200)

        img_top = 1

        category, self.imgs = wl.word_lists_complete.get(self.mainloop.m.game_variant, ("default", []))

        self.category = category
        self.words = self.d["a4a_%s" % category]
        self.current_image_index = -1
        self.max_image_index = len(self.words) - 1

        l = 100
        self.max_word_len = 35
        while l > self.max_word_len:
            self.w_index = self.current_image_index + 1
            if self.w_index > len(self.words) - 1:
                self.w_index = 0
            self.word = ex.unival(self.words[self.w_index])
            if self.word[0] != "<":
                l = len(self.word)
            else:
                l = 100

            self.current_image_index = self.w_index

        if self.mainloop.lang.lang == "ru":
            self.wordsp = eval("self.dp['a4a_%s']" % category)
            self.wordp = ex.unival(self.wordsp[self.w_index])
        else:
            self.wordp = self.word

        img_src = "%s.webp" % self.imgs[self.w_index]

        w_len = len(self.word)

        self.mainloop.redraw_needed = [True, True, True]

        data = [14, 9]
        img_w_size = 4
        img_h_size = 4

        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count > data[0]:
            data[0] = x_count

        self.data = data

        self.board.set_animation_constraints(0, data[0], 0, data[1])

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        base_len = data[0] - 2
        img_left = (base_len - img_w_size) // 2 + 1

        color_bg = (255, 255, 255)

        l = (data[0] - w_len) // 2
        self.left_offset = l


        self.board.add_unit(img_left, img_top, img_w_size, img_h_size, classes.board.ImgShip, self.wordp, color_bg,
                            os.path.join('art4apps', category, img_src))

        self.picture = self.board.ships[-1]
        self.picture.immobilize()
        self.picture.highlight = False
        self.picture.outline_highlight = False
        self.picture.animable = False
        self.picture.outline = False
        self.picture.is_door = False
        self.picture.speaker_val = self.wordp
        self.picture.speaker_val_update = False

        self.units = []

        label_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_tint_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        bg_img_src_w = os.path.join('unit_bg', "universal_r6x1_bg.png")
        #fg_img_src_w = os.path.join('unit_bg', "universal_r6x1_door.png")

        if self.mainloop.scheme is None:
            dc_img_src_w = os.path.join('unit_bg', "universal_r6x1_dc.png")
        else:
            dc_img_src_w = None

        #self.board.add_unit(1, img_h_size + img_top + 1, data[0] - 2, 1, classes.board.Letter, self.word, letter_bg, "", 0)
        self.board.add_universal_unit(grid_x=img_left - 4, grid_y=data[1] - 3, grid_w=12, grid_h=2, txt=self.word,
                                      alpha=True, fg_img_src=bg_img_src_w, bg_img_src=bg_img_src_w,
                                      dc_img_src=dc_img_src_w, bg_color=(0, 0, 0, 0), border_color=None,
                                      font_color=font_color, bg_tint_color=label_color, fg_tint_color=fg_tint_color,
                                      txt_align=(0, 0), font_type=25, multi_color=False, immobilized=True,
                                      fg_as_hover=False)
        self.label = self.board.ships[-1]
        #self.label.draggable = False
        #self.label.highlight = False
        #self.label.outline_highlight = False
        #self.label.set_outline(color=border_color, width=2)
        #self.label.font_color = font_color
        self.label.readable = True
        self.label.speaker_val = self.wordp
        self.label.speaker_val_update = False

        self.board.add_unit(img_left - 3, 2, 2, 2, classes.board.ImgCenteredShip, "", (0, 0, 0, 0),
                            img_src='nav_l_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)
        self.lt = self.board.ships[-1]

        self.board.add_unit(img_left + 5, 2, 2, 2, classes.board.ImgCenteredShip, "", (0, 0, 0, 0),
                            img_src='nav_r_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)
        self.rt = self.board.ships[-1]

        for each in self.board.ships:
            each.immobilize()

    def next_image(self, direction = 1):
        l = 100
        if direction == 1:
            while l > self.max_word_len:
                self.w_index = self.current_image_index + 1
                if self.w_index > len(self.words) - 1:
                    self.w_index = 0
                self.word = ex.unival(self.words[self.w_index])
                if self.word[0] != "<":
                    l = len(self.word)
                else:
                    l = 100
                self.current_image_index = self.w_index
        else:
            while l > self.max_word_len:
                self.w_index = self.current_image_index - 1
                if self.w_index < 0:
                    self.w_index = len(self.words) - 1
                self.word = ex.unival(self.words[self.w_index])
                if self.word[0] != "<":
                    l = len(self.word)
                else:
                    l = 100
                self.current_image_index = self.w_index

        if self.mainloop.lang.lang == "ru":
            self.wordp = ex.unival(self.wordsp[self.w_index])
        else:
            self.wordp = self.word

        # change image and pronunciation
        img_src = "%s.webp" % self.imgs[self.w_index]
        self.picture.change_image(os.path.join('art4apps', self.category, img_src))
        self.picture.speaker_val = self.wordp
        self.picture.update_me = True

        # change label and pronunciation
        self.label.set_value(self.word)
        self.label.speaker_val = self.wordp
        self.label.update_me = True

        self.mainloop.redraw_needed[0] = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            if self.lt.rect.topleft[0] < pos[0] < self.lt.rect.topleft[0] + self.lt.rect.width and \
                    self.lt.rect.topleft[1] < pos[1] < self.lt.rect.topleft[1] + self.lt.rect.height:
                self.next_image(-1)
            elif self.rt.rect.topleft[0] < pos[0] < self.rt.rect.topleft[0] + self.rt.rect.width and \
                    self.rt.rect.topleft[1] < pos[1] < self.rt.rect.topleft[1] + self.rt.rect.height:
                self.next_image(1)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
