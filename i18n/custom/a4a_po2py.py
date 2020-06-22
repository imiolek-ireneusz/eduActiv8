# -*- coding: utf-8 -*-

# Script used to convert translated po files with lists of words to the ordered python lists used by activities here
# adapted from the gCompris 2 eduActiv8 converter

# run with python3 - to keep the utf-8 formatting

import re
import a4a_words
import copy
import os
# lang_list = ['ca', 'de', 'el', 'en_GB', 'en_US', 'es', 'fr', 'it', 'lkt', 'pl', 'pt', 'ru', 'uk']

# use this if only one language has changed
lang_list = ['ar']
#lang_list = ['en_GB', 'en_US']

ea8_lists_str = ["a4a_animals", "a4a_sport", "a4a_body", "a4a_people", "a4a_food", "a4a_clothes_n_accessories",
                 "a4a_actions", "a4a_construction", "a4a_nature", "a4a_jobs", "a4a_fruit_n_veg", "a4a_transport"]

key_pattern = '^msgid\s"(.*?)"'
value_pattern = '^msgstr\s"(.*?)"'
k_prog = re.compile(key_pattern)
v_prog = re.compile(value_pattern)

for lang_id in range(len(lang_list)):
    d = copy.deepcopy(a4a_words.d)
    ea8_lists = list()
    missing_words = list()
    for i in range(len(ea8_lists_str)):
        ea8_lists.append(d[ea8_lists_str[i]])

    #read language file
    file_name = os.path.join('a4a_po', "%s.po" % (lang_list[lang_id]))
    with open(file_name, 'r') as f:
        fl = f.readlines()

    #create directory for all words in po file
    gcomp_dict = dict()

    #go over all lines looking for key and value pairs
    current_key = None
    for each in fl:
        if each != 'msgid ""':
            if current_key is None:
                m = k_prog.match(each)
                if m is not None:
                    current_key = m.group(1)
            else:
                m = v_prog.match(each)
                if m is not None:
                    value = m.group(1)
                    gcomp_dict[current_key] = value
                    current_key = None

    # go over all eduactiv8 lists of words replacing them with the translated version
    for lst in ea8_lists:
        count = 0
        for i in range(len(lst)):

            if lst[i] in gcomp_dict:
                s = gcomp_dict[lst[i]]
                if s != "":
                    lst[i] = gcomp_dict[lst[i]]
                    count += 1
                else:
                    missing_words.append(lst[i])
                    lst[i] = "<%s>" % lst[i]
            else:
                missing_words.append(lst[i])
                lst[i] = "<%s>" % lst[i]

    # create a new string with converted word lists
    s = "# -*- coding: utf-8 -*-\n\n"
    if lang_list[lang_id] in ["ar", "he"]:
        s += 'from classes.extras import reverse\n\n\n'
        s += 'def r(s):\n'
        s += '    return reverse(s, None, "' + lang_list[lang_id] + '")\n\n\n'

        s += 'd = dict()\n'
        for i in range(len(ea8_lists)):
            s += '\nd["%s"] = [' % (ea8_lists_str[i])
            l = len(ea8_lists[i])
            for j in range(l):
                if j < l - 1:
                    s += "r('" + ea8_lists[i][j] + "'), "
                else:
                    s += "r('" + ea8_lists[i][j] + "')"
            s += ']'

    else:
        s += 'd = dict()\n\n'
        for i in range(len(ea8_lists)):
            s += '\nd["%s"] = %s' % (ea8_lists_str[i], repr(ea8_lists[i]))

    # save to file
    file_name = os.path.join('a4a_py', "%s.py" % (lang_list[lang_id]))
    with open(file_name, 'w') as f:
        f.write(s)

print("ALL DONE!!!")
