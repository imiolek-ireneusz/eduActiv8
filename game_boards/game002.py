# -*- coding: utf-8 -*-

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 11, 10)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        self.show_info_btn = False

        color1 = ex.hsv_to_rgb(self.mainloop.cl.get_interface_hue(), 50, 255)
        color2 = ex.hsv_to_rgb(self.mainloop.cl.get_interface_hue(), 30, 255)

        font_color = ex.hsv_to_rgb(self.mainloop.cl.get_interface_hue(), 255, 50)
        data = [18, 11]
        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count > data[0]:
            data[0] = x_count

        self.data = data

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.line_color = (200, 200, 200)
        if self.mainloop.scheme is not None:
            self.board.board_bg.line_color = self.mainloop.scheme.u_line_color
        self.board.board_bg.update_me = True

        middle = self.data[0] // 2
        lang_width = 2
        credits_width = (self.data[0] // 2) - lang_width

        # if there's enough space extend the language width by 1
        # the 7 below is hardcoded based on current length of text, may need adjusting if longer credits text added
        if credits_width > 7:
            lang_width = 3
            credits_width -= 1

        left = 0
        colors = [color1, color2]

        # column 1
        top = 0
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Arabic", self.mainloop.config.arabic], colors[top % 2], "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label, ["Ayman Mahmoud"],
                            colors[top % 2], "", 6)

        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Bulgarian", "Български"], colors[top % 2],
                            "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Vanyo Georgiev"], colors[top % 2], "", 6)

        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Catalan", "Català"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Guillem Jover (www.hadrons.org/~guillem/)", "updated by Jordi Mallach"], colors[top % 2],
                            "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Dutch", "Nederlands"], colors[top % 2],
                            "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["translated by Steven Es", "updated by Larry Myerscough"], colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(0, top, lang_width, 1, classes.board.Label, ["English", "English"], colors[top % 2], "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Kamila Roszak-Imiolek", "Ireneusz Imiolek"],
                            colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Finnish", "Suomalainen"], colors[top % 2],
                            "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label, ["Aapo Rantalainen"],
                            colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["French", "Français"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Gino Ingras", "updated by Johnny Jazeix"],
                            colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["German", "Deutsch"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label, "Oliver van der Bürie",
                            colors[top % 2], "", 6)

        top += 2
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Hebrew", "תירבע"], colors[top % 2], "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label, ["Ori Hoch"],
                            colors[top % 2], "", 6)

        # column 2
        top = 0
        left = middle
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Italian", "Italiano"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label, "Giuliano", colors[top % 2],
                            "", 6)

        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Lakota", "Lakȟótiyapi"], colors[top % 2], "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Peter Hill, Derek Lackaff and Matthew Rama"], colors[top % 2], "", 6)

        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Polish", "Polski"], colors[top % 2], "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Kamila Roszak-Imiolek", "Ireneusz Imiolek"], colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Portuguese", "Português"], colors[top % 2],
                            "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label, "Américo Monteiro",
                            colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Russian", "Русский"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Anton Kayukov (Антон Каюков)", "Alexey Loginov (Алексей Логинов)"], colors[top % 2], "",
                            6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Serbian", "Српски"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Miroslav Nikolic (Мирослав Николић)"], colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Spanish", "Español"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            ["Miriam Ruiz (www.miriamruiz.es)", "updated by Mario Izquierdo"],
                            colors[top % 2], "", 6)
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Ukrainian", "Українська"], colors[top % 2],
                            "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label,
                            "Yuri Chornoivan (Юрій Чорноіван)", colors[top % 2], "",
                            6)
        """
        top += 1
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["", ""], colors[top % 2], "", 6)
        self.board.add_unit(left + lang_width, top, credits_width, 1, classes.board.Label, "", colors[top % 2], "", 6)
        """
        # due to the number of people working on this one - it stays at the bottom and spreads across 2 columns
        # update top - to the height of the tallest column
        top = 8
        left = 0
        self.board.add_unit(left, top, lang_width, 1, classes.board.Label, ["Greek", "Ελληνικά"], colors[top % 2], "",
                            6)
        self.board.add_unit(left + lang_width, top, data[0] - lang_width, 1, classes.board.Label, [
            "Στέλιος, versys650gr, sdim, lucinos and other members of The Official Greek Community of Linux Mint,",
            "updated by Alexandros Moskofidis (Αλέξανδρος Μοσκοφίδης) and Yannis Kaskamanidis (Γιάννης Κασκαμανίδης)"], colors[top % 2], "", 6)

        for each in self.board.units:
            each.font_color = font_color
            each.align = 1

    def handle(self, event):
        gd.BoardGame.handle(self, event)

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
