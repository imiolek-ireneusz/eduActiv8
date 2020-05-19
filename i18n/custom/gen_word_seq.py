# -*- coding: utf-8 -*-

alphabet_lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']

en_list = ["ant", "boat", "cat", "duck", "elephant", "fish", "grapes", "house", "igloo", "honey", "key", "lion", "mouse", "notebook", "owl", "parrot", "queen", "rabbit", "sun", "teapot", "umbrella", "violin", "window", "xylophone", "wool", "zebra", "watermelon", "butterfly", "guitar", "hedgehog", "giraffe", "tree", "yoga", "tomato", "piano", "bread", "flowers", "chimpanzee", "pike", "photographer", "screen", "skirt", "apple", "nophoto", "moth", "horse", "tree", "hippopotam", "clothes", "sleep", "truck", "clock", "ocean", "street", "night", "space", "hamack", "cheese", "wagon", "dolphin", "shoes", "snail", "colt", "train", "bowling pin", "tiger", "sail", "cooker", "hockey", "daffodil", "gnu", "banana", "koala", "yoghurt", "kiwi", "eye", "leopard", "bus", "flower", "mobile", "roll", "water", "beach", "note", "drink", "usher", "button", "lemur", "nostrills", "swing", "turkey", "sack", "nail", "dummy", "student", "paint", "mountain", "rock", "four", "acorn", "three", "juice", "iron"]

trans_list = ["мравка", "лодка", "котка", "патица", "слон", "риба", "грозде", "къща", "иглу", "мед", "ключ", "лъв", "мишка", "тетрадка", "бухал", "папагал", "царица", "заек", "слънце", "чайник", "чадър", "цигулка", "прозорец", "ксилофон", "вълна", "зебра", "диня", "пеперуда", "китара", "таралеж", "жираф", "дърво", "йога", "домат", "пиано", "хляб", "цветя", "шимпанзе", "щука", "фотограф", "екран", "пола", "ябълка", "нофото", "молец", "кон", "дърво", "хипопотам", "дрехи", "сън", "камион", "часовник", "океан", "улица", "нощ", "космически", "хамак", "сирене", "вагон", "делфин", "обувки", "охлюв", "жребче", "влак", "боулинг пин", "тигър", "платно", "печка", "хокей", "нарцис", "гну", "банан", "коала", "кисело мляко", "киви", "око", "леопард", "автобус", "цвете", "мобилен", "рол", "вода", "плаж", "бележка", "питие", "usher", "button", "лемур", "ноздри", "люлка", "пуйка", "чувал", "нокът", "сляпо", "студент", "боя", "планина", "рок", "четири", "жълъд", "три", "сок", "Ютия"]
#print(len(en_list))
#print(len(trans_list))
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
#lst = ['Автобус', 'Бухал', 'Влак', 'Грозде', 'Дърво', 'Екран', 'Жираф', 'Зебра', 'Иглу', 'Йога', 'Котка', 'Лодка', 'Мравка', 'Нарцис', 'Око', 'Патица', 'Риба', 'Слон', 'Тигър', 'Улица', 'Фотограф', 'Хляб', 'Цветя', 'Чайник', 'Шимпанзе', 'Щука', 'Лъв', 'Шофьор', 'Ютия', 'Ябълка']
lst = ['Appel', 'Bus', 'Chimpansee', 'Dolfijn', 'Egel', 'Fortepiano', 'Gitaar', 'Huis', 'Iglo', 'Joga', 'Kat', 'Leeuw', 'Muis', 'Nijlpaard', 'Olifant', 'Papegaai', 'Q', 'Rots', 'Slak', 'Tomaat',  'Uil', 'Viool', 'Water', 'Xylofoon', 'Yoghurt', 'Zebra']
lst2 = []
for each in lst:
    s = "<1>" + each[0] + "<2>" + each[1:]
    lst2.append(s)

print(lst2)
"""
['<1>A<2>ppel', '<1>B<2>us', '<1>C<2>himpansee', '<1>D<2>olfijn', '<1>E<2>gel', '<1>F<2>ortepiano', '<1>G<2>itaar', '<1>H<2>uis', '<1>I<2>glo', '<1>J<2>oga', '<1>K<2>at', '<1>L<2>eeuw', '<1>M<2>uis', '<1>N<2>ijlpaard', '<1>O<2>lifant', '<1>P<2>apegaai', '<1>Q<2>', '<1>R<2>ots', '<1>S<2>lak', '<1>T<2>omaat', '<1>U<2>il', '<1>V<2>iool', '<1>W<2>ater', '<1>X<2>ylofoon', '<1>Y<2>oghurt', '<1>Z<2>ebra']

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