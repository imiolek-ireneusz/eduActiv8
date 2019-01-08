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

numbers = ['један', 'два', 'три', 'четири', 'пет', 'шест', 'седам', 'осам', 'девет', 'десет', 'једанаест', 'дванаест',
           'тринаест', 'четрнаест', 'петнаест', 'шеснаест', 'седамнаест', 'осамнаест', 'деветнаест', 'двадесет',
           'двадесет један', 'двадесет два', 'двадесет три', 'двадесет четири', 'двадесет пет', 'двадесет шест',
           'двадесет седам', 'двадесет осам', 'двадесет девет']
numbers2090 = ['двадесет', 'тридесет', 'четрдесет', 'педесет', 'шездесет', 'седамдесет', 'осамдесет', 'деведесет']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Аутобус', 'Банана', 'Виолина', 'Гитара', 'Делфин', 'Ђак', 'Ексер', 'Жирафа',
                                      'Зебра', 'Игло', 'Јелка', 'Коала', 'Лав', 'Љуљашка', 'Мед', 'Ноћ', 'Њушка',
                                      'Оклагија', 'Патике', 'Риба', 'Сир', 'Телефон', 'Ћуран', 'Улица', 'Фотограф',
                                      'Хлеб', 'Цуцла', 'Чамац', 'Џак', 'Шпорет']
d['abc_flashcards_word_sequence'] = ['<1>А<2>утобус', '<1>Б<2>анана', '<1>В<2>иолина', '<1>Г<2>итара', '<1>Д<2>елфин',
                                     '<1>Ђ<2>ак', '<1>Е<2>ксер', '<1>Ж<2>ирафа', '<1>З<2>ебра', '<1>И<2>гло',
                                     '<1>Ј<2>елка', '<1>К<2>оала', '<1>Л<2>ав', '<1>Љ<2>у<1>љ<2>ашка', '<1>М<2>ед',
                                     '<1>Н<2>оћ', '<1>Њ<2>ушка', '<1>О<2>клагија', '<1>П<2>атике', '<1>Р<2>иба',
                                     '<1>С<2>ир', '<1>Т<2>елефон', '<1>Ћ<2>уран', '<1>У<2>лица', '<1>Ф<2>отогра<1>ф',
                                     '<1>Х<2>леб', '<1>Ц<2>у<1>ц<2>ла', '<1>Ч<2>амац', '<1>Џ<2>ак', '<1>Ш<2>порет']
# d['abc_flashcards_frame_sequence'] = [42, 27, 2, 59, 4, 34, 28, 29, 8, 9, 72, 11, 40, 13, 52, 15, 16, 17, 53, 33, 20, 21, 26, 23, 24, 25]
#                                     77, 71, 21, 28, 59, Ђђ, Ее, 30, 25, 8, 31, 72, 11, Љљ, 9, 54, Њњ, 80, 60, 5, 57, 79, Ћћ, 53, 39, 35, Цц, 1, Џџ, 67
d['abc_flashcards_frame_sequence'] = [77, 71, 21, 28, 59, 94, 92, 30, 25, 8, 31, 72, 11, 89, 9, 54, 88, 80, 60, 5, 57,
                                      79, 90, 53, 39, 35, 93, 1, 91, 67]
# alphabet sr
alphabet_lc = ['а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ', 'о', 'п', 'р', 'с',
               'т', 'ћ', 'у', 'ф', 'х', 'ц', 'ч', 'џ', 'ш']
alphabet_uc = ['А', 'Б', 'В', 'Г', 'Д', 'Ђ', 'Е', 'Ж', 'З', 'И', 'Ј', 'К', 'Л', 'Љ', 'М', 'Н', 'Њ', 'О', 'П', 'Р', 'С',
               'Т', 'Ћ', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Џ', 'Ш']

# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-']
accents_uc = []


def n2txt(n, twoliner=False):
    """takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."""
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
        return "нула"
    elif n == 100:
        return "сто"
    return ""

ha = ["сат", "сата", "сата", "сата", "сати", "сати", "сати", "сати", "сати", "сати", "сати", "сати"]
ma = ["минут", "минута"]


def time2str_short(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55"""
    if m > 29:
        if h == 12:
            h = 1
        else:
            h += 1

    if m == 0:
        return "%s %s" % (n2txt(h), ha[h - 1])
    elif m == 1:
        return "%s и минут" % n2txt(h)
    elif m == 30:
        return "пола %s" % n2txt(h)
    elif m == 59:
        return "минут до %s" % n2txt(h)
    elif m < 30:
        return "%s и %s" % (n2txt(h), n2txt(m))
    elif m > 30:
        return "%s до %s" % (n2txt(60 - m), n2txt(h))
    return ""

def time2str(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55"""
    if m > 29:
        if h == 12:
            h = 1
        else:
            h += 1

        if (60 - m) % 10 == 1:
            mx = ma[0]
        else:
            mx = ma[1]
    else:
        if m % 10 == 1:
            mx = ma[0]
        else:
            mx = ma[1]

    if m == 0:
        return "%s %s" % (n2txt(h), ha[h - 1])
    elif m == 1:
        return "%s %s и минут" % (ha[h - 1], n2txt(h))
    elif m == 30:
        return "пола %s" % n2txt(h)
    elif m == 59:
        return "минут до %s %s" % (n2txt(h), ha[h - 1])
    elif m < 30:
        return "%s %s и %s %s" % (n2txt(h), ha[h - 1], n2txt(m), mx)
    elif m > 30:
        return "%s %s до %s %s" % (n2txt(60 - m), mx, n2txt(h), ha[h - 1])
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
