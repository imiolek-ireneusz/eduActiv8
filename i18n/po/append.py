# A helper program to add new keys to all language files at once.
# The key still have to be added to the default.py and default.pot

import os
import sys

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

# list of language files
langs = ["ca.po", "el.po", "en_GB.po", "en_US.po", "pl.po", "es_ES.po", "pt_PT.po", "fr.po", "it.po", "de.po", "ru.po",
         "fi.po", "te_ST.po"]

# lines = ["Word Builder - Sports","Word Builder - Body","Word Builder - People","Word Builder - Actions","Word Builder - Constructions","Word Builder - Nature","Word Builder - Jobs","Word Builder - Clothes and Accessories","Word Builder - Fruits and Vegetables","Word Builder - Transport","Word Builder - Food"]
lines = []


def add_all():
    for lang in langs:
        FILE = lang
        with open(FILE, "a") as f:
            for line in lines:
                f.write('\n\nmsgid "%s"' % line)
                f.write('\nmsgstr ""')


if __name__ == "__main__":
    add_all()
    print("Done!")

"""
argv = sys.argv
if len(argv) == 2:
    line = argv[1]
else:
    print("Enter the line to be added to all files (or press ENTER to exit):")
    line = raw_input()

if len(line) > 2 and line not in ["exit", "exit()", "cancel", "cancel()"]:
    for i in range(len(langs)):
        FILE = langs[i]
        with open(FILE,"a") as f:
            f.write("\n"+line)
    print("Completed...")
else:
    print("Aborting...")
"""
