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

# word lists

numbers = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once', 'doce', 'trece',
           'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve', 'veinte', 'veintiuno',
           'veintidós', 'veintitrés', 'veinticuatro', 'veinticinco', 'veintiséis', 'veintisiete', 'veintiocho',
           'veintinueve']
numbers2090 = ['veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']

dp['abc_flashcards_word_sequence'] = ['Abeto', 'Búho', 'Casa', 'Dormir', 'Elefante', 'Fortepiano', 'Gato', 'Hormiga',
                                      'Iglú', 'Jirafa', 'Koala', 'Loro', 'Manzana', 'Narciso', 'Ñu', 'Océano',
                                      'Pescado', 'Queso', 'Ratón', 'Sol', 'Tomate', 'Uvas', 'Violín', 'Wagon',
                                      'Xilófono', 'Yoga', 'Zapatos']
d['abc_flashcards_word_sequence'] = ['<1>A<2>beto', '<1>B<2>úho', '<1>C<2>asa', '<1>D<2>ormir',
                                     '<1>E<2>l<1>e<2>fant<1>e', '<1>F<2>ortepiano', '<1>G<2>ato', '<1>H<2>ormiga',
                                     '<1>I<2>glú', '<1>J<2>irafa', '<1>K<2>oala', '<1>L<2>oro', '<1>M<2>anzana',
                                     '<1>N<2>arciso', '<1>Ñ<2>u', '<1>O<2>céan<1>o', '<1>P<2>escado', '<1>Q<2>ueso',
                                     '<1>R<2>atón', '<1>S<2>ol', '<1>T<2>oma<1>t<2>e', '<1>U<2>vas', '<1>V<2>iolín',
                                     '<1>W<2>agon', '<1>X<2>ilófono', '<1>Y<2>oga', '<1>Z<2>apatos']
d['abc_flashcards_frame_sequence'] = [31, 14, 7, 49, 4, 34, 2, 0, 8, 30, 72, 15, 42, 69, 70, 52, 5, 57, 12, 18, 33, 6,
                                      21, 58, 23, 32, 60]

alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['á', 'é', 'í', 'ó', 'ú', 'ü', '-']
accents_uc = ['Á', 'É', 'Í', 'Ó', 'Ú', 'Ü']


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
                return [tens + " y ", ones]
            else:
                return tens + " y " + ones
    elif n == 0:
        return "cero"
    elif n == 100:
        return "cien"
    return ""


h1 = ['La una', 'Las dos', 'Las tres', 'Las cuatro', 'Las cinco', 'Las seis', 'Las siete', 'Las ocho', 'Las nueve',
      'Las diez', 'Las once', 'Las doce']


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s en punto" % h1[h - 1]
    elif m == 1:
        return "%s y un minuto" % h1[h - 1]
    elif m == 15:
        return "%s y cuarto" % h1[h - 1]
    elif m == 30:
        return "%s y media" % h1[h - 1]
    elif m == 45:
        return "%s menos cuarto" % h1[h - 1]
    elif m == 59:
        return "%s menos un minuto" % h1[h - 1]
    elif m < 30:
        return "%s y %s" % (h1[h - 1], n2txt(m))
    elif m > 30:
        return "%s menos %s" % (h1[h - 1], n2txt(60 - m))
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

# word list adapted from GCompris:
# https://github.com/gcompris/GCompris-qt/blob/master/src/activities/lang/resource/content-es.json

d["a4a_animals"] = ['vaca', 'pavo', 'camarón', 'lobo', 'pantera', 'panda', 'garza', 'almeja', 'poni', 'ratón', 'pug', 'coala', 'rana', 'mariquita', 'gorila', '<llama>', 'buitre', 'hámster', 'pájaro', 'estrella de mar', 'cuervo', 'periquito', 'oruga', 'tigre', 'colibrí', 'piraña', 'cerdo', 'escorpión', 'zorro', 'leopardo', 'iguana', 'delfín', 'murciélago', 'pollito', 'cangrejo', 'gallina', 'avispa', 'camaleón', 'ballena', 'erizo', 'cervatillo', 'alce', 'abeja', 'víbora', '<shrike>', 'burro', '<guinea pig>', 'perezoso', 'caballo', '<penguin>', 'nutria', 'oso', 'cebra', 'avestruz', 'camello', 'antílope', 'lémur', 'paloma', 'lama', 'topo', '<ray>', '<ram>', 'mofeta', 'medusa', 'oveja', 'tiburón', 'gatito', 'ciervo', 'caracol', 'flamenco', 'conejo', 'ostra', 'castor', 'gorrión', 'paloma', 'águila', 'escarabajo', 'hipopótamo', 'búho', 'cobra', 'salamandra', 'oca', 'canguro', 'libélula', 'sapo', 'pelícano', 'calamar', '<lion cub>', 'jaguar', 'pato', 'lagartija', 'rinoceronte', 'hiena', 'buey', 'pavo real', 'loro', 'alce', 'caimán', 'hormiga', 'cabra', '<baby rabbit>', 'león', 'ardilla', 'zarigüeya', 'chimpancé', 'ciervo', '<gopher>', 'elefante', 'jirafa', 'araña', 'cachorro', 'arrendajo', '<seal>', 'gallo', 'tortuga', 'toro', 'gato', 'rata', 'babosa', 'búfalo', 'mirlo', 'cisne', 'langosta', 'perro', 'mosquito', 'serpiente', 'pollo', 'oso hormiguero']
d["a4a_sport"] = ['judo', 'piscina', 'ciclista', 'estirar', 'casco', '<ice skating>', 'caminar', 'correr', 'nadar', 'salto', 'caminata', '<boxing>', 'hockey', 'carrera', 'lanzar', 'patinar', 'ganar', 'agacharse', 'esquiar', 'golf', '<whistle>', 'antorcha', '<sailing>', 'derecho', 'tenis', 'saltar', 'remo', 'footing', 'cuerda']
d["a4a_body"] = ['dentadura', 'mejilla', 'tobillo', 'rodilla', 'dedo del pie', 'músculo', 'boca', '<feet>', 'mano', 'codo', 'cabello', 'pestaña', 'barba', '<belly button>', 'pulgar', 'pecho', 'fosa nasal', 'nariz', 'cadera', 'brazo', 'ceja', 'puño', 'cuello', 'muñeca', 'garganta', '<eye>', 'pierna', 'espina', 'oreja', 'dedo', 'pie', 'trenza', 'cara', 'espalda', 'mentón', 'nalgas', 'muslo', 'vientre']
d["a4a_people"] = ['chica', 'masculino', 'hijo', '<mates>', '<friends>', 'bebé', 'niño', 'papá', 'mama', '<twin boys>', '<brothers>', 'hombre', 'madre', 'abuelo', 'familia', 'femenino', 'esposa', 'marido', 'novia', '<madam>', 'abuela', 'pareja', 'mozo', '<twin girls>', 'tribu', 'niño', '<sisters>', 'mujer', 'dama']
d["a4a_food"] = ['caramelo', 'salchicha', 'hamburguesa', '<steak>', 'dulce de chocolate', 'rosquilla', 'coco', 'arroz', '<ice cream>', 'jalea', '<yoghurt>', 'postre', '<pretzel>', '<peanut>', 'mermelada', 'banquete', 'galleta', '<bacon>', 'especia', 'café', 'pastel', 'limonada', 'chocolate', '<water bottle>', 'almuerzo', 'hielo', 'azúcar', 'salsa', 'sopa', 'zumo', 'patata frita', 'pastel', '<mashed potatoes>', '<tea>', 'brioche', 'queso', '<beef>', 'sándwich', '<slice>', 'chispas', 'pizza', 'harina', 'chicle', 'espagueti', 'asado', 'guiso', 'untar', 'carne', 'leche', 'comida', 'maíz', 'pan', 'nuez', 'huevo', '<hot dog>', 'jamón']
d["a4a_clothes_n_accessories"] = ['<jewellery>', 'calcetín', 'chaqueta', 'talón', 'bata', '<shorts>', 'bolsillo', 'collar', 'sudadera', 'uniforme', 'impermeable', '<trousers>', '<sunglasses>', 'abrigo', 'jersey', 'camisa', 'sandalia', 'arreglada', '<pyjamas>', 'falda', '<zip>', '<shoes>', 'joya', '<tie>', 'zapatilla', '<gloves>', 'sombrero', 'manga', 'gorra', '<swimming suit>', '<trainer>', 'chaleco', 'gafas', 'cordón', 'parche', 'bufanda', 'zapato', 'botón', 'vestir', 'faja', '<shoe sole>', 'manto', 'pantalones', 'quimono', '<overalls>']
d["a4a_actions"] = ['lamer', 'mate', 'pedir', '<fell>', 'arañar', 'tocar', 'olfatear', 'ver', 'escalada', 'cavar', 'aullar', 'dormir', 'explorar', 'dibujar', 'abrazar', 'enseñar', 'siesta', 'arcilla', 'pescar', 'palmear', 'llorar', 'cantar', 'encontrarse', 'vender', 'picotear', 'batir', 'arrodillarse', 'encontrar', 'bailar', 'toser', 'cortar', 'pensar', 'ladrido', 'hablar', 'animar', '<bake>', 'escribir', '<punch>', '<strum>', 'estudiar', 'arar', 'sueño', 'buzón', 'inmersión', 'susurrar', 'sollozar', 'sacudir', 'dar de comer', 'gatear', 'campamento', 'derramar', 'limpiar', 'gritar', 'rasgar', 'flotar', 'estirar', '<ate>', 'beso', 'sentarse', 'escotilla', 'guiño', 'escuchar', 'besar', 'jugar', 'lavar', 'charlar', 'conducir', 'beber', 'volar', '<juggle>', 'poco', '<sweep>', 'mirarse', 'tejer', 'levantar', 'traer', 'leer', 'croar', 'mirar fijamente', 'comer']
d["a4a_construction"] = ['faro', 'puerta', 'circo', 'iglesia', '<kennel>', 'templo', 'humo', 'chimenea', 'ladrillo', 'bien', 'calle', 'castillo', 'almacenar', 'escalera', 'escuela', 'granja', 'puente', 'presa', 'pirámide', 'granero', 'molino', 'ventana', 'cabaña', 'peldaño', 'tienda', 'cobertizo', 'techo', 'campanar', 'garaje', 'mezquita', 'hospital', 'tienda', 'casa', 'pared', 'banco', 'contraventana', 'cabaña']
d["a4a_nature"] = ['terreno', 'acantilado', 'colina', 'cañón', 'roca', 'mar', 'lago', 'costa', 'orilla', 'montaña', 'estanque', 'pico', 'lava', 'cueva', 'duna', 'isla', 'bosque', 'desierto', 'iceberg']
d["a4a_jobs"] = ['payaso', 'ingeniero', 'sacerdote', 'veterinario', 'juez', 'cocinero', 'atleta', 'bibliotecaria', 'malabarista', '<policeman>', 'fontanero', 'insignia', 'reina', 'agricultor', '<magician>', 'caballero', 'médico', 'albañil', '<cleaner>', 'maestro', 'cazador', 'soldado', 'músico', 'abogado', 'pescador', 'princesa', 'bombero', 'monja', 'pirata', 'vaquero', 'electricista', 'enfermera', 'rey', 'presidente', '<office worker>', 'carpintero', 'jockey', 'obrero', 'mecánico', 'piloto', 'actor', 'cocinar', 'estudiante', 'carnicero', 'contable', 'príncipe', 'papa', 'marinero', 'boxeador', '<ballet dancer>', 'entrenador', 'astronauta', '<painter>', '<anaesthesiologist>', '<scientist>']
d["a4a_fruit_n_veg"] = ['zanahoria', '<blackberries>', 'apio', 'nabo', 'cacao', 'melocotón', 'melón', 'pomelo', 'brócoli', '<grapes>', 'espinacas', 'higo', 'núcleo', 'rábano', '<tomato>', 'kiwi', 'espárragos', '<olives>', '<cucumbers>', '<beans>', 'fresa', 'pimiento', 'frambuesa', 'albaricoque', '<potatoes>', '<peas>', 'repollo', '<cherries>', 'calabacín', '<blueberries>', 'pera', 'naranja', 'calabaza', 'aguacate', 'ajo', 'cebolla', 'manzana', 'lima', 'coliflor', 'mango', 'lechuga', 'limón', '<aubergine>', '<artichokes>', '<plums>', 'puerro', '<bananas>', 'papaya']
d["a4a_transport"] = ['navegar', 'taxi', 'coche', 'bicicleta', 'balsa', 'pedal', 'autobús', 'manillar', 'bote', 'camión', 'trineo', 'alfombra', 'motocicleta', 'tren', 'barco', 'furgoneta', 'canoa', 'cohete', 'mástil', '<sledge>', '<bicycle>']
