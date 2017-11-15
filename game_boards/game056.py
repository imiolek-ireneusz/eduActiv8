# -*- coding: utf-8 -*-

import copy
import pygame
import random
from math import pi, cos, sin

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        #self.level = lc.Level(self, mainloop, 5, 6)
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 9, 6)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.board.draw_grid = True
        if self.mainloop.scheme is None:
            s = random.randrange(100, 150, 5)
            v = random.randrange(230, 255, 5)
            h = random.randrange(0, 255, 5)
            self.bg_col = (255, 255, 255, 0)
            color1 = ex.hsv_to_rgb(h, s, v)  # highlight 2
            self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
            bg_color = ex.hsv_to_rgb(h, 40, 255)
        else:
            cl = self.mainloop.scheme.u_color
            self.bg_col = (cl[0], cl[1], cl[2], 0)
            color1 = self.mainloop.scheme.u_font_color  # (0,0,0)#ex.hsv_to_rgb(h,s,v) #highlight 2
            self.color2 = self.mainloop.scheme.u_font_color3  # contours & borders
            bg_color = self.bg_col

        data = [9, 6, 3]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        self.row_count = data[6]
        self.font_size = 7
        extra_w = 0
        if self.mainloop.m.game_variant == 0:
            drawing_f = [self.draw_circles, self.draw_rectangles, self.draw_minicircles, self.draw_polygons,
                         self.draw_petals]
            obj_classes = [classes.board.Label, classes.board.Ship, classes.board.Ship, classes.board.Ship,
                           classes.board.Ship]
            instruction = self.d["Fract instr0"]
            instrp = self.dp["Fract instr0"]
        elif self.mainloop.m.game_variant == 1:
            drawing_f = [self.draw_circles, self.draw_rectangles, self.draw_minicircles, self.draw_polygons,
                         self.draw_fractions]
            obj_classes = [classes.board.Label, classes.board.Ship, classes.board.Ship, classes.board.Ship,
                           classes.board.Letter]
            instruction = self.d["Fract instr1"]
            instrp = self.dp["Fract instr1"]
        elif self.mainloop.m.game_variant == 2:
            drawing_f = [self.draw_fractions, self.draw_circles, self.draw_rectangles, self.draw_minicircles,
                         self.draw_polygons]
            obj_classes = [classes.board.Label, classes.board.Ship, classes.board.Ship, classes.board.Ship,
                           classes.board.Ship]
            instruction = self.d["Fract instr2"]
            instrp = self.dp["Fract instr2"]
        elif self.mainloop.m.game_variant == 3:
            drawing_f = [self.draw_percents, self.draw_circles, self.draw_rectangles, self.draw_decimals,
                         self.draw_fractions]
            obj_classes = [classes.board.Label, classes.board.Ship, classes.board.Ship, classes.board.Letter,
                           classes.board.Letter]
            instruction = self.d["Fract instr3"]
            instrp = self.dp["Fract instr3"]
            extra_w = 0
        elif self.mainloop.m.game_variant == 4:
            drawing_f = [self.draw_ratios, self.draw_circles, self.draw_rectangles, self.draw_minicircles,
                         self.draw_polygons]
            obj_classes = [classes.board.Label, classes.board.Ship, classes.board.Ship, classes.board.Ship,
                           classes.board.Ship]
            instruction = self.d["Fract instr4"]
            instrp = self.dp["Fract instr4"]
            extra_w = 1

        data[0] = data[0] + extra_w
        self.data = data
        if self.mainloop.m.game_variant == 4:#2:
            self.board.set_animation_constraints(2, data[0], 0, self.row_count)
        else:
            self.board.set_animation_constraints(1, data[0], 0, self.row_count)

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.num_list = []
        self.num_list2 = []

        sign = "/"
        numbers = []
        # create list of available slots for mixed objects

        slots = []
        for j in range(0, self.row_count):
            for i in range(5, 9):
                slots.append([i, j])
        random.shuffle(slots)
        # num2 = 0
        if data[4] == 0:
            l2 = data[3].split(", ")
            l2l = len(l2)

        while len(numbers) < self.row_count:
            if data[4] == 0:
                num2 = int(l2[random.randint(0, l2l - 1)])
            else:
                num2 = random.randint(data[3], data[4])
            num1 = random.randrange(data[5], num2)

            lst = [num1, num2]
            if lst not in numbers:
                unique = True
                if len(numbers) > 0:  # and i < 50:
                    for each in numbers:
                        if float(num1) / float(num2) == float(each[0]) / float(each[1]):
                            unique = False
                if unique:
                    numbers.append(lst)
                    expr = str(float(num1)) + sign + str(float(num2))
                    disp = str(num1) + sign + str(num2)
                    self.num_list.append(expr)
                    self.num_list2.append(disp)

        # create table to store the solution
        # add objects to the board
        size = self.board.scale
        center = [size // 2, size // 2]
        capt = copy.deepcopy(numbers)

        for i in range(0, 5*self.row_count):
            ew = 0
            xo = 0
            if i < self.row_count:
                xy = [0, i]
                if self.mainloop.m.game_variant == 4:
                    ew = 1
            else:
                xy = slots[i - 5][0], slots[i - 5][1]
                if self.mainloop.m.game_variant == 4:
                    xo = 1
            f_index = i // self.row_count
            disp = ""
            if drawing_f[f_index] == self.draw_fractions:
                #TODO
                #if self.level.lvl > 3:
                #    multi = random.randrange(1, data[5])
                #    capt[i - f_index * 5][0] *= multi
                #    capt[i - f_index * 5][1] *= multi
                disp = ["", str(capt[i - f_index * self.row_count][0]), str(capt[i - f_index * self.row_count][1]), ""]
            elif drawing_f[f_index] == self.draw_ratios:

                if self.lang.lang == "lkt":
                    self.font_size = 5
                    disp = str(capt[i - f_index * self.row_count][0]) + " : " + str(capt[i - f_index * self.row_count][1] - capt[i - f_index * self.row_count][0])
                else:
                    disp = [self.d["Ratio"], str(capt[i - f_index * self.row_count][0]) + " : " + str(
                        capt[i - f_index * self.row_count][1] - capt[i - f_index * self.row_count][0])]
                    self.font_size = 7
            elif drawing_f[f_index] == self.draw_percents:
                percent = (float(capt[i - f_index * self.row_count][0]) / float(capt[i - f_index * self.row_count][1])) * 100
                intperc = int(percent)
                if intperc == percent:
                    disp = str(intperc) + "%"
                else:
                    disp = str(percent) + "%"
            elif drawing_f[f_index] == self.draw_decimals:
                decimal = float(capt[i - f_index * self.row_count][0]) / float(capt[i - f_index * self.row_count][1])
                disp = str(decimal)

            self.board.add_unit(xy[0] + xo, xy[1], 1 + ew, 1, obj_classes[f_index], disp, self.bg_col, "",
                                self.font_size, alpha=True)
            if ew == 1:
                canvas = pygame.Surface([size * 2, size - 1])
            else:
                canvas = pygame.Surface([size, size - 1], flags=pygame.SRCALPHA)
            canvas.fill(self.bg_col)
            drawing_f[f_index](numbers[i - f_index * self.row_count], canvas, size, center, color1)  # data[7](data, canvas, i)

            if i < self.row_count:
                self.board.units[-1].hidden_value = numbers[i]
                self.board.units[-1].font_color = self.color2
                self.board.units[-1].painting = canvas.copy()
            else:
                self.board.ships[-1].hidden_value = numbers[i - f_index * self.row_count]
                self.board.ships[-1].font_color = self.color2
                self.board.ships[-1].painting = canvas.copy()
                self.board.ships[-1].readable = False
                self.board.ships[-1].highlight = False
                self.board.ships[-1].checkable = True
                self.board.ships[-1].init_check_images()

        ind = len(self.board.units)
        for i in range(0, self.row_count):
            self.board.add_door(0, i, 5 + xo, 1, classes.board.Door, "", self.bg_col, "")
            self.board.units[ind + i].door_outline = True
            self.board.units[ind + i].perm_outline_color = self.color2

            self.board.all_sprites_list.move_to_front(self.board.units[ind + i])

        if self.row_count < 5:
            self.board.add_unit(0, data[1] - 1 - (5 - self.row_count), data[0], data[1] - 1 - self.row_count, classes.board.Label, "", self.bg_col, "", 9)

        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, bg_color, "", 9)
        self.board.ships[-1].set_outline(self.color2, 1)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].font_color = self.color2
        self.board.ships[-1].speaker_val = instrp
        self.board.ships[-1].speaker_val_update = False

    def draw_circles(self, numbers, canvas, size, center, color):
        angle_step = 2 * pi / numbers[1]
        angle_start = -pi / 2
        angle_arc_start = -pi / 2
        r = size // 2 - 10
        angle = angle_start
        angle_e = angle_arc_start + numbers[0] * 2 * pi / numbers[1]

        i = 0
        while angle < angle_e:  # maximum of 158 lines per pi
            x = (r - 2) * cos(angle) + center[0]
            y = (r - 2) * sin(angle) + center[1]
            pygame.draw.line(canvas, color, [center[0], center[1]], [x, y], 3)
            i += 1
            angle = angle_start + 0.02 * (i)

        pygame.draw.ellipse(canvas, self.color2, (11, 11, size - 22, size - 22), 1)
        r = r - 1
        for i in range(numbers[1]):
            # angle for line
            angle = angle_start + angle_step * i
            # Calculate the x,y for the end point
            x = r * cos(angle) + center[0]
            y = r * sin(angle) + center[1]

            # Draw the line from the center to the calculated end point
            pygame.draw.line(canvas, self.color2, [center[0], center[1]], [x, y], 1)

    def draw_polygons(self, numbers, canvas, size, center, color):
        half = False
        numbers = numbers[:]
        if numbers[1] == 2:
            numbers[1] = 4
            half = True
        angle_step = 2 * pi / numbers[1]
        angle_start = -pi / 2
        r = size // 2 - 10
        angle = angle_start

        r = r - 1
        x = r * cos(angle) + center[0]
        y = r * sin(angle) + center[1]
        prev = [center[0], center[1]]

        lines = []
        multilines = []
        points = []
        points.append(prev)

        for i in range(numbers[1] + 1):
            # angle for line
            angle = angle_start + angle_step * i
            # Calculate the x,y for the end point
            if i > 0:
                x = r * cos(angle) + center[0]
            else:
                x = center[0]

            y = r * sin(angle) + center[1]
            # Draw the line from the center to the calculated end point
            if half is False or (half is True and i % 2 == 0):
                multilines.append([[center[0], center[1]], [x, y]])

            lines.append(prev)
            prev = [x, y]
            if (half is False and i < numbers[0] + 1) or (half is True and i < 3):
                points.append(prev)

        points.append(center)
        pygame.draw.polygon(canvas, color, points, 0)

        lines.append([x, y])
        # pygame.draw.aalines(canvas, self.color2, True, lines, True)
        pygame.draw.lines(canvas, self.color2, True, lines, 1)
        for each in multilines:
            pygame.draw.line(canvas, self.color2, each[0], each[1], 1)

    def draw_rectangles(self, numbers, canvas, size, center, color):
        points = []
        step = (size - 10) // numbers[1]
        width = step * numbers[1]
        left = (size - width) // 2
        rectangle = [[left, 15], [size - left * 2, size - 30]]

        if numbers[1] > 2:
            for i in range(numbers[1]):
                points.extend([[left + step * i, 15], [left + step * i, size - 15], [left + step * (i + 1), size - 15],
                               [left + step * (i + 1), 15]])
        elif numbers[1] == 2:
            points.extend([[left + step, 15], [left + step, size - 15]])
        # draw fraction
        fraction_rect = [[left, 15], [step * numbers[0], size - 30]]
        pygame.draw.rect(canvas, color, fraction_rect, 0)
        # draw square with grid
        pygame.draw.lines(canvas, self.color2, True, points)
        if numbers[1] == 2:
            pygame.draw.rect(canvas, self.color2, rectangle, 1)

    def draw_minicircles(self, numbers, canvas, size, center, color):
        angle_step = 2 * pi / numbers[1]
        angle_start = -pi / 2
        r = size // 3
        # manually draw the arc - the 100% width of the arc does not impress

        for i in range(numbers[1]):
            # angle for line
            angle = angle_start + angle_step * i

            # Calculate the x,y for the end point
            x = r * cos(angle) + center[0]
            y = r * sin(angle) + center[1]
            if i < numbers[0]:
                pygame.draw.circle(canvas, color, [int(x), int(y)], size // 10, 0)
            pygame.draw.circle(canvas, self.color2, [int(x), int(y)], size // 10, 1)
            # Draw the line from the center to the calculated end point

    def draw_petals(self, numbers, canvas, size, center, color):
        angle_step = 2 * pi / numbers[1]
        angle_start = -pi / 2
        r = size // 3 + size // 10

        multilines = []
        for i in range(numbers[1]):
            # angle for line
            angle = angle_start + angle_step * i

            # Calculate the x,y for the end point
            x = r * cos(angle) + center[0]
            y = r * sin(angle) + center[1]

            x2 = (r - size // 10) * cos(angle - 0.3) + center[0]
            y2 = (r - size // 10) * sin(angle - 0.3) + center[1]

            x3 = (r - size // 10) * cos(angle + 0.3) + center[0]
            y3 = (r - size // 10) * sin(angle + 0.3) + center[1]

            points = [center, [x2, y2], [x, y], [x3, y3]]

            if i < numbers[0]:
                pygame.draw.polygon(canvas, color, points, 0)
            # Draw the line from the center to the calculated end point
            multilines.extend(points)
        pygame.draw.lines(canvas, self.color2, True, multilines, 1)

    def draw_fractions(self, numbers, canvas, size, center, color):
        lh = max(int(size * 0.04), 2)
        la = self.mainloop.config.font_start_at_adjustment * 60 // size
        pygame.draw.line(canvas, self.color2, [center[0] - size // 7, center[1] - lh // 2 + la],
                         [center[0] + size // 7, center[1] - lh // 2 + la], lh)

    def draw_ratios(self, numbers, canvas, size, center, color):
        if self.lang.lang != "lkt":
            pygame.draw.line(canvas, self.color2, [center[0], center[1]], [center[0] * 3, center[1]], 1)

    def draw_decimals(self, numbers, canvas, size, center, color):
        pass

    def draw_percents(self, numbers, canvas, size, center, color):
        pass

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
            self.check_result()

    def auto_check_reset(self):
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        correct = True

        for i in range(len(self.board.ships) - 1):
            ship = self.board.ships[i]
            if ship.grid_x >= self.data[0] - 4:
                correct = False
                break

        if correct:
            for i in range(len(self.board.ships) - 1):
                ship = self.board.ships[i]
                if ship.hidden_value == self.board.units[ship.grid_y].hidden_value:
                    ship.set_display_check(True)
                else:
                    correct = False
                    ship.set_display_check(False)
            if correct:
                self.level.next_board()
