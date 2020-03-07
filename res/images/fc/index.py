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
           100: 'Three', 101: 'Juice', 102: 'Iron', 103: 'Boxing', 104: 'Corner'}

lst = ""
for i in range(105):
    lst += fc_list[i].lower() + ", "

# list of words to be used for tranalation
# print(lst)

fc_list_trans = ['mier', 'boot', 'kat', 'eend', 'olifant', 'vis', 'druiven', 'huis', 'iglo', 'pot', 'sleutel', 'leeuw', 'muis', 'notitieboekje', 'uil', 'papegaai', 'koningin', 'konijn', 'zon', 'theepot', 'paraplu', 'viool', 'venster', 'xylofoon', 'garen', 'zebra', 'watermeloen', 'vlinder', 'gitaar', 'egel', 'giraf', 'boom', 'joga', 'tomaat', 'fortepiano', 'brood', 'bloemen', 'chimpansee', 'vis', 'fotograaf', 'monitor', 'rok', 'appel', 'no-picture', 'mot', 'paard', 'boom', 'nijlpaard', 'kleding', 'slaap', 'vrachtwagen', 'klok', 'oceaan', 'straat', 'nacht', 'ruimte', 'hangmat', 'kaas', 'wagen', 'dolfijn', 'schoenen', 'slak', 'veulen', 'trein', 'kom', 'tijger', 'zeil', 'oven', 'hockey', 'narcis', 'GNU', 'banaan', 'koala', 'yoghurt', 'kiwi', 'oog', 'luipaard', 'bus', 'bloem', 'telefoon', 'deegrol', 'water', 'strand', 'muziek', 'drinken', 'advocaat', 'knop', 'wasbeer', 'neus', 'schommel', 'Turkije', 'zak', 'nagel', 'dummy', 'student', 'verf', 'berg', 'rots', 'vier ', 'eikel', 'drie', 'sap', 'ijzer', 'boksen', 'hoek']
s = ""
# turn into a dictionary
for i in range(105):
    s += ", " + str(i) + ": '" + fc_list_trans[i][0].upper() + fc_list_trans[i][1:] + "'"

# print dictionary
# print(s)

trans = {0: 'Mier', 1: 'Boot', 2: 'Kat', 3: 'Eend', 4: 'Olifant', 5: 'Vis', 6: 'Druiven', 7: 'Huis', 8: 'Iglo', 9: 'Pot', 10: 'Sleutel', 11: 'Leeuw', 12: 'Muis', 13: 'Notitieboekje', 14: 'Uil', 15: 'Papegaai', 16: 'Koningin', 17: 'Konijn', 18: 'Zon', 19: 'Theepot', 20: 'Paraplu', 21: 'Viool', 22: 'Venster', 23: 'Xylofoon', 24: 'Garen', 25: 'Zebra', 26: 'Watermeloen', 27: 'Vlinder', 28: 'Gitaar', 29: 'Egel', 30: 'Giraf', 31: 'Boom', 32: 'Joga', 33: 'Tomaat', 34: 'Fortepiano', 35: 'Brood', 36: 'Bloemen', 37: 'Chimpansee', 38: 'Vis', 39: 'Fotograaf', 40: 'Monitor', 41: 'Rok', 42: 'Appel', 43: 'No-picture', 44: 'Mot', 45: 'Paard', 46: 'Boom', 47: 'Nijlpaard', 48: 'Kleding', 49: 'Slaap', 50: 'Vrachtwagen', 51: 'Klok', 52: 'Oceaan', 53: 'Straat', 54: 'Nacht', 55: 'Ruimte', 56: 'Hangmat', 57: 'Kaas', 58: 'Wagen', 59: 'Dolfijn', 60: 'Schoenen', 61: 'Slak', 62: 'Veulen', 63: 'Trein', 64: 'Kom', 65: 'Tijger', 66: 'Zeil', 67: 'Oven', 68: 'Hockey', 69: 'Narcis', 70: 'GNU', 71: 'Banaan', 72: 'Koala', 73: 'Yoghurt', 74: 'Kiwi', 75: 'Oog', 76: 'Luipaard', 77: 'Bus', 78: 'Bloem', 79: 'Telefoon', 80: 'Deegrol', 81: 'Water', 82: 'Strand', 83: 'Muziek', 84: 'Drinken', 85: 'Advocaat', 86: 'Knop', 87: 'Wasbeer', 88: 'Neus', 89: 'Schommel', 90: 'Turkije', 91: 'Zak', 92: 'Nagel', 93: 'Dummy', 94: 'Student', 95: 'Verf', 96: 'Berg', 97: 'Rots', 98: 'Vier ', 99: 'Eikel', 100: 'Drie', 101: 'Sap', 102: 'Ijzer', 103: 'Boksen', 104: 'Hoek'
}
# new_list = ['Watermelon', 'Butterfly', 'Guitar', 'Hedgehog', 'Giraffe', 'Tree', 'Joga', 'Tomato', 'Fortepiano', 'Bread', 'Flowers', 'Chimpanzee', 'Fish', 'Photographer', 'Monitor', 'Skirt', 'Apple', 'No-Picture', ' Moth', 'Horse', 'Tree', 'Hippo', 'Clothes', 'Sleep', 'Lorry', 'Clock', 'Ocean', 'Street', 'Night', 'Space', 'Hamack', 'Cheese', 'Wagon', 'Dolphin', 'Shoes', 'Snail', 'Foal', 'Train', 'Bowl', 'Tiger', 'Sail', 'Oven', 'Hockey', 'Daffodil', 'Gnu', 'Banana', 'Koala', 'Yogurt', 'Kiwi', 'Eye', 'Leopard', 'Buss', 'Flower', 'Phone', 'Rolling pin', 'Water', 'Beach', 'Music', 'Drink', 'Lawyer', 'Button', 'Racoon', 'Nose', 'Swing', 'Turkey', 'Sack', 'Nail', 'Dummy', 'Student', 'Paint', 'Mountain', 'Rock', 'Four', 'Acorn', 'Three', 'Juice', 'Iron', 'Boxing', 'Corner']

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

#print(word_list)
#print (frame_flow)


# print(string_list)

# result
resulting_dict = {42: 'Appel', 85: 'Advocaat', 1: 'Boot', 31: 'Boom', 35: 'Brood', 36: 'Bloemen', 46: 'Boom', 71: 'Banaan', 77: 'Bus', 78: 'Bloem', 96: 'Berg', 103: 'Boksen', 37: 'Chimpansee', 6: 'Druiven', 59: 'Dolfijn', 80: 'Deegrol', 84: 'Drinken', 93: 'Dummy', 100: 'Drie', 3: 'Eend', 29: 'Egel', 99: 'Eikel', 34: 'Fortepiano', 39: 'Fotograaf', 24: 'Garen', 28: 'Gitaar', 30: 'Giraf', 70: 'GNU', 7: 'Huis', 56: 'Hangmat', 68: 'Hockey', 104: 'Hoek', 8: 'Iglo', 102: 'Ijzer', 32: 'Joga', 2: 'Kat', 16: 'Koningin', 17: 'Konijn', 48: 'Kleding', 51: 'Klok', 57: 'Kaas', 64: 'Kom', 72: 'Koala', 74: 'Kiwi', 86: 'Knop', 11: 'Leeuw', 76: 'Luipaard', 0: 'Mier', 12: 'Muis', 40: 'Monitor', 44: 'Mot', 83: 'Muziek', 13: 'Notitieboekje', 43: 'No-picture', 47: 'Nijlpaard', 54: 'Nacht', 69: 'Narcis', 88: 'Neus', 92: 'Nagel', 4: 'Olifant', 52: 'Oceaan', 67: 'Oven', 75: 'Oog', 9: 'Pot', 15: 'Papegaai', 20: 'Paraplu', 45: 'Paard', 43: 'Q', 41: 'Rok', 55: 'Ruimte', 97: 'Rots', 10: 'Sleutel', 49: 'Slaap', 53: 'Straat', 60: 'Schoenen', 61: 'Slak', 82: 'Strand', 89: 'Schommel', 94: 'Student', 101: 'Sap', 19: 'Theepot', 33: 'Tomaat', 63: 'Trein', 65: 'Tijger', 79: 'Telefoon', 90: 'Turkije', 14: 'Uil', 5: 'Vis', 21: 'Viool', 22: 'Venster', 27: 'Vlinder', 38: 'Vis', 50: 'Vrachtwagen', 62: 'Veulen', 95: 'Verf', 98: 'Vier ', 26: 'Watermeloen', 58: 'Wagen', 81: 'Water', 87: 'Wasbeer', 23: 'Xylofoon', 73: 'Yoghurt', 18: 'Zon', 25: 'Zebra', 66: 'Zeil', 91: 'Zak'}

manually_selected = {42: 'Appel', 77: 'Bus', 37: 'Chimpansee', 59: 'Dolfijn', 29: 'Egel', 34: 'Fortepiano', 28: 'Gitaar', 7: 'Huis', 8: 'Iglo', 32: 'Joga', 2: 'Kat', 11: 'Leeuw', 12: 'Muis', 47: 'Nijlpaard', 4: 'Olifant', 15: 'Papegaai', 43: 'Q', 97: 'Rots', 61: 'Slak', 33: 'Tomaat',  14: 'Uil', 21: 'Viool', 81: 'Water', 23: 'Xylofoon', 73: 'Yoghurt', 25: 'Zebra'}

words = ['Appel', 'Bus', 'Chimpansee', 'Dolfijn', 'Egel', 'Fortepiano', 'Gitaar', 'Huis', 'Iglo', 'Joga', 'Kat', 'Leeuw', 'Muis', 'Nijlpaard', 'Olifant', 'Papegaai', 'Q', 'Rots', 'Slak', 'Tomaat',  'Uil', 'Viool', 'Water', 'Xylofoon', 'Yoghurt', 'Zebra']
keys = [42, 77, 37, 59, 29, 34, 28, 7, 8, 32, 2, 11, 12, 47, 4, 15, 43, 97, 61, 33, 14, 21, 81, 23, 73, 25]

