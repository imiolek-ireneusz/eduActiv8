# -*- coding: utf-8 -*-

import os
import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.decolorable = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 1, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.board.draw_grid = False
        white = (255, 255, 255)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                white = (0, 0, 0)
        outline_color = (150, 150, 150)
        # setting level variable
        # data = [x_count, y_count, number_count, top_limit, ordered]
        if self.level.lvl == 1:
            data = [5, 4, 5, 3, 2]
        elif self.level.lvl == 2:
            data = [5, 5, 8, 3, 3]
        elif self.level.lvl == 3:
            data = [6, 4, 7, 4, 2]
        elif self.level.lvl == 4:
            data = [6, 5, 11, 4, 3]
        elif self.level.lvl == 5:
            data = [6, 6, 15, 4, 4]
        elif self.level.lvl == 6:
            data = [7, 4, 9, 5, 2]
        elif self.level.lvl == 7:
            data = [7, 5, 14, 5, 3]
        elif self.level.lvl == 8:
            data = [7, 6, 19, 5, 4]
        elif self.level.lvl == 9:
            data = [8, 4, 11, 6, 2]
        elif self.level.lvl == 10:
            data = [8, 5, 17, 6, 3]

        self.chapters = [1, 5, 10]

        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            x_count = self.get_x_count(data[1], even=True)
        else:
            x_count = self.get_x_count(data[1], even=False)

        if x_count > data[0]:
            data[0] = x_count

        self.data = data
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        image_src = [os.path.join('numbers_alpha', "n%d.png" % i) for i in range(1, 22)]
        self.choice_list = [x for x in range(1, data[2] + 1)]
        self.shuffled = self.choice_list[:]
        random.shuffle(self.shuffled)

        inversions = ex.inversions(self.shuffled)
        if inversions % 2 != 0:  # if number of inversions is odd it is unsolvable
            # in unsolvable combinations swapping 2 squares will make it solvable
            temp = self.shuffled[0]
            self.shuffled[0] = self.shuffled[1]
            self.shuffled[1] = temp

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4]  # height of the bottom margin
        w2 = (data[0] - data[3]) // 2  # side margin width
        self.check = [h1, h2, w2]

        # create table to store 'binary' solution
        # find position of first door square
        x = w2
        y = h1
        self.mini_grid = []

        h = random.randrange(0, 255, 5)
        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
            img_style = "bb"
            self.default_bg_color = ex.hsv_to_rgb(h, 200, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 230, 90)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 150, 200), ]

            self.selected_color = ex.hsv_to_rgb(h, 150, 50)
            self.selected_font_color = [ex.hsv_to_rgb(h, 150, 100), ]
        else:
            img_style = "wb"
            self.default_bg_color = ex.hsv_to_rgb(h, 150, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 80, self.mainloop.cl.bg_color_v)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 200, self.mainloop.cl.font_color_v), ]

            self.selected_color = ex.hsv_to_rgb(h, 50, self.mainloop.cl.bg_color_v)
            self.selected_font_color = [ex.hsv_to_rgb(h, 50, 250), ]

        self.dc_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        if self.mainloop.m.game_variant == 4:
            self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s150.png" % img_style)
        elif self.mainloop.m.game_variant == 5:
            self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s20.png" % img_style)

        fg_tint_color = (40, 40, 40)

        # add objects to the board
        line = []
        for i in range(data[2]):
            caption = str(self.shuffled[i])
            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=image_src[self.shuffled[i]], bg_img_src=image_src[self.shuffled[i]], dc_img_src=self.dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                          bg_tint_color=None, dc_tint_color=self.default_bg_color,
                                          fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                          multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
            self.units.append(self.board.ships[-1])

            self.board.ships[-1].readable = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            line.append(i)
            x += 1
            if x >= w2 + data[3] or i == data[2] - 1:
                x = w2
                y += 1
                self.mini_grid.append(line)
                line = []
        self.outline_all(outline_color, 1)

        # horizontal
        self.board.add_unit(0, 0, data[0], h1, classes.board.Obstacle, "", white, "", 7)  # top
        self.board.add_unit(0, h1 + data[4], data[0], h2, classes.board.Obstacle, "", white, "", 7)  # bottom 1
        # side obstacles
        self.board.add_unit(0, h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # left
        self.board.add_unit(w2 + data[3], h1, w2, data[4], classes.board.Obstacle, "", white, "", 7)  # right

        self.board.all_sprites_list.move_to_front(self.board.units[0])

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Re-arrange right"])

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        current = [x for x in range(self.data[2] + 1)]  # self.choice_list[:]
        # collect value and x position on the grid from ships list
        for i in range(len(self.board.ships)):
            x = self.board.ships[i].grid_x - self.check[2]
            y = self.board.ships[i].grid_y - self.check[0]
            w = self.data[3]
            pos = x + (y * w)
            current[pos] = int(self.board.ships[i].value)
            if pos < self.data[2]:
                if self.choice_list[pos] == current[pos]:
                    self.board.ships[i].set_display_check(True)
                else:
                    self.board.ships[i].set_display_check(False)
            else:
                self.board.ships[i].set_display_check(False)

        del (current[-1])
        if self.choice_list == current:
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True
