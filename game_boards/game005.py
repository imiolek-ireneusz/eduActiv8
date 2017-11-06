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
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = 100  # random.randrange(150, 190, 5)
        v = 255  # random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)
        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        font_color = ex.hsv_to_rgb(h, 255, 140)

        # data = [x_count, y_count, number_count, bottom_limit, top_limit, ordered, font_size]
        data = [11, 6]
        data.extend(self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group, self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)

        self.data = data

        self.board.set_animation_constraints(0, data[0], 0, data[1] - 1)
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.num_list = []

        if data[5] == True:
            index = random.randrange(data[3], data[4]-data[2]+2)
            n = 0
            for i in range(data[2]):
                self.num_list.append(index + n)
                n += 1
        else:
            while len(self.num_list) < data[2]:
                num = random.randint(data[3], data[4])
                if num not in self.num_list:
                    self.num_list.append(num)
        shuffled = self.num_list[:]
        self.ordered = sorted(self.num_list[:])
        random.shuffle(shuffled)

        color = ((255, 255, 255))

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]

        # find position of first door square
        # x = (data[0] - data[2]) // 2
        self.left_offset = (data[0] - data[2]) // 2

        # add objects to the board
        for i in range(data[2]):
            self.board.add_door(self.left_offset + i, 0, 1, 1, classes.board.Door, "", color, "")
            self.board.units[i].door_outline = True
            h = random.randrange(0, 255, 5)
            y = random.randrange(1, 5)
            number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            caption = str(shuffled[i])
            self.board.add_unit(self.left_offset + i, y, 1, 1, classes.board.Letter, caption, number_color, "", data[6])
            self.board.ships[-1].font_color = ex.hsv_to_rgb(h, 255, 140)
            self.solution_grid[self.left_offset + i] = 1
            self.board.ships[-1].readable = False

            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()

        for each in self.board.units:
            self.board.all_sprites_list.move_to_front(each)

        instruction = self.d["Re-arrange ascending"]
        self.board.add_unit(0, 5, 11, 1, classes.board.Letter, instruction, color0, "", 7)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.board.ships[-1].speaker_val = self.dp["Re-arrange ascending"]
        self.board.ships[-1].speaker_val_update = False
        self.outline_all(0, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.check_result()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check_reset(self):
        for each in self.board.ships:
            each.update_me = True
            each.set_display_check(None)

    def auto_check(self):
        if self.board.grid[0] == self.solution_grid:
            for i in range(self.data[2]):
                if self.ordered[self.board.ships[i].grid_x - self.left_offset] == int(self.board.ships[i].value):
                    self.board.ships[i].set_display_check(True)
                else:
                    self.board.ships[i].set_display_check(False)

    def check_result(self):
        if self.board.grid[0] == self.solution_grid:
            correct = True
            for i in range(self.data[2]):
                if self.ordered[self.board.ships[i].grid_x - self.left_offset] != int(self.board.ships[i].value):
                    correct = False
                    break

            if correct:
                self.auto_check()
                self.level.next_board()
            else:
                self.auto_check()
        self.mainloop.redraw_needed[0] = True
