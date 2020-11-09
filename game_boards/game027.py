# -*- coding: utf-8 -*-

import os
import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 20, 10)

    def create_game_objects(self, level=1):
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        # create non-movable objects
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        font_color = ex.hsv_to_rgb(h, 255, 140)
        white = (255, 255, 255)

        # data = [x_count, y_count, number of items on the list, top_quantity, font-size]
        data = [20, 13]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        # rescale the number of squares horizontally to better match the screen width
        x_count = self.get_x_count(data[1], even=None)
        if x_count > 20:
            data[0] = x_count

        self.data = data

        self.board.set_animation_constraints(0, data[0], 0, data[1])

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.unit_mouse_over = None
        self.units = []

        shelf_len = 7
        # basket
        basket_w = data[0] - shelf_len - 1
        self.board.add_door(data[0] - basket_w, data[1] - 5, basket_w, 5, classes.board.Door, "", white, "")
        self.board.units[0].door_outline = True
        # basket image - 260 x 220
        img_bg_col = white
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                img_bg_col = (0, 0, 0)
        img_src = "basket.png"
        self.board.add_door(data[0] - 6, data[1] - 5, 6, 5, classes.board.Door, "", img_bg_col, img_src, door_alpha=True)
        self.board.units[-1].is_door = False

        self.board.add_unit(data[0] - 7, 0, 7, 1, classes.board.Label, self.d["Shopping List"], white, "", data[4] + 1)
        self.board.units[-1].font_color = font_color
        f_end = ".png"
        items = ["fr_apple1", "fr_apple2", "fr_strawberry", "fr_pear", "fr_orange", "fr_onion", "fr_tomato", "fr_lemon",
                 "fr_cherry", "fr_pepper", "fr_carrot", "fr_banana", "fr_wmelon"]
        self.items = items
        self.img_captions = []
        self.singular_items = ["green apple", "red apple", "strawberry", "pear", "orange [fruit]", "onion", "tomato",
                               "lemon", "cherry", "pepper", "carrot", "banana", "watermelon"]

        #h_list = [15, 61, 5, 44, 17, 23, 9, 42, 253, 2, 17, 35, 60]

        self.count_units = []
        for each in self.singular_items:
            caption = self.lang._n(each, 1)
            if not self.lang.ltr_text:
                caption = ex.reverse(self.lang._n(each, 1), self.lang.lang)
            if caption is None:
                caption = ""
            self.img_captions.append(caption)

        if self.lang.lang in ["ru", "he"]:
            self.img_pcaptions = []
            si = self.lang.dp["fruit"]
            for each in si:
                pcaption = self.lang._n(each, 1)
                if pcaption is None:
                    pcaption = ""
                self.img_pcaptions.append(pcaption)
        else:
            self.img_pcaptions = self.img_captions

        item_indexes = [x for x in range(len(items))]
        self.chosen_items = [[], []]
        self.solution = {}
        # pick items and quantities
        for i in range(data[2]):
            index = random.randrange(0, len(item_indexes))
            self.chosen_items[0].append(item_indexes[index])
            quantity = random.randrange(1, data[3] + 1)
            self.chosen_items[1].append(quantity)
            self.solution[str(item_indexes[index])] = quantity
            del (item_indexes[index])

        if self.lang.ltr_text:
            l = [data[0] - 7, data[0] - 6, data[0] - 5]
        else:
            l = [data[0] - 1, data[0] - 2, data[0] - 7]
        # create shopping list
        for i in range(data[2]):
            ind = self.chosen_items[0][i]
            caption = self.lang._n(self.singular_items[ind], self.chosen_items[1][i])
            if not self.lang.ltr_text:
                caption = ex.reverse(caption, self.lang.lang)
            if caption is None:
                caption = ""
            self.board.add_unit(l[0], i + 1, 1, 1, classes.board.Label, str(self.chosen_items[1][i]) + " ", white, "",
                                data[4])
            self.board.units[-1].font_color = font_color
            self.board.units[-1].checkable = True
            self.board.units[-1].init_check_images(1, 1.5)
            self.count_units.append(len(self.board.units))
            self.board.add_unit(l[1], i + 1, 1, 1, classes.board.ImgShip, "", (0, 0, 0, 0),
                                os.path.join("fr", items[ind] + f_end), data[4], alpha=True)
            self.board.add_unit(l[2], i + 1, 5, 1, classes.board.Label, caption, white, "", data[4])
            self.board.units[-1].font_color = font_color
            self.board.ships[i].immobilize()
            self.board.ships[i].outline = False
            if self.lang.ltr_text:
                self.board.units[-1].align = 1
            else:
                self.board.units[-1].align = 2
        # rearange z-order of red outlines (shopping list and basket)
        for i in range(2):
            self.board.all_sprites_list.move_to_front(self.board.units[i])

        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "dc_hover_wb.png")
        else:
            if self.mainloop.scheme.dark:
                dc_img_src = os.path.join('unit_bg', "dc_hover_bw.png")
            else:
                dc_img_src = os.path.join('unit_bg', "dc_hover_wb.png")

        dc_tint_color = ex.hsv_to_rgb(253, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        # put stuff on shelves:
        for i in range(len(items)):
            image = os.path.join("fr", items[i] + f_end)

            for j in range(0, shelf_len):
                self.board.add_universal_unit(grid_x=j, grid_y=i, grid_w=1, grid_h=1, txt=self.img_captions[i],
                                              fg_img_src=None, bg_img_src=image, dc_img_src=dc_img_src,
                                              bg_color=(0, 0, 0, 0), border_color=None, font_color=None,
                                              bg_tint_color=None, fg_tint_color=None, dc_tint_color=dc_tint_color,
                                              txt_align=(0, 0), font_type=0, multi_color=False, alpha=True,
                                              immobilized=False, dc_as_hover=True, mode=0)
                self.board.ships[-1].audible = False
                self.board.ships[-1].speaker_val = self.img_pcaptions[i]
                self.board.ships[-1].speaker_val_update = False
                self.board.ships[-1].item_code = items[i]
                self.units.append(self.board.ships[-1])
        self.board.all_sprites_list.move_to_front(self.board.units[0])

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Check the shopping list"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def auto_check_reset(self):
        for i in range(self.data[2]):
            self.board.units[self.count_units[i]-1].set_display_check(None)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        # checking what sprites collide with the basket sprite
        purchased = pygame.sprite.spritecollide(self.board.units[0], self.board.ship_list, False, collided=None)
        result = {}
        # count each item and check if they are the items from the shopping list
        for i in range(len(self.items)):
            count = 0
            for each in purchased:
                if each.item_code == self.items[i]:
                    count += 1
            if count > 0:
                result[str(i)] = count
        for i in range(self.data[2]):
            if str(self.chosen_items[0][i]) in result and str(self.chosen_items[0][i]) in self.solution:
                if result[str(self.chosen_items[0][i])] == self.solution[str(self.chosen_items[0][i])]:
                    self.board.units[self.count_units[i]-1].set_display_check(True)
                else:
                    self.board.units[self.count_units[i]-1].set_display_check(False)
            else:
                self.board.units[self.count_units[i]-1].set_display_check(False)

        if result == self.solution:
            self.level.next_board()

        self.mainloop.redraw_needed[0] = True
