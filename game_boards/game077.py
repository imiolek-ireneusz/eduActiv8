# -*- coding: utf-8 -*-

import os
import pygame
import sys

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


# This is pretty messed up - sorry trying to keep multi-language program compatible with both python2 and python3 made me to do some desperately heavy things.
# this would be much simpler with python3 only, but not everything in this world is simple...

class Key(pygame.sprite.Sprite):
    def __init__(self, kbrd, data_list, init_color, highlight_color, font_color, font_highlight_color):
        # data_list = [x, y, w, h, top_left, bottom_left, middle, letter, right_top, right_bottom,color_group]
        pygame.sprite.Sprite.__init__(self)
        self.kbrd = kbrd
        self.id = len(kbrd.keys)
        kbrd_w = self.kbrd.kbrd_w - 10
        self.x = (kbrd_w * data_list[0] // 445) + 5
        self.y = (kbrd_w * data_list[1] // 445) + 5
        self.w = (kbrd_w * data_list[2] // 445)
        self.h = (kbrd_w * data_list[3] // 445)
        self.data_list = data_list
        self.labels = [data_list[4], data_list[5], data_list[6], data_list[7], data_list[8], data_list[9]]
        self.color = init_color
        self.init_color = init_color
        self.highlight_color = highlight_color
        self.font_color = font_color
        self.font_highlight_color = font_highlight_color
        hsv = ex.rgb_to_hsv(highlight_color[0], highlight_color[1], highlight_color[2])
        self.outline_color = ex.hsv_to_rgb(hsv[0], hsv[1], hsv[2] - 50)
        self.font_1 = self.kbrd.kbrd_font[0]
        self.font_2 = self.kbrd.kbrd_font[1]

        self.image = pygame.Surface([self.w, self.h])

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

        self.draw_key()

    def draw_key(self):
        # if button is part of keyboard:
        if self.id < 64:
            self.image.fill(self.color)
        else:
            self.image.fill((255, 255, 255))
            rect = [1, 1, self.w - 2, self.h - 2]
            pygame.draw.ellipse(self.image, self.color, rect, 0)
            pygame.draw.ellipse(self.image, self.outline_color, rect, 1)
            self.image.set_colorkey((255, 255, 255))

    def update(self):
        self.draw_key()
        if sys.version_info < (3, 0):
            val = []
            for each in self.labels:
                try:
                    uni = unicode(each, "utf-8")
                except UnicodeDecodeError:
                    uni = each
                except TypeError:
                    uni = each
                val.append(uni)
        else:
            val = self.labels
        for i in range(6):
            if len(val[i]) > 0:
                if self.id < 64:
                    if i == 3:
                        text = self.font_1.render("%s" % (val[i]), 1, self.font_color)
                        font_x = 4
                        font_y = 0
                    elif i < 3:
                        text = self.font_2.render("%s" % (val[i]), 1, self.font_color)
                        if i == 0:
                            font_x = 4
                            font_y = 0
                        elif i == 1:
                            font_x = 4
                            font_y = self.h - self.font_2.size(val[i])[1] - 2
                        elif i == 2:
                            font_x = ((self.w - self.font_2.size(val[i])[0]) // 2)
                            font_y = ((self.h - self.font_2.size(val[i])[1]) // 2)

                    elif i > 3:
                        text = self.font_2.render("%s" % (val[i]), 1, ((0, 0, 200)))
                        if i == 4:
                            font_x = self.w - self.font_2.size(val[i])[0] - 4
                            font_y = 0
                        elif i == 5:
                            font_x = self.w - self.font_2.size(val[i])[0] - 4
                            font_y = self.h - self.font_2.size(val[i])[1] - 2
                else:
                    text = self.font_2.render("%s" % (val[i]), 1, self.font_color)
                    font_x = ((self.w - self.font_2.size(val[i])[0]) // 2)
                    font_y = ((self.h - self.font_2.size(val[i])[1]) // 2)

                self.image.blit(text, (font_x, font_y))

        self.draw_outline()

    def draw_outline(self):
        "draws an 'outline' around the unit"
        color = self.outline_color  # [20,20,20]
        width = 1
        x = 0
        y = 0
        w2 = 1
        if self.id < 64:
            if self.id != 28 and self.id != 42:
                pygame.draw.lines(self.image, color, True,
                                  [[x, y], [self.w - w2, y], [self.w - w2, self.h - w2], [x, self.h - w2]], width)
            else:
                if self.kbrd.keys[28].h > self.kbrd.keys[42].h:
                    p0x = x
                    p1x = self.w - self.kbrd.keys[28].w
                else:
                    p0x = self.w - self.kbrd.keys[42].w
                    p1x = x

                if self.id == 28:
                    pygame.draw.lines(self.image, color, False,
                                      [[p0x, self.h - w2], [x, self.h - w2], [x, y], [self.w - w2, y],
                                       [self.w - w2, self.h - w2]], width)
                else:
                    pygame.draw.lines(self.image, color, False,
                                      [[p1x, y], [x, y], [x, self.h - w2], [self.w - w2, self.h - w2],
                                       [self.w - w2, y]], width)


class KeyBoard:
    def __init__(self, game_board, screen, kbrd_w, kbrd_h):
        self.game_board = game_board
        self.kbrd_w = kbrd_w
        self.kbrd_h = kbrd_h
        self.points = self.game_board.board.points
        self.a_map = game_board.lang.kbrd.accent_map
        self.a_map2 = game_board.lang.kbrd.accent_map2
        self.highlighted = [-1, -1, -1, -1, -1, -1]
        self.keys = []
        self.keys_list = pygame.sprite.RenderPlain()
        self.kbrd_font = []
        self.kbrd_font.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                               (int(float(self.points) / 2))))
        self.kbrd_font.append(pygame.font.Font(os.path.join('res', 'fonts', 'FreeSans', 'FreeSansBold.ttf'),
                                               (int(float(self.points) / 3))))
        self.canvas = pygame.Surface([kbrd_w, kbrd_h])
        self.canvas.fill(self.game_board.bg_col)
        self.add_keys()
        self.draw_hands()

    def get_btns_to_hl(self, text):
        'prepares a list of keys to highlight based on letter/character passed in key ids hardcoded'
        uc = text
        if text != " ":
            hl = [-1, -1, -1, -1, -1, -1]
            # check if letter is lowercase or what position it is on whether shift is needed
            if sys.version_info < (3, 0):
                text = text.encode("utf-8")
                if text in self.a_map:
                    hl[4] = 39
                    if text in self.a_map2:
                        hl[1] = 55
                        hl[3] = 71
                    text = unicode(self.a_map[text], "utf-8")
                    text = text[1]
                    uc = text
            else:
                if text in self.a_map:
                    hl[4] = 39
                    if text in self.a_map2:
                        hl[1] = 55
                        hl[3] = 71
                    text = self.a_map[text][1]
                    uc = text

            shift = False
            for i in range(0, 55):
                if sys.version_info < (3, 0):
                    labels = []
                    for each in self.keys[i].labels:
                        if len(each) > 0:
                            try:
                                uni = unicode(each, "utf-8")
                            except UnicodeDecodeError:
                                uni = each
                        else:
                            uni = ""
                        labels.append(uni)
                else:
                    labels = [each for each in self.keys[i].labels]

                if uc in labels:
                    hl[0] = i
                    if uc == labels[0]:
                        shift = True
                    elif uc == labels[1]:
                        shift = False
                    if uc == labels[4] or uc == labels[5]:
                        alt = True
                    else:
                        alt = False

                    if shift:
                        if self.keys[i].data_list[10] < 4:
                            # right_shift
                            hl[1] = 55
                            hl[3] = 71
                        elif self.keys[i].data_list[10] > 3:
                            # left_shift
                            hl[1] = 43
                            hl[3] = 64
                    hl[2] = self.keys[i].data_list[10] + 64

                    if alt:
                        hl[4] = 60
                        hl[5] = 73
                        self.highlight(hl, uc.lower())
                    else:
                        self.highlight(hl, uc)
                    break
                else:
                    self.highlight([-1, -1, -1, -1, -1, -1], uc)
        else:
            self.highlight([59, -1, 72, -1, -1, -1], "—")

    def highlight(self, hl_ids, txt):
        'resets the highlight from previous letter and highlights new keys'
        # reset old highlight
        for each in self.highlighted:
            if each > -1:
                self.keys[each].color = self.keys[each].init_color
        if self.highlighted[2] > -1:
            self.keys[self.highlighted[2]].labels[3] = ""
        if self.highlighted[3] > -1:
            self.keys[self.highlighted[3]].labels[3] = ""
        if self.highlighted[5] > -1:
            self.keys[self.highlighted[5]].labels[3] = ""
        # apply highlight to new squares
        for i in range(6):
            if hl_ids[i] > -1:
                self.keys[hl_ids[i]].color = self.keys[hl_ids[i]].highlight_color
                if i == 2:
                    self.keys[hl_ids[i]].labels[3] = txt
                if i == 3:
                    self.keys[hl_ids[i]].labels[3] = "↑"
                if i == 5:
                    self.keys[hl_ids[i]].labels[3] = "Alt"

        self.highlighted = hl_ids[:]

    def add_key(self, data_list, init_color, highlight_color, font_color, font_highlight_color):
        new_key = Key(self, data_list, init_color, highlight_color, font_color, font_highlight_color)
        self.keys.append(new_key)
        self.keys_list.add(new_key)

    def add_keys(self):
        colors = [ex.hsv_to_rgb(0, 100, 255), ex.hsv_to_rgb(35, 100, 255), ex.hsv_to_rgb(35 * 2, 100, 255),
                  ex.hsv_to_rgb(35 * 3, 100, 255), ex.hsv_to_rgb(35 * 4, 100, 255), ex.hsv_to_rgb(35 * 5, 100, 255),
                  ex.hsv_to_rgb(35 * 6, 100, 255), ex.hsv_to_rgb(35 * 7, 100, 255), ex.hsv_to_rgb(25, 100, 255),
                  [186, 186, 186]]
        highlight_colors = [ex.hsv_to_rgb(0, 170, 255), ex.hsv_to_rgb(35, 170, 255), ex.hsv_to_rgb(35 * 2, 170, 255),
                            ex.hsv_to_rgb(35 * 3, 170, 255), ex.hsv_to_rgb(35 * 4, 170, 255),
                            ex.hsv_to_rgb(35 * 5, 170, 255), ex.hsv_to_rgb(35 * 6, 170, 255),
                            ex.hsv_to_rgb(35 * 7, 170, 255), ex.hsv_to_rgb(25, 170, 255), [106, 106, 106]]
        font_colors = [ex.hsv_to_rgb(0, 255, 140), ex.hsv_to_rgb(35, 255, 140), ex.hsv_to_rgb(35 * 2, 255, 140),
                       ex.hsv_to_rgb(35 * 3, 255, 140), ex.hsv_to_rgb(35 * 4, 255, 140),
                       ex.hsv_to_rgb(35 * 5, 255, 140), ex.hsv_to_rgb(35 * 6, 255, 140),
                       ex.hsv_to_rgb(35 * 7, 255, 140), ex.hsv_to_rgb(25, 255, 140), [16, 16, 16]]
        font_highlight_colors = [ex.hsv_to_rgb(0, 255, 140), ex.hsv_to_rgb(35, 255, 140),
                                 ex.hsv_to_rgb(35 * 2, 255, 140), ex.hsv_to_rgb(35 * 3, 255, 140),
                                 ex.hsv_to_rgb(35 * 4, 255, 140), ex.hsv_to_rgb(35 * 5, 255, 140),
                                 ex.hsv_to_rgb(35 * 6, 255, 140), ex.hsv_to_rgb(35 * 7, 255, 140),
                                 ex.hsv_to_rgb(25, 255, 140), [0, 0, 0]]

        keys = self.game_board.lang.kbrd.kbrd_keys
        for each in keys:
            self.add_key(each, colors[each[10]], highlight_colors[each[10]], font_colors[each[10]],
                         font_highlight_colors[each[10]])
        self.kbrd_h = self.keys[61].y + self.keys[61].h

    def scale_img(self, img, new_w, new_h):
        'scales image depending on pygame version either with smoothscale or with scale'
        if pygame.version.vernum < (1, 8):
            return pygame.transform.scale(img, (new_w, new_h))
        else:
            return pygame.transform.smoothscale(img, (new_w, new_h))

    def draw_hands(self):
        # calculate new
        img_size = self.kbrd_w * 341 // 630
        left = (self.kbrd_w - img_size) // 2

        try:
            img_org = pygame.image.load(
                os.path.join('res', 'images', 'schemes', self.game_board.scheme, 'hands.jpg')).convert()
            img = img_org.copy()

            # resize the image
            scaled_img = self.scale_img(img, img_size, img_size)
            pos_x = left
            pos_y = self.kbrd_h + (self.keys[61].h) // 3
            img_pos = (pos_x, pos_y)
            self.canvas.blit(scaled_img, img_pos)
        except:
            pass

    def update(self):
        for each_key in self.keys:
            each_key.update()
        self.keys_list.draw(self.canvas)


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.board.decolorable = False
        self.board.draw_grid = False

        font_color1 = (175, 255, 128)
        font_color2 = (0, 230, 0)
        font_color3 = (200, 200, 200)

        color = (255, 255, 255)
        self.bg_col = (255, 255, 255)
        self.scheme = "white"
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                color = (0, 0, 0)
                self.bg_col = (0, 0, 0)
                self.scheme = "black"
                font_color3 = (100, 100, 100)

        data = [15, 12]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=False)

        if x_count < 15:
            data[0] = 15
        elif x_count > 19:
            data[0] = 19
        else:
            data[0] = x_count

        self.data = data

        self.line = 0
        self.course = self.lang.kbrd_course

        self.level.lvl_count = len(self.course)

        if self.lang.lang in ["en_gb", "en_us"]:
            self.chapters = [1, 3, 5, 7, 10, 13, 15, 18, 20, 22, 24, 26, 28]
        elif self.lang.lang == "pl":
            self.chapters = [1, 3, 5, 7, 10, 12, 14, 16, 18, 20, 23, 26, 29, 32]
        elif self.lang.lang == "ru":
            self.chapters = [1, 3, 5, 7, 10, 13, 15, 18, 20, 22, 24, 26, 28]

        if self.level.lvl > len(self.course):
            self.level.lvl = len(self.course) - 1
            self.t_string = self.course[self.level.lvl - 1][1]
            self.t_multi = self.course[self.level.lvl - 1][0]
        else:
            self.t_string = self.course[-1][1]
            self.t_multi = self.course[-1][0]

        if sys.version_info < (3, 0):
            self.current_line = unicode((self.t_string[0] * self.t_multi[0]).strip(), "utf-8")
        else:
            self.current_line = (self.t_string[0] * self.t_multi[0]).strip()

        self.level.games_per_lvl = len(self.t_string)
        self.level.game_step = 1
        label_w = self.data[0] // 2

        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.add_unit(0, 0, label_w, 1, classes.board.Label, "", color, "", 0)
        self.left = self.board.units[-1]
        self.left.text_wrap = False
        self.left.align = 2
        self.left.font_color = font_color1

        self.board.add_unit(label_w, 0, 1, 1, classes.board.Label, self.current_line[0], color, "", 0)
        self.middle = self.board.units[-1]
        self.middle.font_color = font_color2
        self.middle.set_outline([0, 230, 0], 1)

        self.board.add_unit(label_w + 1, 0, label_w, 1, classes.board.Label, self.current_line[1:], color, "", 0)
        self.right = self.board.units[-1]
        self.right.text_wrap = False
        self.right.align = 1
        self.right.font_color = font_color3

        self.board.add_unit(0, 1, data[0], data[1] - 1, classes.board.Label, "", color, "", 0)

        self.kbrd = KeyBoard(self, self.board.units[3], self.board.units[3].rect.w, self.board.units[3].rect.h)
        self.kbrd.get_btns_to_hl(self.current_line[0])

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.show_msg == False:
            if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                char = event.unicode
                if len(char) > 0:
                    if char == self.middle.value:
                        if len(self.right.value) > 0:
                            self.left.value += char
                            next_letter = self.right.value[0]
                            self.middle.value = next_letter
                            self.right.value = self.right.value[1:]
                            self.kbrd.get_btns_to_hl(next_letter)
                            self.mainloop.sfx.play(15)
                        elif len(self.middle.value) > 0:
                            self.left.value += char
                            self.middle.value = ""
                            self.check_entry()
                        for each in [self.left, self.middle, self.right]:
                            each.update_me = True
                    else:
                        self.mainloop.sfx.play(16)

                self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill((255, 255, 255))
        self.kbrd.update()
        self.board.units[3].painting = self.kbrd.canvas.copy()
        self.board.units[3].update_me = True
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_entry(self):
        if self.line < len(self.t_string) - 1:
            self.line += 1
            if sys.version_info < (3, 0):
                self.current_line = unicode((self.t_string[self.line] * self.t_multi[self.line]).strip(), "utf-8")
            else:
                self.current_line = (self.t_string[self.line] * self.t_multi[self.line]).strip()

            self.level.game_step = self.line + 1
            self.left.value = ""
            self.middle.value = self.current_line[0]
            self.right.value = self.current_line[1:]
            self.kbrd.get_btns_to_hl(self.current_line[0])
            self.mainloop.redraw_needed[1] = True
        else:
            self.level.next_board()

    def check_result(self):
        pass
