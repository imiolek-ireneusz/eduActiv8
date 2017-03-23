# -*- coding: utf-8 -*-

class Color:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.grid_line = (240, 240, 240)

        # orange
        self.menu_l = (255, 75, 0)
        # self.menu_r   = (60,60,60)
        self.menu_r = (33, 121, 149)
        self.info = (70, 70, 70)


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


"""
class YBScheme:
    def __init__(self):
        self.dark = False
        self.u_initcolor = (255,255,0)
        self.u_color = (255,255,0)
        self.u_font_color = (0,0,0)
        self.u_font_color2 = (255,255,255)
        self.u_line_color = (240, 240, 0)
"""


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
