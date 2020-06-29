# -*- coding: utf-8 -*-

import random
import pygame
import os

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 14, 5)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.board.decolorable = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 1, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        h1 = random.randrange(0, 180, 5)
        h2 = random.randrange(h1+30, 255, 5)

        white = [255, 255, 255]
        data = [14, 6]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid, 
                                                            self.mainloop.config.user_age_group)

        self.points = data[2] // 5
        self.data = data

        self.board.set_animation_constraints(4, data[0], 0, data[1])
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        self.num_list = []

        while len(self.num_list) < data[2]:
            num = random.randint(data[3], data[4])
            if num not in self.num_list:
                self.num_list.append(num)

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")

        # find position of first door square
        x = data[0] - 1
        y = data[1] - 1
        # add objects to the board
        bg_colors = [i * (255//data[2]) + random.randint(0, data[2]) for i in range(data[2])]
        random.shuffle(bg_colors)
        for i in range(data[2]):
            if self.level.lvl == 1:
                if self.num_list[i] % 2 == 0:
                    h = h1
                else:
                    h = h2
            else:
                h = bg_colors[i]

            number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
            font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
            fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

            caption = str(self.num_list[i])

            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=bg_img_src,
                                          bg_img_src=bg_img_src,
                                          dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=font_color,
                                          bg_tint_color=number_color,
                                          fg_tint_color=fg_number_color,
                                          txt_align=(0, 0), font_type=data[5], multi_color=False, alpha=True,
                                          immobilized=False, fg_as_hover=True)
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()
            self.board.ships[-1].readable = False

            self.units.append(self.board.ships[-1])

            x -= 1
            if x <= 3:
                x = data[0] - 1
                y -= 1

        if self.level.lvl > 1:
            h2 = h1
        color1 = ex.hsv_to_rgb(h1, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        color2 = ex.hsv_to_rgb(h2, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color1 = ex.hsv_to_rgb(h1, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v)
        font_color2 = ex.hsv_to_rgb(h2, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v)
        self.board.add_unit(0, 0, 4, 2, classes.board.Letter, self.d["Even"], color1, "", 1)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color1
        self.board.add_unit(0, 2, 4, 2, classes.board.Letter, self.d["Odd"], color2, "", 1)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color2
        self.board.add_door(4, 0, data[0] - 4, 2, classes.board.Door, "", white, "")
        self.board.units[-1].door_outline = True

        self.board.add_door(4, 2, data[0] - 4, 2, classes.board.Door, "", white, "")
        self.board.units[-1].door_outline = True

        self.outline_all(0, 1)
        self.board.all_sprites_list.move_to_front(self.board.units[-1])

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Find and separate"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def auto_check_reset(self):
        for i in range(len(self.board.ships) - 2):
            self.board.ships[i].set_display_check(None)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        correct = True
        for i in range(len(self.board.ships) - 2):
            if self.board.ships[i].grid_y < 2 and self.num_list[self.board.ships[i].unit_id] % 2 == 0:
                self.board.ships[i].set_display_check(True)
            elif 1 < self.board.ships[i].grid_y < 4 and self.num_list[self.board.ships[i].unit_id] % 2 != 0:
                self.board.ships[i].set_display_check(True)
            else:
                self.board.ships[i].set_display_check(False)
                correct = False
        if correct:
            self.level.next_board()

        self.mainloop.redraw_needed[0] = True

