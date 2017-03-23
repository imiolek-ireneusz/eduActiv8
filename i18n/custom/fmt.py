import os
import sys

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

l1 = ['Ànec', 'Barca', 'Coala', 'Calçat', 'Dofí', 'Elefant', 'Formiga', 'Gat', 'Hipopotam', 'Iglú', 'Joguina', 'Kiwi',
      'Lleó', 'Mússol', 'Nit', 'Oceà', 'Poma', 'Quadern', 'Ratolí', 'Síndria', 'Tomàquet', 'Ull', 'Violí', 'Windsurf',
      'Xilofon', 'Yoga', 'Zebra']

l2 = []
for each in l1:
    s = "<1>" + each[0] + "<2>" + each[1:]
    l2.append(s)

print(l2)
