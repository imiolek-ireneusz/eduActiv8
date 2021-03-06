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

numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
           'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty one',
           'twenty two', 'twenty three', 'twenty four', 'twenty five', 'twenty six', 'twenty seven', 'twenty eight',
           'twenty nine']
numbers2090 = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Apple', 'Butterfly', 'Cat', 'Dolphin', 'Elephant', 'Fortepiano', 'Guitar',
                                      'Hedgehog', 'Igloo', 'Jar', 'Koala', 'Lion', 'Monitor', 'Notebook', 'Ocean',
                                      'Parrot', 'Queen', 'Rabbit', 'Street', 'Tomato', 'Umbrella', 'Violin',
                                      'Watermelon', 'Xylophone', 'Yarn', 'Zebra']
d['abc_flashcards_word_sequence'] = ['<1>A<2>pple', '<1>B<2>utterfly', '<1>C<2>at', '<1>D<2>olphin',
                                     '<1>E<2>l<1>e<2>phant', '<1>F<2>ortepiano', '<1>G<2>uitar', '<1>H<2>edge<1>h<2>og',
                                     '<1>I<2>gloo', '<1>J<2>ar', '<1>K<2>oala', '<1>L<2>ion', '<1>M<2>onitor',
                                     '<1>N<2>otebook', '<1>O<2>cean', '<1>P<2>arrot', '<1>Q<2>ueen', '<1>R<2>abbit',
                                     '<1>S<2>treet', '<1>T<2>oma<1>t<2>o', '<1>U<2>mbrella', '<1>V<2>iolin',
                                     '<1>W<2>atermelon', '<1>X<2>ylophone', '<1>Y<2>arn', '<1>Z<2>ebra']
d['abc_flashcards_frame_sequence'] = [42, 27, 2, 59, 4, 34, 28, 29, 8, 9, 72, 11, 40, 13, 52, 15, 16, 17, 53, 33, 20,
                                      21, 26, 23, 24, 25]

# alphabet en
alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-']
accents_uc = []

def n2txt(n, twoliner=False):
    "takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."
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
        return "zero"
    elif n == 100:
        return "one hundred"
    return ""

def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s o'clock" % n2txt(h)
    elif m == 1:
        return "one minute past %s" % n2txt(h)
    elif m == 15:
        return "quarter past %s" % n2txt(h)
    elif m == 30:
        return "half past %s" % n2txt(h)
    elif m == 45:
        return "quarter to %s" % n2txt(h)
    elif m == 59:
        return "one minute to %s" % n2txt(h)
    elif m < 30:
        return "%s past %s" % (n2txt(m), n2txt(h))
    elif m > 30:
        return "%s to %s" % (n2txt(60 - m), n2txt(h))
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
