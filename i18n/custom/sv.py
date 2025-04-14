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

numbers = ['ett', 'två', 'tre', 'fyra', 'fem', 'sex', 'sju', 'åtta', 'nio', 'tio', 'elva', 'tolv',
           'tretton', 'fjorton', 'femton', 'sexton', 'sjutton', 'arton', 'nitton', 'tjugo', 'tjugoett',
           'tjugotvå', 'tjugotre', 'tjugofyra', 'tjugofem', 'tjugosex', 'tjugosju', 'tjugoåtta',
           'tjugonio']

numbers2090 = ['tjugo', 'trettio', 'fyrtio', 'femtio', 'sextio', 'sjuttio', 'åttio', 'nittio']


# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Anka', 'Båt', 'Cykel', 'Delfin', 'Elefant', 'Fisk', 'Giraff', 'Hus', 'Igloo',
                                      'Juice', 'Katt', 'Lejon', 'Mus', 'Noshörning', 'Ost', 'Papegoja', 'Quesadilla',
                                      'Räv', 'Sol', 'Tomat', 'Uggla', 'Vattenmelon', 'Wok', 'Xylofon', 'Yoghurt',
                                      'Zebra', 'Åsna', 'Äpple', 'Öga']
d['abc_flashcards_word_sequence'] = ['<1>A<2>pple', '<1>B<2>utterfly', '<1>C<2>at', '<1>D<2>olphin',
                                     '<1>E<2>l<1>e<2>phant', '<1>F<2>ortepiano', '<1>G<2>uitar', '<1>H<2>edge<1>h<2>og',
                                     '<1>I<2>gloo', '<1>J<2>ar', '<1>K<2>oala', '<1>L<2>ion', '<1>M<2>onitor',
                                     '<1>N<2>otebook', '<1>O<2>cean', '<1>P<2>arrot', '<1>Q<2>ueen', '<1>R<2>abbit',
                                     '<1>S<2>treet', '<1>T<2>oma<1>t<2>o', '<1>U<2>mbrella', '<1>V<2>iolin',
                                     '<1>W<2>atermelon', '<1>X<2>ylophone', '<1>Y<2>arn', '<1>Z<2>ebra']
d['abc_flashcards_word_sequence'] = ['<1>A<2>nk<1>a', '<1>B<2>åt', '<1>C<2>ykel', '<1>D<2>elfin', '<1>E<2>l<1>e<2>fant',
                                     '<1>F<2>isk', '<1>G<2>iraff', '<1>H<2>us', '<1>I<2>gloo', '<1>J<2>uice',
                                     '<1>K<2>att', '<1>L<2>ejon', '<1>M<2>us', '<1>N<2>oshör<1>n<2>i<1>n<2>g',
                                     '<1>O<2>st', '<1>P<2>a<1>p<2>egoja', '<1>Q<2>uesadilla', '<1>R<2>äv', '<1>S<2>ol',
                                     '<1>T<2>oma<1>t', '<1>U<2>ggla', '<1>V<2>attenmelon', '<1>W<2>ok', '<1>X<2>ylofon',
                                     '<1>Y<2>oghurt', '<1>Z<2>ebra', '<1>Å<2>sna', '<1>Ä<2>pple', '<1>Ö<2>ga']

d['abc_flashcards_frame_sequence'] = [3, 1, 111, 59, 4, 5, 30, 7, 8, 101, 2, 11, 12, 106, 57, 15, 120, 110, 18, 33, 14,
                                      26, 121, 23, 73, 25, 122, 42, 75]

"""
'Anka' (duck) (3),
'Båt' (boat) (1),
'Cykel' (bicycle) (111), 
'Delfin' (dolphin) (59), 
'Elefant' (elephant) (4),
'Fisk' (fish) (5),
'Giraff' (giraffe) (30),
'Hus' (house) (7),
'Igloo' (igloo) (8), 
'Juice' (juice) (101), 
'Katt' (cat) (2),
'Lejon' (lion) (11), 
'Mus' (mouse) (12), 
'Noshörning' (rhino) (106), 
'Ost' (cheese) (57), 
'Papegoja' (parrot) (15), 
'Quesadilla' (120)
'Räv' (fox) (110), 
'Sol' (sun) (18), 
'Tomat' (tomato) (33), 
'Uggla' (owl) (14), 
'Vattenmelon' (watermelon) (26), 
'Wok'  (121)
'Xylofon' (xylophone) (23), 
'Yoghurt' (yoghurt) (73), 
'Zebra' (zebra) (25),
'Åsna' (donkey) (122)
'Äpple' (apple) (42), 
'Öga' (eye) (75), 
"""

# alphabet en
alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'å', 'ä', 'ö']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z', 'Å', 'Ä', 'Ö']

# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-']
accents_uc = []

def n2txt(n, twoliner=False):
    "takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sextio tre'."
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
                return [tens, ones]
            else:
                return tens + " " + ones

    elif n == 0:
        return "noll"
    elif n == 100:
        return "hundra"
    return ""


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s klockan" % n2txt(h)
    elif m == 1:
        return "en minut över %s" % n2txt(h)
    elif m == 15:
        return "kvart över %s" % n2txt(h)
    elif m == 30:
        return "halv %s" % n2txt(h)
    elif m == 45:
        return "kvart i %s" % n2txt(h)
    elif m == 59:
        return "en minut i %s" % n2txt(h)
    elif m < 30:
        return "%s över %s" % (n2txt(m), n2txt(h))
    elif m > 30:
        return "%s i %s" % (n2txt(60 - m), n2txt(h))
    return ""

# write a fraction in words
numerators = ['ett', 'två', 'tre', 'fyra', 'fem', 'sex', 'sju', 'åtta', 'nio', 'tio', 'elva', 'tolv']
d_singular = ['', 'hälft', 'tredjedel', 'fjärdedel', 'femtedel', 'sjättedel', 'sjundedel', ' åttondel', 'niondel', 'tiondel', 'elftedel', 'tolftedel']
d_plural = ['', 'hälfter', 'tredjedelar', 'fjärdedelar', 'femtedelar', 'sjättedelar', 'sjundedelar', 'åttondelar', 'niondelar', 'tiondelar', 'elftedelar', 'tolftedelar']

def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d-1]
    else:
        return numerators[n-1] + " " + d_plural[d-1]
