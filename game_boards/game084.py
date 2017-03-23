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


        self.ages = [self.lang.b["preschool"], self.lang.b["Year 1"], self.lang.b["Year 2"], self.lang.b["Year 3"], self.lang.b["Year 4"], self.lang.b["Year 5"], self.lang.b["Year 6"], self.lang.b["all groups"]]

        # print(self.results)
        # [(1, 85, 1, 1, 1), (1, 85, 2, 1, 1), (1, 85, 3, 1, 1), (1, 11, 1, 1, 1),
        # (1, 133, 1, 1, 1), (1, 133, 2, 1, 1), (1, 133, 3, 1, 1), (1, 133, 4, 1, 1), (1, 80, 1, 2, 1), (1, 12, 1, 2, 1)]
        # TABLE completions (userid integer KEY, gameid integer KEY, lvl_completed integer, lang_id integer, num_completed integer)
        # gameid, lvl_completed, lang_id , num_completed)
        # [(85, 1, 1, 1), (85, 2, 1, 1), (85, 3, 1, 1), (11, 1, 1, 1), (133, 1, 1, 1),
        # (133, 2, 1, 1), (133, 3, 1, 1), (133, 4, 1, 1), (80, 1, 1, 2), (12, 1, 1, 2)]
        # [(12, 2, 1, 1), (31, 1, 1, 60), (81, 1, 1, 3), (81, 2, 1, 3), (81, 3, 1, 2), (81, 4, 1, 2),
        # (81, 5, 1, 2), (81, 6, 1, 2), (81, 7, 1, 2), (81, 8, 1, 2)]

        if self.badge_count > 0:
            centre = data[0] // 2
            gap = 4
            bw = 3
            lw = 7
            self.x_positions_odd = [centre - 1 - 4 - 3 - 4 - 3, centre - 1 - 4 - 3, centre - 1, centre + 2 + 4,
                                    centre + 2 + 4 + 3 + 4]
            self.x_positions_even = [centre - 2 - 3 - 4 - 3, centre - 2 - 3, centre + 3, centre + 3 + 3 + 4]

            """
            if ln == 10:
                tpos = self.x_positions_odd
                bpos = self.x_positions_odd
            elif ln >= 5:
                tpos


            if ln > 5:
                tpos = self.x_positions_odd
                ln2 = ln - 5
                if ln2 %

            if ln % 2 == 1:
            """
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

                        # ico_g_0100he.png
                        # 0123456789012345

                    # print("%d - %s - %s" %(self.results[i][1], img2_src, self.mainloop.config.id2imgsuffix[self.results[i][2]]))
                    self.board.add_unit(apos[i], y, 3, 4, classes.board.TwoImgsShip, "", color2,
                                        img_src=os.path.join("res", "images", "schemes", scheme, "badge_bg.png"),
                                        img2_src=img2_src, row_data=(24, 24))
                    self.board.ships[-1].immobilize()
                    self.board.ships[-1].outline = False
                    if self.lang.ltr_text:
                        levtxt = "%s %d" % (self.lang.d["Level"], self.results[i][1])
                    else:
                        levtxt = "%d %s" % (self.results[i][1], self.lang.d["Level"])
                    self.board.add_unit(apos[i] - 2, y + 4, 7, 3, classes.board.Label, [self.ages[self.results[i][4]], levtxt, "("+self.mainloop.config.id2lng[self.results[i][2]]+")", ""], color2, "", 1)
                    self.board.units[-1].font_color = (255, 75, 0)
                    # self.board.add_unit(apos[i]+1,y+4,3,1,classes.board.Label,"date",color2,"",0)
                    #self.board.add_unit(apos[i] - 2, y + 6, 7, 1, classes.board.Label,
                    #                    self.mainloop.config.id2lng[self.results[i][2]], color2, "", 3)
                    self.board.units[-1].font_color = (255, 75, 0)
                    # self.mainloop.lang.lang_id[self.results[i][3]]
                else:
                    print(self.results[i][0])
            """
            if ln > 5:
                for i in range(5):
                    #self.board.add_unit(tpos[i],3,3,4,classes.board.Label,str(badges[i]),color2,"",0)
                    self.board.add_unit(tpos[i],3,3,4,classes.board.TwoImgsShip,"",color2, img_src = os.path.join("res","images","schemes",scheme,"badge_bg.png"), img2_src = os.path.join("res","icons",self.mainloop.m.id2icon[i+50]),row_data=(24,24))
                for i in range(5,ln):
                    self.board.add_unit(bpos[i-5],10,3,4,classes.board.TwoImgsShip,"",color2, img_src = os.path.join("res","images","schemes",scheme,"badge_bg.png"), img2_src = os.path.join("res","icons",self.mainloop.m.id2icon[i+50]),row_data=(24,24))
            else:
                for i in range(ln):
                    self.board.add_unit(tpos[i],3,3,4,classes.board.TwoImgsShip,"",color2, img_src = os.path.join("res","images","schemes",scheme,"badge_bg.png"), img2_src = os.path.join("res","icons",self.mainloop.m.id2icon[i+50]),row_data=(24,24))
            """

            """
            for each in self.x_positions_odd:
                self.board.add_unit(each,3,3,4,classes.board.Label,"a",color2,"",0)

            for each in self.x_positions_even:
                self.board.add_unit(each,10,3,4,classes.board.Label,"b",color2,"",0)
            """
            """
            self.board.board_bg.line_color = (200, 200, 200)
            if self.mainloop.scheme is not None:
                self.board.board_bg.line_color = self.mainloop.scheme.u_line_color
            self.board.board_bg.update_me = True
            """
            # if theres more than one page:


            # self.board.add_unit(centre - 4-2, y+7,3,3,classes.board.Letter,"<",color2,"",0)
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


            # self.board.add_unit(0,0,data[0],1,classes.board.Label,self.lang.d["Achievements"],color2,"",0)
            # top = 1
            # self.board.add_unit(0,top,3,1,classes.board.Label,["English & Polish","English & Polski"],color1,"",6)
            # self.board.add_unit(3,top,data[0]-3,1,classes.board.Label,["Kamila Roszak-Imiolek, Ireneusz Imiolek"],color1,"",6)

            # self.outline_all(1,1)
            # for each in self.board.units:
            #    each.font_color = font_color

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
