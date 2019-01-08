# -*- coding: utf-8 -*-

# Translated by Kamila Roszak-Imiolek and Ireneusz Imiolek

# Część zdań skrócona, lub zmieniona ze wzgędów estetycznych bądź też braku miejsca na długie zdania.
# jeśli myślisz że coś mogłoby być lepiej - skontaktuj się z nami - zmienimy...

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

numbers = ['jeden', 'dwa', 'trzy', 'cztery', 'pięć', 'sześć', 'siedem', 'osiem', 'dziewięć', 'dziesięć', 'jedenaście',
           'dwanaście', 'trzynaście', 'czternaście', 'piętnaście', 'szesnaście', 'siedemnaście', 'osiemnaście',
           'dziewiętnaście', 'dwadzieścia', 'dwadzieścia jeden', 'dwadzieścia dwa', 'dwadzieścia trzy',
           'dwadzieścia cztery', 'dwadzieścia pięć', 'dwadzieścia sześć', 'dwadzieścia siedem', 'dwadzieścia osiem',
           'dwadzieścia dziewięć']
numbers2090 = ['dwadzieścia', 'trzydzieści', 'czterdzieści', 'pięćdziesiąt', 'sześćdziesiąt', 'siedemdziesiąt',
               'osiemdziesiąt', 'dziewięćdziesiąt']

dp['abc_flashcards_word_sequence'] = ['Arbuz', 'Pociąg', 'Buty', 'Cymbałki', 'Ćma', 'Dom', 'Ekran', 'Ciężarówka',
                                      'Fortepian', 'Gitara', 'Hamak', 'Iglo', 'Jabłko', 'Kwiatki', 'Lew', 'Łódka',
                                      'Mrówka', 'Noc', 'Koń', 'Okno', 'Królik', 'Pomidor', 'Ryba', 'Sowa', 'Ślimak',
                                      'Tygrys', 'Ulica', 'Winogron', 'Mysz', 'Zebra', 'Źrebak', 'Żyrafa']
d['abc_flashcards_word_sequence'] = ['<1>A<2>rbuz', '<2>Poci<1>ą<2>g', '<1>B<2>uty', '<1>C<2>ymbałki', '<1>Ć<2>ma',
                                     '<1>D<2>om', '<1>E<2>kran', '<2>Ci<1>ę<2>żarówka', '<1>F<2>ortepian',
                                     '<1>G<2>itara', '<1>H<2>amak', '<1>I<2>glo', '<1>J<2>abłko', '<1>K<2>wiat<1>k<2>i',
                                     '<1>L<2>ew', '<1>Ł<2>ódka', '<1>M<2>rówka', '<1>N<2>oc', '<2>Ko<1>ń',
                                     '<1>O<2>kn<1>o', '<2>Kr<1>ó<2>lik', '<1>P<2>omidor', '<1>R<2>yba', '<1>S<2>owa',
                                     '<1>Ś<2>limak', '<1>T<2>ygrys', '<1>U<2>lica', '<1>W<2>inogron', '<1>M<2>ysz',
                                     '<1>Z<2>ebra', '<1>Ź<2>rebak', '<1>Ż<2>yrafa']

d['abc_flashcards_frame_sequence'] = [26, 63, 60, 23, 44, 7, 40, 50, 34, 28, 56, 8, 42, 36, 11, 1, 0, 54, 45, 22, 17,
                                      33, 5, 14, 61, 65, 53, 6, 12, 25, 62, 30]

# alphabet - pl
alphabet_lc = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o', 'ó',
               'p', 'r', 's', 'ś', 't', 'u', 'w', 'y', 'z', 'ź', 'ż']
alphabet_uc = ['A', 'Ą', 'B', 'C', 'Ć', 'D', 'E', 'Ę', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Ł', 'M', 'N', 'Ń', 'O', 'Ó',
               'P', 'R', 'S', 'Ś', 'T', 'U', 'W', 'Y', 'Z', 'Ź', 'Ż']
# correction of eSpeak pronounciation of single letters if needed
letter_names = ['a', 'ą', 'be', 'ce', 'će', 'de', 'e', 'ę', 'ef', 'gje', 'ha', 'i', 'jot', 'ka', 'el', 'eł', 'em', 'en',
                'eń', 'o', 'u kreskowane', 'pe', 'er', 'es', 'eś', 'te', 'u', 'wu', 'igrek', 'zet', 'ziet', 'żet']

accents_lc = ['-', 'q', 'v', 'x']
accents_uc = ['Q', 'V', 'X']


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
        return "sto"
    return ""


ha = ["pierwsza", "druga", "trzecia", "czwarta", "piąta", "szósta", "siódma", "ósma", "dziewiąta", "dziesiąta",
      "jedenasta", "dwunasta"]
hb = ["pierwszej", "drugiej", "trzeciej", "czwartej", "piątej", "szóstej", "siódmej", "ósmej", "dziewiątej",
      "dziesiątej", "jedenastej", "dwunastej"]


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 29:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s godzina" % ha[h - 1]
    elif m == 1:
        return "minuta po %s" % hb[h - 1]
    elif m == 2:
        return "dwie po %s" % hb[h - 1]
    elif m == 15:
        return "kwadrans po %s" % hb[h - 1]
    elif m == 22:
        return "dwadzieścia dwie po %s" % hb[h - 1]
    elif m == 30:
        return "wpół do %s" % hb[h - 1]
    elif m == 38:
        return "za dwadzieścia dwie %s" % ha[h - 1]
    elif m == 45:
        return "za kwadrans %s" % ha[h - 1]
    elif m == 58:
        return "za dwie %s" % ha[h - 1]
    elif m == 59:
        return "za minute %s" % ha[h - 1]
    elif m < 30:
        return "%s po %s" % (n2txt(m), hb[h - 1])
    elif m > 30:
        return "za %s %s" % (n2txt(60 - m), ha[h - 1])
    return ""

#write a fraction in words
numerators = ['jedna', 'dwie', 'trzy', 'cztery', 'pięć', 'sześć', 'siedem', 'osiem', 'dziewięć', 'dziesięć', 'jedenaście', 'dwanaście']
d_singular = ['', 'druga', 'trzecia', 'czwarta', 'piąta', 'szósta', 'siódma', 'ósma', 'dziewiąta', 'dziesiąta', 'jedenasta', 'dwunasta']
d_plural234 = ['', 'drugie', 'trzecie', 'czwarte', 'piąte', 'szóste', 'siódme', 'ósme', 'dziewiąte', 'dziesiąte', 'jedenaste', 'dwunaste']
d_plural567 = ['', 'drugich', 'trzecich', 'czwartych', 'piątych', 'szóstych', 'siódmych', 'ósmych', 'dziewiątych', 'dziesiątych', 'jedenastych', 'dwunastych']

def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d-1]
    elif n in [2, 3, 4]:
        return numerators[n-1] + " " + d_plural234[d-1]
    else:
        return numerators[n-1] + " " + d_plural567[d-1]
