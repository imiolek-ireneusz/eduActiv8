# A helper program to add new keys to all language files at once.
# The key still have to be added to the default.py and default.pot

import os
import sys

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

# recreates the default.pot file removing all translated entries

def add_all():
    FILE = "default.pot"
    FILE2 = "default2.pot"
    with open(FILE, "r") as f1:
        with open(FILE2, "w") as f2:
            array = []
            for line in f1:
                array.append(line)

            for line in array:
                if line.startswith("msgstr \""):
                    f2.write("msgstr \"\"\n")
                elif line.startswith("msgstr[0]"):
                    f2.write("msgstr[0] \"\"\n")
                elif line.startswith("msgstr[1]"):
                    f2.write("msgstr[1] \"\"\n")
                else:
                    f2.write(line)

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
