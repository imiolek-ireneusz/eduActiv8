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

numbers = ['waŋží', 'núŋpa', 'yámni', 'tópa', 'záptaŋ', 'šákpe', 'šakówiŋ', 'šaglóǧaŋ', 'napčíyuŋka', 'wikčémna', 'akéwaŋzi', 'akénuŋpa',
           'akéyamni', 'akétopa', 'akézaptaŋ', 'akéšakpe', 'akéšakowiŋ', 'akéšagloǧaŋ', 'akénapčiyuŋka', 'wikčémna núŋpa', 'wikčémna núŋpa sám waŋží',
           'wikčémna núŋpa sám núŋpa', 'wikčémna núŋpa sám yámni', 'wikčémna núŋpa sám tópa', 'wikčémna núŋpa sám záptaŋ', 'wikčémna núŋpa sám šákpe', 'wikčémna núŋpa sám šakówiŋ', 'wikčémna núŋpa sám šagloǧaŋ',
           'wikčémna núŋpa sám napčíyuŋka']
numbers2090 = ['wikčémna núŋpa', 'wikčémna yámni', 'wikčémna tópa', 'wikčémna záptaŋ', 'wikčémna šákpe', 'wikčémna šakówiŋ', 'wikčémna šaglóǧaŋ', 'wikčémna napčíyuŋka']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Aǧúyapi', 'Aŋpáwi', 'Blé', 'Čísčila', 'Épazo', 'Gmigméla', 'Ǧí', 'Háŋpa', 'Ȟé',
									  'Igmú', 'Íŋyaŋ', 'Kimímela', 'Ločhíŋ', 'Maštíŋčala', 'Nitéhepi', 'Omás’apȟe', 'Pté', 'Skiská',
									  'Šúŋkawakȟaŋ', 'Tópa', 'Úta', 'Uŋžíŋžiŋtka', 'Wówapi', 'Yámni', 'Zíškopela', 'Žaŋžáŋ']
d['abc_flashcards_word_sequence'] = ['<1>A<2>ǧúy<1>a<2>pi', '<1>Aŋ<2>páwi', '<1>B<2>lé', '<1>Č<2>ís<1>č<2>ila',
                                     '<1>É<2>pazo', '<1>G<2>mi<1>g<2>méla', '<1>Ǧ<2>í', '<1>H<2>áŋpa', '<1>Ȟ<2>é', '<1>I<2>gmú',
                                     '<1>Íŋ<2>yaŋ', '<1>K<2>imímela', '<1>L<2>očhíŋ','<1>M<2>aštíŋčala','<1>N<2>itéhepi',
                                     '<1>O<2>más’apȟe', '<1>P<2>té', '<1>S<2>ki<1>s<2>ká', '<1>Š<2>úŋkawakȟaŋ', '<1>T<2>ópa',
                                     '<1>Ú<2>ta', '<1>Uŋ<2>žíŋžiŋtka', '<1>W<2>ó<1>w<2>wapi', '<1>Y<2>ámni', '<1>Z<2>íškopela', '<1>Ž<2>aŋ<1>Ž<2>áŋ']
d['abc_flashcards_frame_sequence'] = [35, 18, 82, 12, 94, 24, 95, 60, 96, 2, 97, 27, 88, 17, 41, 79, 70, 3, 45, 98, 99,
                                      33, 13, 100, 71, 101]

# alphabet en
alphabet_lc = ['a', 'aŋ', 'b', 'č', 'e', 'g', 'ǧ', 'h', 'ȟ', 'i', 'iŋ', 'k', 'l', 'm', 'n', 'o', 'p', 's', 'š', 't', 'u',
               'uŋ', 'w', 'y', 'z', 'ž']
alphabet_uc = ['A', 'Aŋ', 'B', 'Č', 'E', 'G', 'Ǧ', 'H', 'Ȟ', 'I', 'Iŋ', 'K', 'L', 'M', 'N', 'O', 'P', 'S', 'Š', 'T', 'U',
               'Uŋ', 'W', 'Y', 'Z', 'Ž']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-', 'á', 'é', 'í', 'ó', 'ú']
accents_uc = ['Á']


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
        return "tákuni"
    elif n == 100:
        return "opáwiŋǧe"
    return ""


"""
time - mázaškaŋškaŋ
hour - oápȟe
minute - oápȟe čík’ala
second - okpí
o’clock - mázaškaŋškaŋ # (e.g. mázaškaŋškaŋ waŋží = 1:00)
quarter past - mázaškaŋškaŋ # sáŋm šókela (e.g. mázaškaŋškaŋ waŋží sáŋm šókela = 1:15)
half past - mázaškaŋškaŋ # sáŋm okhíse (e.g. mázaškaŋškaŋ waŋží sáŋm okhíse = 1:30)
3 quarters past - mázaškaŋškaŋ # sáŋm šókela yámni (e.g. mázaškaŋškaŋ waŋží sáŋm šókela yámni = 1:45)
X minutes past #:00 - mázaškaŋškaŋ # sáŋm oápȟe čík’ala X (e.g. mázaškaŋškaŋ waŋží sáŋm oápȟe čík’ala tópa = 1:04)
X minutes before #:00 - mázaškaŋškaŋ # itȟókab oápȟe čík’ala X (e.g. mázaškaŋškaŋ waŋží itȟókab oápȟe čík’ala tópa = 12:56)
"""

def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30 and not m == 45:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "mázaškaŋškaŋ %s" % n2txt(h)
    elif m == 15:
        return "mázaškaŋškaŋ %s sáŋm šókela" % n2txt(h)
    elif m == 30:
        return "mázaškaŋškaŋ %s sáŋm okhíse" % n2txt(h)
    elif m == 45:
        return "mázaškaŋškaŋ %s sáŋm šókela yámni" % n2txt(h)
    elif m < 30:
        return "mázaškaŋškaŋ %s sáŋm oápȟe čík’ala %s" % (n2txt(h), n2txt(m))
    elif m > 30:
        return "mázaškaŋškaŋ %s itȟókab oápȟe čík’ala %s" % (n2txt(h), n2txt(60 - m))
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

d["a4a_animals"] = ["ptegléška", "waglékšuŋ", "hokáš’iŋla", "šuŋgmánitu tȟáŋka", "igmútȟaŋka sápa", "matȟówičhá", "halháta", "thukí", "šuŋkčík’ala", "itȟúŋkala", "šuŋkíteblaska",
                    "matȟó itókaǧa", "gnašká", "wíŋyaŋ wablúška", "makhúakipȟela", "lamá", "hečá", "itȟúŋkčhepa", "ziŋtkála", "wičháȟpi hoǧáŋ", "kȟaŋǧí",
                    "ziŋtkála waúŋčhala", "waglúla", "igmúgleǧa", "tȟanáǧila", "hoǧáŋ wóhitika", "khukhúše", "siŋtíčhapȟe", "šuŋǧíla", "igmúgleška",
                    "agléškapȟéyohaŋ", "hoškéhaŋ", "ȟupákiglake", "uŋžíŋčala", "mniwáŋča matúgna", "kȟokȟóyaȟ’aŋla bloká", "wičháyažipa", "iglútȟokčala", "mniwátu", "wapȟáhiŋka",
                    "thíŋgleška", "héblaska", "wičháyažipa tȟáŋka", "peháŋhaŋla", "čhetáŋ watȟápȟela", "šúŋšuŋla", "itȟúŋggleška", "waȟ’áŋhikela", "šúŋkawakȟaŋ", "čháǧa ziŋtkála",
                    "ptáŋ", "matȟó", "šuŋglézela", "waȟúpakoza tȟáŋka", "čhuwínuŋǧa", "niǧésaŋla", "siŋté glegléǧa", "thiwákiŋyela", "lamá", "wahíŋheya", "mniókiŋyela",
                    "hečhíŋškayapi", "maká", "hoštáka", "tȟáȟčašuŋkala", "hoápepȟestola", "igmúla", "tȟáȟča", "waháčhaŋka kič’íŋ", "pȟeháŋ šásaŋ", "maštíŋčala",
                    "thukíhasaŋ", "čhápa", "ziŋtkísčila", "wakíŋyela", "waŋblí", "wablúška", "mnikhúkhuše", "hiŋháŋ", "zuzéča pȟabláska",
                    "asápazila", "maǧá", "tȟáȟčapsiča", "thuswéčha", "matȟápeȟ’a", "blóza", "istó šaglóǧaŋ", "igmú tȟáŋka čhiŋčála", "igmú itókaǧa",
                    "maǧáksiča", "agléška", "phuté hetȟúŋ", "šúŋka iȟáȟa", "ptewák'iŋ", "ziŋtkála siŋtúpi háŋska", "ziŋtkála waúŋčha", "heȟáka", "agléška tȟáŋka", "tȟažúška",
                    "tȟatȟókala", "maštíŋčala čhiŋčála", "igmú tȟáŋka", "zičá", "siŋtéšla", "iȟála", "tȟáȟča wíŋyela", "ithígnila", "phuté wókič’u",
                    "tȟahú háŋska", "iktómi", "šuŋȟpála", "ziŋtkátȟoglegleǧa", "mniwáŋča šúŋka", "kȟokȟóyaȟ’aŋla wíŋyela", "khéya", "tȟablóka", "igmú", "itȟúŋktȟaŋka",
                    "zugzúkela", "tȟatȟáŋka", "wábloša", "maǧáska", "matúgna tȟáŋka", "šúŋka", "čhapȟúŋka", "zuzéča", "kȟokȟóyaȟ’aŋla",
                    "tȟažúška yúta"]
d["a4a_sport"] = ["ksabyá kichízapi", "nuŋwÁŋ", "hunáhomni akáŋyaŋkA", "iglúzičA", "wapȟóštaŋ sutá", "čhaȟ’íčazo", "máni", "íkačhaŋ", "napȟÁ", "oyúso úŋ", "psípsičA",
                  "imáǧaǧaya máni", "napé uŋ kičhízapi", "čháǧa tȟabkápsičapi", "khiíŋyaŋkapi", "kaȟ’ól iyéyA", "čhaŋbláska kič’úŋ", "ohíyA", "pustág nážiŋ", "waákaŋ čhaŋwóslohaŋ kič’úŋ", "tȟab’ákozA", "wayázopi",
                  "pȟetížaŋžaŋye", "tȟatéwata", "hóšnašna kič’úŋ", "tȟabhíŋšma škátapi", "waŋkáyeič’iyA", "watópȟA", "íŋyaŋkA", "wíkȟaŋ uŋ psípsičA"]
d["a4a_body"] = ["hí", "tȟapȟúŋ", "iškáhu", "čhaŋkpé", "sipȟá", "kȟaŋíyuwi", "í", "sí", "napé", "išpá", "pȟehíŋ",
                 "úŋštiŋmapihíŋ", "phuthíŋhiŋ", "čhekpá", "napȟáhuŋka", "makhú", "pȟóǧe", "pȟasú", "niséhu", "istó", "ištáȟehiŋ",
                 "napógmus glúza", "tȟahú", "napókaške", "loté", "ištá", "hú", "čhaŋkȟáhu", "núŋǧe", "napsú", "sí", "osúŋ", "ité",
                 "čhuwí", "ikhú", "uŋzé", "čhečá", "thezí"]
d["a4a_people"] = ["wičhíŋčala", "šič’éšitku", "čhiŋkšítku", "wayáwa", "wakȟáŋyeža", "hokšíčala", "čhiŋkší", "até", "húŋku", "čhekpápi (hokšíla)", "čhiyékičhiyapi",
                   "wičháša", "iná", "kaká", "thiwáhe", "haŋkášitku", "tȟawíču", "hignáku", "hiŋgnátȟuŋ", "wíŋyaŋ",
                   "uŋčí", "akíčhisčupi", "kȟoškéku", "čhekpápi (wičhíŋčala)", "eháŋk’ehaŋ", "hokšíla", "čhuwékičhiyapi", "tȟa-wíčhiŋčala", "wikȟóškalaka"]
d["a4a_food"] = ["čhaŋmháŋska", "tȟašúptȟaŋka", "tȟaló yukpáŋpi", "tȟaló", "čhaŋmháŋska ǧíȟča", "aǧúyabskuya gmigmá", "asáŋpi yaȟúǧapi", "psíŋ", "čhaȟsníyaŋ", "waštágyapi skúyeyapi",
                 "asáŋpi niníyaŋpi", "waskúyeča", "aǧúyapi opémnila", "yaȟúǧapi", "waštágyapi", "waglékšuŋ špaŋyáŋpi", "aǧúyapi ǧiǧíla", "wašíŋ", "pȟáza", "wakȟályapi", "tȟaspáŋ opémnipi",
                 "tȟaspáŋpȟa haŋpí", "čhaŋmháŋska ǧí", "mní", "wíčhokaŋ wótapi", "čháǧa", "čhaŋháŋpi", "iyúltȟuŋ", "waháŋpi", "tȟaspáŋzi haŋpí", "bločhéuŋpap waksáksapi",
                 "aǧúyapi skúyela", "blopátȟaŋpi", "čheyáka", "aǧúyapi pagmúpi", "asáŋpi sutá", "tȟaló špaŋyáŋpi", "čhoǧíŋkhiyapi", "owáslesleče", "akálapila", "aǧúyapi zigzíča",
                 "aǧúyapiblu", "čhaŋšíŋ", "spakéli", "khukhúše čhosyápi", "waȟpékȟalyapi", "čhéǧa", "apášluta", "khukhúše čhečá", "asáŋpi", "wóyute", "wagmíza",
                 "aǧúyapi", "gmá", "wítka", "tȟašúpa", "khukhúše tȟaló"]
d["a4a_clothes_n_accessories"] = ["íŋyaŋ othéȟika úŋpi", "huŋyákȟuŋ", "ógle šóka", "siyéte háŋska", "wawíyuŋpi ógle", "uŋzóǧe ptéčela", "sičháŋophiye", "wanáp’iŋ",
                                  "ógle wapȟóštaŋ yukȟé", "wówaši hayápi", "maǧážu ógle", "uŋzóǧe", "ištámaza sápa", "ógle hiŋšmá", "ógle zigzíča",
                                  "ógle", "maštéhaŋpa", "wówaši hayápi čhó", "ištíŋma hayápi", "nitéhepi", "hayápi hí", "maǧážu haŋpa", "íŋyaŋ othéȟika", "tȟahú ičáške",
                                  "haŋpónašloke", "napíŋkpa", "wapȟóštaŋ", "´ógle aȟčó", "wapȟóštaŋla", "nuŋwáŋ hayápi", "háŋpa", "ógle čhuwíyuksa",
                                  "ištámaza", "haŋpkȟáŋ", "ayáskabtȟúŋpi", "tȟahú ičhósye", "akáŋhaŋpa", "čheškíkȟaŋ", "čhuwígnaka", "iphíyaka",
                                  "akíglake", "šiná hiŋšmá", "mahél úŋpi", "Kisúŋla šiná", "čheškíyutaŋ"]
d["a4a_actions"] = ["slípA", "oíȟpeyA", "wóla", "gliȟpáyA", "yuȟlátA", "épatȟaŋ", "ómna", "waŋyáŋkA", "alí", "ok’Á", "hó", "ištíŋmA",
                    "waátuŋwAŋ", "wičhítowa", "pȟóskil yúzA", "waúŋspewičhákhiyA", "asníkiyA", "wakáǧA", "yukȟápA", "napéglaskápA", "čhéyA", "lowáŋ", "atáyA", "wawíyopȟeyA",
                    "yakpí", "iyápȟa", "čhaŋkpéška makȟágle", "iyéyA", "wačhí", "hoȟpÁ", "yuksÁ", "wíyukčaŋ", "wapȟápȟa", "wóglakA", "waáš’a", "lol’´íȟ’aŋ",
                    "wówa", "apȟÁ", "čhaŋkáhotȟuŋ", "ablézA", "makȟáyublu", "wíhaŋblA", "iyáyeyA", "nuŋwÁŋ", "ožíži", "čhaókit’A", "yuȟláȟla",
                    "wók’u", "slohÁŋ", "éthi", "papsúŋ", "pȟehíŋ glužáža", "šičáhowayA", "yuȟléčA", "ókaǧA", "yutítaŋ", "ločhíŋ", "íputȟakA", "yaŋkÁ",
                    "ikpákpi", "ištákakpaŋ", "naȟ’úŋ", "theȟíla", "škátA", "iglúžaža", "wóglakA", "kaȟápA", "yatkÁŋ", "kiŋyÁŋ", "tȟápa oštéšteya waŋkáyeyA",
                    "yašpÁ", "wakáhiŋtA", "aígluta", "knit", "waš’ág’ič’iyA", "ičú", "wayáwa", "hotȟúŋ", "ayúta", "wótA"]
d["a4a_construction"] = ["thiyóžaŋžaŋ", "thiyópa", "wópazo oštéšteka", "owáčhekiye", "šúŋka othí", "eháŋni thihúȟaka", "šótA", "ošóta inápȟA", "makȟá špáŋpi",
                         "mnič’ápi", "čhaŋkú", "íŋyaŋ thípi", "aǧúyapi okáǧe", "oíyahe", "owáyawa", "wóžuthi", "čheyáktȟuŋpi", "mninátȟakapi", "íŋyaŋ thipȟéstola",
                         "waníyaŋpi othí", "tȟaté ičáhomni", "ožáŋžaŋglepi", "čháŋthipi", "oáli", "mas’óphiye", "thikáitepa", "thičhé", "owákaȟla", "iyéčhiŋkíŋyaŋka onážiŋ",
                         "wiyóhiyaŋpata thípi wakȟáŋ", "okhúže thípi", "wakhéya", "thípi", "thitȟáhepiya", "mázaska thípi", "ožáŋžaŋglepi thiyópa", "thigmígma"]
d["a4a_nature"] = ["makȟóčhe", "mayá", "pahá", "ósmaka", "íŋyaŋ", "mniwáŋča", "blé", "óhuta", "mniwáŋča óhuta", "ȟé", "bléla",
                   "ipȟá", "íŋyaŋšlo", "iǧúǧa oȟlóka", "čhasmú pahá", "wíta", "čhúŋšoke", "čhasmú makȟóčhe", "čháǧa wíta"]
d["a4a_jobs"] = ["heyókȟa", "thikáǧA", "wačhékiye wičháša", "wamákȟaškaŋ aphíyA", "wayásu", "wóhela", "khiíŋyaŋke s’a", "wówapi awáŋyaŋkA", "tȟápa oštéšteya waŋkáyeyA", "čhaŋksáyuha",
                 "mní oíŋyaŋka aphíyA", "čhešká máza", "wíŋyaŋyatápi", "wóžu wičháša", "wakȟáŋȟ’aŋ wičháša", "mas’ákičhita", "waákisniyA", "makȟá špáŋpi awáŋyaŋkA", "thiyúžaža wíŋyaŋ", "waúŋspewičhákhiyA",
                 "wakhúwa", "akíčhita", "olówaŋ káǧA", "waákhiya wičháša", "hokhúwa s’a", "wíŋyaŋyatápila", "pȟelkásni wičháša", "witȟáŋšna úŋ",
                 "mniwáŋča wamánuŋ s’a", "pteóle", "wakȟáŋgli awáŋyaŋkA", "wayázaŋ awáŋyaŋkA", "wičhášayatápi", "tȟuŋkášilayapi", "wówaši oyáŋke", "čhaŋkážipA", "šuŋk’ákaŋyaŋkA",
                 "wówaši", "iyéčhiŋkíŋyaŋka aphíyA", "kiŋyékhiyapi kaȟápA", "škáte s’a", "lol’íȟ’aŋ wičháša", "wayáwa", "wapȟáte s’a", "oíčazo owá", "wičhášayatápila", "pope",
                 "mniwáŋča akíčhita", "napé uŋ kičhízapi", "wačhí wíŋyaŋ", "škalwíčhakhiyA", "wičháȟpi ománi", "itówapi káǧA", "ištíŋmat’ewíčhayA", "wapásikA"]
d["a4a_fruit_n_veg"] = ["pȟaŋǧízizi", "wažúštečasapa", "hútȟotȟo", "thíŋpsiŋla skaská", "čhaŋmháŋskaǧi sú", "tȟaspáŋ hiŋšmá", "suótala", "tȟaspáŋzi tȟáŋka",
                        "waȟčáȟča watȟótȟo", "čhuŋwíyapahe", "waȟpé šokšóka", "tȟamníoȟpi", "čhoǧíŋ", "pȟaŋǧípȟepȟe", "uŋžíŋžiŋtka", "khiwí", "hustóla yútapi",
                        "slála", "kuŋkúŋ", "omníča", "wažúšteča", "pȟayá yútapi", "tȟakȟáŋheča", "tȟaspáŋhiŋšma čík’ala", "bló",
                        "omníča gmigmí", "waȟpéyutapi", "čhaŋpȟá skúyeyapi", "wagmú", "watȟókča tȟóla", "tȟaspáŋ pȟéstola", "tȟaspáŋzi", "wagmúzi", "tȟaspáŋtȟo slá",
                        "pšíŋkčeka", "pšíŋ", "tȟaspáŋ", "tȟaspáŋtȟo pȟá", "waȟčálaska yútapi", "subláska", "maštíŋčatȟawóte", "tȟaspáŋpȟa", "wagmúšatȟo",
                        "tȟókahu yútapi", "kȟáŋta", "pšiŋskúya", "zíškopela", "wagmúčhaŋ"]
d["a4a_transport"] = ["walšína", "wíši iwátȟokšu", "iyéčhiŋkíŋyaŋkA", "hunáhomni", "čhaŋyúwipi káǧapi", "ináhomni", "oyáte itȟókšu", "hunáhomni iyúhomni", "watópȟapila", "iwátȟokšu", "čhaŋwóslohaŋ tȟáŋka",
                      "čhúŋwiŋža akáȟpe", "napȟópȟopela", "mázačhaŋku", "tȟatéwata", "thiwáhe itȟókšu", "čháŋwata", "wičháȟpi wáta", "wápaha", "čhaŋwóslohaŋ", "hunáhomnipi"]