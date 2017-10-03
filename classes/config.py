# -*- coding: utf-8 -*-

import os
import sys

import classes.extras as ex
from classes.cversion import ver


class Config:
    'holds some basic configuration data - screen size among others'

    def __init__(self, android):
        self.font_multiplier = 1
        self.font_line_height_adjustment = 1
        self.font_start_at_adjustment = 0
        self.font_variant = 0
        self.version = ver
        self.settings_changed = False
        self.fs_width = 1024
        self.fs_height = 768
        self.debug_screen_size = None  # [900,600]
        # size_limits - don't let window resizing get out of hand [min_w, min_h, max_w, max_h]
        self.size_limits = [800, 570, 2000, 2000]
        # [670,480,2000,2000] #800 - minimum to fit all buttons, 2000 - with over 2000 pixels each way pygame is not redrawing very well
        # set total size of OS panels and window decorations on both sides - used in windowed version. Not so much important now with resizing enabled.
        # this will not be auto-detected
        self.os_panels_w = 2  # sum of widths of non-hiding vertical Panels (if any) and window border (1px on each side).
        self.os_panels_h = 52  # sum of heights of non-hiding horizontal panels (ie. menu bar(s) + application bar + window bar + border, etc.).

        # the game will 'remember' at what level each game has been left and it will save this data for next session if the save_levels is left at True
        # to reset the game - remove the level_data.txt file check below for the location of these files - it will be recreated next time you close the game
        # if the pickle has been saved with python3 then python2 will not be able to open it and will reset all levels to 1
        # the data is automatically saved to file every time you switch game and on exit.
        self.save_levels = True

        # the following 2 settings will be overridden by configuration file
        # to change any of these do this in the in-game preferences, except fullscreen if there's no config file the value below will be used.
        self.fullscreen = False
        # self.read_inst = False #no longer used
        self.google_trans_languages = False

        self.user_age_group = 0  # default group - showing all games - TO DO: will be overridden by data stored in database
        self.max_age = 7

        # Window title
        self.window_caption = "eduActiv8 - v " + self.version
        self.db_file_name = 'eduactiv8.db'

        """
        #file names paths to level and language files
        $XDG_DATA_HOME defines the base directory relative to which user
        specific data files should be stored. If $XDG_DATA_HOME is either not
        set or empty, a default equal to $HOME/.local/share should be used.
        $XDG_CONFIG_HOME defines the base directory relative to which user
        specific configuration files should be stored. If $XDG_CONFIG_HOME is
        either not set or empty, a default equal to $HOME/.config should be
        used.
        """
        if android is None:
            p = sys.platform
            directory = os.path.dirname(os.path.abspath(os.path.expanduser("~/.config/eduactiv8/")))
            self.window_pos = (3, 30)
            if p == "linux" or p == "linux2":
                # self.window_pos = (10,30)
                self.platform = "linux"
                try:
                    xdg_data_home = os.environ.get('XDG_DATA_HOME')
                except:
                    xdg_data_home = None

                if xdg_data_home is None or xdg_data_home == "":
                    home = os.environ.get('HOME')
                    directory = os.path.join(home, '.local', 'share', 'eduactiv8')
                else:
                    directory = os.path.join(xdg_data_home, 'eduactiv8')

            elif p == "win32" or p == "cygwin":
                #windows or other non linux operating system
                self.platform = "windows"
            elif p == "darwin":
                self.platform = "macos"
                self.window_pos = (0, 0)
                self.os_panels_w = 0  # sum of widths of non-hiding vertical Panels (if any) and window border (1px on each side).
                self.os_panels_h = 120
            self.file_db = os.path.join(directory, self.db_file_name)
        else:
            # android folder creation
            self.platform = "android"
            self.window_pos = (0, 0)
            directory = "assets"
            self.file_db = os.path.join(directory, self.db_file_name)
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except:
            print("Error - can't create directory. The game data won't be saved.")

        # default settings
        self.loaded_settings = False
        """
        lang,
        sounds,
        espeak,
        screenw,
        screenh
        """
        # [0 language, 1 talkative, 2 untranslated languages, 3 full screen, 4 user_name, 5 screen_w, 6 screen_h]

        self.settings = dict()
        try:
            import pyfribidi
            self.fribidi_loaded = True
            self.frididi = pyfribidi
            s = ex.unival('العربية')
            self.arabic = self.frididi.log2vis(s)
        except:
            self.fribidi_loaded = False
            self.frididi = None
            self.arabic = "Arabic"

        self.set_font_family()

        if self.fribidi_loaded:
            self.lang_titles = ["English", "American English", "Català", "Deutsch", "Español", "Français", "Italiano", "Lakȟótiyapi",
                                "Polski", "Português", "Suomalainen", "Ελληνικά", "Русский", "Српски", "Українська",
                                "תירבע", self.arabic, "Test Language"]
            self.all_lng = ["en_GB", "en_US", "ca", "de", "es_ES", "fr", "it", "lkt", "pl", "pt_PT", "fi", "el", "ru", "sr",
                            "uk", "he", "ar", "te_ST"]
            self.ok_lng = ["en_GB", "en_US", "ca", "de", "es_ES", "fr", "it", "lkt", "pl", "pt_PT", "fi", "el", "ru", "sr",
                           "uk", "he"]
        else:
            self.lang_titles = ["English", "American English", "Català", "Deutsch", "Español", "Français", "Italiano", "Lakȟótiyapi",
                                "Polski", "Português", "Suomalainen", "Ελληνικά", "Русский", "Српски", "Українська",
                                "תירבע", "Test Language"]
            self.all_lng = ["en_GB", "en_US", "ca", "de", "es_ES", "fr", "it", "lkt", "pl", "pt_PT", "fi", "el", "ru", "sr",
                            "uk", "he", "te_ST"]
            self.ok_lng = ["en_GB", "en_US", "ca", "de", "es_ES", "fr", "it", "lkt", "pl", "pt_PT", "fi", "el", "ru", "sr",
                           "uk", "he"]

        self.id2lng = {1: "English", 5: "Català", 19: "Српски", 12: "Deutsch", 8: "Español", 16: "Ελληνικά",
                       17: "תירבע", 11: "Italiano", 20:  "Lakȟótiyapi", 3: "Polski", 9: "Português", 13: "Русский", 15: "Suomalainen",
                       14: "Українська", 2: self.arabic, 10: "Français"}
        self.id2imgsuffix = {1: "", 5: "", 18: "ru", 12: "", 8: "", 16: "el", 17: "he", 11: "", 20: "", 3: "", 9: "", 13: "ru",
                             15: "", 14: "ru", 2: "ar", 10: ""}

        """
        self.id2lng = {1: "English", 5: "Català", 19: "Српски", 12: "Deutsch", 8: "Español", 16: "Ελληνικά",
                       17: "תירבע", 11: "Italiano", 20:  "Lakȟótiyapi", 3: "Polski", 9: "Português", 13: "Русский", 15: "Suomalainen",
                       14: "Українська", 2: self.arabic, 6: "Dansk", 10: "Français", 7: "Nederlands", 4: "Slovenčina"}
        self.id2imgsuffix = {1: "", 5: "", 18: "ru", 12: "", 8: "", 16: "el", 17: "he", 11: "", 20: "", 3: "", 9: "", 13: "ru",
                             15: "", 14: "ru", 2: "ar", 6: "", 10: "", 7: "", 4: ""}
        """

    def set_font_family(self, variant=0):
        self.font_variant = variant
        if variant == 0:
            self.font_dir = 'LinLibertine'
            self.font_name_1 = 'LinBiolinum_RB_merged_with_Kacst.ttf'
            self.font_name_2 = 'LinBiolinum_R_merged_with_Kacst.ttf'
            self.font_multiplier = 1
            self.font_line_height_adjustment = 1.5
            self.font_start_at_adjustment = 5

        elif variant == 1:
            self.font_dir = 'FreeSans'
            self.font_name_1 = 'FreeSansBold.ttf'
            self.font_name_2 = 'FreeSans.ttf'
            self.arabic = "Arabic"
            self.font_multiplier = 1
            self.font_line_height_adjustment = 1
            self.font_start_at_adjustment = 0

        elif variant == 2:
            self.font_dir = 'FreeSans'
            self.font_name_1 = 'FreeSansBold.ttf'
            self.font_name_2 = 'FreeSans.ttf'
            self.arabic = "Arabic"
            self.font_multiplier = 1
            self.font_line_height_adjustment = 1
            self.font_start_at_adjustment = 0

        """
        self.font_dir = 'LinLibertine'
        self.font_name_1 = 'LinBiolinum_RBah.ttf'
        self.font_name_2 = 'LinBiolinum_Rah.ttf'
        """

    def set_start_at(self, scale):
        if self.font_variant == 0:
            self.font_start_at_adjustment = int(scale * 5 / 100)

    def reset_settings(self):
        pass

    def load_settings(self, db, userid):
        'loads saved settings from pickled file - language and screen size dimensions and mode'
        # load user settings
        u = db.load_user_settings(userid)
        self.user_age_group = db.get_age_group(userid=userid)
        # load admin settings
        a = db.get_login_defs()
        # lang, sounds, espeak, screenw, screenh

        self.settings["extra_langs"] = int(a[1][2])
        self.settings["full_screen"] = int(a[1][0])

        self.settings["lang"] = u[0]
        self.settings["sounds"] = u[1]
        self.settings["espeak"] = u[2]

        if self.debug_screen_size is None:
            self.settings["screenw"] = u[3]
            self.settings["screenh"] = u[4]
        else:
            self.settings["screenw"] = self.debug_screen_size[0]
            self.settings["screenh"] = self.debug_screen_size[1]

        # self.settings["screenw"] = 1264
        # self.settings["screenh"] = 672

        self.settings["scheme"] = u[5]
        self.loaded_settings = True

    def save_settings(self, db):
        'save settings to file'
        db.save_user_settings(self.settings["lang"], self.settings["sounds"], self.settings["espeak"],
                              self.settings["screenw"], self.settings["screenh"], self.settings["scheme"])
