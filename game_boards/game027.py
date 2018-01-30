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
        #self.level = lc.Level(self, mainloop, 5, 10)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 20, 10)

    def create_game_objects(self, level=1):
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 0, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        # create non-movable objects
        self.board.draw_grid = False
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
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

        shelf_len = 7
        # basket
        basket_w = data[0] - shelf_len - 1
        self.board.add_door(data[0] - basket_w, data[1] - 5, basket_w, 5, classes.board.Door, "", white, "")
        self.board.units[0].door_outline = True
        # basket image - 260 x 220
        img_bg_col = white
        scheme = "white"
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                scheme = "black"
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
        self.count_units = []
        for each in self.singular_items:
            caption = self.lang._n(each, 1)
            if not self.lang.ltr_text:
                caption = ex.reverse(self.lang._n(each, 1), self.lang.alpha, self.lang.lang)
                # caption = self.lang._n(each, 1)
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
                caption = ex.reverse(caption, self.lang.alpha, self.lang.lang)
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

        # put stuff on shelves:
        for i in range(len(items)):
            image = os.path.join("fr", items[i] + f_end)

            for j in range(0, shelf_len):
                self.board.add_unit(j, i, 1, 1, classes.board.ImgShip, self.img_captions[i], (0, 0, 0, 0), image,
                                    data[4], alpha=True)
                self.board.ships[-1].audible = False
                self.board.ships[-1].speaker_val = self.img_pcaptions[i]
                self.board.ships[-1].speaker_val_update = False
                self.board.ships[-1].outline = False
        self.board.all_sprites_list.move_to_front(self.board.units[0])
        """
        instruction = self.d["Check the shopping list"]
        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, color0, "", 3)
        self.board.ships[-1].set_outline(0, 1)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.board.ships[-1].speaker_val = self.dp["Check the shopping list"]
        self.board.ships[-1].speaker_val_update = False
        """

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Check the shopping list"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            #if event.pos[1] > self.layout.info_bar_h + self.layout.score_bar_h:

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

    def auto_check_reset(self):
        for i in range(self.data[2]):
            self.board.units[self.count_units[i]-1].set_display_check(None)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        # checking what sprites collide with the basket sprite
        purchased = pygame.sprite.spritecollide(self.board.units[0], self.board.ship_list, False, collided=None)
        result = {}
        # count each item and check if they are the items from the shopping list
        for i in range(len(self.items)):
            count = 0
            for each in purchased:
                if each.value == self.img_captions[i]:  # self.items[i]:
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
