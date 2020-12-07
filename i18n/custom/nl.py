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

numbers = ['een', 'twee', 'drie', 'vier', 'vijf', 'zes', 'zeven', 'acht', 'negen', 'tien', 'elf', 'twaalf', 'dertien', 'veertien', 'vijftien', 'zestien', 'zeventien', 'achttien', 'negentien', 'twintig', 'eenentwintig', 'tweeëntwintig', 'drieëntwintig', 'vierentwintig', 'vijfentwintig', 'zesentwintig', 'zevenentwintig', 'achtentwintig', 'negenentwintig']
numbers2090 = ['twintig', 'dertig', 'veertig', 'vijftig', 'zestig', 'zeventig', 'tachtig', 'negentig']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Appel', 'Bus', 'Chimpansee', 'Dolfijn', 'Egel', 'Fiets', 'Gitaar', 'Huis', 'Iglo', 'Jas', 'Kat', 'Leeuw', 'Muis', 'Nijlpaard', 'Olifant', 'Papegaai', 'Quad', 'Rots', 'Slak', 'Tomaat',  'Uil', 'Viool', 'Water', 'Xylofoon', 'Yoghurt', 'Zebra']
d['abc_flashcards_word_sequence'] = ['<1>A<2>ppel', '<1>B<2>us', '<1>C<2>himpansee', '<1>D<2>olfijn', '<1>E<2>g<1>e<2>l', '<1>F<2>iets', '<1>G<2>itaar', '<1>H<2>uis', '<1>I<2>glo', '<1>J<2>as', '<1>K<2>at', '<1>L<2>eeuw', '<1>M<2>uis', '<1>N<2>ijlpaard', '<1>O<2>lifant', '<1>P<2>a<1>p<2>egaai', '<1>Q<2>uad', '<1>R<2>ots', '<1>S<2>lak', '<1>T<2>omaa<1>t', '<1>U<2>il', '<1>V<2>iool', '<1>W<2>ater', '<1>X<2>ylofoon', '<1>Y<2>oghurt', '<1>Z<2>ebra']

d['abc_flashcards_frame_sequence'] = [42, 77, 37, 59, 29, 111, 28, 7, 8, 112, 2, 11, 12, 47, 4, 15, 113, 97, 61, 33, 14, 21, 81, 23, 73, 25]

# alphabet en
alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-', 'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ë', 'ï', 'ö', 'ü', 'ĳ']
accents_uc = ['-', 'Á', 'É', 'Í', 'Ó', 'Ú', 'À', 'È', 'Ë', 'Ï', 'Ö', 'Ü', 'Ĳ']


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
            if 1 < m < 4:
                n_and = "ënt"
            else:
                n_and = "ent"

            if twoliner:
                return [ones + n_and + "-", tens]
            else:
                return ones + n_and + tens
    elif n == 0:
        return "nul"
    elif n == 100:
        return "honderd"
    return ""


def time2str(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55"""
    if m > 15:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s uur" % n2txt(h)
    elif m == 15:
        return "kwart over %s" % n2txt(h)
    elif m == 30:
        return "half %s" % n2txt(h)
    elif m == 45:
        return "kwart voor %s" % n2txt(h)
    elif m < 15:
        return "%s over %s" % (n2txt(m), n2txt(h))
    elif m < 30:
        return "%s voor half %s" % (n2txt(30 - m), n2txt(h))
    elif m < 45:
        return "%s over half %s" % (n2txt(m - 30), n2txt(h))
    elif m < 60:
        return "%s voor %s" % (n2txt(60 - m), n2txt(h))
    return ""

# write a fraction in words - needs translating
numerators = ['een', 'twee', 'drie', 'vier', 'vijf', 'zes', 'zeven', 'acht', 'negen', 'tien', 'elf', 'twaalf',]
denominators = ['', 'tweede', 'derde', 'vierde', 'vijfde', 'zesde', 'zevende', 'achtste', 'negende', 'tiende', 'elfde', 'twaalfde']


def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + denominators[d-1]
    else:
        return numerators[n-1] + " " + denominators[d-1]
