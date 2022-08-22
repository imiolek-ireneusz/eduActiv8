# -*- coding: utf-8 -*-

# a script used to convert list of words in GCompris json format to the format used by eduActiv8,
# which is a number of theme grouped dictionaries with lists of words inside
# where a word is not found it will be in brackets like so: <word>
# the activities have been updated to ignore untranslated words
#
# run with python3 - to keep the utf-8 formatting

import re
import word_list
import copy

#lang_files = ["content-es.json", "content-ca.json", "content-it.json", "content-pt.json"]
lang_files = ["content-fi.json"]

ea8_lists_str = ["a4a_animals", "a4a_sport", "a4a_body", "a4a_people", "a4a_food", "a4a_clothes_n_accessories",
                 "a4a_actions", "a4a_construction", "a4a_nature", "a4a_jobs", "a4a_fruit_n_veg", "a4a_transport"]

key_pattern = '^\s+"(.*?).ogg"'
value_pattern = '^\s+"[a-z]+.ogg": "(.*?)"'
k_prog = re.compile(key_pattern)
v_prog = re.compile(value_pattern)

for lang_id in range(len(lang_files)):
    d = copy.deepcopy(word_list.d)
    ea8_lists = list()
    missing_words = list()
    for i in range(len(ea8_lists_str)):
        ea8_lists.append(d[ea8_lists_str[i]])

    #read language file
    with open(lang_files[lang_id], "r") as myfile:
        fl = myfile.readlines()

    #create directory for all words in GCompris file
    gcomp_dict = dict()

    #go over all lines looking for key and value pairs
    for each in fl:
        m = k_prog.match(each)
        if m is not None:
            key = m.group(1)
            m = v_prog.match(each)
            if m is not None:
                value = m.group(1)
                gcomp_dict[key] = value

    # go over all eduactiv8 lists of words replacing them with the translated version
    ind = 0
    lang_count = 0
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

        # check if number of words that have been translated is sufficient for use - display a message if less than 12
        if count < 12:
            print("%s - %s - only %d words translated" % (lang_files[lang_id][8:10], ea8_lists_str[ind], count))
        lang_count += count
        ind += 1

    print("%s - %d out of 585 words translated\n" % (lang_files[lang_id][8:10], lang_count))

    # create a new string with converted word lists
    s = ""
    for i in range(len(ea8_lists)):
        s += '\nd["%s"] = %s' % (ea8_lists_str[i], repr(ea8_lists[i]))

    s += '\n\n"""\nmissing words %d\n%s\n"""' % (len(missing_words), repr(missing_words))

    # save to file
    with open("gcomp2ea8_%s.txt" % (lang_files[lang_id][8:10]), 'w') as f:
        f.write(s)

print("ALL DONE!!!")
