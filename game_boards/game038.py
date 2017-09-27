# -*- coding: utf-8 -*-

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
        s = 100  # random.randrange(30, 80)
        v = 255  # random.randrange(200, 255)
        h = random.randrange(0, 225)
        # languages with standard letters in number names
        self.safe_langs = ["en_gb", "en_us", "it", "el", "ru"]
        self.letter_color = ex.hsv_to_rgb(h, s, v)  # [round(each*255) for each in rgb]
        self.letter_color2 = ex.hsv_to_rgb(h, 50, v)
        font_color = ex.hsv_to_rgb(h, s, 140)
        outline_color = ex.hsv_to_rgb(h, s + 50, v - 50)
        frame_color = [255, 255, 255, 0]
        card_color = ex.hsv_to_rgb(h + 10, s - 25, v)

        data = [14, 10]
        # stretch width to fit the screen size
        data[0] = self.get_x_count(data[1], even=True)
        if data[0] < 10:
            data[0] = 10
        self.data = data
        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        image_src = [os.path.join('memory', "n_img%da.png" % i) for i in range(1, 22)]
        self.fish_img_src = [os.path.join('fish', "n%d.png" % i) for i in range(1, 21)]
        self.word_list = [self.lang.n2txt(i) for i in range(1, 21)]
        self.card_fronts = []

        x = (data[0] - 10) // 2
        x2 = x

        y = 0
        for i in range(1, 21):
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, str(i), self.letter_color, "", 2)
            if self.lang.lang == "he":
                sv = self.lang.n2spk(i)
                self.board.ships[-1].speaker_val = sv
                self.board.ships[-1].speaker_val_update = False

            self.board.ships[-1].font_color = font_color
            self.board.ships[i - 1].set_outline(outline_color, 1)
            self.card_fronts.append(classes.board.ImgSurf(self.board, 2, 2, frame_color, image_src[i]))
            x = x2 + i
            if i > 9:
                x = x2 + i - 10
                y = data[1] - 1

        x = (data[0] - 4) // 2
        y = 1

        self.board.add_unit(x - 2, y + 5, 2, 2, classes.board.ImgShip, "1", frame_color, image_src[1])
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.board.ships[-1].set_outline((255, 0, 0), 3)
        # frame size 432 x 288
        self.board.add_unit(x, y + 1, 6, 4, classes.board.ImgShip, "1", frame_color, self.fish_img_src[0], alpha=True)
        self.board.add_unit(x, y + 5, 6, 1, classes.board.Letter, self.word_list[0], frame_color, "", 2)
        self.board.ships[-1].font_color = font_color
        if self.lang.ltr_text:
            sv = "1"
        else:
            sv = self.lang.n2spk(1)

        self.board.ships[-1].speaker_val = sv
        self.board.ships[-1].speaker_val_update = False
        font_size = 15
        if self.lang.has_cursive:
            handwritten = self.word_list[0]
        else:
            handwritten = ""
        if self.lang.lang == "el":
            font_size = 19
        elif self.lang.lang == "ru":
            font_size = 15
        self.board.add_unit(x, y + 6, 6, 1, classes.board.Letter, handwritten, frame_color, "", font_size)
        self.board.ships[-1].font_color = font_color
        if not self.lang.has_cursive:
            self.board.ships[-1].font_color = frame_color
        self.board.ships[-1].speaker_val = sv
        self.board.ships[-1].speaker_val_update = False

        self.board.add_unit(x - 2, y + 1, 2, 4, classes.board.Letter, "1", frame_color, "", 18)
        self.board.ships[-1].font_color = font_color
        self.board.add_door(x - 2, y + 1, 8, 6, classes.board.Door, "", card_color, "")
        self.board.units[0].door_outline = True
        self.board.all_sprites_list.move_to_front(self.board.units[0])
        self.slide = self.board.ships[21]
        self.slide.perm_outline = True

        for each in self.board.ships:
            each.immobilize()

        self.board.ships[20].outline = False
        self.active_item = self.board.ships[0]
        self.active_item.color = (255, 255, 255)
        self.prev_item = self.active_item

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_item = self.board.ships[self.board.active_ship]
            if self.active_item.unit_id < 20:
                if self.prev_item is not None:
                    self.prev_item.color = self.letter_color2
                    self.prev_item.update_me = True
                self.active_item.color = (255, 255, 255)
                self.create_card(self.active_item)
                self.prev_item = self.active_item
                self.mainloop.redraw_needed[0] = True

    def create_card(self, active):
        if self.lang.ltr_text:
            sv = active.value
        else:
            sv = self.lang.n2spk(int(active.value))
        self.board.ships[24].value = active.value
        self.board.ships[24].speaker_val = sv
        self.board.ships[24].speaker_val_update = False
        self.board.ships[20].value = active.value
        self.board.ships[20].img = self.card_fronts[active.unit_id].img.copy()

        self.board.ships[20].speaker_val = sv
        self.board.ships[20].speaker_val_update = False

        self.slide.value = active.value

        self.slide.speaker_val = sv
        self.slide.speaker_val_update = False

        self.board.ships[22].value = self.word_list[active.unit_id]
        self.board.ships[22].speaker_val = sv
        self.board.ships[22].speaker_val_update = False
        if self.lang.has_cursive:
            self.board.ships[23].value = self.word_list[active.unit_id]
        else:
            self.board.ships[23].value = ""
        self.board.ships[23].speaker_val = sv
        self.board.ships[23].speaker_val_update = False
        self.mainloop.redraw_needed[0] = True
        img_src = os.path.join(self.fish_img_src[active.unit_id])
        self.slide.change_image(img_src)
        self.board.active_ship = -1

        self.slide.update_me = True
        self.board.units[0].update_me = True
        for i in [20, 21, 22, 23, 24]:
            self.board.ships[i].update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
