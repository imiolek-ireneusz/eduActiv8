# -*- coding: utf-8 -*-

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The colour names in other languages than English are already in smaller font.

import sys

from classes.extras import reverse
from classes.extras import unival

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

# alphabet he
alphabet_lc = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
               'ת']
alphabet_uc = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
               'ת']

# correction of eSpeak pronounciation of single letters if needed
# the following is an example how I'd replace pronunciation of single letters in abc games.
# Please correct the following letter names - I got them wrong
letter_names = ["[[aalEf]]", "[[bEit]]", "[[gimEl]]", "[[daled]]", "[[he]]", "[[vav]]", "za'yin", "[[khet]]", "[[tet]]",
                "[[iud]]", "[[khaf]]", "[[lamed]]", "[[mem]]", "[[nun]]", "[[samekh]", "[[ain]]", "[[pe]]", "[[tsadik]",
                "[[kuf]]", "[[reish]]", "[[Cin]]", "[[taf]]"]

# alpha = "אבגדהוזחטיךכלםמןנסעףפץצקרשתװױײ׳״"
# alpha = "אבּבגדהוזחטיכּכךּךלמםנןסעפּפףצץקרשׁשׂתּתװױײ׳״"
alpha = "אבּבגדהוזחטיכּכךּךלמםנןסעפּפףצץקרשׁשׂתּתװױײ׳״"
alpha += ",.;:?-!"


def r(s):
    return reverse(s, alpha, "he")


numbers = ['אחד', 'שתיים', 'שלוש', 'ארבע', 'חמש', 'שש', 'שבע', 'שמונה', 'תשע', 'עשר', 'אחד עשרה', 'שתים עשרה',
           'שלוש-עשרה', 'ארבע-עשרה', 'חמש-עשרה', 'שש-עשרה', 'שבע-עשרה', 'שמונה-עשרה', 'תשע-עשרה', 'עשרים', 'עשרים ואחת',
           'עשרים ושתים', 'עשרים ושלוש', 'עשרים וארבע', 'עשרים וחמש', 'עשרים ושש', 'עשרים ושבע', 'עשרים ושמונה',
           'עשרים ותשע']
numbers2090 = ['עשרים', 'שלושים', 'ארבעים', 'חמישים', 'שישים', 'שבעים', 'שמונים', 'תשעים']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
# d['abc_flashcards_word_sequence'] = ['אבטיח', 'בננה', 'גיטרה', 'Dolphin', 'Elephant', 'Fortepiano', 'Guitar', 'Hedgehog', 'Igloo', 'Jar', 'Koala', 'Lion', 'Monitor', 'Notebook', 'Ocean', 'Parrot', 'Queen', 'Rabbit', 'Street', 'Tomato', 'Umbrella', 'Violin', 'Watermelon', 'Xylophone', 'Yarn', 'Zebra']
# d['abc_flashcards_word_sequence'] = [r("אבטיח"), r("בננה"), r("גיטרה"), r("דולפין"), r("היפופוטם"), r("ורד"), r("זברה"), r("חלזון"), r("טלפון"), r("ינשוף"), r("כינור"), r("לחם"), r("מסך"), r("נעליים"), r("סירה"), r("עין"), r("פרח"), r("צליל"), r("קוף"), r("רכבת"), r("שעון"), r("תפוח")]
d['abc_flashcards_word_sequence'] = ["אבטיח", "בננה", "גיטרה", "דולפין", "היפופוטם", "ורד", "זברה", "חלזון", "טלפון",
                                     "ינשוף", "כינור", "לחם", "מסך", "נעליים", "סירה", "עין", "פרח", "צליל", "קוף",
                                     "רכבת", "שעון", "תפוח"]
d['abc_flashcards_word_sequencer'] = [r("אבטיח"), r("בננה"), r("גיטרה"), r("דולפין"), r("היפופוטם"), r("ורד"),
                                      r("זברה"), r("חלזון"), r("טלפון"), r("ינשוף"), r("כינור"), r("לחם"), r("מסך"),
                                      r("נעליים"), r("סירה"), r("עין"), r("פרח"), r("צליל"), r("קוף"), r("רכבת"),
                                      r("שעון"), r("תפוח")]

d['abc_flashcards_frame_sequence'] = [26, 71, 28, 59, 47, 78, 25, 61, 79, 14, 21, 35, 40, 60, 1, 75, 69, 83, 37, 63, 51,
                                      42]

# letter_names = []

accents_lc = ['-']
accents_uc = []


def n2txt(n, twoliner=False):
    "takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."
    if 0 < n < 30:
        return r(numbers[n - 1])
    elif 30 <= n < 100:
        m = n % 10
        tens = r(numbers2090[(n // 10) - 2])
        if m == 0:
            return tens
        elif m > 0:
            ones = r(numbers[m - 1])
            if twoliner:
                return [tens, ones]
            else:
                return ones + " " + tens

    elif n == 0:
        return r("אפס")
    elif n == 100:
        return r("מאה")
    else:
        return ""


# phonetic transcription - number to spoken number
# TODO - implement the use of the following function
# numbers in left to right order in phonetic transcription
numbersp = ["[[ekhad]]", "[[Ctaim]]", "[[CaloC]]", "[[arba]]", "[[khameC]]", "[[CeC]]", "[[Ceva]]", "[[Cmone]]'",
            "[[teCa]]", "[[eser]]", "[[ekhad esre]]", "[[Cteim esre]]", "[[CloC esre]]", "[[arba esre]]",
            "[[khameC esre]]", "[[CeC esre]]", "[[Cva esre]]", "[[Cmone esre]]", "[[tCa esre]]", "[[esrim]]",
            "[[esrim ve ekhad]]", "[[esrim ve Ctaim]]", "[[esrim ve CaloC]]", "[[esrim ve arba]]",
            "[[esrim ve khameC]]", "[[esrim ve CeC]]", "[[esrim ve Ceva]]", "[[esrim ve Cmone]]", "[[esrim ve teCa]]"]
numbers2090p = ["[[esrim]]", "[[CloCim]]", "[[arbaim]]", "[[khamiCim]]", "[[CiCim]]", "[[Civim]]", "[[Cmonim]]",
                "[[tiCim]]"]


def n2spk(n, twoliner=False):
    "takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."
    if 0 < n < 30:
        return numbersp[n - 1]
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090p[(n // 10) - 2]
        if m == 0:
            return tens
        elif m > 0:
            ones = numbersp[m - 1]
            return tens + " " + ones

    elif n == 0:
        return "אפס"
    elif n == 100:
        return "מאה"
    else:
        return ""


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    # if sys.version_info < (3, 0):
    if sys.version_info[0] < 3:
        if m == 0:
            return unival(n2txt(h))
        elif m == 1:
            return r(unicode(" דקה אחרי", "utf-8")) + n2txt(h)
        elif m == 15:
            return r(unicode(" רבע אחרי", "utf-8")) + n2txt(h)
        elif m == 30:
            return r(unicode("חצי אחרי ", "utf-8")) + n2txt(h)
        elif m == 45:
            return r(unicode("רבע ל ", "utf-8")) + n2txt(h)
        elif m == 59:
            return r(unicode("דקה ל ", "utf-8")) + n2txt(h)
        elif m < 30:
            return n2txt(m) + r(unicode(" אחרי ", "utf-8")) + n2txt(h)
        elif m > 30:
            return n2txt(60 - m) + r(unicode(" ל ", "utf-8")) + n2txt(h)
        return ""
    else:
        if m == 0:
            return n2txt(h)
        elif m == 1:
            return r(" דקה אחרי") + n2txt(h)
        elif m == 15:
            return r(" רבע אחרי") + n2txt(h)
        elif m == 30:
            return r("חצי אחרי ") + n2txt(h)
        elif m == 45:
            return r("רבע ל ") + n2txt(h)
        elif m == 59:
            return r("דקה ל ") + n2txt(h)
        elif m < 30:
            return n2txt(m) + r(" אחרי ") + n2txt(h)
        elif m > 30:
            return n2txt(60 - m) + r(" ל ") + n2txt(h)
        return ""


def time2spk(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55
    but this time in Latin letters for espeak so it can to read it phonetically"""
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return n2spk(h)
    elif m == 1:
        return n2spk(h) + " [[daka akhrei]]"
    elif m == 15:
        return n2spk(h) + " [[reva akhrei]]"
    elif m == 30:
        return n2spk(h) + " [[khetsi akhrei]] "
    elif m == 45:
        return n2spk(h) + " [[reva akhrei]] "
    elif m == 59:
        return n2spk(h) + " [[daka le]] "
    elif m < 30:
        return n2spk(h) + " [[akhrei]] " + n2spk(m)
    elif m > 30:
        return n2spk(h) + " [[le]] " + n2spk(60 - m)
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

dp["Hebrew"] = "Hebrew"
dp['shape_names'] = ["Equilateral Triangle", "Isosceles Triangle", "Obtuse Triangle", "Right Triangle",
                     "Acute Triangle", "Square", "Rectangle", "Right Trapezium", "Isosceles Trapezium", "Rhombus",
                     "Parallelogram", "Pentagon", "Hexagon", "Circle", "Ellipse"]
dp['solid_names'] = ["Cube", "Square Prism", "Triangular Prism", "Square Pyramid", "Triangular Pyramid", "Sphere",
                     "Cylinder", "Cone", "Torus"]
dp['abc_flashcards_word_sequence'] = ["[[avatiakh]]", "[[banana]]", "[[gitara]]", "[[dolfin]]", "[[hipopotam]]",
                                      "[[vered]]", "[[zebra]]", "[[khilazon]]", "[[telefon]]", "[[ianshuf]]",
                                      "[[kinor]]", "[[lekhem]]", "[[masakh]]", "[[na alaim]]", "[[sira]]", "[[ain]]",
                                      "[[perakh]]", "[[tslil]]", "[[kof]]", "[[rakevet]]", "[[Caon]]", "[[tapuakh]]"]

# game start
dp["Hello"] = "[[Calom]]"
dp["Welcome back."] = "[[brukhim habaim lamiskhak]]"
dp["fruit"] = ["[[tapuakh yarok]]", "[[tapuakh adom]]", "[[tut]]", "[[agas]]", "[[tapuz]]", "[[batsal]]", "[[agvania]]",
               "[[limon]]", "[[duvdevan]]", "[[pilpel]]", "[[gezer]]", "[[banana]]", "[[melon]]"]

dp["Drag the slider"] = "Drag the slider up or down so that the right sign is in the red square."
dp["Check the shopping list"] = "Check the shopping list and drag all needed items into the basket."
dp["Drag lt2"] = "Drag one of the lesser, greater or equal to the red square."
dp["Re-arrange right"] = "Re-arrange the above numbers so they are in the right order"
dp["Complete abc"] = "Complete the abc using the letters above."
dp["Write a word:"] = "Write a word:"
dp["Find and separate"] = "Find and separate the Even Numbers from the Odd Numbers in the above series."
dp["Re-arrange alphabetical"] = "Re-arrange the above letters so they are in the alphabetical order."
dp["Re-arrange ascending"] = "Re-arrange the above numbers so they are in the ascending order."
dp["Build the following word using the letters below."] = "Build the following word using the letters below."
dp["Perfect! Task solved!"] = "Perfect! Task solved!"
dp["work harder"] = "You need to work a little bit harder next time."

dp["Game Over!"] = "Game Over!"
dp["Congratulations! Game Completed."] = "Congratulations! You have completed all tasks in this game."
dp["Great job!"] = ["Great job!", "Perfect!", "Awesome!", "Fantastic job!", "Well done!"]
dp["Perfect! Level completed!"] = "Perfect! Level completed!"
dp["Perfect!"] = "Perfect"  # Perfect!

dp["area:"] = "area:"
dp["perimeter:"] = "perimeter:"
dp["circumference:"] = "circumference"
dp["surface area:"] = "surface area:"
dp["volume:"] = "volume:"
dp["divided by"] = "divided by"
dp["multiplied by"] = "times"
dp["equals"] = "equals"
dp["Even"] = "Even"
dp["Odd"] = "Odd"

dp["white"] = "[[lavan]]"
dp["black"] = "[[Cakhor]]"
dp["grey"] = "[[afor]]"
dp["red"] = "[[adom]]"
dp["orange"] = "[[katom]]"
dp["yellow"] = "[[tsahov]]"
dp["olive"] = "[[zait]]"
dp["green"] = "[[iarok]]"
dp["sea green"] = "[[iarok iam]]"
dp["teal"] = "[[tsehavhav]]"
dp["blue"] = "[[kakhol]]"
dp["navy"] = "[[kakhol kehe]]"
dp["purple"] = "[[sagol]]"
dp["violet"] = "[[sagol]]"
dp["magenta"] = "[[magenta]]"
dp["indigo"] = "[[indigo]]"
dp["pink"] = "[[varod]]"
dp["maroon"] = "[[khum armoni]]"
dp["brown"] = "[[khum]]"
dp["aqua"] = "[[akwa]]"
dp["lime"] = "[[sid]]"

dp["more red"] = "[[yoter adom]]"
dp["more green"] = "[[yoter yarok]]"
dp["more blue"] = "[[yoter kakhol]]"
dp["more cyan"] = "[[yoter tsian]]"
dp["more magenta"] = "[[yoter magenta]]"
dp["more yellow"] = "[[yoter tsahov]]"

dp["less red"] = "[[pakhot adom]]"
dp["less green"] = "[[pakhot yarok]]"
dp["less blue"] = "[[pakhot kakhol]]"
dp["less cyan"] = "[[pakhot tsian]]"
dp["less magenta"] = "[[pakhot magenta]]"
dp["less yellow"] = "[[pakhot tsahov]]"

dp["red is ok"] = "[[adom mat'im]]"
dp["green is ok"] = "[[yarok mat'im]]"
dp["blue is ok"] = "[[kakhol mat'im]]"
dp["cyan is ok"] = "[[tsian mat'im]]"
dp["magenta is ok"] = "[[magenta mat'im]]"
dp["yellow is ok"] = "[[tsahov mat'im]]"

dp["Fract instr0"] = "Match fraction charts on the right to the ones on the left"
dp["Fract instr1"] = "Match fraction charts and fractions on the right to the fraction charts on the left"
dp["Fract instr2"] = "Match fraction charts to the fractions on the left"
dp["Fract instr3"] = "Match fraction charts, fractions and decimal fractions on the right to their percentage representations"
dp["Fract instr4"] = "Match charts to the ratios on the left. Ratios are expressed as ratio of coloured pieces to white pieces"

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
