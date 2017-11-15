# -*- coding: utf-8 -*-

import pygame
import random

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
from classes.simple_vector import Vector2


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 2, 12)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 15, 11)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [0, 1, 1, 1, 1, 1, 1, 1, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        # data = [x_count, y_count, square_num, canvas_height, non_vertical, color_difference, games_per_level, mess_drawing_function]

        # setting up game flow / level dificulty
        if self.level.lvl == 1:
            data = [15, 11, 3, 6, 2, 50, 2, self.straight_lines]
        elif self.level.lvl == 2:
            data = [15, 11, 5, 6, 2, 35, 2, self.straight_lines]
        elif self.level.lvl == 3:
            data = [15, 11, 7, 6, 2, 25, 2, self.straight_lines]
        elif self.level.lvl == 4:
            data = [15, 11, 9, 6, 2, 20, 2, self.straight_lines]
        elif self.level.lvl == 5:
            data = [15, 11, 3, 6, 2, 50, 3, self.bezier_lines]
        elif self.level.lvl == 6:
            data = [15, 11, 5, 6, 2, 35, 3, self.bezier_lines]
        elif self.level.lvl == 7:
            data = [15, 11, 7, 6, 2, 25, 3, self.bezier_lines]
        elif self.level.lvl == 8:
            data = [15, 11, 9, 6, 2, 20, 3, self.bezier_lines]
        elif self.level.lvl == 9:
            data = [15, 11, 3, 6, 2, 50, 4, self.bezier2x_lines]
        elif self.level.lvl == 10:
            data = [15, 11, 5, 6, 2, 35, 4, self.bezier2x_lines]
        elif self.level.lvl == 11:
            data = [15, 11, 7, 6, 2, 25, 4, self.bezier2x_lines]
        elif self.level.lvl == 12:
            data = [15, 11, 9, 6, 1, 20, 4, self.bezier2x_lines]

        self.chapters = [1, 5, 9, 12]
        # rescale the number of squares horizontally to better match the screen width
        data[0] = self.get_x_count(data[1], even=False)
        data[3] = data[0] - 4
        self.data = data
        self.board.set_animation_constraints(data[0] - 3, data[0], 0, data[1])

        self.colors = []
        self.level.games_per_lvl = data[6]
        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        s = 20
        v = 255
        h = random.randrange(0, 255)
        self.line_col = (0, 0, 0)
        if self.mainloop.scheme is None:
            color = ex.hsv_to_rgb(h, s, v)
        else:
            color = self.mainloop.scheme.u_color
            if self.mainloop.scheme.dark:
                self.line_col = self.mainloop.scheme.u_font_color

        self.board.add_unit(1, 0, data[0] - 4, data[1], classes.board.Obstacle, "", color)
        self.top_colors = []

        h = random.randrange(0, 75, 1)
        start_from = (data[1] - data[2]) // 2
        end_at = start_from + data[2]
        j = 1
        for i in range(start_from, end_at):
            s = 100
            v = 255
            hx = h + (i - start_from) * data[5]
            color = ex.hsv_to_rgb(hx, s, v)
            color2 = ex.hsv_to_rgb(hx, 255, 200)
            self.colors.append(color2)
            self.board.add_unit(0, i, 1, 1, classes.board.Label, str(j), color, "", 3)
            self.board.units[-1].font_color = ex.hsv_to_rgb(hx, 255, 140)
            self.board.add_unit(data[0] - 1, i, 1, 1, classes.board.Letter, str(j), color, "", 3)
            self.board.ships[-1].font_color = ex.hsv_to_rgb(hx, 255, 140)
            self.board.ships[-1].highlight = False
            self.board.ships[-1].outline_highlight = True
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()

            j += 1
        self.colors_completed = self.colors[:]
        self.outline_all(0, 1)

        self.draw_the_mess(data, start_from, end_at)

        for i in range(data[1]):
            if self.solution_positions[i] == 1:
                self.board.add_door(data[0] - 3, i, 1, 1, classes.board.Door, "", color, "")
                self.board.units[-1].door_outline = True

    def draw_the_mess(self, data, start_from, end_at):
        # set up the beginning and ending positions
        # starting points:
        step = self.board.scale
        self._step = step
        half_st = round(self.board.scale / 2)
        self.possible_positions = []
        self.start_positions = []
        self.end_positions = []
        self.ready_lines = []
        indexes = []
        self.solution = []
        self.solution_colors = []
        self.solution_positions = []
        for i in range(data[1]):
            next_step = [step * data[3] - 1, i * step + half_st]
            self.possible_positions.append(next_step)
            indexes.append(i)
            self.solution_positions.append(0)

        for i in range(start_from, end_at):
            next_step = [0, i * step + half_st]
            self.start_positions.append(next_step)
            # repeat until the difference is larger than 2 steps
            picked = next_step
            while (picked[0] < (next_step[0] + (step * data[4]))) and (picked[0] > (next_step[0] - (step * data[4]))):
                index = random.randrange(0, len(indexes))
                picked = self.possible_positions[indexes[index]]

            self.end_positions.append(picked)
            self.solution.append(indexes[index])
            del (indexes[index])

        # get a list of positions where the squares should be dragged to
        for i in range(0, len(self.solution)):
            self.solution_positions[self.solution[i]] = 1
        self.canvas = pygame.Surface(
            [self.board.units[0].grid_w * self.board.scale, self.board.units[0].grid_h * self.board.scale - 1])
        self.canvas.fill(self.board.units[0].initcolor)

        # create randomized lines
        for i in range(data[2]):
            data[7](data, self.canvas, i)

        # and draw them all at once in a separate loop
        self.draw_lines()

    def draw_lines(self):
        self.canvas.fill(self.board.units[0].initcolor)
        self.swap_colors()

        for i in range(self.data[2]):
            pygame.draw.aalines(self.canvas, self.colors_completed[i], False, self.ready_lines[i])
        self.board.units[0].painting = self.canvas.copy()
        self.board.units[0].update_me = True

    def swap_colors(self):
        for each_item in self.board.ships:
            if each_item.grid_x == self.data[0] - 3 and each_item.grid_y == self.solution[each_item.unit_id]:
                self.colors_completed[each_item.unit_id] = self.colors[each_item.unit_id]
            else:
                self.colors_completed[each_item.unit_id] = self.line_col

    def straight_lines(self, data, canvas, i):
        self.ready_lines.append([self.start_positions[i], self.end_positions[i]])

    def bezier_lines(self, data, canvas, i):
        # points = [[beginning], [beginning_midifier], [end_midifier], [end]]
        # points = [[200, 400], [300, 250], [450, 500], [500, 475]]

        modifiers = [[0, 0], [0, 0]]
        modifiers[0] = [random.randrange(self._step * 2, self._step * data[3]), random.randrange(0, self.layout.game_h)]
        modifiers[1] = [random.randrange(0, self._step * (data[3] - 2)), random.randrange(0, self.layout.game_h)]
        points = [Vector2(self.start_positions[i]), Vector2(modifiers[0]), Vector2(self.end_positions[i]),
                  Vector2(modifiers[1])]
        bezier_points = ex.DrawBezier(points)
        self.ready_lines.append(bezier_points)

    def bezier2x_lines(self, data, canvas, i):
        # points = [[beginning], [beginning_midifier], [end], [end_midifier]]
        # points = [[200, 400], [300, 250], [450, 500], [500, 475]]
        canvas_w = self.layout.game_w - 4 * self._step
        canvas_h = self.layout.game_h  # self._step*data[3]
        bezier = [[[0, 0] for j in range(4)] for j in range(2)]

        # line 1 start
        bezier[0][0] = Vector2(self.start_positions[i])
        bezier[0][1] = Vector2(random.randrange(self._step * 4, canvas_w - self._step),
                               random.randrange(self._step, canvas_h - self._step))  # mod1 #first point modifier

        # line 1 end
        bezier[0][2] = Vector2(random.randrange(self._step * 2, canvas_w - self._step * 2),
                               random.randrange(self._step * 2, canvas_h - self._step * 2))  # first line end
        bezier[0][3] = Vector2(ex.rand_safe_curve(bezier[0][2], canvas_w, canvas_h))

        # line 2 start
        bezier[1][0] = bezier[0][2]
        bezier[1][1] = bezier[0][2] + Vector2(-(Vector2.from_points(bezier[0][2], bezier[0][3])))  # 3rd point modifier

        # line 2 end
        bezier[1][2] = Vector2(self.end_positions[i])  # last point
        bezier[1][3] = Vector2(random.randrange(self._step, canvas_w - self._step * 4),
                               random.randrange(self._step, canvas_h - self._step))  # 4th point modifier
        bezier_points = []
        for j2 in range(2):
            bezier_points.extend(ex.DrawBezier(bezier[j2]))

        self.ready_lines.append(bezier_points)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.draw_lines()
            self.mainloop.redraw_needed[0] = True
            self.check_result()

    def update(self, game):
        game.fill((255, 255, 255))

        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def check_result(self):
        self.result = []
        for i in range(self.data[1]):
            self.result.append(self.board.grid[i][self.data[0] - 3])
        correct = True
        if self.solution_positions == self.result:  # self.board.grid[7]:
            for each_item in self.board.ships:
                if each_item.grid_y == self.solution[each_item.unit_id]:
                    each_item.set_display_check(True)
                else:
                    each_item.set_display_check(False)
                    correct = False
        else:
            correct = False

        if correct == True:
            self.level.next_board()
