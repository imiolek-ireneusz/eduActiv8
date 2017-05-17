#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ast
import xml.etree.cElementTree as ET

class XMLConn:
    def __init__(self):
        self.menu_tree = ET.parse(os.path.join('xml', 'menu.xml'))
        self.menu_root = self.menu_tree.getroot()

        self.lvl_tree = ET.parse(os.path.join('xml', 'levels.xml'))
        self.lvl_root = self.lvl_tree.getroot()

    """
    def get_cat_groups_remove(self):
        cg = []
        for cat_group in self.root:
            cg.append(cat_group)
        return cg
    """

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

    """
        def get_level_data(self, dbgameid, lvl):
        for game in self.root.iter('game'):
            if dbgameid == int(game.attrib["dbid"]):
                print("found game")
                for levels in game.iter("levels"):
                    for level in levels.iter("level"):
                        if int(level.attrib["n"]) == lvl:
                            return ast.literal_eval(level.attrib["data"])
        return None
    """

if __name__ == "__main__":
    xmlc = XMLConn()
    cg = xmlc.get_cat_groups()
    print(cg[0].attrib['title'])

"""
a = ""
#go throught entire xml file
for cat_group in self.root:
    cat_group_id = cat_group.attrib["id"]
    for cat in cat_group:
        cat_id = cat.attrib["id"]
        for game in cat:
            a = game.attrib["id"]
            for level in game:
                b = ast.literal_eval(level.attrib["data"])

#iterate over games to get the right id and print levels
gid = "7"
lvlx = 3






print(get_lvl_data(root, gid, lvlx))

"""

"""
for game in root.iter('game'):
    if gid == game.attrib["dbgameid"]:
        #print(game.attrib["dbgameid"])
        for level in game.iter("level"):
            if int(level.attrib["n"]) == lvl:
                print(ast.literal_eval(level.attrib["data"]))
        break
"""

"""
print("As an Element, root has a tag and a dictionary of attributes:")
print(root.tag)
print(root.attrib)
print("")

print("It also has children nodes over which we can iterate:")
for top_cat in root:
    print top_cat.tag, top_cat.attrib
    for cat in top_cat:
        print cat.tag, cat.attrib
        for game in cat:
            print game.tag, game.attrib
            if game.attrib["variant"] == '2':
                print("variant 2")
print("")
print("Children are nested, and we can access specific child nodes by index:")
#print(root[0][1].text)
print("")

#Finding interesting elements
print("Element has some useful methods that help iterate recursively over all the sub-tree below it (its children, their children, and so on). For example, Element.iter():")
for category in root.iter('category'):
    print category.attrib
print("")
    
print("Element.findall() finds only elements with a tag which are direct children of the current element. Element.find() finds the first child with a particular tag, and Element.text accesses the element’s text content. Element.get() accesses the element’s attributes:")
for game in root.findall('game'):
    rank = game.find('level').text
    name = game.get('title')
    print name, rank
print("")
"""
