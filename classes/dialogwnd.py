# -*- coding: utf-8 -*-

import os
import pygame

import classes.extras as ex


class DialogBtn(pygame.sprite.Sprite):
    def __init__(self, wnd, l, t, w, h, caption, img_src1, fsubmit, fargs):
        pygame.sprite.Sprite.__init__(self)
        self.wnd = wnd
        self.w = w
        self.h = h
        self.l = l
        self.t = t
        self.fsubmit = fsubmit
        self.fargs = fargs
        self.caption = ex.unival(caption)
        self.hover = False
        self.color = (255, 255, 255, 0)
        self.image = pygame.Surface([self.w, self.h], flags=pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.l, self.t]
        self.img_src1 = img_src1
        self.active_img = None
        self.load_images()

    def load_images(self):
        self.bg_tint_color = ex.hsv_to_rgb(self.wnd.mainloop.cl.color_sliders[5][0] * 16, 255, 100)
        if len(self.img_src1) > 0:
            self.img_pos = (0, 0)
            try:
                self.img1 = pygame.image.load(os.path.join('res', 'images', "dialog",  self.img_src1)).convert_alpha()
                self.img3 = pygame.image.load(os.path.join('res', 'images', "dialog", "dialog_bg_n.png")).convert_alpha()
                self.img3.fill(self.bg_tint_color, special_flags=pygame.BLEND_ADD)

                self.img4 = pygame.image.load(os.path.join('res', 'images', "dialog", "dialog_bg_h.png")).convert_alpha()
                self.img4.fill(self.bg_tint_color, special_flags=pygame.BLEND_ADD)

                self.active_img = self.img1
            except:
                pass
        self.update()

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.fsubmit(self.fargs)
            self.wnd.hide_dialog()
            self.mouse_out()
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_over()

    def set_function(self, f):
        self.fsubmit = f

    def mouse_over(self):
        self.active_img = self.img1
        if not self.hover:
            self.hover = True
            self.update()
            self.wnd.update_me = True
            self.wnd.update()

    def mouse_out(self):
        self.active_img = self.img1
        if self.hover:
            self.hover = False
            self.update()
            self.wnd.update_me = True
            self.wnd.update()

    def update(self):
        self.wnd.mainloop.flip_needed = True
        self.image.fill(self.color)
        if self.hover:
            self.image.blit(self.img4, self.img_pos)
        else:
            self.image.blit(self.img3, self.img_pos)

        if len(self.img_src1) > 0:
            self.image.blit(self.active_img, self.img_pos)


class TextRectException:
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


class DialogWnd:
    def __init__(self, mainloop):
        self.mainloop = mainloop
        self.sbg = None
        self.dialog_type = 0

        self.color = (255, 255, 255)
        self.widget_list = pygame.sprite.LayeredUpdates()
        self.widget_list2 = pygame.sprite.LayeredUpdates()

        self.elements = []

        self.elements.append(
            DialogBtn(self, 540, 0, 80, 80, "ok", "dialog_close.png", self.fsubmit_close_wnd,
                      (None)))
        self.elements.append(
            DialogBtn(self, 0, 320, 80, 80, "ok", "dialog_ok.png", self.fsubmit_none, (None)))


        for each in self.elements:
            self.widget_list.add(each)


        self.widget_list2.add(self.elements[1])

        self.bg_type = 0
        self.decor_type = 0

        self.font_size = 0

        self.font_l = pygame.font.Font(
            os.path.join('res', 'fonts', self.mainloop.config.font_dir, self.mainloop.config.font_name_1), 40)
        self.font_s = pygame.font.Font(
            os.path.join('res', 'fonts', self.mainloop.config.font_dir, self.mainloop.config.font_name_1), 20)
        self.font_xs = pygame.font.Font(
            os.path.join('res', 'fonts', self.mainloop.config.font_dir, self.mainloop.config.font_name_1), 20)
        self.default_font = None
        #self.text = ""
        #self.set_text(self.text, font=1)

        self.wnd_close_function = None
        self.load_images()

    def load_images(self):
        self.bg_tint_color = ex.hsv_to_rgb(self.mainloop.cl.color_sliders[5][0] * 16, 255, 100)
        self.font_color = ex.hsv_to_rgb(self.mainloop.cl.color_sliders[5][0] * 16, 255, 100)

        for each in self.elements:
            each.load_images()

        self.img_pos = (40, 40)
        try:
            #self.img = pygame.image.load(os.path.join('res', 'images', "dialog_bg.png")).convert_alpha()
            self.img1 = pygame.image.load(os.path.join('res', 'images', "dialog", "dialog_bg.png")).convert_alpha()
            self.img1.fill(self.bg_tint_color, special_flags=pygame.BLEND_ADD)

            self.img2 = pygame.image.load(os.path.join('res', 'images', "dialog", "dialog_bg_star.png")).convert_alpha()
            self.img2.fill(self.bg_tint_color, special_flags=pygame.BLEND_ADD)

            self.img3 = pygame.image.load(
                os.path.join('res', 'images', "dialog", "dialog_bg_d.png")).convert_alpha()

            self.img4 = pygame.image.load(
                os.path.join('res', 'images', "dialog", "dialog_bg_star_d.png")).convert_alpha()

            self.img5 = pygame.image.load(
                os.path.join('res', 'images', "dialog", "dialog_bg_allstar_d.png")).convert_alpha()
            self.images = [self.img1, self.img2]
            self.decors = [self.img3, self.img4, self.img5]
        except:
            pass

    def fsubmit_none(self, args):
        pass

    def fsubmit_close_game(self, args):
        self.hide_dialog()
        self.mainloop.done = True
        self.mainloop.done4good = True

    def flogout(self, args):
        self.hide_dialog()
        self.mainloop.done = True
        self.mainloop.window_state = "LOG IN"
        self.mainloop.userid = -1
        self.mainloop.logged_out = True
        self.mainloop.db.unset_autologin()

        self.mainloop.size = self.mainloop.wn_size[:]
        self.mainloop.fs_rescale(self.mainloop.info)
        self.mainloop.sizer.update_sizer(self.mainloop.size[0], self.mainloop.size[1])

    def fsubmit_close_wnd(self, args):
        self.hide_dialog()

    def show_dialog(self, dialog_type, txt, f=None, fc=None, bg_type=0, decor_type=0):
        self.sbg = pygame.Surface(
            (self.mainloop.sizer.screen_w, self.mainloop.sizer.screen_h),
            flags=pygame.SRCALPHA)  # the size of your rect
        self.wnd_close_function = fc
        self.mainloop.show_dialogwnd = True
        self.mainloop.redraw_needed = [True, True, True]
        self.dialog_type = dialog_type
        self.bg_type = bg_type
        self.decor_type = decor_type

        # close the game
        if dialog_type == 0:
            self.mainloop.sfx.play(2)
            self.elements[1].set_function(self.fsubmit_close_game)
            self.set_text(text=txt, font=0)
        # logout
        elif dialog_type == 1:
            self.mainloop.sfx.play(2)
            self.elements[1].set_function(self.flogout)
            self.set_text(text=txt, font=0)
        # function argument passed with the show_dialog()
        elif dialog_type == 2:
            if not self.mainloop.speaker.talkative:
                self.mainloop.sfx.play(13)
            self.elements[1].set_function(f)
            self.set_text(text=txt, font=0)
        elif dialog_type == 3:
            self.elements[1].set_function(self.fsubmit_close_wnd)
            self.set_text(text=txt, font=2)

        self.update()

    def set_font(self, font):
        self.font_size = font
        if font == 0:
            self.default_font = self.font_l
        elif font == 1:
            self.default_font = self.font_s
        elif font == 2:
            self.default_font = self.font_xs

    def set_text(self, text, font, justification=1):
        self.set_font(font)
        self.text = text
        if font == 2:
            rect = pygame.Rect((0, 0, 478, 260))
        else:
            rect = pygame.Rect((0, 0, 484, 276))
        self.text_canvas = self.render_textrect(string=self.text, font=self.default_font,
                                                rect=rect, text_color=self.font_color,
                                                background_color=(0, 0, 0, 0), justification=justification)

    def hide_dialog(self):
        self.mainloop.show_dialogwnd = False
        self.mainloop.redraw_needed = [True, True, True]
        self.mainloop.sb.update_me = True
        if self.wnd_close_function is not None:
            self.wnd_close_function()

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            pos = [event.pos[0] - self.mainloop.game_board.sizer.dialogwnd_pos[0],
                   event.pos[1] - self.mainloop.game_board.sizer.dialogwnd_pos[1]]
            found = False
            for each in self.elements:
                if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and \
                        each.rect.topleft[1] + each.rect.height >= pos[1] >= each.rect.topleft[1]:
                    each.handle(event)
                    found = True
            if not found:
                for each in self.elements:
                    each.mouse_out()
        else:
            pass

    def update(self):
        self.screen = self.mainloop.dialogwnd
        self.screenbg = self.mainloop.dialogbg
        self.sbg.fill((255, 255, 255, 180))  # this fills the entire surface
        self.screenbg.blit(self.sbg, (0, 0))
        self.mainloop.redraw_needed = [True, True, True]

        self.screen.blit(self.images[self.bg_type], self.img_pos)

        self.screen.blit(self.decors[self.decor_type], self.img_pos)
        if self.font_size == 2:
            self.screen.blit(self.text_canvas, (72, 70))
        else:
            self.screen.blit(self.text_canvas, (69, 62))

        for each in self.widget_list:
            each.update()

        if self.dialog_type < 3:
            self.widget_list.draw(self.screen)
        else:
            self.widget_list2.draw(self.screen)

    # Title: Word-wrapped text display module - render_textrect
    # Author: David Clark (da_clark at shaw.ca)
    # Submission date: May 23, 2001
    # Available at: http://www.pygame.org/pcr/text_rect/index.php

    def render_textrect(self, string, font, rect, text_color, background_color, justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.

        Takes the following arguments:

        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
                     text color. ex (0, 0, 0) = BLACK
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                        1 horizontally centered
                        2 right-justified

        Returns the following values:

        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """

        final_lines = []
        string = ex.unival(string)

        requested_lines = string.splitlines()

        # Create a series of lines that will fit on the provided
        # rectangle.

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        print("The word " + word + " is too long to fit in the rect passed.")
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Let's try to write the text out on the surface.

        surface = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
        surface.fill(background_color)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                print("Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    print("Invalid justification argument: " + str(justification))
            accumulated_height += font.size(line)[1]

        return surface
