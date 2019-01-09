# A helper program to add new keys to all language files at once.
# The key still have to be added to the default.py and default.pot

import os
import sys

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

# list of language files
langs = ["ca.po", "de.po", "el.po", "es_ES.po", "fi.po", "fr.po", "he.po", "it.po", "lkt.po", "pl.po", "pt_PT.po", "ru.po", "sk.po", "sr.po", "uk.po", "zh.po"]
langs2 = ["en_GB.po", "en_US.po"]

#lines = ["lines to", " add"]
lines = []

def add_all():
    for lang in langs:
        FILE = lang
        with open(FILE, "a") as f:
            for line in lines:
                f.write('\n\nmsgid "%s"' % line)
                f.write('\nmsgstr ""')

    for lang in langs2:
        FILE = lang
        with open(FILE, "a") as f:
            for line in lines:
                f.write('\n\nmsgid "%s"' % line)
                f.write('\nmsgstr "%s"' % line)


if __name__ == "__main__":
    add_all()
    print("Done!")