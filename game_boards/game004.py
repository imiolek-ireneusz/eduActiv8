# -*- coding: utf-8 -*-

import pygame
import classes.game_driver as gd
import classes.level_controller as lc
import classes.menu_items


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 17, 11)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False
        self.unit_mouse_over = None

        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.scheme_dir = "black"
                color = (0, 0, 0, 255)
            else:
                self.scheme_dir = "white"
                color = (255, 255, 255, 255)
        else:
            self.scheme_dir = "white"
            color = (255, 255, 255, 255)
        self.color = color

        l = 0
        self.lncnt = [0, 0, 0]
        if self.mainloop.menu_level == 1:
            self.categories = []
            for each in self.mainloop.m.categories:
                if each.top_id == self.mainloop.menu_group:
                    l += 1
                    self.categories.append(each)
                    if each.menu_line > 0:
                        self.lncnt[each.menu_line - 1] += 1

        elif self.mainloop.menu_level == 2:
            self.categories = []
            for each in self.mainloop.m.cats_current:
                l += 1
                self.categories.append(each)
                if each.menu_line > 0:
                    self.lncnt[each.menu_line - 1] += 1
        else:
            self.games = []
            for each in self.mainloop.m.games_current:
                l += 1
                self.games.append(each)
                if each.menu_line > 0:
                    self.lncnt[each.menu_line - 1] += 1

        if l <= 15:
            data = [31, 19]
            self.h_count = 5
        else:
            data = [43, 19]
            self.h_count = 7

        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=False)
        if x_count > data[0]:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        self.scale = self.layout.scale
        self.board.level_start(data[0], data[1], self.scale)
        self.board.board_bg.initcolor = color
        self.board.board_bg.color = color
        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        self.units = []

        if self.lncnt != [0, 0, 0]:
            # remove any empty rows of icons in the menu
            ln2 = [0, 0, 0]
            j = 0
            for i in range(3):
                if self.lncnt[i] > 0:
                    ln2[j] = self.lncnt[i]
                    j += 1
            self.lncnt = ln2

            x1 = (data[0] - (self.lncnt[0] * 6)) // 2
            x2 = (data[0] - (self.lncnt[1] * 6)) // 2
            x3 = (data[0] - (self.lncnt[2] * 6)) // 2

            px1 = [x1 + (i * 6) for i in range(self.lncnt[0])]
            px2 = [x2 + (i * 6) for i in range(self.lncnt[1])]
            px3 = [x3 + (i * 6) for i in range(self.lncnt[2])]

            py1 = [1 for i in range(self.lncnt[0])]
            py2 = [7 for i in range(self.lncnt[1])]
            py3 = [13 for i in range(self.lncnt[2])]
            posx = px1 + px2 + px3
            posy = py1 + py2 + py3
        else:
            if l < self.h_count+1:
                x = (data[0] - l * 6) // 2
                y = 1
                posx = [x + (i * 6) for i in range(l)]
                posy = [y for i in range(l)]
            elif l < self.h_count * 2 + 1:
                x1 = (data[0] - self.h_count * 6) // 2
                x2 = (data[0] - (l - self.h_count) * 6) // 2
                y1 = 1
                y2 = 7
                px1 = [x1 + (i * 6) for i in range(self.h_count)]
                px2 = [x2 + (i * 6) for i in range(l - self.h_count)]
                posx = px1 + px2
                py1 = [y1 for i in range(self.h_count)]
                py2 = [y2 for i in range(l - self.h_count)]
                posy = py1 + py2
            else:
                x1 = x2 = (data[0] - (self.h_count * 6)) // 2
                x3 = (data[0] - (l - (self.h_count * 2)) * 6) // 2
                y1 = 1
                y2 = 7
                y3 = 13
                px1 = [x1 + (i * 6) for i in range(self.h_count)]
                px3 = [x3 + (i * 6) for i in range(l - self.h_count * 2)]
                posx = px1 + px1 + px3
                py1 = [y1 for i in range(self.h_count)]
                py2 = [y2 for i in range(self.h_count)]
                py3 = [y3 for i in range(l - self.h_count * 2)]
                posy = py1 + py2 + py3

        self.template_units = {0: None, 1: None, 2: None}

        if self.mainloop.menu_level < 3:
            for i in range(l):
                unit = classes.menu_items.Category(self, self.categories[i], posx[i] + 1, posy[i], 5, 5,
                                                   self.categories[i].cat_id, self.color, self.categories[i].img_src,
                                                   self.mainloop.cl.color_sliders[6][0], sequence_id=i)
                self.units.append(unit)
                self.board.all_sprites_list.add(unit)
        else:
            for i in range(l):
                # find out the number of levels
                lvl_count = self.mainloop.xml_conn.get_level_count(self.games[i].dbgameid,
                                                                   self.mainloop.config.user_age_group)
                if self.games[i].dbgameid in self.mainloop.completions_dict:
                    completions = self.mainloop.completions_dict[self.games[i].dbgameid]
                else:
                    show_all_ages = self.mainloop.xml_conn.get_show_all_ages(self.games[i].dbgameid)

                    if show_all_ages is None:
                        show_all_ages = [7, 7]

                    completions = []
                    if lvl_count is not None:
                        all_compl = self.mainloop.db.query_completion_all_ages(self.mainloop.userid,
                                                                               self.games[i].dbgameid,
                                                                               self.games[i].lang_activity)
                        completions = [0 for x in range(0, lvl_count[1])]

                        for each in all_compl:
                            if each[2] - 1 < lvl_count[1]:
                                if (self.mainloop.config.user_age_group == 7 and
                                        show_all_ages[0] <= each[5] <= show_all_ages[1]):
                                    completions[each[2] - 1] = each[4]
                                elif self.mainloop.config.user_age_group == each[5]:
                                    completions[each[2] - 1] = each[4]

                    self.mainloop.completions_dict[self.games[i].dbgameid] = completions

                unit = classes.menu_items.GameIcon(self, self.games[i], posx[i] + 1, posy[i], 5, 5, self.color,
                                                   lvl_count, completions, decor=self.mainloop.cl.color_sliders[6][1],
                                                   sequence_id=i)
                self.units.append(unit)
                self.board.all_sprites_list.add(unit)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            found = False
            for each in self.units:
                if each.rect.left < pos[0] < each.rect.right and each.rect.top < pos[1] < each.rect.bottom:
                    if each != self.unit_mouse_over:
                        if self.unit_mouse_over is not None:
                            self.unit_mouse_over.mouse_out()
                        self.unit_mouse_over = each
                    found = True
                    each.handle(event)
                    break
            if not found:
                if self.unit_mouse_over is not None:
                    self.unit_mouse_over.mouse_out()
                self.unit_mouse_over = None
        self.board.mainloop.redraw_needed[0] = True

    def start_game(self, gameid):
        self.mainloop.m.start_hidden_game(gameid)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
