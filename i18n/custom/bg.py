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

numbers = ['едно', 'две', 'три', 'четири', 'пет', 'шест', 'седем', 'осем', 'девет', 'десет', 'единадесет', 'дванадесет',
           'тринадесет', 'четиринадесет', 'петнадесет', 'шестнадесет', 'седемнадесет', 'осемнадесет', 'деветнадесет', 'двадесет', 'двадесет и едно',
           'двадесет и две', 'двадесет и три', 'двадесет и четири', 'двадесет и пит', 'двадесет и шест', 'двадесет и седем', 'двадесет и осем',
           'двадесет и девет']
numbers2090 = ['двадесет', 'тридесет', 'четиридесет', 'петдесет', 'шестдесет', 'седемдесет', 'осемдесет', 'деветдесет']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Автобус', 'Бухал', 'Влак', 'Грозде', 'Дърво', 'Екран', 'Жираф',
                                      'Зебра', 'Иглу', 'Йога', 'Котка', 'Лодка', 'Мравка', 'Нарцис', 'Око',
                                      'Патица', 'Риба', 'Слон', 'Тигър', 'Улица', 'Фотограф', 'Хляб', 'Цветя',
                                      'Чайник', 'Шимпанзе', 'Щука', 'Ъгъл', 'Боксьор', 'Ютия', 'Ябълка']
d['abc_flashcards_word_sequence'] = ['<1>А<2>втобус', '<1>Б<2>ухал', '<1>В<2>лак', '<1>Г<2>розде', '<1>Д<2>ърво', '<1>Е<2>кран', '<1>Ж<2>ираф',
                                     '<1>З<2>ебра', '<1>И<2>глу', '<1>Й<2>ога', '<1>К<2>от<1>к<2>а', '<1>Л<2>одка', '<1>М<2>равка', '<1>Н<2>арцис', '<1>О<2>к<1>о',
                                     '<1>П<2>атица', '<1>Р<2>иба', '<1>С<2>лон', '<1>Т<2>игър', '<1>У<2>лица', '<1>Ф<2>отогра<1>ф', '<1>Х<2>ляб', '<1>Ц<2>ветя',
                                     '<1>Ч<2>айник', '<1>Ш<2>импанзе', '<1>Щ<2>ука', '<1>Ъ<2>г<1>ъ<2>л', '<2>Бокс<1>ь<2>ор', '<1>Ю<2>тия', '<1>Я<2>бълка']
d['abc_flashcards_frame_sequence'] = [77, 14, 63, 6, 46, 40, 30, 25, 8, 32, 2, 1, 0, 69, 75, 3, 5, 4, 65, 53, 39,
                                      35, 36, 19, 37, 38, 104, 103, 102, 42]

# alphabet en
alphabet_lc = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
               'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я']
alphabet_uc = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
               'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ь', 'Ю', 'Я']
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
                return tens + " и " + ones

    elif n == 0:
        return "нула"
    elif n == 100:
        return "сто"
    return ""


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s часа" % n2txt(h)
    elif m == 1:
        return "%sчаса и една минута" % n2txt(h)
    elif m == 15:
        return "%s и четвърт" % n2txt(h)
    elif m == 30:
        return "%s и половина" % n2txt(h)
    elif m == 45:
        return "%s без четвърт" % n2txt(h)
    elif m == 59:
        return "%s часа без една минута" % n2txt(h)
    elif m < 30:
        return "%s часа и %s минути" % (n2txt(h), n2txt(m))
    elif m > 30:
        return "%s часа без %s минути" % (n2txt(h), n2txt(60 - m))
    return ""

#write a fraction in words
numerators = ['едно', 'две', 'три', 'четири', 'пет', 'шест', 'седем', 'осем', 'девет', 'десет', 'единадесет', 'дванадесет']
d_singular = ['', 'половина', 'трета', 'четвърт', 'пета', 'шеста', 'седма', 'осма', 'девета', 'десета', 'единадесета', 'дванадесета']
d_plural = ['', 'втори', 'трети', 'четвърти', 'пети', 'шести', 'седми', 'осми', 'девети', 'десети', 'единадесети', 'дванадесети']

def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d-1]
    else:
        return numerators[n-1] + " " + d_plural[d-1]
