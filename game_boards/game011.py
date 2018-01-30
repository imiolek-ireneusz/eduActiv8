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
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 14, 5)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 0, 1, 1, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = 100
        v = 255
        h = random.randrange(0, 255, 5)

        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        font_color = ex.hsv_to_rgb(h, 255, 140)
        white = [255, 255, 255]

        data = [14, 4]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid, 
                                                            self.mainloop.config.user_age_group)

        self.points = data[2] // 5
        self.data = data

        self.board.set_animation_constraints(4, data[0], 0, data[1])
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.num_list = []

        while len(self.num_list) < data[2]:
            num = random.randint(data[3], data[4])
            if num not in self.num_list:
                self.num_list.append(num)

        # find position of first door square
        x = data[0] - 1
        y = data[1] - 1
        # add objects to the board
        for i in range(data[2]):
            h = random.randrange(0, 255, 5)
            number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            caption = str(self.num_list[i])
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, caption, number_color, "", data[5])

            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()
            self.board.ships[-1].readable = False
            self.board.ships[-1].font_color = ex.hsv_to_rgb(h, 255, 140)
            x -= 1
            if x <= 3:
                x = data[0] - 1
                y -= 1
        self.board.add_unit(0, 0, 4, 2, classes.board.Letter, self.d["Even"], color0, "", 1)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.board.add_unit(0, 2, 4, 2, classes.board.Letter, self.d["Odd"], color0, "", 1)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color
        self.board.add_door(4, 0, data[0] - 4, 2, classes.board.Door, "", white, "")
        self.board.units[-1].door_outline = True

        self.board.add_door(4, 2, data[0] - 4, 2, classes.board.Door, "", white, "")
        self.board.units[-1].door_outline = True

        """
        instruction = self.d["Find and separate"]
        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, color0, "", 7)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color

        self.board.ships[-1].speaker_val = self.dp["Find and separate"]
        self.board.ships[-1].speaker_val_update = False
        """
        self.outline_all(0, 1)
        self.board.all_sprites_list.move_to_front(self.board.units[-1])

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Find and separate"])

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()

    def auto_check_reset(self):
        for i in range(len(self.board.ships) - 3):
            self.board.ships[i].set_display_check(None)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        correct = True
        for i in range(len(self.board.ships) - 3):
            if self.board.ships[i].grid_y < 2 and self.num_list[self.board.ships[i].unit_id] % 2 == 0:
                self.board.ships[i].set_display_check(True)
            elif self.board.ships[i].grid_y > 1 and self.num_list[self.board.ships[i].unit_id] % 2 != 0:
                self.board.ships[i].set_display_check(True)
            else:
                self.board.ships[i].set_display_check(False)
                correct = False
        if correct:
            self.level.next_board()

        self.mainloop.redraw_needed[0] = True

