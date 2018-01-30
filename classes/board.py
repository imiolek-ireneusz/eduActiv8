# -*- coding: utf-8 -*-

import colorsys
import copy
import os
import pygame
import random
import sys

import classes.extras as ex


class Unit(pygame.sprite.Sprite):
    """basic class for all on-board objects"""

    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", color=(0, 0, 0), alpha=False, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.grid_last_x = grid_x
        self.grid_last_y = grid_y
        self.alpha = alpha
        self.board = board
        self.initcolor = color
        self.color = color
        self.decolorable = True
        self.locked = False
        self.lockable = False
        self.value = value
        self.speaker_val = value
        self.speaker_val_update = True
        self.outline = False
        self.perm_outline = False
        self.perm_outline_color = [255, 0, 0]
        self.perm_outline_width = 2
        self.fraction_line_top = False
        self.fraction_line_bottom = False
        self.fraction_line_color = (0, 0, 0)
        self.hasimg = False
        self.draggable = True
        self.animable = True
        self.keyable = True
        self.show_value = True
        self.readable = True
        self.highlight = True
        self.audible = False  # use true to enable sounds on unit move
        self.outline_highlight = False
        self.font_color = (0, 0, 0, 0)
        self.align = 0  # align: 0 - centered, 1 - left, 2 - right
        self.valign = 0  # align: 0 - centered, 1 - top
        self.idx = 0  # position in sequence
        self.update_me = True

        self.check_display = None  # None - none, True - correct, False - wrong
        self.checkable = False
        # Set height, width, the -1 is to give it some space around for the margin
        if self.alpha:
            self.image = pygame.Surface([grid_w * board.scale - 1, grid_h * board.scale - 1], flags=pygame.SRCALPHA)
        else:
            self.image = pygame.Surface([grid_w * board.scale - 1, grid_h * board.scale - 1])
        self.image.fill(self.color)

        # http://www.pygame.org/docs/ref/surface.html - surface.fill() comment
        # self.image = pygame.Surface([grid_w*board.scale-1, grid_h*board.scale-1],flags=pygame.SRCALPHA)
        # self.image.fill(self.color,special_flags=pygame.BLEND_RGBA_MIN)
        self.painting = self.image

        # Make our top-left corner the passed-in location. The +1 is the margin
        self.rect = self.image.get_rect()
        self.rect.topleft = [grid_x * board.scale + 1, grid_y * board.scale + 1]

        # scale font size:
        self.font = board.font_sizes[0]
        self.text_wrap = True
        self.is_door = False

    def resize_unit(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h
        if self.alpha:
            self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1], flags=pygame.SRCALPHA)
        else:
            self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1])
        self.image.fill(self.color)

        #self.rect = self.image.get_rect()
        #self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

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

        self.check_img1 = self.scaled_img(
            pygame.image.load(os.path.join('res', 'images', "check_ok.png")).convert_alpha(), w, h)
        self.check_img2 = self.scaled_img(
            pygame.image.load(os.path.join('res', 'images', "check_wrong.png")).convert_alpha(), w, h)

    def set_value(self, new_value):
        self.value = ex.unival(new_value)
        self.update_me = True

    def update_font_size(self, font_size):
        self.font = self.board.font_sizes[font_size]

    def set_fraction_lines(self, top, bottom, color):
        if top:
            self.fraction_line_top = True
        else:
            self.fraction_line_top = False
        if bottom:
            self.fraction_line_bottom = True
        else:
            self.fraction_line_bottom = False
        self.fraction_line_color = color

    def draw_fraction_lines(self):
        if self.fraction_line_top or self.fraction_line_bottom:
            width = self.board.scale // 20
            margin = (self.board.scale * self.grid_w) // 8
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
        if self.fraction_line_top:
            pygame.draw.line(self.image, self.fraction_line_color, [x - width + margin, y], [self.board.scale * self.grid_w - w2 + width - margin, y], width)

        if self.fraction_line_bottom:
            pygame.draw.line(self.image, self.fraction_line_color, [x - width + margin, self.board.scale * self.grid_h - w2], [self.board.scale * self.grid_w - w2 + width - margin, self.board.scale * self.grid_h - w2], width)

            """
            pygame.draw.lines(self.image, color, True, [[x - width, y], [self.board.scale * self.grid_w - w2 + width, y],
                                                    [self.board.scale * self.grid_w - w2, y - width],
                                                    [self.board.scale * self.grid_w - w2,
                                                     self.board.scale * self.grid_h - w2 + width],
                                                    [self.board.scale * self.grid_w - w2 + width,
                                                     self.board.scale * self.grid_h - w2],
                                                    [x - width, self.board.scale * self.grid_h - w2],
                                                    [x, self.board.scale * self.grid_h - w2 + width], [x, y - width]],
            """


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

    def scale_img(self, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if self.img.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            self.img = self.img_org = pygame.transform.smoothscale(self.img, (new_w, new_h))
        else:
            self.img = self.img_org = pygame.transform.scale(self.img, (new_w, new_h))

    def scaled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    @property
    def grid_pos(self):
        return [self.grid_x, self.grid_y]

    def set_color(self, color):
        self.color = color
        self.initcolor = color

    def immobilize(self):
        self.keyable = False
        self.draggable = False
        self.highlight = False

    # Update color, image or text
    def update(self, board, **kwargs):
        if self.update_me:
            self.update_me = False
            if self.board.mainloop.scheme is not None and self.board.decolorable and self.decolorable and self.board.mainloop.game_board is not None and (
                isinstance(self, Letter) or isinstance(self, Label)):
                self.initcolor = self.board.mainloop.scheme.u_initcolor  # (255,255,255)
                self.color = self.board.mainloop.scheme.u_color  # (255,255,255)
                self.font_color = self.board.mainloop.scheme.u_font_color  # (0,0,0)

            self.image.fill(self.color)
            self.image.blit(self.painting, (0, 0))
            if not self.hasimg:
                if len(self.value) > 0:
                    if self.show_value:
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

                                            # value = [self.value]
                                    else:
                                        value = [self.value]
                            else:
                                value = self.value
                        else:
                            if isinstance(self.value, str):
                                # if a passed argument is a string turn it into a 1 item list
                                # value = [self.value]
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
                                            # value = [self.value]
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
                                text = self.font.render("%s" % (val), 1, self.font_color)
                            except:
                                pass

                            if self.align == 0:
                                font_x = ((board.scale * self.grid_w - self.font.size(val)[0]) // 2)
                            elif self.align == 1:
                                font_x = 5
                            elif self.align == 2:
                                font_x = board.scale * self.grid_w - self.font.size(val)[0] - 5
                            if lv == 1:
                                font_y = ((board.scale * self.grid_h - self.font.size(val)[1]) // 2)
                            elif lv == self.grid_h:  # number of items is equal to grid height of an object - distribute lines equally in each grid square
                                font_y = ((board.scale - self.font.size(val)[1]) // 2) + board.scale * i
                            else:
                                if self.valign == 0:
                                    # lv - total
                                    line_h = self.font.size(value[0])[
                                                 1] / self.board.mainloop.config.font_line_height_adjustment
                                    line_margin = 0  # (board.scale*self.grid_h - line_h*lv)//lv # self.font.size(value[0])[1]//4
                                    step = line_h + line_margin
                                    center = (board.scale * self.grid_h) // 2
                                    start_at = center - (
                                                        step * lv - line_margin) // 2 - self.board.mainloop.config.font_start_at_adjustment
                                    font_y = start_at + step * i
                                else:
                                    # lv - total
                                    line_h = self.font.size(value[0])[
                                                 1] / self.board.mainloop.config.font_line_height_adjustment
                                    line_margin = 0  # (board.scale*self.grid_h - line_h*lv)//lv # self.font.size(value[0])[1]//4
                                    step = line_h + line_margin
                                    # center = (board.scale*self.grid_h)//2
                                    start_at = 5  # center - (step*lv - line_margin)//2
                                    font_y = start_at + step * i
                            try:
                                self.image.blit(text, (font_x, font_y))
                            except:
                                pass

            if self.speaker_val_update:
                self.speaker_val = self.value

            if self.perm_outline:
                self.draw_outline()

            self.draw_fraction_lines()
            self.draw_check_marks()

    def draw_check_marks(self):
        if self.check_display is not None:
            if self.check_display:
                self.image.blit(self.check_img1, (self.check_x, self.check_y))
            else:
                self.image.blit(self.check_img2, (self.check_x, self.check_y))

    @property
    def reversed_color(self):
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

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = copy.deepcopy(orig_rect)
        rot_rect.center = rot_image.get_rect().center
        rot_image = copy.copy(rot_image.subsurface(rot_rect))
        return rot_image

    def draw_outline(self):
        """draws an 'outline' around the unit"""
        color = self.perm_outline_color  # [255,0,0]
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
        # self.perm_outline_color = color
        # self.perm_outline_color = [255,0,0]
        self.perm_outline_width = width
        self.init_pow = width

    def set_correct(self, correct=True):
        if correct:
            print("correct")
        else:
            print("wrong")


class Obstacle(Unit):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(23, 157, 255), alpha=False,
                 **kwargs):
        self.initcolor = initcolor
        Unit.__init__(self, board, grid_x, grid_y, grid_w, grid_h, "0", self.initcolor, alpha, **kwargs)
        self.unit_id = len(board.units)
        self.value = value


class Label(Obstacle):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), font_size=0,
                 alpha=False, **kwargs):
        Obstacle.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha, **kwargs)
        self.font = board.font_sizes[font_size]

    def update(self, board, **kwargs):
        Unit.update(self, board)


class Ship(Unit):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), alpha=False,
                 **kwargs):
        self.initcolor = initcolor
        self.allow_brightening = True
        Unit.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, self.initcolor, alpha, **kwargs)
        self.unit_id = len(board.ships)

    def move(self, board, x, y):
        board.move(self.unit_id, x, y)

    def update(self, board, point, **kwargs):
        if self.update_me:
            Unit.update(self, board)
            if self.lockable and self.locked:
                self.draw_circle(board, point)

    def enable_circle(self):
        self.locked = True

    def disable_circle(self):
        self.locked = False

    def draw_circle(self, board, point):
        max_radius = board.scale // 2
        step = max_radius // 4
        color = self.reversed_color
        for i in range(1, 4):
            try:
                pygame.draw.ellipse(self.image, color, (
                (point[0] + step, point[1] + step), (board.scale - step * 2, board.scale - step * 2)), 1)
                step += step
            except ValueError:
                pass
        pygame.draw.line(self.image, color, [point[0] + board.scale // 2, point[1]],
                         [point[0] + board.scale // 2, point[1] + board.scale], 1)
        pygame.draw.line(self.image, color, [point[0], point[1] + board.scale // 2],
                         [point[0] + board.scale, point[1] + board.scale // 2], 1)


class Letter(Ship):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), alpha=False,
                 font_size=0, **kwargs):
        Ship.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha, **kwargs)
        self.font = board.font_sizes[font_size]

    def update(self, board, **kwargs):
        Unit.update(self, board)


class MultiColorLetters(Letter):
    """accepts string formatted in a way to allow multiple colours in one line, e.g. "<1>this is in colour one<2>this is in colour two". to initialize colours use the set_font_colours method """

    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(0, 0, 0), alpha=False,
                 **kwargs):
        Letter.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha, **kwargs)
        self.set_font_colors((0, 0, 0), (0, 0, 0))
        self.set_value(value)
        # print(self.value)

    def set_value(self, new_value):
        self.value = ex.unival(new_value)
        value = ex.unival(new_value)
        self.coltxt = self.split_tags(value)
        self.value = "".join(self.coltxt[1])

    def set_font_colors(self, color1, color2, color3=(0, 0, 0), color4=(0, 0, 0)):
        self.colors = [color1, color2, color3, color4]

    def split_tags(self, text):

        txt = []
        col = []
        txtln = []
        tmp = ""
        # for i in range(ln-1):
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

    # Update color, image or text
    def update(self, board, **kwargs):
        # print(self.value)
        # self.update_me = True
        if self.update_me:
            self.update_me = False
            if self.board.mainloop.scheme is not None and self.board.decolorable and self.decolorable and self.board.mainloop.game_board is not None and (
                isinstance(self, Letter) or isinstance(self, Label)):
                self.initcolor = self.board.mainloop.scheme.u_initcolor  # (255,255,255)
                self.color = self.board.mainloop.scheme.u_color  # (255,255,255)
                self.font_color = self.board.mainloop.scheme.u_font_color  # (0,0,0)

            self.image.fill(self.color)
            self.image.blit(self.painting, (0, 0))
            # if self.hasimg == False:
            # if len(self.value) > 0:
            if self.show_value:
                val = ex.unival(self.value)
                # lv = len(val)
                if self.align == 0:
                    font_x = ((board.scale * self.grid_w - self.font.size(val)[0]) // 2)
                elif self.align == 1:
                    font_x = 5
                elif self.align == 2:
                    font_x = board.scale * self.grid_w - self.font.size(val)[0] - 5
                font_y = ((board.scale * self.grid_h - self.font.size(val)[1]) // 2)

                for i in range(len(self.coltxt[0])):
                    text = self.font.render("%s" % (self.coltxt[1][i]), 1, self.colors[self.coltxt[0][i]])
                    self.image.blit(text, (font_x + self.coltxt[2][i], font_y))

            if self.speaker_val_update:
                self.speaker_val = self.value

            if self.perm_outline:
                self.draw_outline()


class ImgSurf(pygame.sprite.Sprite):
    def __init__(self, board, grid_w=1, grid_h=1, color=(255, 157, 23), img_src='', alpha=False):
        pygame.sprite.Sprite.__init__(self)
        # Ship.__init__(self,board,grid_x,grid_y,grid_w,grid_h,value,initcolor,**kwargs)
        self.img_src = img_src
        # grid location and size
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.board = board
        self.color = color
        self.alpha = alpha
        self.image = pygame.Surface([grid_w * board.scale - 1, grid_h * board.scale - 1])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        if len(self.img_src) > 0:
            self.hasimg = True
            self.img = self.image
            self.img_pos = (0, 0)
            self.outline = True
            try:
                if self.alpha:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
                else:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert()
                self.img = self.img_org
                self.img_rect = self.img.get_rect()
                # resize the image
                self.scale_img(self.rect.w, self.rect.h)

                self.img_rect = self.img.get_rect()
                pos_x = ((board.scale * self.grid_w - self.img_rect.w) // 2)
                pos_y = ((board.scale * self.grid_h - self.img_rect.h) // 2)
                self.img_pos = (pos_x, pos_y)
            except:
                pass

    def scale_img(self, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if self.img.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            self.img = self.img_org = pygame.transform.smoothscale(self.img, (new_w, new_h))
        else:
            self.img = self.img_org = pygame.transform.scale(self.img, (new_w, new_h))


class ImgShip(Ship):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), img_src='',
                 alpha=False, door_alpha=False, **kwargs):
        Ship.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha, **kwargs)
        self.img_src2 = None
        self.change_image(img_src)

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.update_me = True
            self.hasimg = True
            self.img = self.image
            self.img_pos = (0, 0)
            self.outline = True
            try:
                if self.alpha:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
                else:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert()
                self.img = self.img_org
                self.img_rect = self.img.get_rect()
                # resize the image
                self.scale_img(self.rect.w, self.rect.h)

                self.img_rect = self.img.get_rect()
                pos_x = ((self.board.scale * self.grid_w - self.img_rect.w) // 2)
                pos_y = ((self.board.scale * self.grid_h - self.img_rect.h) // 2)
                self.img_pos = (pos_x, pos_y)
            except:
                pass

    def update(self, board, **kwargs):
        if self.update_me:
            Unit.update(self, board)
            if len(self.img_src) > 0:
                self.image.blit(self.img, self.img_pos)
            if self.unit_id == board.active_ship and self.outline == True:
                lines = [[0, 0], [self.grid_w * board.scale - 2, 0],
                         [self.grid_w * board.scale - 2, self.grid_h * board.scale - 2],
                         [0, self.grid_h * board.scale - 2]]
                pygame.draw.lines(self.image, (255, 200, 200), True, lines)
            if hasattr(self, "door_outline") and self.door_outline is True:
                self.set_outline(self.perm_outline_color, 2)
            if self.perm_outline:
                self.draw_outline()

            self.draw_check_marks()

    @property
    def brighter(self):
        return self.color


class TwoImgsShip(Ship):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), img_src='',
                 img2_src='', row_data=(0, 0), alpha=False, **kwargs):
        Ship.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha, **kwargs)
        self.img2_pos = row_data
        self.change_image(img_src, img2_src)

    def change_image(self, img_src, img2_src):
        self.img_src = img_src
        self.img2_src = img2_src
        if len(self.img_src) > 0:
            self.hasimg = True
            self.img = self.image
            self.img_pos = (0, 0)
            self.outline = True
            try:
                # if True:
                if self.alpha:
                    self.img_org = pygame.image.load(self.img_src).convert_alpha()
                    self.img2_org = pygame.image.load(self.img2_src).convert_alpha()
                else:
                    self.img_org = pygame.image.load(self.img_src).convert()
                    self.img2_org = pygame.image.load(self.img2_src).convert()
                self.img = self.img_org
                self.img.blit(self.img2_org, self.img2_pos)
                self.img_rect = self.img.get_rect()
                # resize the image
                self.scale_img(self.rect.w, self.rect.h)

                self.img_rect = self.img.get_rect()
                pos_x = ((self.board.scale * self.grid_w - self.img_rect.w) // 2)
                pos_y = ((self.board.scale * self.grid_h - self.img_rect.h) // 2)
                self.img_pos = (pos_x, pos_y)
            except:
                pass

    def update(self, board, **kwargs):
        if self.update_me:
            Unit.update(self, board)
            if len(self.img_src) > 0:
                self.image.blit(self.img, self.img_pos)
            if self.unit_id == board.active_ship and self.outline is True:
                lines = [[0, 0], [self.grid_w * board.scale - 2, 0],
                         [self.grid_w * board.scale - 2, self.grid_h * board.scale - 2],
                         [0, self.grid_h * board.scale - 2]]
                pygame.draw.lines(self.image, (255, 200, 200), True, lines)
            if hasattr(self, "door_outline") and self.door_outline is True:
                self.set_outline(self.perm_outline_color, 2)
            if self.perm_outline:
                self.draw_outline()


class ImgAlphaShip(ImgShip):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), img_src='',
                 alpha=True, **kwargs):
        Ship.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha, **kwargs)
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.hasimg = True
            self.img = self.image
            self.img_pos = (0, 0)
            self.outline = False
            try:
                self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
                self.img = self.img_org
                self.img_rect = self.img.get_rect()
                # resize the image
                self.scale_img(self.rect.w, self.rect.h)

                self.img_rect = self.img.get_rect()
                pos_x = ((board.scale * self.grid_w - self.img_rect.w) // 2)
                pos_y = ((board.scale * self.grid_h - self.img_rect.h) // 2)
                self.img_pos = (pos_x, pos_y)
            except:
                pass

                # self.image.set_colorkey(self.initcolor)


class ImgCenteredShip(Ship):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), img_src='',
                 alpha=False, **kwargs):
        Ship.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha, **kwargs)
        self.change_image(img_src)

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.hasimg = True
            self.img = self.image
            self.img_pos = (0, 0)
            self.outline = False
            self.update_me = True
            try:
                if self.alpha:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
                else:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert()
                self.img = self.img_org
                self.img_rect = self.img.get_rect()
                old_h = self.img_rect.h
                old_w = self.img_rect.w
                if self.grid_x > self.grid_y:
                    new_w = self.rect.w
                    new_h = int((new_w * old_h) / old_w)
                else:
                    new_h = self.rect.h
                    new_w = int((new_h * old_w) / old_h)
                # resize the image
                self.scale_img(new_w, new_h)

                self.img_rect = self.img.get_rect()
                pos_x = ((self.board.scale * self.grid_w - self.img_rect.w) // 2)
                pos_y = ((self.board.scale * self.grid_h - self.img_rect.h) // 2)
                self.img_pos = (pos_x, pos_y)
            except:
                pass
                # self.image.set_colorkey(self.initcolor)

    def update(self, board, **kwargs):
        if self.update_me:
            Unit.update(self, board)
            if len(self.img_src) > 0:
                self.image.blit(self.img, self.img_pos)
            if self.unit_id == board.active_ship and self.outline is True:
                lines = [[0, 0], [self.grid_w * board.scale - 2, 0],
                         [self.grid_w * board.scale - 2, self.grid_h * board.scale - 2],
                         [0, self.grid_h * board.scale - 2]]
                pygame.draw.lines(self.image, (255, 200, 200), True, lines)
            if hasattr(self, "door_outline") and self.door_outline is True:
                # self.set_outline([255,0,0],2)
                self.set_outline(self.perm_outline_color, self.perm_outline_width)
            if self.perm_outline:
                self.draw_outline()


class MultiImgSprite(ImgShip):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), img_src='',
                 alpha=False, frame_flow=[0], frame_count=1, row_data=[1, 1], **kwargs):
        ImgShip.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, img_src, alpha, **kwargs)
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.hasimg = True
            self.img = self.image
            self.img_pos = (0, 0)
            self.outline = False
            self.draggable = False
            self.correction = False
            self.frame_w = grid_w * board.scale
            self.frame_h = grid_h * board.scale
            self.frame_flow = frame_flow
            self.frame_count = frame_count
            self.row_data = row_data  # [number of images per row,number of rows]
            self.correction_factor = 3.0

            self.frame = 0
            try:
                if self.alpha:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
                else:
                    self.img_org = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert()

                self.img = self.img_org
                self.img_rect = self.img.get_rect()

                # image size is most likely different than the sprite so resize is needed
                new_h = self.rect.h * self.row_data[1]
                new_w = new_h * self.img_rect.w // self.img_rect.h
                self.scale_img(new_w, new_h)
                self.img_rect = self.img.get_rect()
                pos_x = 0
                pos_y = 0
                self.img_pos = (pos_x, pos_y)
            except:
                pass

    def next_frame(self):
        if self.frame < self.frame_count - 1:
            self.frame += 1
        else:
            self.frame = 0
        xg = self.frame_flow[self.frame] % self.row_data[0]
        yg = self.frame_flow[self.frame] // self.row_data[0]
        x = -(xg * (self.frame_w - 1))
        y = -(yg * (self.frame_h - 1))
        self.img_pos = (x, y)

    def set_frame(self, frame):
        self.frame = frame
        xg = self.frame_flow[self.frame] % self.row_data[0]
        yg = self.frame_flow[self.frame] // self.row_data[0]
        if self.correction:
            # shift the image by 1px to the right every x frames - to avoid scaling problem with very long images
            shift_x = int(float(xg) / self.correction_factor)
            shift_y = int(
                float(yg) / self.correction_factor)  # int(float(self.frame_flow[self.frame]) / self.correction_factor)
        else:
            shift_x = 0
            shift_y = 0
        x = -(xg * (self.frame_w - 1)) + shift_x
        y = -(yg * (self.frame_h - 1)) + shift_y
        self.img_pos = (x, y)

        # self.img_pos = (-(self.frame_flow[self.frame]*(self.frame_w-1))+shift,0)

    def build_frame_flow(self, frame_count, frame_flow=[]):
        self.frame_count = frame_count
        if len(frame_flow) == 0:
            self.frame_flow = [i for i in range(self.frame_count)]
        else:
            self.frame_flow = frame_flow

    def reset(self):
        self.img_pos = (0, 0)
        self.frame = 0


class Door(ImgShip):
    def __init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, font_size, door_alpha=True, alpha=False, **kwargs):
        ImgShip.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, alpha=door_alpha, **kwargs)
        # (self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), img_src='',
        #         alpha=False, **kwargs)
        self.font = board.font_sizes[font_size]
        if door_alpha:
            self.color = (initcolor[0], initcolor[1], initcolor[2], 0)
        else:
            self.color = initcolor
        # self.image.set_colorkey(self.initcolor)
        self.is_door = True

    def set_pos(self, pos):
        self.grid_x = pos[0]
        self.grid_y = pos[1]
        self.rect.topleft = [pos[0] * self.board.scale + 1, pos[1] * self.board.scale + 1]


class SlidingDoor(MultiImgSprite):
    def set_pos(self, pos):
        self.grid_x = pos[0]
        self.grid_y = pos[1]
        self.rect.topleft = [pos[0] * self.board.scale + 1, pos[1] * self.board.scale + 1]


class PickUp(ImgShip):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 255, 255), img_src='',
                 alpha=False, **kwargs):
        ImgShip.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, initcolor, img_src, alpha, **kwargs)
        door_outline = False


class ImgShipRota(ImgShip):
    def turn(self, d):
        if d == [0, -1]:  # up
            self.img = self.img_org
            self.update_me = True
        elif d == [0, 1]:  # down
            self.img = self.rot_center(self.img_org, 180)
            self.update_me = True
        elif d == [1, 0]:  # right
            self.img = self.rot_center(self.img_org, 270)
            self.update_me = True
        elif d == [-1, 0]:  # left
            self.img = self.rot_center(self.img_org, 90)
            self.update_me = True


class AIUnit(ImgShipRota):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 157, 23), img_src='',
                 alpha=False, **kwargs):
        self.initcolor = initcolor
        ImgShipRota.__init__(self, board, grid_x, grid_y, grid_w, grid_h, value, self.initcolor, img_src, alpha,
                             **kwargs)
        self.unit_id = len(board.aiunits)
        self.prev_pos = [grid_x, grid_y]
        self.now_pos = [grid_x, grid_y]
        self.change_dir([[0, 1], [1, 0], [0, -1], [-1, 0]])

    def change_dir(self, possible):
        # possible_dirs = possible # [[0,1],[1,0],[0,-1],[-1,0]]
        self.move_dir = possible[random.randrange(len(possible))]


class BoardBg(Unit):
    # def update(self,screen,color,screen_w,screen_h,grid_line_w):
    def __init__(self, board, grid_x=0, grid_y=0, grid_w=1, grid_h=1, value="", initcolor=(255, 255, 255), alpha=False,
                 **kwargs):
        # self.initcolor = initcolor
        Unit.__init__(self, board, grid_x, grid_y, grid_w, grid_h, "", initcolor, alpha, **kwargs)
        self.rect.topleft = [0, 0]
        # game,self.cl_grid_line,l.screen_w-l.menu_w,l.game_h,l.grid_line_w
        if self.board.mainloop.scheme is not None:
            self.line_color = self.board.mainloop.scheme.u_line_color
        else:
            self.line_color = (240, 240, 240)  # gb.cl_grid_line
        self.screen_w = self.board.x_count * self.board.scale  # gb.l.screen_w-gb.l.menu_w
        self.screen_h = self.board.y_count * self.board.scale
        self.grid_line_w = 1

    def update(self, board, **kwargs):
        Unit.update(self, board)
        self.painting.fill(self.color)
        """
        if self.board.mainloop.scheme is not None:
            self.line_color = self.board.mainloop.scheme.u_line_color
        else:
            self.line_color = (240, 240, 240)# gb.cl_grid_line
        """
        if self.board.draw_grid:
            for row in range(self.board.x_count + 1):  # draw vertical lines
                pygame.draw.line(self.painting, self.line_color, [row * self.board.scale, 0],
                                 [row * self.board.scale, self.screen_h], self.grid_line_w)
            for column in range(self.board.y_count + 1):  # draw horizontal lines
                pygame.draw.line(self.painting, self.line_color, [0, column * self.board.scale],
                                 [self.screen_w, column * self.board.scale], self.grid_line_w)


class PuzzleTable:
    def __init__(self):
        pass

    def clean(self):
        pass


class Board:
    'Initializes and creates an empty board with the sizes given, ie. a=Board(mainloop,10,10,50)'

    def __init__(self, mainloop, x_count=10, y_count=10, scale=8):
        self.mainloop = mainloop
        self.decolorable = True
        self.draw_grid = True
        self.check_laby = False
        self.laby_dir = -1

        self.font_path_default = None
        self.font_path_default2 = None
        self.font_path_hand = None
        self.font_path_print = None

        self.load_default_fonts()
        self.level_start(x_count, y_count, scale)
        self.animation_c_set = False
        self.ac_l = 0
        self.ac_r = 0
        self.ac_t = 0
        self.ac_b = 0

    def load_default_fonts(self):
        self.font_path_default = os.path.join('res', 'fonts', self.mainloop.config.font_dir,
                                              self.mainloop.config.font_name_1)
        self.font_path_default2 = os.path.join('res', 'fonts', self.mainloop.config.font_dir,
                                               self.mainloop.config.font_name_2)
        self.font_path_hand = os.path.join('res', 'fonts', 'eduactiv8Fonts', 'eduactiv8Hand.ttf')
        self.font_path_print = os.path.join('res', 'fonts', 'eduactiv8Fonts', 'eduactiv8LatinPrint.ttf')

        self.load_fonts()

    def load_fonts(self):
        system_font_list = pygame.font.get_fonts()
        """
        if len(system_font_list) > 0:
            #print(system_font_list[0:10])
            self.font_path_hand = pygame.font.match_font(system_font_list[random.randint(0, len(system_font_list)-1)], bold=False, italic=False)
            self.font_path_print = pygame.font.match_font(system_font_list[random.randint(0, len(system_font_list)-1)], bold=False, italic=False)

            self.font_path_default = pygame.font.match_font(system_font_list[random.randint(0, len(system_font_list)-1)], bold=False, italic=False)
            self.font_path_default2 = pygame.font.match_font(system_font_list[random.randint(0, len(system_font_list)-1)], bold=False, italic=False)
        """

    def level_start(self, x_count, y_count, scale):
        self.grid = []  # square availability list
        self.ships = []  # list of movable objects on board
        self.units = []  # list of non moving units
        self.aiunits = []
        self.ai_enabled = False
        self.x_count = x_count  # number of columns
        self.y_count = y_count  # number of rows
        self.scale = scale  # number of pixels per grid unit
        self.mainloop.config.set_start_at(scale)
        self._create_board(x_count, y_count)
        self.active_ship = -1
        self.board_changed = False
        # This is a list of 'sprites.' Each block in the program is
        # added to this list. The list is managed by a class called 'RenderPlain.'
        self.unit_list = pygame.sprite.LayeredUpdates()
        self.ship_list = pygame.sprite.LayeredUpdates()
        # This is a list of every sprite. All blocks and the player block as well.
        self.all_sprites_list = pygame.sprite.LayeredUpdates()  # pygame.sprite.RenderPlain()
        # self.sprites_to_draw = pygame.sprite.RenderPlain()


        # scaling and creating font sizes:
        self.points = int(round((self.scale * 72 / 96) * 1.2, 0))

        # sizes= [0 1    2   3    4 5    6   7    8 9   10 11 11-hw 12-hw]

        # sizes = [1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,3.0,3.5,4.0]
        sizes = [1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0, 4.75, 7]
        for i in range(len(sizes)):
            sizes[i] = sizes[i] / self.mainloop.config.font_multiplier

        # test_fonts = pygame.font.get_fonts()
        # print(test_fonts)
        # trebuchetms
        # font_path = pygame.font.match_font('eufm10')
        # split_path = os.path.split(font_path)
        # print(split_path[-1])

        self.font_sizes = [pygame.font.Font(self.font_path_default, (int(float(self.points) / float(sizes[i]))))
                           for i in range(len(sizes))]
        # 12+ handwritten
        h_sizes = [25, 17, 10, 1.1, 1.5, 2, 2.3, 0.7]
        handwritten_sizes = [pygame.font.Font(self.font_path_hand, (int(float(self.points) * float(h_sizes[i]))))
                             for i in range(len(h_sizes))]
        # handwritten_sizes = [pygame.font.Font(font_path, (int(float(self.points) * float(h_sizes[i])))) for i in range(len(h_sizes))]

        self.font_sizes.extend(handwritten_sizes)
        # 20
        self.font_sizes.append(pygame.font.Font(self.font_path_print, (int(float(self.points) * float(30)))))
        # 21 - extra large normal print
        self.font_sizes.append(pygame.font.Font(self.font_path_default, (int(self.points * 2.0))))
        self.font_sizes.append(pygame.font.Font(self.font_path_default, (int(self.points * 1.5))))
        # 23 - mini clock sizes
        self.font_sizes.append(pygame.font.Font(self.font_path_default, (int(self.points / 15))))
        self.font_sizes.append(pygame.font.Font(self.font_path_default, (int(self.points / 25))))

        # 25 - h2 - title size
        self.font_sizes.append(pygame.font.Font(self.font_path_default, (int(self.points))))

        # 26 clock font
        self.font_sizes.append(pygame.font.Font(self.font_path_default2, (int(float(self.points) / float(sizes[7])))))
        # 27 credits line under word building games
        self.font_sizes.append(pygame.font.Font(self.font_path_default2, (int(float(self.points) / float(sizes[4])))))

        # extra sizes 28, 29, 30, 31, 32, 33
        xsizes = [5.5, 6.0, 6.5, 0.7, 0.9, 1]
        for i in range(len(xsizes)):
            xsizes[i] = xsizes[i] / self.mainloop.config.font_multiplier
            self.font_sizes.append(pygame.font.Font(self.font_path_default, (int(float(self.points) / float(xsizes[i])))))

        self.board_bg = BoardBg(self, 0, 0, x_count, y_count, "", (255, 255, 255))
        self.unit_list.add(self.board_bg)
        self.all_sprites_list.add(self.board_bg)

    def set_animation_constraints(self, l, r, t, b):
        self.animation_c_set = True
        self.ac_l = l
        self.ac_r = r
        self.ac_t = t
        self.ac_b = b

    def update_layout(self, scale):
        pass

    def clean(self):
        self.unit_list.empty()
        self.ship_list.empty()
        self.all_sprites_list.empty()
        # self.sprites_to_draw.empty()
        del (self.ships)
        del (self.units)
        del (self.aiunits)
        del (self.unit_list)
        del (self.ship_list)
        del (self.all_sprites_list)
        # del(self.sprites_to_draw)

    def _create_board(self, sx, sy):
        'Creates an empty board for the initialisation method'
        self.grid = [[0 for x in range(0, sx)] for y in range(0, sy)]

    def _reset_board(self):
        'Sets all fields on Board to False'
        self.grid = [[0 for x in range(0, self.x_count)] for y in range(0, self.y_count)]

    def _set(self, x, y, grid_w=1, grid_h=1, value=1):
        'Take/Reserve the position on board if True, or free position if False'
        'Before using this method use the _isfree() method first check if all squares in question are available and than go back to each field and set as True'
        x2 = x + grid_w
        y2 = y + grid_h
        for i in range(x, x2):
            for j in range(y, y2):
                self.grid[j][i] = value

    def _isfree(self, x, y, grid_w=1, grid_h=1):
        'check if the position is free and within board'
        x2 = x + grid_w
        y2 = y + grid_h

        # if position + size is within board
        if (0 <= x < x2 <= self.x_count) and (0 <= y < y2 <= self.y_count):
            for i in range(x, x2):
                for j in range(y, y2):
                    if self.grid[j][i] == True:
                        return False
            return True
        return False

    def add_unit(self, grid_x=0, grid_y=0, grid_w=1, grid_h=1, unit_class=Ship, value="A", color=(0, 0, 0), img_src='',
                 font_size=0, frame_flow=[0], frame_count=1, row_data=[1, 1], img2_src=None, alpha=False):
        'adds a new unit to the board'
        if self._isfree(grid_x, grid_y, grid_w, grid_h):
            unit = unit_class(self, grid_x, grid_y, grid_w, grid_h, value, initcolor=color, img_src=img_src,
                              font_size=font_size, frame_flow=frame_flow, frame_count=frame_count, row_data=row_data,
                              img2_src=img2_src, alpha=alpha)
            if isinstance(unit, Ship):
                if isinstance(unit, AIUnit):
                    self.aiunits.append(unit)
                else:
                    self.ships.append(unit)  # add a ship to the ship list
                self.ship_list.add(unit)  # add the ship to the sprites list
            elif isinstance(unit, Obstacle):
                self.units.append(unit)
                self.unit_list.add(unit)
            self.all_sprites_list.add(unit)
            self._set(grid_x, grid_y, grid_w, grid_h)
        else:
            print(
            'Sorry: position taken: (x:%d, y:%d, w:%d, h:%d), board size: %d x %d, game_id: %d, screen size: %d x %d' % (
            grid_x, grid_y, grid_w, grid_h, self.x_count, self.y_count, self.mainloop.m.active_game_id,
            self.mainloop.size[0], self.mainloop.size[1]))

    def add_door(self, grid_x=0, grid_y=0, grid_w=1, grid_h=1, unit_class=Door, value="", color=(0, 0, 0), img_src='',
                 font_size=0, door_alpha=True, alpha=False, frame_flow=[0], frame_count=1, row_data=[1, 1]):
        # add a unit that will be drawn to the board but will not hold a square in the grid
        # this is usually a red square indicating where other squares should be dragged to complete the task
        unit = unit_class(self, grid_x, grid_y, grid_w, grid_h, value, initcolor=color, img_src=img_src,
                          font_size=font_size, door_alpha=door_alpha, alpha=alpha, frame_flow=frame_flow, frame_count=frame_count,
                          row_data=row_data)
        self.unit_list.add(unit)
        self.units.append(unit)
        self.all_sprites_list.add(unit)

    def move(self, ship_id, x, y, ai=False):
        'move the ship, diagonal move possible only if two-step non diagonal move is possible'
        if ai == True:
            s = self.aiunits[ship_id]
        else:
            s = self.ships[self.active_ship]
        # check direction and move if fields in that direction are free
        # set out what squares need checking if move has been taken in each direction
        up = (s.grid_x, s.grid_y - 1, s.grid_w, 1)
        down = (s.grid_x, s.grid_y + s.grid_h, s.grid_w, 1)
        left = (s.grid_x - 1, s.grid_y, 1, s.grid_h)
        right = (s.grid_x + s.grid_w, s.grid_y, 1, s.grid_h)
        teleport = (s.grid_x + x, s.grid_y + y, s.grid_w, s.grid_h)

        # assign 'area to check' to direction
        if x == 0 and y == -1:
            new_rect = up
            self.laby_dir = 2
        elif x == 0 and y == 1:
            new_rect = down
            self.laby_dir = 3
        elif x == -1 and y == 0:
            new_rect = left
            self.laby_dir = 1
        elif x == 1 and y == 0:
            new_rect = right
            self.laby_dir = 0

        # diagonal move (but only for 1x1 blocks: prepare the 2 step move alternatives to check against
        # alt1a -> alternative path 1 firt move: a, second move: b
        else:
            new_rect = teleport
            if self.mainloop.game_board.allow_teleport is True:
                alt1a = (s.grid_x + x, s.grid_y + y, s.grid_w, s.grid_h)
                alt1b = (s.grid_x + x, s.grid_y + y, s.grid_w, s.grid_h)
                alt2a = (s.grid_x + x, s.grid_y + y, s.grid_w, s.grid_h)
                alt2b = (s.grid_x + x, s.grid_y + y, s.grid_w, s.grid_h)
            else:  # s.grid_w == 1 and s.grid_h == 1:
                if x <= -1 and y <= -1:  # up-left
                    alt1a = up
                    alt1b = (s.grid_x - 1, s.grid_y - 1, 1, s.grid_h)
                    alt2a = left
                    alt2b = (s.grid_x - 1, s.grid_y - 1, s.grid_w, 1)
                elif x >= 1 and y <= -1:  # up-right
                    alt1a = up
                    alt1b = (s.grid_x + s.grid_w, s.grid_y - 1, 1, s.grid_h)
                    alt2a = right
                    alt2b = (s.grid_x + 1, s.grid_y - 1, s.grid_w, 1)
                elif x <= -1 and y >= 1:  # down-left
                    alt1a = down
                    alt1b = (s.grid_x - 1, s.grid_y + 1, 1, s.grid_h)
                    alt2a = left
                    alt2b = (s.grid_x - 1, s.grid_y + s.grid_h, s.grid_w, 1)
                elif x >= 1 and y >= 1:  # down-right
                    alt1a = down
                    alt1b = (s.grid_x + s.grid_w, s.grid_y + 1, 1, s.grid_h)
                    alt2a = right
                    alt2b = (s.grid_x + 1, s.grid_y + s.grid_h, s.grid_w, 1)

        mdir = [0, 0]
        if x == 0 or y == 0:
            # standard move: check if positions are empty and move the unit
            if self._isfree(*new_rect):
                self._move_unit(ship_id, ai, x, y)
            else:
                if ai == False and s.audible:
                    self.mainloop.sfx.play(11)
        elif x != 0 and y != 0:
            if True:  # s.grid_w == 1 and s.grid_h == 1:
                self.labi_dir = -1
                # diagonal move simple path finder: check both alternatives in turn and move if possible
                # decreased number of checks to get the direction
                if self._isfree(*alt1a):  # if move up or down possible change y in first alternative
                    mdir[1] = y
                    if self._isfree(*alt1b):  # if move left or right possible change x in first alt.
                        mdir[0] = x
                    else:
                        mdir[0] = 0
                elif self._isfree(*alt2a):  # else if horizontal move possible change x first
                    mdir[0] = x
                    if self._isfree(*alt2b):  # and if second move possible change y second
                        mdir[1] = y
                    else:
                        mdir[1] = 0
                else:
                    if ai == False and s.audible:
                        self.mainloop.sfx.play(11)
                if mdir != [0, 0]:
                    self._move_unit(ship_id, ai, mdir[0], mdir[1])

    def moved(self):
        pass  # print("board - movedunit_id")

    def move_unit(self, unit_id, x, y):
        self._move_unit_to(unit_id, x, y)

    def _move_unit_to(self, unit_id, x, y):
        ship = self.units[unit_id]
        if self.check_laby is False or (self.check_laby is True and self.laby_dir > -1 and not
        self.mainloop.game_board.mylaby.get_cell(ship.grid_x, ship.grid_y).laby_doors[self.laby_dir]):
            self.laby_dir = -1
            # remove ship from board grid - take off
            self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, False)

            # change position of ship in ships list
            ship.grid_x = x
            ship.grid_y = y

            # place the ship back on board - land
            self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, True)

            # update the sprite's position
            ship.rect.topleft = [ship.grid_x * self.scale + 1, ship.grid_y * self.scale + 1]
            self.board_changed = True
            self.moved()

    def _move_unit(self, ship_id, ai, x, y):
        if ai == True:
            ship = self.aiunits[ship_id]
        else:
            ship = self.ships[ship_id]
        if self.check_laby == False or (self.check_laby == True and self.laby_dir > -1 and not
        self.mainloop.game_board.mylaby.get_cell(ship.grid_x, ship.grid_y).laby_doors[self.laby_dir]):
            self.laby_dir = -1
            # remove ship from board grid - take off
            self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, False)

            # change position of ship in ships list
            ship.grid_x += x
            ship.grid_y += y

            # place the ship back on board - land
            self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, True)

            # update the sprite's position
            ship.rect.topleft = [ship.grid_x * self.scale + 1, ship.grid_y * self.scale + 1]
            self.board_changed = True
            if ai == False:
                self.moved()
                if ship.audible:
                    self.mainloop.sfx.play(10)

    def anim_land(self, x, y):
        ship = self.ships[self.active_ship]
        # check direction and move if fields in that direction are free
        # set out what squares need checking if move has been taken in each direction
        new_rect = (x, y, ship.grid_w, ship.grid_h)
        if self._isfree(*new_rect) and self.is_within_bounds(x, y):  # if is free place unit in the square
            # remove ship from board grid - take off
            self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, False)

            # change position of ship in ships list
            ship.grid_x = x
            ship.grid_y = y
            ship.grid_last_x = x
            ship.grid_last_y = y

            # place the ship back on board - land
            self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, True)

            # update the sprite's position
            ship.rect.topleft = [ship.grid_x * self.scale + 1, ship.grid_y * self.scale + 1]
            self.board_changed = True
        else:  # return to last available location

            self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, False)

            # change position of ship in ships list
            ship.grid_x = ship.grid_last_x
            ship.grid_y = ship.grid_last_y

            # place the ship back on board - land
            self._set(ship.grid_last_x, ship.grid_last_y, ship.grid_w, ship.grid_h, True)

            # update the sprite's position
            ship.rect.topleft = [ship.grid_x * self.scale + 1, ship.grid_y * self.scale + 1]
            self.board_changed = True

    def anim_hover(self, x, y):
        # self.mainloop.info.subtitle = "%s %s %s %s %s %s" % (x, y, self.ac_l, self.ac_r, self.ac_t, self.ac_b)
        # self.mainloop.redraw_needed[1] = True
        ship = self.ships[self.active_ship]
        if x < self.ac_l:
            x = self.ac_l
        elif x >= self.ac_r:
            x = self.ac_r - 1
        if y < self.ac_t:
            y = self.ac_t
        elif y >= self.ac_b:
            y = self.ac_b - 1

        new_rect = (x, y, ship.grid_w, ship.grid_h)

        if self.is_within_bounds(x, y) and self._isfree(*new_rect):
            ship.grid_last_x = x
            ship.grid_last_y = y
        else:
            pass
            """
            new_rect = (x, y, ship.grid_w, ship.grid_h)
            if self._isfree(*new_rect):
                if self.is_within_bounds(x, y):
                    ship.grid_last_x = x
                    ship.grid_last_y = y
            """

    def _place_unit(self, ship_id, pos):
        ship = self.ships[ship_id]
        # remove ship from board grid - take off
        self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, False)

        # change position of ship in ships list
        ship.grid_x = pos[0]
        ship.grid_y = pos[1]

        # place the ship back on board - land
        self._set(ship.grid_x, ship.grid_y, ship.grid_w, ship.grid_h, True)

        # update the sprite's position
        ship.rect.topleft = [ship.grid_x * self.scale + 1, ship.grid_y * self.scale + 1]

    def is_within_bounds(self, x, y):
        if self.animation_c_set:
            if self.ac_l <= x <= self.ac_r and self.ac_t <= y <= self.ac_b:
                return True
            else:
                return False
        else:
            return True

    def follow_cursor(self, ship_id, x, y):
        ship = self.ships[ship_id]
        l = x - self.mainloop.layout.game_left
        t = y - self.mainloop.layout.info_bar_h - self.mainloop.layout.score_bar_h
        # if l > 0 and l < self.mainloop.layout.game_right - self.mainloop.layout.game_left:

        # update subtitle - logging
        # self.mainloop.info.subtitle = "%s %s %s %s" % (l, r, t, b)
        # self.mainloop.redraw_needed[1] = True

        # should the unit free movement be limited to a certain area or the entire game screen
        if self.animation_c_set:
            if l < self.ac_l * self.scale:
                ship.rect.left = self.ac_l * self.scale
            elif l > self.mainloop.layout.game_w - ship.grid_w * self.scale - (
                self.mainloop.layout.x_count - self.ac_r) * self.scale:
                ship.rect.left = self.mainloop.layout.game_w - ship.grid_w * self.scale - (
                                                                                          self.mainloop.layout.x_count - self.ac_r) * self.scale + 1
            else:
                ship.rect.left = l

            if t < self.ac_t * self.scale:
                ship.rect.top = self.ac_t * self.scale
            elif t > self.mainloop.layout.game_h - ship.grid_h * self.scale - (
                self.mainloop.layout.y_count - self.ac_b) * self.scale:
                ship.rect.top = self.mainloop.layout.game_h - ship.grid_h * self.scale - (
                                                                                         self.mainloop.layout.y_count - self.ac_b) * self.scale + 1
            else:
                ship.rect.top = t
        else:
            if l < 0:
                ship.rect.left = 0
            elif l > self.mainloop.layout.game_w - ship.grid_w * self.scale:
                ship.rect.left = self.mainloop.layout.game_w - ship.grid_w * self.scale + 1
            else:
                ship.rect.left = l

            if t < 0:
                ship.rect.top = 0
            elif t > self.mainloop.layout.game_h - ship.grid_h * self.scale:
                ship.rect.top = self.mainloop.layout.game_h - ship.grid_h * self.scale + 1
            else:
                ship.rect.top = t

    def get_unit_id(self, x, y):
        for each_unit in self.units:
            if each_unit.grid_x <= x <= each_unit.grid_x + each_unit.grid_w - 1 \
                    and each_unit.grid_y <= y <= each_unit.grid_y + each_unit.grid_h - 1:
                return each_unit.unit_id

    def activate_ship(self, x, y):
        'this only works on binary table'
        # unhighlight and repaint deactivated unit:
        if self.active_ship != -1:
            active = self.ships[self.active_ship]
            active.color = active.initcolor
            if active.outline_highlight:
                active.perm_outline_width = active.init_pow
            active.update_me = True

        # activate new unit
        for each_ship in self.ships:
            if each_ship.grid_x <= x <= each_ship.grid_x + each_ship.grid_w - 1 \
                    and each_ship.grid_y <= y <= each_ship.grid_y + each_ship.grid_h - 1:
                self.active_ship = each_ship.unit_id
                active = self.ships[self.active_ship]
                if active.allow_brightening:
                    active.color = active.brighter
                if active.outline_highlight:
                    active.perm_outline_width = 3
                active.update_me = True
                return True
        self.active_ship = -1
        return False

    @property
    def active_ship_pos(self):
        if self.active_ship > -1:
            ship = self.ships[self.active_ship]
            return (ship.grid_x, ship.grid_y)
        else:
            return (-1, -1)

    @property
    def active_val_len(self):
        if self.active_ship > -1:
            ship = self.ships[self.active_ship]
            return len(ship.value)
        else:
            return 0

    @property
    def active_sval_len(self):
        if self.active_ship > -1:
            ship = self.ships[self.active_ship]
            return len(ship.speaker_val)
        else:
            return 0

    def update_ships(self, circle_lock_pos, **kwargs):
        for each_ship in self.ships:
            """
            if each_ship.unit_id == self.active_ship:
                each_ship.color = each_ship.brighter
                if each_ship.outline_highlight:
                    each_ship.perm_outline_width = 3
            else:
                each_ship.color = each_ship.initcolor
                if each_ship.outline_highlight:
                    each_ship.perm_outline_width = each_ship.init_pow
            """
            each_ship.update(self, point=circle_lock_pos)

        for each_unit in self.units:
            each_unit.update(self)

        for each_ai in self.aiunits:
            each_ai.update(self)

        self.board_bg.update(self)
