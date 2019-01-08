# -*- coding: utf-8 -*-

# traduzido para português da europa por Américo Monteiro (a_monteiro@gmx.com)

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The colour names in other languages than English are already in smaller font.

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

# word list adapted from GCompris:
# https://github.com/gcompris/GCompris-qt/blob/master/src/activities/lang/resource/content-pt_BR.json

d["a4a_animals"] = ['vaca', '<turkey>', 'camarão', '<wolf>', '<panther>', '<panda>', '<magpie>', 'molusco', '<pony>', '<mouse>', 'pug', '<koala>', 'sapo', '<ladybug>', '<gorilla>', '<llama>', '<vulture>', '<hamster>', 'pássaro', 'estrela do mar', 'corvo', '<parakeet>', '<caterpillar>', '<tiger>', '<hummingbird>', '<piranha>', 'porco', '<scorpion>', 'raposa', '<leopard>', '<iguana>', '<dolphin>', 'morcego', 'pintinho', 'caranguejo', 'galinha', '<wasp>', '<chameleon>', '<whale>', '<hedgehog>', '<fawn>', '<moose>', 'abelha', '<viper>', '<shrike>', '<donkey>', '<guinea pig>', '<sloth>', '<horse>', '<penguin>', '<otter>', '<bear>', '<zebra>', '<ostrich>', 'camelo', '<antelope>', '<lemur>', '<pigeon>', '<lama>', 'toupeira', '<ray>', '<ram>', 'gambá', '<jellyfish>', '<sheep>', 'tubarão', '<kitten>', '<deer>', 'caracol', '<flamingo>', '<rabbit>', '<oyster>', '<beaver>', '<sparrow>', '<dove>', '<eagle>', 'besouro', '<hippopotamus>', 'coruja', '<cobra>', '<salamander>', '<goose>', '<kangaroo>', '<dragonfly>', '<toad>', '<pelican>', 'lula', '<lion cub>', '<jaguar>', 'pato', '<lizard>', '<rhinoceros>', '<hyena>', 'boi', '<peacock>', '<parrot>', '<elk>', 'jacaré', '<ant>', 'cabra', '<baby rabbit>', '<lion>', 'esquilo', '<opossum>', 'chimpanzé', '<doe>', '<gopher>', '<elephant>', 'girafa', 'aranha', 'cachorro', '<jay>', '<seal>', '<rooster>', '<turtle>', '<bull>', 'gato', 'rato', '<slug>', '<buffalo>', '<blackbird>', 'cisne', '<lobster>', 'cachorro', 'mosquito', 'cobra', 'frango', '<anteater>']
d["a4a_sport"] = ['<judo>', 'piscina', 'pedalar', 'alongar', '<helmet>', '<ice skating>', 'andar', 'correr', 'nadar', 'saltar', 'caminhar', '<boxing>', '<hockey>', '<race>', 'arremessar', 'patinar', 'ganhar', 'agachar', 'esquiar', '<golf>', '<whistle>', 'tocha', '<sailing>', 'de pé', '<tennis>', 'pular', '<rowing>', 'correr', 'corda']
d["a4a_body"] = ['dentes', '<cheek>', '<ankle>', 'joelho', '<toe>', '<muscle>', 'boca', '<feet>', 'mão', '<elbow>', 'cabelo', '<eyelash>', '<beard>', '<belly button>', '<thumb>', '<breast>', '<nostril>', 'nariz', 'quadril', '<arm>', '<eyebrow>', 'punho', 'pescoço', 'pulso', 'garganta', '<eye>', '<leg>', '<spine>', 'orelha', '<finger>', 'pé', 'trança', 'rosto', 'costas', 'queixo', '<bottom>', 'coxa', '<belly>']
d["a4a_people"] = ['menina', '<male>', '<son>', '<mates>', '<friends>', '<baby>', 'criança', 'pai', '<mom>', '<twin boys>', '<brothers>', '<man>', '<mother>', '<grandfather>', '<family>', '<female>', '<wife>', '<husband>', 'noiva', '<madam>', '<grandmother>', '<couple>', 'rapaz', '<twin girls>', '<tribe>', 'menino', '<sisters>', '<woman>', '<lady>']
d["a4a_food"] = ['doce', '<sausage>', '<hamburger>', '<steak>', 'doce de chocolate', '<doughnut>', '<coconut>', 'arroz', '<ice cream>', '<jelly>', '<yoghurt>', '<dessert>', '<pretzel>', '<peanut>', '<jam>', 'banquete', 'biscoito', '<bacon>', '<spice>', '<coffee>', '<pie>', '<lemonade>', 'chocolate', '<water bottle>', 'lanche', 'gelo', '<sugar>', 'molho', '<soup>', 'suco', '<fries>', 'bolo', '<mashed potatoes>', '<tea>', 'brioche', 'queijo', '<beef>', 'sanduíche', '<slice>', 'granulado', '<pizza>', 'farinha', 'chiclete', 'espaguete', '<roast>', 'ensopado', 'espalhar', '<meat>', '<milk>', '<meal>', 'milho', 'pão', '<walnut>', '<egg>', '<hot dog>', '<ham>']
d["a4a_clothes_n_accessories"] = ['<jewellery>', 'meia', '<jacket>', '<heel>', 'jaleco', '<shorts>', '<pocket>', '<necklace>', '<sweatshirt>', '<uniform>', '<raincoat>', '<trousers>', '<sunglasses>', 'casaco', '<pullover>', 'camisa', '<sandals>', 'terno', '<pyjamas>', 'saia', '<zip>', '<shoes>', 'jóia', '<tie>', '<slippers>', '<gloves>', 'chapéu', 'manga', 'boné', '<swimming suit>', '<trainer>', '<vest>', '<glasses>', '<shoelace>', 'remendo', 'cachecol', 'sapato', '<button>', 'vestido', '<sash>', '<shoe sole>', '<robe>', '<pants>', '<kimono>', '<overalls>']
d["a4a_actions"] = ['lamber', '<slam>', 'implorar', '<fell>', 'arranhar', 'tocar', 'farejar', 'observar', 'escalar', 'escavar', 'uivar', 'dormir', 'explorar', 'desenhar', 'abraçar', 'ensinar', 'cochilar', 'argila', 'pegar', 'palma', 'chorar', 'cantar', 'encontrar', '<sell>', 'bicar', '<beat>', 'ajoelhar', 'encontrar', 'dança', '<cough>', 'cortar', 'pensar', 'latir', '<speak>', 'torcer', '<bake>', 'escrever', '<punch>', '<strum>', 'estudar', 'arar', 'sonhar', '<post>', 'mergulho', 'cochichar', '<sob>', 'sacudir', '<feed>', 'engatinhar', 'acampamento', 'derramar', 'limpar', 'gritar', 'rasgar', 'boiar', '<pull>', '<ate>', '<kiss>', 'sentar', 'chocar', 'piscar', 'escutar', 'beijar', 'brincar', 'lavar', 'conversar', 'dirigir', 'bebida', 'voar', '<juggle>', 'mordida', '<sweep>', 'olhar', 'tricotar', 'levantar', 'buscar', 'ler', 'coaxar', 'olhar', 'comer']
d["a4a_construction"] = ['<lighthouse>', 'porta', '<circus>', '<church>', '<kennel>', '<temple>', 'fumaça', '<chimney>', 'tijolo', '<well>', 'rua', 'castelo', 'mercearia', '<staircase>', 'escola', 'fazenda', 'ponte', '<dam>', '<pyramid>', 'celeiro', '<mill>', '<window>', 'cabana', '<step>', 'loja', 'celeiro', 'telhado', '<steeple>', '<garage>', '<mosque>', '<hospital>', '<tent>', '<house>', '<wall>', 'banco', '<shutter>', 'oca']
d["a4a_nature"] = ['terreno', 'penhasco', '<hill>', '<canyon>', 'rocha', '<sea>', 'lago', '<coast>', 'costa', '<mountain>', '<pond>', '<peak>', '<lava>', 'caverna', 'duna', '<island>', '<forest>', '<desert>', '<iceberg>']
d["a4a_jobs"] = ['palhaço', '<engineer>', '<priest>', 'veterinário', 'juiz', '<chef>', 'atleta', '<librarian>', '<juggler>', '<policeman>', '<plumber>', 'insígnia', 'rainha', '<farmer>', '<magician>', 'cavaleiro', '<doctor>', '<bricklayer>', '<cleaner>', 'professor', 'caçador', '<soldier>', '<musician>', '<lawyer>', '<fisherman>', 'princesa', '<fireman>', '<nun>', '<pirate>', 'vaqueiro', '<electrician>', '<nurse>', '<king>', '<president>', '<office worker>', '<carpenter>', '<jockey>', '<worker>', '<mechanic>', '<pilot>', '<actor>', 'cozinhar', '<student>', '<butcher>', '<accountant>', 'príncipe', 'papa', '<sailor>', '<boxer>', '<ballet dancer>', 'treinador', '<astronaut>', '<painter>', '<anaesthesiologist>', '<scientist>']
d["a4a_fruit_n_veg"] = ['cenoura', '<blackberries>', '<celery>', '<turnip>', '<cacao>', 'pêssego', '<melon>', '<grapefruit>', '<broccoli>', '<grapes>', '<spinach>', '<fig>', '<kernel>', '<radish>', '<tomato>', '<kiwi>', '<asparagus>', '<olives>', '<cucumbers>', '<beans>', 'morango', '<peppers>', '<raspberry>', '<apricot>', '<potatoes>', '<peas>', '<cabbage>', '<cherries>', 'abóbora', '<blueberries>', '<pear>', 'laranja', '<pumpkin>', '<avocado>', '<garlic>', '<onion>', '<apple>', 'limão', '<cauliflower>', '<mango>', '<lettuce>', '<lemon>', '<aubergine>', '<artichokes>', '<plums>', '<leek>', '<bananas>', '<papaya>']
d["a4a_transport"] = ['veleiro', '<taxi>', 'carro', 'bicicleta', '<raft>', '<pedal>', '<bus>', '<handlebar>', 'barco', 'caminhão', 'trenó', '<carpet>', '<motorcycle>', 'trem', 'navio', 'van', 'canoa', '<rocket>', '<mast>', '<sledge>', '<bicycle>']

