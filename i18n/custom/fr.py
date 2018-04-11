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

# how to selling french numbers: http://www.logilangue.com/public/Site/clicGrammaire/Nombres.php
# numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty one', 'twenty two', 'twenty three', 'twenty four', 'twenty five', 'twenty six', 'twenty seven', 'twenty eight', 'twenty nine']
# numbers2090 = ['twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
# 'une' is only for hours/minutes -gender female- otherwise, it's 'un' -gender male-.
numbers = ['un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
           'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf', 'vingt', 'vingt-et-un', 'vingt-deux',
           'vingt-trois', 'vingt-quatre', 'vingt-cinq', 'vingt-six', 'vingt-sept', 'vingt-huit', 'vingt-neuf']

hrs = ['une', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
       'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf', 'vingt', 'vingt-et-une', 'vingt-deux',
       'vingt-trois', 'vingt-quatre', 'vingt-cinq', 'vingt-six', 'vingt-sept', 'vingt-huit', 'vingt-neuf']

numbers2090 = ['vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante-dix', 'quatre-vingt',
               'quatre-vingt-dix']

dp['abc_flashcards_word_sequence'] = ['Arbre', 'Bateau', 'Canard', 'Dormir', 'Éléphant', 'Fleurs', 'Girafe', 'Hibou',
                                      'Iglou', 'Jonquille', 'Koala', 'Lion', 'Maison', 'Nuitée', 'Océan', 'Pomme',
                                      'Quille', 'Raisin', 'Soleil', 'Tomate', 'Univers', 'Violon', 'Wagon', 'Xylophone',
                                      'Yoga', 'Zèbre']
d['abc_flashcards_word_sequence'] = ['<1>A<2>rbre', '<1>B<2>ateau', '<1>C<2>anard', '<1>D<2>ormir',
                                     '<1>É<2>l<1>é<2>phant', '<1>F<2>leurs', '<1>G<2>irafe', '<1>H<2>ibou',
                                     '<1>I<2>glou', '<1>J<2>onquille', '<1>K<2>oala', '<1>L<2>ion', '<1>M<2>aison',
                                     '<1>N<2>uitée', '<1>O<2>céan', '<1>P<2>omme', '<1>Q<2>uille', '<1>R<2>aisin',
                                     '<1>S<2>oleil', '<1>T<2>oma<1>t<2>e', '<1>U<2>nivers', '<1>V<2>iolon',
                                     '<1>W<2>agon', '<1>X<2>ylophone', '<1>Y<2>oga', '<1>Z<2>èbre']
d['abc_flashcards_frame_sequence'] = [31, 1, 3, 49, 4, 36, 30, 14, 8, 69, 72, 11, 7, 54, 52, 42, 64, 6, 18, 33, 55, 21,
                                      58, 23, 32, 25]

# alphabet - fr - "aàâæbcçdeéèêëfghiîïjklmnoôœpqrstuùûüvwxyÿz"
alphabet_lc = ['a', 'à', 'â', 'æ', 'b', 'c', 'ç', 'd', 'e', 'é', 'è', 'ê', 'ë', 'f', 'g', 'h', 'i', 'î', 'ï', 'j', 'k',
               'l', 'm', 'n', 'o', 'ô', 'œ', 'p', 'q', 'r', 's', 't', 'u', 'ù', 'û', 'ü', 'v', 'w', 'x', 'y', 'ÿ', 'z']
alphabet_uc = ['A', 'À', 'Â', 'Æ', 'B', 'C', 'Ç', 'D', 'E', 'É', 'È', 'Ê', 'Ë', 'F', 'G', 'H', 'I', 'Î', 'Ï', 'J', 'K',
               'L', 'M', 'N', 'O', 'Ô', 'Œ', 'P', 'Q', 'R', 'S', 'T', 'U', 'Ù', 'Û', 'Ü', 'V', 'W', 'X', 'Y', 'Ÿ', 'Z']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-']
accents_uc = []


def n2txt(n, twoliner=False, time2txt=False):
    """takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."""
    if 0 < n < 30:
        if time2txt:
            return hrs[n - 1]
        else:
            return numbers[n - 1]
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090[(n // 10) - 2]
        if m == 0:
            return tens
        elif m > 0:
            if time2txt:
                ones = hrs[m - 1]
            else:
                ones = numbers[m - 1]

            if twoliner:
                return [tens, ones]
            else:
                return tens + "-" + ones

    elif n == 0:
        return "zero"
    elif n == 100:
        return "cent"
    return ""


def time2str(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55"""
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        if h == 1:
            return "%s heure" % hrs[h - 1]
        else:
            return "%s heures" % hrs[h - 1]
    elif m == 1:
        if h == 1:
            return "%s heure et une minute" % hrs[h - 1]
        else:
            return "%s heures et une minute" % hrs[h - 1]
    elif m == 15:
        if h == 1:
            return "%s heure et quart" % hrs[h - 1]
        else:
            return "%s heures et quart" % hrs[h - 1]
    elif m == 30:
        if h == 1:
            return "%s heure et demie" % hrs[h - 1]
        else:
            return "%s heures et demie" % hrs[h - 1]
    elif m == 45:
        if h == 1:
            return "%s heure moins le quart" % hrs[h - 1]
        else:
            return "%s heures moins le quart" % hrs[h - 1]
    elif m == 59:
        if h == 1:
            return "%s heure moins une minute" % hrs[h - 1]
        else:
            return "%s heures moins une minute" % hrs[h - 1]
    elif m < 30:
        if h == 1:
            return "%s heure et %s minutes" % (hrs[h - 1], n2txt(m, time2txt=True))
        else:
            return "%s heures et %s minutes" % (hrs[h - 1], n2txt(m, time2txt=True))
    elif m > 30:
        if h == 1:
            return "%s heure moins %s minutes" % (hrs[h - 1], n2txt(60 - m, time2txt=True))
        else:
            return "%s heures moins %s minutes" % (hrs[h - 1], n2txt(60 - m, time2txt=True))
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

# d["a4a_animals"] = ["cow", "turkey", "shrimp", "wolf", "panther", "panda", "magpie", "clam", "pony", "mouse", "pug", "koala", "frog", "ladybug", "gorilla", "llama", "vulture", "hamster", "bird", "starfish", "crow", "parakeet", "caterpillar", "tiger", "hummingbird", "piranha", "pig", "scorpion", "fox", "leopard", "iguana", "dolphin", "bat", "chick", "crab", "hen", "wasp", "chameleon", "whale", "hedgehog", "fawn", "moose", "bee", "viper", "shrike", "donkey", "guinea pig", "sloth", "horse", "penguin", "otter", "bear", "zebra", "ostrich", "camel", "antelope", "lemur", "pigeon", "lama", "mole", "ray", "ram", "skunk", "jellyfish", "sheep", "shark", "kitten", "deer", "snail", "flamingo", "rabbit", "oyster", "beaver", "sparrow", "dove", "eagle", "beetle", "hippopotamus", "owl", "cobra", "salamander", "goose", "kangaroo", "dragonfly", "toad", "pelican", "squid", "lion cub", "jaguar", "duck", "lizard", "rhinoceros", "hyena", "ox", "peacock", "parrot", "elk", "alligator", "ant", "goat", "baby rabbit", "lion", "squirrel", "opossum", "chimp", "doe", "gopher", "elephant", "giraffe", "spider", "puppy", "jay", "seal", "rooster", "turtle", "bull", "cat", "rat", "slug", "buffalo", "blackbird", "swan", "lobster", "dog", "mosquito", "snake", "chicken", "anteater"]
d["a4a_animals"] = ["vache", "dinde", "crevettes", "loup", "panthère", "panda", "pie", "palourde", "poney", "souris",
                    "carlin", "koala", "grenouille", "coccinelle", "gorille", "lama", "vautour", "hamster", "oiseau",
                    "étoile de mer", "corbeau", "perruche", "chenille", "tigre", "colibri", "piranha", "cochon",
                    "scorpion", "renard", "léopard", "iguane", "dauphin", "chauve-souris", "poussin", "crabe", "poule",
                    "guêpe", "caméléon", "baleine", "hérisson", "fauve", "élan", "abeille", "vipère", "passereaux",
                    "âne", "cochon d'inde", "paresseux", "cheval", "pingouin", "loutre", "ours", "zèbre", "autruche",
                    "chameau", "antilope", "lémurien", "pigeon", "lama", "taupe", "raie", "bélier", "putois", "méduse",
                    "mouton", "requin", "chaton", "cerf", "escargot", "flamant rose", "lapin", "huître", "castor",
                    "moineau", "colombe", "aigle", "coléoptère", "hippopotame", "hibou", "cobra", "salamandre", "oie",
                    "kangourou", "libellule", "crapaud", "pélican", "calamar", "lionceau", "jaguar", "canard", "lézard",
                    "rhinocéros", "hyène", "boeuf", "paon", "perroquet", "wapiti", "alligator", "fourmi", "chèvre",
                    "petit lapin", "lion", "écureuil", "marsupial", "chimpanzé", "daim", "gaufre", "éléphant", "girafe",
                    "araignée", "chiot", "geai", "phoque", "coq", "tortue", "taureau", "chat", "rat",
                    "limace", "buffle", "merle", "cygne", "homard", "chien", "moustique", "serpent", "poulet",
                    "tamanoir"]
# d["a4a_sport"] = ["judo", "pool", "ride", "stretch", "helmet", "ice skating", "walk", "ran", "run", "swim", "hop", "hike", "boxing", "hockey", "race", "throw", "skate", "win", "squat", "ski", "golf", "whistle", "torch", "sailing", "stand", "tennis", "jump", "rowing", "jog", "rope"]
d["a4a_sport"] = ["judo", "piscine", "vélo", "étirements", "casque", "patinage", "marche", "courrir", "course", "nager",
                  "sauter", "randonnée", "boxe", "hockey", "course", "javelot", "skate", "gagner", "squat", "ski",
                  "golf", "sifflet", "torche", "voile", "stand", "tennis", "saut", "aviron", "jogging", "corde"]
# d["a4a_body"] = ["teeth", "cheek", "ankle", "knee", "toe", "muscle", "mouth", "feet", "hand", "elbow", "hair", "eyelash", "beard", "belly button", "thumb", "breast", "nostril", "nose", "hip", "arm", "eyebrow", "fist", "neck", "wrist", "throat", "eye", "leg", "spine", "ear", "finger", "foot", "braid", "face", "back", "chin", "bottom", "thigh", "belly"]
d["a4a_body"] = ["dents", "joues", "cheville", "genou", "orteil", "muscle", "bouche", "pieds", "main", "coude",
                 "cheveux", "cils", "barbe", "nombril", "pouce", "poitrine", "narine", "nez", "hanche", "bras",
                 "sourcils", "poing", "cou", "poignet", "gorge", "oeil", "jambe", "colonne vertébrale", "oreille",
                 "doigt", "pied", "tresse", "visage", "dos", "menton", "bas", "cuisse", "ventre"]

# check me for: "lad:garçon"
# d["a4a_people"] = ["girl", "male", "son", "mates", "friends", "baby", "child", "dad", "mom", "twin boys", "brothers", "man", "mother", "grandfather", "family", "female", "wife", "husband", "bride", "madam", "grandmother", "couple", "lad", "twin girls", "tribe", "boy", "sisters", "woman", "lady"]
d["a4a_people"] = ["fille", "male", "fils", "écoliers", "amis", "bébé", "enfant", "papa", "maman", "jumeaux", "frères",
                   "homme", "mère", "grand-père", "famille", "femelle", "femme", "mari", "mariée", "madame",
                   "grand-mère", "couple", "garçon", "jumelles", "tribu", "garçon", "soeurs", "femme", "dame"]

# check me for: "fudge:fondant", "spread:tartiner"
# d["a4a_food"] = ["candy", "sausage", "hamburger", "steak", "fudge", "doughnut", "coconut", "rice", "ice cream", "jelly", "yoghurt", "dessert", "pretzel", "peanut", "jam", "feast", "cookie", "bacon", "spice", "coffee", "pie", "lemonade", "chocolate", "water bottle", "lunch", "ice", "sugar", "sauce", "soup", "juice", "fries", "cake", "mashed potatoes", "tea", "bun", "cheese", "beef", "sandwich", "slice", "sprinkle", "pizza", "flour", "gum", "spaghetti", "roast", "drink", "stew", "spread", "meat", "milk", "meal", "corn", "bread", "walnut", "egg", "hot dog", "ham"]
d["a4a_food"] = ["bonbons", "saucisse", "hamburger", "steak", "fondant", "beignet", "noix de coco", "riz",
                 "crème glacée", "gelée", "yaourt", "dessert", "bretzel", "cacahuète", "confiture", "fête", "cookie",
                 "bacon", "épice", "café", "tarte", "limonade", "chocolat", "bouteille d'eau", "déjeuner", "glace",
                 "sucre", "sauce", "soupe", "jus", "frites", "gâteau", "purée de pomme de terre", "thé", "bon",
                 "fromage", "boeuf", "sandwich", "tranche", "saupoudrer", "pizza", "farine", "gomme", "spaghetti",
                 "rôti", "boire", "ragoût", "tartiner", "viande", "lait", "repas", "maïs", "pain", "noix", "oeuf",
                 "hot dog", "jambon"]

# check me for: "trainer:survêtement"
# d["a4a_clothes_n_accessories"] = ["jewellery", "sock", "jacket", "heel", "smock", "shorts", "pocket", "necklace", "sweatshirt", "uniform", "raincoat", "trousers", "sunglasses", "coat", "pullover", "shirt", "sandals", "suit", "pyjamas", "skirt", "zip", "shoes", "jewel", "tie", "slippers", "gloves", "hat", "sleeve", "cap", "swimming suit", "trainer", "vest", "glasses", "shoelace", "patch", "scarf", "shoe", "button", "dress", "sash", "shoe sole", "robe", "pants", "kimono", "overalls"]
d["a4a_clothes_n_accessories"] = ["bijoux", "chaussette", "veste", "talon", "blouse", "short", "poche", "collier",
                                  "sweat", "uniforme", "imperméable", "pantalon", "lunettes de soleil", "manteau",
                                  "pull", "chemise", "sandales", "costume", "pyjama", "jupe", "braguette", "chaussures",
                                  "bijou", "cravate", "chaussons", "gants", "chapeau", "manche", "cap",
                                  "maillot de bain", "survêtement", "gilet", "lunettes", "lacet", "retouche", "foulard",
                                  "chaussure", "bouton", " robe", "ceinture", "chaussure a semelle", "robe", "pantalon",
                                  "kimono", "salopette"]

# check me for: "slam:viser","dig:creuser","nap:dormir","clay:façonner","strum:jouer","sob:souffrir","bit:ronger","fetch:rapporter","stare:impressioner"
# d["a4a_actions"] = ["lick", "slam", "beg", "fell", "scratch", "touch", "sniff", "see", "climb", "dig", "howl", "sleep", "explore", "draw", "hug", "teach", "nap", "clay", "catch", "clap", "cry", "sing", "meet", "sell", "peck", "beat", "kneel", "find", "dance", "cough", "cut", "think", "bark", "speak", "cheer", "bake", "write", "punch", "strum", "study", "plow", "dream", "post", "dive", "whisper", "sob", "shake", "feed", "crawl", "camp", "spill", "clean", "scream", "tear", "float", "pull", "ate", "kiss", "sit", "hatch", "blink", "hear", "smooch", "play", "wash", "chat", "drive", "drink", "fly", "juggle", "bit", "sweep", "look", "knit", "lift", "fetch", "read", "croak", "stare", "eat"]
d["a4a_actions"] = ["lécher", "viser", "mendier", "tomber", "griffer", "toucher", "sentir", "voir", "grimper",
                    "creuser", "hurler", "dormir", "explorer", "dessiner", "serrer", "enseigner", "dormir", "façonner",
                    "capturer", "taper", "pleurer", "chanter", "rencontrer", "vendre", "picorer", "heurter",
                    "s'agenouiller", "trouver", "danser", "tousser", "couper", "penser", "aboyer", "parler",
                    "encourager", "cuisiner", "écrire", "frapper", "jouer", "étudier", "labourer", "rêver", "poster",
                    "plonger", "chuchoter", "souffrir", "secouer", "nourrir", "ramper", "camper", "renverser",
                    "nettoyer", "crier", "déchirer", "flotter", "tirer", "manger", "embrasser", "s'asseoir", "éclore",
                    " clignoter", "entendre", "embrasser", "jouer", "laver", "discuter", "conduire", "boire", "voler",
                    "jongler", "ronger", "balayer", "regarder", "tricoter", "soulever", "rapporter", "lire", "croasser",
                    "impressioner", "manger"]

# d["a4a_construction"] = ["lighthouse", "door", "circus", "church", "kennel", "temple", "smoke", "chimney", "brick", "well", "street", "castle", "store", "staircase", "school", "farm", "bridge", "dam", "pyramid", "barn", "mill", "window", "cabin", "step", "shop", "shed", "roof", "steeple", "garage", "mosque", "hospital", "tent", "house", "wall", "bank", "shutter", "hut"]
d["a4a_construction"] = ["phare", "porte", "cirque", "église", "chenil", "temple", "fumée", "cheminée", "brique",
                         "puits", "rue", "château", "magasin", "escalier", "école", "ferme", "pont", "barrage",
                         "pyramide", "grange", "moulin", "fenêtre", "cabine", "étape", "boutique", "hangar", "toit",
                         "clocher", "garage", "mosquée", "hôpital", "tente", "maison", "mur", "banque", "volet",
                         "cabane"]
# d["a4a_nature"] = ["land", "cliff", "hill", "canyon", "rock", "sea", "lake", "coast", "shore", "mountain", "pond", "peak", "lava", "cave", "dune", "island", "forest", "desert", "iceberg"]
d["a4a_nature"] = ["terre", "falaise", "colline", "canyon", "rocher", "mer", "lac", "côte", "rivage", "montagne",
                   "étang", "pic", "lave", "grotte", "dune", "île", "forêt", "désert", "iceberg"]
# d["a4a_jobs"] = ["clown", "engineer", "priest", "vet", "judge", "chef", "athlete", "librarian", "juggler", "police", "plumber", "badge", "queen", "farmer", "magic", "knight", "doctor", "bricklayer", "cleaner", "teacher", "hunter", "soldier", "musician", "lawyer", "fisherman", "princess", "fireman", "nun", "pirate", "cowboy", "electrician", "nurse", "king", "president", "office", "carpenter", "jockey", "worker", "mechanic", "pilot", "actor", "cook", "student", "butcher", "accountant", "prince", "pope", "sailor", "boxer", "ballet", "coach", "astronaut", "painter", "anaesthesiologist", "scientist"]
d["a4a_jobs"] = ["clown", "ingénieur", "prêtre", "vétérinaire", "juge", "chef", "athlète", "libraire", "jongleur",
                 "police", "plombier", "insigne", "reine", "agriculteur", "magie", "chevalier", "docteur", "maçon",
                 "nettoyeur", "enseignant", "chasseur", "soldat", "musicien", "avocat", "pêcheur", "princesse",
                 "pompier", "nounou", "pirate", "cowboy", "électricien", "infirmière", "roi", "président",
                 "bureau", "charpentier", "jockey", "travailleur", "mécanicien", "pilote", "acteur", "cuisinier",
                 "étudiant", "boucher", "comptable", "prince", "pape", "marin", "boxeur", "ballet", "coach",
                 "astronaute", "peintre", "anesthésiste", "scientifique"]
# d["a4a_fruit_n_veg"] = ["carrot", "blackberries", "celery", "turnip", "cacao", "peach", "melon", "grapefruit", "broccoli", "grapes", "spinach", "fig", "kernel", "radish", "tomato", "kiwi", "asparagus", "olives", "cucumbers", "beans", "strawberry", "peppers", "raspberry", "apricot", "potatoes", "peas", "cabbage", "cherries", "squash", "blueberries", "pear", "orange", "pumpkin", "avocado", "garlic", "onion", "apple", "lime", "cauliflower", "mango", "lettuce", "lemon", "aubergine", "artichokes", "plums", "leek", "bananas", "papaya"]
d["a4a_fruit_n_veg"] = ["carotte", "mûres", "céleri", "navet", "cacao", "pêche", "melon", "pamplemousse", "brocoli",
                        "raisin", "épinards", "figue", "noyau", "radis", "tomate", "kiwi", "asperges", "olives",
                        "concombres", "haricots", "fraise", "poivrons", "framboise", "abricot", "pommes de terre",
                        "pois", "chou", "cerises", "courge", "myrtille", "poire", "orange", "citrouille", "avocat",
                        "ail", "oignon", "pomme", "citon vert", "chou-fleur", "mangue", "laitue", "citron", "aubergine",
                        "artichauts", "prunes", "poireau", "bananes", "papaye"]
# d["a4a_transport"] = ["sail", "taxi", "car", "bike", "raft", "pedal", "bus", "handlebar", "boat", "truck", "sleigh", "carpet", "motorcycle", "train", "ship", "van", "canoe", "rocket", "mast", "sledge", "bicycle"]
d["a4a_transport"] = ["voile", "taxi", "voiture", "vélo", "radeau", "pédale", "bus", "guidon", "bateau", "camion",
                      "traîneau", "tapis", "moto", "train", "navire", "fourgonette", "canot", "fusée", "mât", "luge",
                      "bicyclette"]
