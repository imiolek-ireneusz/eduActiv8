# -*- coding: utf-8 -*-

# traduzido para português da europa por Américo Monteiro (a_monteiro@gmx.com)

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The colour names in other languages than English are already in smaller font.

# word list adapted from GCompris:
# https://github.com/gcompris/GCompris-qt/blob/master/src/activities/lang/resource/content-pt_BR.json

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

numbers = ['um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 'treze',
           'quatorze', 'quinze', 'dezasseis', 'dezassete', 'dezoito', 'dezanove', 'vinte', 'vinte e um', 'vinte e dois',
           'vinte e três', 'vinte e quatro', 'vinte e cinco', 'vinte e seis', 'vinte e sete', 'vinte e oito',
           'vinte e nove']
numbers2090 = ['vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']

dp['abc_flashcards_word_sequence'] = ['Abeto', 'Barco', 'Casa', 'Dormir', 'Elefante', 'Formiga', 'Girafa', 'Hipopótamo',
                                      'Iglu', 'Janela', 'Koala', 'Leão', 'Maçã', 'Narciso-amarelo', 'Ouriço', 'Peixe',
                                      'Queijo', 'Rainha', 'Sol', 'Tomate', 'Uvas', 'Violino', 'Windsurf', 'Xilofone',
                                      'Y', 'Zebra']
d['abc_flashcards_word_sequence'] = ['<1>A<2>beto', '<1>B<2>arco', '<1>C<2>asa', '<1>D<2>ormir',
                                     '<1>E<2>l<1>e<2>fant<1>e', '<1>F<2>ormiga', '<1>G<2>irafa', '<1>H<2>ipopótamo',
                                     '<1>I<2>glu', '<1>J<2>anela', '<1>K<2>oala', '<1>L<2>eão', '<1>M<2>açã',
                                     '<1>N<2>arciso-amarelo', '<1>O<2>uriç<1>o', '<1>P<2>eixe', '<1>Q<2>ueijo',
                                     '<1>R<2>ainha', '<1>S<2>ol', '<1>T<2>oma<1>t<2>e', '<1>U<2>vas', '<1>V<2>iolino',
                                     '<1>W<2>indsurf', '<1>X<2>ilofone', '<1>Y<2> ', '<1>Z<2>ebra']
d['abc_flashcards_frame_sequence'] = [31, 1, 7, 49, 4, 0, 30, 47, 8, 22, 72, 11, 42, 69, 29, 5, 57, 16, 18, 33, 6, 21,
                                      66, 23, 43, 25]

# alphabet - pt - "abcdefghijlmnopqrstuvxz"
alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['á', 'â', 'ã', 'à', 'ç', 'é', 'ê', 'í', 'ó', 'ô', 'õ', 'ú', '-']
accents_uc = ['Á', 'Â', 'Ã', 'À', 'Ç', 'É', 'Ê', 'Í', 'Ó', 'Ô', 'Õ', 'Ú']


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
                return [tens + " e ", ones]
            else:
                return tens + " e " + ones

    elif n == 0:
        return "zero"
    elif n == 100:
        return "cem"
    return ""


horas = ['uma hora', 'duas horas', 'três horas', 'quatro horas', 'cinco horas', 'seis horas', 'sete horas',
         'oito horas', 'nove horas', 'dez horas', 'onze horas', 'doze horas']


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s em ponto" % horas[h - 1]
    elif m == 1:
        return "%s e um minuto" % horas[h - 1]
    elif m == 15:
        return "%s e um quarto" % horas[h - 1]
    elif m == 30:
        return "%s e meia" % horas[h - 1]
    elif m == 45:
        return "um quarto para %s" % horas[h - 1]
    elif m == 59:
        return "um minuto para %s" % horas[h - 1]
    elif m < 30:
        return "%s e %s minutos" % (horas[h - 1], n2txt(m))
    elif m > 30:
        return "%s minutos para %s" % (n2txt(60 - m), horas[h - 1])
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
