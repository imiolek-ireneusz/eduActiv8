# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 999, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.allow_teleport = False
        self.board.decolorable = False
        self.board.draw_grid = False

        color = ex.hsv_to_rgb(225, 15, 235)
        color2 = (255, 255, 255)
        self.col_c = (0, 255, 255)
        self.col_m = (255, 0, 255)
        self.col_y = (255, 255, 0)
        self.col_k = (0, 0, 0)
        self.col_e = (255, 255, 255)
        colorkey = (2, 2, 2, 0)
        self.col_bg = (0, 0, 0, 0)
        data = [32, 23]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count > 32:
            data[0] = x_count

        self.data = data
        self.vis_buttons = [1, 0, 0, 0, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.initcolor = self.col_e
        self.board.board_bg.color = self.col_e
        self.board.board_bg.update_me = True

        self.guides = []

        self.board.moved = self.moved
        step = 255 / 20.0

        self.picked_steps = []
        self.picked = []

        for i in range(3):
            self.picked_steps.append(random.randrange(0, 21))

        self.cmy = [int(self.picked_steps[i] * step) for i in range(3)]
        self.picked_rgb = [255 - self.cmy[i] for i in range(3)]
        y = data[1] - 3

        self.rgb_g = [y, y, y]
        self.rgbx3 = [self.col_e, self.col_e, self.col_e]

        self.board.add_unit(1, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "brush_c.png", alpha=True)
        self.board.add_unit(4, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "brush_m.png", alpha=True)
        self.board.add_unit(7, y, 2, 3, classes.board.ImgShip, "", self.col_bg, "brush_y.png", alpha=True)

        for each in self.board.ships:
            each.outline = False
            each.audible = False

        # add colour container
        self.board.add_unit(10, 0, data[0] - 10, data[1], classes.board.Label, "", self.col_e, "", 0)

        self.canvas = self.board.units[0]
        self.canvas_center = [(self.canvas.grid_w * self.board.scale) // 2,
                              (self.canvas.grid_h * self.board.scale) // 2]

        # adding borders between the colour tubes
        self.board.add_unit(0, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(3, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(6, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)
        self.board.add_unit(9, 0, 1, data[1], classes.board.Label, "", self.col_e, "", 0)

        # adding colour guides
        self.board.add_door(1, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_c, 1)
        self.board.add_door(4, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_m, 1)
        self.board.add_door(7, 0, 2, data[1], classes.board.Door, "", color, "", 0)
        self.board.units[-1].set_outline(self.col_y, 1)

        # adding colour strips
        self.board.add_door(1, data[1] - 1, 2, 1, classes.board.Door, "", self.col_c, "", 0, door_alpha=False)
        self.board.add_door(4, data[1] - 1, 2, 1, classes.board.Door, "", self.col_m, "", 0, door_alpha=False)
        self.board.add_door(7, data[1] - 1, 2, 1, classes.board.Door, "", self.col_y, "", 0, door_alpha=False)

        # white background
        self.board.add_door(1, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(4, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)
        self.board.add_door(7, 0, 2, data[1], classes.board.Door, "", self.col_e, "", 0, door_alpha=False)
        self.board.units[-1].image.set_colorkey(None)

        # guides
        self.board.add_door(1, data[1] - 2, 2, 2, classes.board.Label, "", colorkey, "", 21, alpha=True)
        self.guides.append(self.board.units[-1])
        self.board.add_door(4, data[1] - 2, 2, 2, classes.board.Label, "", colorkey, "", 21, alpha=True)
        self.guides.append(self.board.units[-1])
        self.board.add_door(7, data[1] - 2, 2, 2, classes.board.Label, "", colorkey, "", 21, alpha=True)
        self.guides.append(self.board.units[-1])

        for each in self.guides:
            each.font_color = self.col_k
            each.checkable = True
            each.init_check_images(1, 1.2)
            each.decolorable = False

        for i in [5, 6, 7, 8, 9, 10, 11, 12, 13]:
            if i > 7:
                self.board.units[i].image.set_colorkey(colorkey)
                self.board.all_sprites_list.move_to_back(self.board.units[i])
            else:
                self.board.all_sprites_list.move_to_front(self.board.units[i])

        self.board.all_sprites_list.move_to_back(self.board.board_bg)
        self.canvas.set_outline([255, 229, 127], 1)
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
        self.canv[3].fill(self.col_e)
        ct = self.canvas_center
        radius = 9 * self.board.scale
        radius2 = 5 * self.board.scale
        x = 1 * self.board.scale
        rect = [[ct[0], ct[1] - x], [ct[0] - x, ct[1] + x], [ct[0] + x, ct[1] + x]]
        for i in range(3):
            pygame.draw.circle(self.canv[i], self.rgbx3[i], rect[i], radius, 0)
            self.canv[3].blit(self.canv[i], [0, 0], special_flags=pygame.BLEND_SUB)
        pygame.draw.circle(self.canv[3], self.cmy, ct, radius2, 0)

        self.canvas.painting = self.canv[3].copy()
        self.canvas.update_me = True

    def update_sliders(self):
        for i in range(3):
            strip = self.board.units[i + 8]
            strip.grid_y = self.rgb_g[i] + 3
            strip.grid_h = self.data[1] - strip.grid_y
            col = []
            step = 255 / 20.0
            for each in strip.initcolor:
                if each == 0:
                    if strip.grid_y == 23:
                        col.append(255)
                    elif strip.grid_y == 3:
                        col.append(0)
                    else:
                        col.append(int((strip.grid_y - 3) * step))
                else:
                    col.append(255)

            col2 = [255 - col[0], 255 - col[1], 255 - col[2]]
            self.rgbx3[i] = col2
            strip.color = col
            strip.pos_update()
            strip.update_me = True

    def moved(self):
        self.mix()

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check_reset(self):
        for each in self.guides:
            each.set_display_check(None)

    def check_result(self):
        if self.picked_steps != self.rgb_g:
            help = ""
            if self.picked_steps[0] < self.rgb_g[0]:
                self.guides[0].value = "⇑"
                help += self.dp['more cyan'] + ", "
            elif self.picked_steps[0] > self.rgb_g[0]:
                self.guides[0].value = "⇓"
                help += self.dp['less cyan'] + ", "
            else:
                self.guides[0].value = " "
                help += self.dp['cyan is ok'] + ", "
                self.guides[0].set_display_check(True)

            if self.picked_steps[1] < self.rgb_g[1]:
                self.guides[1].value = "⇑"
                help += self.dp['more magenta'] + ", "
            elif self.picked_steps[1] > self.rgb_g[1]:
                self.guides[1].value = "⇓"
                help += self.dp['less magenta'] + ", "
            else:
                self.guides[1].value = " "
                help += self.dp['magenta is ok'] + ", "
                self.guides[1].set_display_check(True)

            if self.picked_steps[2] < self.rgb_g[2]:
                self.guides[2].value = "⇑"
                help += self.dp['more yellow'] + ". "
            elif self.picked_steps[2] > self.rgb_g[2]:
                self.guides[2].value = "⇓"
                help += self.dp['less yellow'] + ". "
            else:
                self.guides[2].value = " "
                help += self.dp['yellow is ok'] + ". "
                self.guides[2].set_display_check(True)
            #self.say(help)

            self.level.try_again(silent=self.mainloop.speaker.talkative)

            for each in self.guides:
                each.update_me = True
        else:
            for each in self.guides:
                each.set_display_check(True)
                each.value = ""
            self.level.next_board()
        self.mainloop.redraw_needed[0] = True


