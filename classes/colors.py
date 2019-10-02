# -*- coding: utf-8 -*-

import random
import classes.extras as ex
import copy




class Color:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.grid_line = (240, 240, 240)
        self.menu_l = (255, 75, 0)
        self.menu_r = (33, 121, 149)
        self.info = (70, 70, 70)

        # saturation and vibrance presets - used to create colors to tint unit background images
        self.font_color_s = 255
        self.font_color_v = 150
        self.bg_color_s = 128
        self.bg_color_v = 255
        self.fg_hover_s = 200
        self.fg_hover_v = 255
        self.door_bg_tint_s = 255
        self.door_bg_tint_v = 200

        # color steps
        self.default_color_sliders = [[1, 16, 15], [1, 2, 16], [1, 16, 15], [1, 2, 16], [9, 16, 12], [1, 16, 15], [0, 0, 0]]
        self.reset_colors()
        self.menu_shapes = ["cat_bg_circle", "cat_bg_square", "cat_bg_hex", "cat_bg_star"]

        self.create_colors()

    def reset_default_colors_sv(self, scheme):
        if scheme is None:
            self.font_color_s = 255
            self.font_color_v = 150
            self.bg_color_s = 128
            self.bg_color_v = 255
            self.fg_hover_s = 200
            self.fg_hover_v = 255
            self.door_bg_tint_s = 255
            self.door_bg_tint_v = 200
        else:
            self.font_color_s = scheme.font_color_s
            self.font_color_v = scheme.font_color_v
            self.bg_color_s = scheme.bg_color_s
            self.bg_color_v = scheme.bg_color_v
            self.fg_hover_s = scheme.fg_hover_s
            self.fg_hover_v = scheme.fg_hover_v
            self.door_bg_tint_s = scheme.door_bg_tint_s
            self.door_bg_tint_v = scheme.door_bg_tint_v

    def load_colors(self, json_data_string):
        self.color_sliders = json_data_string
        self.create_colors()

    def reset_colors(self, save=False):
        self.color_sliders = copy.deepcopy(self.default_color_sliders)

    def create_colors(self):
        self.tc_fg_tint_color = ex.hsv_to_rgb(self.color_sliders[0][0] * 16,
                                              self.color_sliders[0][1] * 16,
                                              self.color_sliders[0][2] * 16)

        self.tc_bg_tint_color = ex.hsv_to_rgb(self.color_sliders[1][0] * 16,
                                              self.color_sliders[1][1] * 16,
                                              self.color_sliders[1][2] * 16)

        # category
        self.c_bg_tint_color = ex.hsv_to_rgb(self.color_sliders[0][0] * 16,
                                             self.color_sliders[0][1] * 16,
                                             self.color_sliders[0][2] * 16)

        self.c_fg_tint_color = ex.hsv_to_rgb(self.color_sliders[1][0] * 16,
                                             self.color_sliders[1][1] * 16,
                                             self.color_sliders[1][2] * 16)

        # game
        self.g_bg_tint_color = ex.hsv_to_rgb(self.color_sliders[2][0] * 16,
                                             self.color_sliders[2][1] * 16,
                                             self.color_sliders[2][2] * 16)

        self.g_fg_tint_color = ex.hsv_to_rgb(self.color_sliders[3][0] * 16,
                                             self.color_sliders[3][1] * 16,
                                             self.color_sliders[3][2] * 16)

        # game progress
        self.lvl_completed_col = ex.hsv_to_rgb(self.color_sliders[4][0] * 16,
                                               self.color_sliders[4][1] * 16,
                                               self.color_sliders[4][2] * 16)

        self.lvl_not_compl_col = ex.hsv_to_rgb(self.color_sliders[4][0] * 16, 96, 255)
        self.lvl_not_compl_col_dark = ex.hsv_to_rgb(self.color_sliders[4][0] * 16, 96, 96)

        self.info_buttons_col = ex.hsv_to_rgb(self.color_sliders[5][0] * 16,
                                               self.color_sliders[5][1] * 16,
                                               self.color_sliders[5][2] * 16)

    def update_cfg_color(self, h, s, v):
        self.c_fg_tint_color = ex.hsv_to_rgb(h, s, v)

    def update_cbg_color(self, h, s, v):
        self.c_bg_tint_color = ex.hsv_to_rgb(h, s, v)

    def update_gfg_color(self, h, s, v):
        self.g_fg_tint_color = ex.hsv_to_rgb(h, s, v)

    def update_gbg_color(self, h, s, v):
        self.g_bg_tint_color = ex.hsv_to_rgb(h, s, v)

    def update_lvl_color(self, h, s=0, v=0):
        self.lvl_not_compl_col = ex.hsv_to_rgb(h, 100, 255)
        self.lvl_not_compl_col_dark = ex.hsv_to_rgb(h, 100, 100)
        self.lvl_completed_col = ex.hsv_to_rgb(h, 255, 200)

    def update_info_color(self, h, s, v):
        self.info_buttons_col = ex.hsv_to_rgb(h, s, v)


class WBScheme:
    def __init__(self):
        self.dark = False
        self.u_initcolor = (255, 255, 255)
        self.u_color = (255, 255, 255)
        self.u_font_color = (0, 0, 0)
        self.u_font_color2 = (0, 0, 0)
        self.u_font_color3 = (80, 80, 80)
        self.u_line_color = (240, 240, 240)
        self.shape_color = (230, 230, 230)

        self.color1 = (150, 150, 150)  # bright side of short hand
        self.color3 = (0, 0, 0)  # inner font color
        self.color5 = (90, 90, 90)  # dark side of short hand
        self.color7 = (250, 250, 250)  # inner circle filling

        self.color2 = (100, 100, 255)  # bright side of long hand
        self.color4 = (0, 0, 200)  # outer font color
        self.color6 = (50, 50, 200)  # dark side of long hand
        self.color8 = (230, 230, 230)  # outer circle filling

        self.info_font_color0 = (0, 0, 0, 0)
        self.info_font_color1 = (50, 50, 50, 0)
        self.info_font_color2 = (70, 70, 70, 0)
        self.info_font_color3 = (0, 0, 0, 0)

        self.font_color_s = 255
        self.font_color_v = 127
        self.bg_color_s = 128
        self.bg_color_v = 255
        self.fg_hover_s = 200
        self.fg_hover_v = 255
        self.door_bg_tint_s = 255
        self.door_bg_tint_v = 200


class BWScheme:
    def __init__(self):
        self.dark = True
        self.u_initcolor = (0, 0, 0)
        self.u_color = (0, 0, 0)
        self.u_font_color = (255, 255, 255)
        self.u_font_color2 = (200, 200, 200)
        self.u_font_color3 = (150, 150, 150)
        self.u_line_color = (20, 20, 20)
        self.shape_color = (20, 20, 20)

        self.color1 = (250, 250, 150)  # bright side of short hand
        self.color3 = (200, 200, 0)  # inner font color
        self.color5 = (200, 200, 0)  # dark side of short hand
        self.color7 = (30, 30, 30)  # inner circle filling

        self.color2 = (255, 255, 255)  # bright side of long hand
        self.color4 = (150, 150, 150)  # outer font color
        self.color6 = (150, 150, 200)  # dark side of long hand
        self.color8 = (10, 10, 10)  # outer circle filling

        self.info_font_color0 = (255, 255, 255, 0)
        self.info_font_color1 = (200, 200, 200, 0)
        self.info_font_color2 = (255, 75, 0, 0)
        self.info_font_color3 = (255, 200, 50, 0)

        self.font_color_s = 75
        self.font_color_v = 250
        self.bg_color_s = 200
        self.bg_color_v = 150
        self.fg_hover_s = 200
        self.fg_hover_v = 100
        self.door_bg_tint_s = 100
        self.door_bg_tint_v = 200


class BYScheme:
    def __init__(self):
        self.dark = True
        self.u_initcolor = (0, 0, 0)
        self.u_color = (0, 0, 0)
        self.u_font_color = (255, 255, 0)
        self.u_font_color2 = (50, 50, 255)
        self.u_font_color3 = (150, 150, 0)
        self.u_line_color = (20, 20, 0)
        self.shape_color = (20, 20, 0)

        self.color1 = (250, 250, 150)  # bright side of short hand
        self.color3 = (200, 200, 0)  # inner font color
        self.color5 = (200, 200, 0)  # dark side of short hand
        self.color7 = (30, 30, 30)  # inner circle filling

        self.color2 = (150, 150, 250)  # bright side of long hand
        self.color4 = self.u_font_color2  # outer font color
        self.color6 = (50, 50, 200)  # dark side of long hand
        self.color8 = (10, 10, 10)  # outer circle filling

        self.info_font_color0 = (255, 255, 0, 0)
        self.info_font_color1 = (255, 255, 100, 0)
        self.info_font_color2 = (255, 75, 0, 0)
        self.info_font_color3 = (255, 200, 50, 0)

        self.font_color_s = 75
        self.font_color_v = 250
        self.bg_color_s = 200
        self.bg_color_v = 150
        self.fg_hover_s = 200
        self.fg_hover_v = 100
        self.door_bg_tint_s = 100
        self.door_bg_tint_v = 200
