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

d["a4a_animals"] = ["cow", "turkey", "shrimp", "wolf", "panther", "panda", "magpie", "clam", "pony", "mouse", "pug",
                    "koala", "frog", "ladybug", "gorilla", "llama", "vulture", "hamster", "bird", "starfish", "crow",
                    "parakeet", "caterpillar", "tiger", "hummingbird", "piranha", "pig", "scorpion", "fox", "leopard",
                    "iguana", "dolphin", "bat", "chick", "crab", "hen", "wasp", "chameleon", "whale", "hedgehog",
                    "fawn", "moose", "bee", "viper", "shrike", "donkey", "guinea pig", "sloth", "horse", "penguin",
                    "otter", "bear", "zebra", "ostrich", "camel", "antelope", "lemur", "pigeon", "lama", "mole", "ray",
                    "ram", "skunk", "jellyfish", "sheep", "shark", "kitten", "deer", "snail", "flamingo", "rabbit",
                    "oyster", "beaver", "sparrow", "dove", "eagle", "beetle", "hippopotamus", "owl", "cobra",
                    "salamander", "goose", "kangaroo", "dragonfly", "toad", "pelican", "squid", "lion cub", "jaguar",
                    "duck", "lizard", "rhinoceros", "hyena", "ox", "peacock", "parrot", "elk", "alligator", "ant",
                    "goat", "baby rabbit", "lion", "squirrel", "opossum", "chimp", "doe", "gopher", "elephant",
                    "giraffe", "spider", "puppy", "jay", "seal", "rooster", "turtle", "bull", "cat", "rat",
                    "slug", "buffalo", "blackbird", "swan", "lobster", "dog", "mosquito", "snake", "chicken",
                    "anteater"]
d["a4a_sport"] = ["judo", "pool", "ride", "stretch", "helmet", "ice skating", "walk", "ran", "run", "swim", "hop",
                  "hike", "boxing", "hockey", "race", "throw", "skate", "win", "squat", "ski", "golf", "whistle",
                  "torch", "sailing", "stand", "tennis", "jump", "rowing", "jog", "rope"]
d["a4a_body"] = ["teeth", "cheek", "ankle", "knee", "toe", "muscle", "mouth", "feet", "hand", "elbow", "hair",
                 "eyelash", "beard", "belly button", "thumb", "breast", "nostril", "nose", "hip", "arm", "eyebrow",
                 "fist", "neck", "wrist", "throat", "eye", "leg", "spine", "ear", "finger", "foot", "braid", "face",
                 "back", "chin", "bottom", "thigh", "belly"]
d["a4a_people"] = ["girl", "male", "son", "mates", "friends", "baby", "child", "dad", "mom", "twin boys", "brothers",
                   "man", "mother", "grandfather", "family", "female", "wife", "husband", "bride", "madam",
                   "grandmother", "couple", "lad", "twin girls", "tribe", "boy", "sisters", "woman", "lady"]
d["a4a_food"] = ["candy", "sausage", "hamburger", "steak", "fudge", "doughnut", "coconut", "rice", "ice cream", "jelly",
                 "yoghurt", "dessert", "pretzel", "peanut", "jam", "feast", "cookie", "bacon", "spice", "coffee", "pie",
                 "lemonade", "chocolate", "water bottle", "lunch", "ice", "sugar", "sauce", "soup", "juice", "fries",
                 "cake", "mashed potatoes", "tea", "bun", "cheese", "beef", "sandwich", "slice", "sprinkle", "pizza",
                 "flour", "gum", "spaghetti", "roast", "drink", "stew", "spread", "meat", "milk", "meal", "corn",
                 "bread", "walnut", "egg", "hot dog", "ham"]
d["a4a_clothes_n_accessories"] = ["jewellery", "sock", "jacket", "heel", "smock", "shorts", "pocket", "necklace",
                                  "sweatshirt", "uniform", "raincoat", "trousers", "sunglasses", "coat", "pullover",
                                  "shirt", "sandals", "suit", "pyjamas", "skirt", "zip", "shoes", "jewel", "tie",
                                  "slippers", "gloves", "hat", "sleeve", "cap", "swimming suit", "trainer", "vest",
                                  "glasses", "shoelace", "patch", "scarf", "shoe", "button", "dress", "sash",
                                  "shoe sole", "robe", "pants", "kimono", "overalls"]
d["a4a_actions"] = ["lick", "slam", "beg", "fell", "scratch", "touch", "sniff", "see", "climb", "dig", "howl", "sleep",
                    "explore", "draw", "hug", "teach", "nap", "clay", "catch", "clap", "cry", "sing", "meet", "sell",
                    "peck", "beat", "kneel", "find", "dance", "cough", "cut", "think", "bark", "speak", "cheer", "bake",
                    "write", "punch", "strum", "study", "plow", "dream", "post", "dive", "whisper", "sob", "shake",
                    "feed", "crawl", "camp", "spill", "clean", "scream", "tear", "float", "pull", "ate", "kiss", "sit",
                    "hatch", "blink", "hear", "smooch", "play", "wash", "chat", "drive", "drink", "fly", "juggle",
                    "bit", "sweep", "look", "knit", "lift", "fetch", "read", "croak", "stare", "eat"]
d["a4a_construction"] = ["lighthouse", "door", "circus", "church", "kennel", "temple", "smoke", "chimney", "brick",
                         "well", "street", "castle", "store", "staircase", "school", "farm", "bridge", "dam", "pyramid",
                         "barn", "mill", "window", "cabin", "step", "shop", "shed", "roof", "steeple", "garage",
                         "mosque", "hospital", "tent", "house", "wall", "bank", "shutter", "hut"]
d["a4a_nature"] = ["land", "cliff", "hill", "canyon", "rock", "sea", "lake", "coast", "shore", "mountain", "pond",
                   "peak", "lava", "cave", "dune", "island", "forest", "desert", "iceberg"]
d["a4a_jobs"] = ["clown", "engineer", "priest", "vet", "judge", "chef", "athlete", "librarian", "juggler", "police",
                 "plumber", "badge", "queen", "farmer", "magic", "knight", "doctor", "bricklayer", "cleaner", "teacher",
                 "hunter", "soldier", "musician", "lawyer", "fisherman", "princess", "fireman", "nun",
                 "pirate", "cowboy", "electrician", "nurse", "king", "president", "office", "carpenter", "jockey",
                 "worker", "mechanic", "pilot", "actor", "cook", "student", "butcher", "accountant", "prince", "pope",
                 "sailor", "boxer", "ballet", "coach", "astronaut", "painter", "anaesthesiologist", "scientist"]
d["a4a_fruit_n_veg"] = ["carrot", "blackberries", "celery", "turnip", "cacao", "peach", "melon", "grapefruit",
                        "broccoli", "grapes", "spinach", "fig", "kernel", "radish", "tomato", "kiwi", "asparagus",
                        "olives", "cucumbers", "beans", "strawberry", "peppers", "raspberry", "apricot", "potatoes",
                        "peas", "cabbage", "cherries", "squash", "blueberries", "pear", "orange", "pumpkin", "avocado",
                        "garlic", "onion", "apple", "lime", "cauliflower", "mango", "lettuce", "lemon", "aubergine",
                        "artichokes", "plums", "leek", "bananas", "papaya"]
d["a4a_transport"] = ["sail", "taxi", "car", "bike", "raft", "pedal", "bus", "handlebar", "boat", "truck", "sleigh",
                      "carpet", "motorcycle", "train", "ship", "van", "canoe", "rocket", "mast", "sledge", "bicycle"]
