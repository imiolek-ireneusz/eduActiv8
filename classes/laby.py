# -*- coding: utf8 -*-
"""
Laby, par Mehdi Cherti 2010(mehdidc): 
    - generation d'un labyrinthe
    - utilisation de l'algorithme astar pour trouver le a_path le plus court(selection de la destination avec la souris)

Laby, 2010 by Mehdi Cherti(mehdidc):
- Generation of a labyrinth
- Use of astar algorithm to find the shortest path(selection of the destination with the mouse) #removed
downloaded from:
    http://www.pythonfrance.com/codes/GENERATION-LABYRINTHE-AVEC-RECHERCHE-CHEMIN-PLUS-COURT-AVEC_51293.aspx
    
Rebuild and translated by Ireneusz Imiolek
"""

import pygame
from  random import randint, choice


class def_const:
    def __getattr__(self, attr):
        return Const.__dict__[attr]

    def __setattr__(self, attr, value):
        if attr in self.__dict__.keys():
            raise Exception("Impossible to redefine the constant")
        else:
            self.__dict__[attr] = value

    def __str__(self):
        return self.__dict.__str__()


const = def_const()
""" definitions des constantes """

# colours
const.white = (255, 255, 255)
const.pink = (255, 0, 255)
const.black = (0, 0, 0)
const.yellow = (255, 255, 0)

# directions
const.right = 0
const.left = 1
const.up = 2
const.down = 3


class Point:
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]


"""Laby Cell Class definition"""


class Laby_cell:
    def __init__(self):
        self.state = False
        self.laby_doors = [True, True, True, True]  # Right, Left, Up, Down


""" Laby Class """


class laby:
    def __init__(self, w, h, sx=0, sy=0, scale=30, col=(0, 0, 0), line_width = 3):
        self.w = w
        self.h = h
        self.color = col
        self.line_width = line_width
        self.Laby_cells = []
        self.wc = scale  # const.wc
        self.hc = scale  # const.hc
        self.sx = sx
        self.sy = sy
        self.displayed_once = True

        """ Laby_cells initialization for each Laby_cell, it initializes its position in the labyrinth """
        for v in range(self.w * self.h):
            a = Laby_cell()
            a.x = v % self.w
            a.y = v // self.w
            self.Laby_cells.append(a)

    """ returns the Laby_cell corresponding to the position(x, y) """

    def get_cell(self, x, y):
        return self.Laby_cells[x + y * self.w]

    """ return direction opposite to a direction """

    def notdir(self, dir):
        if dir == const.right: return const.left
        if dir == const.left: return const.right
        if dir == const.up: return const.down
        if dir == const.down: return const.up

    """ generation of the labyrinth """

    def generate_laby(self, x=-1, y=-1):
        if x == -1:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)
        cell_act = self.get_cell(x, y)
        if not cell_act.state:
            cell_act.state = True
            tab = []
            if x + 1 < self.w and not self.get_cell(x + 1, y).state: tab.append((x + 1, y, const.right))
            if x - 1 >= 0 and not self.get_cell(x - 1, y).state: tab.append((x - 1, y, const.left))
            if y - 1 >= 0 and not self.get_cell(x, y - 1).state: tab.append((x, y - 1, const.up))
            if y + 1 < self.h and not self.get_cell(x, y + 1).state: tab.append((x, y + 1, const.down))
            if tab:
                while tab:
                    C = choice(tab)
                    if not self.get_cell(C[0], C[1]).state:
                        cell = self.get_cell(C[0], C[1])
                        cell_act.laby_doors[C[2]] = False
                        cell.laby_doors[self.notdir(C[2])] = False
                        self.generate_laby(C[0], C[1])
                    tab.remove(C)
                return True
            else:
                return False

    """ display the labyrinth """

    def show(self, buffer):
        W, H = self.wc, self.hc
        sx, sy = self.sx, self.sy
        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)
                if c.laby_doors[const.right]:
                    pygame.draw.line(buffer, self.color, (sx + (x + 1) * W, sy + y * H),
                                     (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)
                if c.laby_doors[const.down]:
                    pygame.draw.line(buffer, self.color, (sx + (x) * W, sy + (y + 1) * H),
                                     (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)
        x = self.w - 1
        for y in range(self.h - 1):
            c = self.get_cell(x, y)
            if c.laby_doors[const.down]:
                pygame.draw.line(buffer, self.color, (sx + x * W, sy + (y + 1) * H),
                                 (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)
        y = self.h - 1
        for x in range(self.w - 1):
            c = self.get_cell(x, y)
            if c.laby_doors[const.right]:
                pygame.draw.line(buffer, self.color, (sx + (x + 1) * W, sy + (y) * H),
                                 (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)

    """ create the labyrinth grid table twice as big as the original laby"""

    def labi_to_array(self):
        W, H = self.wc, self.hc
        sx, sy = self.sx, self.sy
        labi_grid = [[0 for x in range(0, self.w * 2 - 1)] for y in range(0, self.h * 2 - 1)]
        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)
                if c.laby_doors[const.right]:
                    gx = x * 2 + 1
                    gy = y * 2
                    labi_grid[gy][gx] = 1
                    if y > 0:
                        labi_grid[gy - 1][gx] = 1
                    if y < self.h - 1:
                        labi_grid[gy + 1][gx] = 1
                if c.laby_doors[const.down]:
                    gx = x * 2
                    gy = y * 2 + 1
                    labi_grid[gy][gx] = 1
                    if x > 0:
                        labi_grid[gy][gx - 1] = 1
                    if x < self.w - 1:
                        labi_grid[gy][gx + 1] = 1
        x = self.w - 1
        for y in range(self.h - 1):
            c = self.get_cell(x, y)
            if c.laby_doors[const.down]:
                gx = x * 2
                gy = y * 2 + 1
                labi_grid[gy][gx] = 1
                labi_grid[gy][gx - 1] = 1
        y = self.h - 1
        for x in range(self.w - 1):
            c = self.get_cell(x, y)
            if c.laby_doors[const.right]:
                gx = x * 2 + 1
                gy = y * 2
                labi_grid[gy][gx] = 1
                labi_grid[gy - 1][gx] = 1
        return labi_grid
