# -*- coding: utf-8 -*-

# Script used to convert current lists of words to the gettext po format to enable translation

# run with python3 - to keep the utf-8 formatting

import os
import a4a_words

import a4a_py.ca, a4a_py.de, a4a_py.el, a4a_py.en_GB, a4a_py.en_US, a4a_py.es, a4a_py.fr, a4a_py.it, a4a_py.lkt, a4a_py.pl, a4a_py.pt, a4a_py.ru, a4a_py.uk, a4a_py.bg

#lang_list = ['ca', 'de', 'el', 'en_GB', 'en_US', 'es', 'fi', 'fr', 'it', 'lkt', 'pl', 'pt', 'ru', 'sr', 'uk']
#mod_list = [ca, de, el, en_gb, en_us, es, fi, fr, it, lkt, pl, pt, ru, sr, uk]

#lang_list = ['ca', 'de', 'el', 'en_GB', 'en_US', 'es', 'fr', 'it', 'lkt', 'pl', 'pt', 'ru', 'uk']
#mod_list = [a4a_py.ca, a4a_py.de, a4a_py.el, a4a_py.en_GB, a4a_py.en_US, a4a_py.es, a4a_py.fr, a4a_py.it, a4a_py.lkt, a4a_py.pl, a4a_py.pt, a4a_py.ru, a4a_py.uk]

#lang_list = ['bg']
#mod_list = [a4a_py.bg]

lang_list = ['bg']
mod_list = [a4a_py.bg]

lists_str = ["a4a_animals", "a4a_sport", "a4a_body", "a4a_people", "a4a_food", "a4a_clothes_n_accessories", "a4a_actions", "a4a_construction", "a4a_nature", "a4a_jobs", "a4a_fruit_n_veg", "a4a_transport"]

lists_len = len(lists_str)
langs_len = len(lang_list)

header = """# eduActiv8 - word lists - translation file.
# Copyright (C) 2019 Ireneusz Imiolek
# This file is part of the eduActiv8 project and is distributed under GPLv3 licence.
#
msgid ""
msgstr ""
"Project-Id-Version: 4.19.02\\n"
"Report-Msgid-Bugs-To: Ireneusz Imiolek <imiolek.i@gmail.com>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"""

# find strings and add to po file
for lang in range(0, langs_len):
    s = header + '"Language: %s\\n"\n\n' % lang_list[lang]
    for i in range(0, lists_len):
        for j in range(0, len(a4a_words.d[lists_str[i]])):
            a = mod_list[lang]
            a = mod_list[lang].d[lists_str[i]]
            try:
                a = mod_list[lang].d[lists_str[i]][j]
            except:
                print(mod_list[lang].d[lists_str[i]])
                print(len(a))

            a = mod_list[lang].d[lists_str[i]][j][0]
            if mod_list[lang].d[lists_str[i]][j][0] != "<":
                s += 'msgid "%s"\nmsgstr "%s"\n\n' % (a4a_words.d[lists_str[i]][j], mod_list[lang].d[lists_str[i]][j])
            else:
                s += 'msgid "%s"\nmsgstr ""\n\n' % (a4a_words.d[lists_str[i]][j])

    # save to file
    file_name = os.path.join('a4a_po', "%s.po" % (lang_list[lang]))
    with open(file_name, 'w') as f:
        f.write(s)

# create pot
s = header + '"Language: en_GB\\n"\n\n'
for i in range(0, lists_len):
    for j in range(0, len(a4a_words.d[lists_str[i]])):
        s += 'msgid "%s"\nmsgstr ""\n\n' % (a4a_words.d[lists_str[i]][j])

# save pot to file
file_name = os.path.join('a4a_po', "a4a_word_list.pot")
with open(file_name, 'w') as f:
    f.write(s)

print("DONE!!!")
