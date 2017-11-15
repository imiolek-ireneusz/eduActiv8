# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 6, 3)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.board.decolorable = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False

        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 30, 240)  # highlight 1
        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
        self.font_color = self.color2
        black = (2, 2, 2)
        white = (255, 255, 255)

        bg_col = (255, 255, 255)
        if self.mainloop.scheme is not None:
            if self.level.lvl > 1:
                self.font_color = self.mainloop.scheme.u_font_color
            if self.mainloop.scheme.dark:
                bg_col = (0, 0, 0)
                color0 = (0, 0, 0)
                black = (30, 30, 30)
            else:
                color0 = (255, 255, 255)
                white = (240, 240, 240)

        choice = [x for x in range(0, 20)]
        self.color_choice = [self.d["white"], self.d["black"], self.d["grey"], self.d["red"], self.d["orange"],
                             self.d["yellow"], self.d["olive"], self.d["green"], self.d["sea green"], self.d["teal"],
                             self.d["blue"], self.d["navy"], self.d["purple"], self.d["magenta"], self.d["indigo"],
                             self.d["pink"], self.d["maroon"], self.d["brown"], self.d["aqua"], self.d["lime"]]
        # self.color_choice= ["white",    "black",      "grey",       "red",     "orange",  "yellow",   "olive",    "green",  "sea green","teal",     "blue",   "navy",   "purple",   "violet",     "magenta",  "indigo",  "pink"       "maroon",  "brown",     "aqua",      "lime" ]
        self.hue_choice = [[255, 255, 255], [2, 2, 2], [140, 140, 140], [255, 0, 0], [255, 138, 0], [255, 255, 0],
                           [181, 219, 3], [0, 160, 0], [41, 131, 82], [0, 130, 133], [0, 0, 255], [0, 0, 132],
                           [132, 0, 132], [255, 0, 255], [74, 0, 132], [255, 20, 138], [132, 0, 0], [140, 69, 16],
                           [0, 255, 255], [0, 255, 0]]
        self.hue_choice2 = [[150, 150, 150], [100, 100, 100], [100, 100, 100], [200, 0, 0], [200, 80, 0], [200, 200, 0],
                            [121, 159, 3], [0, 100, 0], [31, 100, 52], [0, 90, 90], [0, 0, 200], [0, 0, 82],
                            [92, 0, 92], [200, 0, 200], [44, 0, 82], [200, 10, 88], [100, 0, 0], [100, 39, 6],
                            [0, 200, 200], [0, 200, 0]]
        self.font_colorx = [[0, 0, 0], [225, 225, 225], [0, 0, 0], [100, 0, 0], [100, 40, 0], [100, 100, 0],
                            [60, 80, 3], [0, 50, 0], [11, 50, 22], [0, 40, 40], [0, 0, 100], [0, 0, 255], [255, 0, 255],
                            [100, 0, 100], [140, 0, 255], [100, 5, 48], [200, 50, 50], [200, 100, 26], [0, 155, 155],
                            [0, 155, 0]]
        self.init_font_color = [white, black, [140, 140, 140], [255, 0, 0], [255, 138, 0], [255, 255, 0], [181, 219, 3],
                                [0, 160, 0], [41, 131, 82], [0, 130, 133], [0, 0, 255], [0, 0, 132], [132, 0, 132],
                                [255, 0, 255], [74, 0, 132], [255, 20, 138], [132, 0, 0], [140, 69, 16], [0, 255, 255],
                                [0, 255, 0]]

        font_size = 6
        self.disp_counter = 0
        self.disp_len = 1

        if self.level.lvl == 1:
            data = [8, 3, 3, 2, 3]
        elif self.level.lvl == 2:
            data = [8, 4, 3, 2, 4]
        elif self.level.lvl == 3:
            data = [8, 5, 3, 2, 5]

        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            x = self.get_x_count(data[1], even=True)
        else:
            x = self.get_x_count(data[1], even=False)

        if x > data[0]:
            data[0] = x

        self.data = data

        self.found = 0
        self.clicks = 0

        self.squares = self.data[3] * self.data[4]

        self.square_count = self.squares * 2  # self.data[3]*self.data[4]
        self.history = [None, None]

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.completed_mode = False

        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4]  # -1 #height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3] * 4) // 2  # side margin width

        small_slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2, w2 + data[3]):
                small_slots.append([i, j])
        random.shuffle(small_slots)

        wide_slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2 + data[3], data[0] - w2, 3):
                wide_slots.append([i, j])
        random.shuffle(wide_slots)

        switch = self.square_count // 2
        for i in range(self.square_count):
            fc = self.font_color
            if i < switch:
                caption = ""
                position_list = small_slots
                pos = i
                xw = 1
            else:
                caption = self.color_choice[self.chosen[i - switch]]
                position_list = wide_slots
                pos = i - switch
                xw = 3
                if self.level.lvl == 1:
                    fc = self.init_font_color[self.chosen[i - switch]]
            self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, 1, classes.board.Letter, caption,
                                color0, "", font_size)
            self.board.ships[-1].font_color = fc

            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(self.color2, 1)

        lines = [[135, 128], [133, 132], [135, 137], [157, 157], [158, 161], [155, 165], [150, 166], [146, 163],
                 [133, 140], [129, 138], [125, 139],
                 [122, 142], [122, 144], [128, 157], [128, 159], [126, 161], [123, 161], [121, 160], [114, 147],
                 [112, 145], [107, 145], [104, 148],
                 [104, 154], [110, 179], [111, 186], [110, 192], [105, 194], [100, 193], [98, 188], [98, 180],
                 [101, 154], [100, 148], [96, 146],
                 [93, 147], [92, 149], [88, 163], [86, 165], [83, 165], [80, 164], [80, 161], [80, 158], [83, 147],
                 [82, 143], [73, 139],
                 [65, 143], [55, 167], [52, 174], [48, 179], [42, 178], [37, 174], [38, 169], [43, 163], [57, 151],
                 [63, 144], [67, 137],
                 [66, 129], [60, 126], [51, 138], [47, 141], [44, 142], [40, 140], [38, 136], [40, 134], [44, 131],
                 [57, 124], [56, 117],
                 [51, 114], [43, 120], [40, 122], [38, 124], [36, 124], [34, 122], [34, 119], [36, 117], [50, 111],
                 [52, 108], [53, 102],
                 [51, 98], [46, 96], [38, 97], [11, 103], [5, 103], [3, 99], [4, 94], [10, 92], [36, 94], [44, 94],
                 [50, 91],
                 [53, 87], [52, 83], [46, 81], [21, 79], [14, 78], [9, 76], [8, 73], [10, 71], [15, 71], [22, 72],
                 [45, 77],
                 [51, 77], [53, 74], [52, 69], [40, 60], [39, 57], [39, 55], [41, 53], [44, 53], [47, 54], [55, 59],
                 [58, 59],
                 [61, 58], [62, 55], [61, 52], [54, 43], [54, 41], [55, 38], [58, 37], [61, 39], [71, 51], [74, 52],
                 [80, 50],
                 [81, 46], [80, 40], [77, 32], [66, 18], [62, 12], [61, 6], [65, 3], [70, 2], [74, 6], [76, 13],
                 [79, 30],
                 [81, 37], [86, 42], [91, 43], [95, 41], [95, 39], [93, 28], [93, 25], [93, 23], [96, 22], [99, 22],
                 [100, 24],
                 [100, 28], [99, 39], [101, 41], [103, 42], [106, 42], [108, 40], [111, 29], [112, 26], [114, 25],
                 [117, 24], [119, 26],
                 [120, 29], [119, 33], [116, 45], [117, 48], [119, 50], [122, 50], [135, 33], [137, 31], [140, 31],
                 [142, 34], [142, 37],
                 [133, 53], [133, 56], [134, 59], [137, 59], [141, 56], [155, 40], [160, 36], [164, 35], [169, 38],
                 [170, 42], [168, 46],
                 [163, 50], [146, 59], [144, 62], [145, 66], [149, 67], [160, 64], [162, 63], [164, 64], [165, 66],
                 [165, 69], [164, 71],
                 [150, 77], [148, 79], [148, 84], [150, 88], [155, 89], [173, 81], [179, 79], [183, 79], [185, 83],
                 [186, 90], [184, 93],
                 [180, 95], [175, 94], [158, 95], [154, 99], [153, 103], [156, 106], [163, 108], [185, 113], [190, 115],
                 [191, 118], [189, 122],
                 [184, 121], [163, 111], [156, 109], [151, 110], [147, 115], [145, 120], [146, 124], [151, 128],
                 [163, 135], [168, 139], [171, 142],
                 [171, 146], [167, 146], [162, 144], [158, 140], [149, 132], [144, 128], [140, 127]]
        size = self.board.ships[0].grid_w * self.board.scale
        margin = size // 20
        # new point = size * orig_point / 200
        self.scaled_lines = [
            [int((size - 2 * margin) * each[0] / 200.0) + margin, int((size - 2 * margin) * each[1] / 200.0) + margin]
            for each in lines]
        for i in range(self.squares):
            color1 = self.hue_choice[self.chosen[i]]  # ex.hsv_to_rgb(h,s,v)
            color2 = self.hue_choice2[self.chosen[i]]  # ex.hsv_to_rgb(h,255,255)
            canvas = pygame.Surface([size, size - 1])
            canvas.fill(self.board.ships[i].initcolor)
            self.draw_splash(canvas, size, color1, color2)  # data[7](data, canvas, i)
            self.board.ships[i].painting = canvas.copy()
            self.board.ships[i].image = canvas.copy()

    def draw_splash(self, canvas, size, color, outline_color):
        pygame.draw.polygon(canvas, color, self.scaled_lines, 0)
        pygame.draw.aalines(canvas, outline_color, True, self.scaled_lines)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[
            1] == None and self.ai_enabled == False:  # and self.start_sequence==False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if active.uncovered == False:
                    if self.history[0] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[0] = active
                        self.clicks += 1
                        active.uncovered = True
                    elif self.history[1] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[1] = active
                        self.clicks += 1
                        if self.chosen[self.history[0].unit_id] != self.chosen[self.history[1].unit_id]:
                            self.ai_enabled = True
                            self.history[0].uncovered = False
                        else:
                            self.history[0].uncovered = True
                            self.history[1].uncovered = True
                            self.history[0].perm_outline_color = self.color2  # [50,255,50]
                            self.history[1].perm_outline_color = self.color2
                            self.history[0].image.set_alpha(50)
                            self.history[1].image.set_alpha(50)
                            self.history[0].update_me = True
                            self.history[1].update_me = True
                            self.history[0].set_display_check(True)
                            self.history[1].set_display_check(True)

                            self.found += 2
                            if self.found == self.square_count:
                                self.completed_mode = True
                                self.ai_enabled = True
                            self.history = [None, None]
                    active.update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.level.next_board()
            else:
                self.history[0].perm_outline_width = 1
                self.history[0].perm_outline_color = self.color2
                self.history[1].perm_outline_width = 1
                self.history[1].perm_outline_color = self.color2
                self.history[0].update_me = True
                self.history[1].update_me = True
                self.history = [None, None]
                self.ai_enabled = False
                self.disp_counter = 0

    def check_result(self):
        pass
