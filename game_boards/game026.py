# -*- coding: utf-8 -*-

import pygame
import random
from math import pi, cos, sin

import classes.board
import classes.drw.fraction_hq
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc
import classes.drw.fraction_hq


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.lvlc = mainloop.xml_conn.get_level_count(mainloop.m.game_dbid, mainloop.config.user_age_group)
        self.level = lc.Level(self, mainloop, self.lvlc[0], self.lvlc[1])
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 7)

    def create_game_objects(self, level=1):
        self.board.decolorable = False
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 1]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)
        self.board.draw_grid = False
        if self.mainloop.scheme is None:
            s = 127  # random.randrange(100, 150, 5)
            v = 255  # random.randrange(230, 255, 5)
            h = random.randrange(0, 255, 5)
            white = (255, 255, 255)
            self.bg_col = white
            color1 = ex.hsv_to_rgb(h, s, v)  # highlight 2
            color3 = ex.hsv_to_rgb(h, s, v)
            color1a = color1
            self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
            self.font_color = ex.hsv_to_rgb(h, 255, 100)
        else:
            color1a = self.mainloop.scheme.u_font_color
            self.font_color = self.mainloop.scheme.u_font_color  # ex.hsv_to_rgb(h,255,100)
            if self.mainloop.scheme.dark:
                self.bg_col = (0, 0, 1)
                color1 = (30, 30, 35)
                self.color2 = (0, 0, 200)
                color3 = (0, 0, 1)
            else:
                self.bg_col = (254, 254, 255)
                color1 = (254, 254, 255)
                self.color2 = (0, 0, 200)
                color3 = (254, 254, 255)

        if self.mainloop.scheme is not None:
            white = self.mainloop.scheme.u_color

            h1 = 170
            h2 = 40
            color1 = ex.hsv_to_rgb(h1, 255, 255)
            color2 = ex.hsv_to_rgb(h2, 75, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 127, 155)
            bd_color2 = ex.hsv_to_rgb(h2, 127, 155)
        else:
            white = (255, 255, 255)

            h1 = h#random.randrange(0, 255, 5)
            h2 = h1

            color1 = ex.hsv_to_rgb(h1, 150, 255)
            color2 = ex.hsv_to_rgb(h2, 30, 255)
            bd_color1 = ex.hsv_to_rgb(h1, 187, 200)
            bd_color2 = ex.hsv_to_rgb(h2, 150, 225)

        data = [13, 5, 3]
        data.extend(
            self.mainloop.xml_conn.get_level_data(self.mainloop.m.game_dbid, self.mainloop.config.user_age_group,
                                                  self.level.lvl))
        data.append(5)
        self.chapters = self.mainloop.xml_conn.get_chapters(self.mainloop.m.game_dbid,
                                                            self.mainloop.config.user_age_group)
        self.data = data
        self.layout.update_layout(data[0], data[1])
        self.board.set_animation_constraints(5, data[0] - 5, 0, data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)

        self.num_list = []
        self.num_list2 = []

        sign = "/"
        numbers = []
        for i in range(2):
            num1 = random.randrange(1, data[3])
            num2 = random.randrange(num1 + 1, data[3] + 1)
            numbers.append([num1, num2])
            expr = str(float(num1)) + sign + str(float(num2))
            disp = ["", str(num1), str(num2), ""]
            self.num_list.append(expr)
            self.num_list2.append(disp)

        # create table to store 'binary' solution
        self.solution_grid = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.expression = [" " for x in range(data[0])]
        # find position of first door square
        xd = (data[0] - data[2]) // 2

        # add objects to the board
        self.board.add_unit(0, 0, 5, 5, classes.board.Label, "", self.bg_col, "", data[4])
        self.board.add_unit(8, 0, 5, 5, classes.board.Label, "", self.bg_col, "", data[4])

        size = self.board.scale
        center = [size // 2, size // 2]

        for i in range(0, 2):
            x2 = xd + i * 2
            caption = self.num_list2[i]
            self.board.add_unit(x2, 2, 1, 1, classes.board.Label, caption, color3, "", data[4])
            self.board.units[-1].font_color = self.font_color
            self.board.units[i + 2].set_outline(self.font_color, 1)
            self.draw_fractions(self.board.units[i + 2].painting, size, center, color1)
            self.board.units[i + 2].image = self.board.units[i + 2].painting.copy()
            self.expression[x2] = str(self.num_list[i])
            if i < 1:
                self.solution_grid[x2 + 1] = 1

        signs = [" < ", " = ", " > "]
        if self.level.lvl > 12: signs.append(" < ")  # just for the symetry

        for i in range(len(signs)):
            if len(signs) < data[0]:
                if i == 0 and len(signs) % 2 == 0:
                    x = data[0] // 2
                    y = 2
                else:
                    x = (data[0] - len(signs)) // 2
                    y = 0

            self.board.add_unit(x + i, y, 1, 1, classes.board.Letter, signs[i], color3, "", data[4])
            self.board.ships[-1].checkable = True
            self.board.ships[-1].init_check_images()
            self.board.ships[-1].font_color = self.font_color
            #self.board.ships[-1].allow_brightening = False
            self.board.ships[i].readable = False
            self.board.ships[i].set_outline(self.font_color, 1)

        ind = len(self.board.units)
        self.board.add_door(xd + 1, 2, 1, 1, classes.board.Door, "", self.bg_col, "")
        self.board.units[ind].door_outline = True
        self.board.all_sprites_list.move_to_front(self.board.units[ind])

        """
        instruction = self.d["Drag lt"]
        self.board.add_unit(0, data[1] - 1, data[0], 1, classes.board.Letter, instruction, self.bg_col, "", 9)
        self.board.ships[-1].font_color = self.font_color
        self.board.ships[-1].immobilize()
        self.board.ships[-1].speaker_val = self.d["Drag lt2"]
        self.board.ships[-1].set_outline(self.font_color, 1)
        self.board.ships[-1].speaker_val_update = False
        """

        """
        size = self.board.units[0].grid_w * self.board.scale
        center = [size // 2, size // 2]
        
        for i in range(2):
            canvas = pygame.Surface([size, size - 1])
            canvas.fill(self.board.units[i].initcolor)
            self.draw_circles(numbers[i], canvas, size, center, color1a)  # data[7](data, canvas, i)
            self.board.units[i].painting = canvas.copy()
        """
        for i in range(2):
            self.fraction = classes.drw.fraction_hq.Fraction(1, self.board.scale * self.board.units[i].grid_w, color1, color2, bd_color1,
                                                             bd_color2, numbers[i], 1)
            self.board.units[i].painting = self.fraction.get_canvas().copy()

    def show_info_dialog(self):
        self.mainloop.dialog.show_dialog(3, self.d["Drag lt"])


    def draw_fractions(self, canvas, size, center, color):
        lh = max(int(size * 0.05), 2)
        la = self.mainloop.config.font_start_at_adjustment
        pygame.draw.line(canvas, self.font_color, [center[0] - size // 7, center[1] - lh // 2 + la],
                         [center[0] + size // 7, center[1] - lh // 2 + la], lh)

    def draw_circles(self, numbers, canvas, size, center, color):
        angle_step = 2 * pi / numbers[1]
        angle_start = -pi / 2
        angle_arc_start = -pi / 2
        r = size // 2 - size // 20
        angle = angle_start
        angle_s = angle_arc_start
        angle_e = angle_arc_start + numbers[0] * 2 * pi / numbers[1]

        # manually draw the arc - the 100% width of the arc does not impress
        i = 0
        while angle < angle_e:  # maximum of 158 lines per pi
            x = (r - 2) * cos(angle) + center[0]
            y = (r - 2) * sin(angle) + center[1]
            pygame.draw.line(canvas, color, [center[0], center[1]], [x, y], 8)
            i += 1
            angle = angle_start + 0.02 * i
            points = []
            multipoints = []

        for i in range(numbers[1]):
            # angle for line
            angle = angle_start + angle_step * i

            # Calculate the x,y for the end point
            x = r * cos(angle) + center[0]
            y = r * sin(angle) + center[1]

            multipoints.append([x, y])

        # draw clipping polygon
        points.append(center)
        for i in range(numbers[0], numbers[1]):
            points.append(multipoints[i])
        points.append([center[0], center[1] - r])
        pygame.draw.polygon(canvas, self.bg_col, points, 0)

        if numbers == [1, 2]:  # white area to the left...
            pygame.draw.line(canvas, self.bg_col, [center[0] - 3, center[1] - r], [center[0] - 3, center[1] + r], 6)

        # Draw the line from the center to the calculated end points
        for each in multipoints:
            pygame.draw.aaline(canvas, self.color2, center, each)
        pygame.draw.circle(canvas, self.color2, center, r, 2)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.check_result()

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.auto_check_reset()
        elif event.type == pygame.KEYUP:
            self.check_result()

    def update(self, game):
        game.fill(self.bg_col)
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def auto_check_reset(self):#ex.hsv_to_rgb(h, s + 50, v - 50)
        for each in self.board.ships:
            if each.checkable:
                each.set_display_check(None)

    def check_result(self):
        if self.board.grid[2] == self.solution_grid:
            found = None
            for i in range(len(self.board.ships)):
                if self.board.ships[i].grid_y == 2:  # if the sign is on line with expression
                    found = self.board.ships[i]
                    value = self.board.ships[i].value
                    if value == " = ":
                        value = "=="
                    self.expression[self.board.ships[i].grid_x] = value
            eval_string = ''.join(self.expression)
            eval_string.strip()
            if eval(eval_string) == True:
                self.level.next_board()
                if found is not None:
                    found.set_display_check(True)
            else:
                if found is not None:
                    found.set_display_check(False)
        else:
            self.auto_check_reset()
        self.mainloop.redraw_needed[0] = True
