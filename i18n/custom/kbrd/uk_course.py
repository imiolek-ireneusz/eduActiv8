# -*- coding: utf-8 -*-


from classes.extras import get_word_list, word_typing_course
from i18n.custom.kbrd.uk_cinderella import cinderella
from i18n.custom.word_lists.uk_di import di

# course = [[[1],["a"]]]
course = []

uk_course = [

    # lvl1 - learning home keys фіва олдж
    [[3, 3, 3, 3, 3, 3],
     ["фіва авіф ", "олдж ждло ", "фіва олдж ждло авіф ", "фоілвдаж жадвліоф ", "фжідвлао аовлідфж ",
      "фводіалж жлаідовф "]
     ],

    # lvl2 - adding п, р, є - фівап ролджє
    [[3, 3, 3, 3, 3, 3],
     ["фівап павіф ", "ролджє єждлор ", "фівап ролджє єждлор павіф ", "фріовладпжє єжпдалвоірф ",
      "фжідвлаопр рпоалвдіжф ", "фвпрлж іаодє "]
     ],

    # lvl3 - training left hand - learning letters - йцуке
    [[4, 4, 5, 3, 3, 3, 3, 3, 3, 3, 3],
     ["ака аеа ", "фйф іці вув ака аеа ", "йфціувкаеп пеаквуіцфй ", "йфувепціка акіцпевуфй ", "фіцуів уквакеап ",
      "паекавку віуціф ", "фцвкп еауій ", "йіуае пквцф ", "фкйа айкф ", "фуац цауф ", "уфкіцвуа аувцікфу "]
     ],

    # lvl4 - learning letters - нгшщзхї
    [[4, 3, 3, 3, 3, 3],
     ["оно ого ", "оно ого лшл дщд жзж жхж жїж ", "лшгол дщшлд жзщдж єхзжє ", "їхєжзщжд щшдлшглогнор ",
      "їєхжзд щлшогрн  рноглш дщжзєхї ", "нршлзж гощдхєї їєхжзд щлшогрн "]
     ],

    # lvl5 - learning letters - zxcvb - ячсми
    [[4, 4, 4, 3, 3],
     ["аиа ама ", "аиа ама всв ічі фяф ", "фцвч іуас вкпм ", "фяі ічв вса амп ", "фяічвсами имасвчіяф "]
     ],

    # lvl5 - learning letters - тьбюґ
    [[4, 4, 4, 3, 3, 3],
     ["ото оьо ", "ото оьо лбл дюд ", "отьл лбюд дюж ", "трьо блюд ", "отьо льбл дбюд ", "фйф фґф "]
     ],

    # lvl6 - learning uppercase letters
    [[3, 3, 3],
     ["Фі Ыв Ва Ап Пр Ро Ол Лд Дж Жє Эє ", "Йф Ці Ув Ка Еа Но Го Шл Щд Зж Хж Ъж ", "Яф Чі Св Ма Иа То Ьо Бл Юд "]
     ],

    # lvl7 - learning position of , . ? !
    [[2, 2],
     ["ж.ж Ж,Ж ", "да? да! да, да. "]
     ],

    # lvl8 - quick home keys revision
    [[2, 2],
     ["фґфйфяф іцічі вувсв акаеамаиапа ", "оноготоьоро лшлбл дщдюд жзж.ж жхжїжєж "]
     ]
]
course.extend(uk_course)

# add Language specific word list - words taken from uk_di.py file.
word_list = get_word_list(di)
word_course = word_typing_course(word_list)
course.extend(word_course)
course.extend(cinderella)
