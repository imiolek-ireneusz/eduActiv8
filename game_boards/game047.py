# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
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
        s = 70
        v = 230
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 40, 230)
        font_color = ex.hsv_to_rgb(h, 255, 140)

        data = [11, 3]
        data.extend(self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group, self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group)

        self.data = data
        self.board.set_animation_constraints(0, data[0], 0, data[1])
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
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
        #for i in range(self.alph_len - data[2]):
        #    self.positions.append((i, 0))

        if data[3] == True:
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
        color = (255, 255, 255)

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]

        # find position of first door square
        x = (data[0] - data[2]) // 2

        self.positions = []
        for i in range(data[2]):
            self.positionsd[self.indexes[i]] = i
            self.positions.append([x + i, 0])

        # add objects to the board
        for i in range(data[2]):
            self.board.add_door(x + i, 0, 1, 1, classes.board.Door, "", color, "")
            self.board.units[i].door_outline = True
            y = random.randrange(1, data[1])
            number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            caption = self.alphabet[shuffled[i]]
            self.board.add_unit(x + i, y, 1, 1, classes.board.Letter, caption, number_color, "", data[4])
            self.board.ships[-1].font_color = font_color
            # self.board.ships[i].highlight = False
            self.board.ships[i].outline_highlight = True
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
            self.board.ships[i].home_location = [x + self.positionsd[shuffled[i]], 0]
            self.solution_grid[x + i] = 1

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)

        """
        instruction = self.d["Re-arrange alphabetical"]
        self.board.add_unit(0, 5, 11, 1, classes.board.Letter, instruction, color0, "", 7)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.board.ships[-1].speaker_val = self.dp["Re-arrange alphabetical"]
        self.board.ships[-1].speaker_val_update = False
        """
        self.outline_all(0, 1)

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Re-arrange alphabetical"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            if True:  # self.data[5] == 1:
                self.auto_check()
            self.check_result()

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
        gd.BoardGame.update(self, game)  # rest of painting done by parent

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
                    if ships_sorted[i][1] != self.alphabet[self.indexes[i]]:
                        correct = False
            if correct == True:
                self.auto_check()
                self.level.next_board()
            else:
                self.auto_check()
        else:
            self.auto_check_reset()
