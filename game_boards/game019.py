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
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 7)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        h = random.randrange(0, 255)
        color3 = ex.hsv_to_rgb(h, 150, 75)

        # data = [0-x_count, 1-y_count, 2-bottom_range1, 3-top_range1, 4-bottom_range2, 5-top_range2, 6-operator, 7-font_size]
        data = [11, 7]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        if self.mainloop.m.game_variant == 2:
            data[6] = "*"
        elif self.mainloop.m.game_variant == 3:
            data[6] = "/"

        # stretch width to fit the screen size
        data[0] = self.get_x_count(data[1], even=False)
        if data[0] < 9:
            data[0] = 9
        self.data = data

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.unit_mouse_over = None
        self.units = []

        self.num_list = []
        self.num_list2 = []
        self.solution = []

        if data[6] == "+":
            while len(self.solution) < 5:
                first_num = random.randint(data[2], data[3])
                second_num = random.randint(data[4], data[5])
                sm = first_num + second_num
                if sm not in self.solution:
                    self.num_list.append(first_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)
        elif data[6] == "-":
            while len(self.solution) < 5:
                first_num = random.randint(data[2], data[3])
                if self.mainloop.m.game_var2 == 0:
                    second_num = random.randint(data[4], first_num - 1)
                else:
                    second_num = random.randint(data[4], data[5])
                sm = first_num - second_num
                if sm not in self.solution:
                    self.num_list.append(first_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)
        elif data[6] == "*":
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)

            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(self.solution) < 5:
                if data[3] == 0:
                    first_num = int(l1[random.randint(0, l1l-1)])
                else:
                    first_num = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l-1)])
                else:
                    second_num = random.randint(data[4], data[5])
                sm = first_num * second_num
                if sm not in self.solution:
                    self.num_list.append(first_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)

        elif data[6] == "/":
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)
            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(self.solution) < 5:
                if data[3] == 0:
                    first = int(l1[random.randint(0, l1l - 1)])
                else:
                    first = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l - 1)])
                else:
                    second_num = random.randint(data[4], data[5])
                sm = first
                if first * second_num not in self.num_list:
                    self.num_list.append(first * second_num)
                    self.num_list2.append(second_num)
                    self.solution.append(sm)

        self.shuffled = self.num_list2[:]
        random.shuffle(self.shuffled)

        # create objects
        if data[6] == "*":
            operator = chr(215)
        elif data[6] == "/":
            operator = chr(247)
        else:
            operator = data[6]

        x = (data[0] - 5) // 2
        y = 1
        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")

        door_bg_tint = ex.hsv_to_rgb(h, self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
        if self.mainloop.scheme is None:
            door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        else:
            door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")
            if self.mainloop.scheme.dark:
                door_bg_img_src = os.path.join('unit_bg', "universal_sq_door_no_trans.png")

        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        for i in range(5):
            self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=str(self.num_list[i]),
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[7], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=1)

            self.board.add_universal_unit(grid_x=x + 1, grid_y=y, grid_w=1, grid_h=1, txt=operator,
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[7], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=1)

            self.board.add_universal_unit(grid_x=x + 2, grid_y=y, grid_w=1, grid_h=1, txt="",
                                          fg_img_src=None, bg_img_src=door_bg_img_src, dc_img_src=None,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                          bg_tint_color=door_bg_tint, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[7], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=2)

            self.board.add_universal_unit(grid_x=x + 3, grid_y=y, grid_w=1, grid_h=1, txt="=",
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[7], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=1)
            self.board.add_universal_unit(grid_x=x + 4, grid_y=y, grid_w=1, grid_h=1, txt=str(self.solution[i]),
                                          fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=None,
                                          txt_align=(0, 0), font_type=data[7], multi_color=False, alpha=True,
                                          immobilized=True, fg_as_hover=False, mode=1)

            self.board.add_universal_unit(grid_x=x + 6, grid_y=y, grid_w=1, grid_h=1, txt=str(self.shuffled[i]),
                                          fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                          bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                          bg_tint_color=number_color, fg_tint_color=fg_number_color,
                                          txt_align=(0, 0), font_type=data[7], multi_color=False, alpha=True,
                                          immobilized=False, fg_as_hover=True, mode=0)
            self.board.ships[-1].audible = False
            self.board.ships[-1].readable = False
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()
            self.units.append(self.board.ships[-1])
            y += 1
        for i in range(2, 25, 5):
            self.board.all_sprites_list.move_to_front(self.board.units[i])
        for each in self.board.units:
            each.font_color = color3
        for each in self.board.ships:
            each.font_color = color3

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.auto_check()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def auto_check_reset(self):
        for each in self.board.ships:
            each.set_display_check(None)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def auto_check(self):
        count = 0
        for i in range(5):
            if self.board.ships[i].grid_x == self.board.units[-3].grid_x and 0 < self.board.ships[i].grid_y < 6:
                count += 1
        if count == 5:
            self.check_result()
        else:
            self.auto_check_reset()

    def check_result(self):
        correct = True
        for i in range(5):
            if self.board.ships[i].grid_x == self.board.units[-3].grid_x and 0 < self.board.ships[i].grid_y < 6:
                # if position from the left is in line with target squares
                if self.board.ships[i].value != str(self.num_list2[self.board.ships[i].grid_y - 1]):
                    correct = False
                    self.board.ships[i].set_display_check(False)
                else:
                    self.board.ships[i].set_display_check(True)
            else:
                correct = False
                self.board.ships[i].set_display_check(None)
        if correct:
            tts = self.d["Perfect! Task solved!"]
            self.level.next_board(tts)

        self.mainloop.redraw_needed[0] = True
