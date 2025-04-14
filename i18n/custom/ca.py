# -*- coding: utf-8 -*-

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The color names in other languages than English are already in smaller font.

# word list adapted from GCompris:
# https://github.com/gcompris/GCompris-qt/blob/master/src/activities/lang/resource/content-ca.json

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

numbers = ['u', 'dos', 'tres', 'quatre', 'cinc', 'sis', 'set', 'vuit', 'nou', 'deu', 'onze', 'dotze', 'tretze',
           'catorze', 'quinze', 'setze', 'disset', 'divuit', 'dinou', 'vint', 'vint-i-u', 'vint-i-dos', 'vint-i-tres',
           'vint-i-quatre', 'vint-i-cinc', 'vint-i-sis', 'vint-i-set', 'vint-i-vuit', 'vint-i-nou']
numbers2090 = ['vint', 'trenta', 'quaranta', 'cinquanta', 'seixanta', 'setanta', 'vuitanta', 'noranta']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Ànec', 'Barca', 'Coala', 'Calçat', 'Dofí', 'Elefant', 'Formiga', 'Gat',
                                      'Hipopòtam', 'Iglú', 'Joguina', 'Kiwi', 'Lleó', 'Mussol', 'Nit', 'Oceà', 'Poma',
                                      'Quadern', 'Ratolí', 'Síndria', 'Tomàquet', 'Ull', 'Violí', 'Windsurf', 'Xilòfon',
                                      'Yoga', 'Zebra']
d['abc_flashcards_word_sequence'] = ['<1>À<2>nec', '<1>B<2>arca', '<1>C<2>oala', '<2>Cal<1>ç<2>at', '<1>D<2>ofí',
                                     '<1>E<2>l<1>e<2>fant', '<1>F<2>ormiga', '<1>G<2>at', '<1>H<2>ipopòtam',
                                     '<1>I<2>glú', '<1>J<2>oguina', '<1>K<2>iwi', '<1>L<2>leó', '<1>M<2>ussol',
                                     '<1>N<2>it', '<1>O<2>ceà', '<1>P<2>oma', '<1>Q<2>uadern', '<1>R<2>atolí',
                                     '<1>S<2>índria', '<1>T<2>omàque<1>t', '<1>U<2>ll', '<1>V<2>iolí', '<1>W<2>indsurf',
                                     '<1>X<2>ilòfon', '<1>Y<2>oga', '<1>Z<2>ebra']
 

d['abc_flashcards_frame_sequence'] = [3, 1, 72, 60, 59, 4, 0, 2, 47, 8, 58, 74, 11, 14, 54, 52, 42, 13, 12, 26, 33, 75,
                                      21, 66, 23, 32, 25]

# alphabet ca
alphabet_lc = ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['à', 'é', 'è', 'í', 'ò', 'ó', 'ú', '-']
accents_uc = ['À', 'É', 'È', 'Í', 'Ò', 'Ó', 'Ú']


def n2txt(n, twoliner=False):
    """takes a number from 0 - 100 and returns it back in a word form, ie: 63 returns 'sixty three'."""
    if 0 < n < 30:
        return numbers[n - 1]
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090[(n // 10) - 2]
        if m == 0:
            return tens
        elif m > 0:
            ones = numbers[m - 1]
            if twoliner:
                return [tens + "-", ones]
            else:
                return tens + "-" + ones

    elif n == 0:
        return "zero"
    elif n == 100:
        return "cent"
    return ""


hores = ['una', 'dues', 'tres', 'quatre', 'cinc', 'sis', 'set', 'vuit', 'nou', 'deu', 'onze', 'dotze', 'una']


def time2str(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55"""
    if m > 7:
        if h == 12:
            h = 1
        else:
            h += 1

    if h == 1:
        if m == 0:
            return "la una en punt"
        elif m == 1:
            return "la una i un minut"
        elif 0 < m < 8:
            return "la una i %s" % n2txt(m)
        elif 7 < m < 15:
            return "un quart menys %s d'una" % n2txt(15 - m)
        elif m == 15:
            return "un quart d'una"
        elif 15 < m < 23:
            return "un quart i %s d'una" % n2txt(m - 15)
        elif 22 < m < 30:
            return "dos quarts menys %s d'una" % n2txt(30 - m)
        elif m == 30:
            return "dos quarts d'una"
        elif 30 < m < 38:
            return "dos quarts i %s d'una" % n2txt(m - 30)
        elif 37 < m < 45:
            return "tres quarts menys %s d'una" % n2txt(45 - m)
        elif m == 45:
            return "tres quarts d'una"
        elif 45 < m < 53:
            return "tres quarts i %s d'una" % n2txt(m - 45)
        elif 52 < m < 59:
            return "la una menys %s" % n2txt(60 - m)
        elif m == 59:
            return "la una menys un minut"
    else:
        if m == 0:
            return "les %s en punt" % hores[h - 1]
        elif m == 1:
            return "les %s i un minut" % hores[h - 1]
        elif 0 < m < 8:
            return "les %s i %s" % (hores[h - 1], n2txt(m))
        elif 7 < m < 15:
            return "un quart menys %s de %s" % (n2txt(15 - m), hores[h - 1])
        elif m == 15:
            return "un quart de %s" % hores[h - 1]
        elif 15 < m < 23:
            return "un quart i %s de %s" % (n2txt(m - 15), hores[h - 1])
        elif 22 < m < 30:
            return "dos quarts menys %s de %s" % (n2txt(30 - m), hores[h - 1])
        elif m == 30:
            return "dos quarts de %s" % hores[h - 1]
        elif 30 < m < 38:
            return "dos quarts i %s de %s" % (n2txt(m - 30), hores[h - 1])
        elif 37 < m < 45:
            return "tres quarts menys %s de %s" % (n2txt(45 - m), hores[h - 1])
        elif m == 45:
            return "tres quarts de %s" % hores[h - 1]
        elif 45 < m < 53:
            return "tres quarts i %s de %s" % (n2txt(m - 45), hores[h - 1])
        elif 52 < m < 59:
            return "les %s menys %s" % (hores[h - 1], n2txt(60 - m))
        elif m == 59:
            return "les %s menys un minut" % hores[h - 1]

#write a fraction in words
numerators = ['un', 'dos', 'tres', 'quatre', 'cinc', 'sis', 'set', 'vuit', 'nou', 'deu', 'onze', 'dotze']

# Singular forms for 1/x
d_singular = [
    '',         # dummy 0
    'mig',      # 1/2
    'terç',     # 1/3
    'quart',    # 1/4
    'cinquè',   # 1/5
    'sisè',     # 1/6
    'setè',     # 1/7
    'vuitè',    # 1/8
    'novè',     # 1/9
    'desè',     # 1/10
    'onzè',     # 1/11
    'dotzè'     # 1/12
]

# Plural forms for 2+/x
d_plural = [
    '',           # dummy 0
    'migs',       # 2/2
    'terços',     # 2/3
    'quarts',     # 2/4
    'cinquens',   # 2/5
    'sisens',     # 2/6
    'setens',     # 2/7
    'vuitens',    # 2/8
    'novens',     # 2/9
    'desens',     # 2/10
    'onzens',     # 2/11
    'dotzens'     # 2/12
]


def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d - 1]
    else:
        return numerators[n - 1] + " " + d_plural[d - 1]
