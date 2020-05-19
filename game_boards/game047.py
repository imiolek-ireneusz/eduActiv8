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

        data = [11, 3]
        data.extend(self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group, self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group)

        self.data = data
        self.board.set_animation_constraints(0, data[0], 0, data[1])
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        if self.mainloop.m.game_variant == 0:
            if self.lang.ltr_text:
                self.alphabet = self.lang.alphabet_lc
            else:
                ts = "".join(self.lang.alphabet_lc)
                ts = ex.unival(ts)
                self.alphabet = ts[::-1]
        elif self.mainloop.m.game_variant == 1:
            self.alphabet = self.lang.alphabet_uc

        self.alph_len = len(self.alphabet)

        self.num_list = []
        self.indexes = []
        self.choice_indexes = [x for x in range(self.alph_len)]

        self.positionsd = {}

        if data[3]:
            choice_list = [x for x in range(self.alph_len - data[2])]
            index = random.randrange(0, len(choice_list))
            for i in range(data[2]):
                self.num_list.append(choice_list[index] + i)
                self.indexes.append(index + i)
                self.positionsd[index + i] = i
        else:
            choice_list = [x for x in range(self.alph_len)]
            for i in range(data[2]):
                index = random.randrange(0, len(choice_list))
                self.num_list.append(choice_list[index])
                self.indexes.append(choice_list[index])
                del (choice_list[index])

        self.indexes.sort()

        shuffled = self.num_list[:]
        random.shuffle(shuffled)

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]

        # find position of first door square
        x = (data[0] - data[2]) // 2

        self.positions = []
        for i in range(data[2]):
            self.positionsd[self.indexes[i]] = i
            self.positions.append([x + i, 0])

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")

        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
            bg_door_img_src = os.path.join('unit_bg', "universal_sq_door_no_trans.png")
        else:
            bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        # add objects to the board
        for i in range(data[2]):
            # add new door
            self.board.add_universal_unit(grid_x=x+i, grid_y=0, grid_w=1, grid_h=1, txt=None,
                                          fg_img_src=None,
                                          bg_img_src=bg_door_img_src,
                                          dc_img_src=None,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=None,
                                          bg_tint_color=number_color,
                                          fg_tint_color=None,
                                          txt_align=(0, 0), font_type=10, multi_color=False, alpha=True,
                                          immobilized=True, mode=2)
            y = random.randrange(1, data[1])
            caption = self.alphabet[shuffled[i]]
            self.board.add_universal_unit(grid_x=x+i, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                          fg_img_src=bg_img_src,
                                          bg_img_src=bg_img_src,
                                          dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0),
                                          border_color=None, font_color=font_color,
                                          bg_tint_color=number_color,
                                          fg_tint_color=fg_number_color,
                                          txt_align=(0, 0), font_type=data[4], multi_color=False, alpha=True,
                                          immobilized=False, fg_as_hover=True)
            self.units.append(self.board.ships[-1])
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            self.board.ships[i].home_location = [x + self.positionsd[shuffled[i]], 0]
            self.solution_grid[x + i] = 1

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)

        self.outline_all(0, 1)

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Re-arrange alphabetical"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
                self.auto_check()
            self.check_result()

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def auto_check(self):
        for each in self.board.ships:
            each.update_me = True
            if each.checkable and (each.grid_y == 0):
                if each.home_location[0] == each.grid_x and each.home_location[1] == each.grid_y:
                    each.set_display_check(True)
                else:
                    each.set_display_check(False)
            else:
                each.set_display_check(None)

    def auto_check_reset(self):
        for each in self.board.ships:
            each.update_me = True
            each.set_display_check(None)

    def update(self, game):
        game.fill((0, 0, 0))
        gd.BoardGame.update(self, game)

    def check_result(self):
        if self.board.grid[0] == self.solution_grid:
            ships = []

            # collect value and x position on the grid from ships list
            for i in range(self.data[2]):
                ships.append([self.board.ships[i].grid_x, self.board.ships[i].value])
            ships_sorted = sorted(ships)
            correct = True
            for i in range(self.data[2]):
                if i < self.data[2] - 1:
                    if ships_sorted[i][1] != ex.unival(self.alphabet[self.indexes[i]]):
                        correct = False
            if correct:
                self.auto_check()
                self.level.next_board()
            else:
                self.auto_check()
        else:
            self.auto_check_reset()
