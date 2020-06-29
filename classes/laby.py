# -*- coding: utf8 -*-
"""
Laby, par Mehdi Cherti 2010(mehdidc): 
    - generation d'un labyrinthe
    - utilisation de l'algorithme astar pour trouver le a_path le plus court(selection de la destination avec la souris)

Laby, 2010 by Mehdi Cherti(mehdidc):
- Generation of a labyrinth
- Use of astar algorithm to find the shortest path (selection of the destination with the mouse) # removed
Available at:
    http://www.pythonfrance.com/codes/GENERATION-LABYRINTHE-AVEC-RECHERCHE-CHEMIN-PLUS-COURT-AVEC_51293.aspx
    
Rebuild and translated by Ireneusz Imiolek
"""

import pygame
from random import randint, choice


class LabyCell:
    def __init__(self):
        self.state = False
        self.laby_doors = [True, True, True, True]  # Right, Left, Up, Down


class Laby:
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

        self.right = 0
        self.left = 1
        self.up = 2
        self.down = 3

        self.displayed_once = True

        """ Laby_cells initialization for each Laby_cell, it initializes its position in the labyrinth """
        for v in range(self.w * self.h):
            a = LabyCell()
            a.x = v % self.w
            a.y = v // self.w
            self.Laby_cells.append(a)

    def get_cell(self, x, y):
        """ returns the Laby_cell corresponding to the position(x, y) """
        return self.Laby_cells[x + y * self.w]

    def notdir(self, dir):
        """ return a direction opposite to the direction """
        if dir % 2 == 0:
            return dir + 1
        else:
            return dir - 1

    def generate_laby(self, x=-1, y=-1):
        """ generation of the labyrinth """
        if x == -1:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)
        cell_act = self.get_cell(x, y)
        if not cell_act.state:
            cell_act.state = True
            tab = []
            if x + 1 < self.w and not self.get_cell(x + 1, y).state: tab.append((x + 1, y, self.right))
            if x - 1 >= 0 and not self.get_cell(x - 1, y).state: tab.append((x - 1, y, self.left))
            if y - 1 >= 0 and not self.get_cell(x, y - 1).state: tab.append((x, y - 1, self.up))
            if y + 1 < self.h and not self.get_cell(x, y + 1).state: tab.append((x, y + 1, self.down))
            if tab:
                while tab:
                    c = choice(tab)
                    if not self.get_cell(c[0], c[1]).state:
                        cell = self.get_cell(c[0], c[1])
                        cell_act.laby_doors[c[2]] = False
                        cell.laby_doors[self.notdir(c[2])] = False
                        self.generate_laby(c[0], c[1])
                    tab.remove(c)
                return True
            else:
                return False

    def show(self, bfr):
        """ display the labyrinth """
        W, H = self.wc, self.hc
        sx, sy = self.sx, self.sy
        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)
                if c.laby_doors[self.right]:
                    pygame.draw.line(bfr, self.color, (sx + (x + 1) * W, sy + y * H),
                                     (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)
                if c.laby_doors[self.down]:
                    pygame.draw.line(bfr, self.color, (sx + (x) * W, sy + (y + 1) * H),
                                     (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)
        x = self.w - 1
        for y in range(self.h - 1):
            c = self.get_cell(x, y)
            if c.laby_doors[self.down]:
                pygame.draw.line(bfr, self.color, (sx + x * W, sy + (y + 1) * H),
                                 (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)
        y = self.h - 1
        for x in range(self.w - 1):
            c = self.get_cell(x, y)
            if c.laby_doors[self.right]:
                pygame.draw.line(bfr, self.color, (sx + (x + 1) * W, sy + (y) * H),
                                 (sx + (x + 1) * W, sy + (y + 1) * H), self.line_width)

    def labi_to_array(self):
        """ create the labyrinth grid table twice as big as the original laby. """
        labi_grid = [[0 for x in range(0, self.w * 2 - 1)] for y in range(0, self.h * 2 - 1)]
        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)
                if c.laby_doors[self.right]:
                    gx = x * 2 + 1
                    gy = y * 2
                    labi_grid[gy][gx] = 1
                    if y > 0:
                        labi_grid[gy - 1][gx] = 1
                    if y < self.h - 1:
                        labi_grid[gy + 1][gx] = 1
                if c.laby_doors[self.down]:
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
            if c.laby_doors[self.down]:
                gx = x * 2
                gy = y * 2 + 1
                labi_grid[gy][gx] = 1
                labi_grid[gy][gx - 1] = 1
        y = self.h - 1
        for x in range(self.w - 1):
            c = self.get_cell(x, y)
            if c.laby_doors[self.right]:
                gx = x * 2 + 1
                gy = y * 2
                labi_grid[gy][gx] = 1
                labi_grid[gy - 1][gx] = 1
        return labi_grid
