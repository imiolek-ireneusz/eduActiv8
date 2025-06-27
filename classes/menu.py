# -*- coding: utf-8 -*-

import ast
import sys
import logging # Added logging for better debugging

import classes.extras as ex

"""
#games currently not used 30?, 40?, 57, 58, 83, 86
"""

# the following is used to enable Windows packaging script to import all the games (otherwise imported dynamically).
if sys.platform == "win32" or sys.platform == "cygwin":
    from game_boards import game000, game001, game002, game003, game004, game005, game006, game007, game008, game009, \
        game010, game011, game012, game013, game014, game015, game016, game017, game018, game019, game020, game021, \
        game022, game023, game024, game025, game026, game027, game028, game029, game030, game031, game032, game033, \
        game034,  game035, game036, game037, game038, game039, game040, game041, game042, game043, game044, game045, \
        game046, game047, game048, game049, game050, game051, game052, game053, game054, game055, game056, game057, \
        game058, game059, game060, game061, game062, game063, game064, game065, game066, game067, game068, game069, \
        game070, game071, game072, game073, game074, game075, game076, game077, game078, game079, game080, game081, \
        game082, game083, game084, game085, game086, game087, game088, game089, game090, game091, game092, game093, \
        game094, game095, game096, game097, game098, game099, game100, game101, game102, game103, game104, game105, \
        game106, game107, game108, game109, game110, game111, game112, game113, game114, game115, game116, game117, \
        game118, game119, game120, game121


class MenuCategoryGroup:
    def __init__(self, menu, unit_id, title, subtitle, menu_line):
        self.selected = False
        self.categories = []
        self.menu = menu
        self.unit_id = unit_id
        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)
        self.menu_line = menu_line


class MenuCategory:
    def __init__(self, menu, top_id, cat_id, title, subtitle, img_src, has_inner, menu_line):
        self.menu = menu
        self.cat_id = cat_id
        self.top_id = top_id
        self.has_inner = has_inner
        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)
        self.img_src = img_src
        self.menu_line = menu_line


class MenuItem:
    def __init__(self, menu, dbgameid, item_id, cat_id, title, subtitle, constructor, img_src, img_src2,
                 variant=0, var2=0, max_age=7, menu_line=0):
        self.menu = menu
        self.item_id = item_id
        self.cat_id = cat_id
        self.game_constructor = constructor
        self.variant = variant
        self.var2 = var2
        self.dbgameid = dbgameid
        self.lang_activity = False
        self.title = ex.unival(title)
        self.subtitle = ex.unival(subtitle)
        self.max_age = max_age
        self.img_src = img_src
        self.img_src2 = img_src2
        self.menu_line = menu_line


class Menu:
    # Modified constructor to accept xml_conn directly
    def __init__(self, mainloop, xml_conn_instance):
        self.mainloop = mainloop
        self.lang = self.mainloop.lang
        self.uage = self.mainloop.config.user_age_group
        self.categories_dict = dict()
        self.create_lists()
        self.active_game_id = 0
        self.active_o = None
        self.active_cat_o = None
        self.game_started_id = -1
        self.active_cat = 0
        self.lang_activity = False
        self.current_inner = False
        self.show_all = 0
        self.game_constructor = "game000.Board"
        self.game_dbid = 0
        self.game_variant = 0
        self.game_var2 = 0
        self.en_list = []  # list of games that need the speaker to be switched to English
        # Assign xml_conn_instance directly
        self.xml = xml_conn_instance
        if self.xml is None:
            logging.error("Menu initialized with None xml_conn_instance. This will cause issues!")
        self.create_menu()

    def load_levels(self):
        if self.mainloop.config.save_levels:
            temp = self.mainloop.db.load_all_cursors(self.mainloop.userid)
            for key in self.saved_levels.keys():
                if key not in temp.keys():
                    temp[key] = self.saved_levels[key]
            self.saved_levels = temp

    def create_lists(self):
        self.top_categories = []
        self.categories = []
        self.categories_dict.clear()
        self.elements = []
        self.games = []
        self.games_current = []
        self.cats_current = []
        self.saved_levels = dict()

    def add_categories_to_groups(self):
        for each in self.categories:
            if 0 < each.top_id < len(self.top_categories) + 1: # Added bounds check
                self.top_categories[each.top_id - 1].categories.append(each)

    def create_menu(self):
        self.add_all()
        self.add_categories_to_groups()
        self.scroll_l = 0
        self.scroll_r = 0
        self.load_levels()

    def lang_change(self):
        self.create_lists()
        self.create_menu()
        self.change_cat(self.active_cat)

    def play_sound(self, sound_id):
        self.mainloop.sfx.play(sound_id)

    def start_hidden_game(self, gameid):
        for each in self.games:
            if each.dbgameid == gameid:
                self.active_game_id = each.item_id
                self.play_sound(4)
                self.mainloop.config.max_age = each.max_age
                self.game_constructor = each.game_constructor
                self.game_dbid = each.dbgameid
                self.game_variant = each.variant
                self.game_var2 = each.var2
                self.lang_activity = each.lang_activity
                self.mainloop.score = 0
                self.mainloop.redraw_needed = [True, True, True]
                return True
        return False

    def reset_titles(self):
        # These are now attributes of the info bar, accessed via mainloop
        self.mainloop.info.title = ""
        self.mainloop.info.subtitle = ""
        self.mainloop.info.game_id = ""
        self.mainloop.redraw_needed[1] = True # Signal info bar area needs redraw

    def add_top_category(self, top_id, title, subtitle, img_src1, menu_line):  # 105
        new_top_category = MenuCategoryGroup(self, top_id, title, subtitle, menu_line)
        self.top_categories.append(new_top_category)
        self.elements.append(new_top_category)

    def add_all(self):
        self.add_category(0, 0, "", "", "ico_c_00.png", False, None)

        self.badge_count = self.mainloop.db.get_completion_count(self.mainloop.userid)

        c_id = 0  # Add the home screens
        self.add_game(0, c_id, 0, 7, "game000.Board", "", "", "ico_g_0001.png")
        self.games[-1].hidden = True
        self.add_game(3, c_id, 0, 7, "game003.Board", self.lang.d["Language"], "", "ico_g_0001.png", "0")
        self.games[-1].hidden = True
        self.add_game(2, c_id, 0, 7, "game002.Board", self.lang.d["Translators"], "", "ico_g_0001.png", "0")
        self.games[-1].hidden = True
        self.add_game(1, c_id, 0, 7, "game001.Board", self.lang.d["Credits"], "", "ico_g_0001.png", "0")
        self.games[-1].hidden = True
        self.add_game(271, c_id, 0, 7, "game004.Board", "", "", "ico_g_0001.png", "0")
        self.games[-1].hidden = True
        self.add_game(272, c_id, 0, 7, "game004.Board", "", "", "ico_g_0001.png", "0")
        self.games[-1].hidden = True
        self.add_game(273, c_id, 0, 7, "game113.Board", self.lang.d["Theme Editor"], self.lang.d["Make the game look your way"], "ico_g_0001.png", "0")
        self.games[-1].hidden = True

        # Ensure xml.menu_root exists before iterating
        if self.xml and hasattr(self.xml, 'menu_root') and self.xml.menu_root is not None:
            for top_cat in self.xml.menu_root:
                #add category groups
                self.add_top_category(int(top_cat.attrib['id']), self.lang.d[top_cat.attrib['title']], "",
                                      top_cat.attrib['icon'], int(top_cat.attrib['mline']))
                self.add_cats_from_topcat(top_cat)
        else:
            logging.error("XML menu root is not available. Cannot add categories from XML.")

    def add_cats_from_topcat(self, top_cat):
        for cat in top_cat:
            #add categories
            cat_add = True

            if 'visible' in cat.attrib and cat.attrib['visible'] == "0":
                cat_add = False
            # check the age range if not in display all
            elif self.uage != 7:
                if 'min_age' in cat.attrib and self.uage < int(cat.attrib['min_age']):
                    cat_add = False
                elif 'max_age' in cat.attrib and self.uage > int(cat.attrib['max_age']):
                    cat_add = False

            # check for languages included/excluded
            if 'lang_incl' in cat.attrib and cat.attrib['lang_incl'] != "":
                try:
                    lin = ast.literal_eval(cat.attrib['lang_incl'])
                    if self.mainloop.lang.lang[0:2] not in lin:
                        cat_add = False
                except (ValueError, SyntaxError) as e:
                    logging.error(f"Error parsing lang_incl for category {cat.attrib.get('id', 'N/A')}: {e}")
                    cat_add = False # Assume it's invalid and exclude
            elif 'lang_excl' in cat.attrib and cat.attrib['lang_excl'] != "":
                try:
                    lex = ast.literal_eval(cat.attrib['lang_excl'])
                    if self.mainloop.lang.lang[0:2] in lex:
                        cat_add = False
                except (ValueError, SyntaxError) as e:
                    logging.error(f"Error parsing lang_excl for category {cat.attrib.get('id', 'N/A')}: {e}")
                    cat_add = False # Assume it's invalid and exclude
            # check if the activity requires espeak to work correctly
            if ('listening' in cat.attrib and ast.literal_eval(cat.attrib['listening']) is True and
                (not hasattr(self.mainloop.speaker, 'started') or self.mainloop.speaker.started is False)):
                cat_add = False

            if cat_add:
                c_id = int(cat.attrib['id'])
                ico = cat.attrib['icon'] # Default icon
                if 'icosuffix' in cat.attrib and ast.literal_eval(cat.attrib["icosuffix"]):
                    ico = cat.attrib['icon'][0:8] + self.lang.ico_suffix + cat.attrib['icon'][8:]

                # Ensure all required attributes exist before passing to add_category
                try:
                    self.add_category(int(top_cat.attrib['id']), c_id,
                                      self.lang.d[cat.attrib['title']], self.lang.d[cat.attrib['subtitle']], ico,
                                      ast.literal_eval(cat.attrib['has_inner']), int(cat.attrib['mline']))
                except KeyError as e:
                    logging.error(f"Missing attribute {e} for category {cat.attrib.get('id', 'N/A')}. Skipping.")
                    continue # Skip this category if essential attributes are missing

                if 'has_inner' in cat.attrib and ast.literal_eval(cat.attrib['has_inner']) is True:
                    self.add_cats_from_topcat(cat)
                else:
                    self.add_games_from_cat(cat, c_id)

    def add_games_from_cat(self, cat, c_id):
        for game in cat:
            # add games in current category
            add = True

            if 'visible' in game.attrib and game.attrib['visible'] == "0":
                add = False
            # check the age range and display code
            elif self.uage != 7:
                if 'min_age' in game.attrib and self.uage < int(game.attrib['min_age']):
                    add = False
                elif 'max_age' in game.attrib and self.uage > int(game.attrib['max_age']):
                    add = False

            if add:
                # check for languages included/excluded
                if 'lang_incl' in game.attrib and game.attrib['lang_incl'] != "":
                    try:
                        lin = ast.literal_eval(game.attrib['lang_incl'])
                        if self.mainloop.lang.lang[0:2] not in lin:
                            add = False
                    except (ValueError, SyntaxError) as e:
                        logging.error(f"Error parsing lang_incl for game {game.attrib.get('dbid', 'N/A')}: {e}")
                        add = False
                elif 'lang_excl' in game.attrib and game.attrib['lang_excl'] != "":
                    try:
                        lex = ast.literal_eval(game.attrib['lang_excl'])
                        if self.mainloop.lang.lang[0:2] in lex:
                            add = False
                    except (ValueError, SyntaxError) as e:
                        logging.error(f"Error parsing lang_excl for game {game.attrib.get('dbid', 'N/A')}: {e}")
                        add = False

                # check if the game requires the alphabet to have upper case
                if ('require_uc' in game.attrib and ast.literal_eval(game.attrib['require_uc']) is True and
                    self.lang.has_uc is False):
                    add = False
                elif ('android' in game.attrib and ast.literal_eval(game.attrib['android']) is False and
                      self.mainloop.android is not None):
                    add = False
                elif ('listening' in game.attrib and ast.literal_eval(game.attrib['listening']) is True and
                      (not hasattr(self.mainloop.speaker, 'started') or self.mainloop.speaker.started is False)):
                    add = False

            if add:
                # dbgameid, cat_id, min_age, max_age, constructor, title, subtitle, img_src, variant=0, var2=0
                ico_suffix = ""
                if 'icosuffix' in game.attrib and ast.literal_eval(game.attrib["icosuffix"]):
                    ico_suffix = self.lang.ico_suffix

                try:
                    dbid = int(game.attrib['dbid'])
                    min_age = int(game.attrib["min_age"])
                    max_age = int(game.attrib["max_age"])
                    constructor_id = int(game.attrib["constructor_id"])
                    constructor_name = f"game{constructor_id:03d}.Board"
                    title = self.lang.d[game.attrib['title']]
                    subtitle = self.lang.d[game.attrib['subtitle']]
                    icon = game.attrib['icon'][0:10] + ico_suffix + game.attrib['icon'][10:] if ico_suffix else game.attrib['icon']
                    ico_group = game.attrib.get('ico_group', "") # Use .get with default
                    variant = int(game.attrib.get("variant", 0))
                    var2 = int(game.attrib.get("var2", 0))
                    mline = int(game.attrib.get('mline', 0))

                    self.add_game(dbid, c_id, min_age, max_age, constructor_name,
                                  title, subtitle, icon, ico_group, variant, var2, mline)

                    # Ensure games list is not empty before accessing last element
                    if self.games:
                        self.games[-1].lang_activity = ast.literal_eval(game.attrib.get('lang_activity', 'False'))
                except KeyError as e:
                    logging.error(f"Missing attribute {e} for game {game.attrib.get('dbid', 'N/A')}. Skipping.")
                except ValueError as e:
                    logging.error(f"Type conversion error for game {game.attrib.get('dbid', 'N/A')}: {e}. Skipping.")


    def add_category(self, top_id, cat_id, title, subtitle, img_src, has_inner, menu_line):
        new_category = MenuCategory(self, top_id, cat_id, title, subtitle, img_src, has_inner, menu_line)
        self.categories.append(new_category)
        self.categories_dict[cat_id] = new_category

    def add_game(self, dbgameid, cat_id, min_age, max_age, constructor, title, subtitle, img_src, img_src2="",
                 variant=0, var2=0, menu_line=None):
        # Ensure self.uage is properly initialized before comparison
        if self.uage is None:
            logging.warning("User age (self.uage) is None in Menu.add_game. Defaulting to show all games.")
            can_add_by_age = True
        else:
            can_add_by_age = (min_age <= self.uage <= max_age) or (self.uage == 7)

        if can_add_by_age:
            new_game = MenuItem(self, dbgameid, len(self.games), cat_id, title, subtitle, constructor,
                                img_src, img_src2, variant, var2, max_age, menu_line)
            self.games.append(new_game)
        self.saved_levels[dbgameid] = 1 # Always record level as saved, regardless of age filter for menu display

    def change_cat(self, cat_id):
        if cat_id not in self.categories_dict:
            logging.error(f"Category ID {cat_id} not found in categories_dict.")
            return # Prevent KeyError

        if self.categories_dict[cat_id].has_inner is not True:
            self.games_current = []
            for each_item in self.games:
                if each_item.cat_id == cat_id:
                    self.games_current.append(each_item)
            # self.cats_current = [] # Ensure cats_current is empty if showing games
        else:
            self.cats_current = []
            for each_item in self.categories:
                if each_item.top_id == cat_id:
                    self.cats_current.append(each_item)
            # self.games_current = [] # Ensure games_current is empty if showing categories
