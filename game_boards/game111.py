# -*- coding: utf-8 -*-

import random
import pygame
import os

import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 6)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        h = random.randrange(0, 255, 5)

        # data = [x_count, y_count, number_count, bottom_limit, top_limit, ordered, font_size]
        data = [11, 4]
        data.extend(self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group, self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        self.data = data

        self.board.set_animation_constraints(0, data[0], 0, data[1])
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        self.num_list = []

        if data[5]:
            index = random.randrange(data[3], data[4]-data[2]+2)
            n = 0
            for i in range(data[2]):
                self.num_list.append(index + n)
                n += 1
        else:
            while len(self.num_list) < data[2]:
                num = random.randint(data[3], data[4])
                if num not in self.num_list:
                    self.num_list.append(num)
        shuffled = self.num_list[:]
        self.ordered = sorted(self.num_list[:])
        random.shuffle(shuffled)

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]

        # find position of first door square
        self.left_offset = (data[0] - data[2]) // 2

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        door_bg_tint = ex.hsv_to_rgb(h, self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        # add objects to the board
        for i in range(data[2]):
            # empty slot
            self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=0, grid_w=1, grid_h=1, txt=None,
                                          fg_img_src=None,
                                          bg_img_src=bg_door_img_src,
                                          dc_img_src=None,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=None,
                                          bg_tint_color=door_bg_tint,
                                          fg_tint_color=None,
                                          txt_align=(0, 0), font_type=10, multi_color=False, alpha=True,
                                          immobilized=True, mode=2)

            # number object
            y = random.randrange(1, 3)
            caption = str(shuffled[i])
            self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=bg_img_src,
                                          bg_img_src=bg_img_src,
                                          dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=font_color,
                                          bg_tint_color=number_color,
                                          fg_tint_color=fg_number_color,
                                          txt_align=(0, 0), font_type=data[6], multi_color=False, alpha=True,
                                          immobilized=False, fg_as_hover=True)
            self.units.append(self.board.ships[-1])

            self.solution_grid[self.left_offset + i] = 1
            self.board.ships[-1].readable = False

            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Re-arrange ascending"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.check_result()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def auto_check_reset(self):
        for each in self.board.ships:
            each.update_me = True
            each.set_display_check(None)

    def auto_check(self):
        if self.board.grid[0] == self.solution_grid:
            for i in range(self.data[2]):
                if self.ordered[self.board.ships[i].grid_x - self.left_offset] == int(self.board.ships[i].value):
                    self.board.ships[i].set_display_check(True)
                else:
                    self.board.ships[i].set_display_check(False)

    def check_result(self):
        if self.board.grid[0] == self.solution_grid:
            correct = True
            for i in range(self.data[2]):
                if self.ordered[self.board.ships[i].grid_x - self.left_offset] != int(self.board.ships[i].value):
                    correct = False
                    break

            if correct:
                self.auto_check()
                self.level.next_board()
            else:
                self.auto_check()
        self.mainloop.redraw_needed[0] = True
