# -*- coding: utf-8 -*-
import sys, os
import pygame
import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.menu_items
import classes.universal

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)
        self.max_size = 99

    def create_game_objects(self, level=1):
        self.allow_unit_animations = False
        self.board.decolorable = False
        self.board.draw_grid = False

        self.unit_mouse_over = None

        self.bg_color = [255, 255, 255, 0]
        color = [255, 255, 255, 0]
        self.transp = (0, 0, 0, 0)

        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.bg_color = (0, 0, 0, 0)
                color = (0, 0, 0, 0)
                self.guides_color = (30, 30, 30, 0)

        #data = [28, 18]
        data = [28, 23]

        x_count = self.get_x_count(data[1], even=None)
        if x_count > 28:
            data[0] = x_count - 1

        self.data = data

        self.mainloop.info.hide_buttons(0, 0, 0, 0, 1, 0, 1, 0, 0)
        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.scale = scale
        self.border_width = self.scale // 4
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.line_color = (20, 20, 20)

        self.template_units = None

        self.btns_left = self.data[0] - 7
        self.color_selectors_left = 13


        self.cat_sample = classes.menu_items.Category(self, self.mainloop.m.categories[0], 1, 1,
                                                      6, 6, self.mainloop.m.categories[0].cat_id,
                                                   self.bg_color, "ico_tn_02.png", 0, sequence_id=0)

        self.game_sample = classes.menu_items.GameIcon(self, self.mainloop.m.games[11], 1, 11,
                                                       6, 6, self.bg_color, [0, 5],
                                                       [1, 0, 1, 0, 1], "ico_c_13.png", 0,
                                                       sequence_id=0)


        self.cat_ind = classes.menu_items.Category(self, self.mainloop.m.categories[0], 8, 1, 3, 3,
                                                   self.mainloop.m.categories[0].cat_id,
                                                   self.bg_color, "ico_theme_rb_a.png", 0, sequence_id=0)

        self.cat_ind2 = classes.menu_items.Category(self, self.mainloop.m.categories[0], 8, 4, 3, 3,
                                                    self.mainloop.m.categories[0].cat_id,
                                                    self.bg_color, "ico_theme_rb_n.png", 1, sequence_id=0)


        """
        self.game_ind = classes.menu_items.Category(self, self.mainloop.m.categories[0], 8, 10, 3, 3,
                                                   self.mainloop.m.categories[0].cat_id,
                                                   self.bg_color, "ico_theme_rb_a.png", 0, sequence_id=0)

        self.game_ind2 = classes.menu_items.Category(self, self.mainloop.m.categories[0], 8, 13, 3, 3,
                                                    self.mainloop.m.categories[0].cat_id,
                                                    self.bg_color, "ico_theme_rb_n.png", 1, sequence_id=0)

        """
        self.game_ind = classes.menu_items.GameIcon(self, self.mainloop.m.games[11], 8, 11, 3, 3, self.bg_color,
                                                    [0, 5], [1, 1, 1, 1, 1], "ico_theme_rb_a.png", 0, sequence_id=0)

        self.game_ind2 = classes.menu_items.GameIcon(self, self.mainloop.m.games[11], 8, 14, 3, 3, self.bg_color,
                                                     [0, 5], [0, 0, 0, 0, 0], "ico_theme_rb_n.png", 1, sequence_id=0)

        self.game_ind.challenge_completed = False
        self.game_ind2.challenge_completed = False

        self.initialize_styles()

        self.menu_inds = [self.cat_sample, self.cat_ind, self.cat_ind2, self.game_sample, self.game_ind, self.game_ind2]

        for each in self.menu_inds:
            each.show_titles_on_hover = False
            self.board.all_sprites_list.add(each)
        #16, 2
        self.board.add_universal_unit(grid_x=2, grid_y=18, grid_w=4, grid_h=4, txt="",
                                      fg_img_src="info_m_h.png",
                                      bg_img_src="info_m.png", dc_img_src="info_d.png", bg_color=self.bg_color,
                                      border_color=None, font_color=None,
                                      bg_tint_color=self.mainloop.cl.info_buttons_col,
                                      fg_tint_color=self.mainloop.cl.info_buttons_col,
                                      txt_align=(0, 0), font_type=0, multi_color=False, alpha=True, immobilized=False,
                                      fg_as_hover=True)

        self.info_ind = self.board.ships[-1]

        if self.data[0] > 30:
            l_shift = 1
        else:
            l_shift = 0
        #self.shape_loc1 = [[14 + l_shift, 1], [14 + l_shift, 5], [18 + l_shift, 1], [18 + l_shift, 5]]
        #self.shape_loc2 = [[14 + l_shift, 1], [14 + l_shift, 3], [16 + l_shift, 1], [16 + l_shift, 3]]

        self.shape_loc1 = [[0, 7], [2, 7], [4, 7], [6, 7]]
        self.shape_loc2 = [[0, 7], [2, 7], [4, 7], [6, 7]]
        self.shape_imgs = ["menu_circle.png", "menu_square.png", "menu_hex.png", "menu_star.png"]
        self.shape_inds = []

        for i in range(4):
            if i == self.mainloop.cl.color_sliders[6][2]:
                self.board.add_universal_unit(grid_x=self.shape_loc2[i][0], grid_y=self.shape_loc2[i][1], grid_w=2, grid_h=2,
                                              bg_img_src=self.shape_imgs[i], dc_img_src=None,
                                              fg_img_src="shape_radio_btn.png", bg_color=self.bg_color,
                                              bg_tint_color=self.mainloop.cl.info_buttons_col, fg_tint_color=self.bg_color,
                                              immobilized=True)
            else:
                self.board.add_universal_unit(grid_x=self.shape_loc1[i][0], grid_y=self.shape_loc1[i][1], grid_w=2, grid_h=2,
                                              bg_img_src=self.shape_imgs[i], dc_img_src=None,
                                              fg_img_src=None, bg_color=self.bg_color,
                                              bg_tint_color=self.mainloop.cl.info_buttons_col, fg_tint_color=self.bg_color,
                                              immobilized=True)

            self.shape_inds.append(self.board.ships[-1])

        self.color_sliders = self.mainloop.cl.color_sliders
        self.functions = [self.mainloop.cl.update_cbg_color, self.mainloop.cl.update_cfg_color, self.mainloop.cl.update_gbg_color, self.mainloop.cl.update_gfg_color, self.mainloop.cl.update_lvl_color, self.mainloop.cl.update_info_color]
        self.current_funct = self.functions[0]
        self.sections = []

        self.board.add_unit(self.color_selectors_left, 2, 2, 2, classes.board.ImgShip, "", self.mainloop.cl.c_bg_tint_color,
                           "bg_col_a.png", 0, alpha=True)
        self.board.add_unit(self.color_selectors_left, 4, 2, 2, classes.board.ImgShip, "", self.mainloop.cl.c_fg_tint_color,
                            "fg_col_n.png", 0, alpha=True)
        self.board.add_unit(self.color_selectors_left, 11, 2, 2, classes.board.ImgShip, "", self.mainloop.cl.g_bg_tint_color,
                            "bg_col_n.png", 0, alpha=True)
        self.board.add_unit(self.color_selectors_left, 13, 2, 2, classes.board.ImgShip, "", self.mainloop.cl.g_fg_tint_color,
                            "fg_col_n.png", 0, alpha=True)
        self.board.add_unit(self.color_selectors_left, 15, 2, 2, classes.board.ImgShip, "", self.mainloop.cl.lvl_completed_col,
                            "circle_n.png", 0, alpha=True)
        # 21, 3
        self.board.add_unit(self.color_selectors_left, 19, 2, 2, classes.board.ImgShip, "", self.mainloop.cl.info_buttons_col,
                            "circle_n.png", 0, alpha=True)

        for i in range(-6, 0):
            self.board.ships[i].my_id = i + 6
            self.board.ships[i].set_outline(self.bg_color, self.border_width)
            self.sections.append(self.board.ships[i])

        squirrel = os.path.join('squirrels', "squirrel-with-paintbrush.webp")
        squirel_img_size = min(self.data[0] - 20, 14)

        self.board.add_unit(self.data[0]-squirel_img_size-3, self.data[1] - squirel_img_size, squirel_img_size, squirel_img_size, classes.board.ImgShip, "", self.bg_color, squirrel, 0, alpha=True)
        self.board.ships[-1].immobilize()

        self.prev_selection = self.sections[0]
        self.active_selection = self.sections[0]
        self.active_selection.set_outline(self.bg_color, 2)

        self.board.add_unit(data[0] - 3, 0, 1, 1, classes.board.Letter, "H", color, "", 2)
        self.board.add_unit(data[0] - 2, 0, 1, 1, classes.board.Letter, "S", color, "", 2)
        self.board.add_unit(data[0] - 1, 0, 1, 1, classes.board.Letter, "V", color, "", 2)
        self.selector_count = self.mainloop.cl.selector_count
        self.step = self.mainloop.cl.step

        self.custom_color_hsv = [self.color_sliders[0][0] * self.step,
                                 self.color_sliders[0][1] * self.step,
                                 self.color_sliders[0][2] * self.step]
        self.h_units = []
        self.s_units = []
        self.v_units = []

        # hue selectors
        for i in range(0, self.selector_count):
            c0 = ex.hsv_to_rgb(int(self.step * i), 255, 255)
            self.board.add_unit(data[0] - 3, i + 1, 1, 1, classes.board.Ship, "", c0, "", 0)
            self.h_units.append(self.board.ships[-1])

        # saturation selectors
        for i in range(0, self.selector_count):
            c1 = ex.hsv_to_rgb(0, int(self.step * i), 255)
            self.board.add_unit(data[0] - 2, i + 1, 1, 1, classes.board.Ship, "", c1, "", 0)
            self.s_units.append(self.board.ships[-1])

        # vibrance selectors
        for i in range(0, self.selector_count):
            c2 = ex.hsv_to_rgb(0, 255, int(self.step * i))
            self.board.add_unit(data[0] - 1, i + 1, 1, 1, classes.board.Ship, "", c2, "", 0)
            self.v_units.append(self.board.ships[-1])

        for each in self.board.ships:
            each.outline = False
            each.immobilize()
            each.readable = False

        self.board.add_door(data[0] - 3, self.color_sliders[0][0] + 1, 1, 1, classes.board.Door, "", color, "")
        self.h_door = self.board.units[-1]
        self.h_door.door_outline = True
        self.h_door.perm_outline_color = (200, 0, 0)
        self.h_door.perm_outline_width = 10
        self.board.all_sprites_list.move_to_front(self.h_door)

        self.board.add_door(data[0] - 2, self.color_sliders[0][1] + 1, 1, 1, classes.board.Door, "", color, "")
        self.s_door = self.board.units[-1]
        self.s_door.door_outline = True
        self.s_door.perm_outline_color = (200, 0, 0)
        self.s_door.perm_outline_width = 10
        self.board.all_sprites_list.move_to_front(self.s_door)

        self.board.add_door(data[0] - 1, self.color_sliders[0][2] + 1, 1, 1, classes.board.Door, "", color, "")
        self.v_door = self.board.units[-1]
        self.v_door.door_outline = True
        self.v_door.perm_outline_color = (200, 0, 0)
        self.v_door.perm_outline_width = 10
        self.board.all_sprites_list.move_to_front(self.v_door)

        # add a frame around the colour electors
        self.board.add_door(self.color_selectors_left - 1, 1, 4, self.data[1] - 2, classes.board.Door, "", color, "")
        self.selector_frame = self.board.units[-1]
        self.selector_frame.door_outline = True
        self.selector_frame.perm_outline_color = self.mainloop.cl.info_buttons_col
        self.selector_frame.perm_outline_width = 1
        # self.board.all_sprites_list.move_to_front(self.selector_frame)

        self.update_colors()

    def update_color_choosers(self, h=None, s=None, v=None):
        if h is not None:
            self.custom_color_hsv[0] = int(h * self.step)
        if s is not None:
            self.custom_color_hsv[1] = int(s * self.step)
        if v is not None:
            self.custom_color_hsv[2] = int(v * self.step)

        for i in range(0, self.selector_count):
            self.h_units[i].color = ex.hsv_to_rgb(int(i * self.step), self.custom_color_hsv[1], self.custom_color_hsv[2])
            self.h_units[i].initcolor = self.h_units[i].color
            self.h_units[i].update_me = True

        for i in range(0, self.selector_count):
            self.s_units[i].color = ex.hsv_to_rgb(self.custom_color_hsv[0], int(i * self.step), self.custom_color_hsv[2])
            self.s_units[i].initcolor = self.s_units[i].color
            self.s_units[i].update_me = True

        for i in range(0, self.selector_count):
            self.v_units[i].color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], int(i * self.step))
            self.v_units[i].initcolor = self.v_units[i].color
            self.v_units[i].update_me = True

    def update_colors(self, h=None, s=None, v=None):
        self.update_color_choosers(h, s, v)
        if self.current_funct is not None:
            self.current_funct(self.custom_color_hsv[0], self.custom_color_hsv[1], self.custom_color_hsv[2])
            self.active_selection.set_color(ex.hsv_to_rgb(self.custom_color_hsv[0],
                                                          self.custom_color_hsv[1],
                                                          self.custom_color_hsv[2]))
            self.active_selection.update_me = True
            self.cat_ind.redraw_image()
            self.game_ind.redraw_image()
            self.cat_ind2.redraw_image()
            self.game_ind2.redraw_image()
            self.cat_sample.redraw_image()
            self.game_sample.redraw_image()
            self.selector_frame.perm_outline_color = self.mainloop.cl.info_buttons_col
            self.selector_frame.update_me = True

        self.active_color = ex.hsv_to_rgb(self.custom_color_hsv[0], self.custom_color_hsv[1], self.custom_color_hsv[2])
        self.active_color.append(127)

        if self.active_selection.my_id == 5:
            self.info_ind.change_colors(self.bg_color, None, self.active_color, self.active_color)
            self.mainloop.dialog.load_images()
            self.mainloop.cl.create_colors()
            self.mainloop.info.load_font_colors()
            self.mainloop.info.reload_colors()

        if self.active_selection.my_id == 0:
            for each in self.shape_inds:
                each.change_colors(self.bg_color, None, self.active_color, None)
                each.update_me = True
                each.init_images()

    def set_sliders_color(self):
        h = self.color_sliders[self.active_selection.my_id][0]
        s = self.color_sliders[self.active_selection.my_id][1]
        v = self.color_sliders[self.active_selection.my_id][2]

        self.h_door.set_pos((self.h_door.grid_x, h + 1))
        self.s_door.set_pos((self.s_door.grid_x, s + 1))
        self.v_door.set_pos((self.v_door.grid_x, v + 1))
        self.update_color_choosers(h, s, v)


    def initialize_styles(self):
        if self.mainloop.cl.color_sliders[6][0] == 0:
            self.cat_sample.decor_style = 0
            self.cat_ind.change_image("ico_theme_rb_a.png")
            self.cat_ind2.change_image("ico_theme_rb_n.png")

        elif self.mainloop.cl.color_sliders[6][0] == 1:
            self.cat_sample.decor_style = 1
            self.cat_ind.change_image("ico_theme_rb_n.png")
            self.cat_ind2.change_image("ico_theme_rb_a.png")

        if self.mainloop.cl.color_sliders[6][1] == 0:
            self.game_sample.decor_style = 0
            self.game_ind.change_image("ico_theme_rb_a.png")
            self.game_ind2.change_image("ico_theme_rb_n.png")
            self.game_ind.completions = [1, 1, 1, 1, 1]
            self.game_ind2.completions = [0, 0, 0, 0, 0]

        elif self.mainloop.cl.color_sliders[6][1] == 1:
            self.game_sample.decor_style = 1
            self.game_ind.change_image("ico_theme_rb_n.png")
            self.game_ind2.change_image("ico_theme_rb_a.png")
            self.game_ind2.completions = [1, 1, 1, 1, 1]
            self.game_ind.completions = [0, 0, 0, 0, 0]


        self.cat_ind.redraw_image()
        self.cat_ind2.redraw_image()
        self.cat_sample.redraw_image()

        self.game_ind.redraw_image()
        self.game_ind2.redraw_image()
        self.game_sample.redraw_image()


    def style_select(self, item):
        if item == self.cat_ind and self.mainloop.cl.color_sliders[6][0] == 1:
            self.cat_sample.decor_style = 0
            self.cat_ind.change_image("ico_theme_rb_a.png")
            self.cat_ind2.change_image("ico_theme_rb_n.png")
            self.cat_ind.redraw_image()
            self.cat_ind2.redraw_image()
            self.cat_sample.redraw_image()
            self.mainloop.cl.color_sliders[6][0] = 0

        elif item == self.cat_ind2 and self.mainloop.cl.color_sliders[6][0] == 0:
            self.cat_sample.decor_style = 1
            self.cat_ind.change_image("ico_theme_rb_n.png")
            self.cat_ind2.change_image("ico_theme_rb_a.png")
            self.cat_ind.redraw_image()
            self.cat_ind2.redraw_image()
            self.cat_sample.redraw_image()
            self.mainloop.cl.color_sliders[6][0] = 1

        elif item == self.game_ind and self.mainloop.cl.color_sliders[6][1] == 1:
            self.game_sample.decor_style = 0
            self.game_ind.change_image("ico_theme_rb_a.png")
            self.game_ind2.change_image("ico_theme_rb_n.png")
            self.game_ind.completions = [1,1,1,1,1]
            self.game_ind2.completions = [0,0,0,0,0]
            self.game_ind.redraw_image()
            self.game_ind2.redraw_image()
            self.game_sample.redraw_image()
            self.mainloop.cl.color_sliders[6][1] = 0

        elif item == self.game_ind2 and self.mainloop.cl.color_sliders[6][1] == 0:
            self.game_sample.decor_style = 1
            self.game_ind.change_image("ico_theme_rb_n.png")
            self.game_ind2.change_image("ico_theme_rb_a.png")
            self.game_ind2.completions = [1,1,1,1,1]
            self.game_ind.completions = [0,0,0,0,0]
            self.game_ind.redraw_image()
            self.game_ind2.redraw_image()
            self.game_sample.redraw_image()
            self.mainloop.cl.color_sliders[6][1] = 1

    def shape_select(self, item):
        for i in range(4):
            if item == self.shape_inds[i]:
                self.shape_inds[i].resize_unit(2, 2)
                #self.shape_inds[i].set_grid_pos(self.shape_loc2[i][0], self.shape_loc2[i][1])
                self.shape_inds[i].fg_img_src = "shape_radio_btn.png"
                self.shape_inds[i].init_images()
                self.shape_inds[i].update_me = True
                self.mainloop.cl.color_sliders[6][2] = i
            else:
                self.shape_inds[i].resize_unit(2, 2)
                #self.shape_inds[i].set_grid_pos(self.shape_loc1[i][0], self.shape_loc1[i][1])
                self.shape_inds[i].fg_img_src = None
                self.shape_inds[i].init_images()
                self.shape_inds[i].update_me = True

        self.cat_ind.redraw_image()
        self.cat_ind2.redraw_image()
        self.cat_sample.redraw_image()

    def reset_colors(self, args=None):
        self.mainloop.cl.reset_colors(save=True)
        self.mainloop.cl.create_colors()
        self.shape_select(self.shape_inds[0])
        self.mainloop.info.load_font_colors()
        self.mainloop.info.reload_colors()
        self.mainloop.dialog.load_images()
        self.mainloop.db.save_user_colors()
        #recreate game to reset all items
        self.create_game_objects()

    def get_image(self, current_image, active=False):
        if active and current_image[-5] == "n":
            return current_image[:-5] + "a.png"
        elif not active and current_image[-5] == "a":
            return current_image[:-5] + "n.png"
        else:
            return current_image

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEMOTION:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            found = False
            for each in self.menu_inds:
                if (each.rect.left < pos[0] < each.rect.right and each.rect.top < pos[1] < each.rect.bottom):
                    if each != self.unit_mouse_over:
                        if self.unit_mouse_over is not None:
                            self.unit_mouse_over.mouse_out()
                        self.unit_mouse_over = each
                    found = True
                    each.handle(event)
                    break
            if self.info_ind.rect.left < pos[0] < self.info_ind.rect.right and self.info_ind.rect.top < pos[1] < self.info_ind.rect.bottom:
                if self.info_ind != self.unit_mouse_over:
                    if self.unit_mouse_over is not None:
                        self.unit_mouse_over.mouse_out()
                    self.unit_mouse_over = self.info_ind
                    self.info_ind.handle(event)
                found = True

            if not found:
                if self.unit_mouse_over is not None:
                    self.unit_mouse_over.mouse_out()
                self.unit_mouse_over = None

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            active = self.board.active_ship
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            found = False
            if self.info_ind.rect.left < pos[0] < self.info_ind.rect.right and self.info_ind.rect.top < pos[1] < self.info_ind.rect.bottom:
                self.mainloop.dialog.show_dialog(2, self.mainloop.lang.d["Reset colors back to default?"],
                                                 self.reset_colors, fc=None, bg_type=0, decor_type=0)
                found = True
            for each in self.menu_inds:
                if each.rect.left < pos[0] < each.rect.right and each.rect.top < pos[1] < each.rect.bottom:
                    self.style_select(each)
                    self.mainloop.db.save_user_colors()
                    found = True
                    break
            if not found:
                for each in self.shape_inds:
                    if each.rect.left < pos[0] < each.rect.right and each.rect.top < pos[1] < each.rect.bottom:
                        self.shape_select(each)
                        self.mainloop.db.save_user_colors()
                        found = True
                        break
            if found:
                self.mainloop.redraw_needed[0] = True

            if not found and active > -1:
                if self.board.ships[active] in self.sections:
                    self.current_funct = self.functions[self.board.ships[active].my_id]
                    self.active_selection = self.sections[self.board.ships[active].my_id]
                    img = self.get_image(self.active_selection.img_src, active=True)
                    self.active_selection.change_image(img)

                    self.active_selection.set_outline(self.bg_color, 2)
                    if self.prev_selection is not None and self.prev_selection != self.active_selection:
                        self.prev_selection.set_outline(self.bg_color, self.border_width)
                        img = self.get_image(self.prev_selection.img_src, active=False)
                        self.prev_selection.change_image(img)
                        self.prev_selection.update_me = True
                    self.prev_selection = self.active_selection
                    self.set_sliders_color()

                    if self.active_selection.my_id == 4:
                        self.s_door.perm_outline_color = (100, 100, 100)
                        self.v_door.perm_outline_color = (100, 100, 100)
                        self.s_door.update_me = True
                        self.v_door.update_me = True
                    else:
                        self.s_door.perm_outline_color = (200, 0, 0)
                        self.v_door.perm_outline_color = (200, 0, 0)
                        self.s_door.update_me = True
                        self.v_door.update_me = True
                    self.active_selection.update_me = True
                    self.mainloop.redraw_needed[0] = True

                elif self.board.ships[active] in self.h_units:
                    self.h_door.set_pos(self.board.active_ship_pos)
                    c = active - self.h_units[0].unit_id
                    self.color_sliders[self.active_selection.my_id][0] = c
                    self.update_colors(c, None, None)
                    self.mainloop.redraw_needed[0] = True
                    self.mainloop.db.save_user_colors()
                elif self.board.ships[active] in self.s_units:
                    if self.active_selection.my_id != 4:
                        self.s_door.set_pos(self.board.active_ship_pos)
                        c = active - self.s_units[0].unit_id
                        self.color_sliders[self.active_selection.my_id][1] = c
                        self.update_colors(None, c, None)
                        self.mainloop.redraw_needed[0] = True
                        self.mainloop.db.save_user_colors()
                elif self.board.ships[active] in self.v_units:
                    if self.active_selection.my_id != 4:
                        self.v_door.set_pos(self.board.active_ship_pos)
                        c = active - self.v_units[0].unit_id
                        self.color_sliders[self.active_selection.my_id][2] = c
                        self.update_colors(None, None, c)
                        self.mainloop.redraw_needed[0] = True
                        self.mainloop.db.save_user_colors()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)
