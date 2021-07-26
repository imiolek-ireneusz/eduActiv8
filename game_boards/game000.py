# -*- coding: utf-8 -*-

import os
import pygame
import classes.board
import classes.game_driver as gd
import classes.level_controller as lc
import classes.menu_items


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 25, 16)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False
        self.mainloop.menu_level = 0

        self.unit_mouse_over = None

        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                self.scheme_dir = "black"
                color = (0, 0, 0, 0)
            else:
                self.scheme_dir = "white"
                color = (255, 255, 255, 0)
        else:
            self.scheme_dir = "white"
            color = (255, 255, 255, 0)

        self.color = color
        font_color2 = (20, 75, 92)
        self.digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.imput_limit = 3

        data = [25, 16]

        x_count = self.get_x_count(data[1], even=False)
        if x_count > 25:
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

        self.last_hover = None
        self.board.add_unit(data[0] - 7, 0, 7, 1, classes.board.Label, "v.%s" % self.mainloop.config.version,
                            color, "", 2)
        self.board.units[-1].align = 2
        self.board.units[-1].font_color = font_color2

        # main category item locations and icons
        posx = [data[0] // 2 - 8, data[0] // 2 - 2, data[0] // 2 + 4]
        ico = ["ico_tn_00.png", "ico_tn_01.png", "ico_tn_02.png"]

        # activity quick launch
        self.board.add_unit(posx[1], 13, 5, 1, classes.board.Letter, "", color, "", 0)
        self.board.ships[-1].font_color = font_color2
        self.board.ships[-1].immobilize()


        self.board.add_unit(7, 0, data[0]-14, 4, classes.board.ImgCenteredShip, "", color, "home_screen_icon.png", alpha=True)

        self.board.ships[-1].immobilize()

        self.board.add_unit(0, 5, data[0], 3, classes.board.ImgCenteredShip, "", color,
                            os.path.join("schemes", self.scheme_dir, 'home_logo.png'))
        self.board.ships[-1].immobilize()


        self.board.add_unit((data[0]-11)//2, 14, 11, 2, classes.board.Label,
                            ["www.eduactiv8.org   |   info%seduactiv8%sorg" % ("@", "."),
                             "Copyright (C) 2012 - 2021  Ireneusz Imiolek"], color, "", 3)
        self.board.units[-1].font_color = font_color2
        self.board.units[-1].update_lng_font_size("def_2.0")

        self.top_categories = []
        self.units = []
        i = 0
        for each in self.mainloop.m.top_categories:
            self.top_categories.append(each)

            unit = classes.menu_items.TopCategory(self, self.top_categories[-1], posx[i], 8, 5, 5,
                                                  i, self.color, ico[i],
                                                  decor=self.mainloop.cl.color_sliders[6][0], sequence_id=i)
            self.units.append(unit)
            self.board.all_sprites_list.add(unit)
            i += 1

        #add home info icons
        self.home_icons = [["home_icon_1.png", "home_icon_2.png", "home_icon_3.png", "home_icon_4.png"],
                           ["home_ico_1.png", "home_ico_2.png", "home_ico_3.png", "home_ico_4.png"]]

        self.board.add_unit(data[0]-5, data[1] - 2, 3, 2, classes.board.ImgCenteredShip, "", color,
                            os.path.join("home_icons", "home_icon_1.png"), alpha=True)
        self.board.ships[-1].immobilize()

        self.board.add_unit(0, data[1]-2, 2, 2, classes.board.ImgShip, "", color,
                            os.path.join("home_icons", "home_icon_2.png"), alpha=True)
        self.board.ships[-1].immobilize()

        self.board.add_unit((data[0]-11)//2-2, data[1]-2, 2, 2, classes.board.ImgShip, "", color,
                            os.path.join("home_icons", "home_icon_3.png"), alpha=True)
        self.board.ships[-1].immobilize()

        self.board.add_unit(data[0]//2 + 6, data[1]-2, 2, 2, classes.board.ImgShip, "", color,
                            os.path.join("home_icons", "home_icon_4.png"), alpha=True)
        self.board.ships[-1].immobilize()

        # add scheme switchers
        if self.mainloop.scheme_code is None:
            img = 'score_hc_anone_l.png'
        else:
            img = 'score_hc_none_l.png'
        self.board.add_unit(data[0]-2, data[1]-2, 1, 1, classes.board.ImgShip, "", color,
                            os.path.join("home_icons", img), alpha=True)
        self.board.ships[-1].immobilize()

        if self.mainloop.scheme_code == "WB":
            img = 'score_hc_awb_l.png'
        else:
            img = 'score_hc_wb_l.png'
        self.board.add_unit(data[0]-2, data[1]-1, 1, 1, classes.board.ImgShip, "", color,
                            os.path.join("home_icons", img), alpha=True)
        self.board.ships[-1].immobilize()

        if self.mainloop.scheme_code == "BW":
            img = 'score_hc_abw_l.png'
        else:
            img = 'score_hc_bw_l.png'
        self.board.add_unit(data[0]-1, data[1]-2, 1, 1, classes.board.ImgShip, "", color,
                            os.path.join("home_icons", img), alpha=True)
        self.board.ships[-1].immobilize()

        if self.mainloop.scheme_code == "BY":
            img = 'score_hc_aby_l.png'
        else:
            img = 'score_hc_by_l.png'
        self.board.add_unit(data[0]-1, data[1]-1, 1, 1, classes.board.ImgShip, "", color,
                            os.path.join("home_icons", img), alpha=True)
        self.board.ships[-1].immobilize()

        # check if espeak icon needs disabling on display of home screen
        if self.lang.lang in self.lang.tts_disabled_lngs:
            self.mainloop.sb.espeak_avail(False)
        else:
            self.mainloop.sb.espeak_avail(True)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.KEYDOWN and (event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER):
            self.active_unit = self.board.ships[0]
            lhv = len(self.active_unit.value)
            self.changed_since_check = True
            if event.key == pygame.K_BACKSPACE:
                if lhv > 0:
                    self.active_unit.value = self.active_unit.value[0:lhv - 1]
            else:
                char = event.unicode
                if len(char) > 0 and (char in self.digits):
                    if lhv < self.imput_limit:
                        self.active_unit.value += char
                    else:
                        self.active_unit.value = char
            self.active_unit.update_me = True
            self.mainloop.redraw_needed[0] = True
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            lhv = len(self.active_unit.value)
            if lhv > 0:
                try:
                    activity_id = int(self.active_unit.value)
                    if activity_id > 0:
                        self.start_game(activity_id)
                except:
                    pass

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

        if event.type == pygame.MOUSEMOTION:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            for i in range(-8, -4):
                if (self.board.ships[i].rect.left < pos[0] < self.board.ships[i].rect.right
                and self.board.ships[i].rect.top < pos[1] < self.board.ships[i].rect.bottom):
                    self.board.ships[i].change_image(os.path.join("home_icons", self.home_icons[1][8 + i]))
                    self.board.ships[i].update_me = True
                    self.mainloop.redraw_needed[0] = True
                else:
                    self.board.ships[i].change_image(os.path.join("home_icons", self.home_icons[0][8 + i]))
                    self.board.ships[i].update_me = True
                    self.mainloop.redraw_needed[0] = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active = self.board.active_ship
                if active > 0:
                    if self.board.ships[active] == self.board.ships[-4]:
                        self.mainloop.switch_scheme(None)
                    elif self.board.ships[active] == self.board.ships[-3]:
                        self.mainloop.switch_scheme("WB")
                    elif self.board.ships[active] == self.board.ships[-2]:
                        self.mainloop.switch_scheme("BW")
                    elif self.board.ships[active] == self.board.ships[-1]:
                        self.mainloop.switch_scheme("BY")

                    elif self.board.ships[active] == self.board.ships[-8]:
                        self.start_game(273)
                    elif self.board.ships[active] == self.board.ships[-7]:
                        self.start_game(3)
                    elif self.board.ships[active] == self.board.ships[-6]:
                        self.start_game(1)
                    elif self.board.ships[active] == self.board.ships[-5]:
                        self.start_game(2)

    def start_game(self, gameid):
        game_changed = self.mainloop.m.start_hidden_game(gameid)
        if game_changed:
            self.mainloop.menu_level = 1
            self.mainloop.menu_type = 1
            self.mainloop.info.realign()
            self.mainloop.info.reset_titles()
        else:
            self.board.ships[0].value = ""
            self.board.ships[0].update_me = True
            self.mainloop.redraw_needed[0] = True

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
