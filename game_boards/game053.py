# -*- coding: utf-8 -*-

import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.draw_grid = False

        color = ex.hsv_to_rgb(225, 15, 235)
        self.col_r = (255, 0, 0)
        self.col_g = (0, 255, 0)
        self.col_b = (0, 0, 255)
        self.col_k = (0, 0, 0)
        self.col_e = (255, 255, 255)
        colorkey = (2, 2, 2)
        self.col_bg = (255, 255, 255)  # self.col_k #(255,246,219)
        data = [32, 23]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count > 32:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.initcolor = self.col_bg
        self.board.board_bg.color = self.col_bg
        self.board.board_bg.update_me = True

        self.board.moved = self.moved

        y = data[1] - 3

        self.rgb_g = [y, y, y]
        self.rgbx3 = [self.col_k, self.col_k, self.col_k]

        self.board.add_unit(1, y, 2, 3, classes.board.ImgAlphaShip, "", (0, 0, 0, 0), "light_r.png", alpha=True)
        self.board.add_unit(4, y, 2, 3, classes.board.ImgAlphaShip, "", (0, 0, 0, 0), "light_g.png", alpha=True)
        self.board.add_unit(7, y, 2, 3, classes.board.ImgAlphaShip, "", (0, 0, 0, 0), "light_b.png", alpha=True)

        for each in self.board.ships:
            each.outline = False
            each.audible = False
            #each.image.set_colorkey(each.initcolor)

        # add colour circles - canvas
        self.board.add_unit(10, 0, data[0] - 10, data[1], classes.board.Label, "", self.col_e, "", 0)

        self.canvas = self.board.units[0]
        self.canvas_center = [(self.canvas.grid_w * self.board.scale) // 2,
                              (self.canvas.grid_h * self.board.scale) // 2]

        # adding borders between the colour tubes
        self.board.add_unit(0, 0, 1, data[1], classes.board.Label, "", self.col_bg, "", 0)
        self.board.add_unit(3, 0, 1, data[1], classes.board.Label, "", self.col_bg, "", 0)
        self.board.add_unit(6, 0, 1, data[1], classes.board.Label, "", self.col_bg, "", 0)
        self.board.add_unit(9, 0, 1, data[1], classes.board.Label, "", self.col_bg, "", 0)

        # adding colour guides
        self.board.add_door(1, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_r, 1)
        self.board.add_door(4, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_g, 1)
        self.board.add_door(7, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_b, 1)

        # adding colour strips
        self.board.add_door(1, data[1] - 1, 2, 1, classes.board.Door, "", self.col_r, "", 0, door_alpha=False)
        self.board.add_door(4, data[1] - 1, 2, 1, classes.board.Door, "", self.col_g, "", 0, door_alpha=False)
        self.board.add_door(7, data[1] - 1, 2, 1, classes.board.Door, "", self.col_b, "", 0, door_alpha=False)

        # black background
        self.board.add_door(1, 0, 2, data[1], classes.board.Door, "", self.col_k, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(4, 0, 2, data[1], classes.board.Door, "", self.col_k, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(7, 0, 2, data[1], classes.board.Door, "", self.col_k, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)

        # self.color_info = self.board.units[-1]
        for i in [5, 6, 7, 8, 9, 10, 11, 12, 13]:
            if i > 7:
                self.board.units[i].image.set_colorkey(colorkey)
                self.board.all_sprites_list.move_to_back(self.board.units[i])
            else:
                self.board.all_sprites_list.move_to_front(self.board.units[i])
        self.canvas.set_outline((255, 75, 0), 1)
        self.canv = []
        for i in range(4):
            self.canv.append(
                pygame.Surface([self.canvas.grid_w * self.board.scale, self.canvas.grid_h * self.board.scale - 1]))

        self.board.all_sprites_list.move_to_back(self.board.board_bg)
        self.mix()

    def mix(self):
        for i in range(3):
            self.rgb_g[i] = self.board.ships[i].grid_y
        self.update_sliders()
        self.canv[3].fill(self.col_k)
        ct = self.canvas_center
        radius = 9 * self.board.scale
        x = 1 * self.board.scale
        rect = [[ct[0], ct[1] - x], [ct[0] - x, ct[1] + x], [ct[0] + x, ct[1] + x]]
        for i in range(3):
            pygame.draw.circle(self.canv[i], self.rgbx3[i], rect[i], radius, 0)
            self.canv[3].blit(self.canv[i], [0, 0], special_flags=pygame.BLEND_ADD)
        self.canvas.painting = self.canv[3].copy()
        self.canvas.update_me = True

    def update_sliders(self):
        for i in range(3):
            strip = self.board.units[i + 8]
            strip.grid_y = self.rgb_g[i]
            strip.grid_h = self.data[1] - strip.grid_y + 3
            col = []
            for each in strip.initcolor:
                if each > 0:
                    if strip.grid_y == 20:
                        col.append(0)
                    elif strip.grid_y == 0:
                        col.append(255)
                    else:
                        step = 255 / 20.0
                        col.append(int(255 - (strip.grid_y) * step))
                else:
                    col.append(0)
            self.rgbx3[i] = col
            strip.color = col
            strip.pos_update()
            strip.update_me = True

    def moved(self):
        self.mix()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up

    def update(self, game):
        game.fill((0, 0, 0))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
