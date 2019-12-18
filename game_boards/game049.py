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
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 26, 9)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        if not self.lang.has_uc:
            self.level.lvl_count = 8

        if self.level.lvl > self.level.lvl_count:
            self.level.lvl = self.level.lvl_count
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        v = 255
        h = random.randrange(0, 255)
        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1

        lvl_data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid,
                                                         self.mainloop.config.user_age_group,
                                                         self.level.lvl)

        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        self.alphabet_lc = self.lang.alphabet_lc
        self.alphabet_uc = self.lang.alphabet_uc
        self.alphabet_len = len(self.alphabet_lc)

        if self.alphabet_len % 2 == 0:
            self.alphabet_width = self.alphabet_len // 2
            self.last_block = False
        else:
            self.alphabet_width = self.alphabet_len // 2 + 1
            self.last_block = True

        # number of letters to find
        self.font_size = 0
        if self.mainloop.lang.lang == "lkt":
            self.font_size = 1

        if self.mainloop.m.game_variant == 0:
            data = [self.alphabet_width, 5, self.alphabet_lc]
        else:
            data = [self.alphabet_width, 5, self.alphabet_uc]
        data.extend(lvl_data)
        nlf = min(int(self.alphabet_len * data[4] / 100), self.alphabet_len)

        self.data = data
        self.board.set_animation_constraints(0, data[0], 0, data[1])

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        self.word = self.data[2][:]
        word_len = self.alphabet_len
        if not self.lang.ltr_text:
            sx = "".join(self.word)
            sx = ex.unival(sx)
            self.word = sx[data[0] - 1:0:-1] + sx[0]
            self.word += sx[word_len:data[0] - 1:-1]
        chosen_indexes = []
        index_list_org = [x for x in range(self.alphabet_len)]
        index_list = [x for x in range(self.alphabet_len)]

        lowered = []
        for i in range(nlf):  # picking letters to lower
            index = random.randrange(0, len(index_list))
            chosen_indexes.append(index_list[index])
            lowered.append(index_list[index])
            del (index_list[index])
        random.shuffle(lowered)

        # create table to store 'binary' solution
        self.solution_grid = [1 for x in range(data[0])]

        x = 0
        y = 0

        if nlf < data[0]:
            x2 = (data[0] - len(lowered)) // 2
            x3 = 0
        else:
            x2 = 0
            x3 = (data[0] - (len(lowered) - data[0])) // 2

        y2 = 2
        j = 0
        h_step = 255 // self.alphabet_len
        s = 128

        self.positions = []
        for i in range(self.alphabet_len):
            self.positions.append((x, y))
            x += 1
            if x >= data[0]:
                if not self.last_block:
                    x = 0
                else:
                    if self.lang.ltr_text:
                        x = 0
                    else:
                        x = 1
                y = data[1] - 1
        x = 0
        y = 0

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        for i in range(self.alphabet_len):
            picked = False
            if i in lowered:
                picked = True
            if data[3] == 1:
                door_color = ex.hsv_to_rgb(h, s, v)
            else:
                if self.lang.ltr_text:
                    door_color = ex.hsv_to_rgb(h_step * i, s, v)
                else:
                    door_color = ex.hsv_to_rgb(h_step * (self.alphabet_len - i), s, v)
                if self.lang.ltr_text:
                    if picked:
                        h = round(h_step * lowered[j])
                    else:
                        h = round(h_step * index_list_org[i])
                else:
                    if picked:
                        h = round(h_step * (self.alphabet_len - lowered[j]))
                    else:
                        h = round(h_step * (self.alphabet_len - index_list_org[i]))

            number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
            font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
            fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

            if picked:
                if j < data[0]:
                    xj = x2 + j
                else:
                    xj = x3 + j - data[0]
                    y2 = 3
                caption = self.word[lowered[j]]
                self.board.add_universal_unit(grid_x=xj, grid_y=y2, grid_w=1, grid_h=1, txt=caption,
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                              bg_tint_color=number_color, fg_tint_color=fg_number_color,
                                              txt_align=(0, 0), font_type=self.font_size, multi_color=False, alpha=True,
                                              immobilized=False, fg_as_hover=True)
                self.units.append(self.board.ships[-1])
                # add new door
                self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=None,
                                              fg_img_src=None,  bg_img_src=bg_door_img_src, dc_img_src=None,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                              bg_tint_color=door_color, fg_tint_color=None, txt_align=(0, 0),
                                              font_type=10, multi_color=False, alpha=True, immobilized=True, mode=2)
                self.board.ships[i].idx = i
                self.board.ships[i].checkable = True
                self.board.ships[i].init_check_images()
                self.board.ships[i].home_location = self.positions[lowered[j]]
                j += 1
            else:
                caption = self.word[i]
                self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                              fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                              bg_tint_color=number_color, fg_tint_color=None, txt_align=(0, 0),
                                              font_type=self.font_size, multi_color=False, alpha=True, immobilized=True)
                self.board.ships[i].idx = i

            x += 1
            if x >= data[0]:
                if not self.last_block:
                    x = 0
                else:
                    if self.lang.ltr_text:
                        x = 0
                    else:
                        x = 1
                y = data[1] - 1

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)

        if self.last_block:
            # if odd number of letters - add an empty square at the end
            if self.lang.ltr_text:
                x = data[0] - 1
            else:
                x = 0
            self.board.add_unit(x, data[1] - 1, 1, 1, classes.board.Label, "", color0, "", 0)

        self.outline_all(0, 1)

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Complete abc"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            if self.data[5] == 1:
                self.auto_check()
            self.check_result()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def auto_check(self):
        for each in self.board.ships:
            each.update_me = True
            if each.checkable and (each.grid_y == 0 or each.grid_y == self.data[1] - 1):
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
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        result = [" " for i in range(self.alphabet_len)]
        if self.board.grid[0] == self.board.grid[self.data[1] - 1] == self.solution_grid:
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 0:
                    result[self.board.ships[i].grid_x] = self.board.ships[i].value
                elif self.board.ships[i].grid_y == self.data[1] - 1:
                    if self.last_block and not self.lang.ltr_text:
                        result[self.data[0] + self.board.ships[i].grid_x - 1] = self.board.ships[i].value
                    else:
                        result[self.data[0] + self.board.ships[i].grid_x] = self.board.ships[i].value
            if ex.unival("".join(self.word)) == ex.unival("".join(result)):
                self.auto_check()
                self.level.next_board()
            else:
                self.auto_check()
        elif self.data[5] == 0:
            self.auto_check_reset()
