# -*- coding: utf-8 -*-

import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 5, 9)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 14, 5)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [1, 1, 1, 1, 1, 1, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        s = 100  # random.randrange(150, 190, 5)
        v = 255  # random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)

        color0 = ex.hsv_to_rgb(h, 40, 230)  # highlight 1
        font_color = ex.hsv_to_rgb(h, 255, 140)
        white = [255, 255, 255]

        # data = [x_count, y_count, number_count, top_limit, ordered]
        if self.level.lvl == 1:
            data = [14, 5, 10, 10, 1]
        elif self.level.lvl == 2:
            data = [14, 5, 10, 20, 2]
        elif self.level.lvl == 3:
            data = [14, 5, 10, 99, 2]
        elif self.level.lvl == 4:
            data = [14, 5, 15, 20, 2]
        elif self.level.lvl == 5:
            data = [14, 5, 15, 50, 2]
        elif self.level.lvl == 6:
            data = [14, 5, 15, 99, 2]
        elif self.level.lvl == 7:
            data = [14, 5, 20, 30, 2]
        elif self.level.lvl == 8:
            data = [14, 5, 20, 50, 2]
        elif self.level.lvl == 9:
            data = [14, 5, 20, 99, 2]
        self.chapters = [1, 4, 7, 9]
        self.points = data[2] // 5
        self.data = data

        self.board.set_animation_constraints(4, data[0], 0, data[1] - 1)
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.num_list = []

        choice_list = [x for x in range(1, data[3] + 1)]
        for i in range(data[2]):
            index = random.randrange(0, len(choice_list))
            self.num_list.append(choice_list[index])
            del (choice_list[index])

        # find position of first door square
        x = data[0] - 1  # (data[0]-data[2])//2
        y = data[1] - 2
        # add objects to the board
        for i in range(data[2]):
            h = random.randrange(0, 255, 5)
            number_color = ex.hsv_to_rgb(h, s, v)  # highlight 1
            caption = str(self.num_list[i])
            self.board.add_unit(x, y, 1, 1, classes.board.Letter, caption, number_color, "", data[4])
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

        instruction = self.d["Find and separate"]
        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, color0, "", 7)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = font_color

        self.board.ships[-1].speaker_val = self.dp["Find and separate"]
        self.board.ships[-1].speaker_val_update = False
        self.outline_all(0, 1)
        self.board.all_sprites_list.move_to_front(self.board.units[-1])

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        correct = True
        for i in range(len(self.board.ships) - 3):
            each = self.board.ships[i]
            if each.grid_y < 2 and self.num_list[each.unit_id] % 2 != 0 \
                    or each.grid_y > 1 and self.num_list[each.unit_id] % 2 == 0:
                correct = False
        if correct == True:
            # self.update_score(self.points)
            self.level.next_board()
        else:
            if self.points > 0:
                self.points -= 1
            self.level.try_again()
