# -*- coding: utf-8 -*-

import os
import pygame
from math import pi, cos, sin, sqrt
import classes.game_driver as gd
import classes.level_controller as lc


class Category(pygame.sprite.Sprite):
    """basic class for all on-board objects"""

    def __init__(self, board, cat_obj, grid_x=0, grid_y=0, grid_w=1, grid_h=1, item_id="", color=(0, 0, 0, 0), img_src=''):
        pygame.sprite.Sprite.__init__(self)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.item_id = item_id
        self.board = board
        self.cat_obj = cat_obj
        self.color = color
        self.update_me = True
        self.hover = False

        self.image = pygame.Surface([grid_w * board.scale - 1, grid_h * board.scale - 1])
        self.rect = self.image.get_rect()
        self.rect.topleft = [grid_x * board.scale + 1, grid_y * board.scale + 1]

        self.change_image(img_src)
        self.update(self.board.mainloop.game)

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.update_me = True
            self.img = self.image
            self.img_pos = (0, 0)
            try:
                self.img1_org = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert_alpha()
                self.img2_org = pygame.image.load(os.path.join('res', 'icons', "menu_c_bg.png")).convert_alpha()
                self.img2_org_h = pygame.image.load(os.path.join('res', 'icons', "menu_c_bg_h.png")).convert_alpha()

                self.img1_rect = self.img1_org.get_rect()
                inner_w = int(sqrt(pow(self.rect.w / 2, 2) * 2) * 0.8)
                self.img1 = self.scaled_img(self.img1_org, inner_w, inner_w)
                self.img2 = self.scaled_img(self.img2_org, self.rect.w, self.rect.h)
                self.img2h = self.scaled_img(self.img2_org_h, self.rect.w, self.rect.h)

                self.img1_rect = self.img1.get_rect()
                self.img2_rect = self.img2.get_rect()
                pos_x = ((self.board.scale * self.grid_w - inner_w) // 2)
                pos_y = ((self.board.scale * self.grid_h - inner_w) // 2)
                self.img1_pos = (pos_x, pos_y)

                pos2_x = ((self.board.scale * self.grid_w - self.img2_rect.w) // 2)
                pos2_y = ((self.board.scale * self.grid_h - self.img2_rect.h) // 2)
                self.img2_pos = (pos2_x, pos2_y)
            except:
                pass

    def resize_unit(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h
        self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1])
        self.image.fill(self.color)

    def pos_update(self):
        if self.grid_w > 0 and self.grid_h > 0:
            self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1])
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]
        else:
            self.image = pygame.Surface([1, 1])
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

    def scaled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    @property
    def grid_pos(self):
        return [self.grid_x, self.grid_y]

    def set_color(self, color):
        self.color = color

    def set_tint_color(self, color):
        self.tint_color = color

    def update(self, board, **kwargs):
        if self.update_me:
            self.update_me = False
            self.board.mainloop.redraw_needed[0] = True
            self.image.fill(self.color)
            if self.hover:
                self.image.blit(self.img2h, self.img2_pos)
            else:
                self.image.blit(self.img2, self.img2_pos)
            self.image.blit(self.img1, self.img1_pos)

    def mouse_out(self):
        self.board.mainloop.m.reset_titles()
        self.hover = False
        self.update_me = True
        self.update(self.board)

    def mouse_click(self):
        if self.board.mainloop.menu_level == 1:
            self.board.mainloop.menu_level = 2
            self.board.mainloop.menu_category = self.item_id
            self.board.mainloop.m.change_cat(self.item_id)
            self.board.mainloop.m.start_hidden_game(272)
        elif self.board.mainloop.menu_level == 2:
            self.board.mainloop.menu_level = 3
            self.board.mainloop.m.start_hidden_game(self.item_id)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            if not self.hover:
                self.board.mainloop.redraw_needed[1] = True
                self.board.mainloop.info.title = self.cat_obj.title
                self.board.mainloop.info.subtitle = self.cat_obj.subtitle
                self.board.mainloop.info.game_id = "#%03i" % self.cat_obj.cat_id
                self.hover = True
                self.update_me = True
                self.update(self.board)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_click()


class GameIcon(pygame.sprite.Sprite):
    """basic class for all on-board objects"""

    def __init__(self, board, game_obj, grid_x=0, grid_y=0, grid_w=1, grid_h=1, color=(0, 0, 0, 0), lvl_count=None, completions=None):
        pygame.sprite.Sprite.__init__(self)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.game_obj = game_obj
        self.item_id = game_obj.dbgameid
        self.img_src = game_obj.img_src
        self.completions = completions
        self.level_count = lvl_count

        self.challenge_completed = False
        if self.completions is not None:
            if self.completions and 0 not in self.completions:
                self.challenge_completed = True

        self.board = board
        self.color = color

        self.lvl_not_compl_col = (230, 255, 145)

        if self.board.mainloop.scheme is not None:
            self.canvas_color = self.board.mainloop.scheme.u_color
            if self.board.mainloop.scheme.dark:
                self.lvl_not_compl_col = (80, 100, 0)
        else:
            self.canvas_color = (255, 255, 255)

        self.lvl_completed_col = (176, 218, 0)

        self.update_me = True
        self.hover = False
        self.size = 256

        if self.game_obj.img_src2 == "":
            self.challenge = True
        else:
            self.challenge = False

        self.image = pygame.Surface([grid_w * board.scale - 1, grid_h * board.scale - 1])
        self.rect = self.image.get_rect()
        self.rect.topleft = [grid_x * board.scale + 1, grid_y * board.scale + 1]

        if self.challenge and not self.challenge_completed: #not completed
            self.canvas = pygame.Surface([self.size, self.size])
            self.canvas.fill(self.canvas_color)
            self.draw_levels()
            self.canvas2 = self.scaled_img(self.canvas, self.rect.w, self.rect.h)

        self.change_image(self.img_src)
        self.update(self.board.mainloop.game)

    def change_image(self, img_src):
        self.img_src = img_src
        if len(self.img_src) > 0:
            self.update_me = True
            self.img = self.image
            self.img_pos = (0, 0)
            try:
                self.img1_org = pygame.image.load(os.path.join('res', 'icons', self.img_src)).convert_alpha()

                self.img2_org = pygame.image.load(os.path.join('res', 'icons', "menu_bg_n.png")).convert_alpha()
                self.img2_org_h = pygame.image.load(os.path.join('res', 'icons', "menu_bg_h.png")).convert_alpha()

                if not self.challenge:
                    self.img3_org = pygame.image.load(os.path.join('res', 'icons', "menu_ring_01.png")).convert_alpha()
                    self.img3_org_h = pygame.image.load(os.path.join('res', 'icons', "menu_ring_01h.png")).convert_alpha()
                    self.img3 = self.scaled_img(self.img3_org, self.rect.w, self.rect.h)
                    self.img3h = self.scaled_img(self.img3_org_h, self.rect.w, self.rect.h)

                elif self.challenge_completed:
                    self.img3_org = pygame.image.load(os.path.join('res', 'icons', "menu_ring_02.png")).convert_alpha()
                    self.img3_org_h = pygame.image.load(
                        os.path.join('res', 'icons', "menu_ring_02h.png")).convert_alpha()
                    self.img3 = self.scaled_img(self.img3_org, self.rect.w, self.rect.h)
                    self.img3h = self.scaled_img(self.img3_org_h, self.rect.w, self.rect.h)
                else:
                    self.img3_org = pygame.image.load(os.path.join('res', 'icons', "menu_ring_03.png")).convert_alpha()
                    self.img3_org_h = pygame.image.load(
                        os.path.join('res', 'icons', "menu_ring_03h.png")).convert_alpha()
                    self.img3 = self.scaled_img(self.img3_org, self.rect.w, self.rect.h)
                    self.img3h = self.scaled_img(self.img3_org_h, self.rect.w, self.rect.h)

                self.img1_rect = self.img1_org.get_rect()

                self.img1 = self.scaled_img(self.img1_org, self.rect.w // 2, self.rect.h // 2)
                self.img2 = self.scaled_img(self.img2_org, self.rect.w, self.rect.h)
                self.img2h = self.scaled_img(self.img2_org_h, self.rect.w, self.rect.h)

                self.img1_rect = self.img1.get_rect()
                self.img2_rect = self.img2.get_rect()
                pos_x = ((self.board.scale * self.grid_w - self.img1_rect.w) // 2)
                pos_y = ((self.board.scale * self.grid_h - self.img1_rect.h) // 2)
                self.img1_pos = (pos_x, pos_y)

                pos2_x = ((self.board.scale * self.grid_w - self.img2_rect.w) // 2)
                pos2_y = ((self.board.scale * self.grid_h - self.img2_rect.h) // 2)
                self.img2_pos = (pos2_x, pos2_y)
            except:
                pass

    def resize_unit(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h
        self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1], flags=pygame.SRCALPHA)
        self.image.fill(self.color)

    def pos_update(self):
        if self.grid_w > 0 and self.grid_h > 0:
            self.image = pygame.Surface([self.grid_w * self.board.scale - 1, self.grid_h * self.board.scale - 1])
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]
        else:
            self.image = pygame.Surface([1, 1])
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.grid_x * self.board.scale + 1, self.grid_y * self.board.scale + 1]

    def scaled_img(self, image, new_w, new_h):
        'scales image depending on pygame version and bit depth using either smoothscale or scale'
        if image.get_bitsize() in [32, 24] and pygame.version.vernum >= (1, 8):
            img = pygame.transform.smoothscale(image, (new_w, new_h))
        else:
            img = pygame.transform.scale(image, (new_w, new_h))
        return img

    @property
    def grid_pos(self):
        return [self.grid_x, self.grid_y]

    def set_color(self, color):
        self.color = color

    def set_tint_color(self, color):
        self.tint_color = color

    def draw_levels(self):
        r = 127
        r2 = r * 0.78
        m = (self.size - r * 2) // 2
        cx = m + r
        cy = m + r
        if self.level_count is not None:
            levels = self.level_count[1]

            padding = 4
            w = ((360.0 - (levels * padding)) / levels)
            for i in range(levels):
                # get start angle
                a = (i * w + i * padding + 2 - 90) % 360

                #get end angle
                b = ((i + 1) * w + (i) * padding + 2 - 90) % 360
                if a > b:
                    b += 360

                # get points on circle at the above angles
                p = []
                p2 = []

                # add points along the ring
                for n in range(int(a), int(b)+1):
                    x = cx + int(round(r * cos(n * pi / 180)))
                    y = cy + int(round(r * sin(n * pi / 180)))
                    p.append((x, y))

                    x = cx + int(round(r2 * cos(n * pi / 180)))
                    y = cy + int(round(r2 * sin(n * pi / 180)))
                    p2.append((x, y))

                # add reversed points on the inner ring
                p.extend(reversed(p2))

                # finish off - close off the polygon
                p.append(p[0])

                if self.completions is not None:
                    if self.completions[i] > 0:
                        pygame.draw.polygon(self.canvas, self.lvl_completed_col, p, 0)
                    else:
                        pygame.draw.polygon(self.canvas, self.lvl_not_compl_col, p, 0)

    def update(self, board, **kwargs):
        if self.update_me:
            self.update_me = False
            self.board.mainloop.redraw_needed[0] = True
            self.image.fill(self.color)
            if self.challenge and not self.challenge_completed:
                self.image.blit(self.canvas2, self.img2_pos)

            if self.hover:
                self.image.blit(self.img2h, self.img2_pos)
            else:
                self.image.blit(self.img2, self.img2_pos)

            self.image.blit(self.img1, self.img1_pos)

            if self.hover:
                self.image.blit(self.img3h, self.img2_pos)
            else:
                self.image.blit(self.img3, self.img2_pos)

    def mouse_out(self):
        self.board.mainloop.m.reset_titles()
        self.update_me = True
        self.hover = False
        self.update(self.board)

    def mouse_click(self):
            self.board.mainloop.menu_level = 3
            self.board.mainloop.completions = self.completions
            self.board.mainloop.m.start_hidden_game(self.item_id)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            if not self.hover:
                self.hover = True
                self.board.mainloop.redraw_needed[1] = True
                self.board.mainloop.info.title = self.game_obj.title
                self.board.mainloop.info.subtitle = self.game_obj.subtitle
                self.board.mainloop.info.game_id = "#%s/%03i" % (self.game_obj.game_constructor[4:7], self.game_obj.dbgameid)
                self.update_me = True
                self.update(self.board)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_click()


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
        if self.mainloop.menu_level == 1:
            self.categories = []
            for each in self.mainloop.m.categories:
                if each.top_id == self.mainloop.menu_group:
                    l += 1
                    self.categories.append(each)
        else:
            self.games = []
            for each in self.mainloop.m.games_current:
                l += 1
                self.games.append(each)

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
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)
        self.board.board_bg.initcolor = color
        self.board.board_bg.color = color
        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        self.units = []

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

        if self.mainloop.menu_level == 1:
            for i in range(l):
                unit = Category(self.board, self.categories[i], posx[i] + 1, posy[i], 5, 5, self.categories[i].cat_id,
                                self.color, self.categories[i].img_src)
                self.units.append(unit)
                self.board.all_sprites_list.add(unit)
        else:
            for i in range(l):
                #find out the number of levels
                lvl_count = self.mainloop.xml_conn.get_level_count(self.games[i].dbgameid,
                                                                   self.mainloop.config.user_age_group)
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
                            if self.mainloop.config.user_age_group == 7 and show_all_ages[0] <= each[5] <= show_all_ages[1]:
                                completions[each[2] - 1] = each[4]
                            elif self.mainloop.config.user_age_group == each[5]:
                                completions[each[2] - 1] = each[4]

                unit = GameIcon(self.board, self.games[i], posx[i] + 1, posy[i], 5, 5, self.color, lvl_count, completions)
                self.units.append(unit)
                self.board.all_sprites_list.add(unit)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            found = False
            for each in self.units:
                if (each.rect.left < pos[0] < each.rect.right and each.rect.top < pos[1] < each.rect.bottom):
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
