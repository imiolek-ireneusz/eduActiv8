# -*- coding: utf-8 -*-

import colorsys
import copy
import os
import pygame
import sys

import classes.extras as ex


class ImageLayer:
    def __init__(self, canvas, img_src, alpha):
        self.canvas = canvas
        self.img_src = img_src
        self.alpha = alpha
        self.rect = self.canvas.get_rect()
        self.img = None
        self.img_pos = (0, 0)
        self.change_image(img_src)

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.update_me = True
            self.hasimg = True
            try:
                if self.alpha:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
                else:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert()
                self.img_rect = self.img_org.get_rect()
                self.img = self.scalled_img(self.img_org, self.rect.w, self.rect.h)
                self.img_rect = self.img.get_rect()

            except:
                pass

    def get_tinted_img(self, tint_color):
        tinted_img = self.img.copy()
        tinted_img.fill(tint_color, special_flags=pygame.BLEND_ADD)
        return tinted_img

    def scalled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img


class Universal(pygame.sprite.Sprite):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1,
                 txt=None,
                 fd_img_src=None,
                 bg_img_src=None,
                 dc_img_src=None,
                 bg_color=(0, 0, 0, 0),
                 border_color=None,
                 font_colors=None,
                 bg_tint_color=None,
                 fd_tint_color=None,
                 txt_align=(0, 0),
                 font_type=0,
                 multi_color=False,
                 alpha=True,
                 immobilized=False):

        pygame.sprite.Sprite.__init__(self)

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.grid_last_x = grid_x
        self.grid_last_y = grid_y
        self.alpha = alpha
        self.board = board

        self.bg_color = bg_color
        self.border_color = border_color
        self.font_colors = font_colors  # needs to be a list

        self.bg_tint_color = bg_tint_color
        self.fd_tint_color = fd_tint_color

        self.bg_img_src = bg_img_src
        self.fd_img_src = fd_img_src
        self.dc_img_src = dc_img_src

        self.txt = txt
        self.txt_align = txt_align[0]  # align: 0 - centered, 1 - left, 2 - right
        self.txt_valign = txt_align[1]  # align: 0 - centered, 1 - top

        self.multi_color = multi_color

        self.initcolor = self.bg_color
        self.allow_brightening = True

        self.decolorable = False
        self.value = txt
        if txt is not None:
            self.speaker_val = txt
        else:
            self.speaker_val = ""

        self.draggable = True
        self.animable = True
        self.show_value = True
        self.readable = False
        self.audible = False  # use true to enable sounds on unit move
        self.outline_highlight = False
        self.update_me = True
        self.hidden = False

        self.check_display = None  # None - none, True - correct, False - wrong
        self.checkable = False

        # Set height, width, the -1 is to give it some space around for the margin
        if self.alpha:
            self.image = pygame.Surface([grid_w * board.scale - 1, grid_h * board.scale - 1], flags=pygame.SRCALPHA)
        else:
            self.image = pygame.Surface([grid_w * board.scale - 1, grid_h * board.scale - 1])

        # Make our top-left corner the passed-in location. The +1 is the margin
        self.rect = self.image.get_rect()
        self.rect.topleft = [grid_x * board.scale + 1, grid_y * board.scale + 1]

        # scale font size:
        self.font = board.font_sizes[font_type]
        self.text_wrap = True

        self.unit_id = len(board.ships)
        self.img_src2 = None

        if bg_img_src is not None:
            self.layer_bg = ImageLayer(self.image, bg_img_src, alpha)

        if fd_img_src is not None:
            self.layer_fd = ImageLayer(self.image, fd_img_src, alpha)

        if dc_img_src is not None:
            self.layer_dc = ImageLayer(self.image, dc_img_src, alpha)

        if immobilized:
            self.immobilize()

        self.set_value(self.txt)
        if self.border_color is not None:
            self.set_outline(self.border_color, 2)
        self.compose_image()

    def resize_unit(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h
        if self.alpha:
            self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1], flags=pygame.SRCALPHA)
        else:
            self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1])
        self.image.fill(self.color)

    def set_display_check(self, value):
        self.check_display = value
        self.update_me = True

    def init_check_images(self, align=2, shrink=2):
        # w = int((self.grid_w * self.board.scale) / shrink)
        h = w = int((self.grid_h * self.board.scale) / shrink)
        if align == 2:
            self.check_x = int((self.grid_w * self.board.scale * 0.95) - w)
            self.check_y = int((self.grid_h * self.board.scale * 0.95) - h)
        elif align == 1:
            self.check_x = ((self.grid_w * self.board.scale) - w) // 2
            self.check_y = ((self.grid_h * self.board.scale) - h) // 2

        self.check_img1 = self.scalled_img(
            pygame.image.load(os.path.join('res', 'images', "check_ok.png")).convert_alpha(), w, h)
        self.check_img2 = self.scalled_img(
            pygame.image.load(os.path.join('res', 'images', "check_wrong.png")).convert_alpha(), w, h)

    def scalled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    def update_font_size(self, font_size):
        self.font = self.board.font_sizes[font_size]

    def set_value(self, new_value):
        self.value = ex.unival(new_value)
        self.update_me = True
        if self.multi_color:
            self.coltxt = self.split_tags(self.value)
            self.value = "".join(self.coltxt[1])

    def split_tags(self, text):
        txt = []
        col = []
        txtln = []
        tmp = ""

        ln = len(text)
        i = 0
        while i < ln:
            if text[i] == "<":
                if i > 0:
                    if len(txt) > 0:
                        txtln.append(self.font.size("".join(txt) + tmp)[0] - self.font.size(tmp)[0])
                    else:
                        txtln.append(0)
                    txt.append(tmp)
                    tmp = ""
                i += 1
            if text[i] == ">":
                col.append(int(tmp) - 1)
                tmp = ""
                i += 1

            tmp += text[i]
            i += 1

        txtln.append(self.font.size("".join(txt) + tmp)[0] - self.font.size(tmp)[0])
        txt.append(tmp)
        return [col, txt, txtln]

    def pos_update(self):
        if self.grid_w > 0 and self.grid_h > 0:
            self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1])
            self.painting = self.image
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]
        else:
            self.image = pygame.Surface([1, 1])
            # self.painting = self.image
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

    @property
    def grid_pos(self):
        return [self.grid_x, self.grid_y]

    def immobilize(self):
        self.keyable = False
        self.draggable = False
        self.highlight = False

    def add_to_handle(self):
        if self.speaker_val_update:
            self.speaker_val = self.value

    def compose_image(self):
        if self.board.mainloop.scheme is not None and self.board.decolorable and self.decolorable and self.board.mainloop.game_board is not None:
            self.initcolor = self.board.mainloop.scheme.u_initcolor  # (255,255,255)
            self.color = self.board.mainloop.scheme.u_color  # (255,255,255)
            if not self.multi_color:
                self.font_colors = (self.board.mainloop.scheme.u_font_color, )  # (0,0,0)

        # draw background color
        self.image.fill(self.bg_color)

        # draw background image
        if self.bg_img_src is not None:
            if self.layer_bg.img is not None:
                # apply background tint
                if self.bg_tint_color is not None:
                    self.image.blit(self.layer_bg.get_tinted_img(self.bg_tint_color), (0, 0))
                else:
                    self.image.blit(self.layer_bg.img, (0, 0))

        # draw background border
        if self.border_color is not None:
            self.draw_outline()

        # draw foreground image
        if self.fd_img_src is not None:
            if self.layer_fd.img is not None:
                # apply foreground tint
                if self.fd_tint_color is not None:
                    self.image.blit(self.layer_fd.get_tinted_img(self.fd_tint_color), (0, 0))
                else:
                    self.image.blit(self.layer_fd.img, (0, 0))

        # draw custom drawn image

        # draw foreground text
        self.display_text()

        # draw highlight or other decor layer
        if self.dc_img_src is not None:
            if self.layer_dc.img is not None:
                self.image.blit(self.layer_dc.img, (0, 0))

    def update(self, board, **kwargs):
        if self.update_me:
            self.update_me = False
            self.compose_image()

            # apply checkmarks
            self.draw_check_marks()

    def display_text(self):
        if self.txt is not None and self.show_value:
            if not self.multi_color:
                if sys.version_info < (3, 0):
                    if isinstance(self.value, basestring):
                        # if a passed argument is a string turn it into a 1 item list
                        if self.font.size(self.value)[0] < self.rect.w or not self.text_wrap:
                            value = [self.value]
                        else:
                            # else enter extra line breaks
                            if len(self.value) > 5:
                                line = ""
                                test_line = ""
                                word = ""
                                value = []
                                valx = ""
                                try:
                                    valx = unicode(self.value, "utf-8")
                                except UnicodeDecodeError:
                                    valx = self.value
                                except TypeError:
                                    valx = self.value
                                linelen = len(valx)

                                for i in range(linelen):
                                    if valx[i] == "\n":
                                        test_line = "" + word
                                        word = ""
                                        value.append(line)
                                        line = "" + test_line
                                    elif valx[i] == " " or i == linelen - 1:
                                        test_line = test_line + word + valx[i]
                                        if self.font.size(test_line)[0] < self.rect.w:
                                            line = "" + test_line
                                            word = ""
                                        else:
                                            test_line = "" + word + valx[i]
                                            word = ""
                                            value.append(line)
                                            line = "" + test_line
                                    else:
                                        word += valx[i]
                                if len(test_line) > 0:
                                    value.append(test_line)
                            else:
                                value = [self.value]
                    else:
                        value = self.value
                else:
                    if isinstance(self.value, str):
                        # if a passed argument is a string turn it into a 1 item list
                        if self.font.size(self.value)[0] < self.rect.w or not self.text_wrap:
                            value = [self.value]
                        else:
                            # else enter extra line breaks
                            if len(self.value) > 5:
                                line = ""
                                test_line = ""
                                word = ""
                                value = []
                                valx = self.value
                                linelen = len(valx)

                                for i in range(linelen):
                                    if valx[i] == "\n":
                                        test_line = "" + word
                                        word = ""
                                        value.append(line)
                                        line = "" + test_line
                                    elif valx[i] == " " or i == linelen - 1:
                                        test_line = test_line + word + valx[i]
                                        if self.font.size(test_line)[0] < self.rect.w:
                                            line = "" + test_line
                                            word = ""
                                        else:
                                            test_line = "" + word + valx[i]
                                            word = ""
                                            value.append(line)
                                            line = "" + test_line
                                    else:
                                        word += valx[i]
                                if len(test_line) > 0:
                                    value.append(test_line)
                            else:
                                value = [self.value]
                    else:
                        value = self.value

                lv = len(value)
                for i in range(lv):
                    if sys.version_info < (3, 0):
                        try:
                            val = unicode(value[i], "utf-8")
                        except UnicodeDecodeError:
                            val = value[i]
                        except TypeError:
                            val = value[i]
                    else:
                        val = value[i]
                    try:
                        text = self.font.render("%s" % (val), 1, self.font_colors[0])
                    except:
                        pass

                    if self.txt_align == 0:
                        font_x = ((self.board.scale * self.grid_w - self.font.size(val)[0]) // 2)
                    elif self.txt_align == 1:
                        font_x = 5
                    elif self.txt_align == 2:
                        font_x = self.board.scale * self.grid_w - self.font.size(val)[0] - 5
                    if lv == 1:
                        font_y = ((self.board.scale * self.grid_h - self.font.size(val)[1]) // 2)
                    elif lv == self.grid_h:
                        # number of items is equal to grid height of an object - distribute lines equally in each grid square
                        font_y = ((self.board.scale - self.font.size(val)[1]) // 2) + self.board.scale * i
                    else:
                        if self.txt_valign == 0:
                            # lv - total
                            line_h = self.font.size(value[0])[
                                         1] / self.board.mainloop.config.font_line_height_adjustment
                            line_margin = 0
                            step = line_h + line_margin
                            center = (self.board.scale * self.grid_h) // 2
                            start_at = center - (
                                    step * lv - line_margin) // 2 - self.board.mainloop.config.font_start_at_adjustment
                            font_y = start_at + step * i
                        else:
                            line_h = self.font.size(value[0])[
                                         1] / self.board.mainloop.config.font_line_height_adjustment
                            line_margin = 0
                            step = line_h + line_margin
                            start_at = 5
                            font_y = start_at + step * i
                    try:
                        self.image.blit(text, (font_x, font_y))
                    except:
                        pass
            else: # multi-color
                if self.show_value:
                    val = ex.unival(self.value)
                    if self.txt_align == 0:
                        font_x = ((self.board.scale * self.grid_w - self.font.size(val)[0]) // 2)
                    elif self.txt_align == 1:
                        font_x = 5
                    elif self.txt_align == 2:
                        font_x = self.board.scale * self.grid_w - self.font.size(val)[0] - 5
                    font_y = ((self.board.scale * self.grid_h - self.font.size(val)[1]) // 2)

                    for i in range(len(self.coltxt[0])):
                        text = self.font.render("%s" % (self.coltxt[1][i]), 1, self.font_colors[self.coltxt[0][i]])
                        self.image.blit(text, (font_x + self.coltxt[2][i], font_y))


    def draw_check_marks(self):
        if self.check_display is not None:
            if self.check_display:
                self.image.blit(self.check_img1, (self.check_x, self.check_y))
            else:
                self.image.blit(self.check_img2, (self.check_x, self.check_y))

    @property
    def reversed_colorx(self):
        return [int(each / 1.5) for each in reversed(self.initcolor)]

    @property
    def brighter(self):
        if self.highlight:
            color = [each / 255.0 for each in self.initcolor]
            hsv = colorsys.rgb_to_hsv(color[0], color[1], color[2])
            rgb = colorsys.hsv_to_rgb(hsv[0], 0.2, 1)
            return [int(each * 255) for each in rgb]
        else:
            return self.initcolor

    def turn(self, d):
        pass

    def rot_centerx(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = copy.deepcopy(orig_rect)
        rot_rect.center = rot_image.get_rect().center
        rot_image = copy.copy(rot_image.subsurface(rot_rect))
        return rot_image

    def draw_outline(self):
        """draws an 'outline' around the unit"""
        color = self.perm_outline_color
        width = self.perm_outline_width
        if width > 1:
            x = width // 2 - 1
            y = width // 2 - 1
            if width % 2 == 0:
                w2 = width // 2 + 2
            else:
                w2 = width // 2 + 1
        elif width == 1:
            x = 0
            y = 0
            w2 = 2
        pygame.draw.lines(self.image, color, True, [[x - width, y], [self.board.scale * self.grid_w - w2 + width, y],
                                                    [self.board.scale * self.grid_w - w2, y - width],
                                                    [self.board.scale * self.grid_w - w2,
                                                     self.board.scale * self.grid_h - w2 + width],
                                                    [self.board.scale * self.grid_w - w2 + width,
                                                     self.board.scale * self.grid_h - w2],
                                                    [x - width, self.board.scale * self.grid_h - w2],
                                                    [x, self.board.scale * self.grid_h - w2 + width], [x, y - width]],
                          width)

    def set_outline(self, color=[255, 0, 0], width=2):
        'enables the draw_outline and sets line color and width'
        self.perm_outline = True
        if color == 0 and hasattr(self, "door_outline") is False:  # if color is 0 calculate colour from base colour
            # convert to hsv
            c = self.color
            h, s, v = ex.rgb_to_hsv(c[0], c[1], c[2])
            outline_color = ex.hsv_to_rgb(h, s + 50, v - 50)
            self.perm_outline_color = outline_color
        elif color == 1:
            c = self.color
            h, s, v = ex.rgb_to_hsv(c[0], c[1], c[2])
            outline_color = ex.hsv_to_rgb(h, s + 20, v - 20)
            self.perm_outline_color = outline_color
        elif hasattr(self, "door_outline") is False:
            self.perm_outline_color = color
        else:
            pass
        self.perm_outline_width = width
        self.init_pow = width

    def move(self, board, x, y):
        board.move(self.unit_id, x, y)

    def on_mouse_out(self):
        self.update_me = True
        self.hover = False

    def on_mouse_click(self):
        pass

    def on_mouse_enter(self):
        self.hover = True
        self.update_me = True
        self.board.mainloop.redraw_needed[1] = True
        self.update(self.board)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            if not self.hover:
                self.on_mouse_enter()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_mouse_click()

