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

# d["a4a_animals"] = ["cow", "turkey", "shrimp", "wolf", "panther", "panda", "magpie", "clam", "pony", "mouse", "pug", "koala", "frog", "ladybug", "gorilla", "llama", "vulture", "hamster", "bird", "starfish", "crow", "parakeet", "caterpillar", "tiger", "hummingbird", "piranha", "pig", "scorpion", "fox", "leopard", "iguana", "dolphin", "bat", "chick", "crab", "hen", "wasp", "chameleon", "whale", "hedgehog", "fawn", "moose", "bee", "viper", "shrike", "donkey", "guinea pig", "sloth", "horse", "penguin", "otter", "bear", "zebra", "ostrich", "camel", "antelope", "lemur", "pigeon", "lama", "mole", "ray", "ram", "skunk", "jellyfish", "sheep", "shark", "kitten", "deer", "snail", "flamingo", "rabbit", "oyster", "beaver", "sparrow", "dove", "eagle", "beetle", "hippopotamus", "owl", "cobra", "salamander", "goose", "kangaroo", "dragonfly", "toad", "pelican", "squid", "lion cub", "jaguar", "duck", "lizard", "rhinoceros", "hyena", "ox", "peacock", "parrot", "elk", "alligator", "ant", "goat", "baby rabbit", "lion", "squirrel", "opossum", "chimp", "doe", "gopher", "elephant", "giraffe", "spider", "puppy", "jay", "seal", "rooster", "turtle", "bull", "cat", "rat", "slug", "buffalo", "blackbird", "swan", "lobster", "dog", "mosquito", "snake", "chicken", "anteater"]
d["a4a_animals"] = ['krowa', 'indyk', 'krewetka', 'wilk', 'pantera', 'panda', 'sroka', 'małż', 'kucyk', 'mysz', 'pies',
                    'koala', 'żaba', 'biedronka', 'goryl', 'lama', 'sęp', 'chomik', 'ptak', 'rozgwiazda', 'kruk',
                    'papuga', 'gąsienica', 'tygrysek', 'koliber', 'pirania', 'świnia', 'skorpion', 'lis', 'lampart',
                    'iguana', 'delfin', 'nietoperz', 'kurczątko', 'krab', 'kura', 'osa', 'kameleon', 'wieloryb', 'jeż',
                    'jelonek', 'łoś', 'pszczoła', 'żmija', 'dzierzba', 'osioł', 'świnka morska', 'leniwiec', 'koń',
                    'pingwin', 'wydra', 'niedźwiedź', 'zebra', 'struś', 'wielbłąd', 'antylopa', 'lemur', 'gołąb',
                    'lama', 'kret', 'płaszczka', 'baran', 'skunks', 'meduza', 'owca', 'rekin', 'kot', 'jeleń', 'ślimak',
                    'fleming', 'królik', 'ostryga', 'bóbr', 'wróbel', 'gołąb', 'orzeł', 'chrząszcz', 'hipopotam',
                    'sowa', 'kobra', 'salamandra', 'gęś', 'kangur', 'ważka', 'ropucha', 'pelikan', 'kalmar', 'lwiątko',
                    'jaguar', 'kaczka', 'jaszczurka', 'nosorożec', 'hiena', 'wół', 'paw', 'papuga', 'łoś', 'aligator',
                    'mrówka', 'koza', 'króliczek', 'lew', 'wiewiórka', 'opos', 'szympans', 'sarenka', 'gopher', 'słoń',
                    'żyrafa', 'pająk', 'szczeniak', 'sójka', 'foka', 'kogut', 'żółw', 'byk', 'kot', 'szczur',
                    'ślimak', 'bawół', 'kos', 'łabędź', 'homar', 'pies', 'komar', 'wąż', 'kurczak', 'mrówkojad']

# d["a4a_sport"] = ["judo", "pool", "ride", "stretch", "helmet", "ice skating", "walk", "ran", "run", "swim", "hop", "hike", "boxing", "hockey", "race", "throw", "skate", "win", "squat", "ski", "golf", "whistle", "torch", "sailing", "stand", "tennis", "jump", "rowing", "jog", "rope"]
d["a4a_sport"] = ["judo", "basen", "jazda na rowerze", "rozciąganie", "kask", "łyżwy", "spacer", "bieg", "bieg",
                  "pływanie", "skakanie na trampolinie", "wędrówka", "boks", "hokej", "wyścig", "rzucać",
                  "jazda na deskorolce", "wygrywać", "przysiady", "narciarstwo", "golf", "gwizdek", "pochodnia",
                  "żeglarstwo", "stanie", "tenis", "skok", "wioślarstwo", "bieg", "skakanka"]

# d["a4a_body"] = ["teeth", "cheek", "ankle", "knee", "toe", "muscle", "mouth", "feet", "hand", "elbow", "hair", "eyelash", "beard", "belly button", "thumb", "breast", "nostril", "nose", "hip", "arm", "eyebrow", "fist", "neck", "wrist", "throat", "eye", "leg", "spine", "ear", "finger", "foot", "braid", "face", "back", "chin", "bottom", "thigh", "belly"]
d["a4a_body"] = ["zęby", "policzek", "kostka", "kolano", "palec u nogi", "mięsień", "usta", "stopy", "dłoń", "łokieć",
                 "włosy", "rzęsy", "broda", "pępek", "kciuk", "piersi", "dziórka w nosie", "nos", "biodro", "ręka",
                 "brwi", "pięść", "szyja", "nadgarstek", "gardło ", "oko", "noga", "kręgosłup", "ucho", "palec",
                 "stopa", "warkocz", "twarz", "plecy", "podbródek", "tyłek", "udo", "brzuch"]

# d["a4a_people"] = ["girl", "male", "son", "mates", "friends", "baby", "child", "dad", "mom", "twin boys", "brothers", "man", "mother", "grandfather", "family", "female", "wife", "husband", "bride", "madam", "grandmother", "couple", "lad", "twin girls", "tribe", "boy", "sisters", "woman", "lady"]
d["a4a_people"] = ["dziewczyna", "chłopiec", "syn", "koledzy", "przyjaciele", "niemowle", "dziecko", "tata", "mama",
                   "bliźnięta", "bracia", "mężczyzna", "matka", "dziadek", "rodzina", "dziewczyna", "żona", "mąż",
                   "panna młoda", "pani", "babcia", "para", "chłopak", "bliźniaczki", "plemię", "chłopak", "siostry",
                   "kobieta", "pani"]

# d["a4a_food"] = ["candy", "sausage", "hamburger", "steak", "fudge", "doughnut", "coconut", "rice", "ice cream", "jelly", "yoghurt", "dessert", "pretzel", "peanut", "jam", "feast", "cookie", "bacon", "spice", "coffee", "pie", "lemonade", "chocolate", "water bottle", "lunch", "ice", "sugar", "sauce", "soup", "juice", "fries", "cake", "mashed potatoes", "tea", "bun", "cheese", "beef", "sandwich", "slice", "sprinkle", "pizza", "flour", "gum", "spaghetti", "roast", "drink", "stew", "spread", "meat", "milk", "meal", "corn", "bread", "walnut", "egg", "hot dog", "ham"]
d["a4a_food"] = ["słodycze", "kiełbasa", "hamburger", "stek", "krówka", "pączek", "kokos", "ryż", "lód", "galaretka",
                 "jogurt", "deser", "precel", "orzeszek ziemny", "dżem", "uczta", "ciasteczko", "boczek", "przyprawy",
                 "kawa", "ciasto", "lemoniada", "czekolada", "butelka wody", "lunch", "lód", "cukier", "sos", "zupa",
                 "soki", "frytki", "ciasto", "ziemniaki puree", "herbata", "drożdżówka", "ser", "wołowina", "kanapka",
                 "plasterki", "posypka", "pizza", "mąka", "guma do żucia", "spaghetti", "pieczeń", "napój", "gulasz",
                 "smarować", "mięso ", "mleko", "objad", "kukurydza", "chleb", "orzech włoski", "jajko", "hot dog",
                 "szynka"]

# d["a4a_clothes_n_accessories"] = ["jewellery", "sock", "jacket", "heel", "smock", "shorts", "pocket", "necklace", "sweatshirt", "uniform", "raincoat", "trousers", "sunglasses", "coat", "pullover", "shirt", "sandals", "suit", "pyjamas", "skirt", "zip", "shoes", "jewel", "tie", "slippers", "gloves", "hat", "sleeve", "cap", "swimming suit", "sneaker", "vest", "glasses", "shoelace", "patch", "scarf", "shoe", "button", "dress", "sash", "shoe sole", "robe", "pants", "kimono", "overalls"]
d["a4a_clothes_n_accessories"] = ["biżuteria", "skarpetka", "kurtka", "obcas", "kitel", "spodenki", "kieszeń",
                                  "naszyjnik", "bluza", "mundur", "płaszcz przeciwdeszczowy", "spodnie",
                                  "okulary przeciwsłoneczne", "płaszcz", "sweter", "koszula", "sandały", "garnitur",
                                  "piżama", "spódnica", "zamek błyskawiczny", "buty", "klejnot", "krawat", "pantofle",
                                  "rękawiczki", "kapelusz", "rękaw", "czapka", "kostium pływacki", "but sportowy",
                                  "kamizelka", "okulary", "sznurówki", "łata", "szalik", "buty", "guzik", "sukienka",
                                  "szarfa", "podeszwa buta", "szata", "spodnie", "kimono", "kombinezon"]

# d["a4a_actions"] = ["lick", "slam", "beg", "fell", "scratch", "touch", "sniff", "see", "climb", "dig", "howl", "sleep", "explore", "draw", "hug", "teach", "nap", "clay", "catch", "clap", "cry", "sing", "meet", "sell", "peck", "beat", "kneel", "find", "dance", "cough", "cut", "think", "bark", "speak", "cheer", "bake", "write", "punch", "strum", "study", "plow", "dream", "post", "dive", "whisper", "sob", "shake", "feed", "crawl", "camp", "spill", "clean", "scream", "tear", "float", "pull", "ate", "kiss", "sit", "hatch", "blink", "hear", "smooch", "play", "wash", "chat", "drive", "drink", "fly", "juggle", "bit", "sweep", "look", "knit", "lift", "fetch", "read", "croak", "stare", "eat"]
d["a4a_actions"] = ["lizać", "rzucać", "żebrać", "spadać", "drapać", "dotykać", "wąchać", "patrzeć", "wspinać się",
                    "kopać", "wyć", "spać", "zwiedzać", "rysować", "przytulić", "uczyć się", "drzemać", "lepić z gliny",
                    "złowić", "klepnąć", "płakać", "śpiewać", "spotkać", "sprzedać", "dziobać", "oberwać", "uklęknąć",
                    "znaleźć", "tańczyć", "kaszleć", "uciąć", "myśleć", "szczekać", "mówić", "dopingować", "piec",
                    "pisać", "uderzyć", "brzdąkać", "uczyć się", "orać", "marzyć", "wysyłać", "nurkować", "szeptać",
                    "szlochać", "potrząsnąć", "nakarmić", "raczkować", "biwakować", "rozlać", "myć się", "krzyczeć",
                    "rozerwać", "unosić się", "ciągnąć", "zjeść", "pocałować", "siedzieć", "wykluwać się",
                    "puścić oczko", "słyszeć", "pocałować", "bawić się", "kąpać się", "rozmawiać", "jeździć", "pić",
                    "latać", "żonglować", "ugryźć", "zamiatać", "patrzeć", "robić na drutach", "podnieść", "przynieść",
                    "czytać", "rechotać", "gapić się", "jeść"]

# d["a4a_construction"] = ["lighthouse", "door", "circus", "church", "kennel", "temple", "smoke", "chimney", "brick", "well", "street", "castle", "store", "staircase", "school", "farm", "bridge", "dam", "pyramid", "barn", "mill", "window", "cabin", "step", "shop", "shed", "roof", "steeple", "garage", "mosque", "hospital", "tent", "house", "wall", "bank", "shutter", "hut"]
d["a4a_construction"] = ["latarnia morska", "drzwi", "cyrk", "kościół", "buda", "świątynia", "dym", "komin", "cegła",
                         "studnia", "ulica", "zamek", "sklep", "schody", "szkoła", "gospodarstwo", "most", "tama",
                         "piramida", "stodoła", "młyn", "okno", "szopa", "schód", "sklep", "szopa", "dach", "wieża",
                         "garaż", "meczet", "szpital", "namiot", "dom", "ściana", "bank", "okiennica", "szałas"]

# d["a4a_nature"] = ["land", "cliff", "hill", "canyon", "rock", "sea", "lake", "coast", "shore", "mountain", "pond", "peak", "lava", "cave", "dune", "island", "forest", "desert", "iceberg"]
d["a4a_nature"] = ["ziemia", "klif", "wzgórze", "kanion", "skała", "morze", "jezioro", "wybrzeże", "plaża", "góra",
                   "staw", "szczyt", "lawa", "jaskinia", "wydma", "wyspa", "las", "pustynia", "góra lodowa"]

# d["a4a_jobs"] = ["clown", "engineer", "priest", "vet", "judge", "chef", "athlete", "librarian", "juggler", "police", "plumber", "badge", "queen", "farmer", "magic", "knight", "doctor", "bricklayer", "cleaner", "teacher", "hunter", "soldier", "musician", "lawyer", "fisherman", "princess", "fireman", "nun", "pirate", "cowboy", "electrician", "nurse", "king", "president", "office", "carpenter", "jockey", "worker", "mechanic", "pilot", "actor", "cook", "student", "butcher", "accountant", "prince", "pope", "sailor", "boxer", "ballet", "coach", "astronaut", "painter", "anaesthesiologist", "scientist"]
d["a4a_jobs"] = ['klaun', 'inżynier', 'ksiądz', 'weterynarz', 'sędzia', 'szef kuchni', 'sportowiec', 'bibliotekarz',
                 'żongler', 'policjant', 'hydraulik', 'medal', 'królowa', 'rolnik', 'magia', 'rycerz', 'lekarz',
                 'murarz', 'sprzątaczka', 'nauczyciel', 'myśliwy', 'żołnierz', 'muzyk', 'prawnik', 'wędkarz',
                 'księżniczka', 'strażak', 'zakonnica', 'pirat', 'kowboj', 'elektryk', 'pielęgniarka', 'król',
                 'prezydent', 'pracownik biurowy', 'stolarz', 'dżokej', 'pracownik', 'mechanik', 'pilot', 'aktor', 'kucharz',
                 'student', 'rzeźnik', 'księgowy', 'książę', 'papież', 'marynarz', 'bokser', 'baletnica', 'trener',
                 'astronauta', 'malarz', 'anestezjolog', 'naukowiec']

# d["a4a_fruit_n_veg"] = ["carrot", "blackberries", "celery", "turnip", "cacao", "peach", "melon", "grapefruit", "broccoli", "grapes", "spinach", "fig", "kernel", "radish", "tomato", "kiwi", "asparagus", "olives", "cucumbers", "beans", "strawberry", "peppers", "raspberry", "apricot", "potatoes", "peas", "cabbage", "cherries", "squash", "blueberries", "pear", "orange", "pumpkin", "avocado", "garlic", "onion", "apple", "lime", "cauliflower", "mango", "lettuce", "lemon", "aubergine", "artichokes", "plums", "leek", "bananas", "papaya"]
d["a4a_fruit_n_veg"] = ["marchew", "jeżyny", "seler", "rzepa", "kakao", "brzoskwinia", "melon", "grejpfrut", "brokuła",
                        "winogrona", "szpinak", "figa", "pestka", "rzodkiewka", "pomidor", "kiwi", "szparagi", "oliwki",
                        "ogórki", "fasola", "truskawka", "papryka", "malina", "morela", "ziemniaki", "groszek",
                        "kapusta", "wiśnie", "dynia", "jagody", "gruszka", "pomarańcza", "dynia", "awokado", "czosnek",
                        "cebula", "jabłko", "limonka", "kalafior", "mango", "sałata", "cytryna", "bakłażan",
                        "karczochy", "śliwki", "pora", "banany", "papaja"]

# d["a4a_transport"] = ["sail", "taxi", "car", "bike", "raft", "pedal", "bus", "handlebar", "boat", "truck", "sleigh", "carpet", "motorcycle", "train", "ship", "van", "canoe", "rocket", "mast", "sledge", "bicycle"]
d["a4a_transport"] = ["żagiel", "taksówka", "samochód", "rower", "tratwa", "pedał", "autobus", "kierownica", "łódź",
                      "ciężarówka", "sanie", "latający dywan", "motocykl", "pociąg", "statek", "van", "kajak",
                      "rakieta", "maszt", "sanki", "rower"]
