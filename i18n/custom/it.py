# -*- coding: utf-8 -*-

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The colour names in other languages than English are already in smaller font.

# word list partially adapted from GCompris and completed by Giuliano.
# https://github.com/gcompris/GCompris-qt/blob/master/src/activities/lang/resource/content-it.json

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

numbers = ['uno', 'due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto', 'nove', 'dieci', 'undici', 'dodici',
           'tredici', 'quattordici', 'quindici', 'sedici', 'diciassette', 'diciotto', 'diciannove', 'venti', 'ventuno',
           'ventidue', 'ventitré', 'ventiquattro', 'venticinque', 'ventisei', 'ventisette', 'ventotto', 'ventinove']
numbers2090 = ['venti', 'trenta', 'quaranta', 'cinquanta', 'sessanta', 'settanta', 'ottanta', 'novanta']

dp['abc_flashcards_word_sequence'] = ['Anguria', 'Barca', 'Casa', 'Dormire', 'Elefante', 'Fiori', 'Giraffa', 'Hockey',
                                      'Iglù', 'Koala', 'Leone', 'Mela', 'Narciso', 'Ombrello', 'Pomodoro', 'Quaderno',
                                      'Riccio', 'Sole', 'Teiera', 'Uva', 'Violino', 'Xilofono', 'Yoga', 'Zebra']
d['abc_flashcards_word_sequence'] = ['<1>A<2>nguri<1>a', '<1>B<2>arca', '<1>C<2>asa', '<1>D<2>ormire',
                                     '<1>E<2>l<1>e<2>fant<1>e', '<1>F<2>iori', '<1>G<2>iraffa', '<1>H<2>ockey',
                                     '<1>I<2>glù', '<1>K<2>oala', '<1>L<2>eone', '<1>M<2>ela', '<1>N<2>arciso',
                                     '<1>O<2>mbrell<1>o', '<1>P<2>omodoro', '<1>Q<2>uaderno', '<1>R<2>iccio',
                                     '<1>S<2>ole', '<1>T<2>eiera', '<1>U<2>va', '<1>V<2>iolino', '<1>X<2>ilofono',
                                     '<1>Y<2>oga', '<1>Z<2>ebra']
d['abc_flashcards_frame_sequence'] = [26, 1, 7, 49, 4, 36, 30, 68, 8, 72, 11, 42, 69, 20, 33, 13, 29, 18, 19, 6, 21, 23,
                                      32, 25]

# used in telling time activity
# the number lists below are for languages with a bit more complex forms, ie. different suffixes depending on context - if your language is like that check Polish translation to see how to use them

# alphabet - it
alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['à', 'è', 'é', 'ì', 'í', 'î', 'ò', 'ó', 'ù', 'ú', '-']
accents_uc = ['À', 'È', 'É', 'Ì', 'Í', 'Î', 'Ò', 'Ó', 'Ù', 'Ú']


def n2txt(n, twoliner=False):
    "takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."
    if 0 < n < 30:
        return numbers[n - 1]
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090[(n // 10) - 2]
        if m > 0:
            ones = numbers[m - 1]
        else:
            ones = ""
        if m in [1, 8]:
            return tens[0:-1] + ones
        elif m == 3:
            return tens + "tré"
        else:
            if twoliner:
                return [tens + "-", ones]
            else:
                return tens + ones
    elif n == 0:
        return "zero"
    elif n == 100:
        return "cento"
    return ""


hrs = ["l'una", 'le due', 'le tre', 'le quattro', 'le cinque', 'le sei', 'le sette', 'le otto', 'le nove', 'le dieci',
       'le undici', 'le dodici']


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m == 0:
        return "%s in punto" % hrs[h - 1]
    elif m == 1:
        return "%s e un minuto" % hrs[h - 1]
    else:
        return "%s e %s" % (hrs[h - 1], n2txt(m))

# scrivi una frazione in parole
numerators = ['un', 'due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto', 'nove', 'dieci', 'undici', 'dodici']

# denominatori singolari, eg. 1/3 - un terzo, 1/8 - un ottavo
d_singular = ['', 'mezzo', 'terzo', 'quarto', 'quinto', 'sesto', 'settimo', 'ottavo', 'nono', 'decimo', 'undicesimo', 'dodicesimo']

# denominatori plurali, eg. 2/5 - due quinti, 5/9 - cinque noni
d_plural = ['', 'mezzi', 'terzi', 'quarti', 'quinti', 'sesti', 'settimi', 'ottavi', 'noni', 'decimi', 'undicesimi', 'dodicesimi']

def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d-1]
    else:
        return numerators[n-1] + " " + d_plural[d-1]
