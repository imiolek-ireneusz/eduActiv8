# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.splash
import classes.drw.fraction


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 11)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False
        h = random.randrange(0, 255, 5)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.scheme_dir = "black"
                color = (0, 0, 0)
            else:
                self.scheme_dir = "white"
                color = (255, 255, 255)
        else:
            self.scheme_dir = "white"
            color = (255, 255, 255)

        self.color = color

        """lvl_data = [term_len_min, term_len_max, term_count_min, term_count_max, term_completed_count, semi_completed_count, shuffled]"""
        lvl_data = self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                         self.level.lvl)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        self.term_len = random.randint(lvl_data[0], lvl_data[1])
        self.term_count = random.randint(lvl_data[2], lvl_data[3])
        term_completed_count = lvl_data[4]
        if lvl_data[5] > 1:
            term_semi_completed_count = max(2, random.randint(2, lvl_data[5]))
        else:
            term_semi_completed_count = lvl_data[5]

        self.task_len = self.term_len * self.term_count
        self.term = self.generate_term(self.term_len)
        self.task = self.generate_task(self.term, self.term_len, self.term_count, term_completed_count,
                                       term_semi_completed_count, shuffled=lvl_data[6])

        if self.mainloop.m.game_variant < 2:
            # make the backgrounds different for each letter or number
            unit_clrs = []
            unit_clrs_fg = []
            font_clrs = []
            for i in range(self.term_len):
                if self.level.lvl < 3:
                    h = random.randrange(0, 100, 5)
                    gap = i * (155//self.term_len)
                else:
                    gap = 0
                unit_clrs.append(ex.hsv_to_rgb(h + gap, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v))
                unit_clrs_fg.append(ex.hsv_to_rgb(h + gap, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v))
                font_clrs.append(ex.hsv_to_rgb(h + gap, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v))
            if self.mainloop.m.game_variant == 0:
                if random.randint(0, 1) == 0:
                    self.choices = self.lang.alphabet_uc[:]
                else:
                    self.choices = self.lang.alphabet_lc[:]
            elif self.mainloop.m.game_variant == 1:
                self.choices = [str(x) for x in range(0, 9)]
        elif self.mainloop.m.game_variant == 2:
            self.choices = [x for x in range(2, 20)]
        elif self.mainloop.m.game_variant == 3:
            self.initiate_images()
            self.choices = [x for x in range(len(self.imgs))]
        elif self.mainloop.m.game_variant == 5:
            self.initiate_shapes()
            self.choices = [x for x in range(len(self.imgs))]
            random.shuffle(self.color_ind)
            if self.level.lvl < 3:
                self.mixed_colours = True
            else:
                self.mixed_colours = False
        elif self.mainloop.m.game_variant == 4:
            self.func_number = random.randint(0, 3)

            #create fractions
            self.fractions = []
            full = False
            while not full:
                a = random.randint(1, 4)
                b = random.randint(a+1, 6)
                l = [a, b]
                if l not in self.fractions:
                    self.fractions.append(l)
                if len(self.fractions) >= self.term_len:
                    full = True
            clrs1 = []
            clrs2 = []
            hues = []
            for i in range(self.term_len):
                if self.level.lvl < 3:
                    h = random.randrange(0, 100, 5)
                    gap = i * (155 // self.term_len)
                else:
                    gap = 0
                clrs1.append(ex.hsv_to_rgb(h + gap, 150, 230))
                clrs2.append(ex.hsv_to_rgb(h + gap, 255, 140))
                hues.append(h + gap)
            self.choices = [x for x in range(2, 20)]

        random.shuffle(self.choices)
        self.term_values = self.choices[0:self.term_len]

        data = [self.task_len, 4]
        self.data = data

        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.board.set_animation_constraints(0, data[0], 0, data[1])
        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.unit_mouse_over = None
        self.units = []

        self.board.board_bg.initcolor = color
        self.board.board_bg.color = color
        self.board.board_bg.update_me = True

        self.left_offset = (self.data[0] - len(self.task)) // 2

        self.positions = [x for x in range(self.left_offset, len(self.task)+self.left_offset)]
        self.solution_grid = [0 for x in range(data[0])]

        random.shuffle(self.positions)
        p_ind = 0

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None

        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")

        if self.mainloop.m.game_variant == 5:
            fg_tint_color = (30, 30, 30)

        dc_tint_color = ex.hsv_to_rgb(160, self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
        if self.mainloop.m.game_variant == 3:
            fg_tint_color = (30, 30, 30)
            if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
                bg_door_img_src = os.path.join('unit_bg', "img_decor_bb.png")
                dc_tint_color = None
            else:
                bg_door_img_src = os.path.join('unit_bg', "img_decor_w.png")
        if self.mainloop.m.game_variant == 4:
            bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        if self.mainloop.m.game_variant == 2:
            bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
            fg_img_src = "splash_mask.png"
            hue_choice = [[255, 255, 255], [2, 2, 2], [140, 140, 140], [255, 0, 0], [255, 138, 0], [255, 255, 0],
                          [181, 219, 3], [0, 160, 0], [41, 131, 82], [0, 130, 133], [0, 0, 255], [0, 0, 132],
                          [132, 0, 132], [255, 0, 255], [74, 0, 132], [255, 20, 138], [132, 0, 0], [140, 69, 16],
                          [0, 255, 255], [0, 255, 0]]

        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]

        for i in range(len(self.task)):
            self.solution_grid[self.left_offset + i] = 1
            if self.task[i] == "?":
                #add placeholder and the items to add
                self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=0, grid_w=1, grid_h=1, txt=None,
                                              fg_img_src=None, bg_img_src=None, dc_img_src=bg_door_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                              bg_tint_color=None, fg_tint_color=None, txt_align=(0, 0),
                                              font_type=10, multi_color=False, alpha=True, immobilized=True, mode=2,
                                              dc_tint_color=dc_tint_color)
                if self.mainloop.m.game_variant < 2:
                    v = self.term_values[int(self.term[i % self.term_len])]
                else:
                    v = ""
                if self.mainloop.m.game_variant == 3:
                    img = "%s.jpg" % self.imgs[self.term_values[int(self.term[i % self.term_len])]]
                    img_src = os.path.join('art4apps', self.category, img)
                    self.board.add_universal_unit(grid_x=self.positions[p_ind], grid_y=2, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=img_src, bg_img_src=img_src, dc_img_src=None,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=None, dc_tint_color=None,
                                                  fg_tint_color=(50, 50, 50), txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                    self.board.ships[-1].set_blit_mask(os.path.join('unit_bg', 'img_mask.png'))
                elif self.mainloop.m.game_variant == 5:
                    img = "%s.png" % self.imgs[self.term_values[int(self.term[i % self.term_len])]]
                    img_src = os.path.join('shapes', img)

                    if self.mixed_colours:
                        bg_tint_color = self.shape_colors[self.color_ind[int(self.term[i % self.term_len])]]
                        fg_tint_color = self.shape_colors_fg[self.color_ind[int(self.term[i % self.term_len])]]
                    else:
                        bg_tint_color = self.shape_colors[self.color_ind[0]]
                        fg_tint_color = self.shape_colors_fg[self.color_ind[0]]
                    self.board.add_universal_unit(grid_x=self.positions[p_ind], grid_y=2, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=img_src, bg_img_src=img_src, dc_img_src=None,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=bg_tint_color, dc_tint_color=None,
                                                  fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                elif self.mainloop.m.game_variant == 2:
                    color_index = self.term_values[int(self.term[i % self.term_len])]
                    dc_tint_colorx = hue_choice[color_index]
                    if color_index < 3:
                        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
                            bg_tint_color = (90, 90, 90)
                            fg_tint_color = (60, 60, 60)
                        else:
                            bg_tint_color = (200, 200, 200)
                            fg_tint_color = (160, 160, 160)
                    else:
                        bg_tint_color = ex.hsv_to_rgb(
                            ex.rgb_to_hsv(dc_tint_colorx[0], dc_tint_colorx[1], dc_tint_colorx[2])[0],
                            self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)

                        fg_tint_color = ex.hsv_to_rgb(
                            ex.rgb_to_hsv(dc_tint_colorx[0], dc_tint_colorx[1], dc_tint_colorx[2])[0],
                            self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)
                    self.board.add_universal_unit(grid_x=self.positions[p_ind], grid_y=2, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=fg_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=bg_tint_color, dc_tint_color=dc_tint_colorx,
                                                  fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                elif self.mainloop.m.game_variant == 4:
                    bg_color = ex.hsv_to_rgb(hues[int(self.term[i % self.term_len])], self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
                    fg_color = ex.hsv_to_rgb(hues[int(self.term[i % self.term_len])], self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)
                    self.board.add_universal_unit(grid_x=self.positions[p_ind], grid_y=2, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=None,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=bg_color, dc_tint_color=None,
                                                  fg_tint_color=fg_color, txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                    fraction = classes.drw.fraction.Fraction(1, self.board.scale, clrs1[int(self.term[i % self.term_len])], clrs2[int(self.term[i % self.term_len])], self.fractions[int(self.term[i % self.term_len])], self.func_number)
                    self.board.ships[-1].manual_painting_layer = 1
                    self.board.ships[-1].init_m_painting()
                    self.board.ships[-1].manual_painting = fraction.get_canvas().copy()
                    self.board.ships[-1].update_me = True

                elif self.mainloop.m.game_variant < 2:
                    self.board.add_universal_unit(grid_x=self.positions[p_ind], grid_y=2, grid_w=1, grid_h=1, txt=v,
                                                  fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=[font_clrs[int(self.term[i % self.term_len])],],
                                                  bg_tint_color=unit_clrs[int(self.term[i % self.term_len])], fg_tint_color=unit_clrs_fg[int(self.term[i % self.term_len])],
                                                  txt_align=(0, 0), font_type=0, multi_color=False,
                                                  alpha=True, immobilized=False, fg_as_hover=True)

                self.units.append(self.board.ships[-1])

                self.board.ships[-1].pattern_value = self.term[i % self.term_len]
                self.board.ships[-1].highlight = False
                self.board.ships[-1].readable = False
                self.board.ships[-1].checkable = True
                self.board.ships[-1].init_check_images()
                p_ind += 1
            else:
                #add pre-entered part of a pattern
                if self.mainloop.m.game_variant < 2:
                    v = self.term_values[int(self.task[i])]
                else:
                    v = ""
                if self.mainloop.m.game_variant == 3:
                    img = "%s.jpg" % self.imgs[self.term_values[int(self.term[i % self.term_len])]]
                    img_src = os.path.join('art4apps', self.category, img)
                    self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=0, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=None, bg_img_src=img_src, dc_img_src=bg_door_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=None, dc_tint_color=dc_tint_color,
                                                  fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=True, fg_as_hover=False)
                elif self.mainloop.m.game_variant == 5:
                    img = "%s.png" % self.imgs[self.term_values[int(self.term[i % self.term_len])]]
                    img_src = os.path.join('shapes', img)
                    if self.mixed_colours:
                        bg_tint_color = self.shape_colors[self.color_ind[int(self.term[i % self.term_len])]]
                    else:
                        bg_tint_color = self.shape_colors[self.color_ind[0]]
                    self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=0, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=None, bg_img_src=img_src, dc_img_src=bg_door_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=bg_tint_color, dc_tint_color=dc_tint_color,
                                                  fg_tint_color=None, txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=True, fg_as_hover=False)

                elif self.mainloop.m.game_variant == 2:
                    color_index = self.term_values[int(self.term[i % self.term_len])]
                    dc_tint_colorx = hue_choice[color_index]
                    if color_index < 3:
                        if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
                            bg_tint_color = (90, 90, 90)
                            fg_tint_color = (60, 60, 60)
                        else:
                            bg_tint_color = (200, 200, 200)
                            fg_tint_color = (160, 160, 160)
                    else:
                        bg_tint_color = ex.hsv_to_rgb(
                            ex.rgb_to_hsv(dc_tint_colorx[0], dc_tint_colorx[1], dc_tint_colorx[2])[0],
                            self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)

                        fg_tint_color = ex.hsv_to_rgb(
                            ex.rgb_to_hsv(dc_tint_colorx[0], dc_tint_colorx[1], dc_tint_colorx[2])[0],
                            self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)
                    self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=0, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=fg_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=bg_tint_color, dc_tint_color=dc_tint_colorx,
                                                  fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                elif self.mainloop.m.game_variant == 4:
                    bg_color = ex.hsv_to_rgb(hues[int(self.term[i % self.term_len])], self.mainloop.cl.bg_color_s,
                                             self.mainloop.cl.bg_color_v)
                    self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=0, grid_w=1, grid_h=1, txt="",
                                                  fg_img_src=None, bg_img_src=bg_img_src, dc_img_src=None,
                                                  bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                                  bg_tint_color=bg_color, dc_tint_color=None,
                                                  fg_tint_color=None, txt_align=(0, 0), font_type=0,
                                                  multi_color=False, alpha=True, immobilized=True, fg_as_hover=False)

                    fraction = classes.drw.fraction.Fraction(1, self.board.scale, clrs1[int(self.term[i % self.term_len])], clrs2[int(self.term[i % self.term_len])], self.fractions[int(self.term[i % self.term_len])], self.func_number)
                    self.board.ships[-1].manual_painting_layer = 0
                    self.board.ships[-1].init_m_painting()
                    self.board.ships[-1].manual_painting = fraction.get_canvas().copy()
                    self.board.ships[-1].update_me = True
                elif self.mainloop.m.game_variant < 2:
                    self.board.add_universal_unit(grid_x=self.left_offset + i, grid_y=0, grid_w=1, grid_h=1, txt=v,
                                                  fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                                  bg_color=(0, 0, 0, 0), border_color=None,
                                                  font_color=[font_clrs[int(self.term[i % self.term_len])], ],
                                                  bg_tint_color=unit_clrs[int(self.term[i % self.term_len])],
                                                  fg_tint_color=unit_clrs_fg[int(self.term[i % self.term_len])],
                                                  txt_align=(0, 0), font_type=0, multi_color=False,
                                                  alpha=True, immobilized=False, fg_as_hover=True)

                if self.mainloop.m.game_variant == 2 or self.mainloop.m.game_variant == 5:
                    self.board.ships[-1].outline = False

                self.board.ships[-1].pattern_value = self.term[i % self.term_len]
                self.board.ships[-1].immobilize()
                self.board.ships[-1].highlight = False
                self.board.ships[-1].readable = False
                self.board.ships[-1].checkable = True
                self.board.ships[-1].init_check_images()

        #add noise
        for i in range(p_ind, len(self.positions)):
            if self.mainloop.m.game_variant < 2:
                v = self.term_values[int(self.term[i % self.term_len])]
            else:
                v = ""
            if self.mainloop.m.game_variant == 3:
                img = "%s.jpg" % self.imgs[self.term_values[int(self.term[i % self.term_len])]]
                img_src = os.path.join('art4apps', self.category, img)
                self.board.add_universal_unit(grid_x=self.positions[i], grid_y=2, grid_w=1, grid_h=1, txt="",
                                              fg_img_src=img_src, bg_img_src=img_src, dc_img_src=None,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                              bg_tint_color=None, dc_tint_color=None,
                                              fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                              multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                self.board.ships[-1].set_blit_mask(os.path.join('unit_bg', 'img_mask.png'))
            elif self.mainloop.m.game_variant == 5:
                img = "%s.png" % self.imgs[self.term_values[int(self.term[i % self.term_len])]]
                img_src = os.path.join('shapes', img)
                if self.mixed_colours:
                    bg_tint_color = self.shape_colors[self.color_ind[int(self.term[i % self.term_len])]]
                    fg_tint_color = self.shape_colors_fg[self.color_ind[int(self.term[i % self.term_len])]]
                else:
                    bg_tint_color = self.shape_colors[self.color_ind[0]]
                    fg_tint_color = self.shape_colors_fg[self.color_ind[0]]
                self.board.add_universal_unit(grid_x=self.positions[i], grid_y=2, grid_w=1, grid_h=1, txt="",
                                              fg_img_src=img_src, bg_img_src=img_src, dc_img_src=None,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                              bg_tint_color=bg_tint_color, dc_tint_color=None,
                                              fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                              multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
            elif self.mainloop.m.game_variant == 2:
                color_index = self.term_values[int(self.term[i % self.term_len])]
                dc_tint_colorx = hue_choice[color_index]
                if color_index < 3:
                    if self.mainloop.scheme is not None and self.mainloop.scheme.dark:
                        bg_tint_color = (90, 90, 90)
                        fg_tint_color = (60, 60, 60)
                    else:
                        bg_tint_color = (200, 200, 200)
                        fg_tint_color = (160, 160, 160)
                else:
                    bg_tint_color = ex.hsv_to_rgb(
                        ex.rgb_to_hsv(dc_tint_colorx[0], dc_tint_colorx[1], dc_tint_colorx[2])[0],
                        self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
                    fg_tint_color = ex.hsv_to_rgb(
                        ex.rgb_to_hsv(dc_tint_colorx[0], dc_tint_colorx[1], dc_tint_colorx[2])[0],
                        self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)
                self.board.add_universal_unit(grid_x=self.positions[i], grid_y=2, grid_w=1, grid_h=1, txt="",
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=fg_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                              bg_tint_color=bg_tint_color, dc_tint_color=dc_tint_colorx,
                                              fg_tint_color=fg_tint_color, txt_align=(0, 0), font_type=0,
                                              multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
            elif self.mainloop.m.game_variant == 4:
                bg_color = ex.hsv_to_rgb(hues[int(self.term[i % self.term_len])], self.mainloop.cl.bg_color_s,
                                         self.mainloop.cl.bg_color_v)
                fg_color = ex.hsv_to_rgb(hues[int(self.term[i % self.term_len])], self.mainloop.cl.fg_hover_s,
                                         self.mainloop.cl.fg_hover_v)
                self.board.add_universal_unit(grid_x=self.positions[i], grid_y=2, grid_w=1, grid_h=1, txt="",
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=None,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=font_color,
                                              bg_tint_color=bg_color, dc_tint_color=None,
                                              fg_tint_color=fg_color, txt_align=(0, 0), font_type=0,
                                              multi_color=False, alpha=True, immobilized=False, fg_as_hover=True)
                fraction = classes.drw.fraction.Fraction(1, self.board.scale, clrs1[int(self.term[i % self.term_len])],
                                                         clrs2[int(self.term[i % self.term_len])],
                                                         self.fractions[int(self.term[i % self.term_len])],
                                                         self.func_number)
                self.board.ships[-1].manual_painting_layer = 1
                self.board.ships[-1].init_m_painting()
                self.board.ships[-1].manual_painting = fraction.get_canvas().copy()
                self.board.ships[-1].update_me = True
            elif self.mainloop.m.game_variant < 2:
                self.board.add_universal_unit(grid_x=self.positions[i], grid_y=2, grid_w=1, grid_h=1, txt=v,
                                              fg_img_src=bg_img_src, bg_img_src=bg_img_src, dc_img_src=dc_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None,
                                              font_color=[font_clrs[int(self.term[i % self.term_len])], ],
                                              bg_tint_color=unit_clrs[int(self.term[i % self.term_len])],
                                              fg_tint_color=unit_clrs_fg[int(self.term[i % self.term_len])],
                                              txt_align=(0, 0), font_type=0, multi_color=False,
                                              alpha=True, immobilized=False, fg_as_hover=True)

            if self.mainloop.m.game_variant == 2 or self.mainloop.m.game_variant == 5:
                self.board.ships[-1].outline = False

            self.units.append(self.board.ships[-1])

            self.board.ships[-1].pattern_value = self.term[i % self.term_len]
            self.board.ships[-1].highlight = False
            self.board.ships[-1].readable = False
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.lang.d["Complete the pattern"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.check_result()
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def start_game(self, gameid):
        self.mainloop.m.start_hidden_game(gameid)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check(self):
        for each in self.board.ships:
            each.update_me = True
            if each.checkable and (each.grid_y == 0):
                if each.pattern_value == self.term[(self.left_offset + each.grid_x) % self.term_len]:
                    each.set_display_check(True)
                else:
                    each.set_display_check(False)
            else:
                each.set_display_check(None)
        self.check_for_pattern()

    def check_for_pattern(self):
        pattern = [" " for i in range(self.task_len)]
        for each in self.board.ships:
            each.update_me = True
            if each.checkable and (each.grid_y == 0):
                pattern[each.grid_x - self.left_offset] = each.pattern_value

        if self.has_pattern(pattern):
            self.level.next_board()
            for each in self.board.ships:
                each.update_me = True
                if each.checkable and (each.grid_y == 0):
                    each.set_display_check(True)

    def auto_check_reset(self):
        for each in self.board.ships:
            each.update_me = True
            each.set_display_check(None)

    def check_result(self):
        if self.board.grid[0] == self.solution_grid:
            self.auto_check()
        else:
            self.auto_check_reset()

    def generate_term(self, s_len):
        found = False
        while not found:
            sequence = ""
            for i in range(s_len):
                sequence += str(random.randint(0, s_len-1))
                if i > 0 and not found:
                    if sequence[i-1] != sequence[i]:
                        found = True
            if found:
                # if len is even and halves are the same then regenerate to avoid having half len term, ie 1212 1212
                if s_len > 3 and s_len % 2 == 0:
                    if sequence[0:s_len//2] == sequence[s_len//2:]:
                        found = False
                        continue
                return sequence

    def generate_task(self, term, term_len, term_count, term_completed_count, term_semi_completed_count, shuffled=False):
        s = []
        indexes = [x for x in range(term_len)]
        for i in range(term_completed_count):
            s.append(term)

        for i in range(term_semi_completed_count):
            count2show = random.randint(1, term_len-1)
            # make sure all numbers are displayed by the last semi-shown sequence
            if i == term_semi_completed_count-1:
                li = len(indexes)
                if count2show < li:
                    count2show = li

            ts = ["?" for each in range(term_len)]
            if count2show <= len(indexes):
                for j in range(count2show):
                    p = random.randint(0, len(indexes)-1)
                    ts[indexes[p]] = term[indexes[p]]
                    del indexes[p]
            else:
                li = len(indexes)
                if li > 0:
                    for j in range(li):
                        p = random.randint(0, len(indexes) - 1)
                        ts[indexes[p]] = term[indexes[p]]
                        del indexes[p]

                for j in range(count2show-li):
                    p = random.randint(0, term_len-1)
                    ts[p] = term[p]
            s.append("".join(ts))
        for i in range(term_count-(term_completed_count+term_semi_completed_count)):
            s.append("?" * term_len)
        if shuffled:
            random.shuffle(s)
            return "".join(s)
        else:
            return "".join(s)

    def has_pattern(self, sequence):
        l = len(sequence)
        # pattern needs to repeat at least 2 times and needs to have at least 2 different items
        has_pattern = False
        for i in range(2, l//2 + 1):
            if l % i == 0:  # is the "i" one of the factors?
                has_pattern = True
                # check if all parts are equal
                for j in range(i, l, i):
                    if sequence[j:j+i] != sequence[j-i:j]:
                        has_pattern = False
                if has_pattern:
                    return has_pattern
        return has_pattern

    def initiate_shapes(self):
        self.shape_colors = []
        self.shape_colors_fg = []
        for h in range(0, 255, 15):
            s = random.randint(200, 235)
            v = random.randint(150, 235)
            self.shape_colors.append(ex.hsv_to_rgb(h, s, v))
            self.shape_colors_fg.append(ex.hsv_to_rgb(h, s - 40, v + 20))
        self.color_ind = [x for x in range(len(self.shape_colors))]
        self.imgs = ["s%d" % x for x in range(1, 18)]

    def initiate_images(self):
        gv = random.randint(0, 15)
        if gv == 0:
            self.category = "animals"
            self.imgs = ['panda', 'pug', 'koala', 'gorilla', 'kitten', 'rabbit', 'baby_rabbit', 'chimp', 'puppy', 'cat', 'dog']
        elif gv == 12:
            self.category = "animals"  # farm
            self.imgs = ['cow', 'pony', 'pig', 'donkey', 'sheep', 'buffalo', 'bull', 'goat', 'horse', 'ram', 'ox']
        elif gv == 13:
            self.category = "animals"  # large predators
            self.imgs = ['wolf', 'panther', 'tiger', 'fox', 'leopard', 'bear', 'lion_cub', 'jaguar', 'hyena', 'lion']
        elif gv == 14:
            self.category = "animals"  #
            self.imgs = ['fawn', 'llama', 'moose', 'zebra', 'camel', 'antelope', 'anteater', 'lama', 'deer', 'hippopotamus', 'kangaroo', 'elk', 'rhinoceros', 'elephant', 'giraffe']
        elif gv == 15:
            self.category = "animals"  # rodents
            self.imgs = ['mouse', 'hamster', 'bat', 'hedgehog', 'guinea_pig', 'squirrel', 'sloth', 'rat', 'otter', 'mole', 'gopher', 'beaver', 'skunk', 'lemur', 'opossum', ]
        elif gv == 1:
            self.category = "animals"  # birds
            self.imgs = ['turkey', 'magpie', 'vulture', 'bird', 'crow', 'parakeet', 'hummingbird', 'chick', 'hen', 'shrike', 'penguin', 'ostrich', 'pigeon', 'flamingo', 'sparrow', 'dove', 'eagle', 'owl', 'goose', 'pelican', 'duck', 'peacock', 'parrot', 'jay', 'rooster', 'blackbird', 'swan', 'chicken']
        elif gv == 2:
            self.category = "animals"  # bugs
            self.imgs = ['ladybug', 'spider', 'mosquito', 'slug', 'caterpillar', 'scorpion', 'bee', 'snail', 'beetle', 'dragonfly', 'ant']
        elif gv == 3:
            self.category = "animals"  # water animals
            self.imgs = ['shrimp', 'seal', 'lobster', 'crab', 'clam', 'squid', 'starfish', 'piranha', 'dolphin', 'whale', 'jellyfish', 'shark', 'ray', 'oyster']
        elif gv == 4:
            self.category = "animals"  # reptiles and amphibians
            self.imgs = ['frog', 'turtle', 'iguana', 'snake', 'chameleon', 'viper', 'cobra', 'salamander', 'toad', 'lizard', 'alligator']
        elif gv == 5:
            self.category = "sport"
            self.imgs = ['judo', 'pool', 'ride', 'stretch', 'walk', 'run', 'swim', 'hop', 'hike', 'boxing', 'hockey', 'throw', 'skate', 'win', 'squat', 'ski', 'golf', 'stand', 'tennis', 'jump', 'rowing', 'jog', 'rope']
        elif gv == 6:
            self.category = "construction"
            self.imgs = ['lighthouse', 'circus', 'temple', 'well', 'street', 'castle', 'store', 'school', 'farm', 'bridge', 'dam', 'pyramid', 'barn', 'mill', 'cabin', 'shed', 'garage', 'mosque', 'hospital', 'tent', 'house',  'bank', 'hut']
        elif gv == 7:
            self.category = "nature"
            self.imgs = ['land', 'canyon', 'sea', 'shore', 'mountain', 'pond', 'cave', 'island', 'forest', 'desert', 'iceberg']
        elif gv == 8:
            self.category = "jobs"
            self.imgs = ['clown', 'engineer', 'priest', 'vet', 'judge', 'chef', 'athlete', 'librarian', 'juggler', 'police', 'plumber', 'queen', 'farmer', 'magic', 'knight', 'doctor', 'bricklayer', 'cleaner', 'teacher', 'hunter', 'soldier', 'musician', 'fisherman', 'princess', 'fireman', 'nun', 'pirate', 'cowboy', 'electrician', 'nurse', 'king', 'president', 'office', 'carpenter', 'worker', 'mechanic', 'actor', 'cook', 'student', 'butcher', 'accountant', 'prince', 'pope', 'sailor', 'boxer', 'ballet', 'astronaut', 'painter', 'anaesthesiologist', 'scientist']
        elif gv == 9:
            self.category = "clothes_n_accessories"
            self.imgs = ['gloves', 'hat', 'jacket', 'overalls', 'pullover', 'sandals', 'shirt', 'shoe', 'shoes', 'shorts', 'slippers', 'sneaker', 'sweatshirt', 'trousers', 'vest']
        elif gv == 10:
            self.category = "fruit_n_veg"
            self.imgs = ['carrot', 'blackberries', 'celery', 'turnip', 'cacao', 'peach', 'melon', 'grapefruit', 'broccoli', 'grapes', 'spinach', 'fig', 'radish', 'tomato', 'kiwi', 'asparagus', 'olives', 'cucumbers', 'beans', 'strawberry', 'peppers', 'raspberry', 'apricot', 'potatoes', 'peas', 'cabbage', 'cherries', 'squash', 'blueberries', 'pear', 'orange', 'pumpkin', 'avocado', 'garlic', 'onion', 'apple', 'lime', 'cauliflower', 'mango', 'lettuce', 'lemon', 'aubergine', 'artichokes', 'plums', 'leek', 'bananas', 'papaya']
        elif gv == 11:
            self.category = "transport"
            self.imgs = ['taxi', 'car', 'bike', 'raft', 'bus', 'boat', 'truck', 'sleigh', 'carpet', 'motorcycle', 'train', 'ship', 'van', 'canoe', 'rocket', 'sledge', 'bicycle']
