# -*- coding: utf-8 -*-

import os
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 5)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 9)

    def create_game_objects(self, level=1):
        self.board.decolorable = False
        self.board.draw_grid = True

        color = ex.hsv_to_rgb(225, 15, 235)
        self.col_bg = (180, 180, 180)
        if self.mainloop.scheme is None or not self.mainloop.scheme.dark:
            self.red_color = (220, 220, 255)
            self.green_color = (220, 255, 220)
            self.blue_color = (255, 255, 220)
            self.red_color2 = (0, 0, 255)
            self.green_color2 = (0, 255, 0)
            self.blue_color2 = (255, 255, 0)
            font_color = (0, 0, 0)
        else:
            self.red_color = (0, 0, 55)
            self.green_color = (0, 55, 0)
            self.blue_color = (55, 55, 0)
            self.red_color2 = (0, 0, 155)
            self.green_color2 = (0, 155, 0)
            self.blue_color2 = (155, 155, 0)
            font_color = (255, 255, 255)
            self.col_bg = (50, 50, 50)
        self.turn = 1
        if self.level.lvl == 1:
            data = [10, 12, 2]
        elif self.level.lvl == 2:
            data = [10, 14, 2]
        elif self.level.lvl == 3:
            data = [10, 16, 1]
        elif self.level.lvl == 4:
            data = [10, 18, 0]
        elif self.level.lvl == 5:
            data = [10, 20, 0]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count > 10:
            data[0] = x_count

        self.data = data
        self.scores = [0, 0, 0]
        self.score_board = []
        self.imgs = []
        self.moves_taken = 0
        self.max_moves = self.data[0] * (self.data[1] - 3)
        self.game_state = [[0 for x in range(0, data[1])] for y in range(0, data[0])]
        self.lookaround = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]

        self.vis_buttons = [0, 1, 1, 1, 1, 1, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        # player label
        self.board.add_unit(1, 0, data[0] - 6, 1, classes.board.Letter, self.d["Player"] + " 1", self.red_color2, "",
                            self.data[2])
        self.board.add_unit(1, 1, data[0] - 6, 1, classes.board.Letter, self.d["Player"] + " 2", self.green_color, "",
                            self.data[2])
        self.board.add_unit(1, 2, data[0] - 6, 1, classes.board.Letter, self.d["Player"] + " 3", self.blue_color, "",
                            self.data[2])
        self.board.board_bg.line_color = self.col_bg
        scheme = "white"
        if self.mainloop.scheme is not None:
            self.board.board_bg.line_color = self.col_bg
            if self.mainloop.scheme.dark:
                scheme = "black"
                self.board.board_bg.line_color = (200, 200, 200)
        self.board.board_bg.update_me = True

        ttx = os.path.join("schemes", scheme, "tictactoe_x.png")
        tto = os.path.join("schemes", scheme, "tictactoe_o.png")
        tts = os.path.join("schemes", scheme, "tictactoe_s.png")
        ttx2 = os.path.join("schemes", scheme, "tictactoe_x2.png")
        tto2 = os.path.join("schemes", scheme, "tictactoe_o2.png")
        tts2 = os.path.join("schemes", scheme, "tictactoe_s2.png")
        ttv = os.path.join("schemes", scheme, "tictactoe_v.png")
        ttyx = os.path.join("schemes", scheme, "tictactoe_y.png")

        # player colour label
        self.board.add_unit(data[0] - 5, 0, 1, 1, classes.board.ImgShip, "x", self.red_color, ttx, 0)
        self.imgs.append(self.board.ships[-1].img.copy())

        self.board.add_unit(data[0] - 5, 1, 1, 1, classes.board.ImgShip, "o", self.green_color, tto, 0)
        self.imgs.append(self.board.ships[-1].img.copy())

        self.board.add_unit(data[0] - 5, 2, 1, 1, classes.board.ImgShip, "s", self.blue_color, tts, 0)
        self.imgs.append(self.board.ships[-1].img.copy())

        self.board.add_unit(data[0] - 4, 0, 1, 1, classes.board.ImgShip, "x", self.red_color, ttx2, 0)
        self.imgs.append(self.board.ships[-1].img.copy())

        self.board.add_unit(data[0] - 4, 1, 1, 1, classes.board.ImgShip, "o", self.green_color, tto2, 0)
        self.imgs.append(self.board.ships[-1].img.copy())

        self.board.add_unit(data[0] - 4, 2, 1, 1, classes.board.ImgShip, "s", self.blue_color, tts2, 0)
        self.imgs.append(self.board.ships[-1].img.copy())

        # score counters
        self.board.add_unit(data[0] - 3, 0, 3, 1, classes.board.Letter, str(self.scores[0]), self.red_color, "", 0)
        self.score_board.append(self.board.ships[-1])

        self.board.add_unit(data[0] - 3, 1, 3, 1, classes.board.Letter, str(self.scores[1]), self.green_color, "", 0)
        self.score_board.append(self.board.ships[-1])

        self.board.add_unit(data[0] - 3, 2, 3, 1, classes.board.Letter, str(self.scores[1]), self.blue_color, "", 0)
        self.score_board.append(self.board.ships[-1])

        # indicator
        self.board.add_unit(0, 0, 1, 1, classes.board.ImgShip, "", self.red_color, ttv, 0)
        self.ind = self.board.ships[-1]

        self.legend_count = len(self.board.ships)
        for k in range(self.legend_count):
            self.board.ships[k].immobilize()
            self.board.ships[k].readable = False
            self.board.ships[k].outline = False

        k = self.legend_count
        for j in range(3, data[1]):
            for i in range(data[0]):
                self.board.add_unit(i, j, 1, 1, classes.board.ImgShip, "", color, ttyx, 0)
                self.board.ships[k].immobilize();
                self.board.ships[k].readable = False
                self.board.ships[k].outline = False
                k += 1

        for each in self.board.ships:
            each.font_color = font_color

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.show_msg == False:
            if self.board.active_ship >= self.legend_count:
                active = self.board.ships[self.board.active_ship]
                if len(active.value) == 0:
                    if self.turn == 1:
                        active.initcolor = self.red_color
                        active.value = "x"
                        active.img = self.imgs[0].copy()
                        self.game_state[active.grid_x][active.grid_y] = 1
                        self.board._place_unit(self.ind.unit_id, (0, 1))
                        self.look_around(active)
                        self.move_taken(active)
                        self.turn = 2
                        self.board.ships[0].color = self.red_color
                        self.board.ships[1].color = self.green_color2
                        self.board.ships[2].color = self.blue_color
                    elif self.turn == 2:
                        active.initcolor = self.green_color
                        active.value = "o"
                        active.img = self.imgs[1].copy()
                        self.game_state[active.grid_x][active.grid_y] = 2
                        self.board._place_unit(self.ind.unit_id, (0, 2))
                        self.look_around(active)
                        self.move_taken(active)
                        self.turn = 3
                        self.board.ships[0].color = self.red_color
                        self.board.ships[1].color = self.green_color
                        self.board.ships[2].color = self.blue_color2
                    elif self.turn == 3:
                        active.initcolor = self.blue_color
                        active.value = "s"
                        active.img = self.imgs[2].copy()
                        self.game_state[active.grid_x][active.grid_y] = 3
                        self.board._place_unit(self.ind.unit_id, (0, 0))
                        self.look_around(active)
                        self.move_taken(active)
                        self.turn = 1
                        self.board.ships[0].color = self.red_color2
                        self.board.ships[1].color = self.green_color
                        self.board.ships[2].color = self.blue_color

                    self.board.ships[0].update_me = True
                    self.board.ships[1].update_me = True
                    self.board.ships[2].update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def move_taken(self, active):
        self.moves_taken += 1
        if self.moves_taken == self.max_moves:
            if self.scores[0] == self.scores[1] == self.scores[2]:
                self.board.ships[0].value += " " + self.d["Game Draw"]
                self.board.ships[1].value += " " + self.d["Game Draw"]
                self.board.ships[2].value += " " + self.d["Game Draw"]
            else:
                if self.scores[0] >= self.scores[1] and self.scores[0] >= self.scores[2]:
                    # Player1 - Winner
                    self.board.ships[0].value += " " + self.d["Won"]
                if self.scores[1] >= self.scores[0] and self.scores[1] >= self.scores[2]:
                    # Player1 - Winner
                    self.board.ships[1].value += " " + self.d["Won"]
                if self.scores[2] >= self.scores[0] and self.scores[2] >= self.scores[1]:
                    # Player1 - Winner
                    self.board.ships[2].value += " " + self.d["Won"]

            self.board.ships[0].update_me = True
            self.board.ships[1].update_me = True
            self.board.ships[2].update_me = True

    def look_around(self, active):
        matched = []
        for i in range(8):
            first_pos = [active.grid_x + self.lookaround[i][0], active.grid_y + self.lookaround[i][1]]
            if 0 <= first_pos[0] < self.board.x_count and 2 <= first_pos[1] < self.board.y_count:
                first_neigh = self.game_state[first_pos[0]][first_pos[1]]
                if first_neigh == self.turn:
                    # fix number of points given to each player for multiple lines
                    second_pos = [active.grid_x + self.lookaround[i][0] + self.lookaround[i][0],
                                  active.grid_y + self.lookaround[i][1] + self.lookaround[i][1]]
                    if 0 <= second_pos[0] < self.board.x_count and 2 <= second_pos[1] < self.board.y_count:
                        second_neigh = self.game_state[second_pos[0]][second_pos[1]]
                        if second_neigh == self.turn:
                            matched.append(first_pos)
                            matched.append(second_pos)

                            # check further in that direction
                    opposite_pos = [active.grid_x - self.lookaround[i][0], active.grid_y - self.lookaround[i][1]]
                    if 0 <= opposite_pos[0] < self.board.x_count and 2 <= opposite_pos[1] < self.board.y_count:
                        opposite_neigh = self.game_state[opposite_pos[0]][opposite_pos[1]]
                        if opposite_neigh == self.turn:
                            # check in the oposite direction
                            matched.append(first_pos)
                            matched.append(opposite_pos)
        matched_count = len(matched)
        if matched_count > 0:
            matched.append([active.grid_x, active.grid_y])
        matched_set = set()
        for each in matched:
            matched_set.add(tuple(each))
            self.game_state[each[0]][each[1]] = 0
            ship_id = (each[0] + (each[1] - 3) * self.data[0]) + self.legend_count
            self.board.ships[ship_id].value = " "
            self.board.ships[ship_id].img = self.imgs[self.turn + 2].copy()
            self.board.ships[ship_id].update_me = True
        self.scores[self.turn - 1] += len(matched_set)
        self.score_board[0].value = str(self.scores[0])
        self.score_board[0].update_me = True
        self.score_board[1].value = str(self.scores[1])
        self.score_board[1].update_me = True
        self.score_board[2].value = str(self.scores[2])
        self.score_board[2].update_me = True

    def check_result(self):
        pass
