# -*- coding: utf-8 -*-

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
        s = 100  # random.randrange(30, 80)
        v = 255  # random.randrange(200, 255)
        h = random.randrange(0, 225)
        # languages with standard letters in number names
        self.safe_langs = ["en_gb", "en_us", "it", "el", "ru"]
        self.letter_color = ex.hsv_to_rgb(h, s, v)  # [round(each*255) for each in rgb]
        self.letter_color2 = ex.hsv_to_rgb(h, 50, v)

        card_font_color = ex.hsv_to_rgb(h, 255, 140)

        arrow_color = ex.hsv_to_rgb(h, 200, 200)
        outline_color = ex.hsv_to_rgb(h, s + 50, v - 50)
        outline_color2 = (255, 102, 0)
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

        self.unit_mouse_over = None
        self.units = []

        image_src = [os.path.join('memory', "n_img%da.png" % i) for i in range(1, 22)]
        self.fish_img_src = [os.path.join('fish', "n%d.png" % i) for i in range(1, 21)]
        self.word_list = [self.lang.n2txt(i) for i in range(1, 21)]
        self.card_fronts = []

        label_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_tint_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        self.bg_color_active = ex.hsv_to_rgb(h, 200, 255)
        self.bg_color_done = ex.hsv_to_rgb(h, 50, 255)

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None
            if self.mainloop.scheme.dark:
                self.bg_color_active = ex.hsv_to_rgb(h, 255, 200)
                self.bg_color_done = ex.hsv_to_rgb(h, 255, 55)

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")

        x = (data[0] - 10) // 2
        x2 = x
        y = 0
        for i in range(1, 21):
            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=str(i),
                                          fg_img_src=bg_img_src,
                                          bg_img_src=bg_img_src,
                                          dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=font_color,
                                          bg_tint_color=label_color,
                                          fg_tint_color=fg_tint_color,
                                          txt_align=(0, 0), font_type=1, multi_color=False, alpha=True,
                                          immobilized=True,
                                          fg_as_hover=True)
            self.units.append(self.board.ships[-1])

            if self.lang.lang == "he":
                sv = self.lang.n2spk(i)
                self.board.ships[-1].speaker_val = sv
                self.board.ships[-1].speaker_val_update = False

            self.board.ships[-1].font_color = card_font_color
            self.board.ships[-1].readable = False
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
                self.board.ships[-1].set_outline(outline_color2, 2)
        # frame size 432 x 288
        self.board.add_unit(x, y + 1, 6, 4, classes.board.ImgShip, "1", frame_color, self.fish_img_src[0], alpha=True)
        self.board.ships[-1].set_outline(outline_color2, 2)

        hand_y_offset = 0
        n2txt_font_size = 2
        if self.lang.lang == "ar":
            hand_y_offset = 1
            n2txt_font_size = 31

        self.board.add_unit(x, y + 5, 6, 1 + hand_y_offset, classes.board.Letter, self.word_list[0], frame_color, "",
                            n2txt_font_size)
        self.board.ships[-1].font_color = card_font_color
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
        self.board.add_unit(x, y + 6 + hand_y_offset, 6, 1, classes.board.Letter, handwritten, frame_color, "", font_size)
        self.board.ships[-1].font_color = card_font_color
        if not self.lang.has_cursive:
            self.board.ships[-1].font_color = card_font_color
        self.board.ships[-1].speaker_val = sv
        self.board.ships[-1].speaker_val_update = False

        self.board.add_unit(x - 2, y + 1, 2, 4, classes.board.Letter, "1", frame_color, "", 18)
        self.board.ships[-1].font_color = card_font_color
        self.board.add_door(x - 2, y + 1, 8, 6, classes.board.Door, "", card_color, "")
        self.board.units[0].set_outline(outline_color2, 2)
        self.board.all_sprites_list.move_to_front(self.board.units[0])
        self.slide = self.board.ships[21]
        self.slide.perm_outline = True

        self.board.add_unit(x - 3, y+1, 1, 6, classes.board.ImgCenteredShip, "", frame_color,
                            img_src='nav_l_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)
        self.lt = self.board.ships[-1]

        self.board.add_unit(x + 6, y+1, 1, 6, classes.board.ImgCenteredShip, "", frame_color,
                            img_src='nav_r_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)
        self.rt = self.board.ships[-1]

        for each in self.board.ships:
            each.immobilize()

        self.board.ships[20].outline = False
        self.active_item = self.board.ships[0]
        self.active_item.bg_tint_color = self.bg_color_active
        self.active_item.update_me = True
        self.prev_item = self.active_item

        self.current_letter_index = 0

    def activate_letter(self):
        if self.prev_item is not None:
            self.prev_item.bg_tint_color = self.bg_color_done
            self.prev_item.update_me = True
        self.active_item.bg_tint_color = self.bg_color_active
        self.create_card(self.active_item)
        self.prev_item = self.active_item
        self.mainloop.redraw_needed[0] = True

    def next_slide(self, n):
        if n == 1:
            if self.current_letter_index < 19:
                self.current_letter_index += 1
                self.active_item = self.board.ships[self.current_letter_index]
            else:
                self.active_item = self.board.ships[0]
                self.current_letter_index = 0
        else:
            if self.current_letter_index > 0:
                self.current_letter_index -= 1
                self.active_item = self.board.ships[self.current_letter_index]
            else:
                self.active_item = self.board.ships[19]
                self.current_letter_index = 19

        self.active_item.update_me = True
        self.activate_letter()

        self.mainloop.redraw_needed[0] = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_item = self.board.ships[self.board.active_ship]
            if self.active_item.unit_id < 20:
                self.current_letter_index = self.active_item.unit_id
                self.activate_letter()
            else:
                pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
                if self.lt.rect.topleft[0] < pos[0] < self.lt.rect.topleft[0] + self.lt.rect.width and \
                                        self.lt.rect.topleft[1] < pos[1] < self.lt.rect.topleft[
                            1] + self.lt.rect.height:
                    self.next_slide(-1)
                elif self.rt.rect.topleft[0] < pos[0] < self.rt.rect.topleft[0] + self.rt.rect.width and \
                                        self.rt.rect.topleft[1] < pos[1] < self.rt.rect.topleft[
                            1] + self.rt.rect.height:
                    self.next_slide(1)
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

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

        if sys.version_info < (3, 0):
            self.say(sv.encode("utf-8"))
        else:
            self.say(sv)

        for i in [20, 21, 22, 23, 24]:
            self.board.ships[i].update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
