# -*- coding: utf-8 -*-

import pygame
import random
import os

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 5, 3)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 13, 9)

    def create_game_objects(self, level=1):
        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.ai_enabled = False
        self.board.draw_grid = False
        s = random.randrange(100, 150, 5)
        v = random.randrange(230, 255, 5)
        h = random.randrange(0, 255, 5)
        bg_col = (255, 255, 255)
        if self.mainloop.scheme is not None:
            if self.mainloop.scheme.dark:
                bg_col = (0, 0, 0)
        color0 = ex.hsv_to_rgb(h, 1, 255)  # highlight 1
        self.color2 = ex.hsv_to_rgb(h, 255, 170)  # contours & borders
        self.font_color = self.color2

        white = (255, 255, 255)

        self.disp_counter = 0
        self.disp_len = 1
        lvl = 0

        gv = self.mainloop.m.game_variant
        if gv == 0:
            category = "animals"
            self.imgs = ['cow', 'turkey', 'shrimp', 'wolf', 'panther', 'panda', 'magpie', 'clam', 'pony', 'mouse',
                         'pug', 'koala', 'frog', 'ladybug', 'gorilla', 'llama', 'vulture', 'hamster', '',
                         'starfish', 'crow', 'parakeet', 'caterpillar', 'tiger', 'hummingbird', 'piranha', 'pig',
                         'scorpion', 'fox', 'leopard', 'iguana', 'dolphin', 'bat', 'chick', 'crab', 'hen', 'wasp',
                         'chameleon', 'whale', 'hedgehog', 'fawn', 'moose', 'bee', 'viper', 'shrike', 'donkey',
                         'guinea_pig', 'sloth', 'horse', 'penguin', 'otter', 'bear', 'zebra', 'ostrich', 'camel',
                         'antelope', 'lemur', 'pigeon', '', 'mole', 'ray', 'ram', 'skunk', 'jellyfish', 'sheep',
                         'shark', 'kitten', 'deer', 'snail', 'flamingo', 'rabbit', 'oyster', 'beaver', 'sparrow',
                         'dove', 'eagle', 'beetle', 'hippopotamus', 'owl', 'cobra', 'salamander', 'goose', 'kangaroo',
                         'dragonfly', '', 'pelican', 'squid', 'lion_cub', 'jaguar', 'duck', 'lizard', 'rhinoceros',
                         'hyena', 'ox', 'peacock', 'parrot', '', 'alligator', 'ant', 'goat', 'baby_rabbit', 'lion',
                         'squirrel', 'opossum', 'chimp', 'doe', 'gopher', 'elephant', 'giraffe', 'spider', 'puppy',
                         'jay', 'seal', 'rooster', 'turtle', 'bull', 'cat', 'rat', 'slug', 'buffalo',
                         'blackbird', 'swan', 'lobster', 'dog', 'mosquito', 'snake', 'chicken', 'anteater']
        elif gv == 1:
            category = "sport"
            self.imgs = ['judo', 'pool', 'ride', 'stretch', 'helmet', 'ice_skating', 'walk', '', 'run', 'swim',
                         '', '', 'boxing', 'hockey', 'race', 'throw', 'skate', 'win', 'squat', 'ski', 'golf',
                         'whistle', 'torch', 'sailing', 'stand', 'tennis', 'jump', 'rowing', '', 'rope']
        elif gv == 2:
            category = "body"
            self.imgs = ['teeth', 'cheek', 'ankle', 'knee', 'toe', 'muscle', 'mouth', 'feet', 'hand', 'elbow', 'hair',
                         'eyelash', 'beard', 'belly_button', 'thumb', 'breast', 'nostril', 'nose', 'hip', 'arm',
                         'eyebrow', 'fist', 'neck', 'wrist', 'throat', 'eye', 'leg', 'spine', 'ear', 'finger', 'foot',
                         'braid', 'face', 'back', 'chin', 'bottom', 'thigh', 'belly']
        elif gv == 3:
            category = "people"
            self.imgs = ['girl', '', 'son', '', 'friends', 'baby', 'child', 'dad', 'mom', 'twin_boys',
                         'brothers', 'man', '', 'grandfather', 'family', '', 'wife', 'husband', '',
                         '', 'grandmother', 'couple', '', 'twin_girls', 'tribe', 'boy', 'sisters', 'woman',
                         '']
        elif gv == 4:
            category = "actions"
            self.imgs = ['lick', 'slam', 'beg', 'fell', 'scratch', 'touch', 'sniff', 'see', 'climb', 'dig', 'howl',
                         'sleep', 'explore', 'draw', 'hug', 'teach', 'nap', 'clay', 'catch', 'clap', 'cry', 'sing',
                         'meet', 'sell', 'peck', 'beat', 'kneel', 'find', 'dance', 'cough', 'cut', 'think', 'bark',
                         'speak', 'cheer', 'bake', 'write', 'punch', 'strum', 'study', 'plow', 'dream', 'post', 'dive',
                         'whisper', 'sob', 'shake', 'feed', 'crawl', 'camp', 'spill', 'clean', 'scream', 'tear',
                         'float', 'pull', 'ate', 'kiss', 'sit', 'hatch', 'blink', 'hear', 'smooch', 'play', 'wash',
                         'chat', 'drive', 'drink', 'fly', 'juggle', 'bit', 'sweep', 'look', 'knit', 'lift', 'fetch',
                         'read', 'croak', 'stare', 'eat']
        elif gv == 5:
            category = "construction"
            self.imgs = ['lighthouse', 'door', 'circus', 'church', 'kennel', 'temple', 'smoke', 'chimney', 'brick',
                         'well', 'street', 'castle', 'store', 'staircase', 'school', 'farm', 'bridge', 'dam', 'pyramid',
                         'barn', 'mill', 'window', '', 'step', 'shop', 'shed', 'roof', 'steeple', 'garage',
                         'mosque', 'hospital', 'tent', 'house', 'wall', 'bank', 'shutter', 'hut']
        elif gv == 6:
            category = "nature"
            self.imgs = ['land', 'cliff', 'hill', 'canyon', 'rock', 'sea', 'lake', 'coast', 'shore', 'mountain', 'pond',
                         'peak', 'lava', 'cave', 'dune', 'island', 'forest', 'desert', 'iceberg']
        elif gv == 7:
            category = "jobs"
            self.imgs = ['clown', 'engineer', 'priest', 'vet', 'judge', '', 'athlete', 'librarian', 'juggler',
                         'police', 'plumber', '', 'queen', 'farmer', 'magic', 'knight', 'doctor', 'bricklayer',
                         'cleaner', 'teacher', 'hunter', 'soldier', 'musician', 'lawyer', 'fisherman', 'princess',
                         'fireman', 'nun', 'pirate', 'cowboy', 'electrician', 'nurse', 'king', 'president',
                         'office', 'carpenter', 'jockey', 'worker', 'mechanic', 'pilot', 'actor', 'cook', 'student',
                         'butcher', 'accountant', 'prince', 'pope', 'sailor', 'boxer', 'ballet', 'coach', 'astronaut',
                         'painter', 'anaesthesiologist', 'scientist']
        elif gv == 8:
            category = "clothes_n_accessories"
            self.imgs = ['jewellery', 'sock', 'jacket', 'heel', 'smock', 'shorts', 'pocket', 'necklace', 'sweatshirt',
                         'uniform', 'raincoat', 'trousers', 'sunglasses', 'coat', 'pullover', 'shirt', 'sandals',
                         'suit', 'pyjamas', 'skirt', 'zip', 'shoes', 'jewel', 'tie', 'slippers', 'gloves', 'hat',
                         'sleeve', 'cap', 'swimming_suit', 'sneaker', 'vest', 'glasses', 'shoelace', 'patch', 'scarf',
                         'shoe', 'button', 'dress', 'sash', 'shoe_sole', 'robe', 'pants', 'kimono', 'overalls']
        elif gv == 9:
            category = "fruit_n_veg"
            self.imgs = ['carrot', 'blackberries', 'celery', 'turnip', 'cacao', 'peach', 'melon', 'grapefruit',
                         'broccoli', 'grapes', 'spinach', 'fig', 'kernel', 'radish', 'tomato', 'kiwi', 'asparagus',
                         'olives', 'cucumbers', 'beans', 'strawberry', 'peppers', 'raspberry', 'apricot', 'potatoes',
                         'peas', 'cabbage', 'cherries', 'squash', 'blueberries', 'pear', 'orange', 'pumpkin', 'avocado',
                         'garlic', 'onion', 'apple', 'lime', 'cauliflower', 'mango', 'lettuce', 'lemon', 'aubergine',
                         'artichokes', 'plums', 'leek', 'bananas', 'papaya']
        elif gv == 10:
            category = "transport"
            self.imgs = ['sail', 'taxi', 'car', '', 'raft', 'pedal', 'bus', 'handlebar', 'boat', 'truck', 'sleigh',
                         'carpet', 'motorcycle', 'train', 'ship', 'van', 'canoe', 'rocket', 'mast', 'sledge', 'bicycle']
        elif gv == 11:
            category = "food"
            self.imgs = ['candy', 'sausage', 'hamburger', 'steak', 'fudge', 'doughnut', 'coconut', 'rice', 'ice_cream',
                         'jelly', 'yoghurt', 'dessert', 'pretzel', 'peanut', 'jam', 'feast', 'cookie', 'bacon', 'spice',
                         'coffee', 'pie', 'lemonade', 'chocolate', 'water_bottle', 'lunch', 'ice', 'sugar', 'sauce',
                         'soup', 'juice', 'fries', 'cake', 'mashed_potatoes', 'tea', 'bun', 'cheese', 'beef',
                         'sandwich', 'slice', 'sprinkle', 'pizza', 'flour', 'gum', 'spaghetti', 'roast', 'drink',
                         'stew', 'spread', 'meat', 'milk', 'meal', 'corn', 'bread', 'walnut', 'egg', 'hot_dog', 'ham']

        # Maximum words per screen 19 (nature)

        self.captions = self.d["a4a_%s" % category]

        if self.level.lvl > self.level.lvl_count:
            self.level.lvl = self.level.lvl_count
        if self.level.lvl == 1:
            data = [10, 3, 3, 2, 3]
        elif self.level.lvl == 2:
            data = [10, 4, 3, 2, 4]
        elif self.level.lvl == 3:
            data = [10, 5, 3, 2, 5]

        # rescale the number of squares horizontally to better match the screen width
        m = data[0] % 2
        if m == 0:
            x = self.get_x_count(data[1], even=True)
        else:
            x = self.get_x_count(data[1], even=False)

        if x > data[0]:
            data[0] = x

        self.data = data

        self.found = 0
        self.clicks = 0

        self.squares = self.data[3] * self.data[4]

        self.square_count = self.squares * 2  # self.data[3]*self.data[4]
        self.history = [None, None]

        self.layout.update_layout(data[0], data[1])
        self.board.level_start(data[0], data[1], self.layout.scale)
        texts1 = []
        texts2 = []

        l = len(self.imgs)
        drawn_numbers = []
        while len(drawn_numbers) < data[1] * 2:
            r = random.randint(0, l-1)
            if r not in drawn_numbers:
                if self.imgs[r] != '':
                    drawn_numbers.append(r)

        self.completed_mode = False

        choice = [x for x in range(0, self.square_count // 2)]
        shuffled = choice[:]
        random.shuffle(shuffled)
        self.chosen = shuffled[0:self.square_count // 2]
        self.chosen = self.chosen * 2

        h1 = (data[1] - data[4]) // 2  # height of the top margin
        h2 = data[1] - h1 - data[4]  # -1 #height of the bottom margin minus 1 (game label)
        w2 = (data[0] - data[3] * 4) // 2 - 1  # side margin width

        x = w2
        y = h1
        small_slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2, w2 + data[3]):
                small_slots.append([i, j])
        random.shuffle(small_slots)

        wide_slots = []
        for j in range(h1, data[1] - h2):
            for i in range(w2 + data[3], data[0] - w2, 4):
                wide_slots.append([i, j])
        random.shuffle(wide_slots)
        switch = self.square_count // 2
        for i in range(self.square_count):
            if i < switch:
                img = "%s.jpg" % self.imgs[drawn_numbers[i]]
                img_src = os.path.join('art4apps', category, img)
                position_list = small_slots
                pos = i
                xw = 1
                self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, 1, classes.board.ImgShip, "",
                                    color0, img_src)
            else:
                caption = self.captions[drawn_numbers[i - switch]]
                position_list = wide_slots
                pos = i - switch
                xw = 4
                self.board.add_unit(position_list[pos][0], position_list[pos][1], xw, 1, classes.board.Letter, caption,
                                    color0, "", 8)
                self.board.ships[-1].font_color = self.font_color
            self.board.ships[i].immobilize()
            self.board.ships[i].readable = False
            self.board.ships[i].perm_outline = True
            self.board.ships[i].uncovered = False
            self.board.ships[i].checkable = True
            self.board.ships[i].init_check_images()
        self.outline_all(self.color2, 1)

    def handle(self, event):
        gd.BoardGame.handle(self, event)  # send event handling up
        if event.type == pygame.MOUSEBUTTONDOWN and self.history[
            1] == None and self.ai_enabled == False:  # and self.start_sequence==False:
            if 0 <= self.board.active_ship < self.square_count:
                active = self.board.ships[self.board.active_ship]
                if active.uncovered == False:
                    if self.history[0] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[0] = active
                        self.clicks += 1
                        active.uncovered = True
                    elif self.history[1] is None:
                        active.perm_outline_width = 6
                        active.perm_outline_color = [150, 150, 255]
                        self.history[1] = active
                        self.clicks += 1
                        if self.chosen[self.history[0].unit_id] != self.chosen[self.history[1].unit_id]:
                            self.ai_enabled = True
                            self.history[0].uncovered = False
                        else:
                            self.history[0].uncovered = True
                            self.history[1].uncovered = True
                            self.history[0].perm_outline_color = self.color2  # [50,255,50]
                            self.history[1].perm_outline_color = self.color2
                            self.history[0].image.set_alpha(50)
                            self.history[1].image.set_alpha(50)
                            self.history[0].update_me = True
                            self.history[1].update_me = True
                            self.history[0].set_display_check(True)
                            self.history[1].set_display_check(True)
                            self.found += 2
                            if self.found == self.square_count:
                                self.completed_mode = True
                                self.ai_enabled = True
                            self.history = [None, None]
                    active.update_me = True

    def update(self, game):
        game.fill((255, 255, 255))
        gd.BoardGame.update(self, game)  # rest of painting done by parent

    def ai_walk(self):
        if self.disp_counter < self.disp_len:
            self.disp_counter += 1
        else:
            if self.completed_mode:
                self.history = [None, None]
                self.level.next_board()
            else:
                self.history[0].perm_outline_width = 1
                self.history[0].perm_outline_color = self.color2
                self.history[1].perm_outline_width = 1
                self.history[1].perm_outline_color = self.color2
                self.history[0].update_me = True
                self.history[1].update_me = True
                self.history = [None, None]
                self.ai_enabled = False
                self.disp_counter = 0

    def check_result(self):
        pass
