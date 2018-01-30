# -*- coding: utf-8 -*-

import math
import os
import pygame

import classes.board
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        self.badge_count = mainloop.db.get_completion_count(mainloop.userid)
        self.pages_total = int(math.ceil(self.badge_count / 10.0))
        if self.pages_total == 0:
            self.pages_total = 1
        self.current_page = 1

        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 10)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False

        color1 = (220, 220, 220)
        color2 = (255, 255, 255)

        font_color = (40, 40, 40)
        data = [35, 21]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=False)
        if x_count > 35:
            data[0] = x_count

        self.data = data

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.offset = (self.current_page - 1) * 10

        self.results = self.mainloop.db.completion_book(self.mainloop.userid, offset=self.offset)


        self.ages = [self.lang.b["preschool"], self.lang.b["Year 1"], self.lang.b["Year 2"], self.lang.b["Year 3"], self.lang.b["Year 4"], self.lang.b["Year 5"], self.lang.b["Year 6"], self.lang.b["Year 6"]]  # , self.lang.b["all groups"]

        if self.badge_count > 0:
            centre = data[0] // 2
            gap = 4
            bw = 3
            lw = 7
            self.x_positions_odd = [centre - 1 - 4 - 3 - 4 - 3, centre - 1 - 4 - 3, centre - 1, centre + 2 + 4,
                                    centre + 2 + 4 + 3 + 4]
            self.x_positions_even = [centre - 2 - 3 - 4 - 3, centre - 2 - 3, centre + 3, centre + 3 + 3 + 4]

            bpos = []

            # badges = range(1,random.randint(2,11))
            ln = len(self.results)
            if ln == 1:
                tpos = self.x_positions_odd[2:3]
            elif ln == 2:
                tpos = self.x_positions_even[1:3]
            elif ln == 3:
                tpos = self.x_positions_odd[1:4]
            elif ln == 4:
                tpos = self.x_positions_even[:]
            else:  # ln = 5:
                tpos = self.x_positions_odd[:]
                if ln == 6:
                    bpos = self.x_positions_odd[2:3]
                elif ln == 7:
                    bpos = self.x_positions_even[1:3]
                elif ln == 8:
                    bpos = self.x_positions_odd[1:4]
                elif ln == 9:
                    bpos = self.x_positions_even[:]
                else:  # ln = 10:
                    bpos = self.x_positions_odd[:]

            apos = []
            apos.extend(tpos)
            apos.extend(bpos)
            scheme = "white"
            if self.mainloop.scheme is not None:
                if self.mainloop.scheme.dark:
                    scheme = "black"
                    color2 = (0, 0, 0)
            y = 2
            for i in range(ln):
                if i > 4:
                    y = 10
                if self.results[i][0] in self.mainloop.m.id2icon:
                    self.board.add_unit(apos[i], y - 1, 3, 1, classes.board.Label, "%d x" % (self.results[i][3]),
                                        color2, "", 1)
                    self.board.units[-1].font_color = (0, 75, 255)
                    if self.results[i][0] not in self.mainloop.m.lang_customized_icons:
                        img2_src = os.path.join("res", "icons", self.mainloop.m.id2icon[self.results[i][0]])
                    else:
                        file2_src = "%s%s%s" % (self.mainloop.m.id2icon[self.results[i][0]][0:10],
                                                self.mainloop.config.id2imgsuffix[self.results[i][2]], ".png")
                        img2_src = os.path.join("res", "icons", file2_src)

                    self.board.add_unit(apos[i], y, 3, 4, classes.board.TwoImgsShip, "", color2,
                                        img_src=os.path.join("res", "themes", self.mainloop.theme, "images", "badge_bg.png"),
                                        img2_src=img2_src, row_data=(21, 21), alpha=True)
                    self.board.ships[-1].immobilize()
                    self.board.ships[-1].outline = False
                    if self.lang.ltr_text:
                        levtxt = "%s %d" % (self.lang.d["Level"], self.results[i][1])
                    else:
                        levtxt = "%d %s" % (self.results[i][1], self.lang.d["Level"])
                    if self.results[i][2] != 0:
                        lng = "(" + self.mainloop.config.id2lng[self.results[i][2]] + ")"
                    else:
                        lng = ""
                    self.board.add_unit(apos[i] - 2, y + 4, 7, 3, classes.board.Label, [self.ages[self.results[i][4]], levtxt, lng, ""], color2, "", 1)
                    self.board.units[-1].font_color = (255, 75, 0)
                    self.board.units[-1].font_color = (255, 75, 0)
                else:
                    print(self.results[i][0])

            if self.badge_count > 10:
                if self.current_page == 1:
                    self.board.add_unit(centre - 4 - 3, 17, 3, 3, classes.board.ImgShip, "", color2,
                                        os.path.join("schemes", scheme, "pglu.png"))
                else:
                    self.board.add_unit(centre - 4 - 3, 17, 3, 3, classes.board.ImgShip, "", color2,
                                        os.path.join("schemes", scheme, "pgl.png"))
                self.btn_prev = self.board.ships[-1]
                self.btn_prev.immobilize()
                self.btn_prev.outline = False

                self.board.add_unit(centre - 1 - 3, 17, 9, 3, classes.board.Label,
                                    "%d / %d" % (self.current_page, self.pages_total), color2, "", 21)
                if self.current_page == self.pages_total:
                    self.board.add_unit(centre + 2 + 3, 17, 3, 3, classes.board.ImgShip, "", color2,
                                        os.path.join("schemes", scheme, "pgru.png"))
                else:
                    self.board.add_unit(centre + 2 + 3, 17, 3, 3, classes.board.ImgShip, "", color2,
                                        os.path.join("schemes", scheme, "pgr.png"))
                self.btn_next = self.board.ships[-1]
                self.btn_next.immobilize()
                self.btn_next.outline = False
        else:
            self.board.add_unit(0, 2, data[0], 2, classes.board.Label, self.lang.d["Achievements"], color2, "", 25)
            self.board.units[-1].font_color = (255, 75, 0, 0)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if self.badge_count > 10:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    active = self.board.active_ship
                    if active > 0:
                        if self.board.ships[active] == self.btn_prev and self.current_page > 1:
                            self.change_page(-1)
                        elif self.board.ships[active] == self.btn_next and self.current_page < self.pages_total:
                            self.change_page(1)

    def change_page(self, page_inc):
        self.current_page = self.current_page + page_inc
        self.create_game_objects()

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def check_result(self):
        pass
