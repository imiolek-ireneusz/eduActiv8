# -*- coding: utf-8 -*-

import os
import ast
import sys

if sys.platform == "win32" or sys.platform == "cygwin":
    import xml.etree.cElementTree as et
else:
    import xml.etree.ElementTree as et

class XMLConn:
    def __init__(self, mainloop):
        self.mainloop = mainloop
        self.level_path = ""
        self.menu_path = ""
        self.load_xml_files()

    def load_xml_files(self):
        # check for language specific files:
        reload_files = False
        lang_level_path = os.path.join('xml', 'levels_' + self.mainloop.lang.lang + '.xml')
        if os.path.exists(lang_level_path):
            if self.level_path != lang_level_path:
                self.level_path = lang_level_path
                reload_files = True
        else:
            if self.level_path != os.path.join('xml', 'levels.xml'):
                self.level_path = os.path.join('xml', 'levels.xml')
                reload_files = True

        lang_menu_path = os.path.join('xml', 'menu_' + self.mainloop.lang.lang + '.xml')
        if os.path.exists(lang_menu_path):
            if self.menu_path != lang_menu_path:
                self.menu_path = lang_menu_path
                reload_files = True
        else:
            if self.menu_path != os.path.join('xml', 'menu.xml'):
                self.menu_path = os.path.join('xml', 'menu.xml')
                reload_files = True

        if reload_files:
            self.menu_tree = et.parse(self.menu_path)
            self.menu_root = self.menu_tree.getroot()

            self.lvl_tree = et.parse(self.level_path)
            self.lvl_root = self.lvl_tree.getroot()

    def get_level_data(self, dbgameid, age, lvl):
        """Checks the xml structure to find a matching dbgameid and level,
        if found returns a list containing data used to build a level"""
        for game in self.lvl_root.iter('game'):
            if str(dbgameid) in (game.attrib["dbids"]).split(", "):
                if age == 7 and int(game.attrib["show_all"]) == 1 or int(game.attrib["min_age"]) <= age <= int(game.attrib["max_age"]):
                    for levels in game.iter("levels"):
                        for level in levels.iter("level"):
                            if int(level.attrib["n"]) == lvl:
                                if age == 7 and int(game.attrib["show_all"]) == 1:
                                    self.mainloop.config.max_age = int(game.attrib["max_age"])
                                return ast.literal_eval(level.attrib["data"])
        return None

    def get_chapters(self, dbgameid, age):
        """Checks the xml structure to find a matching dbgameid and level,
        if found returns a list containing data used to build a level"""
        for game in self.lvl_root.iter('game'):
            if str(dbgameid) in (game.attrib["dbids"]).split(", "):
                if age == 7 and int(game.attrib["show_all"]) == 1 or int(game.attrib["min_age"]) <= age <= int(game.attrib["max_age"]):
                    for chapter in game.iter("chapters"):
                        return ast.literal_eval(chapter.attrib["data"])
        return None

    def get_level_count(self, dbgameid, age):
        """Checks the xml structure to find a matching dbgameid and level,
        if found returns a list containing data used to build a level"""
        for game in self.lvl_root.iter('game'):
            if str(dbgameid) in (game.attrib["dbids"]).split(", "):
                if age == 7 and int(game.attrib["show_all"]) == 1 or int(game.attrib["min_age"]) <= age <= int(game.attrib["max_age"]):
                    for levels in game.iter("levels"):
                        return [int(levels.attrib["games_per_level"]), int(levels.attrib["count"])]
        return None

    def get_show_all_ages(self, dbgameid):
        """Checks the xml structure to find a matching dbgameid and level,
        if found returns a list containing data used to build a level"""
        for game in self.lvl_root.iter('game'):
            if str(dbgameid) in (game.attrib["dbids"]).split(", "):
                if int(game.attrib["show_all"]) == 1:
                    return [int(game.attrib["min_age"]), int(game.attrib["max_age"])]
        return None


class XMLLangs:
    def __init__(self):
        self.lang_path = ""
        self.load_xml_lng()

    def load_xml_lng(self):
        # check for language specific files:
        reload_file = False
        if self.lang_path != os.path.join('xml', 'langs.xml'):
            self.lang_path = os.path.join('xml', 'langs.xml')
            reload_file = True

        if reload_file:
            self.lang_tree = et.parse(self.lang_path)
            self.lang_root = self.lang_tree.getroot()

    def get_lang_config(self, lng_code):
        for lang in self.lang_root.iter('lang'):
            if lng_code == (lang.attrib["code"]):
                return lang
        return None

    def get_tts_disabled(self):
        tts_disabled = []
        for lang in self.lang_root.iter('lang'):
            if lang.attrib["voice"] == "None":
                tts_disabled.append(lang.attrib["code"])
        return tts_disabled
