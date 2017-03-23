# -*- coding: utf-8 -*-
from classes.extras import get_word_list, word_typing_course
from i18n.custom.kbrd.fr_cinderella import cinderella
from i18n.custom.word_lists.fr_di import di

base_qwerty = [
    # lvl1 - learning home keys qsdf jklm
    [[3, 3, 3, 3, 3, 3],
     ["qsdf fdsq ", "jklm mlkj ", "qsdf jklm mlkj fdsq ", "qjskdlfm mfldksjq ", "qmsldkfj fjdkslqm ",
      "qdjlsfkm mkdsljdq "]
     ],

    # lvl2 - adding g and h
    [[3, 3, 3, 3, 3, 3],
     ["qsdfg gfdsq ", "hjklm mlkjh ", "qsdfg hjklm mlkjh gfdsq ", "qjskdlfmhg ghfmldksjq ", "qmsldkfjgh hgjfkdlsmq ",
      "qdgjl sfhkm "]
     ],

    # lvl3 - training left hand - learning letters - azert
    [[4, 4, 5, 3, 3, 3, 3, 3, 3, 3, 3],
     ["frf ftf ", "qaq szs ded frf ftf ", "aqzsedrftg gtfrdeszaq ", "aqedtgzsrf frszgtdeqa ", "qszesd erdfrtfg ",
      "gftrfdre dsezsq ", "azdrg tfesa ", "aseft grdzq ", "qrqf fqrq ", "qefz zfeq ", "eqrszdef fedzsrqe "]
     ],

    # lvl4 - adding right hand - learning letters - nm
    [[4, 4, 4, 3, 3, 3, 3],
     ["hnqjns kndlnfmng", "nqna nsnz ", "qnemenrn ", "ajzkelrm rmelzkaj ", "tjfrkfekd zlsalq ", "aqjzskedl rfktfj ",
      "nqmsjd kflgfm "]
     ],

    # lvl5 - learning letters - yuiop
    [[4, 4, 4, 3, 3, 3, 3],
     ["jyj juj ", "jyj juj kik lol mpm ", "jnyj knyj ", "kiujk loikj ", "polkiuj jnhuj kmjik ",
      "pmolikujyh hyjukilomp ", "yhikujolpm pokuh "]
     ],

    # lvl6 - learning letters - zxcvb
    [[4, 4, 4, 3, 3],
     ["fbf fvf ", "fbf fvf dcd sxs qwq ", "qzdx sefc drgv ", "qws sxd dcf fvg ", "qwsxdcfvb bvfcdxswq "]
     ],

    # lvl7 - learning uppercase letters
    [[3, 3, 3],
     ["Qs Sd Df Fg Gh Hj Jk Kl Lm ", "Aa Zs Ed Rf Tf Yj Uj Ik Ol Pm ", "Wa Xs Cd Vf Bf Nj "]
     ],

    # lvl8 - learning position of ", . ; : ?" !
    [[2, 2],
     ["k,k l.l ;p; ", "ok? ok! ok, ok. "]
     ],

    # lvl9 - quick home keys revision
    [[2, 2],
     ["qaqwq szsxs dedcd frfvf gtgbg", "hyhnh juj,j kik;k lol:l mpm!m "]
     ]]

fr_course = [
    # lvl10 - French Letters Introduction
    [[1, ],
     ["àzer âzer æscf çijn érty èfvg êdcf ëzaq îopml ïuolj ôpimlk ùyikh ûhkiy üyhki ÿuio "]
     ]]

course = []

# add "qwerty" course - in fact it's azerty in this case
course.extend(base_qwerty)
course.extend(fr_course)

# add Language specific word list - words taken from fr_di.py file.
word_list = get_word_list(di)
word_course = word_typing_course(word_list)
course.extend(word_course)
course.extend(cinderella)
