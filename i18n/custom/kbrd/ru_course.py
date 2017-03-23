# -*- coding: utf-8 -*-


from classes.extras import get_word_list, word_typing_course
from i18n.custom.kbrd.ru_cinderella import cinderella
from i18n.custom.word_lists.ru_di import di

# course = [[[1],["a"]]]
course = []

ru_course = [

    # lvl1 - learning home keys фыва олдж
    [[3, 3, 3, 3, 3, 3],
     ["фыва авыф ", "олдж ждло ", "фыва олдж ждло авыф ", "фоылвдаж жадвлыоф ", "фжыдвлао аовлыдфж ",
      "фводыалж жлаыдовф "]
     ],

    # lvl2 - adding п, р, э - фывап ролджэ
    [[3, 3, 3, 3, 3, 3],
     ["фывап павыф ", "ролджэ эждлор ", "фывап ролджэ эждлор павыф ", "фрыовладпжэ эжпдалвоырф ",
      "фжыдвлаопр рпоалвдыжф ", "фвпрлж ыаодэ "]
     ],

    # lvl3 - training left hand - learning letters - йцуке
    [[4, 4, 5, 3, 3, 3, 3, 3, 3, 3, 3],
     ["ака аеа ", "фйф ыцы вув ака аеа ", "йфцыувкаеп пеаквуыцфй ", "йфувепцыка акыцпевуфй ", "фыцуыв уквакеап ",
      "паекавку выуцыф ", "фцвкп еауый ", "йыуае пквцф ", "фкйа айкф ", "фуац цауф ", "уфкыцвуа аувцыкфу "]
     ],

    # lvl4 - learning letters - нгшщзхъ
    [[4, 3, 3, 3, 3, 3],
     ["оно ого ", "оно ого лшл дщд жзж жхж жъж ", "лшгол дщшлд жзщдж эхзжэ ", "ъхэжзщжд щшдлшглогнор ",
      "ъэхжзд щлшогрн  рноглш дщжзэхъ ", "нршлзж гощдхэъ ъэхжзд щлшогрн "]
     ],

    # lvl5 - learning letters - zxcvb - ячсми
    [[4, 4, 4, 3, 3],
     ["аиа ама ", "аиа ама всв ычы фяф ", "фцвч ыуас вкпм ", "фяы ычв вса амп ", "фяычвсами имасвчыяф "]
     ],

    # lvl5 - learning letters - тьбюё
    [[4, 4, 4, 3, 3, 3],
     ["ото оьо ", "ото оьо лбл дюд ", "отьл лбюд дюж ", "трьо блюд ", "отьо льбл дбюд ", "фйф фёф "]
     ],

    # lvl6 - learning uppercase letters
    [[3, 3, 3],
     ["Фы Ыв Ва Ап Пр Ро Ол Лд Дж Жэ Ээ ", "Йф Цы Ув Ка Еа Но Го Шл Щд Зж Хж Ъж ", "Яф Чы Св Ма Иа То Ьо Бл Юд "]
     ],

    # lvl7 - learning position of , . ? !
    [[2, 2],
     ["ж.ж Ж,Ж ", "да? да! да, да. "]
     ],

    # lvl8 - quick home keys revision
    [[2, 2],
     ["фёфйфяф ыцычы вувсв акаеамаиапа ", "оноготоьоро лшлбл дщдюд жзж.ж жхжъжэж "]
     ]
]
course.extend(ru_course)

# add Language specific word list - words taken from ru_di.py file.
word_list = get_word_list(di)
word_course = word_typing_course(word_list)
course.extend(word_course)
course.extend(cinderella)
