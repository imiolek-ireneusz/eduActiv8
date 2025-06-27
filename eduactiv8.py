#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# eduActiv8 - Educational Activities for Kids
# Copyright (C) 2012-2025  Ireneusz Imiolek

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
# Although currently there's no way to build for Android, especially that
# the application is being updated to Python 3+ we are still keeping the
# Android logic.

# import stresstest

__version__ = "4.25.07"
try:
    import android
except ImportError:
    android = None

import gc
import os
import pygame
import sys
import time
import logging
import importlib
from abc import ABC, abstractmethod  # For abstract base classes

# Core classes
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

from classes.enums import MenuLevel, DialogType, GamePlayConfig

# setting the working directory to the directory of this file
path = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(path)

SPLASH_IMAGE_PATH = os.path.join('res', 'images', 'schemes', 'white', 'home_logo.png')
ICON_PATH = os.path.join('res', 'icon', 'ico256.png')


class BaseState(ABC):
    """
    Abstract Base Class for all game states.
    Each state will inherit from this and implement its specific logic.
    """

    def __init__(self, game_play):
        self.game_play = game_play  # Reference to the main GamePlay instance

    @abstractmethod
    def enter(self):
        """Called when entering this state. Used for initialization."""
        pass

    @abstractmethod
    def exit(self):
        """Called when exiting this state. Used for cleanup."""
        pass

    @abstractmethod
    def handle_event(self, event):
        """Handles Pygame events specific to this state."""
        pass

    @abstractmethod
    def update(self):
        """Updates game logic for this state."""
        pass

    @abstractmethod
    def draw(self):
        """Renders the screen for this state."""
        pass


class LoginState(BaseState):
    """Represents the application's login screen state."""

    def __init__(self, game_play):
        super().__init__(game_play)
        self.loginscreen = None  # Will be initialized in enter()

    def enter(self):
        """Initializes the login screen display and elements."""
        logging.info("Entering LoginState.")
        gp = self.game_play

        gp.set_init_vals()  # Reset global flags for new state

        # Determine size for login screen
        if gp.android is None:
            # For desktop, use a fixed login size unless logged out (then use wn_size)
            login_size = [GamePlayConfig.DEFAULT_WINDOWED_WIDTH, GamePlayConfig.DEFAULT_WINDOWED_HEIGHT] if not gp.logged_out else gp.wn_size[:]
        else:
            login_size = gp.android_login_size[:]

        gp._set_display_mode(login_size, False)  # Login screen is always windowed
        pygame.display.set_caption(gp.config.window_caption)

        # Initialize LoginScreen UI
        self.loginscreen = classes.loginscreen.LoginScreen(gp, gp.screen, login_size)
        gp.flip_needed = True

    def exit(self):
        """Cleans up login screen resources."""
        logging.info("Exiting LoginState.")
        if self.loginscreen:
            del self.loginscreen
            self.loginscreen = None
        self.game_play.logged_out = False

    def handle_event(self, event):
        """Handles events for the LoginState."""
        gp = self.game_play

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            gp.running = False  # Signal application exit
            return

        # Delegate event handling to the login screen UI
        if self.loginscreen:
            self.loginscreen.handle(event)

        # Check if login was successful and transition to GameState
        if gp.userid != -1:  # userid is set by loginscreen upon successful login
            logging.debug(f"UserID set successfully. UserID: {gp.userid}, UserName: {gp.user_name}")
            gp.change_state(GameState(gp))

    def update(self):
        """Updates login screen logic."""
        # Check Android pause/resume
        gp = self.game_play
        if gp.android is not None:
            if gp.android.check_pause():
                gp.android.wait_for_resume()
                gp.redraw_needed = [True, True, True]  # Force redraw on resume

        if self.loginscreen and self.loginscreen.update_me:  # Check if login screen needs internal update
            self.loginscreen.update()
            #gp.redraw_needed[0] = True  # Indicate that the login screen area needs redraw

    def draw(self):
        """Draws the login screen."""
        gp = self.game_play
        if gp.redraw_needed[0] and self.loginscreen:
            # The loginscreen.update() should have already drawn to its internal surface
            # If it draws directly to gp.screen, this blit is redundant.
            # Assuming loginscreen manages its own drawing onto self.game_play.screen.
            self.loginscreen.draw(gp.screen)  # Ensure loginscreen has a draw method that takes screen
            gp.flip_needed = True

        if gp.flip_needed:
            pygame.display.flip()
            gp.flip_needed = False


class GameState(BaseState):
    """Represents the main game screen state."""

    def __init__(self, game_play):
        super().__init__(game_play)
        # Initialize UI elements that persist across game instances
        self.game_board = None
        self.xml_conn = None
        self.m = None
        self.info = None
        self.dialog = None
        self.sizer = None
        self.sb = None

        # Flags for resize debounce
        self.new_size = self.game_play.size[:]
        self.resizing = False
        self.frames_since_resize = 0

    def enter(self):
        """Initializes the game screen, including setting up display mode,
        loading UI elements, and displaying a splash screen."""
        logging.info("Entering GameState.")
        gp = self.game_play
        gp.set_init_vals()  # Reset global flags for new state

        gp.set_up_user()  # Load user settings, language, start speaker etc.

        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Set before any pygame.display.init() calls
        gp.config.fs_width = gp.display_info.current_w
        gp.config.fs_height = gp.display_info.current_h

        # Determine initial windowed size based on settings or default
        if gp.config.platform != "macos" and \
                gp.config.settings["screenw"] >= gp.config.size_limits[0] and \
                gp.config.settings["screenh"] >= gp.config.size_limits[1] and \
                gp.config.settings["screenw"] <= gp.config.size_limits[2] and \
                gp.config.settings["screenh"] <= gp.config.size_limits[3]:
            gp.wn_size = [gp.config.settings["screenw"], gp.config.settings["screenh"]]
        else:
            gp.wn_size = [GamePlayConfig.DEFAULT_WINDOWED_WIDTH, GamePlayConfig.DEFAULT_WINDOWED_HEIGHT]
            gp.config.settings["screenw"] = gp.wn_size[0]
            gp.config.settings["screenh"] = gp.wn_size[1]

        gp.fs_size = [gp.config.fs_width, gp.config.fs_height]

        # Set initial display mode based on platform and fullscreen config
        if gp.android is not None:
            gp.wn_size = gp.android_screen_size[:]  # Ensure Android sizes are consistent
            gp.fs_size = gp.android_screen_size[:]
            gp.size = gp.android_screen_size[:]
            gp._set_display_mode(gp.android_screen_size, False)
        else:
            gp.size = gp.fs_size[:] if gp.config.fullscreen else gp.wn_size[:]
            gp._set_display_mode(gp.size, gp.config.fullscreen)

        pygame.display.set_caption(gp.config.window_caption)

        # Initialize core UI components
        self.sizer = classes.sizer.Sizer(gp, gp.size[0], gp.size[1])
        gp.sizer = self.sizer  # Update GamePlay's sizer reference

        self.sb = classes.score_bar.ScoreBar(gp)
        gp.sb = self.sb  # Update GamePlay's score_bar reference

        gp.create_subsurfaces()  # Re-create global subsurfaces based on new sizer

        # Display splash screen during loading
        gp.screen.fill((255, 255, 255))
        try:
            loading_image = pygame.image.load(SPLASH_IMAGE_PATH)
            image_x = (gp.size[0] - loading_image.get_width()) // 2
            image_y = (gp.size[1] - loading_image.get_height()) // 2
            gp.screen.blit(loading_image, (image_x, image_y))
        except pygame.error as e:
            logging.error(f"Could not load splash image from {SPLASH_IMAGE_PATH}: {e}")
            font = pygame.font.Font(None, 50)
            text_surface = font.render("Loading...", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(gp.size[0] // 2, gp.size[1] // 2))
            gp.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        if pygame.display.get_surface().get_bitsize() not in [32, 24]:
            pygame.draw.aalines = pygame.draw.lines
            pygame.draw.aaline = pygame.draw.line

        # First, initialize xml_conn
        self.xml_conn = classes.xml_conn.XMLConn(gp)
        gp.xml_conn = self.xml_conn  # Update GamePlay's reference

        # Then, pass xml_conn to Menu
        self.m = classes.menu.Menu(gp, self.xml_conn)
        gp.m = self.m  # Update GamePlay's menu reference

        self.info = classes.info_bar.InfoBar(gp)
        gp.info = self.info  # Update GamePlay's info_bar reference

        self.dialog = classes.dialogwnd.DialogWnd(gp)
        gp.dialog = self.dialog  # Update GamePlay's dialog reference

        # Set application icon
        try:
            icon = pygame.image.load(ICON_PATH)
            pygame.display.set_icon(icon)
        except pygame.error as e:
            logging.error(f"Could not load application icon from {ICON_PATH}: {e}")

        # Initial game board setup (will be loaded by the game loop if active_game_id is set)
        self.game_board = None  # actual game board created on demand
        gp.game_board = self.game_board

        gp.redraw_needed = [True, True, True]  # Force full redraw on state entry

    def exit(self):
        """Cleans up game screen resources."""
        logging.info("Exiting GameState.")
        gp = self.game_play
        if self.game_board:
            self.game_board.board.clean()
            del self.game_board
            self.game_board = None
        if self.xml_conn: del self.xml_conn
        if self.m: del self.m
        if self.info: del self.info
        if self.dialog: del self.dialog
        if self.sizer: del self.sizer
        if self.sb: del self.sb
        # Ensure settings are saved on exit
        if gp.config.settings_changed:
            logging.info("Saving settings before GameState exit.")
            gp.config.save_settings(gp.db)
        gc.collect()

    def handle_event(self, event):
        """Handles events for the GameState."""
        gp = self.game_play

        if event.type == pygame.QUIT:
            # show a confirmation dialog before quitting
            self.dialog.show_dialog(DialogType.EXIT_GAME, gp.lang.d["Do you want to exit the game?"])
            return  # Don't exit immediately, wait for dialog response

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and (event.mod & pygame.KMOD_LCTRL):
                gp.fullscreen_toggle(self.info)
            elif event.key == pygame.K_F5:  # refresh - reload level
                if self.game_board and self.game_board.level:
                    self.game_board.level.load_level()
                    gp.redraw_needed[0] = True  # Force game board redraw
            elif event.key == pygame.K_F8:
                gp.on_resize([1280, 720], self.info)  # Auto resize for screenshots
            elif event.key == pygame.K_ESCAPE:
                # show a confirmation dialog for logout or exit
                # If dialog is already shown, escape might close it
                if gp.show_dialogwnd:
                    self.dialog.hide_dialog()
                else:
                    self.dialog.show_dialog(DialogType.EXIT_GAME, gp.lang.d["Do you want to exit the game?"])
                return  # Don't process other events while dialog decision is pending

        elif event.type == pygame.VIDEORESIZE:
            # Delegate resize event, but actual update will be debounced
            if not gp.config.fullscreen:
                self.new_size = list(event.size)
                self.resizing = True
                self.frames_since_resize = 0  # Reset debounce counter
            return  # Event processed, return early

        # If a dialog is shown, it takes precedence for mouse/keyboard events
        if gp.show_dialogwnd:
            self.dialog.handle(event)
            return  # Dialog consumed the event, no need to process further for game elements

        # Delegate events to game elements if no dialog is active
        # Handle mouse interaction with UI elements
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            if event.type == pygame.MOUSEBUTTONDOWN:
                logging.debug("Handling mouse button down event in GameState.")
            if event.type == pygame.MOUSEBUTTONUP:
                logging.debug("Handling mouse button up event in GameState.")
            self._handle_mouse_event(event)
        elif self.game_board:  # Delegate to game board for other unhandled events
            self.game_board.handle(event)

    def _handle_mouse_event(self, event):
        """
        Helper to handle mouse events for game screen elements.
        Ensures that mouse events are handled only once by the relevant component.
        """
        gp = self.game_play
        pos = event.pos
        event_handled = False # Flag to track if the event has been handled

        # Check interaction with score bar
        if pos[0] > 0 and self.sizer.score_bar_h > pos[1]:
            if gp.mouse_over[0] is not None and gp.mouse_over[0] != self.sb:
                gp.mouse_over[0].on_mouse_out()
            gp.mouse_over[0] = self.sb
            self.sb.handle(event)
            event_handled = True
        # Check interaction with info bar
        elif pos[0] > 0 and self.sizer.top_margin > pos[1]:
            if gp.mouse_over[0] is not None and gp.mouse_over[0] != self.info:
                gp.mouse_over[0].on_mouse_out()
            gp.mouse_over[0] = self.info
            self.info.handle(event, self.game_board.layout, gp)
            event_handled = True
        # Check interaction with game board area
        elif gp.game_board and pos[0] > 0 and self.sizer.top_margin < \
                pos[1] < self.game_board.layout.game_h + self.sizer.top_margin:
            # If a message is shown on the game board, a click dismisses it
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_board.show_msg is True:
                self.game_board.show_msg = False
                self.game_board.level.next_board_load()
            else:
                # Delegate to game_board's handle method for internal menu/game element interaction
                self.game_board.handle(event)
            if gp.mouse_over[0] is not None and gp.mouse_over[0] != gp.game_board:
                gp.mouse_over[0].on_mouse_out()
            gp.mouse_over[0] = gp.game_board
            event_handled = True
        else:
            # Mouse is outside defined UI areas (score bar, info bar, game board)
            if gp.mouse_over[0] is not None and gp.mouse_over[0] != gp.game_board:
                gp.mouse_over[0].on_mouse_out()
            gp.mouse_over[0] = gp.game_board # Still might be relevant for some global game_board logic

            # Handle specific click to dismiss message if clicked outside explicit UI elements but within game_bg
            if event.type == pygame.MOUSEBUTTONDOWN and gp.game_board and gp.game_board.show_msg is True:
                gp.game_board.show_msg = False
                gp.game_board.level.next_board_load()
                event_handled = True # Event handled by message dismissal

        # Only reset cursor if mouse button is released and not on Android
        if event.type == pygame.MOUSEBUTTONUP and gp.android is None:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)


    def update(self):
        """Updates game logic for the GameState."""
        gp = self.game_play

        # Check Android pause/resume
        if gp.android is not None:
            if gp.android.check_pause():
                gp.android.wait_for_resume()
                gp.redraw_needed = [True, True, True]  # Force redraw on resume

        # Handle debounced window resizing for desktop
        if self.resizing:
            self.frames_since_resize += 1
            if self.frames_since_resize > GamePlayConfig.RESIZE_DEBOUNCE_FRAMES:
                gp.on_resize(self.new_size, self.info)  # Perform the actual resize
                self.resizing = False
                self.frames_since_resize = 0
                # Dialog also needs to resize when main window resizes
                if self.dialog:
                    self.dialog.resize()  # Call resize on dialog
                self.info.rescale_title_space()  # Info bar also needs rescale
                gp.redraw_needed = [True, True, True]  # Force full redraw after resize

        # Check if a new game needs to be loaded (different game_id)
        if self.m.active_game_id != self.m.game_started_id:
            logging.info(f"Loading new screen: G-{str(self.m.game_constructor)[4:7]}.")
            # Clean up previous game board resources
            if self.game_board is not None:
                self.game_board.board.clean()
                del self.game_board
                self.game_board = None
                gp.game_board = None  # Clear GamePlay's reference too

            try:
                module_name, class_name = self.m.game_constructor.split(".")
                module = importlib.import_module(f"game_boards.{module_name}")
                game_const = getattr(module, class_name)
                self.game_board = game_const(gp, gp.speaker, gp.config, gp.size[0], gp.size[1])
                gp.game_board = self.game_board  # Update GamePlay's reference
            except (ImportError, AttributeError) as e:
                logging.error(f"Failed to load game constructor {self.m.game_constructor}: {e}")
                # Fallback to menu or show error dialog gracefully
                self.dialog.show_dialog(DialogType.INFO_ONLY, gp.lang.d["Failed to load game. Please try another."])
                # Consider transitioning back to login/menu state if game loading is critical
                # gp.change_state(LoginState(gp))
                return

            self.m.game_started_id = self.m.active_game_id
            gp.layout = self.game_board.layout
            gp.recreate_game_screen()  # Recreate game surface for new game
            self.info.new_game(self.game_board, gp.info_bar)
            gp.set_up_scheme()
            gc.collect()

        # Check if the level within the current game has changed
        elif self.game_board and self.game_board.level.lvl != self.game_board.level.prev_lvl and self.m.game_started_id not in [4, 5]:
            if self.m.game_started_id  > 6:
                logging.info(f"Loading new level: {self.game_board.level.lvl}")
            gp.layout = self.game_board.layout
            self.sizer.update_sizer(gp.size[0], gp.size[1])
            gp.recreate_game_screen()
            self.info.new_game(self.game_board, gp.info_bar)
            self.game_board.level.prev_lvl = self.game_board.level.lvl
            gp.redraw_needed[0] = True  # Force game board redraw
            gc.collect()

        # Check if the menu content (e.g., menu_level) has changed for the current menu screen
        elif self.game_board and gp.menu_content_changed:
            logging.info("Menu content changed, re-initializing current activity.")
            # Clean up the existing game board instance
            if self.game_board is not None:
                self.game_board.board.clean()
                del self.game_board
                self.game_board = None
                gp.game_board = None

            # Re-create the current game board
            try:
                module_name, class_name = self.m.game_constructor.split(".")
                module = importlib.import_module(f"game_boards.{module_name}")
                game_const = getattr(module, class_name)
                self.game_board = game_const(gp, gp.speaker, gp.config, gp.size[0], gp.size[1])
                gp.game_board = self.game_board  # Update GamePlay's reference
            except (ImportError, AttributeError) as e:
                logging.error(f"Failed to re-load game constructor {self.m.game_constructor} for menu update: {e}")
                self.dialog.show_dialog(DialogType.INFO_ONLY, gp.lang.d["Failed to re-load game. Please try again."])
                # Consider reverting menu state or transitioning
                return

            gp.layout = self.game_board.layout
            gp.recreate_game_screen()
            self.info.new_game(self.game_board, gp.info_bar)
            gp.set_up_scheme()
            gc.collect()
            gp.menu_content_changed = False  # Reset the flag after handling the change

        # Handle post-game message display (if no dialog is active)
        if not gp.show_dialogwnd and self.game_board and self.game_board.show_msg:
            self.sb.draw(gp.score_bar)
            gp.redraw_needed = [True, True, True]
            if time.time() - self.game_board.level.completed_time > 1.5:
                self.game_board.show_msg = False
                self.game_board.level.next_board_load()
                gp.redraw_needed = [True, True, True]

        # Update game board and AI if they exist
        if self.game_board:
            self.game_board.process_ai()  # AI processing
            # Update specific game elements if not handled by self.game_board.update()
            # self.game_board.update() # If game_board has its own update logic without surface parameter

        # Debounced settings save
        if gp.config.settings_changed:
            gp.settings_save_timer += gp.clock.get_time() / 1000.0  # Add delta time in seconds
            if gp.settings_save_timer >= gp.SETTINGS_SAVE_DELAY:
                logging.info("Debounced saving settings...")
                gp.config.save_settings(gp.db)
                gp.config.settings_changed = False
                gp.settings_save_timer = 0.0

    def draw(self):
        """Draws the GameState screen."""
        gp = self.game_play

        # Draw main game elements if redraw is needed
        if gp.redraw_needed[1]:  # Info bar
            self.info.draw(gp.info_bar)
            gp.redraw_needed[1] = False
            gp.flip_needed = True

        if gp.redraw_needed[0]:  # Game board
            if self.game_board and gp.game:  # Ensure game_board and game surface exist
                self.game_board.update(gp.game)  # Assuming game_board.update draws to gp.game
            gp.redraw_needed[0] = False
            gp.flip_needed = True

        if self.sb.update_me:  # Score bar
            self.sb.draw(gp.score_bar)
            gp.flip_needed = True
            self.sb.update_me = False

        # Draw dialog overlay if active
        if gp.show_dialogwnd and self.dialog.update_me:
            # If dialog type 2 (game completion) has a short delay, draw only after delay
            if self.dialog.dialog_type != DialogType.CUSTOM_FUNCTION or \
                    (self.dialog.dialog_type == DialogType.CUSTOM_FUNCTION and self.game_board and \
                     time.time() - self.game_board.level.completed_time > 0.5):
                self.sb.draw(gp.score_bar)  # Redraw score bar even with dialog
                self.dialog.update()  # Update and draw dialog content
            gp.flip_needed = True  # Always flip if dialog is shown for potential animation

        # Perform screen flip if any redraw was needed
        if gp.flip_needed:
            pygame.display.flip()
            gp.flip_needed = False


class GamePlay:
    """
    The top-level class managing the application's lifecycle, states, and global resources.
    This acts as the state manager, delegating logic to the current active state.
    """

    def __init__(self, speaker, lang, configo, updater):
        self.speaker = speaker
        self.lang = lang
        self.config = configo
        self.updater = updater
        self.android = android

        # Global application state variables
        self.running = True
        self.current_state = None

        # Pygame resources (initialized later in initialize_application)
        self.screen = None
        self.display_info = None
        self.clock = None
        self.db = None

        # UI element references (will be set by states, but declared here for GamePlay's access)
        self.sizer = None
        self.sb = None
        self.info = None
        self.dialog = None  # DialogWnd instance
        self.game_board = None  # Reference to the active game board
        self.layout = None  # Reference to the active game board's layout
        self.m = None  # Reference to the Menu instance

        # Other GamePlay-level variables
        self.first_run = True
        self.updater_started = False
        self.show_dialogwnd = False  # Flag for dialog overlay
        self.cl = classes.colors.Color()
        self.sfx = classes.sound.SoundFX(self)
        self.userid = -1
        self.user_name = None
        self.score = 0
        self.theme = "default"
        self.menu_type = 1  # TODO menu type = 0
        self.menu_group = 0
        self.menu_category = 0
        self.menu_inner_cat = 0
        self.menu_level = MenuLevel.HOME
        self.completions = None
        self.completions_dict = None
        self.logged_out = False  # Used to influence login screen sizing
        self.redraw_needed = [True, True, True]  # [game_area, info_bar, score_bar]
        self.flip_needed = True
        self.init_resize = True  # Flag for initial resize handling
        self.mouse_over = [None, None, None]  # mouse over [surface, group of objects, top most object]
        self.mbtndno = None  # mouse button down object

        # For debouncing settings save
        self.settings_save_timer = 0.0
        self.SETTINGS_SAVE_DELAY = GamePlayConfig.SETTINGS_SAVE_DEBOUNCE_DELAY_SECONDS

        # Flag to indicate menu content needs re-creation
        self.menu_content_changed = False

        if android is not None:
            infoObject = pygame.display.Info()
            h = 770
            login_h = 570
            self.android_screen_size = [int(infoObject.current_w * h / infoObject.current_h), h]
            self.android_login_size = [int(infoObject.current_w * login_h / infoObject.current_h), login_h]

        # Initial window sizes (will be set in initialize_application or state enter methods)
        self.wn_size = [GamePlayConfig.DEFAULT_WINDOWED_WIDTH, GamePlayConfig.DEFAULT_WINDOWED_HEIGHT]
        self.fs_size = []
        self.size = []  # Current active screen size

    def set_init_vals(self):
        """Resets initial values for game loop, typically at the start of a new game or state."""
        self.redraw_needed = [True, True, True]  # [game_area, info_bar, score_bar]
        self.flip_needed = True
        self.init_resize = True  # Flag for initial resize handling

        # mouse over [surface, group of objects, top most object]
        self.mouse_over = [None, None, None]

    def safe_subsurface(self, rect):
        """Safely create a subsurface, ensuring the rect is within screen bounds."""
        if not hasattr(self, 'screen') or self.screen is None:
            logging.error("safe_subsurface: self.screen is not initialized.")
            return None
        try:
            r = pygame.Rect(rect)
            screen_rect = self.screen.get_rect()
            if screen_rect.contains(r):
                return self.screen.subsurface(r)
            else:
                logging.warning(f"safe_subsurface: Rect {r} is out of bounds (screen size: {screen_rect})")
                # Clamp rect to screen bounds if partially out of bounds
                clamped_rect = r.clip(screen_rect)
                if clamped_rect.width <= 0 or clamped_rect.height <= 0:
                    logging.warning(f"safe_subsurface: Clamped rect is empty: {clamped_rect}. Returning 1x1 surface.")
                    return pygame.Surface((1, 1), pygame.SRCALPHA)  # Return minimal transparent surface
                else:
                    logging.info(f"safe_subsurface: Clamped rect {clamped_rect} to fit screen bounds.")
                return self.screen.subsurface(clamped_rect)
        except pygame.error as e:
            logging.exception(f"safe_subsurface: Pygame error creating subsurface from rect {rect}: {e}")
        except Exception as e:
            logging.exception(f"safe_subsurface: Failed to create subsurface from rect {rect}: {e}")
        return pygame.Surface((1, 1), pygame.SRCALPHA)  # Fallback on error

    def create_subsurfaces(self):
        """Create subsurfaces & set initial layout constraints safely."""
        # Ensure sizer is initialized before creating subsurfaces
        if self.sizer is None:
            logging.error("create_subsurfaces: Sizer not initialized. Cannot create subsurfaces.")
            return

        self.dialogbg = self.safe_subsurface(self.sizer.dialogbg_pos)
        self.dialogwnd = self.safe_subsurface(self.sizer.dialogwnd_pos)
        # Note: game_bg, info_bar, score_bar might be initialized in GameState.enter
        self.game_bg = self.safe_subsurface(self.sizer.game_bg_pos)
        self.info_bar = self.safe_subsurface(self.sizer.info_bar_pos)
        self.score_bar = self.safe_subsurface(self.sizer.score_bar_pos)

        if self.sb is not None:
            self.sb.resize()  # Tell score bar to resize its internal elements

    def recreate_game_screen(self):
        """Recreates the main game subsurface after layout changes."""
        if self.layout is not None:
            # Ensure layout.game_pos provides valid dimensions (positive width/height)
            game_pos_rect = pygame.Rect(self.layout.game_pos)
            # Ensure dimensions are at least 1x1
            game_pos_rect.width = max(1, game_pos_rect.width)
            game_pos_rect.height = max(1, game_pos_rect.height)
            self.game = self.safe_subsurface(game_pos_rect)
            if self.game is None:
                logging.warning("recreate_game_screen: Failed to recreate game surface (returned None).")
        else:
            logging.warning("recreate_game_screen: self.layout is not initialized.")
            self.game = None  # Ensure game surface is None if layout is missing

    def _set_display_mode(self, size, is_fullscreen):
        """
        Helper to set the Pygame display mode.
        Handles setting flags and updating self.screen.
        Ensures minimum 1x1 size.
        """
        w, h = max(1, size[0]), max(1, size[1])  # Ensure positive dimensions
        flag = pygame.FULLSCREEN if is_fullscreen else pygame.RESIZABLE
        try:
            if not pygame.display.get_init():
                pygame.display.init()
            self.screen = pygame.display.set_mode((w, h), flag)
            logging.info(f"Set display mode to {(w, h)} with flags: {flag}")
        except pygame.error as e:
            logging.critical(
                f"Pygame failed to set display mode to {(w, h)} with flags {flag}: {e}. Attempting emergency shutdown.")
            self.running = False  # Critical error, attempt to shut down gracefully
        except Exception as e:
            logging.critical(
                f"Failed to set display mode to {(w, h)} with flags {flag}: {e}. Attempting emergency shutdown.")
            self.running = False

    def update_display_elements(self, info):
        """
        Updates all game layout and UI elements after a screen size change
        (either fullscreen toggle or window resize).
        """
        logging.info(f"Updating display elements for size: {self.size}")
        # Step 1: Update sizer with new screen dimensions
        self.sizer.update_sizer(self.size[0], self.size[1])

        # Step 2: Update game board layout if it exists
        if self.game_board and self.game_board.layout:
            self.game_board.layout.update_layout_fs(
                self.size[0], self.size[1],
                self.game_board.layout.x_count,
                self.game_board.layout.y_count
            )
            # Step 3: Reload level to fit new layout
            self.game_board.level.load_level()  # This might be heavy, consider if always needed
            # Step 4: Adjust layout for game data
            self.game_board.layout.update_layout(
                self.game_board.data[0], self.game_board.data[1]
            )
        else:
            logging.warning("update_display_elements: game_board or its layout not initialized.")

        # Step 5: Recreate subsurfaces safely
        self.create_subsurfaces()

        # Step 6: Safely recreate the main game surface
        self.recreate_game_screen()  # This now handles self.game

        # Step 7: Re-initialize info bar with updated game board and info bar surface
        if self.game_board and self.info_bar:
            info.new_game(self.game_board, self.info_bar)
        else:
            logging.warning("update_display_elements: Missing game_board or info_bar surface for info.new_game.")

        self.redraw_needed = [True, True, True]  # Ensure a full redraw after update

    def fullscreen_toggle(self, info):
        """
        Toggles between fullscreen and windowed version with CTRL + F.
        Current activity will be reset.
        """
        """
        if pygame.version.vernum[0] >= 2 or self.config.platform == "macos":
            logging.info("Fullscreen toggle temporarily disabled for Pygame 2+ or MacOS due to potential issues.")
            return
        """

        self.config.fullscreen = not self.config.fullscreen
        new_size = self.fs_size[:] if self.config.fullscreen else self.wn_size[:]
        self.size = new_size

        self._set_display_mode(new_size, self.config.fullscreen)
        self.update_display_elements(info)

        self.redraw_needed = [True, True, True]
        pygame.display.flip()

    def on_resize(self, new_size_tuple, info):
        """
        Handles screen resize events.
        Clamps the new size to configured limits for desktop.
        """
        new_size = list(new_size_tuple)

        if self.android is None:
            # Clamp width and height for desktop
            min_w, min_h, max_w, max_h = self.config.size_limits
            clamped_w = max(min_w, min(new_size[0], max_w))
            clamped_h = max(min_h, min(new_size[1], max_h))
            clamped_size = [clamped_w, clamped_h]

            if clamped_size != self.size:
                self.wn_size = clamped_size[:]
                self.size = clamped_size[:]

                self._set_display_mode(self.size, self.config.fullscreen)

                # Resize logic: Update sizer and game elements
                self.sizer.update_sizer(self.size[0], self.size[1])
                self.update_display_elements(info)

                # Mark settings as changed for debounced saving
                self.config.settings["screenw"] = self.size[0]
                self.config.settings["screenh"] = self.size[1]
                self.config.settings_changed = True
        else:
            # Android path: Android handles screen size changes differently.
            self.size = self.android_screen_size[:]
            self.sizer.update_sizer(self.size[0], self.size[1])
            self.update_display_elements(info)

        # Dialog and Info bar also need to be notified of resize
        if self.dialog:  # Check if dialog exists before calling resize
            self.dialog.resize()
        if self.info:  # Check if info exists
            self.info.rescale_title_space()
        self.redraw_needed = [True, True, True]

    def set_up_user(self):
        """Loads and sets up user settings, language, and initializes speaker."""
        self.config.load_settings(self.db, self.userid)
        self.lang.load_language()
        self.completions_dict = {}
        self.speaker.talkative = self.config.settings["espeak"]
        self.speaker.start_server()  # Ensure speaker server is started
        self.config.check_updates = self.config.settings["check_updates"]
        if self.android is None and self.config.check_updates and self.first_run:
            self.first_run = False
            self.updater_started = True
            if self.updater is not None:
                self.updater.start()
        if self.config.loaded_settings:
            self.config.fullscreen = self.config.settings["full_screen"]

        uname = self.user_name if self.lang.lang != 'he' else ""
        self.welcome_msg = f"{self.lang.dp['Hello']} {uname}! {self.lang.dp['Welcome back.']}"
        self.speaker.say(self.welcome_msg)

    def switch_scheme(self, scheme):
        """Switches the visual scheme of the game."""
        self.redraw_needed = [True, True, True]
        self.scheme_code = scheme
        if scheme is None:
            self.scheme = None
        else:
            scheme_map = {"WB": classes.colors.WBScheme, "BW": classes.colors.BWScheme, "BY": classes.colors.BYScheme}
            self.scheme = scheme_map.get(scheme, lambda: None)()  # Use .get with a default lambda for safety
            if self.scheme is None:
                logging.warning(f"Unknown scheme: {scheme}. Defaulting to no scheme.")

        if self.info:  # Ensure info bar exists before updating
            self.info.create()
            self.update_display_elements(self.info)

        if self.game_board and self.game_board.board:
            self.game_board.board.line_color = self.game_board.board.board_bg.line_color

        s_id = 0
        if scheme == "WB":
            s_id = 1
        elif scheme == "BW":
            s_id = 2
        elif scheme == "BY":
            s_id = 3

        self.cl.reset_default_colors_sv(self.scheme)
        self.config.settings["scheme"] = s_id
        self.config.settings_changed = True
        if self.info:
            self.info.realign()

    def set_up_scheme(self):
        """Applies the current scheme setting."""
        s_id = self.config.settings["scheme"]
        scheme = None
        if s_id == 1:
            scheme = "WB"
        elif s_id == 2:
            scheme = "BW"
        elif s_id == 3:
            scheme = "BY"

        if scheme != self.scheme_code:
            self.switch_scheme(scheme)

    def initialize_application(self):
        """Initializes core application components like Pygame, database, and display info."""
        logging.debug(f"Initializing application.")

        if android is None:
            pygame.init()  # Ensure Pygame is initialized

        self.db = classes.dbconn.DBConnection(self.config.file_db, self)
        self.scheme = None
        self.scheme_code = None
        self.user_name = None
        self.display_info = pygame.display.Info()
        self.clock = pygame.time.Clock()

    def shut_down(self):
        """Performs cleanup operations before exiting the application."""
        logging.info("Shutting down application...")
        if self.config.settings_changed:
            logging.info("Saving settings before shutdown.")
            self.config.save_settings(self.db)

        if self.db:
            self.db.close()
        if self.speaker and self.speaker.process is not None:
            self.speaker.stop_server()

        pygame.quit()
        gc.collect()
        if android is None:
            sys.exit()

    def change_state(self, new_state: BaseState):
        """
        Transitions the game to a new state.
        Calls exit() on the current state and enter() on the new state.
        """
        if type(self.current_state).__name__ == type(new_state).__name__:
            logging.debug(f"State change aborted - new state is the same as current state: {type(new_state).__name__}")
            return

        logging.info(f"Changing state from {type(self.current_state).__name__} to {type(new_state).__name__}")
        if self.current_state:
            self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()

    def auto_login(self, al):
        userid = None

        if al is not None:
            if al[1] and not self.logged_out:
                userid = al[0]

        if userid is not None:
            self.db.login_auto(userid)

            self.user_name = self.db.username
            self.userid = self.db.userid

            # Transition to GameState directly
            # self.loading = True  # Show loading screen during transition
            # self.update_me = True
            self.redraw_needed[0] = True

    def run(self):
        """
        Main application entry point.
        Manages the game loop and delegates control to the current state.
        """
        self.initialize_application()

        # Start with the LoginState
        #al = self.db.get_autologin()
        #logging.debug(f"Auto-login check: {al}")
        self.change_state(LoginState(self))

        while self.running:
            # uncomment the following line to test all activities across multiple languages as specified in the stresstest.py
            # if type(self.current_state).__name__ == "GameState":
            #    stresstest.step(self)
            # Check for Android pause/resume outside the state loop
            if self.android is not None and self.android.check_pause():
                self.android.wait_for_resume()
                # Force a redraw for the current state after resuming
                if self.current_state:
                    self.redraw_needed = [True, True, True]  # Global redraw flag
                    self.current_state.draw()  # Force immediate redraw if resumed

            for event in pygame.event.get():
                # Allow the current state to handle the event
                if self.current_state:
                    self.current_state.handle_event(event)

            # Update and draw the current state
            if self.current_state:
                self.current_state.update()
                self.current_state.draw()  # State is responsible for drawing itself

            self.clock.tick(GamePlayConfig.GAME_FPS)  # Control global FPS

        self.shut_down()


def main():
    """Main function to initialize and run the eduActiv8 application."""
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    if android is None or len(sys.argv) == 1:
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        if android is not None:
            # Pygame init for Android might be done earlier in GamePlay.initialize_application
            # but ensure Android specific init is here.
            pygame.init()  # Ensure Pygame is initialized if not already
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        else:
            try:
                icon = pygame.image.load(ICON_PATH)
                pygame.display.set_icon(icon)
            except pygame.error as e:
                logging.error(f"Could not load application icon from {ICON_PATH} in main: {e}")

        configo = classes.config.Config(android)
        lang = classes.lang.Language(configo, path)
        speaker = classes.speaker.Speaker(lang, configo, android)
        updater = None

        app = GamePlay(speaker, lang, configo, updater)
        if android is None:
            speaker.start()  # Start speaker thread for desktop
        app.run()
    elif len(sys.argv) == 2:
        if sys.argv[1] in ("v", "version"):
            from classes.cversion import ver
            print(f"eduactiv8-{ver}")
    else:
        logging.warning("Sorry arguments not recognized.")


if __name__ == "__main__":
    main()
