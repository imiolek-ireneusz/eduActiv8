# -*- coding: utf-8 -*-

import pygame
import random
import os

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.img
import classes.word_lists as wl


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 5, 3)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
        self.font_color = self.color2

        self.disp_counter = 0
        self.disp_len = 1

        # Maximum words per screen 19 (nature)

        category, self.imgs = wl.word_lists_filtered.get(self.mainloop.m.game_variant, ("default", []))
        self.captions = self.d[f"a4a_{category}"]

        #self.captions = self.d["a4a_%s" % category]
        if self.mainloop.lang.lang == "ru":
            self.captionsp = self.dp.get(f"a4a_{category}", []) #eval("self.dp['a4a_%s']" % category)

        if self.level.lvl > self.level.lvl_count:
            self.level.lvl = self.level.lvl_count
        if self.level.lvl == 1:
            data = [10, 3, 3, 2, 3]
        elif self.level.lvl == 2:
            data = [10, 4, 3, 2, 4]
        elif self.level.lvl == 3:
            data = [10, 5, 3, 2, 5]

        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            x = self.get_x_count(data[1], even=True)
        else:
            x = self.get_x_count(data[1], even=False)

        if x > data[0]:
            data[0] = x

        self.data = data

        self.found = 0
        self.clicks = 0

        self.squares = self.data[3] * self.data[4]

        self.square_count = self.squares * 2
        self.history = [None, None]

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        l = len(self.imgs)
        drawn_numbers = []
        while len(drawn_numbers) < data[1] * 2:
            r = random.randint(0, l-1)
            if r not in drawn_numbers:
                if self.imgs[r] != '' and self.captions[r][0] != "<":
                    drawn_numbers.append(r)

        self.completed_mode = False

        choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        self.units = []
        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
            self.default_bg_color = ex.hsv_to_rgb(h, 200, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 230, 90)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 150, 200), ]

            self.selected_color = ex.hsv_to_rgb(h, 150, 50)
            self.selected_font_color = [ex.hsv_to_rgb(h, 150, 100), ]
        else:
            self.default_bg_color = ex.hsv_to_rgb(h, 150, self.mainloop.cl.bg_color_v)
            self.hover_bg_color = ex.hsv_to_rgb(h, 255, self.mainloop.cl.fg_hover_v)
            self.font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

            self.semi_selected_color = ex.hsv_to_rgb(h, 80, self.mainloop.cl.bg_color_v)
            self.semi_selected_font_color = [ex.hsv_to_rgb(h, 200, self.mainloop.cl.font_color_v), ]

            self.selected_color = ex.hsv_to_rgb(h, 50, self.mainloop.cl.bg_color_v)
            self.selected_font_color = [ex.hsv_to_rgb(h, 50, 250), ]

        self.bg_img_src = os.path.join('unit_bg', "universal_sq_bg_liter.png")
        self.door_bg_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        self.bg_img_src_w = os.path.join('unit_bg', "universal_r4x1_bg.png")
        self.door_bg_img_src_w = os.path.join('unit_bg', "universal_r4x1_door.png")
        dc_tint_color = ex.hsv_to_rgb(h, self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
            # img_style = "bb"
            bg_door_img_src = os.path.join('unit_bg', "img_decor_bb.png")
            dc_tint_color = None

            self.dc_selected_img_src = bg_door_img_src # os.path.join('unit_bg', "dc_hover_%s20.png" % img_style)
        else:
            img_style = "wb"
            bg_door_img_src = os.path.join('unit_bg', "img_decor_w.png")

            self.dc_selected_img_src = os.path.join('unit_bg', "dc_hover_%s20.png" % img_style)


        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4]  # -1 #height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3] * 4) // 2 - 1  # side margin width

        small_slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2, w2 + data[3]):
                small_slots.append([i, j])
        random.shuffle(small_slots)

        wide_slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2 + data[3], data[0] - w2, 4):
                wide_slots.append([i, j])
        random.shuffle(wide_slots)
        switch = self.square_count // 2
        if self.lang.lang == 'ar':
            font_size = 2
        else:
            font_size = 8
        for i in range(self.square_count):
            if i < switch:
                img = "%s.webp" % self.imgs[drawn_numbers[i]]
                img_src = os.path.join("res", "images", 'art4apps', category, img)
                position_list = small_slots
                pos = i
                xw = 1
                self.board.add_universal_unit(grid_x=position_list[pos][0], grid_y=position_list[pos][1], grid_w=xw,
                                              grid_h=1, txt="", fg_img_src=self.bg_img_src,
                                              bg_img_src=self.bg_img_src, dc_img_src=bg_door_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=self.font_color,
                                              bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color,
                                              dc_tint_color=dc_tint_color, txt_align=(0, 0),
                                              font_type=font_size, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)

                im = classes.drw.img.Img(xw, 1, self.board.scale, img_src, scale_factor=0.9, bg_color=(255, 255, 255))

                self.board.ships[-1].add_image(0, im)
            else:
                caption = self.captions[drawn_numbers[i - switch]]
                position_list = wide_slots
                pos = i - switch
                xw = 4
                self.board.add_universal_unit(grid_x=position_list[pos][0], grid_y=position_list[pos][1], grid_w=xw,
                                              grid_h=1, txt=caption, fg_img_src=self.bg_img_src_w,
                                              bg_img_src=self.bg_img_src_w, dc_img_src=self.door_bg_img_src_w,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=self.font_color,
                                              bg_tint_color=self.default_bg_color,
                                              fg_tint_color=self.hover_bg_color,
                                              dc_tint_color=self.default_bg_color, txt_align=(0, 0),
                                              font_type=font_size, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=True)

            self.units.append(self.board.ships[-1])

            self.board.ships[i].readable = False
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
        o.bg_tint_color = self.semi_selected_color
        o.mouse_out()
        o.update_me = True

    def select(self):
        for each in self.history:
            each.dc_tint_color = self.selected_color

            if each.grid_w == 1:
                if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
                    each.dc_tint_color = None
                each.set_dc_img(self.dc_selected_img_src)
            else:
                each.bg_tint_color = self.selected_color
            each.uncovered = True
            each.set_display_check(True)
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]

    def deselect(self):
        for each in self.history:
            each.bg_tint_color = self.default_bg_color
            each.mouse_out()
            each.update_me = True
        self.history = [None, None]
        self.ai_enabled = False
        self.disp_counter = 0

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

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
