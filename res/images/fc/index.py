# -*- coding: utf-8 -*-
""" This file contains all words associated with images in res/images/fc folder.
    It can be used to assist in creation of a list of words starting with each of
    the letters of the alphabet. The list first needs to be translated (ideally automatically)
    and then the resulting list can be sorted to easily pick out the most appropriate word/image pair"""


def stop():
    raise Exception('manual stop')


fc_list = {0: 'Ant', 1: 'Boat', 2: 'Cat', 3: 'Duck', 4: 'Elephant',
           5: 'Fish', 6: 'Grapes', 7: 'House', 8: 'Igloo', 9: 'Jar',
           10: 'Key', 11: 'Lion', 12: 'Mouse', 13: 'Notebook', 14: 'Owl',
           15: 'Parrot', 16: 'Queen', 17: 'Rabbit', 18: 'Sun', 19: 'Teapot',
           20: 'Umbrella', 21: 'Violin', 22: 'Window', 23: 'Xylophone', 24: 'Yarn',
           25: 'Zebra', 26: 'Watermelon', 27: 'Butterfly', 28: 'Guitar', 29: 'Hedgehog',
           30: 'Giraffe', 31: 'Tree', 32: 'Joga', 33: 'Tomato', 34: 'Fortepiano',
           35: 'Bread', 36: 'Flowers', 37: 'Chimpanzee', 38: 'Fish', 39: 'Photographer',
           40: 'Monitor', 41: 'Skirt', 42: 'Apple', 43: 'No-Picture', 44: ' Moth',
           45: 'Horse', 46: 'Tree', 47: 'Hippo', 48: 'Clothes', 49: 'Sleep',
           50: 'Lorry', 51: 'Clock', 52: 'Ocean', 53: 'Street', 54: 'Night',
           55: 'Space', 56: 'Hammack', 57: 'Cheese', 58: 'Wagon', 59: 'Dolphin',
           60: 'Shoes', 61: 'Snail', 62: 'Foal', 63: 'Train', 64: 'Bowl',
           65: 'Tiger', 66: 'Sail', 67: 'Oven', 68: 'Hockey', 69: 'Daffodil',
           70: 'Gnu', 71: 'Banana', 72: 'Koala', 73: 'Yoghurt', 74: 'Kiwi',
           75: 'Eye', 76: 'Leopard', 77: 'Buss', 78: 'Flower', 79: 'Phone',
           80: 'Rolling pin', 81: 'Water', 82: 'Beach', 83: 'Music', 84: 'Drink',
           85: 'Lawyer', 86: 'Button', 87: 'Raccoon', 88: 'Nose', 89: 'Swing',
           90: 'Turkey', 91: 'Sack', 92: 'Nail', 93: 'Dummy', 94: 'Student',
           95: 'Paint', 96: 'Mountain', 97: 'Rock', 98: 'Four', 99: 'Acorn',
           100: 'Three', 101: 'Juice', 102: 'Iron', 103: 'Boxing', 104: 'Corner',
           105: 'Frog', 106: 'Rhinoceros', 107: 'Climb', 108: 'Gold', 109: 'Envelope',
           110: 'Fox', 111: 'Bicycle', 112: 'Coat', 113: 'Quad'}

n = len(fc_list)
lst = ""
for i in range(n):
    lst += fc_list[i].lower()
    if i < n - 1:
        lst += ", "

# print the list to copy it for translation
# print(lst)
# stop()

# enter the translated string here
translated_string = "ant, boat, cat, duck, elephant, fish, grapes, house, igloo, jar, key, lion, mouse, notebook, owl, parrot, queen, rabbit, sun, teapot, umbrella, violin, window, xylophone, yarn, zebra, watermelon, butterfly, guitar, hedgehog, giraffe, tree, joga, tomato, fortepiano, bread, flowers, chimpanzee, fish, photographer, monitor, skirt, apple, no-picture,  moth, horse, tree, hippo, clothes, sleep, lorry, clock, ocean, street, night, space, hammack, cheese, wagon, dolphin, shoes, snail, foal, train, bowl, tiger, sail, oven, hockey, daffodil, gnu, banana, koala, yoghurt, kiwi, eye, leopard, buss, flower, phone, rolling pin, water, beach, music, drink, lawyer, button, raccoon, nose, swing, turkey, sack, nail, dummy, student, paint, mountain, rock, four, acorn, three, juice, iron, boxing, corner, frog, rhinoceros, climb, gold, envelope, fox, bicycle, coat, quad"
fc_list_trans = translated_string.split(', ')

# turn into a dictionary string
s = "{"
for i in range(n):
    s += str(i) + ": '" + fc_list_trans[i][0].upper() + fc_list_trans[i][1:] + "'"
    if i < n - 1:
        s += ", "
s += "}"

trans = eval(s)

alphabet_uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']

word_list = []
frame_flow = []
string_list = ""

for i in range(len(alphabet_uc)):
    found = False
    for j in range(len(trans)):
        if trans[j][0] == alphabet_uc[i]:
            word_list.append(trans[j])
            frame_flow.append(j)
            found = True
            string_list += str(j) + ": '" + trans[j] + "', "
    if not found:
        word_list.append(alphabet_uc[i])
        frame_flow.append(43)
        string_list += '43' + ": '" + alphabet_uc[i] + "', "

# print(string_list)

# replace the resulting dict with the result of the string_dict and select keys for each letter -
# the words will be automatically matched in the next step

resulting_dict = {42: 'Appel', 85: 'Advocaat', 1: 'Boot', 31: 'Boom', 35: 'Brood', 36: 'Bloemen', 46: 'Boom', 71: 'Banaan', 77: 'Bus', 78: 'Bloem', 96: 'Berg', 103: 'Boksen', 37: 'Chimpansee', 6: 'Druiven', 59: 'Dolfijn', 80: 'Deegrol', 84: 'Drinken', 93: 'Dummy', 100: 'Drie', 3: 'Eend', 29: 'Egel', 99: 'Eikel', 34: 'Fortepiano', 39: 'Fotograaf', 24: 'Garen', 28: 'Gitaar', 30: 'Giraf', 70: 'GNU', 7: 'Huis', 56: 'Hangmat', 68: 'Hockey', 104: 'Hoek', 8: 'Iglo', 102: 'Ijzer', 32: 'Joga', 2: 'Kat', 16: 'Koningin', 17: 'Konijn', 48: 'Kleding', 51: 'Klok', 57: 'Kaas', 64: 'Kom', 72: 'Koala', 74: 'Kiwi', 86: 'Knop', 11: 'Leeuw', 76: 'Luipaard', 0: 'Mier', 12: 'Muis', 40: 'Monitor', 44: 'Mot', 83: 'Muziek', 13: 'Notitieboekje', 43: 'No-picture', 47: 'Nijlpaard', 54: 'Nacht', 69: 'Narcis', 88: 'Neus', 92: 'Nagel', 4: 'Olifant', 52: 'Oceaan', 67: 'Oven', 75: 'Oog', 9: 'Pot', 15: 'Papegaai', 20: 'Paraplu', 45: 'Paard', 43: 'Q', 41: 'Rok', 55: 'Ruimte', 97: 'Rots', 10: 'Sleutel', 49: 'Slaap', 53: 'Straat', 60: 'Schoenen', 61: 'Slak', 82: 'Strand', 89: 'Schommel', 94: 'Student', 101: 'Sap', 19: 'Theepot', 33: 'Tomaat', 63: 'Trein', 65: 'Tijger', 79: 'Telefoon', 90: 'Turkije', 14: 'Uil', 5: 'Vis', 21: 'Viool', 22: 'Venster', 27: 'Vlinder', 38: 'Vis', 50: 'Vrachtwagen', 62: 'Veulen', 95: 'Verf', 98: 'Vier ', 26: 'Watermeloen', 58: 'Wagen', 81: 'Water', 87: 'Wasbeer', 23: 'Xylofoon', 73: 'Yoghurt', 18: 'Zon', 25: 'Zebra', 66: 'Zeil', 91: 'Zak'}

manually_selected = {42: 'Appel', 77: 'Bus', 37: 'Chimpansee', 59: 'Dolfijn', 29: 'Egel', 34: 'Fortepiano', 28: 'Gitaar', 7: 'Huis', 8: 'Iglo', 32: 'Joga', 2: 'Kat', 11: 'Leeuw', 12: 'Muis', 47: 'Nijlpaard', 4: 'Olifant', 15: 'Papegaai', 43: 'Q', 97: 'Rots', 61: 'Slak', 33: 'Tomaat',  14: 'Uil', 21: 'Viool', 81: 'Water', 23: 'Xylofoon', 73: 'Yoghurt', 25: 'Zebra'}
manually_selected_keys = [42, 77, 37, 59, 29, 34, 28, 7, 8, 32, 2, 11, 12, 47, 4, 15, 43, 97, 61, 33, 14, 21, 81, 23, 73, 25]

words = "words = ["
for i in range(len(manually_selected_keys)):
    words += "'" + resulting_dict[manually_selected_keys[i]] + "'"
    if i < len(manually_selected_keys) - 1:
        words += ", "
s += "]"
print (words)

# words = ['Appel', 'Bus', 'Chimpansee', 'Dolfijn', 'Egel', 'Fortepiano', 'Gitaar', 'Huis', 'Iglo', 'Joga', 'Kat', 'Leeuw', 'Muis', 'Nijlpaard', 'Olifant', 'Papegaai', 'Q', 'Rots', 'Slak', 'Tomaat',  'Uil', 'Viool', 'Water', 'Xylofoon', 'Yoghurt', 'Zebra']
