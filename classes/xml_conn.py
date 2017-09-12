#!/usr/bin/env python
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
        self.menu_tree = et.parse(os.path.join('xml', 'menu.xml'))
        self.menu_root = self.menu_tree.getroot()

        self.lvl_tree = et.parse(os.path.join('xml', 'levels.xml'))
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
