# -*- coding: utf-8 -*-

import os
import pygame
import sys
import math
import random

import classes.extras as ex

class Colors:
    def __init__(self, mainloop):
        # Background colors
        self.outer_color = (255, 255, 255, 255)  # color outside of the frame - visible on logout

        h1 = 132
        h2 = 28
        h3 = 28
        h4 = 141
        s = 200
        v = 250

        c1 = ex.hsva_to_rgba(h1, s, 200, 255)  # bottom
        c2 = ex.hsva_to_rgba(h2, s, v, 255)  # top
        c3 = ex.hsva_to_rgba(h3, s, v, 115)  # left
        c4 = ex.hsva_to_rgba(h4, s, 20, 200)  # right

        #self.color_mono = (45, 75, 65)
        self.color_mono = (0, 0, 0, 50)
        self.android_backup_color = (45, 75, 65)

        #self.color_mono_focused = (45, 75, 65)
        self.color_mono_focused = (255, 0, 0, 100)
        self.color_mono_font = (27, 44, 39)

        """ brown
        self.color_mono = (111, 38, 12)
        self.color_mono_focused = (71, 18, 3)
        self.color_mono_font = (51, 8, 3)
        """

        self.inner_color = c2  # main frame of the panel
        self.inner_color_end = c1

        self.inner_color2 = c3  # main frame of the panel
        self.inner_color2_end = c4

        self.alpha_overlay = (255, 255, 255, 2)

        self.transparent_fill = (255, 255, 255, 0)

        # PEdit Colors
        self.bg_color = (255, 255, 255, 50)  # normal edit fields
        self.bg_focus = (255, 255, 255, 100)
        self.bg_color_disabled = (255, 255, 255, 10)  # default disabled color of the age buttons
        self.border_disabled = (255, 255, 255, 30)  # age buttons disabled

        self.border_color = self.color_mono #(128, 116, 85)
        self.border_focused = self.color_mono_focused # (118, 106, 75)

        self.font_color = self.color_mono_font #(81, 35, 4)
        self.edit_font_color = self.color_mono_font

        #Check boxes
        self.cb_bg_col = (255, 255, 255, 0)
        self.cb_color = (255, 255, 255, 50)
        self.cb_focus = (255, 255, 255, 100)
        self.cb_border_color = (0, 0, 0)
        self.cb_border_focused = (255, 0, 0)

        #PButon
        self.btn_bg_color = (255, 255, 255, 50)  # all butons and non selected age buttons
        self.btn_bg_focus = (255, 255, 255, 100)  # selected state age and focus on buttons
        self.btn_font_color = self.color_mono_font  # (52, 17, 2)
        self.trans_btn_font_color = (255, 85, 85)

        self.btn_border_color = self.color_mono #(26, 6, 0)
        self.btn_border_focused = self.color_mono_focused #(72, 17, 2)
        self.btn_border_color_l = self.color_mono #(26, 6, 0)
        self.btn_border_focused_l = self.color_mono_focused #(72, 17, 2)

        self.c2a_btn_bg_color = (25, 255, 25, 125)  # all butons and non selected age buttons
        self.c2a_btn_bg_focus = (55, 255, 55, 150)  # selected state age and focus on buttons

        #PScrollBar
        self.slb_bg_color = (255, 255, 255, 50)
        self.slb_bg_focus = (255, 255, 255, 100)
        self.slb_border_color = self.color_mono
        self.slb_border_focused = self.color_mono_focused
        self.slb_mid_lines = self.color_mono

        #LoginScreen
        self.ls_font_color = self.color_mono_font #(81, 35, 4)
        self.ls_header_font_color = self.color_mono_font #(255, 179, 111)
        self.ls_bg_col = (255, 255, 255, 70)  # main panel
        self.bg_col = self.ls_bg_col
        self.ls_bg_sidecol = (0, 0, 0, 50)  # menu panel

        #Keyboard Key
        self.key_bg_color_normal = (255, 255, 255, 70)
        self.key_bg_color_activated = (255, 255, 255, 130)
        self.key_bg_color_disabled = self.inner_color
        self.key_bg_color = self.bg_color_disabled


        self.key_bg_color_mouse_dn = (255, 255, 255, 130)
        self.key_bg_color_mouse_ovr = (255, 255, 255, 100)

        self.key_border_disabled = (62, 17, 2)
        self.key_bg_focus = (255, 255, 255, 100)
        self.key_border_color = (0, 0, 0)
        self.key_border_focused = (255, 0, 0)
        self.key_font_color = self.color_mono_font #(81, 35, 4)

    def fill_gradient(self, surface, color, gradient, rect=None, vertical=True, forward=True):
        """fill a surface with a gradient pattern
        Parameters:
        color -> starting color
        gradient -> final color
        rect -> area to fill; default is surface's rect
        vertical -> True=vertical; False=horizontal
        forward -> True=forward; False=reverse

        Pygame recipe: http://www.pygame.org/wiki/GradientCode
        """

        if rect is None:
            rect = surface.get_rect()
        x1, x2 = rect.left, rect.right
        y1, y2 = rect.top, rect.bottom

        if vertical:
            h = y2 - y1
        else:
            h = x2 - x1
        if forward:
            a, b = color, gradient
        else:
            b, a = color, gradient
        rate = (
            float(b[0] - a[0]) / h,
            float(b[1] - a[1]) / h,
            float(b[2] - a[2]) / h,
            float(b[3] - a[3]) / h
        )
        fn_line = pygame.draw.line
        if vertical:
            for line in range(y1, y2):
                color = (
                    int(min(max(a[0] + (rate[0] * (line - y1)), 0), 255)),
                    int(min(max(a[1] + (rate[1] * (line - y1)), 0), 255)),
                    int(min(max(a[2] + (rate[2] * (line - y1)), 0), 255)),
                    int(min(max(a[3] + (rate[3] * (line - y1)), 0), 255))
                )
                fn_line(surface, color, (x1, line), (x2, line))
        else:
            for col in range(x1, x2):
                color = (
                    int(min(max(a[0] + (rate[0] * (col - x1)), 0), 255)),
                    int(min(max(a[1] + (rate[1] * (col - x1)), 0), 255)),
                    int(min(max(a[2] + (rate[2] * (col - x1)), 0), 255)),
                    int(min(max(a[3] + (rate[3] * (col - x1)), 0), 255))
                )
                fn_line(surface, color, (col, y1), (col, y2))

class PEdit(pygame.sprite.Sprite):
    def __init__(self, ls, w, h, l, t, focus_order, hide=False, right_align=False, transparent=False):
        pygame.sprite.Sprite.__init__(self)
        self.ls = ls
        self.w = w
        self.h = h
        self.left = l
        self.top = t
        self.focus_order = focus_order
        self.hide = hide
        self.right_align = right_align
        if not self.ls.lang.ltr_text and not isinstance(self, PButton):
            self.right_align = True
        self.transparent = transparent
        # self.value = "Tejsζę"
        self.value = ""
        self.visible = True
        self.select_item = False
        self.checked = False
        self.disabled = False
        self.users = False
        # self.displayed_value = ""
        self.cursor_pos = 0
        self.focused = False
        self.update_me = True
        # self.color = (255,255,255)
        # self.bg_color = (255,255,255)
        self.bg_color = self.ls.colors.bg_color
        self.bg_color_disabled = self.ls.colors.bg_color_disabled
        self.border_disabled = self.ls.colors.border_disabled
        self.bg_focus = self.ls.colors.bg_focus
        self.border_color = self.ls.colors.border_color
        self.border_focused = self.ls.colors.border_focused
        self.font_color = self.ls.colors.font_color

        self.lines = [[0, 0], [self.w - 1, 0], [self.w - 1, self.h - 1], [0, self.h - 1]]
        self.lines_focused = [[0, 0], [self.w - 2, 0], [self.w - 2, self.h - 2], [0, self.h - 2]]
        self.image = pygame.Surface([w, h], flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [l, t]
        self.update()

    def update(self):
        if self.update_me and self.visible:
            # self.update_me = False
            if self.users:
                if self.focused or self.checked:
                    self.image.fill(self.bg_focus)
                    pygame.draw.line(self.image, self.border_focused, self.lines[0], self.lines[1], 1)
                    pygame.draw.line(self.image, self.border_focused, self.lines[2], self.lines[3], 1)
                    pygame.draw.line(self.image, self.border_focused, self.lines[0], self.lines[3], 1)
                else:
                    self.image.fill(self.bg_color)
                    # pygame.draw.lines(self.image, self.border_color, True, self.lines,1)
                    pygame.draw.line(self.image, self.border_color, self.lines[0], self.lines[1], 1)
                    pygame.draw.line(self.image, self.border_color, self.lines[2], self.lines[3], 1)
                    pygame.draw.line(self.image, self.border_color, self.lines[0], self.lines[3], 1)
            else:
                if self.disabled:
                    self.image.fill(self.bg_color_disabled)
                    pygame.draw.lines(self.image, self.border_color, True, self.lines, 2)
                elif self.focused or self.checked:
                    self.image.fill(self.bg_focus)
                    pygame.draw.lines(self.image, self.border_focused, True, self.lines_focused, 2)
                else:
                    self.image.fill(self.bg_color)
                    pygame.draw.lines(self.image, self.border_color, True, self.lines, 1)
            if self.hide:
                val = ""
                for i in range(len(self.value)):
                    val += "*"
            else:
                if sys.version_info < (3, 0):
                    try:
                        val = unicode(self.value, "utf-8")
                    except UnicodeDecodeError:
                        val = self.value
                    except TypeError:
                        val = self.value
                else:
                    val = self.value
            text = self.ls.font_2.render("%s" % (val), 1, self.ls.colors.edit_font_color)

            if self.select_item:
                self.font_x = (self.w - self.ls.font_2.size(val)[0]) // 2
            else:
                if self.right_align:
                    self.font_x = (self.w - self.ls.font_2.size(val)[0]) - 5
                else:
                    if isinstance(self, PButton):
                        self.font_x = (self.w - self.ls.font_2.size(val)[0]) // 2
                    else:
                        self.font_x = 5
            self.font_y = (self.h - self.ls.font_2.size(val)[1]) // 2

            self.image.blit(text, (self.font_x, self.font_y))
            self.image.blit(text, (self.font_x, self.font_y))
        elif self.update_me and not self.visible:
            self.image.fill(self.bg_color)

    def handle(self, event):
        if self.visible:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.onMouseButtonDown()
            if event.type == pygame.MOUSEBUTTONUP:
                self.onMouseButtonUp()
            if event.type == pygame.KEYDOWN:
                self.onKeyDown(event)

    def is_editable(self):
        return True

    def onKeyDown(self, event):
        if not self.select_item:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                pass
            elif event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER and event.key != pygame.K_TAB:
                lhv = len(self.value)
                if event.key == pygame.K_BACKSPACE:
                    if lhv > 0:
                        if self.ls.lang.ltr_text:
                            self.value = self.value[0:lhv - 1]
                        else:
                            self.value = self.value[1:lhv]
                else:
                    char = event.unicode
                    if len(char) > 0 and lhv < 21:
                        if self.ls.lang.ltr_text:
                            self.value = self.value + char
                        else:
                            self.value = char + self.value
                self.ls.reload_selects()
                self.ls.set_scrollbar_top(self.ls.scroll_min_top)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_TAB:
                self.nextFocus()

            self.update_trigger()

    def onMouseButtonDown(self):
        self.onFocus()
        if self.select_item and self.focus_order > -1 and self.ls.state == "LOGIN":
            if self.value != "":
                if self.ls.username_count > 5:
                    self.onBlur()
                self.ls.username.value = self.value

                self.ls.reload_selects()
                if self.ls.require_pass:
                    if ex.unival(self.ls.username.value) != ex.unival(self.ls.lang.b["Guest"]):
                        if self.ls.username_count > 5:
                            self.ls.in_focus = self.ls.password
                            self.ls.password.onFocus()
                    else:
                        pass
                        # self.ls.in_focus = self.ls.loginbtn
                        # self.ls.update_me = True
                        # self.ls.loginbtn.onFocus()
                        # self.ls.flogin()
                else:
                    pass
                    # self.ls.in_focus = self.ls.username
                    # self.ls.username.onFocus()
                    # self.ls.flogin()

                self.ls.set_scrollbar_top(self.ls.scroll_min_top)
        elif self.select_item and self.focus_order > -1 and self.ls.state == "FONTS":
            self.ls.update_sample_font(self.value)
        if self.users and self.focus_order > -1 and self.ls.state == "USERS":
            self.ls.fdetails(self.value)

    def onMouseButtonUp(self):
        pass

    def onFocus(self):
        if self.select_item is False or (self.select_item and len(self.value) > 0):
            self.focused = True
            self.update_trigger()

    def onBlur(self):
        self.focused = False
        self.update_trigger()

    def nextFocus(self):
        self.ls.nextFocus(self.focus_order)

    def update_trigger(self):
        self.update_me = True
        self.ls.update_me = True
        self.ls.mainloop.redraw_needed[0] = True



class PSelect(PEdit):
    def __init__(self, ls, w, h, l, t, focus_order, right_align=False, transparent=False):
        PEdit.__init__(self, ls, w, h, l, t, focus_order, False, right_align, transparent)

    def is_editable(self):
        return False


class PCheckbox(pygame.sprite.Sprite):
    def __init__(self, ls, w, h, l, t, checked, value, hide=False):
        pygame.sprite.Sprite.__init__(self)
        self.ls = ls
        self.w = w
        self.h = h
        self.left = l
        self.top = t
        self.focus_order = -1
        self.hide = hide
        self.value = value
        self.select_item = False
        self.checked = checked
        self.cursor_pos = 0
        self.focused = False
        self.update_me = True
        self.bg_color = self.ls.colors.cb_bg_col
        self.cb_color = self.ls.colors.cb_color
        self.cb_focus = self.ls.colors.cb_focus
        self.visible = True

        if self.ls.lang.ltr_text:
            self.right_align = False
            self.lines = [[0, 5], [20, 5], [20, 25], [0, 25]]
            self.cbtick = [[3, 15], [8, 20], [17, 10]]
        else:
            self.right_align = True
            self.lines = [[w - 0 - 3, h - 5], [w - 20 - 3, h - 5], [w - 20 - 3, h - 25], [w - 0 - 3, h - 25]]
            self.cbtick = [[w - 20 + 3 - 3, 15], [w - 20 + 8 - 3, 20], [w - 20 + 17 - 3, 10]]

        self.border_color = self.ls.colors.cb_border_color
        self.border_focused = self.ls.colors.cb_border_focused

        self.font_color = self.ls.font_color
        self.image = pygame.Surface([w, h], flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [l, t]

    def update(self):
        if self.visible and self.update_me:
            # self.update_me = False
            self.image.fill(self.bg_color)
            pygame.draw.polygon(self.image, self.cb_focus, self.lines, 0)
            if self.focused:
                pygame.draw.lines(self.image, self.border_focused, True, self.lines, 1)
            else:
                pygame.draw.lines(self.image, self.border_color, True, self.lines, 1)

            if self.checked:
                pygame.draw.lines(self.image, self.border_color, False, self.cbtick, 3)

            if sys.version_info < (3, 0):
                try:
                    val = unicode(self.value, "utf-8")
                except UnicodeDecodeError:
                    val = self.value
                except TypeError:
                    val = self.value
            else:
                val = self.value
            text = self.ls.font_2.render("%s" % (val), 1, self.font_color)
            if self.right_align:
                font_x = (self.w - self.ls.font_2.size(val)[0]) - 35
            else:
                font_x = 30
            font_y = (self.h - self.ls.font_2.size(val)[1]) // 2
            self.image.blit(text, (font_x, font_y))
        elif self.update_me:
            self.image.fill(self.bg_color)

    def handle(self, event):
        if self.visible:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.onMouseButtonDown()
            if event.type == pygame.MOUSEBUTTONUP:
                self.onMouseButtonUp()
            if event.type == pygame.KEYDOWN:
                self.onKeyDown(event)

    def onKeyDown(self, event):
        pass

    def onMouseButtonDown(self):
        self.onFocus()
        if self.checked:
            self.checked = False
        else:
            self.checked = True

    def onMouseButtonUp(self):
        pass

    def onFocus(self):
        if not self.select_item or (self.select_item and len(self.value) > 0):
            self.focused = True
            self.update_trigger()

    def onBlur(self):
        self.focused = False
        self.update_trigger()

    def nextFocus(self):
        self.ls.nextFocus(self.focus_order)

    def update_trigger(self):
        self.update_me = True
        self.ls.update_me = True
        self.ls.mainloop.redraw_needed[0] = True


class PLabel(pygame.sprite.Sprite):
    def __init__(self, ls, w, h, l, t, value):
        pygame.sprite.Sprite.__init__(self)
        self.ls = ls
        self.w = w
        self.h = h
        self.left = l
        self.top = t
        self.focus_order = -1
        if self.ls.lang.ltr_text:
            self.right_align = False
        else:
            self.right_align = True
        self.font_color = self.ls.colors.font_color
        self.value = value
        self.select_item = False
        self.update_me = True
        self.image = pygame.Surface([w, h], flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [l, t]
        self.font_v = self.ls.font_2

    def update(self):
        if self.update_me:
            self.image.fill(self.ls.colors.transparent_fill)
            if sys.version_info < (3, 0):
                try:
                    val = unicode(self.value, "utf-8")
                except UnicodeDecodeError:
                    val = self.value
                except TypeError:
                    val = self.value
            else:
                val = self.value
            try:
                text = self.font_v.render("%s" % val, 1, self.font_color)

                if self.right_align:
                    self.font_x = (self.w - self.font_v.size(val)[0]) - 5
                else:
                    self.font_x = 0
                self.font_y = (self.h - self.font_v.size(val)[1]) // 2

                self.image.blit(text, (self.font_x, self.font_y))
            except:
                pass

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.onMouseButtonDown()
        if event.type == pygame.MOUSEBUTTONUP:
            self.onMouseButtonUp()
        if event.type == pygame.KEYDOWN:
            self.onKeyDown(event)

    def onKeyDown(self, event):
        pass

    def onMouseButtonDown(self):
        pass

    def onMouseButtonUp(self):
        pass

    def onFocus(self):
        pass

    def onBlur(self):
        pass

    def nextFocus(self):
        pass


class PButton(PEdit):
    def __init__(self, ls, w, h, l, t, focus_order, value, fsubmit, right_align=False, transparent=False):
        PEdit.__init__(self, ls, w, h, l, t, focus_order, False, right_align, transparent)
        self.value = value
        self.fsubmit = fsubmit
        self.checked = False
        if not self.transparent:
            # self.bg_color = (205,255,155)
            self.bg_color = self.ls.colors.btn_bg_color
            self.bg_focus = self.ls.colors.btn_bg_focus
            self.font_color = self.ls.colors.btn_font_color
            self.border_color = self.ls.colors.btn_border_color
            self.border_focused = self.ls.colors.btn_border_focused
        else:
            self.bg_color = self.ls.colors.transparent_fill
            self.bg_focus = self.ls.colors.transparent_fill
            self.font_color = self.ls.colors.trans_btn_font_color
            self.border_color = self.ls.colors.transparent_fill
            self.border_focused = self.ls.colors.transparent_fill

    def onKeyDown(self, event):
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.fsubmit()
            self.update_trigger()

    def is_editable(self):
        return False

    def onMouseButtonUp(self):
        pass

    def onMouseButtonDown(self):
        PEdit.onMouseButtonDown(self)
        self.onFocus()

        self.fsubmit()
        self.update_trigger()

    def set_call2action_style(self):
        self.bg_color = self.ls.colors.c2a_btn_bg_color
        self.bg_focus = self.ls.colors.c2a_btn_bg_focus


class PButton2(PButton):
    def __init__(self, ls, w, h, l, t, focus_order, value, fsubmit, right_align=False, transparent=False):
        self.font_v = ls.font_1
        self.font_v2 = ls.font_2
        self.value2 = ""
        PButton.__init__(self, ls, w, h, l, t, focus_order, value, fsubmit, right_align=right_align,
                         transparent=transparent)
        self.disabled = True

    def set_value2(self, txt):
        self.value2 = txt
        self.update_me = True

    def update(self):
        if self.update_me:
            if self.disabled:
                self.image.fill(self.bg_color_disabled)
                pygame.draw.lines(self.image, self.border_disabled, True, self.lines, 2)
            elif self.focused or self.checked:
                self.image.fill(self.bg_focus)
                pygame.draw.lines(self.image, self.border_focused, True, self.lines_focused, 2)
            else:
                self.image.fill(self.bg_color)
                pygame.draw.lines(self.image, self.border_color, True, self.lines, 1)

            val = ex.unival(self.value)

            text = self.font_v.render(val, 1, self.font_color)

            font_x = (self.w - self.font_v.size(val)[0]) // 2
            if self.value2:
                val2 = ex.unival(self.value2)
                text2 = self.font_v2.render(val2, 1, self.font_color)
                font_y = 0
                font_x2 = (self.w - self.font_v2.size(val2)[0]) // 2
                font_y2 = 25
                self.image.blit(text2, (font_x2, font_y2))
            else:
                font_y = (self.h - self.font_v.size(val)[1]) // 2
            # double blit due to a problem with semi-transparent background - especially with Hebrew letters
            self.image.blit(text, (font_x, font_y))
            self.image.blit(text, (font_x, font_y))
            if self.ls.mainloop.lang.lang == "he":
                self.image.blit(text, (font_x, font_y))
                self.image.blit(text, (font_x, font_y))


class PScrollBar(pygame.sprite.Sprite):
    def __init__(self, ls, w, h, l, t, focus_order, hide=False):
        pygame.sprite.Sprite.__init__(self)
        self.ls = ls
        self.w = w
        self.h = h
        self.left = l
        self.top = t
        self.focus_order = focus_order
        self.hide = hide
        self.dist2top = 0
        self.value = ""
        self.select_item = False
        self.cursor_pos = 0
        self.focused = False
        self.update_me = True
        self.bg_color = self.ls.colors.slb_bg_color
        self.bg_focus = self.ls.colors.slb_bg_focus
        self.border_color = self.ls.colors.slb_border_color
        self.border_focused = self.ls.colors.slb_border_focused
        self.line_focused_w = 2
        self.rect_init()

    def rect_init(self):
        self.image = pygame.Surface([self.w, self.h], flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.left, self.top]

        self.lines = [[0, 0], [self.w - 1, 0], [self.w - 1, self.h - 1], [0, self.h - 1]]
        self.lines_focused = [[0, 0], [self.w - 2, 0], [self.w - 2, self.h - 2], [0, self.h - 2]]

    def update(self):
        if self.update_me:
            if self.focused:
                if self.ls.usr_count > 5:
                    self.image.fill(self.bg_focus)
                    pygame.draw.lines(self.image, self.border_focused, True, self.lines_focused, 2)
                else:
                    self.image.fill(self.bg_color)
                    pygame.draw.lines(self.image, self.border_color, True, self.lines, 1)
            else:
                self.image.fill(self.bg_color)
                pygame.draw.lines(self.image, self.border_color, True, self.lines, 1)
            s = [[3, self.h // 2 - 5], [5, self.h // 2], [3, self.h // 2 + 5]]
            e = [[self.w - 3, self.h // 2 - 5], [self.w - 5, self.h // 2], [self.w - 3, self.h // 2 + 5]]
            for i in range(3):
                pygame.draw.line(self.image, self.ls.colors.slb_mid_lines, s[i], e[i], 1)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.onMouseButtonDown(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self.onMouseButtonUp()
        if event.type == pygame.KEYDOWN:
            self.onKeyDown(event)

    def onKeyDown(self, event):
        pass

    def onMouseButtonDown(self, event):
        self.onFocus()
        self.ls.scroll_down = True
        self.dist2top = event.pos[1] - self.top

    def onMouseButtonUp(self):
        pass

    def onFocus(self):
        if self.select_item == False or (self.select_item and len(self.value) > 0):
            self.focused = True
            self.update_trigger()

    def onBlur(self):
        self.focused = False
        self.update_trigger()

    def nextFocus(self):
        self.ls.nextFocus(self.focus_order)

    def update_trigger(self):
        self.update_me = True
        self.ls.update_me = True
        self.ls.mainloop.redraw_needed[0] = True


class PIMGButton(pygame.sprite.Sprite):
    def __init__(self, ls, w, h, l, t, focus_order, img_src, img_src2, fsubmit):
        pygame.sprite.Sprite.__init__(self)
        self.ls = ls
        self.w = w
        self.h = h
        self.left = l
        self.top = t
        self.value = ""
        self.hover = False
        self.focused = False
        self.highlight = False
        self.select_item = False
        self.focus_order = focus_order
        self.fsubmit = fsubmit
        self.img_src = img_src
        self.img_src2 = img_src2
        self.update_me = True
        self.visible = True
        self.bg_color = (255, 250, 200, 0)

        #self.lines = [[0, 0], [self.w - 1, 0], [self.w - 1, self.h - 1], [0, self.h - 1]]
        #self.lines_focused = [[0, 0], [self.w - 2, 0], [self.w - 2, self.h - 2], [0, self.h - 2]]
        self.image = pygame.Surface([w, h], flags=pygame.SRCALPHA)
        self.img_loaded = False
        try:
            self.img = pygame.image.load(os.path.join('res', 'images', self.img_src)).convert_alpha()
            self.img2 = pygame.image.load(os.path.join('res', 'images', self.img_src2)).convert_alpha()
            self.img_pos = (0, 0)
            self.img_loaded = True
        except IOError:
            pass
        self.rect = self.image.get_rect()
        self.rect.topleft = [l, t]

    def update(self):
        if self.update_me and self.visible:
            self.image.fill(self.bg_color)
            if self.img_loaded:
                if self.hover:
                    self.image.blit(self.img2, self.img_pos)
                else:
                    self.image.blit(self.img, self.img_pos)

        elif self.update_me and not self.visible:
            self.image.fill(self.bg_color)

    def handle(self, event):
        if self.visible:
            if event.type == pygame.MOUSEMOTION:
                self.onMouseMotion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.onMouseButtonDown()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.onMouseButtonUp()
            elif event.type == pygame.KEYDOWN:
                self.onKeyDown(event)

    def onMouseButtonDown(self):
        self.onFocus()

    def onMouseButtonUp(self):
        self.fsubmit()
        self.update_trigger()

    def onMouseMotion(self, event):
        if not self.highlight:
            pos = event.pos
            if self.rect.topleft[0] + self.rect.width - 10 >= pos[0] >= self.rect.topleft[0] + 10 and self.rect.topleft[
                1] + self.rect.height - 10 >= pos[1] >= self.rect.topleft[1] + 10:
                if self.hover == False:
                    self.update_trigger()
                self.hover = True
            else:
                if self.hover == True:
                    self.update_trigger()
                self.hover = False

    def onFocus(self):
        pass

    def onBlur(self):
        pass

    def nextFocus(self):
        pass

    def update_trigger(self):
        self.update_me = True
        self.ls.update_me = True
        self.ls.mainloop.redraw_needed[0] = True

    def onKeyDown(self, event):
        pass

class KbrdKey(pygame.sprite.Sprite):
    def __init__(self, ls, x, y, w, h, lower, upper, fcode = 0):
        pygame.sprite.Sprite.__init__(self)
        self.label_lower = lower
        self.label_upper = upper
        self.case = 1  # 1 - lower, -1 - upper
        self.enabled = True
        self.fcode = fcode
        self.mouse_dn = False
        self.mouse_ovr = False

        self.ls = ls

        #size and position
        self.x = x+1
        self.y = y+1
        self.w = w-2
        self.h = h-2

        self.font_x = 0
        self.font_y = 0

        self.bg_color_normal = self.ls.colors.key_bg_color_normal
        self.bg_color_activated = self.ls.colors.key_bg_color_activated
        self.bg_color_disabled = self.ls.colors.key_bg_color_disabled
        self.bg_color_mouse_dn = self.ls.colors.key_bg_color_mouse_dn
        self.bg_color_mouse_ovr = self.ls.colors.key_bg_color_mouse_ovr
        self.bg_color = self.bg_color_disabled

        self.border_disabled = self.ls.colors.key_border_disabled
        self.bg_focus = self.ls.colors.key_bg_focus
        self.border_color = self.ls.colors.key_border_color
        self.border_focused = self.ls.colors.key_border_focused
        self.font_color = self.ls.colors.key_font_color

        self.lines = [[0, 0], [self.w - 1, 0], [self.w - 1, self.h - 1], [0, self.h - 1]]
        self.lines_focused = [[0, 0], [self.w - 2, 0], [self.w - 2, self.h - 2], [0, self.h - 2]]
        self.image = pygame.Surface([self.w, self.h], flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

        self.font_v = self.ls.font_3
        self.update()

    def change_case(self):
        self.case *= -1

    def get_value(self):
        if self.case == 1:
            return self.label_lower
        else:
            return self.label_upper

    def enable(self, enable=True):
        self.enabled = enable
        if self.enabled:
            self.bg_color = self.bg_color_normal
            if self.fcode == 2:
                self.activate_color()
        else:
            self.bg_color = self.bg_color_disabled
        self.update()

    def activate_color(self): #use on shift only
        if self.case == 1:
            self.bg_color = self.bg_color_normal
        else:
            self.bg_color = self.bg_color_activated
        self.ls.update_me = True
        self.update()

    def update(self):
        if self.mouse_dn:
            self.image.fill(self.bg_color_mouse_dn)
        elif self.mouse_ovr:
            self.image.fill(self.bg_color_mouse_ovr)
        else:
            self.image.fill(self.bg_color)

        if sys.version_info < (3, 0):
            try:
                val = unicode(self.get_value(), "utf-8")
            except UnicodeDecodeError:
                val = self.get_value()
            except TypeError:
                val = self.get_value()
        else:
            val = self.get_value()
        try:
            text = self.font_v.render("%s" % (val), 1, self.font_color)
            self.font_x = (self.w - self.font_v.size(val)[0]) // 2
            self.font_y = (self.h - self.font_v.size(val)[1]) // 2
            self.image.blit(text, (self.font_x, self.font_y))
        except:
            pass

    def mouse_down(self):
        if not self.mouse_dn:
            self.mouse_dn = True
            self.ls.update_me = True
            self.ls.mainloop.redraw_needed[0] = True

    def mouse_up(self):
        if self.mouse_dn:
            self.mouse_dn = False
            self.ls.update_me = True
            self.ls.mainloop.redraw_needed[0] = True

    def mouse_over(self):
        if not self.mouse_ovr:
            self.mouse_ovr = True
            self.ls.update_me = True
            self.ls.mainloop.redraw_needed[0] = True

    def mouse_out(self):
        if self.mouse_ovr:
            self.mouse_ovr = False
            self.ls.update_me = True
            self.ls.mainloop.redraw_needed[0] = True

    def handle(self, event):
        if self.enabled:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #pos = event.pos
                if self.fcode == 2: # shift
                    self.ls.keyboard.shift_it()
                    self.activate_color()
                elif self.ls.in_focus is not None:
                    lhv = len(self.ls.in_focus.value)
                    if isinstance(self.ls.in_focus, PEdit):
                        if self.fcode == 0: # key
                            char = ex.unival(self.get_value())
                            if len(char) > 0 and lhv < 21:
                                if self.ls.lang.ltr_text:
                                    self.ls.in_focus.value = ex.unival(self.ls.in_focus.value) + char
                                else:
                                    self.ls.in_focus.value = char + ex.unival(self.ls.in_focus.value)
                        if self.fcode == 1: # backspace
                            if lhv > 0:
                                if self.ls.lang.ltr_text:
                                    self.ls.in_focus.value = self.ls.in_focus.value[0:lhv - 1]
                                else:
                                    self.ls.in_focus.value = self.ls.in_focus.value[1:lhv]
                        if self.ls.username_count > 5:
                            self.ls.reload_selects()
                        self.ls.set_scrollbar_top(self.ls.scroll_min_top)
                        self.ls.in_focus.update_trigger()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pass


class Keyboard:
    def __init__(self, ls, x, y, w, h):
        self.ls = ls
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.enabled = False

        self.keys = pygame.sprite.LayeredUpdates()
        self.key_size = 0
        self.alpha_len = 0
        self.add_keys()

    def add_keys(self):
        self.keys.empty()
        self.alpha_len = len(self.ls.lang.alphabet_lc)
        self.all_key_count = self.alpha_len + 11 + 8
        self.keys_per_line = int(math.ceil(self.all_key_count / 3))

        self.last_key_len = 4 - (self.all_key_count - self.keys_per_line * 3)
        self.key_w = self.w // self.keys_per_line
        self.margin = (self.w - (self.key_w * self.keys_per_line)) // 2
        self.key_h = self.h // 3

        self.extra_chars = ["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.lower_list = self.ls.lang.alphabet_lc[:]
        self.upper_list = self.ls.lang.alphabet_uc[:]
        self.lower_list.extend(self.extra_chars)
        self.upper_list.extend(self.extra_chars)
        if self.ls.lang.ltr_text:
            bsp_key = "←"
            for i in range(self.all_key_count - 8):
                if i < self.keys_per_line-2:
                    j = 0
                elif i < self.keys_per_line * 2-4:
                    j = 1
                else:
                    j = 2
                x = self.margin + self.x + (i - j * (self.keys_per_line-2)) * self.key_w
                y = self.y + j * self.key_h

                key = KbrdKey(self.ls, x, y, self.key_w, self.key_h, self.lower_list[i], self.upper_list[i])
                self.keys.add(key)
            # add backspace, shift and space
            key = KbrdKey(self.ls, self.margin + self.x + (self.keys_per_line - 2) * self.key_w, self.y, self.key_w * 2,
                          self.key_h, bsp_key, bsp_key, 1)
            self.bsp_key = key
            self.keys.add(key)
            key = KbrdKey(self.ls, self.margin + self.x + (self.keys_per_line - 2) * self.key_w, self.y + self.key_h,
                          self.key_w * 2, self.key_h, "⌂", "⌂", 2)
            self.shift_key = key
            self.keys.add(key)
            key = KbrdKey(self.ls, self.margin + self.x + (self.keys_per_line - self.last_key_len) * self.key_w,
                          self.y + self.key_h * 2, self.key_w * self.last_key_len, self.key_h, " ", " ")
            self.space_key = key
            self.keys.add(key)
        else:
            bsp_key = "→"
            for i in range(self.all_key_count - 8):
                if i < self.keys_per_line-2:
                    j = 0
                elif i < self.keys_per_line * 2-4:
                    j = 1
                else:
                    j = 2
                x = self.margin + self.x + (self.keys_per_line - 1 - (i - j * (self.keys_per_line-2))) * self.key_w
                y = self.y + j * self.key_h

                key = KbrdKey(self.ls, x, y, self.key_w, self.key_h, self.lower_list[i], self.upper_list[i])
                self.keys.add(key)
            # add backspace, shift and space
            key = KbrdKey(self.ls, self.margin + self.x, self.y, self.key_w * 2, self.key_h * 2, bsp_key, bsp_key, 1)
            self.bsp_key = key
            self.keys.add(key)
            key = KbrdKey(self.ls, self.margin + self.x, self.y + self.key_h * 2, self.key_w * (self.last_key_len),
                          self.key_h, " ", " ")
            self.space_key = key
            self.keys.add(key)

    def shift_it(self):
        for each in self.keys:
            each.change_case()
        self.update()
        self.ls.update_me = True

    def enable(self, enabled=True):
        for each in self.keys:
            each.enable(enabled)
        self.enabled = enabled
        #self.ls.db_status = " "
        self.ls.update_me = True

    def update(self):
        for each in self.keys:
            each.update()
        self.keys.draw(self.ls.screen)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            for each in self.keys:
                if each.x < pos[0] < each.x + each.w and each.y < pos[1] < each.y + each.h:
                    each.mouse_over()
                    #each.handle(event)
                else:
                    each.mouse_out()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.enabled:
                pos = event.pos
                for each in self.keys:
                    if each.x < pos[0] < each.x + each.w and each.y < pos[1] < each.y + each.h:
                        each.mouse_down()
                        each.handle(event)
                    else:
                        each.mouse_up()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.enabled:
                pos = event.pos
                for each in self.keys:
                    each.mouse_up()
                    if each.x < pos[0] < each.x + each.w and each.y < pos[1] < each.y + each.h:
                        each.handle(event)
                        return
            self.update()
            self.ls.update_me = True

class LoginScreen:
    def __init__(self, mainloop, screen, size):
        self.screen = screen
        self.mainloop = mainloop
        self.config = self.mainloop.config
        self.colors = Colors(mainloop)

        if self.mainloop.android is not None:
            self.w = self.mainloop.android_login_size[0]  # size[0] 800
        else:
            self.w = 800
        self.h = 570
        self.keyboard_h = 120
        self.scroll_min_top = 0
        self.side_panel_w = 80
        self.loading = False
        self.load_login_defs()
        self.lang = self.mainloop.lang
        self.lang.load_language(lang_code=self.default_lang)
        self.user_exists = True
        self.admin_authorised = False
        self.admin_exists = self.mainloop.db.admin_exists()
        self.def_screenw = self.w
        self.def_screenh = self.h
        self.left = (size[0] - self.def_screenw) // 2
        self.top = (size[1] - self.def_screenh) // 2
        self.loginto = None
        self.scroll_down = False
        self.usr_count = 1
        self.in_focus = None
        self.state = "LOGIN"
        self.side_highlight = None
        self.font_color = self.colors.ls_font_color
        self.header_font_color = self.colors.ls_header_font_color
        self.bg_col = self.colors.ls_bg_col
        self.bg_sidecol = self.colors.ls_bg_sidecol
        self.login_welcome_msg = ""
        self.db_status = self.login_welcome_msg
        self.prev_checked = None
        self.prev_user_checked = None
        self.age_groups = []

        self.points = int(round((50 * 72 / 96) / 4, 0))

        self.load_fonts()
        self.mainloop.redraw_needed[0] = True
        self.update_me = True

        self.edit_list = pygame.sprite.LayeredUpdates()
        self.btn_list = pygame.sprite.LayeredUpdates()
        self.all_list = pygame.sprite.LayeredUpdates()
        self.usercount = 1

        self.img = pygame.image.load(os.path.join('res', 'images', "login_screen_logo.png")).convert_alpha()
        self.img_rect = self.img.get_rect()

        #if self.mainloop.android is not None:
        try:
            self.bg_img = self.scale_img(
                pygame.image.load(os.path.join('res', 'images', "gradient_large.jpg")).convert(),
                self.screen.get_size()[0],
                self.screen.get_size()[1])
        except:
            try:
                self.bg_img = self.scale_img(
                    pygame.image.load(os.path.join('res', 'images', "gradient.jpg")).convert(),
                    self.screen.get_size()[0],
                    self.screen.get_size()[1])
            except:
                self.bg_img = None

            #self.bg_img_rect = self.img.get_rect()


        # add keyboard
        self.keyboard = Keyboard(self, self.left+5, self.top + self.h - self.keyboard_h - 5, self.w-10, self.keyboard_h)

        normal_login = True
        al = self.mainloop.db.get_autologin()
        if al is not None:
            if al[1] and not self.mainloop.logged_out:
                normal_login = False
                self.fauto_login(al[0])

        if normal_login:
            self.in_focus = None
            self.add_login_elements()
            self.add_side_btns()
            self.merge_sprite_lists()
            self.swich_hl(self.login_tab)

        self.layer1 = pygame.Surface(screen.get_size(), flags=pygame.SRCALPHA, depth=32)
        self.layer4 = pygame.Surface(screen.get_size(), flags=pygame.SRCALPHA, depth=32)
        self.draw_background()

    def scale_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    def draw_background(self):

        layer2 = pygame.Surface(self.screen.get_size(), flags=pygame.SRCALPHA, depth=32)
        layer3 = pygame.Surface(self.screen.get_size(), flags=pygame.SRCALPHA, depth=32)

        if self.bg_img is not None:
            self.layer1.blit(self.bg_img, (0, 0), self.layer1.get_rect())
        else:
            if self.mainloop.android is None:
                self.colors.fill_gradient(self.layer1, self.colors.inner_color, self.colors.inner_color_end, rect=None,
                                          vertical=True, forward=True)
                self.colors.fill_gradient(layer2, self.colors.inner_color2, self.colors.inner_color2_end, rect=None,
                                          vertical=False, forward=True)
                self.layer1.blit(layer2, (0, 0), self.layer1.get_rect())
            else:
                self.layer1.fill(self.colors.android_backup_color)


        lines = [[self.left + 0, self.top + 0], [self.left + self.w - 1, self.top + 0],
                 [self.left + self.w - 1, self.top + self.h - 1], [self.left + 0, self.top + self.h - 1]]
        pygame.draw.polygon(layer3, self.colors.inner_color, lines, 0)
        pygame.draw.polygon(layer3, self.colors.alpha_overlay, lines, 0)
        pygame.draw.lines(layer3, (255, 255, 255, 100), True, lines, 1)


        lines = [[self.left + 10, self.top + 10], [self.left + self.w - self.side_panel_w - 30, self.top + 10],
                 [self.left + self.w - self.side_panel_w - 30, self.top + self.h - 30 - self.keyboard_h],
                 [self.left + 10, self.top + self.h - 30 - self.keyboard_h]]
        pygame.draw.polygon(layer3, self.bg_col, lines, 0)
        pygame.draw.lines(layer3, (255, 255, 255, 100), True, lines, 1)


        lines = [[self.left + self.w - self.side_panel_w - 10, self.top + 10 + 55],
                 [self.left + self.w - 10, self.top + 10 + 55],
                 [self.left + self.w - 10, self.top + self.h - 30 - self.keyboard_h],
                 [self.left + self.w - self.side_panel_w - 10, self.top + self.h - 30 - self.keyboard_h]]
        pygame.draw.polygon(layer3, self.bg_sidecol, lines, 0)
        pygame.draw.lines(layer3, (255, 255, 255, 100), True, lines, 1)


        self.layer4.blit(self.layer1, (0, 0), self.layer1.get_rect())
        self.layer4.blit(layer3, (0, 0), self.layer1.get_rect())

    def load_fonts(self):
        # headers
        self.font_1 = pygame.font.Font(
            os.path.join('res', 'fonts', self.mainloop.config.font_dir, self.mainloop.config.font_name_1),
            (int(self.points * 2.0)))

        # buttons & edit fields
        self.font_2 = pygame.font.Font(
            os.path.join('res', 'fonts', self.mainloop.config.font_dir, self.mainloop.config.font_name_1),
            (int(self.points * 1.8)))

        #keyboard Keys
        self.font_3 = pygame.font.Font(
            os.path.join('res', 'fonts', self.mainloop.config.font_dir, self.mainloop.config.font_name_1),
            (int(self.points * 3.5)))

    def load_login_defs(self):
        self.login_defs = self.mainloop.db.get_login_defs()
        self.default_lang = self.login_defs[0]
        self.full_screen = bool(int(self.login_defs[1][0]))
        self.check_updates = bool(int(self.login_defs[1][2]))
        self.require_pass = bool(int(self.login_defs[1][3]))
        self.require_adminpass = bool(int(self.login_defs[1][4]))

    def merge_sprite_lists(self):
        self.all_list.empty()
        self.db_status_lbl = PLabel(self, self.w - 135, 30, self.left + 15, self.top + self.h - 55 - self.keyboard_h + 25, "")
        self.db_status_lbl.bg_color = (0, 0, 0, 0)
        self.db_status_lbl.font_color = (255, 255, 255)
        self.edit_list.add(self.db_status_lbl)
        for each in self.edit_list:
            self.all_list.add(each)
        for each in self.btn_list:
            self.all_list.add(each)

    def add_login_elements(self):
        self.load_usernames()
        self.username_count = len(self.usernames)
        #self.keyboard.enable()
        self.scroll_item_count = 5
        self.db_status = self.login_welcome_msg
        self.halfw = self.w // 2 - 50
        label_w = self.halfw - 35

        # header
        self.hlb1 = PLabel(self, label_w, 30, self.left + 20, self.top + 15, self.lang.b["Log in:"])
        self.hlb1.font_color = self.header_font_color
        self.hlb1.font_v = self.font_1
        self.edit_list.add(self.hlb1)

        self.lb4 = PLabel(self, label_w, 30, self.left + 20, self.top + 55, self.lang.b["user name:"])
        self.edit_list.add(self.lb4)

        self.username = PEdit(self, self.halfw - 40, 30, self.left + 20, self.top + 82, 1)
        if self.username_count > 5:
            self.edit_list.add(self.username)

        if self.require_pass:
            btn_top = 345  # 350

            self.lb5 = PLabel(self, label_w, 30, self.left + 20, self.top + 285 - 5, self.lang.b["password:"])
            self.edit_list.add(self.lb5)

            self.password = PEdit(self, self.halfw - 40, 30, self.left + 20, self.top + 310, 2, True)
            self.edit_list.add(self.password)
        else:
            btn_top = 273  # 278

        self.cb_remember = PCheckbox(self, label_w, 30, self.left + 20, self.top + btn_top, False,
                                     self.lang.b["remember me"])
        self.edit_list.add(self.cb_remember)
        self.loginbtn = PButton(self, self.halfw // 2 - 40 + 20, 35, self.left + 0 + self.halfw // 2,
                                self.top + btn_top + 30, 3, self.lang.b["Login"], self.flogin)
        self.loginbtn.set_call2action_style()
        self.edit_list.add(self.loginbtn)
        self.select = []
        if self.username_count > 5:
            hs = [120, 150, 180, 210, 240]
            h = 30
        else:
            #hs = [80, 150, 180, 210, 240]

            h = 190 // self.username_count
            hs = []
            for i in range(0, self.username_count):
                hs.append(80 + i * h)
        if self.username_count < 6:
            editw = self.halfw - 40
            l = self.username_count
        else:
            editw = self.halfw - 40 - 20
            l = 5
        for i in range(l):
            #self.select.append(PSelect(self, editw, h, self.left + 20, self.top + hs[i], 0))
            self.select.append(PButton2(self, editw, h, self.left + 20, self.top + hs[i], 0, "", self.change_user_selection))
            self.select[i].select_item = True
            self.select[i].disabled = False
            self.edit_list.add(self.select[i])

        if self.username_count > 5:
            self.scroll_max_h = self.scroll_item_count * 30 - 4  # 150
            self.scroll_min_h = 30
            self.scroll_min_top = self.top + 120 + 2
            self.scroll_bg = PEdit(self, 20, self.scroll_item_count * 30, self.left + self.halfw - 40 - 20 + 20,
                                   self.top + 120, -1)
            self.edit_list.add(self.scroll_bg)
            self.scroll_bg.select_item = True
            self.scroll_bar = PScrollBar(self, 16, 30, self.left + self.halfw - 40 - 20 + 20 + 2, self.top + 122, 0)
            self.edit_list.add(self.scroll_bar)

        self.reload_selects()

        self.hlb2 = PLabel(self, self.halfw - 35, 30, self.left + self.halfw + 20, self.top + 15, self.lang.b["Select age group:"])
        self.hlb2.font_color = self.header_font_color
        self.hlb2.font_v = self.font_1
        self.edit_list.add(self.hlb2)
        self.lb6 = PLabel(self, label_w, 30, self.left + self.halfw + 20, self.top + 55,
                          self.lang.b["show activities for:"])
        self.edit_list.add(self.lb6)
        self.age_groups_labels = [self.lang.b["preschool"], self.lang.b["Year 1"], self.lang.b["Year 2"],
                                  self.lang.b["Year 3"], self.lang.b["Year 4"], self.lang.b["Year 5"],
                                  self.lang.b["Year 6"], self.lang.b["all groups"]]
        self.age_groups = []
        group_ind = [0, 1, 2, 3, 4, 5, 6, 7]
        count = len(self.age_groups_labels)
        h = 41
        top = self.top + 82 - h
        for i in range(count):
            top = top + h
            tmp_btn = PButton2(self, self.halfw - 40, h, self.left + self.halfw + 20, top, 7, self.age_groups_labels[i],
                               self.change_age_group)
            tmp_btn.age_group = group_ind[i]
            self.edit_list.add(tmp_btn)
            self.age_groups.append(tmp_btn)

        #preselect first user
        if self.username_count < 6:
            self.select[0].onMouseButtonDown()
            self.select[0].onBlur()


    def change_age_group(self):
        if self.username.value in self.usernames:
            for each in self.age_groups:
                if each.focused and not each.disabled:
                    each.checked = True
                    if self.prev_checked:
                        self.prev_checked.checked = False
                    self.prev_checked = each
                    if self.username.value in self.usernames:
                        self.mainloop.db.update_age_group(self.username.value, each.age_group)

    def change_user_selection(self):
        for each in self.select:
            if each.focused and not each.disabled:
                each.checked = True
                if self.prev_user_checked:
                    self.prev_user_checked.checked = False
                self.prev_user_checked = each

    def add_admin_login_elements(self):
        #self.keyboard.enable()
        self.hlb1 = PLabel(self, self.w - 135, 30, self.left + 20, self.top + 15, self.lang.b["Administrator Login:"])
        self.hlb1.font_color = self.header_font_color
        self.hlb1.font_v = self.font_1
        self.edit_list.add(self.hlb1)

        self.lb1 = PLabel(self, 400, 30, self.left + 150, self.top + 55, self.lang.b["user name:"])
        self.edit_list.add(self.lb1)

        self.lb2 = PLabel(self, 400, 30, self.left + 150, self.top + 122 - 5, self.lang.b["password:"])
        self.edit_list.add(self.lb2)

        self.db_status = ""
        self.username = PEdit(self, 400, 30, self.left + 150, self.top + 82, 1)
        self.edit_list.add(self.username)
        self.password = PEdit(self, 400, 30, self.left + 150, self.top + 144, 2, True)
        self.edit_list.add(self.password)

        self.loginbtn = PButton(self, 200, 30, self.left + 250, self.top + 184, 3, self.lang.b["Login"],
                                self.fadminlogin)
        self.edit_list.add(self.loginbtn)
        self.in_focus = self.username
        self.username.onFocus()

    def add_lang_elements(self):
        self.keyboard.enable(False)
        self.db_status = ""
        self.scroll_item_count = len(self.config.all_lng)
        if self.mainloop.android is not None:
            self.scroll_item_count -= 1
        self.halfw = self.w // 2 - 50


        self.hlb1 = PLabel(self, self.w - 135, 30, self.left + 20, self.top + 15, self.lang.b["Default Language:"])
        self.hlb1.font_color = self.header_font_color
        self.hlb1.font_v = self.font_1
        self.edit_list.add(self.hlb1)

        # user list
        self.select = []

        # hs = [60,90,120,150,180,210,240,270,300,330,360,390]
        # hs = [60,90,120,150,180,210,240,280,320,350,380,410,430,450]
        #hs = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 60, 90, 120, 150, 180, 210, 240, 270]  # ,150]#,180]
        #hs = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 60, 90, 120, 150, 180, 210, 240, 270]  # ,150]#,180]
        if self.mainloop.android:
            rows = 4
        else:
            rows = 5
        frows = float(rows)
        cols = int(math.ceil(self.scroll_item_count / frows))

        self.lang_w = (self.w - 120) // cols

        #print(cols)

        h = (360 + 30 - 45) // rows
        w = self.lang_w - 15
        k = 0

        for i in range(self.scroll_item_count):
            if k > rows-1:
                k = 0
            """
            if i <= rows-1:
                j = 0
            elif i <= (rows-1) * 2+1:
                j = 1
            else:
                j = 2
            """
            j = int(math.floor(i / frows))
            self.select.append(
                PButton(self, w, h, self.left + self.lang_w*j+5+13, self.top + 60 + h * k, 0, self.config.lang_titles[i],
                        self.fset_lang))
            self.edit_list.add(self.select[i])
            self.select[i].bg_color = self.colors.btn_bg_color
            self.select[i].bg_focus = self.colors.btn_bg_focus
            self.select[i].border_color = self.colors.btn_border_color_l
            self.select[i].border_focused = self.colors.btn_border_focused_l
            self.select[i].font_color = self.colors.edit_font_color
            self.select[i].iso_code = self.config.all_lng[i]
            self.select[i].right_align = False
            self.select[i].select_item = True
            k += 1

        self.fselect_lang()

    def add_users_elements(self):
        #self.keyboard.enable()
        self.db_status = ""
        self.scroll_item_count = 7
        self.halfw = self.w // 2 - 50
        self.thirdw = (self.w - 96) // 3

        cw = self.thirdw - 20

        self.hlb1 = PLabel(self, self.w - 135, 30, self.left + 20, self.top + 15, self.lang.b["User Management"])
        self.hlb1.font_color = self.header_font_color
        self.hlb1.font_v = self.font_1
        self.edit_list.add(self.hlb1)

        # user list
        self.select = []

        hs = [60, 90, 120, 150, 180, 210, 240, 270, 300]  # ,330,360]
        for i in range(self.scroll_item_count):
            self.select.append(PSelect(self, cw, 30, self.left + 20, self.top + hs[i], 0))
            self.select[i].select_item = True
            self.edit_list.add(self.select[i])

            self.select[i].users = True
            self.select[i].bg_color = self.colors.btn_bg_color
            self.select[i].bg_focus = self.colors.btn_bg_focus
            self.select[i].border_color = self.colors.btn_border_color_l
            self.select[i].border_focused = self.colors.btn_border_focused_l
            self.select[i].font_color = self.colors.edit_font_color

        self.scroll_max_h = self.scroll_item_count * 30 - 4  # 150
        self.scroll_min_h = 30
        self.scroll_min_top = self.top + 60 + 2

        self.scroll_bg = PEdit(self, 20, self.scroll_item_count * 30, self.left + cw + 20, self.top + 60, -1)
        self.edit_list.add(self.scroll_bg)
        self.scroll_bg.select_item = True

        self.scroll_bar = PScrollBar(self, 16, 30, self.left + cw + 20 + 2, self.top + 62, 0)
        self.edit_list.add(self.scroll_bar)

        self.reload_selects()

        # add new user
        self.lb1 = PLabel(self, self.w - 135, 30, self.left + 20, self.top + 285, self.lang.b["Add new user:"])
        self.lb1.font_color = self.colors.ls_font_color # (255, 179, 111)
        self.lb2 = PLabel(self, cw, 30, self.left + 20, self.top + 315, self.lang.b["user name:"])
        self.rusername = PEdit(self, cw, 30, self.left + 20, self.top + 340, 1)
        self.lb3 = PLabel(self, cw, 30, self.left + 20 + cw + 10, self.top + 315, self.lang.b["password:"])
        self.rpassword = PEdit(self, cw, 30, self.left + 20 + cw + 10, self.top + 340, 2, True)
        self.lb4 = PLabel(self, cw, 30, self.left + 20 + cw + 10 + cw + 10, self.top + 315,
                          self.lang.b["confirm password:"])
        self.rconfirmpassword = PEdit(self, cw, 30, self.left + 20 + cw + 10 + cw + 10, self.top + 340, 3, True)
        self.rregisterbtn = PButton(self, cw*2 + 10, 30, self.left + 20 + cw + 10, self.top + 380, 4,
                                    self.lang.b["Register"], self.fregister)

        # user info elements w h l t
        self.dlb1 = PLabel(self, cw * 2 - 10, 30, self.left + cw + 50, self.top + 60, self.lang.b["Please select"])  # name field
        self.dlb1.font_color = self.colors.ls_font_color # (100, 200, 255)
        if self.lang.ltr_text:
            l = [self.left + cw + 70, self.left + 2 * cw + 40]
        else:
            l = [self.left + 2 * cw + 20, self.left + cw + 50]
        self.ilb1 = PLabel(self, cw, 30, l[0], self.top + 90, "")  # registered label
        self.ilb2 = PLabel(self, cw, 30, l[0], self.top + 120, "")  # last login label
        self.dlb2 = PLabel(self, cw, 30, l[1], self.top + 90, "")  # registered field
        self.dlb3 = PLabel(self, cw, 30, l[1], self.top + 120, "")  # last login field
        if self.lang.ltr_text:
            self.dlb2.right_align = True
            self.dlb3.right_align = True
        # delete user buttons
        # calculate distance from right
        text = self.lang.b["delete user"]
        w = self.get_text_w(text) + 6

        # add text button
        self.delete_btn = PButton(self, w, 30, self.left + self.w - 150 - w, self.top + 220, 0, text, self.showfdeluser,
                                  right_align=True, transparent=True)
        self.delete_btn.visible = False
        self.delete_btn.update()
        self.delete_imgbtn = PIMGButton(self, 30, 30, self.left + self.w - 150, self.top + 220, 0, "login_delete_usr.png",
                                        "login_delete_usr.png", self.showfdeluser)

        self.delete_imgbtn.visible = False

        # confirm delete
        text = self.lang.b["Cancel"]
        w1 = self.get_text_w(text) + 6
        self.delete_no = PButton(self, w1, 30, self.left + self.w - 120 - w1, self.top + 250, 0, text, self.hidefdeluser,
                                 right_align=True, transparent=True)
        self.delete_no.visible = False
        self.delete_no.font_color = (40, 255, 40)
        text = self.lang.b["Delete"]
        w2 = self.get_text_w(text) + 6
        self.delete_yes = PButton(self, w2, 30, self.left + self.w - 120 - w1 - w2 - 15, self.top + 250, 0, text, self.fdeluser,
                                  right_align=True, transparent=True)
        self.delete_yes.visible = False
        self.delete_yes.font_color = (255, 40, 40)
        # add all form elements to a sprites group
        form_elements = [self.lb1, self.lb2, self.lb3, self.lb4, self.rusername, self.rpassword, self.rconfirmpassword,
                         self.rregisterbtn, self.ilb1, self.ilb2, self.dlb1, self.dlb2, self.dlb3, self.delete_yes,
                         self.delete_no, self.delete_btn, self.delete_imgbtn]

        for each in form_elements:
            self.edit_list.add(each)

    def add_fonts_elements(self):
        #self.keyboard.enable()
        self.scroll_item_count = 10
        self.db_status = self.login_welcome_msg
        self.halfw = self.w // 2 - 50
        label_w = 310
        # header
        self.hlb1 = PLabel(self, label_w, 30, self.left + 20, self.top + 15, self.lang.b["Log in:"])
        self.hlb1.font_color = self.header_font_color
        self.hlb1.font_v = self.font_1
        self.edit_list.add(self.hlb1)

        btn_top = 333

        self.loginbtn = PButton(self, self.halfw // 2 - 40, 30, self.left + 20 + self.halfw // 2,
                                self.top + btn_top + 30, 3, self.lang.b["Apply"], self.fapplyfont)
        self.edit_list.add(self.loginbtn)
        self.select = []

        hs = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
        for i in range(10):
            self.select.append(PSelect(self, self.halfw - 40 - 20, 30, self.left + 20, self.top + hs[i], 0))
            self.select[i].select_item = True
            self.edit_list.add(self.select[i])

        self.scroll_max_h = self.scroll_item_count * 30 - 4
        self.scroll_min_h = 30
        self.scroll_min_top = self.top + 60 + 2
        self.scroll_bg = PEdit(self, 20, self.scroll_item_count * 30, self.left + self.halfw - 40 - 20 + 20,
                               self.top + 60, -1)
        self.edit_list.add(self.scroll_bg)
        self.scroll_bg.select_item = True

        self.scroll_bar = PScrollBar(self, 16, 30, self.left + self.halfw - 40 - 20 + 20 + 2, self.top + 62, 0)
        self.edit_list.add(self.scroll_bar)
        text = self.lang.b["Hello"]
        self.sample_text = PLabel(self, 250, 100, self.left + self.halfw + 20, self.top + 30, text)
        self.sample_text.font_color = self.header_font_color
        self.sample_text.font_v = self.font_1
        self.edit_list.add(self.sample_text)

        text = "0123456789"
        self.sample_text2 = PLabel(self, 250, 100, self.left + self.halfw + 20, self.top + 100, text)
        self.sample_text2.font_color = self.header_font_color
        self.sample_text2.font_v = self.font_1
        self.edit_list.add(self.sample_text2)

        self.reload_font_selects()

    def update_sample_font(self, font_name):
        try:
            self.sample_text.font_v = pygame.font.Font(pygame.font.match_font(font_name.lower()),
                                                       (int(self.points * 4.0)))
            self.sample_text2.font_v = self.sample_text.font_v
        except:
            pass

    def showfdeluser(self):
        self.delete_no.visible = True
        self.delete_yes.visible = True
        self.update_me = True
        self.mainloop.redraw_needed[0] = True
        self.delete_yes.update_me = True
        self.delete_no.update_me = True

    def hidefdeluser(self):
        self.delete_no.visible = False
        self.delete_yes.visible = False
        self.update_me = True
        self.mainloop.redraw_needed[0] = True
        self.delete_yes.update_me = True
        self.delete_no.update_me = True

    def fdeluser(self):
        m = self.mainloop.db.del_user(self.dlb1.value)
        if m == 0:
            self.db_status = ex.unival(self.lang.b["user deleted"]) % ex.unival(self.dlb1.value)
        else:
            self.db_status = self.lang.b["Failed to delete"]
        self.reload_selects()
        self.update_scrollbar_top(0)
        self.fdetails(None)

    def fset_lang(self):
        prev_guest = ex.unival(self.lang.b["Guest"])
        self.mainloop.db.set_lang(self.in_focus.iso_code)
        self.default_lang = self.in_focus.iso_code
        self.lang.load_language(lang_code=self.default_lang)
        self.flang()
        new_guest = ex.unival(self.lang.b["Guest"])
        self.mainloop.db.change_username(prev_guest, new_guest)
        self.login_welcome_msg = ""
        self.keyboard.add_keys()

    def fselect_lang(self):
        iso_code = self.mainloop.db.get_lang()
        for each in self.select:
            if each.iso_code == iso_code:
                if self.in_focus is not None:
                    self.in_focus.onBlur()
                    self.load_fonts()
                self.in_focus = each
                self.in_focus.update_me = True
                self.in_focus.onFocus()

    def recheck(self):
        if self.mainloop.android is None:
            self.cb0.checked = self.full_screen
            self.cb2.checked = self.check_updates
        self.cb3.checked = self.require_pass
        self.cb4.checked = self.require_adminpass

    def add_prefs_elements(self):
        #self.keyboard.enable()
        self.hlb1 = PLabel(self, self.w - 135, 30, self.left + 20, self.top + 15, self.lang.b["Preferences"])
        self.hlb1.font_color = self.header_font_color
        self.hlb1.font_v = self.font_1
        self.edit_list.add(self.hlb1)
        self.halfw = (self.w - 150) // 2
        self.db_status = ""
        #positions - 60, 90, 120, 150
        self.cb0 = PCheckbox(self, self.w - 135, 30, self.left + 20, self.top + 120, False,
                             self.lang.b["switch to full screen after login"])
        if self.mainloop.android is not None:
            self.cb0.visible = False
        self.edit_list.add(self.cb0)
        self.cb2 = PCheckbox(self, self.w - 135, 30, self.left + 20, self.top + 150, False,
                             self.lang.b["check for updates"])
        if self.mainloop.android is not None:
            self.cb2.visible = False
        self.edit_list.add(self.cb2)
        self.cb3 = PCheckbox(self, self.w - 135, 30, self.left + 20, self.top + 60, False,
                             self.lang.b["require password to log in"])
        self.edit_list.add(self.cb3)
        self.cb4 = PCheckbox(self, self.w - 135, 30, self.left + 20, self.top + 90, False,
                             self.lang.b["require password to access admin area"])
        self.edit_list.add(self.cb4)
        if self.admin_exists:
            self.lb1 = PLabel(self, self.w - 140, 30, self.left + 20, self.top + 220, self.lang.b["Update admin's password:"])

            self.lb2 = PLabel(self, self.w - 140, 30, self.left + 20, self.top + 255, self.lang.b["previous password:"])
            self.username = PEdit(self, self.w - 140, 30, self.left + 20, self.top + 280, 1, True)

            self.lb3 = PLabel(self, self.halfw, 30, self.left + 20, self.top + 315, self.lang.b["new password:"])
            self.password = PEdit(self, self.halfw, 30, self.left + 20, self.top + 340, 2, True)

            self.lb4 = PLabel(self, self.halfw, 30, self.left + self.halfw + 30, self.top + 315, self.lang.b["confirm new password:"])
            self.cpassword = PEdit(self, self.halfw, 30, self.left + self.halfw + 30, self.top + 340, 3, True)
        else:
            self.lb1 = PLabel(self, self.w - 140, 30, self.left + 20, self.top + 220, self.lang.b["Create admin's account:"])

            self.lb2 = PLabel(self, self.w - 140, 30, self.left + 20, self.top + 255, self.lang.b["admin's user name:"])
            self.username = PEdit(self, self.w - 140, 30, self.left + 20, self.top + 280, 1)

            self.lb3 = PLabel(self, self.halfw, 30, self.left + 20, self.top + 315, self.lang.b["admin's password:"])
            self.password = PEdit(self, self.halfw, 30, self.left + 20, self.top + 340, 2, True)

            self.lb4 = PLabel(self, self.halfw, 30, self.left + self.halfw + 30, self.top + 315, self.lang.b["confirm admin's password:"])
            self.cpassword = PEdit(self, self.halfw, 30, self.left + self.halfw + 30, self.top + 340, 3, True)

        self.savebtn = PButton(self, 200, 30, self.left + self.halfw - 75, self.top + 380, 4, self.lang.b["Save"], self.fprefsave)

        self.edit_list.add(self.lb1)
        self.edit_list.add(self.lb2)
        self.edit_list.add(self.lb3)
        self.edit_list.add(self.lb4)

        self.edit_list.add(self.username)
        self.edit_list.add(self.password)
        self.edit_list.add(self.cpassword)
        self.edit_list.add(self.savebtn)

    def add_side_btns(self):
        sp = 20
        self.close_tab = PIMGButton(self, 70, 35, self.left + self.w - 84,
                                    self.top + 17, 1, "login_close_n.png",
                                    "login_close.png", self.fclose)
        self.btn_list.add(self.close_tab)
        self.login_tab = PIMGButton(self, 70, 70, self.left + self.w - 85, self.top + sp + 35 + sp, 1, "login_login_n.png",
                                    "login_login.png", self.flogint)
        self.btn_list.add(self.login_tab)
        self.settings_tab = PIMGButton(self, 70, 70, self.left + self.w - 85, self.top + sp + 35 + sp + 70 + sp + sp + 70, 1,
                                       "login_settings_n.png", "login_settings.png", self.fprefs)
        self.btn_list.add(self.settings_tab)
        self.lang_tab = PIMGButton(self, 70, 70, self.left + self.w - 85, self.top + sp + 35 + sp + 70 + sp, 1,
                                   "login_lang_n.png", "login_lang.png", self.flang)
        self.btn_list.add(self.lang_tab)
        self.users_tab = PIMGButton(self, 70, 70, self.left + self.w - 85, self.top + sp + 35 + sp + 70 + sp + 70 + sp + 70 + sp,
                                    1, "login_users_n.png", "login_users.png", self.fusers)
        self.btn_list.add(self.users_tab)

    def reload_selects(self, j=0):
        if self.username_count > 5 or self.state == "USERS":
            self.load_usernames()
            self.usernames_filtered = self.filter_usernames()
            self.usr_count = len(self.usernames_filtered)
            self.reload_scroll_bar_h()
            index = 0
            for i in range(j, j + self.scroll_item_count):
                if i < self.usr_count:
                    self.select[index].value = self.usernames_filtered[i]
                    index += 1
                else:
                    self.select[index].value = ""
                    index += 1
        else:
            for i in range(0, self.username_count):
                self.select[i].value = self.usernames[i]
        if self.username_count < 6:
            self.age_groups_trigger()
            self.users_trigger()

    def reload_font_selects(self, j=0):
        system_font_list = pygame.font.get_fonts()
        sorted_font_list = sorted(system_font_list)
        self.usr_count = len(sorted_font_list)
        self.reload_scroll_bar_h()
        index = 0
        for i in range(j, j + self.scroll_item_count):
            if i < self.usr_count:
                self.select[index].value = sorted_font_list[i].title()
                index += 1
            else:
                self.select[index].value = ""
                index += 1

    def age_groups_trigger(self):
        if self.username.value in self.usernames:
            if self.prev_checked:
                self.prev_checked.checked = False
            for each in self.age_groups:
                each.disabled = False
            age_group = self.mainloop.db.get_age_group(self.username.value)
            if age_group is not None:
                self.prev_checked = self.age_groups[age_group]
                self.age_groups[age_group].checked = True
        else:
            for each in self.age_groups:
                each.disabled = True

    def users_trigger(self):
        if self.prev_user_checked:
            self.prev_user_checked.checked = False
        for each in self.select:
            each.disabled = False

        if self.in_focus is not None and self.in_focus.select_item:
            pass
            #self.prev_user_checked = self.in_focus
            #self.prev_user_checked.checked = True
        #age_group = self.mainloop.db.get_age_group(self.username.value)
        #if age_group is not None:
        #    self.prev_checked = self.age_groups[age_group]
        #    self.age_groups[age_group].checked = True


    def filter_usernames(self):
        if self.state == "LOGIN":
            fltr = self.username.value

            self.age_groups_trigger()
        else:
            fltr = ""
        ln = len(fltr)
        usr_fltred = []
        if ln == 0:
            return self.usernames
        else:
            for each in self.usernames:
                if each[0:ln] == fltr:
                    usr_fltred.append(each)
            return usr_fltred

    def reload_scroll_bar_h(self):
        if len(self.usernames) > 5:
            if self.usr_count < self.scroll_item_count + 1:
                self.scroll_h = self.scroll_max_h
            else:
                h = int((self.scroll_item_count * 30) / (self.usr_count / float(self.scroll_item_count)))
                if h > self.scroll_min_h:
                    self.scroll_h = h
                else:
                    self.scroll_h = self.scroll_min_h

            self.scroll_max_top = self.scroll_min_top + (self.scroll_item_count * 30) - self.scroll_h - 4
            self.max_offset = self.scroll_max_top - self.scroll_min_top
            self.scroll_bar.h = self.scroll_h
            self.scroll_bar.rect.h = self.scroll_h
            self.scroll_bar.rect_init()
            self.scroll_bar.update()

    def update_scrollbar_top(self, top):
        if len(self.usernames) > 5:
            if self.usr_count > self.scroll_item_count:
                if top > self.scroll_max_top + self.scroll_bar.dist2top:
                    t = self.scroll_max_top
                elif top < self.scroll_min_top + self.scroll_bar.dist2top:
                    t = self.scroll_min_top
                else:
                    t = top - self.scroll_bar.dist2top
                self.set_scrollbar_top(t)

                bar_offset = t - self.scroll_min_top
                usr_offset = int((bar_offset * (self.usr_count - self.scroll_item_count)) / float(self.max_offset))
                self.reload_selects(usr_offset)
            else:
                self.set_scrollbar_top(self.scroll_min_top)

    def update_fonts_scrollbar_top(self, top):
        if self.usr_count > self.scroll_item_count:
            if top > self.scroll_max_top + self.scroll_bar.dist2top:
                t = self.scroll_max_top
            elif top < self.scroll_min_top + self.scroll_bar.dist2top:
                t = self.scroll_min_top
            else:
                t = top - self.scroll_bar.dist2top
            self.set_scrollbar_top(t)

            bar_offset = t - self.scroll_min_top
            usr_offset = int((bar_offset * (self.usr_count - self.scroll_item_count)) / float(self.max_offset))
            self.reload_font_selects(usr_offset)
        else:
            self.set_scrollbar_top(self.scroll_min_top)

    def set_scrollbar_top(self, t):
        if len(self.usernames) > 5:
            if (self.state == "USERS" or self.state == "FONTS") and self.scroll_bar.top != t:
                if self.in_focus is not None:
                    if self.scroll_down == False:
                        self.in_focus.onBlur()
                    if self.state == "USERS":
                        self.fdetails(None)

            self.scroll_bar.top = t
            self.scroll_bar.rect.top = t
            self.scroll_bar.rect_init()
            self.scroll_bar.update()
            self.update_me = True
            self.mainloop.redraw_needed[0] = True

    def update(self):
        if self.update_me:
            self.update_me = False
            self.screen.fill(self.colors.outer_color)


            if not self.loading:
                self.screen.blit(self.layer4, (0, 0), self.screen.get_rect())

                if self.db_status != "":
                    self.db_status_lbl.value = self.db_status
                    self.db_status_lbl.update_me = True

                #self.screen.blit(self.layer3, (0, 0), self.screen.get_rect())

                for each_edit in self.edit_list:
                    each_edit.update()

                for each_btn in self.btn_list:
                    each_btn.update()
                self.edit_list.draw(self.screen)
                self.btn_list.draw(self.screen)
                if self.keyboard.enabled:
                    self.keyboard.update()
                else:
                    self.screen.blit(self.img, (self.left + (self.w-self.img_rect.w)//2, self.top + self.h - self.img_rect.h - 30), (0, 0, self.img_rect.w, self.img_rect.h))#(self.left + (self.w-self.img_rect.w)//2, self.top + self.h - self.img_rect.h - 30, self.img_rect.w, self.img_rect.h))
            else:
                self.screen.blit(self.layer1, (0, 0), self.screen.get_rect())

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            if pos[1] < self.keyboard.y:
                if self.scroll_down == False:
                    for each in self.btn_list:
                        if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and each.rect.topleft[1] + each.rect.height >= pos[1] >= each.rect.topleft[1]:
                            each.handle(event)
                else:
                    if self.state == "LOGIN" or self.state == "USERS":
                        self.update_scrollbar_top(pos[1])
                    elif self.state == "FONTS":
                        self.update_fonts_scrollbar_top(pos[1])

            self.keyboard.handle(event)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #self.draw_background()
            pos = event.pos
            if pos[1] < self.keyboard.y:
                focus_changed = False
                self.prev_focus = self.in_focus
                for each in self.all_list:
                    if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and each.rect.topleft[
                        1] + each.rect.height >= pos[1] >= each.rect.topleft[1]:
                        if self.in_focus is not None:
                            self.in_focus.onBlur()
                            focus_changed = True

                        self.in_focus = each
                        each.handle(event)

                # if focus_changed is False and self.prev_focus is not None and self.state != "LANG":
                if focus_changed is False and self.prev_focus is not None:
                    if not self.prev_focus.select_item:
                        self.prev_focus.onBlur()
                        self.prev_focus = None
                        self.in_focus = None
                self.mainloop.redraw_needed[0] = True
            else:
                self.keyboard.handle(event)

            if self.in_focus is not None and isinstance(self.in_focus, PEdit) and self.in_focus.is_editable():
                self.keyboard.enable(True)
            else:
                self.keyboard.enable(False)



        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.scroll_bar.dist2top = 0
            if self.state == "LOGIN" or self.state == "USERS":
                self.update_scrollbar_top(self.scroll_bar.top - 5)
            elif self.state == "FONTS":
                self.update_fonts_scrollbar_top(self.scroll_bar.top - 5)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.scroll_bar.dist2top = 0
            if self.state == "LOGIN" or self.state == "USERS":
                self.update_scrollbar_top(self.scroll_bar.top + 5)
            elif self.state == "FONTS":
                self.update_fonts_scrollbar_top(self.scroll_bar.top + 5)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = event.pos
            if self.scroll_down:
                self.scroll_down = False
                if self.state == "LOGIN" or self.state == "USERS":
                    self.update_scrollbar_top(pos[1])
                elif self.state == "FONTS":
                    self.update_fonts_scrollbar_top(pos[1])
            for each in self.all_list:
                if each.rect.topleft[0] + each.rect.width >= pos[0] >= each.rect.topleft[0] and each.rect.topleft[
                    1] + each.rect.height >= pos[1] >= each.rect.topleft[1]:
                    if self.in_focus == each:
                        each.handle(event)

            self.keyboard.handle(event)

        elif event.type == pygame.KEYDOWN:
            if self.in_focus is not None:
                self.in_focus.handle(event)

    def nextFocus(self, current_focus):
        for each in self.edit_list:
            if each.focus_order == current_focus + 1:
                self.in_focus.onBlur()
                self.in_focus = each
                self.in_focus.onFocus()

    def fapplyfont(self):
        pass

    def flogin(self):
        if self.require_pass:
            if ex.unival(self.username.value) == ex.unival(self.lang.b["Guest"]):
                m = self.mainloop.db.login_user_no_pass(self.username.value)
                if m == -1:
                    self.db_status = self.lang.b["This username doesn't exist."]
                self.complete_login()
            elif len(self.username.value) < 3:
                self.db_status = self.lang.b["Please enter user name (at least 3 characters long)"]
                self.in_focus.onBlur()
                self.in_focus = self.username
                self.username.onFocus()
            elif len(self.password.value) < 4:
                self.db_status = self.lang.b["Please enter password (at least 4 characters long)"]
                self.in_focus.onBlur()
                self.in_focus = self.password
                self.password.onFocus()
            else:
                m = self.mainloop.db.login_user(self.username.value, self.password.value)
                if m == -1:
                    self.db_status = self.lang.b["This username and password combination doesn't exist."]
                self.complete_login()
        else:
            if len(self.username.value) < 3:
                self.db_status = self.lang.b["Please enter user name (at least 3 characters long)"]
                self.in_focus.onBlur()
                self.in_focus = self.username
                self.username.onFocus()
            else:
                m = self.mainloop.db.login_user_no_pass(self.username.value)
                if m == -1:
                    self.db_status = self.lang.b["This username doesn't exist."]
                self.complete_login()

    def fauto_login(self, userid):
        m = self.mainloop.db.login_auto(userid)
        self.mainloop.user_name = self.mainloop.db.username
        self.mainloop.userid = self.mainloop.db.userid

        self.mainloop.done = True
        self.mainloop.window_state = self.mainloop.window_states[1]

    def complete_login(self):
        if self.mainloop.db.userid > -1:
            self.loading = True
            self.update_me = True
            self.edit_list.empty()
            self.btn_list.empty()
            self.all_list = []
            self.screen.fill((70, 70, 70))

            if self.cb_remember.checked:
                self.mainloop.db.set_autologin(self.mainloop.db.userid)
            else:
                self.mainloop.db.unset_autologin()

            self.mainloop.user_name = self.mainloop.db.username
            self.mainloop.userid = self.mainloop.db.userid

            self.mainloop.done = True
            self.mainloop.window_state = self.mainloop.window_states[1]

    def fregister(self):
        if len(self.rusername.value) < 3:
            self.db_status = self.lang.b["Please enter user name (at least 3 characters long)"]
            self.in_focus.onBlur()
            self.in_focus = self.rusername
            self.rusername.onFocus()
        elif len(self.rpassword.value) < 4:
            self.db_status = self.lang.b["Please enter password (at least 4 characters long)"]
            self.in_focus.onBlur()
            self.in_focus = self.rpassword
            self.rpassword.onFocus()
        elif self.rpassword.value != self.rconfirmpassword.value:
            self.db_status = self.lang.b["Passwords don't match"]
            self.in_focus.onBlur()
            self.in_focus = self.rpassword
            self.rpassword.onFocus()
            self.rpassword.value = ""
            self.rconfirmpassword.value = ""
        else:
            m = self.mainloop.db.add_user(self.rusername.value, self.rpassword.value, self.default_lang, 0, 0,
                                          self.def_screenw, self.def_screenh)
            if m == 0:
                self.db_status = ex.unival(self.lang.b["%s added"]) % ex.unival(self.rusername.value)
            else:
                self.db_status = self.lang.b["This user name already exists, please choose a different one"]
            self.reload_selects()
            self.in_focus.onBlur()
            self.rusername.value = ""
            self.rpassword.value = ""
            self.rconfirmpassword.value = ""
            self.reload_scroll_bar_h()
            self.update_scrollbar_top(0)
            self.update_me = True
            self.mainloop.redraw_needed[0] = True

    def load_usernames(self):
        self.usernames = self.mainloop.db.load_usernames()

    def fdetails(self, username):
        self.hidefdeluser()
        if username is not None:
            details = self.mainloop.db.load_user_details(username)
        else:
            details = None

        if details is not None:
            self.ilb1.value = self.lang.b["registered:"]
            self.dlb1.value = details[0]
            self.dlb2.value = details[1]
            self.ilb2.value = self.lang.b["last login:"]
            if details[2] != "":
                self.dlb3.value = details[2]
            else:
                self.dlb3.value = ""
            self.delete_btn.visible = True
            self.delete_imgbtn.visible = True
            self.update_me = True
            self.mainloop.redraw_needed[0] = True
        else:
            self.ilb1.value = ""
            self.ilb2.value = ""
            self.dlb1.value = ""
            self.dlb2.value = ""
            self.dlb3.value = ""
            self.delete_btn.visible = False
            self.delete_imgbtn.visible = False
            self.update_me = True
            self.mainloop.redraw_needed[0] = True
        self.delete_btn.update_me = True
        self.delete_imgbtn.update_me = True

    def flogint(self):
        self.state = "LOGIN"
        self.edit_list.empty()

        self.add_login_elements()
        self.merge_sprite_lists()

        self.update_me = True
        self.mainloop.redraw_needed[0] = True
        self.swich_hl(self.login_tab)

    def swich_hl(self, tab):
        if self.side_highlight is not None:
            self.side_highlight.highlight = False
            if self.side_highlight.hover:
                self.side_highlight.update_trigger()
            self.side_highlight.hover = False
            self.side_highlight.update_me = True
        self.side_highlight = tab

        if not self.side_highlight.hover:
            self.side_highlight.update_trigger()
        self.side_highlight.hover = True
        self.side_highlight.highlight = True
        self.side_highlight.update_me = True

    def fprefs(self):
        self.edit_list.empty()
        if (self.admin_authorised or not self.require_adminpass) or not self.admin_exists:
            self.state = "PREFERENCES"
            self.add_prefs_elements()
            self.recheck()
        else:
            self.state = "ADMINLOGIN"
            self.loginto = "PREFERENCES"
            self.add_admin_login_elements()
        self.merge_sprite_lists()
        self.swich_hl(self.settings_tab)
        self.update_me = True
        self.mainloop.redraw_needed[0] = True

    def fusers(self):
        self.edit_list.empty()
        if (self.admin_authorised or not self.require_adminpass) or not self.admin_exists:
            self.state = "USERS"
            self.add_users_elements()
            self.merge_sprite_lists()
        else:
            self.state = "ADMINLOGIN"
            self.loginto = "USERS"
            self.add_admin_login_elements()
            self.merge_sprite_lists()
        self.swich_hl(self.users_tab)
        self.update_me = True
        self.mainloop.redraw_needed[0] = True

    def flang(self):
        self.edit_list.empty()
        #if (self.admin_authorised or not self.require_adminpass) or not self.admin_exists:
        self.state = "LANG"
        self.add_lang_elements()
        self.merge_sprite_lists()
        #else:
        #    self.state = "ADMINLOGIN"
        #    self.loginto = "LANG"
        #    self.add_admin_login_elements()
        #    self.merge_sprite_lists()
        self.swich_hl(self.lang_tab)

        self.update_me = True
        self.mainloop.redraw_needed[0] = True

    def ffonts(self):
        self.edit_list.empty()
        if (self.admin_authorised or not self.require_adminpass) or not self.admin_exists:
            self.state = "FONTS"
            self.add_fonts_elements()
            self.merge_sprite_lists()
        else:
            self.state = "ADMINLOGIN"
            self.loginto = "FONTS"
            self.add_admin_login_elements()
            self.merge_sprite_lists()
        self.swich_hl(self.settings_tab)
        self.update_me = True
        self.mainloop.redraw_needed[0] = True

    def fadminlogin(self):
        if len(self.username.value) < 3:
            self.db_status = self.lang.b["Please enter user name (at least 3 characters long)"]
            self.in_focus.onBlur()
            self.in_focus = self.username
            self.username.onFocus()
        elif len(self.password.value) < 4:
            self.db_status = self.lang.b["Please enter password (at least 4 characters long)"]
            self.in_focus.onBlur()
            self.in_focus = self.password
            self.password.onFocus()
        else:
            m = self.mainloop.db.login_admin(self.username.value, self.password.value)
            if m == 0:
                self.db_status = ""
            elif m == -1:
                self.db_status = self.lang.b["This username and password combination doesn't exist."]
            else:
                self.db_status = "ERROR FAL-2"
            if self.mainloop.db.userid == -2:
                self.admin_authorised = True
                if self.loginto == "USERS":
                    self.fusers()
                elif self.loginto == "PREFERENCES":
                    self.fprefs()
                elif self.loginto == "LANG":
                    self.flang()
                elif self.loginto == "FONTS":
                    self.ffonts()

    def fprefsave(self):
        self.update_me = True
        # update username or password
        if self.username.value != "":
            if self.password.value != self.cpassword.value:
                self.db_status = self.lang.b["Passwords don't match"]
                self.password.value = ""
                self.cpassword.value = ""
                self.in_focus.onBlur()
                self.in_focus = self.password
                self.password.onFocus()
            else:
                if self.admin_exists == False:
                    if len(self.username.value) < 3:
                        self.db_status = self.lang.b["Please enter user name (at least 3 characters long)"]
                        self.in_focus.onBlur()
                        self.in_focus = self.username
                        self.username.onFocus()
                    elif len(self.password.value) < 4:
                        self.db_status = self.lang.b["Please enter password (at least 4 characters long)"]
                        self.in_focus.onBlur()
                        self.in_focus = self.password
                        self.password.onFocus()
                    else:
                        m = self.mainloop.db.add_admin_name(self.username.value, self.password.value)
                        if m == 0:
                            self.db_status = self.lang.b["Admin's password has been updated"]
                            self.admin_exists = True
                            self.admin_authorised = True
                            self.fprefs()
                        elif m == -1:
                            self.db_status = self.lang.b["ERROR: This operation is not allowed at this point"]
                else:
                    if len(self.username.value) < 4:
                        self.db_status = self.lang.b["Please enter previous password (at least 4 characters long)"]
                        self.in_focus.onBlur()
                        self.in_focus = self.username
                        self.username.onFocus()
                    elif len(self.password.value) < 4:
                        self.db_status = self.lang.b["Please enter new password (at least 4 characters long)"]
                        self.in_focus.onBlur()
                        self.in_focus = self.password
                        self.password.onFocus()
                    else:
                        m = self.mainloop.db.update_admin_password(self.username.value, self.password.value)
                        if m == 0:
                            self.db_status = self.lang.b["Admin's password has been updated"]
                        else:
                            self.db_status = self.lang.b["Previous password doesn't seem to be in the database"]
                        self.in_focus.onBlur()
                        self.username.value = ""
                        self.password.value = ""
                        self.cpassword.value = ""
        # update prefs
        defs = ""
        for i in range(5):
            if i == 1:
                defs += "1"
            else:
                defs += str(int(eval("self.cb" + str(i) + ".checked")))

        self.mainloop.db.update_defaults(defs)
        self.load_login_defs()
        self.savebtn.onBlur()
        if self.db_status == "":
            self.db_status = self.lang.b["Prefs saved..."]

    def fclose(self):
        self.mainloop.done = True
        self.mainloop.done4good = True

    def get_text_w(self, text):
        if sys.version_info < (3, 0):
            try:
                val = unicode(text, "utf-8")
            except UnicodeDecodeError:
                val = text
            except TypeError:
                val = text
        else:
            val = text

        return self.font_2.size(val)[0]
