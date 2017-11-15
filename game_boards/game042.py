# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 10, 4)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 5, 3)

    def create_game_objects(self, level=1):
        self.board.decolorable = False
        self.board.draw_grid = False
        white = (255, 255, 255, 0)
        self.font_col = (0, 0, 0)
        if self.mainloop.scheme is not None:
            if self.level.lvl > 1:
                self.font_col = self.mainloop.scheme.u_font_color

        if self.level.lvl == 1:
            choice = [x for x in range(0, 20)]
            self.color_choice = [self.d["white"], self.d["black"], self.d["grey"], self.d["red"], self.d["orange"],
                                 self.d["yellow"], self.d["olive"], self.d["green"], self.d["sea green"],
                                 self.d["teal"], self.d["blue"], self.d["navy"], self.d["purple"], self.d["magenta"],
                                 self.d["indigo"], self.d["pink"], self.d["maroon"], self.d["brown"], self.d["aqua"],
                                 self.d["lime"]]
            self.color_choicep = [self.dp["white"], self.dp["black"], self.dp["grey"], self.dp["red"],
                                  self.dp["orange"], self.dp["yellow"], self.dp["olive"], self.dp["green"],
                                  self.dp["sea green"], self.dp["teal"], self.dp["blue"], self.dp["navy"],
                                  self.dp["purple"], self.dp["magenta"], self.dp["indigo"], self.dp["pink"],
                                  self.dp["maroon"], self.dp["brown"], self.dp["aqua"], self.dp["lime"]]
            # self.color_choice= ["white",    "black",      "grey",       "red",     "orange",  "yellow",   "olive",    "green",  "sea green","teal",     "blue",   "navy",   "purple",    "magenta",  "indigo",  "pink"       "maroon",  "brown",     "aqua",      "lime" ]
            self.hue_choice = [[255, 255, 255, 255], [0, 0, 0, 255], [140, 140, 140], [255, 0, 0], [255, 138, 0], [255, 255, 0],
                               [181, 219, 3], [0, 160, 0], [41, 131, 82], [0, 130, 133], [0, 0, 255], [0, 0, 132],
                               [132, 0, 132], [255, 0, 255], [74, 0, 132], [255, 20, 138], [132, 0, 0], [140, 69, 16],
                               [0, 255, 255], [0, 255, 0]]
            self.hue_choice2 = [[150, 150, 150], [100, 100, 100], [100, 100, 100], [200, 0, 0], [200, 80, 0],
                                [200, 200, 0], [121, 159, 3], [0, 100, 0], [31, 100, 52], [0, 90, 90], [0, 0, 200],
                                [0, 0, 82], [92, 0, 92], [200, 0, 200], [44, 0, 82], [200, 10, 88], [100, 0, 0],
                                [100, 39, 6], [0, 200, 200], [0, 200, 0]]
            self.font_color = [[0, 0, 0], [225, 225, 225], [0, 0, 0], [100, 0, 0], [100, 40, 0], [100, 100, 0],
                               [60, 80, 3], [0, 50, 0], [11, 50, 22], [0, 40, 40], [0, 0, 100], [0, 0, 255],
                               [255, 0, 255], [100, 0, 100], [140, 0, 255], [100, 5, 48], [200, 50, 50], [200, 100, 26],
                               [0, 155, 155], [0, 155, 0]]
            self.init_font_color = [[230, 230, 230], [2, 2, 2], [140, 140, 140], [255, 0, 0], [255, 138, 0],
                                    [255, 255, 0], [181, 219, 3], [0, 160, 0], [41, 131, 82], [0, 130, 133],
                                    [0, 0, 255], [0, 0, 132], [132, 0, 132], [255, 0, 255], [74, 0, 132],
                                    [255, 20, 138], [132, 0, 0], [140, 69, 16], [0, 255, 255], [0, 255, 0]]
        elif self.level.lvl == 2:
            choice = [x for x in range(0, 13)]
            self.color_choice = [self.d["white"], self.d["black"], self.d["grey"], self.d["red"], self.d["orange"],
                                 self.d["yellow"], self.d["olive"], self.d["green"], self.d["blue"], self.d["navy"],
                                 self.d["purple"], self.d["pink"], self.d["brown"]]
            self.color_choicep = [self.dp["white"], self.dp["black"], self.dp["grey"], self.dp["red"],
                                  self.dp["orange"], self.dp["yellow"], self.dp["olive"], self.dp["green"],
                                  self.dp["blue"], self.dp["navy"], self.dp["purple"], self.dp["pink"],
                                  self.dp["brown"]]
            # self.color_choice= ["white",    "black",      "grey",      "red",     "orange",   "yellow",   "olive",    "green",  "blue",    "navy",   "purple",   "pink"]
            self.hue_choice = [[255, 255, 255, 255], [0, 0, 0, 255], [140, 140, 140], [255, 0, 0], [255, 138, 0], [255, 255, 0],
                               [181, 219, 3], [0, 160, 0], [0, 0, 255], [0, 0, 132], [132, 0, 132], [255, 20, 138],
                               [140, 69, 16]]
            self.hue_choice2 = [[150, 150, 150], [100, 100, 100], [100, 100, 100], [200, 0, 0], [200, 80, 0],
                                [200, 200, 0], [121, 159, 3], [0, 100, 0], [0, 0, 200], [0, 0, 82], [92, 0, 92],
                                [200, 10, 88], [100, 39, 6]]
            self.font_color = [[0, 0, 0], [225, 225, 225], [0, 0, 0], [100, 0, 0], [100, 40, 0], [100, 100, 0],
                               [60, 80, 3], [0, 50, 0], [0, 0, 100], [0, 0, 255], [255, 0, 255], [100, 5, 48],
                               [200, 100, 26]]
            self.init_font_color = [self.font_col for i in range(13)]
        elif self.level.lvl >= 3:
            choice = [x for x in range(0, 20)]
            self.color_choice = [self.d["white"], self.d["black"], self.d["grey"], self.d["red"], self.d["orange"],
                                 self.d["yellow"], self.d["olive"], self.d["green"], self.d["sea green"],
                                 self.d["teal"], self.d["blue"], self.d["navy"], self.d["purple"], self.d["magenta"],
                                 self.d["indigo"], self.d["pink"], self.d["maroon"], self.d["brown"], self.d["aqua"],
                                 self.d["lime"]]
            self.color_choicep = [self.dp["white"], self.dp["black"], self.dp["grey"], self.dp["red"],
                                  self.dp["orange"], self.dp["yellow"], self.dp["olive"], self.dp["green"],
                                  self.dp["sea green"], self.dp["teal"], self.dp["blue"], self.dp["navy"],
                                  self.dp["purple"], self.dp["magenta"], self.dp["indigo"], self.dp["pink"],
                                  self.dp["maroon"], self.dp["brown"], self.dp["aqua"], self.dp["lime"]]
            # self.color_choice= ["white",    "black",      "grey",       "red",     "orange",  "yellow",   "olive",    "green",  "sea green","teal",     "blue",   "navy",   "purple",    "magenta",  "indigo",  "pink"       "maroon",  "brown",     "aqua",      "lime" ]
            self.hue_choice = [[255, 255, 255, 255], [0, 0, 0, 255], [140, 140, 140], [255, 0, 0], [255, 138, 0], [255, 255, 0],
                               [181, 219, 3], [0, 160, 0], [41, 131, 82], [0, 130, 133], [0, 0, 255], [0, 0, 132],
                               [132, 0, 132], [255, 0, 255], [74, 0, 132], [255, 20, 138], [132, 0, 0], [140, 69, 16],
                               [0, 255, 255], [0, 255, 0]]
            self.hue_choice2 = [[150, 150, 150], [100, 100, 100], [100, 100, 100], [200, 0, 0], [200, 80, 0],
                                [200, 200, 0], [121, 159, 3], [0, 100, 0], [31, 100, 52], [0, 90, 90], [0, 0, 200],
                                [0, 0, 82], [92, 0, 92], [200, 0, 200], [44, 0, 82], [200, 10, 88], [100, 0, 0],
                                [100, 39, 6], [0, 200, 200], [0, 200, 0]]
            self.font_color = [[0, 0, 0], [225, 225, 225], [0, 0, 0], [100, 0, 0], [100, 40, 0], [100, 100, 0],
                               [60, 80, 3], [0, 50, 0], [11, 50, 22], [0, 40, 40], [0, 0, 100], [0, 0, 255],
                               [255, 0, 255], [100, 0, 100], [140, 0, 255], [100, 5, 48], [200, 50, 50], [200, 100, 26],
                               [0, 155, 155], [0, 155, 0]]
            self.init_font_color = [self.font_col for i in range(20)]

        self.bg_col = (255, 255, 255, 0)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.bg_col = (0, 0, 0, 0)
                if self.level.lvl == 1:
                    self.init_font_color[1] = (30, 30, 30)

        data = [5, 3]

        if self.lang.lang in ["en_GB", "en_US"]:
            font_size = 10
        else:
            font_size = 11
        # stretch width to fit the screen size
        max_x_count = self.get_x_count(data[1], even=False)
        if max_x_count > 5:
            data[0] = max_x_count

        self.data = data
        self.center = self.data[0] // 2
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:5]

        self.shuffled2 = self.chosen[:]
        random.shuffle(self.shuffled2)
        x = self.center - 2
        self.color_pos_offset = x
        for i in range(5):
            self.board.add_door(x + i, 0, 1, 1, classes.board.Door, self.color_choice[self.chosen[i]], self.bg_col)
            self.board.add_unit(x + i, 2, 1, 1, classes.board.Letter, self.color_choice[self.shuffled2[i]], self.bg_col,
                                "", alpha=True, font_size=font_size)

            self.board.ships[-1].speaker_val = self.color_choicep[self.shuffled2[i]]
            self.board.ships[-1].speaker_val_update = False
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()
            font_color = self.init_font_color[self.shuffled2[i]]
            if self.level.lvl == 1:
                self.board.ships[i].font_color = font_color
            else:
                self.board.ships[i].font_color = self.font_col
            if self.level.lvl == 4:
                self.board.ships[i].readable = False
        # self.board.add_door(0,0,data[0],data[1],classes.board.Door,"",white)
        # self.board.units[-1].image.set_colorkey(None)
        for each in self.board.ships:
            self.board.all_sprites_list.move_to_front(each)
            each.highlight = False
            # each.outline_highlight = False
            # each.set_outline([180, 180, 250], 1)

        for each in self.board.units:
            each.outline = False
            each.show_value = False

        # splash polygon - unscalled - size 200x200
        lines = [[135, 128], [133, 132], [135, 137], [157, 157], [158, 161], [155, 165], [150, 166], [146, 163],
                 [133, 140], [129, 138], [125, 139], [122, 142], [122, 144], [128, 157], [128, 159], [126, 161],
                 [123, 161], [121, 160], [114, 147], [112, 145], [107, 145], [104, 148], [104, 154], [110, 179],
                 [111, 186], [110, 192], [105, 194], [100, 193], [98, 188], [98, 180], [101, 154], [100, 148],
                 [96, 146], [93, 147], [92, 149], [88, 163], [86, 165], [83, 165], [80, 164], [80, 161], [80, 158],
                 [83, 147], [82, 143], [73, 139], [65, 143], [55, 167], [52, 174], [48, 179], [42, 178], [37, 174],
                 [38, 169], [43, 163], [57, 151], [63, 144], [67, 137], [66, 129], [60, 126], [51, 138], [47, 141],
                 [44, 142], [40, 140], [38, 136], [40, 134], [44, 131], [57, 124], [56, 117], [51, 114], [43, 120],
                 [40, 122], [38, 124], [36, 124], [34, 122], [34, 119], [36, 117], [50, 111], [52, 108], [53, 102],
                 [51, 98], [46, 96], [38, 97], [11, 103], [5, 103], [3, 99], [4, 94], [10, 92], [36, 94], [44, 94],
                 [50, 91], [53, 87], [52, 83], [46, 81], [21, 79], [14, 78], [9, 76], [8, 73], [10, 71], [15, 71],
                 [22, 72], [45, 77], [51, 77], [53, 74], [52, 69], [40, 60], [39, 57], [39, 55], [41, 53], [44, 53],
                 [47, 54], [55, 59], [58, 59], [61, 58], [62, 55], [61, 52], [54, 43], [54, 41], [55, 38], [58, 37],
                 [61, 39], [71, 51], [74, 52], [80, 50], [81, 46], [80, 40], [77, 32], [66, 18], [62, 12], [61, 6],
                 [65, 3], [70, 2], [74, 6], [76, 13], [79, 30], [81, 37], [86, 42], [91, 43], [95, 41], [95, 39],
                 [93, 28], [93, 25], [93, 23], [96, 22], [99, 22], [100, 24], [100, 28], [99, 39], [101, 41], [103, 42],
                 [106, 42], [108, 40], [111, 29], [112, 26], [114, 25], [117, 24], [119, 26], [120, 29], [119, 33],
                 [116, 45], [117, 48], [119, 50], [122, 50], [135, 33], [137, 31], [140, 31], [142, 34], [142, 37],
                 [133, 53], [133, 56], [134, 59], [137, 59], [141, 56], [155, 40], [160, 36], [164, 35], [169, 38],
                 [170, 42], [168, 46], [163, 50], [146, 59], [144, 62], [145, 66], [149, 67], [160, 64], [162, 63],
                 [164, 64], [165, 66], [165, 69], [164, 71], [150, 77], [148, 79], [148, 84], [150, 88], [155, 89],
                 [173, 81], [179, 79], [183, 79], [185, 83], [186, 90], [184, 93], [180, 95], [175, 94], [158, 95],
                 [154, 99], [153, 103], [156, 106], [163, 108], [185, 113], [190, 115], [191, 118], [189, 122],
                 [184, 121], [163, 111], [156, 109], [151, 110], [147, 115], [145, 120], [146, 124], [151, 128],
                 [163, 135], [168, 139], [171, 142], [171, 146], [167, 146], [162, 144], [158, 140], [149, 132],
                 [144, 128], [140, 127]]
        size = self.board.units[0].grid_w * self.board.scale
        # new point = size * orig_point / 200
        self.scaled_lines = [[int(size * each[0] / 200.0), int(size * each[1] / 200.0)] for each in lines]
        for i in range(5):
            color1 = self.hue_choice[self.chosen[i]]
            color2 = self.hue_choice2[self.chosen[i]]
            canvas = pygame.Surface([size, size - 1], flags=pygame.SRCALPHA)
            canvas.fill(self.board.units[i].initcolor)
            self.draw_splash(canvas, size, color1, color2)
            self.board.units[i].painting = canvas.copy()

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def draw_splash(self, canvas, size, color, outline_color):
        pygame.draw.polygon(canvas, color, self.scaled_lines, 0)
        #pygame.draw.aalines(canvas, outline_color, True, self.scaled_lines)
        pygame.draw.lines(canvas, outline_color, True, self.scaled_lines)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        if event.type == pygame.MOUSEMOTION:
            if self.drag:
                self.swap_font_color()
            #  if self.drag and self.mouse_entered_new:
            #  self.swap_font_color()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.swap_font_color()
            self.check_result()
            #  if self.drag and self.mouse_entered_new:
            #  self.swap_font_color()

    def after_keydown_move(self):
        # in case somebody uses keyboard to move the labels
        self.swap_font_color()

    def swap_font_color(self):
        active_ship = self.board.ships[self.board.active_ship]
        if active_ship.grid_y == 0 and self.color_pos_offset <= active_ship.grid_x < 5 + self.color_pos_offset:
            active_ship.font_color = self.font_color[self.chosen[active_ship.grid_x - self.color_pos_offset]]
        else:
            if self.level.lvl == 1:
                active_ship.font_color = self.init_font_color[self.shuffled2[self.board.active_ship]]
            else:
                active_ship.font_color = self.font_col  # (0,0,0,0)
        active_ship.update_me = True

    def update(self, game):
        game.fill(self.bg_col)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        # checking copied from number sorting game and re-done
        match_found = False
        if self.board.grid[0][self.center - 2:self.center + 3] == [1, 1, 1, 1, 1]:  # self.solution_grid:
            ships = []
            units = []
            # collect value and x position on the grid from ships list
            for i in range(5):
                ships.append([self.board.ships[i].grid_x, self.board.ships[i].value, self.board.ships[i]])
                units.append([self.board.units[i].grid_x, self.board.units[i].value])
            # ships_sorted = sorted(ships)
            ships.sort()
            units.sort()
            correct = True
            for i in range(5):
                if ships[i][1] != units[i][1]:
                    ships[i][2].set_display_check(False)
                    correct = False
                else:
                    ships[i][2].set_display_check(True)

            if correct == True:
                match_found = True
                #break
        if match_found:
            self.level.next_board()

        self.mainloop.redraw_needed[0] = True
