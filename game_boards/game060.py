# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders

        self.disp_counter = 0
        self.disp_len = 1

        texts1 = []
        texts2 = []
        data = [4, 2]
        data.extend(self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                     self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        if self.mainloop.m.game_variant < 4:
            data[0] = data[9]
            data[1] = data[10]
        else:
            data[0] = data[2]
            data[1] = data[3]
        self.square_count = data[0] * data[1]

        if self.mainloop.m.game_variant == 0:
            while len(texts1) < self.square_count // 2:
                first_num = random.randrange(data[2], data[3] + 1)
                second_num = random.randrange(data[4], data[5] + 1)
                my_sum = str(first_num + second_num)
                if my_sum not in texts1:
                    texts1.append(str(my_sum))
                    if second_num < 0:
                        texts2.append("%d + (%d)" % (first_num, second_num))
                    else:
                        texts2.append("%d + %d" % (first_num, second_num))

        elif self.mainloop.m.game_variant == 1:
            while len(texts1) < self.square_count // 2:
                first_num = random.randrange(data[2], data[3] + 1)
                if first_num - 1 <= data[4] and self.mainloop.m.game_var2 == 0:
                    continue
                else:
                    if self.mainloop.m.game_var2 == 0:
                        second_num = random.randint(data[4], first_num - 1)
                    else:
                        second_num = random.randint(data[4], data[5])
                    my_sum = str(first_num - second_num)
                    if my_sum not in texts1:
                        texts1.append(str(my_sum))
                        if second_num < 0:
                            texts2.append("%d - (%d)" % (first_num, second_num))
                        else:
                            texts2.append("%d - %d" % (first_num, second_num))

        elif self.mainloop.m.game_variant == 2:
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)

            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(texts1) < self.square_count // 2:
                if data[3] == 0:
                    first_num = int(l1[random.randint(0, l1l-1)])
                else:
                    first_num = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l-1)])
                else:
                    second_num = random.randint(data[4], data[5])
                my_sum = str(first_num * second_num)
                if my_sum not in texts1:
                    texts1.append(str(my_sum))
                    if second_num < 0:
                        texts2.append("%d %s (%d)" % (first_num, chr(215), second_num))
                    else:
                        texts2.append("%d %s %d" % (first_num, chr(215), second_num))

        elif self.mainloop.m.game_variant == 3:
            if data[3] == 0:
                l1 = data[2].split(", ")
                l1l = len(l1)

            if data[5] == 0:
                l2 = data[4].split(", ")
                l2l = len(l2)

            while len(texts1) < self.square_count // 2:
                if data[3] == 0:
                    first = int(l1[random.randint(0, l1l - 1)])
                else:
                    first = random.randint(data[2], data[3])
                if data[5] == 0:
                    second_num = int(l2[random.randint(0, l2l - 1)])
                else:
                    second_num = random.randint(data[4], data[5])
                first_num = first * second_num
                my_sum = str(first)
                if my_sum not in texts1:
                    texts1.append(my_sum)
                    if second_num < 0:
                        texts2.append("%d %s (%d)" % (first_num, chr(247), second_num))
                    else:
                        texts2.append("%d %s %d" % (first_num, chr(247), second_num))

        elif self.mainloop.m.game_variant == 4:
            if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
                image_src1 = [os.path.join('memory', "m_img%da.png" % i) for i in range(1, 22)]
            else:
                image_src1 = [os.path.join('schemes', "black", "match_animals", "m_img%da.png" % i) for i in range(1, 22)]
            image_src2 = image_src1

        elif self.mainloop.m.game_variant == 5:
            if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
                image_src1 = [os.path.join('memory', "m_img%da.png" % i) for i in range(1, 22)]
                image_src2 = [os.path.join('memory', "m_img%db.png" % i) for i in range(1, 22)]
            else:
                image_src1 = [os.path.join('schemes', "black", "match_animals", "m_img%da.png" % i) for i in range(1, 22)]
                image_src2 = [os.path.join('schemes', "black", "match_animals", "m_img%db.png" % i) for i in range(1, 22)]

        self.data = data
        self.found = 0
        self.clicks = 0
        self.history = [None, None]
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        self.completed_mode = False

        self.units = []

        if self.mainloop.m.game_variant in [4, 5]:
            choice = [x for x in range(0, 21)]
        else:
            choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        h1 = (data[1] - data[1]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[1]  # -1 #height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[0]) // 2  # side margin width

        slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2, w2 + data[0]):
                slots.append([i, j])
        random.shuffle(slots)

        switch = self.square_count // 2

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
        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        if self.mainloop.m.game_variant == 4:
            self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s150.png" % img_style)
        elif self.mainloop.m.game_variant == 5:
            self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s20.png" % img_style)

        door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        for i in range(self.square_count):
            if self.mainloop.m.game_variant in [4, 5]:
                fg_tint_color = (40, 40, 40)
                if i < switch:
                    src = image_src1[self.chosen[i]]
                else:
                    src = image_src2[self.chosen[i - switch]]
                    if self.mainloop.m.game_variant == 5:
                        fg_tint_color = (20, 20, 20)
                        self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s150.png" % img_style)

                self.board.add_universal_unit(grid_x=slots[i][0], grid_y=slots[i][1], grid_w=1, grid_h=1, txt="",
                                              fg_img_src=src, bg_img_src=src, dc_img_src=self.dc_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                              bg_tint_color=None, dc_tint_color=self.default_bg_color,
                                              fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                              multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                self.board.ships[-1].set_blit_mask(os.path.join('unit_bg', 'img_mask.png'))
                self.units.append(self.board.ships[-1])
            else:
                if i < switch:
                    caption = texts1[self.chosen[i]]
                else:
                    caption = texts2[self.chosen[i - switch]]

                self.board.add_universal_unit(grid_x=slots[i][0], grid_y=slots[i][1], grid_w=1, grid_h=1, txt=caption,
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=door_bg_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=self.font_color,
                                              bg_tint_color=self.default_bg_color, fg_tint_color=self.hover_bg_color,
                                              dc_tint_color=self.default_bg_color, txt_align=(0, 0), font_type=data[8], multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)
                self.units.append(self.board.ships[-1])

            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(self.color2, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[1] is None and self.ai_enabled is False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if not active.uncovered:
                    if self.history[0] is None:
                        self.history[0] = active
                        self.semi_select(active)
                        self.clicks += 1
                        active.uncovered = True
                    elif self.history[1] is None:
                        self.history[1] = active
                        self.semi_select(active)
                        self.clicks += 1
                        if self.chosen[self.history[0].unit_id] != self.chosen[self.history[1].unit_id]:
                            self.ai_enabled = True
                            self.history[0].uncovered = False
                        else:
                            self.select()
                            self.found += 2
                            if self.found == self.square_count:
                                self.completed_mode = True
                                self.ai_enabled = True

                    active.update_me = True

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.custom_hover(event)

    def semi_select(self, o):
        if self.mainloop.m.game_variant == 4:
            o.dc_tint_color = self.semi_selected_color
            o.bg_tint_color = (50, 50, 50)
        elif self.mainloop.m.game_variant == 5:
            o.dc_tint_color = self.semi_selected_color
        else:
            o.bg_tint_color = self.semi_selected_color
            o.font_colors = self.semi_selected_font_color
        o.mouse_out()
        o.update_me = True

    def select(self):
        for each in self.history:
            if self.mainloop.m.game_variant in [4, 5]:
                each.dc_tint_color = self.selected_color
                each.set_dc_img(self.dc_selected_img_src)
            else:
                each.bg_tint_color = self.selected_color
                each.font_colors = self.selected_font_color
            each.uncovered = True
            each.set_display_check(True)
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]

    def deselect(self):
        for each in self.history:
            if self.mainloop.m.game_variant in [4, 5]:
                each.dc_tint_color = self.default_bg_color
                each.bg_tint_color = None
            else:
                each.bg_tint_color = self.default_bg_color
                each.font_colors = self.font_color
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]
        self.ai_enabled = False
        self.disp_counter = 0

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.ai_enabled = False
                self.level.next_board()
            else:
                self.deselect()

    def custom_hover(self, event):
        if not self.drag and not self.ai_enabled:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            found = False
            for each in self.units:
                if each.rect.left < pos[0] < each.rect.right and each.rect.top < pos[1] < each.rect.bottom:
                    if each != self.unit_mouse_over:
                        if self.unit_mouse_over is not None:
                            self.unit_mouse_over.mouse_out()
                        self.unit_mouse_over = each
                    found = True
                    if not each.uncovered:
                        each.handle(event)
                    break
            if not found:
                if self.unit_mouse_over is not None:
                    self.unit_mouse_over.mouse_out()
                self.unit_mouse_over = None

    def check_result(self):
        pass
