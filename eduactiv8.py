#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# eduActiv8 - Educational Activities for Kids
# Copyright (C) 2012-2022  Ireneusz Imiolek

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
__version__ = "4.22.11"
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
import classes.score_bar
import classes.dialogwnd
import classes.updater
import classes.sizer

# import stresstest

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
        self.layout = None
        self.cl = classes.colors.Color()
        self.sfx = classes.sound.SoundFX(self)
        self.m = None
        self.userid = -1
        self.score = 0
        self.window_states = ["LOG IN", "GAME"]
        self.window_state = self.window_states[0]
        self.theme = "default"
        #self.menu_type = 1 #TODO menu type = 0

        self.menu_group = 0
        self.menu_category = 0
        self.menu_inner_cat = 0
        self.menu_level = 0  # 0 - home, 1 - categories, 2 games in a category
        self.completions = None
        self.completions_dict = None

        # As long as this is False the main loop of a state will keep running. If some action sets it to True the loop ends and so does the current state.
        self.done = False

        # but if you log out you are still given a chance to log back in...
        self.done4good = False
        self.logged_out = False
        self.android = android
        self.draw_func = None
        self.draw_func_args = None

        self.mbtndno = None  # mouse button down object

        if android is not None:
            infoObject = pygame.display.Info()
            h = 770
            login_h = 570
            self.android_screen_size = [int(infoObject.current_w * h / infoObject.current_h), h]
            self.android_login_size = [int(infoObject.current_w * login_h / infoObject.current_h), login_h]

    def set_init_vals(self):
        self.redraw_needed = [True, True, True]
        self.flip_needed = True
        self.init_resize = True
        self.done = False

        # mouse over [surface, group of objects, top most object]
        self.mouse_over = [None, None, None]

    def create_subsurfaces(self):
        # create subsurfaces & set some of the initial layout constraints

        self.game_bg = self.screen.subsurface(self.sizer.game_bg_pos)
        #self.game = self.screen.subsurface(self.game_board.layout.game_pos)  # game panel - all action happens here
        self.info_bar = self.screen.subsurface(self.sizer.info_bar_pos)  # info panel - level control, game info, etc.
        self.score_bar = self.screen.subsurface(self.sizer.score_bar_pos)  # top panel - holding username, score etc.
        self.dialogbg = self.screen.subsurface(self.sizer.dialogbg_pos)
        self.dialogwnd = self.screen.subsurface(self.sizer.dialogwnd_pos)
        self.sb.resize()

    def recreate_game_screen(self):
        try:
            self.game = self.screen.subsurface(self.layout.game_pos)
        except:
            pass

    def fs_rescale(self, info):
        """rescale the game after fullscreen toggle, this will restart the board
        could not get all the game objects to scale nicely"""
        # pass new screen resolution
        self.sizer.update_sizer(self.size[0], self.size[1])
        self.game_board.layout.update_layout_fs(self.size[0], self.size[1], self.game_board.layout.x_count,
                                                self.game_board.layout.y_count)
        # load new game - create game objects
        self.game_board.level.load_level()
        # adjust the layout to accommodate changes to number of squares automatically added due to screen ratio change
        self.game_board.layout.update_layout(self.game_board.data[0], self.game_board.data[1])
        self.create_subsurfaces()
        self.game = self.screen.subsurface(self.game_board.layout.game_pos)
        info.new_game(self.game_board, self.info_bar)
        #self.m.reset_scroll()

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
            # repost = False
            if size[0] < self.config.size_limits[0]:
                size[0] = self.config.size_limits[0]
                # repost = True
            if size[0] > self.config.size_limits[2]:
                size[0] = self.config.size_limits[2]
                # repost = True

            if size[1] < self.config.size_limits[1]:
                size[1] = self.config.size_limits[1]
                # repost = True
            if size[1] > self.config.size_limits[3]:
                size[1] = self.config.size_limits[3]
                # repost = True

            if size != self.fs_size or self.config.platform == "macos":
                self.wn_size = size[:]
                self.size = size[:]
            self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

            self.sizer.update_sizer(self.size[0], self.size[1])
            self.fs_rescale(info)
            #self.create_subsurfaces()

            self.config.settings["screenw"] = self.size[0]
            self.config.settings["screenh"] = self.size[1]
            self.config.settings_changed = True
            self.config.save_settings(self.db)

            # TODO check if commenting out the following code affects Windows/MacOS
            """
            if repost:
                pygame.event.post(
                    pygame.event.Event(pygame.VIDEORESIZE, size=self.size[:], w=self.size[0], h=self.size[1]))
            """

        if android is not None:
            self.size = self.android_screen_size[:]
        self.info.rescale_title_space()

    def set_up_user(self):
        # load and set up user settings
        self.config.load_settings(self.db, self.userid)
        self.lang.load_language()
        self.completions_dict = dict()
        self.speaker.talkative = self.config.settings["espeak"]
        self.speaker.start_server()
        self.config.check_updates = self.config.settings["check_updates"]
        if self.android is None and self.config.check_updates and self.first_run:
            self.first_run = False
            self.updater_started = True
            if self.updater is not None:
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
        # self.m.lang_change()
        self.game_board.line_color = self.game_board.board.board_bg.line_color

        if scheme is None:
            s_id = 0
        elif scheme == "WB":
            s_id = 1
        elif scheme == "BW":
            s_id = 2
        elif scheme == "BY":
            s_id = 3

        self.cl.reset_default_colors_sv(self.scheme)
        self.config.settings["scheme"] = s_id
        self.config.settings_changed = True
        self.config.save_settings(self.db)
        self.info.realign()

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
        self.clock = pygame.time.Clock()

        while self.done4good is False:
            if self.window_state == "LOG IN":
                self.done = False
                self.set_init_vals()
                """
                if self.config.platform != "windows" and android is None:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
                    self.config.window_pos[0], self.config.window_pos[1])
                """
                os.environ['SDL_VIDEO_CENTERED'] = '1'
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

                        if self.redraw_needed[0] and self.loginscreen.update_me:
                            self.loginscreen.update()
                            self.flip_needed = True

                        if self.flip_needed:
                            # update the screen with what we've drawn.
                            pygame.display.flip()
                            self.flip_needed = False

                    self.clock.tick(30)

            if self.window_state == "GAME":
                self.set_up_user()

                self.done = False
                self.game_const = None
                self.set_init_vals()
                """
                if android is None:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.config.window_pos[0], self.config.window_pos[1])
                """

                os.environ['SDL_VIDEO_CENTERED'] = '1'

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
                    # set default screen size - as small as possible
                    #self.wn_size = [min(self.config.fs_width - self.config.os_panels_w, self.config.size_limits[2]),
                    #                min(self.config.fs_height - self.config.os_panels_h, self.config.size_limits[3])]
                    self.wn_size = [800, 600]
                    self.config.settings["screenw"] = self.wn_size[0]
                    self.config.settings["screenh"] = self.wn_size[1]

                self.fs_size = [self.config.fs_width, self.config.fs_height]

                if self.config.fullscreen:
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
                self.sizer = classes.sizer.Sizer(self, self.size[0], self.size[1])
                self.sb = classes.score_bar.ScoreBar(self)
                self.create_subsurfaces()

                # display splash screen during loading
                self.screen.fill((255, 255, 255))
                loading_image = pygame.image.load(os.path.join('res', 'images', 'schemes', 'white', 'home_logo.png'))
                self.screen.blit(loading_image, ((self.size[0] - 750) // 2, (self.size[1] - 180) // 2))
                pygame.display.flip()

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

                # create info panel integrated with level control - holds current level/game and some buttons to change levels, etc.
                info = classes.info_bar.InfoBar(self)
                self.info = info

                self.dialog = classes.dialogwnd.DialogWnd(self)

                # recreate the icon
                icon = pygame.image.load(os.path.join('res', 'icon', 'ico256.png'))
                pygame.display.set_icon(icon)

                new_size = self.size[:]
                resizing = False
                frames_since_resize = 0

                # -------- Main Program Loop ----------- #
                wait = False
                while self.done is False:
                    # uncomment the following line to test all activities across multiple languages as specified in the stresstest.py
                    # stresstest.step(self)

                    resizing_this_frame = False
                    if android is not None:
                        if android.check_pause():
                            wait = True
                            android.wait_for_resume()
                        else:
                            if wait:
                                self.redraw_needed = [True, True, True]
                            wait = False

                    if not wait:
                        if m.active_game_id != m.game_started_id:  # if game id changed since last frame or selected activity is the Language changing panel
                            if self.game_board is not None:
                                # if this is not the first start of a game - the self.game_board has been already 'created' at least once
                                self.game_board.board.clean()  # empty sprite groups, delete lists
                                del (self.game_board)  # delete all previous game objects
                                self.game_board = None

                            exec("import game_boards.%s" % m.game_constructor[0:7])
                            self.game_const = eval("game_boards.%s" % m.game_constructor)
                            self.game_board = self.game_const(self, self.speaker, self.config, self.size[0], self.size[1])
                            m.game_started_id = m.active_game_id
                            self.layout = self.game_board.layout
                            self.recreate_game_screen()
                            info.new_game(self.game_board, self.info_bar)
                            self.set_up_scheme()
                            gc.collect()  # force garbage collection to remove remaining variables to free memory

                        elif self.game_board.level.lvl != self.game_board.level.prev_lvl:
                            # if game id is the same but the level changed load new level

                            self.layout = self.game_board.layout
                            self.sizer.update_sizer(self.size[0], self.size[1])
                            self.recreate_game_screen()
                            info.new_game(self.game_board, self.info_bar)
                            self.game_board.level.prev_lvl = self.game_board.level.lvl
                            self.redraw_needed[0] = True

                            gc.collect()

                        if not self.show_dialogwnd:
                            if self.game_board.show_msg:
                                self.sb.draw(self.score_bar)
                                self.redraw_needed = [True, True, True]
                                if time.time() - self.game_board.level.completed_time > 1.5:
                                    self.game_board.show_msg = False
                                    self.game_board.level.next_board_load()
                                    self.redraw_needed = [True, True, True]

                        # Process or delegate events
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (
                                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                self.done = True
                                self.done4good = True
                                # don't show dialog if closing with window manager or ESC
                                # self.dialog.show_dialog(0, self.lang.d["Do you want to exit the game?"])
                            elif event.type == pygame.VIDEORESIZE:
                                if not self.config.fullscreen:
                                    new_size = list(event.size)
                                    resizing = True
                                    resizing_this_frame = True
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f and (
                                        event.mod & pygame.KMOD_LCTRL):
                                # eduActiv8 crashes in fullscreen mode in pygame 2 so temporarily not available
                                if pygame.version.vernum[0] < 2:
                                    self.fullscreen_toggle(info)
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F5:  # refresh - reload level
                                self.game_board.level.load_level()
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F8:
                                # auto resize window to prep for screenshots and video
                                self.on_resize([1280, 720], self.info)
                            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                                pos = event.pos
                                if self.show_dialogwnd:
                                    self.dialog.handle(event)
                                else:
                                    if pos[0] > 0 and self.sizer.score_bar_h > pos[1]:
                                        if self.mouse_over[0] is not None and self.mouse_over[0] != self.sb:
                                            self.mouse_over[0].on_mouse_out()
                                        self.mouse_over[0] = self.sb

                                        self.sb.handle(event)
                                    elif pos[0] > 0 and self.sizer.top_margin > pos[1]:
                                        if self.mouse_over[0] is not None and self.mouse_over[0] != info:
                                            self.mouse_over[0].on_mouse_out()
                                        self.mouse_over[0] = info

                                        info.handle(event, self.game_board.layout, self)

                                    elif pos[0] > 0 and self.sizer.top_margin < \
                                            pos[1] < self.game_board.layout.game_h + self.sizer.top_margin:
                                        # clicked on game board
                                        if event.type == pygame.MOUSEBUTTONDOWN and self.game_board.show_msg is True:
                                            # if dialog after completing the game is shown then hide it and load next game
                                            self.game_board.show_msg = False
                                            self.game_board.level.next_board_load()
                                        else:
                                            self.game_board.handle(event)
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
                                    if pos[0] > 0 and self.sizer.top_margin < \
                                            pos[1] < self.game_board.layout.game_h + self.sizer.top_margin:
                                        self.game_board.handle(event)
                                        gbh = True
                                    elif pos[0] > 0 and pos[1] < self.sizer.score_bar_h:
                                        self.sb.handle(event)
                                    elif pos[0] > 0 and pos[1] < self.sizer.top_margin:
                                        # make the game finish drag, etc.
                                        self.game_board.handle(event)

                                        # handle info button clicks
                                        info.handle(event, self.game_board.layout, self)

                                    if not gbh:
                                        self.game_board.handle(event)

                                    if android is None:
                                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                            else:
                                if self.show_dialogwnd:
                                    self.dialog.handle(event)
                                else:
                                    # let the game handle other events
                                    self.game_board.handle(event)
                        if resizing:
                            # changed the window resizing behaviour:
                            # only resize contents 15 frames after the user stopped resizing
                            if not resizing_this_frame:
                                frames_since_resize += 1
                                if frames_since_resize > 15:
                                    self.on_resize(new_size, info)
                                    resizing = False
                                    frames_since_resize = 0
                            else:
                                frames_since_resize = 0

                        # checking if any of the subsurfaces need updating and updating them if needed
                        if self.redraw_needed[1]:
                            info.draw(self.info_bar)
                            self.redraw_needed[1] = False
                            self.flip_needed = True

                        if self.redraw_needed[0]:
                            self.game_board.update(self.game)
                            self.redraw_needed[0] = False
                            self.flip_needed = True

                        if self.sb.update_me:
                            self.sb.draw(self.score_bar)
                            self.flip_needed = True
                            self.sb.update_me = False

                        if self.flip_needed:
                            # update the screen with what we've drawn.
                            if self.show_dialogwnd:
                                if self.dialog.dialog_type != 2 or (self.dialog.dialog_type == 2 and time.time() - self.game_board.level.completed_time > 0.5):
                                    self.sb.draw(self.score_bar)
                                    self.dialog.update()

                            pygame.display.flip()
                            self.flip_needed = False

                        if self.show_dialogwnd:
                            if self.dialog.dialog_type == 2:
                                self.flip_needed = True

                        # Limit to 30 frames per second but most redraws are made when needed - less often
                        # 30 frames per second used mainly for event handling
                        self.game_board.process_ai()
                    self.clock.tick(30)

                # close eSpeak process, quit pygame, collect garbage and exit the game.
                if self.config.settings_changed:
                    self.config.save_settings(self.db)
                self.clock.tick(300)
        self.db.close()
        if self.speaker.process is not None:
            self.speaker.stop_server()

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
        else:
            icon = pygame.image.load(os.path.join('res', 'icon', 'ico256.png'))
            pygame.display.set_icon(icon)
        configo = classes.config.Config(android)

        # create the language object
        lang = classes.lang.Language(configo, path)

        # create the Thread objects and start the threads
        speaker = classes.speaker.Speaker(lang, configo, android)

        #cancel out checking for updates so that the PC does not have to connect to the Internet
        updater = None #classes.updater.Updater(configo, android)

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
