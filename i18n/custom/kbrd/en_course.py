# -*- coding: utf-8 -*-
from classes.extras import get_word_list, word_typing_course
from i18n.custom.kbrd.en_cinderella import cinderella
from i18n.custom.word_lists.en_gb_di import di

base_qwerty = [
    # lvl1 - learning home keys asdf jkl
    [[3, 3, 3, 3, 3, 3],
     ["asdf fdsa ", "jkl lkj ", "asdf jkl lkj fdsa ", "ajskdlf fldksja ", "alskdjf fjdksla ", "adjlskf ljdakfs "]
     ],

    # lvl2 - adding g and h
    [[3, 3, 3, 3, 3, 3],
     ["asdfg gfdsa ", "hjkl lkjh ", "asdfg hjkl lkjh gfdsa ", "ajskdlfhg ghfldksja ", "alskdjfhg ghfjdksla ",
      "adghkl sfhgjl "]
     ],

    # lvl3 - training left hand - learning letters - qwert
    [[4, 4, 5, 3, 3, 3, 3, 3, 3, 3, 3],
     ["frf ftf ", "aqa sws ded frf ftf ", "qawsedrftg gtfrdeswaq ", "qaedtgwsrf frswgtdeaq ", "aswesd erdfrtfg ",
      "gftrfdre dsewsa ", "awdrg tfesq ", "qseft grdwa ", "arqf fqra ", "aefw wfea ", "earswdef fedwsrae "]
     ],

    # lvl4 - adding right hand - learning letters - nm
    [[4, 4, 4, 3, 3, 3, 3],
     ["hnajms kndlmf ", "nanq msmw ", "qnwmenrm ", "qjwkelr rlekwjq ", "tjfrkfekd wlsqla ", "qajwskedl rfktfj ",
      "namsjd kflgf "]
     ],

    # lvl5 - learning letters - yuiop
    [[4, 4, 4, 3, 3, 3, 3],
     ["jyj juj ", "jyj juj kik lol pop ", "jnyj jmuj ", "kiujk loikj ", "polkiuj jnhuj kmjik ", "plokijuhy hyjukilop ",
      "yhikujolp pokuh "]
     ],

    # lvl6 - learning letters - zxcvb
    [[4, 4, 4, 3, 3],
     ["fbf fvf ", "fbf fvf dcd sxs aza ", "awdx sefc drgv ", "azs sxd dcf fvg ", "azsxdcfvb bvfcdxsza "]
     ],

    # lvl7 - learning uppercase letters
    [[3, 3, 3],
     ["As Sd Df Fg Gh Hj Jk Kl L; ", "Qa Ws Ed Rf Tf Yj Uj Ik Ol P; ", "Za Xs Cd Vf Bf Nj Mj "]
     ],

    # lvl8 - learning position of ", . ; : ?" !
    [[2, 2],
     ["k,k l.l ;p; ", "ok? ok! ok, ok. "]
     ],

    # lvl9 - quick home keys revision
    [[2, 2],
     ["aqaza swsxs dedcd frftfvfbfgf ", "jyjujnjmjhj kik,k lol.l ;p; "]
     ]]

course = []

# add English qwerty course
course.extend(base_qwerty)

# add Language specific word list - words taken from en_gb_di.py file.
word_list = get_word_list(di)
word_course = word_typing_course(word_list)
course.extend(word_course)
course.extend(cinderella)
