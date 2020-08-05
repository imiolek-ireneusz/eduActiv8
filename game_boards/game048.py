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

from classes.extras import reverse


def r(s):
    return reverse(s, "ar")


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.board.draw_grid = False
        hue = random.randrange(0, 225)

        card_font_color = ex.hsv_to_rgb(hue, 255, 140)
        arrow_color = ex.hsv_to_rgb(hue, 200, 200)
        font_color2 = ex.hsv_to_rgb(hue, 255, 50)
        outline_color2 = (255, 102, 0)

        if self.mainloop.scheme is not None:
            card_color = self.mainloop.scheme.u_color
        else:
            card_color = (255, 255, 255)


        alc = self.lang.lang_file.alphabet_ar_iso
        self.al_i = self.lang.lang_file.alphabet_ar_ini
        self.al_m = self.lang.lang_file.alphabet_ar_mid
        self.al_e = self.lang.lang_file.alphabet_ar_end

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

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.unit_mouse_over = None
        self.units = []

        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        self.font_size = 17
        self.word_list = self.lang.d['abc_flashcards_word_sequence']
        self.pword_list = self.lang.dp['abc_flashcards_word_sequence']
        self.frame_flow = self.lang.d['abc_flashcards_frame_sequence']

        self.words = [
            [r('الفيل'), r('العنب'), r('الفأر'), r('ابريق الشاي'), r('الحمار الوحشي'), r('البطيخ'), r('الشمبانزي'),
             r('الفراغ'), r('الهوكي'), r('النرجس البري'), r('الزبادي'), r('الراكون'), r('الجبل'), r('الثعلب')],
            [r('بطة'), r('بيت الاسكيمو'), r('بومة'), r('ببغاء'), r('بيانو'), r('بوسه'), r('بلوط')],
            [r('تنورة'), r('تفاحة'), r('تأرجح'), r('تسلق')], [r('ثور امريكى'), r('ثلاثة')], [r('جوغا'), r('جبنه')],
            [r('حشرة العتة'), r('حصان'), r('حلزون'), r('حديد')], [r('خبز')], [r('دفتر'), r('دولفين'), r('ديك رومي')],
            [r('ذهب')], [r('رسم'), r('ركن')], [r('زرافة'), r('زهور'), r('زهرة'), r('زر')],
            [r('سمك'), r('سمك'), r('ساعة حائط')],
            [r('شمس'), r('شجرة'), r('شجرة'), r('شاحنة'), r('شارع'), r('شوبك'), r('شاطئ بحر')],
            [r('صندوق العربة'), r('صخرة')], [r('ضفدع')], [r('طماطم'), r('طالب علم')], [r('ظرف')],
            [r('عاء'), r('عين'), r('عصير')], [r('غزل'), r('غيتار'), r('غبي')],
            [r('فراشة'), r('فرس النهر'), r('فرن'), r('فهد')],
            [r('قارب'), r('قط'), r('قنفذ'), r('قطار'), r('قارب شراعى')], [r('كمان'), r('كوالا'), r('كيوي'), r('كيس')],
            [r('ليل')],
            [r('منزل'), r('مفتاح'), r('ملكة'), r('مظلة'), r('مصور فوتوغرافي'), r('مراقب'), r('ملابس'), r('محيط'),
             r('مهر'), r('موز'), r('ماء'), r('موسيقى'), r('محامي'), r('مسمار'), r('ملاكمة')],
            [r('نملة'), r('نافذة او شباك'), r('نمر')], [r('هاتف')], [r('وحيد القرن')], [r('ينام'), r('يشرب')]]
        self.imgs = [[4, 6, 12, 19, 25, 26, 37, 55, 68, 69, 73, 87, 96, 110], [3, 8, 14, 15, 34, 77, 99],
                     [41, 42, 89, 107], [70, 100], [32, 57], [44, 45, 61, 102], [35], [13, 59, 90], [108], [95, 104],
                     [30, 36, 78, 86], [5, 38, 51], [18, 31, 46, 50, 53, 80, 82], [58, 97], [105], [33, 94], [109],
                     [64, 75, 101], [24, 28, 93], [27, 47, 67, 76], [1, 2, 29, 63, 66], [21, 72, 74, 91], [54],
                     [7, 10, 16, 20, 39, 40, 48, 52, 62, 71, 81, 83, 85, 92, 103], [0, 22, 65], [79], [106], [49, 84]]

        x = data[0] - 2
        y = 0
        label_color = ex.hsv_to_rgb(hue, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(hue, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_tint_color = ex.hsv_to_rgb(hue, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        self.bg_color_active = ex.hsv_to_rgb(hue, 200, 255)
        self.bg_color_done = ex.hsv_to_rgb(hue, 50, 255)

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_r2x1_dc.png")
        else:
            dc_img_src = None
            if self.mainloop.scheme.dark:
                self.bg_color_active = ex.hsv_to_rgb(hue, 255, 200)
                self.bg_color_done = ex.hsv_to_rgb(hue, 255, 55)

        bg_img_src = os.path.join('unit_bg', "universal_r2x1_bg_s150.png")

        for i in range(self.abc_len):
            caption = alc[i]
            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=2, grid_h=1, txt=caption,
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
            y += 1
            if y >= data[1]:
                if i > 2 * data[1] - 2:
                    x = data[0] - 6
                    y = 0
                else:
                    x = data[0] - 4
                    y = 0

        x = (data[0] - 10) // 2

        y = 1

        # Card
        w = 6
        xd = 1
        img_plus = 1
        self.board.add_unit(x + 2 - xd, y - 1, 2, 2, classes.board.Label, alc[0], card_color, "", 31)

        # add letter position indicators
        self.board.add_universal_unit(grid_x=x - xd, grid_y=y + 3, grid_w=2, grid_h=1, txt=caption,
                                      fg_img_src="ar_end.png",
                                      bg_img_src=None,
                                      dc_img_src=None,
                                      bg_color=(0, 0, 0, 0),
                                      border_color=None, font_color=None,
                                      bg_tint_color=None,
                                      fg_tint_color=label_color,
                                      txt_align=(0, 0), font_type=1, multi_color=False, alpha=True,
                                      immobilized=True,
                                      fg_as_hover=False)
        self.units.append(self.board.ships[-1])

        self.board.add_universal_unit(grid_x=x + 2 - xd, grid_y=y + 3, grid_w=2, grid_h=1, txt=caption,
                                      fg_img_src="ar_mid.png",
                                      bg_img_src=None,
                                      dc_img_src=None,
                                      bg_color=(0, 0, 0, 0),
                                      border_color=None, font_color=None,
                                      bg_tint_color=None,
                                      fg_tint_color=label_color,
                                      txt_align=(0, 0), font_type=1, multi_color=False, alpha=True,
                                      immobilized=True,
                                      fg_as_hover=False)
        self.units.append(self.board.ships[-1])

        self.board.add_universal_unit(grid_x=x + 4 - xd, grid_y=y + 3, grid_w=2, grid_h=1, txt=caption,
                                      fg_img_src="ar_ini.png",
                                      bg_img_src=None,
                                      dc_img_src=None,
                                      bg_color=(0, 0, 0, 0),
                                      border_color=None, font_color=None,
                                      bg_tint_color=None,
                                      fg_tint_color=label_color,
                                      txt_align=(0, 0), font_type=1, multi_color=False, alpha=True,
                                      immobilized=True,
                                      fg_as_hover=False)
        self.units.append(self.board.ships[-1])


        self.board.add_unit(x - xd, y + 1, 2, 2, classes.board.Label, self.al_e[0], card_color, "", 31)
        self.board.add_unit(x + 2 - xd, y + 1, 2, 2, classes.board.Label, self.al_m[0], card_color, "", 31)
        self.board.add_unit(x + 4 - xd, y + 1, 2, 2, classes.board.Label, self.al_i[0], card_color, "", 31)

        self.pos_l_labels = [self.board.units[-3], self.board.units[-2], self.board.units[-1]]

        # frame size 288 x 216
        img_src = os.path.join('fc', "fc%03i.jpg" % self.imgs[0][0])
        self.board.add_unit(x - xd + img_plus, y + 4, 4, 3, classes.board.ImgShip, self.words[0][0], card_color,
                            img_src)
        self.slide = self.board.ships[-1]
        self.slide.speaker_val = self.words[0][0]
        self.slide.speaker_val_update = False

        # TO DO adjust for color schemes
        font_colors = ((200, 0, 0), font_color2)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                font_colors = (self.mainloop.scheme.u_font_color3, self.mainloop.scheme.u_font_color)

        self.board.add_unit(x - 2 + xd, y + 7, w, 2, classes.board.Letter, self.words[0][0], card_color, "", 33)
        self.word_label = self.board.ships[-1]

        self.word_label.speaker_val = self.pword_list[0]
        self.word_label.speaker_val_update = False
        h = 8
        self.board.add_door(x - 2 + xd, y, w, h, classes.board.Door, "", card_color, "")
        #self.board.units[-1].set_outline(color=outline_color2, width=2)
        self.board.all_sprites_list.move_to_front(self.board.units[-1])

        self.board.add_unit(x - 3 + xd, 4, 1, 5, classes.board.ImgCenteredShip, "", (0, 0, 0, 0),
                            img_src='nav_l_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)

        self.lt = self.board.ships[-1]
        self.board.add_unit(x - 2 + xd + w, 4, 1, 5, classes.board.ImgCenteredShip, "", (0, 0, 0, 0),
                            img_src='nav_r_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)
        self.rt = self.board.ships[-1]


        self.slide.set_outline(color=outline_color2, width=2)
        for each in self.board.ships:
            each.immobilize()
            each.font_color = card_font_color
        for each in self.board.units:
            each.font_color = card_font_color
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
            if self.current_letter_index < self.abc_len - 1:
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
                self.active_item = self.board.ships[self.abc_len - 1]
                self.current_letter_index = self.abc_len - 1

        self.active_item.update_me = True
        self.activate_letter()
        self.mainloop.redraw_needed[0] = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active_item = self.board.ships[self.board.active_ship]
            if self.active_item.unit_id < self.abc_len:
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
        val = ex.unival(active.value)
        if sys.version_info < (3, 0):
            self.say(val[0].encode("utf-8"))
        else:
            self.say(val[0])
        indx = [0, 1]
        self.board.units[0].value = val

        word_index = random.randint(0, len(self.words[active.unit_id]) - 1)

        self.slide.value = self.words[active.unit_id][word_index]
        self.slide.speaker_val = self.words[active.unit_id][word_index]
        self.word_label.set_value(self.words[active.unit_id][word_index])
        self.word_label.speaker_val = self.words[active.unit_id][word_index]

        self.pos_l_labels[0].set_value(self.al_e[active.unit_id])
        self.pos_l_labels[1].value = self.al_m[active.unit_id]
        self.pos_l_labels[2].value = self.al_i[active.unit_id]
        for each in self.pos_l_labels:
            each.update_me = True

        indx2 = [self.abc_len, self.abc_len + 1]
        img_src = os.path.join('fc', "fc%03i.jpg" % self.imgs[active.unit_id][word_index])
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
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
