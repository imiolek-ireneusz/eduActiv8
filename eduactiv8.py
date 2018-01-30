#!/usr/bin/env python
# -*- coding: utf-8 -*-

# eduActiv8 - Educational Activities for Kids
# Copyright (C) 2012-2017  Ireneusz Imiolek

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESSED OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
except ImportError:
    android = None

import gc
import os
import pygame
import sys
import time

import classes.config
import classes.sound
import classes.dbconn
import classes.loginscreen
import classes.game_driver
import classes.level_controller
import classes.board
import classes.xml_conn
import classes.menu
import classes.info_bar
import classes.speaker
import classes.colors
import classes.lang
import classes.logoimg
import classes.score_bar
import classes.dialogwnd
import classes.updater

# setting the working directory to the directory of this file
path = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(path)


class GamePlay:
    """The top most class - subclasses the Thread to keep the game and speaker in two different processes
    holds main loop"""

    def __init__(self, speaker, lang, configo, updater):
        # Create / set additional top level game objects and mainloop variables
        self.speaker = speaker
        self.lang = lang
        self.config = configo
        self.updater = updater
        self.first_run = True
        self.updater_started = False
        self.show_dialogwnd = False
        self.game_board = None
        self.cl = classes.colors.Color()
        self.sfx = classes.sound.SoundFX(self)
        self.m = None
        self.userid = -1
        self.score = 0
        self.window_states = ["LOG IN", "GAME"]
        self.window_state = self.window_states[0]
        self.theme = "default"

        # As long as this is False the main loop of a state will keep running. If some action sets it to True the loop ends and so does the current state.
        self.done = False

        # but if you log out you are still given a chance to log back in...
        self.done4good = False
        self.logged_out = False
        self.android = android
        self.draw_func = None
        self.draw_func_args = None

        if android is not None:
            infoObject = pygame.display.Info()
            h = 770
            login_h = 570
            self.android_screen_size = [int(infoObject.current_w * h / infoObject.current_h), h]
            self.android_login_size = [int(infoObject.current_w * login_h / infoObject.current_h), login_h]

    def set_init_vals(self):
        self.redraw_needed = [True, True, True]
        self.game_redraw_tick = [0, 0, 0]
        self.flip_needed = True
        self.init_resize = True
        # menu scrolling speed
        self.menu_speed = 7
        self.menu_tick = 7
        self.done = False

        # mouse over [surface, group of objects, top most object]
        self.mouse_over = [None, None, None]

    def create_subsurfaces(self, game_board):
        self.layout = self.game_board.layout
        # create subsurfaces & set some of the initial layout constraints
        self.menu = self.screen.subsurface(self.game_board.layout.menu_pos)  # menu panel
        self.menu_l = self.menu.subsurface(self.game_board.layout.menu_l_pos)  # category menu
        self.menu_r = self.menu.subsurface(
            self.game_board.layout.menu_r_pos)  # game selection menu - games in a category
        self.game_bg = self.screen.subsurface(self.game_board.layout.game_bg_pos)
        self.game = self.screen.subsurface(self.game_board.layout.game_pos)  # game panel - all action happens here
        self.info_bar = self.screen.subsurface(
            self.game_board.layout.info_bar_pos)  # info panel - level control, game info, etc.
        self.score_bar = self.screen.subsurface(
            self.game_board.layout.score_bar_pos)  # top panel - holding username, score etc.
        self.misio = self.screen.subsurface(
            self.game_board.layout.misio_pos)  # holds an image/logo in top left corner - over menu
        self.misio.set_colorkey((255, 75, 0))
        self.dialogbg = self.screen.subsurface(self.game_board.layout.dialogbg_pos)
        self.dialogwnd = self.screen.subsurface(self.game_board.layout.dialogwnd_pos)
        self.sb.resize()

    def fs_rescale(self, info):
        """rescale the game after fullscreen toggle, this will restart the board
        could not get all the game objects to scale nicely"""
        # pass new screen resolution
        self.game_board.layout.update_layout_fs(self.size[0], self.size[1], self.game_board.layout.x_count,
                                                self.game_board.layout.y_count)
        # load new game - create game objects
        self.game_board.level.load_level()
        if self.game_board.game_type == "Board":
            # adjust the layout to accommodate changes to number of squares automatically added due to screen ratio change
            self.game_board.layout.update_layout(self.game_board.data[0], self.game_board.data[1])
        else:
            self.game_board.layout.update_layout()
        self.create_subsurfaces(self.game_board)
        info.new_game(self.game_board, self.info_bar)
        self.m.reset_scroll()

    def fullscreen_toggle(self, info):
        """toggle between fullscreen and windowed version with CTRL + F
        current activity will be reset"""
        self.redraw_needed = [True, True, True]
        if self.config.fullscreen is True:
            self.config.fullscreen = False
            self.size = self.wn_size[:]
            self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
            self.fs_rescale(info)
        else:
            self.config.fullscreen = True
            self.size = self.fs_size[:]
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
            self.fs_rescale(info)

            pygame.display.flip()

    def on_resize(self, size, info):
        if android is None:
            repost = False
            if size[0] < self.config.size_limits[0]:
                size[0] = self.config.size_limits[0]
                repost = True
            if size[0] > self.config.size_limits[2]:
                size[0] = self.config.size_limits[2]
                repost = True

            if size[1] < self.config.size_limits[1]:
                size[1] = self.config.size_limits[1]
                repost = True
            if size[1] > self.config.size_limits[3]:
                size[1] = self.config.size_limits[3]
                repost = True

            if size != self.fs_size or self.config.platform == "macos":
                self.wn_size = size[:]
                self.size = size[:]
            self.config.settings["screenw"] = self.size[0]
            self.config.settings["screenh"] = self.size[1]
            self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

            self.fs_rescale(info)
            self.config.settings_changed = True
            self.config.save_settings(self.db)
            if repost:
                pygame.event.post(
                    pygame.event.Event(pygame.VIDEORESIZE, size=self.size[:], w=self.size[0], h=self.size[1]))

        if android is not None:
            self.size = self.android_screen_size[:]
        self.info.rescale_title_space()

    def set_up_user(self):
        # load and set up user settings
        self.config.load_settings(self.db, self.userid)
        self.lang.load_language()
        self.speaker.talkative = self.config.settings["espeak"]
        self.speaker.start_server()
        self.config.check_updates = self.config.settings["check_updates"]
        if self.android is None and self.config.check_updates and self.first_run:
            self.first_run = False
            self.updater_started = True
            self.updater.start()
        if self.config.loaded_settings:
            self.config.fullscreen = self.config.settings["full_screen"]
        # message said at the start of the game

        if self.lang.lang != 'he':
            uname = self.user_name
        else:
            uname = ""

        if sys.version_info < (3, 0):
            try:
                self.welcome_msg = self.lang.dp["Hello"] + " " + uname.encode("utf-8") + "! " + self.lang.dp[
                    "Welcome back."]
            except:
                self.welcome_msg = self.lang.dp["Hello"]
        else:
            self.welcome_msg = self.lang.dp["Hello"] + " " + uname + "! " + self.lang.dp["Welcome back."]
        self.speaker.say(self.welcome_msg)  # say welcome message

    def switch_scheme(self, scheme):
        self.redraw_needed = [True, True, True]
        self.scheme_code = scheme
        if scheme is None:
            self.scheme = None
        else:
            self.scheme = eval("classes.colors.%sScheme()" % scheme)
        self.info.create()
        self.fs_rescale(self.info)
        self.m.lang_change()
        self.game_board.line_color = self.game_board.board.board_bg.line_color

        if scheme is None:
            s_id = 0
        elif scheme == "WB":
            s_id = 1
        elif scheme == "BW":
            s_id = 2
        elif scheme == "BY":
            s_id = 3
        self.config.settings["scheme"] = s_id
        self.config.settings_changed = True
        self.config.save_settings(self.db)

    def set_up_scheme(self):
        s_id = self.config.settings["scheme"]
        if s_id == 0:
            scheme = None
        elif s_id == 1:
            scheme = "WB"
        elif s_id == 2:
            scheme = "BW"
        elif s_id == 3:
            scheme = "BY"
        if scheme != self.scheme_code:
            self.switch_scheme(scheme)

    def run(self):
        # start of this Thread
        if android is None:
            pygame.init()

        self.db = classes.dbconn.DBConnection(self.config.file_db, self)
        self.scheme = None  # classes.colors.BYScheme() #BW, WB, BY
        self.scheme_code = None

        self.user_name = None
        self.display_info = pygame.display.Info()
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        self.clock = clock

        while self.done4good is False:
            if self.window_state == "LOG IN":
                self.done = False
                self.set_init_vals()
                if self.config.platform != "windows" and android is None:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
                    self.config.window_pos[0], self.config.window_pos[1])
                if android is None:
                    if not self.logged_out:
                        self.size = [800, 570]
                    else:
                        self.size = self.wn_size
                else:
                    self.size = self.android_login_size
                self.screen = pygame.display.set_mode(self.size)

                pygame.display.set_caption(self.config.window_caption)
                self.loginscreen = classes.loginscreen.LoginScreen(self, self.screen, self.size)
                wait = False
                while self.done is False and self.userid < 0:
                    if android is not None:
                        if android.check_pause():
                            wait = True
                            android.wait_for_resume()
                        else:
                            wait = False
                    if not wait:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (
                                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                self.done = True  # mark to finish the loop and the game
                                self.done4good = True
                            else:
                                self.loginscreen.handle(event)

                        if (self.redraw_needed[0] and self.game_redraw_tick[0] < 3) and self.loginscreen.update_me:
                            self.loginscreen.update()
                            self.game_redraw_tick[0] += 1
                            if self.game_redraw_tick[0] == 2:
                                self.redraw_needed[0] = False
                                self.game_redraw_tick[0] = 0
                            self.flip_needed = True

                        if self.flip_needed:
                            # update the screen with what we've drawn.
                            pygame.display.flip()
                            self.flip_needed = False

                    clock.tick(30)

            if self.window_state == "GAME":
                self.set_up_user()

                self.done = False
                self.set_init_vals()
                if android is None:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.config.window_pos[0], self.config.window_pos[1])
                self.config.fs_width = self.display_info.current_w
                self.config.fs_height = self.display_info.current_h

                # check if there's a size available from previous session, but not on MacOS
                if self.config.platform != "macos" and \
                                self.config.settings["screenw"] >= self.config.size_limits[0] and \
                                self.config.settings["screenh"] >= self.config.size_limits[1] and \
                                self.config.settings["screenw"] <= self.config.size_limits[2] and \
                                self.config.settings["screenh"] <= self.config.size_limits[3]:
                    self.wn_size = [self.config.settings["screenw"], self.config.settings["screenh"]]
                else:
                    self.wn_size = [min(self.config.fs_width - self.config.os_panels_w, self.config.size_limits[2]),
                                    min(self.config.fs_height - self.config.os_panels_h, self.config.size_limits[3])]
                    self.config.settings["screenw"] = self.wn_size[0]
                    self.config.settings["screenh"] = self.wn_size[1]

                self.fs_size = [self.config.fs_width, self.config.fs_height]

                if self.config.fullscreen == True:
                    self.size = self.fs_size[:]
                    flag = pygame.FULLSCREEN
                else:
                    self.size = self.wn_size[:]
                    flag = pygame.RESIZABLE

                # restarting the display to solve a bug causing some of the game area unresponsive after resizing (this bug affected the game only when it was set to start in fullscreen)
                if android is None:
                    pygame.display.quit()
                    pygame.display.init()
                    self.screen = pygame.display.set_mode(self.size, flag)
                else:
                    self.wn_size = self.android_screen_size
                    self.fs_size = self.android_screen_size
                    self.size = self.android_screen_size
                    self.screen = pygame.display.set_mode(self.android_screen_size)

                # Set title of the window
                pygame.display.set_caption(self.config.window_caption)

                # create a list of one sprite holding game image or logo
                self.sprites_list = pygame.sprite.RenderPlain()

                # create a dummy self.game_board variable to be deleted and recreated at the beginning of the main loop
                self.game_board = None

                # kind of a dirty workaround to avoid issues with anti-aliasing on devices not supporting aa compatible bit depths - hopefully it works (not tested - haven't got such device)
                if pygame.display.get_surface().get_bitsize() not in [32, 24]:
                    pygame.draw.aalines = pygame.draw.lines
                    pygame.draw.aaline = pygame.draw.line

                # create game menu / game manager
                self.xml_conn = classes.xml_conn.XMLConn(self)
                m = classes.menu.Menu(self)
                self.m = m

                self.sb = classes.score_bar.ScoreBar(self)

                # create info panel integrated with level control - holds current level/game and some buttons to change levels, etc.
                info = classes.info_bar.InfoBar(self)
                self.info = info

                self.dialog = classes.dialogwnd.DialogWnd(self)

                # create the logo object and add it to the list to render on update
                self.front_img = classes.logoimg.LogoImg(self)
                self.sprites_list.add(self.front_img)

                # -------- Main Program Loop ----------- #
                wait = False
                while self.done is False:
                    if android is not None:
                        if android.check_pause():
                            wait = True
                            android.wait_for_resume()
                        else:
                            if wait:
                                self.redraw_needed = [True, True, True]
                            wait = False

                    if not wait:
                        if m.active_game_id != m.game_started_id:  # or m.active_game_id == 0: #if game id changed since last frame or selected activity is the Language changing panel
                            if self.game_board is not None:
                                # if this is not the first start of a game - the self.game_board has been already 'created' at least once
                                self.game_board.board.clean()  # empty sprite groups, delete lists
                                del (self.game_board)  # delete all previous game objects
                                self.game_board = None
                            # recreate a new game and subsurfaces
                            exec("import game_boards.%s" % m.game_constructor[0:7])
                            game_const = eval("game_boards.%s" % m.game_constructor)
                            self.game_board = game_const(self, self.speaker, self.config, self.size[0],
                                                                 self.size[1])
                            m.game_started_id = m.active_game_id
                            m.l = self.game_board.layout
                            self.create_subsurfaces(self.game_board)
                            info.new_game(self.game_board, self.info_bar)
                            self.set_up_scheme()
                            gc.collect()  # force garbage collection to remove remaining variables to free memory

                        elif self.game_board.level.lvl != self.game_board.level.prev_lvl or self.game_board.update_layout_on_start:
                            # if game id is the same but the level changed load new level
                            self.create_subsurfaces(self.game_board)
                            info.new_game(self.game_board, self.info_bar)
                            self.game_board.level.prev_lvl = self.game_board.level.lvl
                            self.game_board.update_layout_on_start = False
                            gc.collect()

                        if not self.show_dialogwnd:
                            if self.game_board.show_msg == True:
                                # if dialog after completing the game is shown then hide it and load next game
                                if time.time() - self.game_board.level.completed_time > 1.25:
                                    self.game_board.show_msg = False
                                    self.game_board.level.next_board_load()

                        # Process or delegate events
                        for event in pygame.event.get():  # pygame.event.get(): # User did something
                            if event.type == pygame.QUIT or (
                                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                self.dialog.show_dialog(0, self.lang.d["Do you want to exit the game?"])
                            elif event.type == pygame.VIDEORESIZE:
                                if self.config.fullscreen == False:
                                    self.on_resize(list(event.size), info)
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f and (
                                        event.mod & pygame.KMOD_LCTRL):
                                self.fullscreen_toggle(info)
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F5:  # refresh - reload level
                                self.game_board.level.load_level()
                            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                                pos = event.pos
                                if self.show_dialogwnd:
                                    self.dialog.handle(event)
                                else:
                                    if pos[0] > self.game_board.layout.menu_a_w and self.game_board.layout.score_bar_h > \
                                            pos[1]:
                                        if self.mouse_over[0] is not None and self.mouse_over[0] != self.sb:
                                            self.mouse_over[0].on_mouse_out()
                                        self.mouse_over[0] = self.sb

                                        self.sb.handle(event)
                                    elif pos[
                                        0] > self.game_board.layout.menu_a_w and self.game_board.layout.top_margin > \
                                            pos[1]:
                                        if self.mouse_over[0] is not None and self.mouse_over[0] != info:
                                            self.mouse_over[0].on_mouse_out()
                                        self.mouse_over[0] = info

                                        info.handle(event, self.game_board.layout, self)

                                    elif pos[
                                        0] > self.game_board.layout.menu_a_w and self.game_board.layout.top_margin < \
                                            pos[1] < self.game_board.layout.game_h + self.game_board.layout.top_margin:
                                        # clicked on game board
                                        if event.type == pygame.MOUSEBUTTONDOWN and self.game_board.show_msg is True:
                                            # if dialog after completing the game is shown then hide it and load next game
                                            self.game_board.show_msg = False
                                            self.game_board.level.next_board_load()
                                        else:
                                            self.game_board.handle(event)
                                    elif pos[0] < self.game_board.layout.menu_a_w and pos[1] < \
                                            self.game_board.layout.misio_pos[3]:
                                        self.front_img.handle(event)
                                        if self.mouse_over[0] is not None and self.mouse_over[0] != self.front_img:
                                            self.mouse_over[0].on_mouse_out()
                                        self.mouse_over[0] = self.front_img
                                    elif pos[0] < self.game_board.layout.menu_a_w and pos[1] > \
                                            self.game_board.layout.misio_pos[3]:
                                        # clicked on menu panel
                                        if self.mouse_over[0] is not None and self.mouse_over[0] != m:
                                            self.mouse_over[0].on_mouse_out()
                                        self.mouse_over[0] = m
                                        if pos[0] < self.game_board.layout.menu_l_w:
                                            # clicked on category menu
                                            m.handle_menu_l(event)
                                        else:
                                            # clicked on game selection menu
                                            m.handle_menu_r(event, self.game_board.layout.menu_l_w)
                                    else:
                                        # clicked on info panel
                                        if self.mouse_over[0] is not None and self.mouse_over[0] != self.game_board:
                                            self.mouse_over[0].on_mouse_out()
                                        self.mouse_over[0] = self.game_board

                                        if event.type == pygame.MOUSEBUTTONDOWN and self.game_board.show_msg is True:
                                            # if dialog after completing the game is shown then hide it and load next game
                                            self.game_board.show_msg = False
                                            self.game_board.level.next_board_load()
                            elif event.type == pygame.MOUSEBUTTONUP:
                                pos = event.pos
                                if self.show_dialogwnd:
                                    self.dialog.handle(event)
                                else:
                                    gbh = False
                                    if pos[0] < self.game_board.layout.menu_a_w and pos[1] > \
                                            self.game_board.layout.misio_pos[3]:
                                        # clicked on menu panel
                                        if pos[0] < self.game_board.layout.menu_l_w:
                                            # clicked on category menu
                                            m.handle_menu_l(event)
                                        else:
                                            # clicked on game selection menu
                                            m.handle_menu_r(event, self.game_board.layout.menu_l_w)
                                    elif pos[0] < self.game_board.layout.menu_a_w and pos[1] < \
                                            self.game_board.layout.misio_pos[3]:
                                        self.front_img.handle(event)
                                    elif pos[
                                        0] > self.game_board.layout.menu_a_w and self.game_board.layout.top_margin < \
                                            pos[1] < self.game_board.layout.game_h + self.game_board.layout.top_margin:
                                        self.game_board.handle(event)
                                        gbh = True
                                    elif pos[0] > self.game_board.layout.menu_a_w and pos[1] < \
                                            self.game_board.layout.score_bar_h:
                                        self.sb.handle(event)
                                    elif pos[0] > self.game_board.layout.menu_a_w and pos[1] < \
                                            self.game_board.layout.top_margin:
                                        # make the game finish drag, etc.
                                        self.game_board.handle(event)

                                        # handle info button clicks
                                        info.handle(event, self.game_board.layout, self)

                                    if not gbh:
                                        self.game_board.handle(event)

                                    if android is None:
                                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                                    m.swipe_reset()
                            else:
                                if self.show_dialogwnd:
                                    self.dialog.handle(event)
                                else:
                                    # let the game handle other events
                                    self.game_board.handle(event)

                        # trying to save the CPU - only update a subsurface entirely, (can't be bothered to play with dirty sprites)
                        # if anything has changed on the subsurface or it's size has changed

                        # creating list of drawing functions and arguments for each subsurface
                        self.draw_func = [self.game_board.update, info.draw, m.draw_menu]
                        self.draw_func_args = [[self.game], [self.info_bar],
                                          [self.menu, self.menu_l, self.menu_r, self.game_board.layout]]

                        if self.m.scroll_direction != 0:
                            if self.menu_speed == self.menu_tick:
                                self.m.scroll_menu()
                                self.menu_tick = 0
                            else:
                                self.menu_tick += 1

                        # checking if any of the subsurfaces need updating and updating them if needed
                        # in reverse order so the menu is being drawn first

                        for i in range(2, -1, -1):
                            if self.redraw_needed[i]:
                                self.draw_func[i](*self.draw_func_args[i])
                                if i > 0:
                                    self.redraw_needed[i] = False
                                    self.flip_needed = True
                                else:
                                    if self.game_redraw_tick[i] == 2:
                                        self.redraw_needed[i] = False
                                        self.flip_needed = True
                                        self.game_redraw_tick[i] = 0
                                    else:
                                        self.game_redraw_tick[i] += 1

                                # draw the logo over menu - top left corner
                                self.front_img.update()
                                self.sprites_list.draw(self.misio)

                        if self.sb.update_me:
                            self.sb.draw(self.score_bar)
                            self.flip_needed = True
                            self.sb.update_me = False

                        if self.flip_needed:
                            # update the screen with what we've drawn.
                            if self.show_dialogwnd:
                                self.sb.draw(self.score_bar)
                                self.dialog.update()
                            pygame.display.flip()
                            self.flip_needed = False

                        # Limit to 30 frames per second but most redraws are made when needed - less often
                        # 30 frames per second used mainly for event handling
                        self.game_board.process_ai()
                    clock.tick(30)

                # close eSpeak process, quit pygame, collect garbage and exit the game.
                if self.config.settings_changed:
                    self.config.save_settings(self.db)
                clock.tick(300)
        self.db.close()
        if self.speaker.process is not None:
            self.speaker.stop_server()

        # self.speaker.stop_server_en()
        pygame.quit()
        gc.collect()
        if android is None:
            os.sys.exit()


def main():
    # create configuration object
    if android is not None or len(sys.argv) == 1:
        # Map the back button to the escape key.

        if android is not None:
            pygame.init()
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        configo = classes.config.Config(android)

        # create the language object
        lang = classes.lang.Language(configo, path)

        # create the Thread objects and start the threads
        speaker = classes.speaker.Speaker(lang, configo, android)

        updater = classes.updater.Updater(configo, android)

        app = GamePlay(speaker, lang, configo, updater)
        if android is None:
            speaker.start()
        app.run()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "v" or sys.argv[1] == "version":
            from classes.cversion import ver
            print("eduactiv8-%s" % ver)
    else:
        print("Sorry arguments not recognized.")


if __name__ == "__main__":
    main()
