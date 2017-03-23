# -*- coding: utf-8 -*-

import math
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


def cubicInt(t, a, b):
    weight = t * t * (3 - 2 * t)
    return a + weight * (b - a)


def get_r(r, y, b):
    # red
    x0 = cubicInt(b, 1.0, 0.163)
    x1 = cubicInt(b, 1.0, 0.0)
    x2 = cubicInt(b, 1.0, 0.5)
    x3 = cubicInt(b, 1.0, 0.2)
    y0 = cubicInt(y, x0, x1)
    y1 = cubicInt(y, x2, x3)
    return int(math.ceil(255 * cubicInt(r, y0, y1)))


def get_g(r, y, b):
    # green
    x0 = cubicInt(b, 1.0, 0.373)
    x1 = cubicInt(b, 1.0, 0.66)
    x2 = cubicInt(b, 0.0, 0.0)
    x3 = cubicInt(b, 0.5, 0.094)
    y0 = cubicInt(y, x0, x1)
    y1 = cubicInt(y, x2, x3)
    return int(math.ceil(255 * cubicInt(r, y0, y1)))


def get_b(r, y, b):
    # blue
    x0 = cubicInt(b, 1.0, 0.6)
    x1 = cubicInt(b, 0.0, 0.2)
    x2 = cubicInt(b, 0.0, 0.5)
    x3 = cubicInt(b, 0.0, 0.0)
    y0 = cubicInt(y, x0, x1)
    y1 = cubicInt(y, x2, x3)
    return int(math.ceil(255 * cubicInt(r, y0, y1)))


def ryb_to_rgb(r, y, b):
    if 0 <= r <= 1 and 0 <= y <= 1 and 0 <= b <= 1:
        rgb = [[], [], []]
        rgb[0] = get_r(r, y, b)
        rgb[1] = get_g(r, y, b)
        rgb[2] = get_b(r, y, b)
        return rgb
    else:
        return (255, 255, 255)


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.decolorable = False
        self.board.draw_grid = False

        color = ex.hsv_to_rgb(225, 15, 235)
        color2 = (255, 255, 255)
        self.col_r = (254, 39, 18)
        self.col_y = (254, 254, 51)
        self.col_b = (2, 71, 254)
        self.col_k = (0, 0, 0)
        self.col_e = (255, 255, 255)
        self.col_e2 = (240, 240, 240)
        self.col_e3 = (235, 235, 235)
        colorkey = (2, 2, 2)
        # self.col_bg = (255, 255, 255, 0)
        self.col_bg = (0, 0, 0, 0)
        data = [30, 23]
        x_count = self.get_x_count(data[1], even=True)
        if x_count > 30:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.initcolor = self.col_e
        self.board.board_bg.color = self.col_e
        self.board.board_bg.update_me = True

        self.board.moved = self.moved

        y = data[1] - 3

        self.rybke_g = [y, y, y, y, y]
        self.rybke = [0, 0, 0, 0, 0]

        self.board.add_unit(1, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "tube_r.png", alpha=True)
        self.board.add_unit(4, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "tube_y.png", alpha=True)
        self.board.add_unit(7, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "tube_b.png", alpha=True)
        self.board.add_unit(10, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "tube_k.png", alpha=True)
        self.board.add_unit(13, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "tube_e.png", alpha=True)

        for each in self.board.ships:
            each.outline = False
            each.audible = False

        # add colour container
        self.board.add_unit(16, 0, data[0] - 16, data[1], classes.board.Label, "", self.col_e, "", 0)

        self.canvas = self.board.units[0]
        self.canvas_center = [(self.canvas.grid_w * self.board.scale) // 2,
                              (self.canvas.grid_h * self.board.scale) // 2]

        # adding borders between the colour tubes
        self.board.add_unit(0, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(3, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(6, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(9, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(12, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(15, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)

        # adding colour guides
        self.board.add_door(1, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_r, 1)
        self.board.add_door(4, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_y, 1)
        self.board.add_door(7, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_b, 1)
        self.board.add_door(10, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_k, 1)
        self.board.add_door(13, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_e3, 1)

        # adding colour strips
        self.board.add_door(1, data[1] - 1, 2, 1, classes.board.Door, "", self.col_r, "", 0, door_alpha=False)
        self.board.add_door(4, data[1] - 1, 2, 1, classes.board.Door, "", self.col_y, "", 0, door_alpha=False)
        self.board.add_door(7, data[1] - 1, 2, 1, classes.board.Door, "", self.col_b, "", 0, door_alpha=False)
        self.board.add_door(10, data[1] - 1, 2, 1, classes.board.Door, "", self.col_k, "", 0, door_alpha=False)
        self.board.add_door(13, data[1] - 1, 2, 1, classes.board.Door, "", self.col_e2, "", 0, door_alpha=False)

        # white background
        self.board.add_door(1, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(4, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(7, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(10, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(13, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)

        for i in range(8, 24 - 2):
            if i > 12:
                self.board.units[i].image.set_colorkey(colorkey)
                self.board.all_sprites_list.move_to_back(self.board.units[i])
            else:
                self.board.all_sprites_list.move_to_front(self.board.units[i])

        self.canvas.set_outline([255, 229, 127], 1)
        self.canv = pygame.Surface([self.canvas.grid_w * self.board.scale, self.canvas.grid_h * self.board.scale - 1])
        self.board.all_sprites_list.move_to_back(self.board.board_bg)
        self.mix()

    def mix(self):
        # get the volume
        for i in range(5):
            self.rybke_g[i] = self.board.ships[i].grid_y
            self.rybke[i] = ((self.data[1] - 3) - self.rybke_g[i]) * 5
        # calculate the RYB ratio
        ratio = [0, 0, 0]
        total = self.rybke[0] + self.rybke[1] + self.rybke[2]
        total_bw = self.rybke[3] + self.rybke[4]
        mixed_total = total + total_bw
        if total == 0:
            if total_bw > 0:
                white_ratio = ((self.rybke[4] * 100 // total_bw) * 255) // 100
                e = [white_ratio, white_ratio, white_ratio]
                rgb = e
            else:
                rgb = (0, 0, 0)

        elif total > 0:

            m = max(self.rybke[0:3])
            for i in range(3):
                ratio[i] = self.rybke[i] / (m * 1.0)

            rgb = ryb_to_rgb(ratio[0], ratio[1], ratio[2])
            # ryb color converted - now time to add some black and/or white paint
            # add black
            if self.rybke[3] > 0 or self.rybke[4] > 0:
                hsl = ex.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
                x = 0
                if self.rybke[3] > 0:
                    k = self.rybke[3] * 100 // mixed_total  # (total+self.rybke[3])
                    xk = k * hsl[2] // 100
                    x -= xk
                if self.rybke[4] > 0:
                    e = self.rybke[4] * 100 // mixed_total  # (total+self.rybke[4])
                    xe = e * (255 - hsl[2]) // 100
                    x += xe

                desaturator = total_bw - (max(self.rybke[3:5]) - min(self.rybke[3:5]))
                d = desaturator * 100 // mixed_total  # %
                xd = d * hsl[1] // 100

                rgb = ex.hsl_to_rgb(hsl[0], hsl[1] - xd, hsl[2] + x)

        self.canv.fill(self.col_e)
        # draw container
        x = self.canvas_center[0] - 5 * self.board.scale
        w = 10 * self.board.scale
        y = self.board.scale
        h = (self.canvas.grid_h - 2) * self.board.scale
        container_lines = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
        pygame.draw.lines(self.canv, [0, 0, 0], False, container_lines, 1)

        # fill the container
        h = mixed_total * self.board.scale // 25
        y = (self.canvas.grid_h - 1) * self.board.scale - h

        pygame.draw.rect(self.canv, rgb, [x + 1, y, w - 1, h], 0)
        self.canvas.painting = self.canv.copy()
        self.canvas.update_me = True

        self.update_sliders()

    def update_sliders(self):
        for i in range(5):
            strip = self.board.units[i + 12]
            strip.grid_y = self.rybke_g[i] + 3
            strip.grid_h = self.data[1] - strip.grid_y
            strip.pos_update()
            strip.update_me = True

    def moved(self):
        self.mix()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
