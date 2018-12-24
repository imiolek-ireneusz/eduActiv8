# -*- coding: utf-8 -*-

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The color names in other languages than English are already in smaller font.


d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

numbers = ['u', 'dos', 'tres', 'quatre', 'cinc', 'sis', 'set', 'vuit', 'nou', 'deu', 'onze', 'dotze', 'tretze',
           'catorze', 'quinze', 'setze', 'disset', 'divuit', 'dinou', 'vint', 'vint-i-u', 'vint-i-dos', 'vint-i-tres',
           'vint-i-quatre', 'vint-i-cinc', 'vint-i-sis', 'vint-i-set', 'vint-i-vuit', 'vint-i-nou']
numbers2090 = ['vint', 'trenta', 'quaranta', 'cinquanta', 'seixanta', 'setanta', 'vuitanta', 'noranta']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
dp['abc_flashcards_word_sequence'] = ['Ànec', 'Barca', 'Coala', 'Calçat', 'Dofí', 'Elefant', 'Formiga', 'Gat',
                                      'Hipopòtam', 'Iglú', 'Joguina', 'Kiwi', 'Lleó', 'Mussol', 'Nit', 'Oceà', 'Poma',
                                      'Quadern', 'Ratolí', 'Síndria', 'Tomàquet', 'Ull', 'Violí', 'Windsurf', 'Xilòfon',
                                      'Yoga', 'Zebra']
d['abc_flashcards_word_sequence'] = ['<1>À<2>nec', '<1>B<2>arca', '<1>C<2>oala', '<2>Cal<1>ç<2>at', '<1>D<2>ofí',
                                     '<1>E<2>l<1>e<2>fant', '<1>F<2>ormiga', '<1>G<2>at', '<1>H<2>ipopòtam',
                                     '<1>I<2>glú', '<1>J<2>oguina', '<1>K<2>iwi', '<1>L<2>leó', '<1>M<2>ussol',
                                     '<1>N<2>it', '<1>O<2>ceà', '<1>P<2>oma', '<1>Q<2>uadern', '<1>R<2>atolí',
                                     '<1>S<2>índria', '<1>T<2>omàque<1>t', '<1>U<2>ll', '<1>V<2>iolí', '<1>W<2>indsurf',
                                     '<1>X<2>ilòfon', '<1>Y<2>oga', '<1>Z<2>ebra']
 

d['abc_flashcards_frame_sequence'] = [3, 1, 72, 60, 59, 4, 0, 2, 47, 8, 58, 74, 11, 14, 54, 52, 42, 13, 12, 26, 33, 75,
                                      21, 66, 23, 32, 25]

# alphabet ca
alphabet_lc = ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['à', 'é', 'è', 'í', 'ò', 'ó', 'ú', '-']
accents_uc = ['À', 'É', 'È', 'Í', 'Ò', 'Ó', 'Ú']


def n2txt(n, twoliner=False):
    "takes a number from 0 - 100 and returns it back in a word form, ie: 63 returns 'sixty three'."
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
                return [tens + "-", ones]
            else:
                return tens + "-" + ones

    elif n == 0:
        return "zero"
    elif n == 100:
        return "cent"
    return ""


hores = ['una', 'dues', 'tres', 'quatre', 'cinc', 'sis', 'set', 'vuit', 'nou', 'deu', 'onze', 'dotze', 'una']


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 7:
        if h == 12:
            h = 1
        else:
            h += 1

    if h == 1:
        if m == 0:
            return "la una en punt"
        elif m == 1:
            return "la una i un minut"
        elif 0 < m < 8:
            return "la una i %s" % n2txt(m)
        elif 7 < m < 15:
            return "un quart menys %s d'una" % n2txt(15 - m)
        elif m == 15:
            return "un quart d'una"
        elif 15 < m < 23:
            return "un quart i %s d'una" % n2txt(m - 15)
        elif 22 < m < 30:
            return "dos quarts menys %s d'una" % n2txt(30 - m)
        elif m == 30:
            return "dos quarts d'una"
        elif 30 < m < 38:
            return "dos quarts i %s d'una" % n2txt(m - 30)
        elif 37 < m < 45:
            return "tres quarts menys %s d'una" % n2txt(45 - m)
        elif m == 45:
            return "tres quarts d'una"
        elif 45 < m < 53:
            return "tres quarts i %s d'una" % n2txt(m - 45)
        elif 52 < m < 59:
            return "la una menys %s" % n2txt(60 - m)
        elif m == 59:
            return "la una menys un minut"
    else:
        if m == 0:
            return "les %s en punt" % hores[h - 1]
        elif m == 1:
            return "les %s i un minut" % hores[h - 1]
        elif 0 < m < 8:
            return "les %s i %s" % (hores[h - 1], n2txt(m))
        elif 7 < m < 15:
            return "un quart menys %s de %s" % (n2txt(15 - m), hores[h - 1])
        elif m == 15:
            return "un quart de %s" % hores[h - 1]
        elif 15 < m < 23:
            return "un quart i %s de %s" % (n2txt(m - 15), hores[h - 1])
        elif 22 < m < 30:
            return "dos quarts menys %s de %s" % (n2txt(30 - m), hores[h - 1])
        elif m == 30:
            return "dos quarts de %s" % hores[h - 1]
        elif 30 < m < 38:
            return "dos quarts i %s de %s" % (n2txt(m - 30), hores[h - 1])
        elif 37 < m < 45:
            return "tres quarts menys %s de %s" % (n2txt(45 - m), hores[h - 1])
        elif m == 45:
            return "tres quarts de %s" % hores[h - 1]
        elif 45 < m < 53:
            return "tres quarts i %s de %s" % (n2txt(m - 45), hores[h - 1])
        elif 52 < m < 59:
            return "les %s menys %s" % (hores[h - 1], n2txt(60 - m))
        elif m == 59:
            return "les %s menys un minut" % hores[h - 1]

#write a fraction in words
numerators = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
d_singular = ['', 'half', 'third', 'quarter', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
d_plural = ['', 'halves', 'thirds', 'quarters', 'fifths', 'sixths', 'sevenths', 'eighths', 'ninths', 'tenths', 'elevenths', 'twelfths']

def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d-1]
    else:
        return numerators[n-1] + " " + d_plural[d-1]

# word list adapted from GCompris:
# https://github.com/gcompris/GCompris-qt/blob/master/src/activities/lang/resource/content-ca.json

d["a4a_animals"] = ['vaca', 'gall dindi', 'gamba', 'llop', 'pantera', 'ós panda', 'garsa', 'cloïssa', 'poni', 'ratolí', 'carlí', 'coala', 'granota', 'marieta', 'goril·la', '<llama>', 'voltor', '<hamster>', 'ocell', 'estrella de mar', 'corb', 'periquito', 'eruga', 'tigre', 'colibrí', 'piranya', 'porc', 'escorpí', 'guineu', 'lleopard', 'iguana', 'dofí', 'ratpenat', 'pollet', 'cranc', 'gallina', 'vespa', 'camaleó', 'balena', 'eriçó', 'cervatell', 'ant', 'abella', 'escurçó', '<shrike>', '<donkey>', '<guinea pig>', 'peresós', 'cavall', '<penguin>', 'llúdriga', 'ós', 'zebra', 'estruç', 'camell', 'antílop', 'lèmur', 'tórtora', 'llama', 'talp', '<ray>', '<ram>', 'mofeta', 'medusa', 'ovella', 'tauró', 'gatet', 'cérvol', 'cargol', 'flamenc', 'conill', 'ostra', 'castor', 'pardal', 'colom', 'àguila', 'escarabat', 'hipopòtam', 'òliba', 'cobra', 'salamandra', 'oca', 'cangur', 'libèl·lula', 'gripau', 'pelicà', 'calamar', '<lion cub>', 'jaguar', 'ànec', 'llangardaix', 'rinoceront', 'hiena', 'bou', 'paó', 'lloro', 'uapití', 'caiman', 'formiga', 'cabra', '<baby rabbit>', 'lleó', 'esquirol', 'opòssum', 'ximpanzé', 'cérvola', '<gopher>', '<elephant>', 'girafa', 'aranya', 'cadell', 'gaig', '<seal>', '<rooster>', 'tortuga', 'toro', 'gat', 'rata', 'llimac', 'búfal', 'merla', 'cigne', 'llagosta', 'gos', 'mosquit', 'serp', 'pollastre', 'ós formiguer']
d["a4a_sport"] = ['judo', 'piscina', 'ciclista', 'estirar', 'casc', '<ice skating>', 'caminar', 'córrer', 'córrer', 'nedar', 'saltar', 'caminar', '<boxing>', 'hoquei', 'cursa', 'llançar', 'patinar', 'guanyar', 'ajupir', 'esquiar', 'golf', '<whistle>', 'torxa', '<sailing>', 'dret', 'tennis', 'saltar', 'rem', 'fúting', 'corda']
d["a4a_body"] = ['dentadura', 'galta', 'turmell', 'genoll', 'dit del peu', 'múscul', 'boca', '<feet>', 'mà', 'colze', 'cabell', 'pestanya', 'barba', '<belly button>', 'polze', 'pit', 'nariu', 'nas', 'maluc', 'braç', '<eyebrow>', 'puny', 'coll', 'canell', 'gola', '<eye>', 'cama', 'espina', 'orella', 'dit', 'peu', 'trena', 'cara', 'esquena', 'barbeta', 'natges', 'cuixa', 'panxa']
d["a4a_people"] = ['noia', '<male>', 'fill', '<mates>', '<friends>', '<baby>', 'nen', 'pare', 'mama', '<twin boys>', '<brothers>', 'home', 'mare', '<grandfather>', 'família', '<female>', 'muller', 'marit', 'núvia', '<madam>', 'àvia', 'parella', 'mosso', '<twin girls>', 'tribu', 'noi', '<sisters>', 'dona', 'dama']
d["a4a_food"] = ['caramel', 'salsitxa', 'hamburguesa', '<steak>', 'dolç de xocolata', 'bunyol', 'coco', 'arròs', '<ice cream>', 'gelatina', '<yoghurt>', 'postre', '<pretzel>', '<peanut>', 'melmelada', 'banquet', 'galeta', '<bacon>', 'espècia', 'cafè', 'pastís', 'llimonada', 'xocolata', '<water bottle>', 'dinar', 'glaçó', 'sucre', 'salsa', 'sopa', 'suc', 'patata fregida', 'pastís', '<mashed potatoes>', '<tea>', 'brioix', 'formatge', '<beef>', 'sandvitx', '<slice>', 'espurnes', 'pizza', 'farina', 'xiclet', 'espagueti', 'rostit', 'beguda', 'guisat', 'untar', 'carn', 'llet', 'àpat', 'blat de moro', 'pa', 'nou', 'ou', '<hot dog>', 'pernil']
d["a4a_clothes_n_accessories"] = ['<jewellery>', 'mitjó', 'jaqueta', 'taló', 'bata', '<shorts>', 'butxaca', 'collaret', 'dessuadora', 'uniforme', 'impermeable', '<trousers>', '<sunglasses>', 'abric', 'jersei', 'camisa', 'sandàlia', 'mudada', '<pyjamas>', 'faldilla', '<zip>', '<shoes>', 'joia', '<tie>', 'sabatilla', '<gloves>', 'barret', 'màniga', 'gorra', '<swimming suit>', '<trainer>', 'armilla', 'ulleres', 'cordó', 'pedaç', 'bufanda', 'sabata', 'botó', 'vestit', 'faixa', '<shoe sole>', 'mantell', 'pantalons', 'quimono', '<overalls>']
d["a4a_actions"] = ['llepar', 'esmaixada', 'demanar', '<fell>', 'esgarrapar', 'tocar', 'ensumar', 'mirar', 'escalada', 'cavar', 'udolar', 'dormir', 'explorar', 'dibuixar', 'abraçar', 'ensenyar', 'migdiada', 'argila', 'pescar', 'picar de mans', 'plorar', 'cantar', 'trobar-se', '<sell>', 'picotejar', 'batre', 'agenollar', 'trobar', 'ballar', 'tossir', 'tallar', 'pensar', 'bordar', 'parlar', 'animar', '<bake>', 'escriure', '<punch>', '<strum>', 'estudiar', 'llaurar', 'somiar', 'bústia', 'immersió', 'xiuxiuejar', 'sanglotar', 'sacsejar', 'donar de menjar', 'gatejar', 'acampar', 'vessar', 'rentar', 'cridar', 'esquinçar', 'flotar', 'estirar', '<ate>', 'petó', 'seure', "sortir de l'ou", "picada d'ullet", 'sentir', 'bessar', 'jugar', 'banyar', 'parlar', 'conduir', 'beguda', 'volar', '<juggle>', 'mica', '<sweep>', 'mirar-se', 'teixir', 'aixecar', 'informar', 'llegir', 'raucar', 'mirar fixament', 'menjar']
d["a4a_construction"] = ['far', 'porta', 'circ', '<church>', '<kennel>', 'temple', 'fum', 'xemeneia', 'maó', '<well>', 'carrer', 'castell', 'botiga', 'escala', 'escola', 'granja', 'pont', 'presa', 'piràmide', 'graner', 'molí', 'finestra', 'cabana', 'esglaó', 'botiga', 'cobert', 'teulada', 'campanar', 'garatge', 'mesquita', 'hospital', 'tenda', 'casa', 'mur', 'banc', 'finestró', 'cabana']
d["a4a_nature"] = ['terreny', 'penya-segat', 'turó', 'canó', 'roca', 'mar', 'llac', 'costa', 'riba', 'muntanya', 'estany', 'pic', 'lava', 'cova', 'duna', 'illa', 'bosc', 'desert', 'iceberg']
d["a4a_jobs"] = ['pallasso', 'enginyer', 'sacerdot', 'veterinari', 'jutge', 'cuiner', 'atleta', 'bibliotecària', 'malabarista', '<policeman>', 'fontaner', 'insígnia', 'reina', 'granger', '<magician>', 'cavaller', 'metge', 'paleta', '<cleaner>', 'professora', 'caçador', 'soldat', 'músic', 'advocat', 'pescador', 'princesa', 'bomber', 'monja', 'pirata', 'vaquer', 'electricista', 'infermera', 'rei', 'president', '<office worker>', 'fuster', 'joquei', 'treballador', 'mecànic', 'pilot', 'actor', 'cuinar', 'estudiant', 'carnisser', 'comptable', 'princep', 'papa', 'mariner', 'boxejador', '<ballet dancer>', 'entrenador', 'astronauta', '<painter>', '<anaesthesiologist>', '<scientist>']
d["a4a_fruit_n_veg"] = ['pastanaga', '<blackberries>', 'api', 'nap', 'cacau', 'préssec', 'meló', 'pomelo', 'bròquil', '<grapes>', 'espinac', 'figa', 'nucli', 'rave', '<tomato>', 'kiwi', 'espàrrec', '<olives>', '<cucumbers>', '<beans>', 'maduixa', 'pebrot', 'gerd', 'albercoc', '<potatoes>', '<peas>', 'col', '<cherries>', 'carbassó', '<blueberries>', 'pera', 'taronja', 'carbassa', 'alvocat', 'all', 'ceba', 'poma', 'llima', 'coliflor', 'mango', 'enciam', 'llimona', '<aubergine>', '<artichokes>', '<plums>', 'porro', '<bananas>', 'papaia']
d["a4a_transport"] = ['veler', 'taxi', 'cotxe', 'bicicleta', 'barca solera', 'pedal', 'autobús', 'manillar', 'barca', 'camió', 'trineu', 'catifa', 'moto', 'tren', 'vaixell', 'furgoneta', 'canoa', 'coet', 'màstil', '<sledge>', '<bicycle>']
