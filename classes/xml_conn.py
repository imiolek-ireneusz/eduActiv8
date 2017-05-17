#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ast
import xml.etree.cElementTree as et

class XMLConn:
    def __init__(self):
        self.menu_tree = et.parse(os.path.join('xml', 'menu.xml'))
        self.menu_root = self.menu_tree.getroot()

        self.lvl_tree = et.parse(os.path.join('xml', 'levels.xml'))
        self.lvl_root = self.lvl_tree.getroot()

    def get_level_data(self, dbgameid, lvl):
        """Checks the xml structure to find a matching dbgameid and level,
        if found returns a list containing data used to build a level"""
        for game in self.lvl_root.iter('game'):
            if dbgameid == int(game.attrib["dbid"]):
                for levels in game.iter("levels"):
                    for level in levels.iter("level"):
                        if int(level.attrib["n"]) == lvl:
                            return ast.literal_eval(level.attrib["data"])
        return None

    def get_chapters(self, dbgameid):
        """Checks the xml structure to find a matching dbgameid and level,
        if found returns a list containing data used to build a level"""
        for game in self.lvl_root.iter('game'):
            if dbgameid == int(game.attrib["dbid"]):
                for chapter in game.iter("chapters"):
                    return ast.literal_eval(chapter.attrib["data"])
        return None

    def get_level_count(self, dbgameid):
        """Checks the xml structure to find a matching dbgameid and level,
        if found returns a list containing data used to build a level"""
        for game in self.lvl_root.iter('game'):
            if dbgameid == int(game.attrib["dbid"]):
                for levels in game.iter("levels"):
                    return [int(levels.attrib["games_per_level"]), int(levels.attrib["count"])]
        return None
