# -*- coding: utf-8 -*-

alphabet_lc = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
               'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я']
alphabet_uc = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
               'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ь', 'Ю', 'Я']

en_list = ["ant", "boat", "cat", "duck", "elephant", "fish", "grapes", "house", "igloo", "honey", "key", "lion", "mouse", "notebook", "owl", "parrot", "queen", "rabbit", "sun", "teapot", "umbrella", "violin", "window", "xylophone", "wool", "zebra", "watermelon", "butterfly", "guitar", "hedgehog", "giraffe", "tree", "yoga", "tomato", "piano", "bread", "flowers", "chimpanzee", "pike", "photographer", "screen", "skirt", "apple", "nophoto", "moth", "horse", "tree", "hippopotam", "clothes", "sleep", "truck", "clock", "ocean", "street", "night", "space", "hamack", "cheese", "wagon", "dolphin", "shoes", "snail", "colt", "train", "bowling pin", "tiger", "sail", "cooker", "hockey", "daffodil", "gnu", "banana", "koala", "yoghurt", "kiwi", "eye", "leopard", "bus", "flower", "mobile", "roll", "water", "beach", "note", "drink", "usher", "button", "lemur", "nostrills", "swing", "turkey", "sack", "nail", "dummy", "student", "paint", "mountain", "rock", "four", "acorn", "three", "juice", "iron"]

trans_list = ["мравка", "лодка", "котка", "патица", "слон", "риба", "грозде", "къща", "иглу", "мед", "ключ", "лъв", "мишка", "тетрадка", "бухал", "папагал", "царица", "заек", "слънце", "чайник", "чадър", "цигулка", "прозорец", "ксилофон", "вълна", "зебра", "диня", "пеперуда", "китара", "таралеж", "жираф", "дърво", "йога", "домат", "пиано", "хляб", "цветя", "шимпанзе", "щука", "фотограф", "екран", "пола", "ябълка", "нофото", "молец", "кон", "дърво", "хипопотам", "дрехи", "сън", "камион", "часовник", "океан", "улица", "нощ", "космически", "хамак", "сирене", "вагон", "делфин", "обувки", "охлюв", "жребче", "влак", "боулинг пин", "тигър", "платно", "печка", "хокей", "нарцис", "гну", "банан", "коала", "кисело мляко", "киви", "око", "леопард", "автобус", "цвете", "мобилен", "рол", "вода", "плаж", "бележка", "питие", "usher", "button", "лемур", "ноздри", "люлка", "пуйка", "чувал", "нокът", "сляпо", "студент", "боя", "планина", "рок", "четири", "жълъд", "три", "сок", "Ютия"]
print(len(en_list))
print(len(trans_list))
"""
words_with_trans = True
# Find all words starting with a particular letter and print all
if not words_with_trans:
    for i in range(len(alphabet_lc)):
        found = False
        words = ""
        for each in trans_list:
            if alphabet_lc[i] == each[0]:
                s = alphabet_uc[i] + each[1:]
                words += "'" + s + "', "
                found = True
        if not found:
            words = "'" + alphabet_uc[i] + "', "
        print(words)

    # print translations separately
    trans = []
    for i in range(len(en_list)):
        trans.append(en_list[i] + ": " + trans_list[i])
    print(trans)
else:
    for i in range(len(alphabet_lc)):
        found = False
        words = ""
        for j in range(len(trans_list)):
            if alphabet_lc[i] == trans_list[j][0]:
                s = alphabet_uc[i] + trans_list[j][1:]
                words += "'" + s + "' (" + en_list[j] + ") " + "(" + str(j) + ")" + ", "
                found = True
        if not found:
            words = "'" + alphabet_uc[i] + "', "
        print(words)
"""

# create list with colour markup
lst = ['Автобус', 'Бухал', 'Влак', 'Грозде', 'Дърво', 'Екран', 'Жираф', 'Зебра', 'Иглу', 'Йога', 'Котка', 'Лодка', 'Мравка', 'Нарцис', 'Око', 'Патица', 'Риба', 'Слон', 'Тигър', 'Улица', 'Фотограф', 'Хляб', 'Цветя', 'Чайник', 'Шимпанзе', 'Щука', 'Лъв', 'Шофьор', 'Ютия', 'Ябълка']
lst2 = []
for each in lst:
    s = "<1>" + each[0] + "<2>" + each[1:]
    lst2.append(s)

print(lst2)
"""
['<1>А<2>втобус', '<1>Б<2>ухал', '<1>В<2>лак', '<1>Г<2>розде', '<1>Д<2>ърво', '<1>Е<2>кран', '<1>Ж<2>ираф', '<1>З<2>ебра', '<1>И<2>глу', '<1>Й<2>ога', '<1>К<2>отка', '<1>Л<2>одка', '<1>М<2>равка', '<1>Н<2>арцис', '<1>О<2>ко', '<1>П<2>атица', '<1>Р<2>иба', '<1>С<2>лон', '<1>Т<2>игър', '<1>У<2>лица', '<1>Ф<2>отограф', '<1>Х<2>ляб', '<1>Ц<2>ветя', '<1>Ч<2>айник', '<1>Ш<2>импанзе', '<1>Щ<2>ука', '<1>Л<2>ъв', '<1>Ш<2>офьор', '<1>Ю<2>тия', '<1>Я<2>бълка']

"""
# Results copied over from the terminal and best matches selected
"""
'Автобус' (bus) (77), 
'Бухал' (owl) (14),
'Влак' (train) (63), 
'Грозде' (grapes) (6), 
'Дърво' (tree) (46), 
'Екран' (screen) (40), 
'Жираф' (giraffe) (30), 
'Зебра' (zebra) (25), 
'Иглу' (igloo) (8), 
'Йога' (yoga) (32), 
'Котка' (cat) (2),  
'Лодка' (boat) (1),  
'Мравка' (ant) (0),
'Нарцис' (daffodil) (69), 
'Око' (eye) (75), 
'Патица' (duck) (3), 
'Риба' (fish) (5), 
'Слон' (elephant) (4),  
'Тигър' (tiger) (65), 
'Улица' (street) (53), 
'Фотограф' (photographer) (39), 
'Хляб' (bread) (35), 
'Цветя' (flowers) (36),
'Чайник' (teapot) (19),
'Шимпанзе' (chimpanzee) (37), 
'Щука' (pike) (38), 
'Ъ' 'Лъв' (lion) (11),
'Ь', 'Шофьор' (driver) (103),
'Ю', 'Ютия' (iron) (102),
'Ябълка' (apple) (42), 

'Автобус', 
'Бухал',
'Влак', 
'Грозде', 
'Дърво', 
'Екран', 
'Жираф', 
'Зебра', 
'Иглу', 
'Йога', 
'Котка',  
'Лодка',  
'Мравка',
'Нарцис', 
'Око', 
'Патица', 
'Риба', 
'Слон',  
'Тигър', 
'Улица', 
'Фотограф', 
'Хляб', 
'Цветя',
'Чайник',
'Шимпанзе', 
'Щука', 
'Лъв',
'Шофьор',
'Ютия',
'Ябълка', 
"""