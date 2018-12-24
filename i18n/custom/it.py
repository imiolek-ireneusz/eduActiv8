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

numbers = ['uno', 'due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto', 'nove', 'dieci', 'undici', 'dodici',
           'tredici', 'quattordici', 'quindici', 'sedici', 'diciassette', 'diciotto', 'diciannove', 'venti', 'ventuno',
           'ventidue', 'ventitré', 'ventiquattro', 'venticinque', 'ventisei', 'ventisette', 'ventotto', 'ventinove']
numbers2090 = ['venti', 'trenta', 'quaranta', 'cinquanta', 'sessanta', 'settanta', 'ottanta', 'novanta']

dp['abc_flashcards_word_sequence'] = ['Anguria', 'Barca', 'Casa', 'Dormire', 'Elefante', 'Fiori', 'Giraffa', 'Hockey',
                                      'Iglù', 'Koala', 'Leone', 'Mela', 'Narciso', 'Ombrello', 'Pomodoro', 'Quaderno',
                                      'Riccio', 'Sole', 'Teiera', 'Uva', 'Violino', 'Xilofono', 'Yoga', 'Zebra']
d['abc_flashcards_word_sequence'] = ['<1>A<2>nguri<1>a', '<1>B<2>arca', '<1>C<2>asa', '<1>D<2>ormire',
                                     '<1>E<2>l<1>e<2>fant<1>e', '<1>F<2>iori', '<1>G<2>iraffa', '<1>H<2>ockey',
                                     '<1>I<2>glù', '<1>K<2>oala', '<1>L<2>eone', '<1>M<2>ela', '<1>N<2>arciso',
                                     '<1>O<2>mbrell<1>o', '<1>P<2>omodoro', '<1>Q<2>uaderno', '<1>R<2>iccio',
                                     '<1>S<2>ole', '<1>T<2>eiera', '<1>U<2>va', '<1>V<2>iolino', '<1>X<2>ilofono',
                                     '<1>Y<2>oga', '<1>Z<2>ebra']
d['abc_flashcards_frame_sequence'] = [26, 1, 7, 49, 4, 36, 30, 68, 8, 72, 11, 42, 69, 20, 33, 13, 29, 18, 19, 6, 21, 23,
                                      32, 25]

# used in telling time activity
# the number lists below are for languages with a bit more complex forms, ie. different suffixes depending on context - if your language is like that check Polish translation to see how to use them

# alphabet - it
alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'X', 'Y', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['à', 'è', 'é', 'ì', 'í', 'î', 'ò', 'ó', 'ù', 'ú', '-']
accents_uc = ['À', 'È', 'É', 'Ì', 'Í', 'Î', 'Ò', 'Ó', 'Ù', 'Ú']


def n2txt(n, twoliner=False):
    "takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."
    if 0 < n < 30:
        return numbers[n - 1]
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090[(n // 10) - 2]
        if m > 0:
            ones = numbers[m - 1]
        else:
            ones = ""
        if m in [1, 8]:
            return tens[0:-1] + ones
        elif m == 3:
            return tens + "tré"
        else:
            if twoliner:
                return [tens + "-", ones]
            else:
                return tens + ones
    elif n == 0:
        return "zero"
    elif n == 100:
        return "cento"
    return ""


hrs = ["l'una", 'le due', 'le tre', 'le quattro', 'le cinque', 'le sei', 'le sette', 'le otto', 'le nove', 'le dieci',
       'le undici', 'le dodici']


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m == 0:
        return "%s in punto" % hrs[h - 1]
    elif m == 1:
        return "%s e un minuto" % hrs[h - 1]
    else:
        return "%s e %s" % (hrs[h - 1], n2txt(m))

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
# https://github.com/gcompris/GCompris-qt/blob/master/src/activities/lang/resource/content-it.json

d["a4a_animals"] = ['la mucca', '<turkey>', 'il gambero', '<wolf>', '<panther>', '<panda>', '<magpie>', 'la conchiglia', '<pony>', '<mouse>', '<pug>', '<koala>', 'la rana', '<ladybug>', '<gorilla>', '<llama>', '<vulture>', '<hamster>', "l'uccello", 'la stella di mare', 'il corvo', '<parakeet>', '<caterpillar>', '<tiger>', '<hummingbird>', '<piranha>', 'il maiale', '<scorpion>', 'la volpe', '<leopard>', '<iguana>', '<dolphin>', 'il pipistrello', 'il pulcino', 'il granchio', 'la gallina', '<wasp>', '<chameleon>', '<whale>', '<hedgehog>', '<fawn>', '<moose>', "l'ape", '<viper>', '<shrike>', '<donkey>', '<guinea pig>', '<sloth>', '<horse>', '<penguin>', '<otter>', '<bear>', '<zebra>', '<ostrich>', 'il cammello', '<antelope>', '<lemur>', '<pigeon>', '<lama>', 'la talpa', '<ray>', '<ram>', 'la puzzola', '<jellyfish>', '<sheep>', 'il pescecane', '<kitten>', '<deer>', 'la lumaca', '<flamingo>', '<rabbit>', '<oyster>', '<beaver>', '<sparrow>', '<dove>', '<eagle>', 'lo scarabeo', '<hippopotamus>', 'il gufo', '<cobra>', '<salamander>', '<goose>', '<kangaroo>', '<dragonfly>', '<toad>', '<pelican>', 'il calamaro', '<lion cub>', '<jaguar>', "l'anatra", '<lizard>', '<rhinoceros>', '<hyena>', 'il bue', '<peacock>', '<parrot>', '<elk>', "l'alligatore", '<ant>', 'la capra', '<baby rabbit>', '<lion>', 'lo scoiattolo', '<opossum>', 'la scimmia', '<doe>', '<gopher>', '<elephant>', 'la giraffa', 'il ragno', 'il cucciolo', '<jay>', '<seal>', '<rooster>', '<turtle>', '<bull>', 'il gatto', 'il ratto', '<slug>', '<buffalo>', '<blackbird>', 'il cigno', '<lobster>', 'il cane', 'la zanzara', 'il serpente', 'la gallina', '<anteater>']
d["a4a_sport"] = ['<judo>', 'la piscina', 'andare in bicicletta', '<stretch>', '<helmet>', '<ice skating>', 'camminare', 'corre', 'corre', 'nuotare', '<hop>', '<hike>', '<boxing>', '<hockey>', '<race>', 'lanciare', 'pattinare', '<win>', '<squat>', 'sciare', '<golf>', '<whistle>', 'la torcia', '<sailing>', '<stand>', '<tennis>', 'saltare', '<rowing>', 'correre', 'la corda']
d["a4a_body"] = ['i denti', '<cheek>', '<ankle>', 'il ginocchio', '<toe>', '<muscle>', 'la bocca', '<feet>', 'la mano', '<elbow>', 'i capelli', '<eyelash>', '<beard>', '<belly button>', '<thumb>', '<breast>', '<nostril>', 'il naso', 'i fianchi', '<arm>', '<eyebrow>', 'il pugno', 'il collo', 'il polso', 'la gola', '<eye>', '<leg>', '<spine>', "l'orecchio", '<finger>', 'il piede', 'la treccia', 'la faccia', 'la schiena', 'il mento', '<bottom>', 'la coscia', '<belly>']
d["a4a_people"] = ['la ragazza', '<male>', '<son>', '<mates>', '<friends>', '<baby>', 'il bambino', 'il papà', '<mom>', '<twin boys>', '<brothers>', '<man>', '<mother>', '<grandfather>', '<family>', '<female>', '<wife>', '<husband>', 'la sposa', '<madam>', '<grandmother>', '<couple>', '<lad>', '<twin girls>', '<tribe>', 'il ragazzo', '<sisters>', '<woman>', '<lady>']
d["a4a_food"] = ['la caramella', '<sausage>', '<hamburger>', '<steak>', '<fudge>', '<doughnut>', '<coconut>', 'il riso', '<ice cream>', '<jelly>', '<yoghurt>', '<dessert>', '<pretzel>', '<peanut>', '<jam>', '<feast>', 'i biscotti', '<bacon>', '<spice>', '<coffee>', '<pie>', '<lemonade>', 'il cioccolato', '<water bottle>', 'la merenda', 'il ghiaccio', '<sugar>', 'la salsa', '<soup>', "il succo d'arancia", '<fries>', 'il dolce', '<mashed potatoes>', '<tea>', 'il panino', 'il formaggio', '<beef>', 'il panino', '<slice>', '<sprinkle>', '<pizza>', 'la farina', 'la gomma da masticare', 'gli spaghetti', '<roast>', 'il caffè', 'lo stufato', 'spalmare', '<meat>', '<milk>', '<meal>', 'la pannocchia', 'il pane', '<walnut>', '<egg>', '<hot dog>', '<ham>']
d["a4a_clothes_n_accessories"] = ['<jewellery>', 'il calzino', '<jacket>', '<heel>', '<smock>', '<shorts>', '<pocket>', '<necklace>', '<sweatshirt>', '<uniform>', '<raincoat>', '<trousers>', '<sunglasses>', 'il cappotto', '<pullover>', 'la camicia', '<sandals>', "l'abito", '<pyjamas>', 'la gonna', '<zip>', '<shoes>', 'il gioiello', '<tie>', '<slippers>', '<gloves>', 'il cappello', 'la manica', 'il cappellino', '<swimming suit>', '<trainer>', '<vest>', '<glasses>', '<shoelace>', 'la toppa', 'la sciarpa', 'la scarpa', '<button>', 'il vestito', '<sash>', '<shoe sole>', '<robe>', '<pants>', '<kimono>', '<overalls>']
d["a4a_actions"] = ['leccare', '<slam>', 'pregare', '<fell>', '<scratch>', 'toccare', 'annusare', 'vedere', '<climb>', 'scavare', 'ululare', 'dormire', '<explore>', 'disegnare', 'abbracciare', 'insegnare', 'pisolare', "l'argilla", 'pescare', '<clap>', 'piangere', 'cantare', 'incontrare', '<sell>', 'beccare', '<beat>', '<kneel>', 'trovare', '<dance>', '<cough>', 'tagliare', 'pensare', 'abbaiare', '<speak>', '<cheer>', '<bake>', '<write>', '<punch>', '<strum>', 'studiare', 'dissodare', 'sognare', '<post>', '<dive>', 'sussurrare', '<sob>', '<shake>', '<feed>', 'gattonare', '<camp>', '<spill>', '<clean>', 'urlare', 'strappare', 'galleggiare', '<pull>', '<ate>', '<kiss>', 'sedere', 'schiudere', '<blink>', 'ascoltare', '<smooch>', 'giocare', '<wash>', 'bisbigliare', 'guida', 'il caffè', 'volare', '<juggle>', 'il bocconcino', '<sweep>', 'guardare', 'lavorare ai ferri', 'sollevare i pesi', 'riportare', 'leggere', 'gracidare', 'lo sguardo', 'mangiare']
d["a4a_construction"] = ['<lighthouse>', 'la porta', '<circus>', '<church>', '<kennel>', '<temple>', 'il fumo', '<chimney>', 'i mattoni', '<well>', 'la via', 'il castello', 'il negozio', '<staircase>', 'la scuola', 'la fattoria', 'il ponte', '<dam>', '<pyramid>', 'il fienile', '<mill>', '<window>', '<cabin>', '<step>', 'il negozio', '<shed>', 'il tetto', '<steeple>', '<garage>', '<mosque>', '<hospital>', '<tent>', '<house>', '<wall>', 'la banca', '<shutter>', 'la capanna']
d["a4a_nature"] = ['la terra', 'il burrone', '<hill>', '<canyon>', 'la roccia', '<sea>', 'il lago', '<coast>', 'il bagnasciuga', '<mountain>', '<pond>', '<peak>', '<lava>', 'la grotta', 'la duna', '<island>', '<forest>', '<desert>', '<iceberg>']
d["a4a_jobs"] = ['il pagliaccio', '<engineer>', '<priest>', 'il veterinario', 'il giudice', '<chef>', "l'atleta", '<librarian>', '<juggler>', '<policeman>', '<plumber>', 'la medaglia', 'la regina', '<farmer>', '<magician>', 'il cavaliere', '<doctor>', '<bricklayer>', '<cleaner>', 'la maestra', 'il cacciatore', '<soldier>', '<musician>', '<lawyer>', '<fisherman>', 'la principessa', '<fireman>', '<nun>', '<pirate>', 'il cowboy', '<electrician>', '<nurse>', '<king>', '<president>', '<office worker>', '<carpenter>', '<jockey>', '<worker>', '<mechanic>', '<pilot>', '<actor>', 'cucinare', '<student>', '<butcher>', '<accountant>', 'il principe', 'il papa', '<sailor>', '<boxer>', '<ballet dancer>', "l'allenatrice", '<astronaut>', '<painter>', '<anaesthesiologist>', '<scientist>']
d["a4a_fruit_n_veg"] = ['la carota', '<blackberries>', '<celery>', '<turnip>', '<cacao>', 'la pesca', '<melon>', '<grapefruit>', '<broccoli>', '<grapes>', '<spinach>', '<fig>', '<kernel>', '<radish>', '<tomato>', '<kiwi>', '<asparagus>', '<olives>', '<cucumbers>', '<beans>', 'la fragola', '<peppers>', '<raspberry>', '<apricot>', '<potatoes>', '<peas>', '<cabbage>', '<cherries>', 'la zucca', '<blueberries>', '<pear>', "l'arancio", '<pumpkin>', '<avocado>', '<garlic>', '<onion>', '<apple>', 'il lime', '<cauliflower>', '<mango>', '<lettuce>', '<lemon>', '<aubergine>', '<artichokes>', '<plums>', '<leek>', '<bananas>', '<papaya>']
d["a4a_transport"] = ['la vela', '<taxi>', "l'automobile", 'la bicicletta', '<raft>', '<pedal>', '<bus>', '<handlebar>', 'la barca', 'il camion', 'la slitta', '<carpet>', '<motorcycle>', 'il treno', 'la nave', '<van>', 'la canoa', '<rocket>', '<mast>', '<sledge>', '<bicycle>']
