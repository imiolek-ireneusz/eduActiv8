# -*- coding: utf-8 -*-

from classes.extras import get_word_list, word_typing_course
from i18n.custom.kbrd.en_course import base_qwerty
from i18n.custom.kbrd.pl_cinderella import cinderella
from i18n.custom.word_lists.pl_di import di

# each sub-list in the course list is a level - the more the sub-lists the more levels game will have
# each level consists of two lists: groups of words and corresponding number of repetitions for each group

course = []
# add English qwerty course
course.extend(base_qwerty)

# create additional, Polish specific course data
pl_course = [
    # lvl10 - Polish Letter Introduction
    [[4, 4, 4, 4, 4, 4, 4, 4, 4],
     ["aą kąt ", "cć ćma ", "eę sęk ", "lł łąka ", "nń koń ", "oó mrówka ", "sś ściana ", "xź źdźbło ", "zż żółw "]
     ],

    # lvl11 - Polish Letter Introduction - uppercase
    [[4, 4, 4, 4, 4, 4, 4, 4, 4],
     ["AĄ kąt ", "CĆ Ćma ", "EĘ sęk ", "LŁ Łąka ", "NŃ koń ", "OÓ mrówka ", "SŚ Ściana ", "XŹ Źdźbło ", "ZŻ Żółw "]
     ]]

# add it to the course
course.extend(pl_course)

# add Language specific word list - words taken from pl_di.py file.
word_list = get_word_list(di)
word_course = word_typing_course(word_list)
course.extend(word_course)
course.extend(cinderella)
