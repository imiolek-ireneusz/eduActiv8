# -*- coding: utf-8 -*-

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The colour names in other languages than English are already in smaller font.

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

# how to spell french numbers: http://www.logilangue.com/public/Site/clicGrammaire/Nombres.php
# 'une' is only for hours/minutes -gender female- otherwise, it's 'un' -gender male-.
numbers = ['un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
           'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf', 'vingt', 'vingt-et-un', 'vingt-deux',
           'vingt-trois', 'vingt-quatre', 'vingt-cinq', 'vingt-six', 'vingt-sept', 'vingt-huit', 'vingt-neuf']

hrs = ['une', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
       'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf', 'vingt', 'vingt-et-une', 'vingt-deux',
       'vingt-trois', 'vingt-quatre', 'vingt-cinq', 'vingt-six', 'vingt-sept', 'vingt-huit', 'vingt-neuf']

numbers2090 = ['vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante-dix', 'quatre-vingt',
               'quatre-vingt-dix']

dp['abc_flashcards_word_sequence'] = ['Arbre', 'Bateau', 'Canard', 'Dormir', 'Éléphant', 'Fleurs', 'Girafe', 'Hibou',
                                      'Iglou', 'Jonquille', 'Koala', 'Lion', 'Maison', 'Nuitée', 'Océan', 'Pomme',
                                      'Quille', 'Raisin', 'Soleil', 'Tomate', 'Univers', 'Violon', 'Wagon', 'Xylophone',
                                      'Yoga', 'Zèbre']
d['abc_flashcards_word_sequence'] = ['<1>A<2>rbre', '<1>B<2>ateau', '<1>C<2>anard', '<1>D<2>ormir',
                                     '<1>É<2>l<1>é<2>phant', '<1>F<2>leurs', '<1>G<2>irafe', '<1>H<2>ibou',
                                     '<1>I<2>glou', '<1>J<2>onquille', '<1>K<2>oala', '<1>L<2>ion', '<1>M<2>aison',
                                     '<1>N<2>uitée', '<1>O<2>céan', '<1>P<2>omme', '<1>Q<2>uille', '<1>R<2>aisin',
                                     '<1>S<2>oleil', '<1>T<2>oma<1>t<2>e', '<1>U<2>nivers', '<1>V<2>iolon',
                                     '<1>W<2>agon', '<1>X<2>ylophone', '<1>Y<2>oga', '<1>Z<2>èbre']
d['abc_flashcards_frame_sequence'] = [31, 1, 3, 49, 4, 36, 30, 14, 8, 69, 72, 11, 7, 54, 52, 42, 64, 6, 18, 33, 55, 21,
                                      58, 23, 32, 25]

# alphabet - fr - "abcdefghijklmnopqrstuvwxyz"
alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-', 'à', 'â', 'æ', 'ç', 'é', 'è', 'ê', 'ë', 'î', 'ï', 'ô', 'œ', 'ù', 'û', 'ü', 'ÿ']
accents_uc = ['À', 'Â', 'Æ', 'Ç', 'É', 'È', 'Ê', 'Ë', 'Î', 'Ï', 'Ô', 'Œ', 'Ù', 'Û', 'Ü', 'Ÿ']

def n2txt(n, twoliner=False, time2txt=False):
    """takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."""
    if 0 < n < 30:
        if time2txt:
            return hrs[n - 1]
        else:
            return numbers[n - 1]
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090[(n // 10) - 2]
        if m == 0:
            return tens
        elif m > 0:
            if time2txt:
                ones = hrs[m - 1]
            else:
                ones = numbers[m - 1]

            if twoliner:
                return [tens, ones]
            else:
                return tens + "-" + ones

    elif n == 0:
        return "zero"
    elif n == 100:
        return "cent"
    return ""


def time2str(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55"""
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        if h == 1:
            return "%s heure" % hrs[h - 1]
        else:
            return "%s heures" % hrs[h - 1]
    elif m == 1:
        if h == 1:
            return "%s heure et une minute" % hrs[h - 1]
        else:
            return "%s heures et une minute" % hrs[h - 1]
    elif m == 15:
        if h == 1:
            return "%s heure et quart" % hrs[h - 1]
        else:
            return "%s heures et quart" % hrs[h - 1]
    elif m == 30:
        if h == 1:
            return "%s heure et demie" % hrs[h - 1]
        else:
            return "%s heures et demie" % hrs[h - 1]
    elif m == 45:
        if h == 1:
            return "%s heure moins le quart" % hrs[h - 1]
        else:
            return "%s heures moins le quart" % hrs[h - 1]
    elif m == 59:
        if h == 1:
            return "%s heure moins une minute" % hrs[h - 1]
        else:
            return "%s heures moins une minute" % hrs[h - 1]
    elif m < 30:
        if h == 1:
            return "%s heure et %s minutes" % (hrs[h - 1], n2txt(m, time2txt=True))
        else:
            return "%s heures et %s minutes" % (hrs[h - 1], n2txt(m, time2txt=True))
    elif m > 30:
        if h == 1:
            return "%s heure moins %s minutes" % (hrs[h - 1], n2txt(60 - m, time2txt=True))
        else:
            return "%s heures moins %s minutes" % (hrs[h - 1], n2txt(60 - m, time2txt=True))
    return ""

#write a fraction in words
numerators = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
d_singular = ['', 'half', 'third', 'quarter', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
d_plural = ['', 'halves', 'thirds', 'quarters', 'fifths', 'sixths', 'sevenths', 'eighths', 'ninths', 'tenths', 'elevenths', 'twelfths']

def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d-1]
    else:
        return numerators[n-1] + " " + d_plural[d-1]
