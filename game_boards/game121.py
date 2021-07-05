# -*- coding: utf-8 -*-

import os
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc


class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 1, 1)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 20, 10)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        color = (234, 218, 225)
        self.color = color
        h = self.mainloop.cl.get_interface_hue()
        arrow_color = ex.hsv_to_rgb(h, 200, 200)

        img_top = 1
        gv = self.mainloop.m.game_variant
        if gv == 0:
            category = "animals"
            self.imgs = ['cow', 'turkey', 'shrimp', 'wolf', 'panther', 'panda', 'magpie', 'clam', 'pony', 'mouse',
                         'pug', 'koala', 'frog', 'ladybug', 'gorilla', 'llama', 'vulture', 'hamster', 'bird',
                         'starfish', 'crow', 'parakeet', 'caterpillar', 'tiger', 'hummingbird', 'piranha', 'pig',
                         'scorpion', 'fox', 'leopard', 'iguana', 'dolphin', 'bat', 'chick', 'crab', 'hen', 'wasp',
                         'chameleon', 'whale', 'hedgehog', 'fawn', 'moose', 'bee', 'viper', 'shrike', 'donkey',
                         'guinea_pig', 'sloth', 'horse', 'penguin', 'otter', 'bear', 'zebra', 'ostrich', 'camel',
                         'antelope', 'lemur', 'pigeon', 'lama', 'mole', 'ray', 'ram', 'skunk', 'jellyfish', 'sheep',
                         'shark', 'kitten', 'deer', 'snail', 'flamingo', 'rabbit', 'oyster', 'beaver', 'sparrow',
                         'dove', 'eagle', 'beetle', 'hippopotamus', 'owl', 'cobra', 'salamander', 'goose', 'kangaroo',
                         'dragonfly', 'toad', 'pelican', 'squid', 'lion_cub', 'jaguar', 'duck', 'lizard', 'rhinoceros',
                         'hyena', 'ox', 'peacock', 'parrot', 'elk', 'alligator', 'ant', 'goat', 'baby_rabbit', 'lion',
                         'squirrel', 'opossum', 'chimp', 'doe', 'gopher', 'elephant', 'giraffe', 'spider', 'puppy',
                         'jay', 'seal', 'rooster', 'turtle', 'bull', 'cat', 'rat', 'slug', 'buffalo',
                         'blackbird', 'swan', 'lobster', 'dog', 'mosquito', 'snake', 'chicken', 'anteater']
        elif gv == 1:
            category = "sport"
            self.imgs = ['judo', 'pool', 'ride', 'stretch', 'helmet', 'ice_skating', 'walk', 'run', 'swim',
                         'hop', 'hike', 'boxing', 'hockey', 'race', 'throw', 'skate', 'win', 'squat', 'ski', 'golf',
                         'whistle', 'torch', 'sailing', 'stand', 'tennis', 'jump', 'rowing', 'jog', 'rope']
        elif gv == 2:
            category = "body"
            self.imgs = ['teeth', 'cheek', 'ankle', 'knee', 'toe', 'muscle', 'mouth', 'feet', 'hand', 'elbow', 'hair',
                         'eyelash', 'beard', 'belly_button', 'thumb', 'breast', 'nostril', 'nose', 'hip', 'arm',
                         'eyebrow', 'fist', 'neck', 'wrist', 'throat', 'eye', 'leg', 'spine', 'ear', 'finger', 'foot',
                         'braid', 'face', 'back', 'chin', 'bottom', 'thigh', 'belly']
        elif gv == 3:
            category = "people"
            self.imgs = ['girl', 'male', 'son', 'mates', 'friends', 'baby', 'child', 'dad', 'mom', 'twin_boys',
                         'brothers', 'man', 'mother', 'grandfather', 'family', 'female', 'wife', 'husband', 'bride',
                         'madam', 'grandmother', 'couple', 'lad', 'twin_girls', 'tribe', 'boy', 'sisters', 'woman',
                         'lady']
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
                         'barn', 'mill', 'window', 'cabin', 'step', 'shop', 'shed', 'roof', 'steeple', 'garage',
                         'mosque', 'hospital', 'tent', 'house', 'wall', 'bank', 'shutter', 'hut']
        elif gv == 6:
            category = "nature"
            self.imgs = ['land', 'cliff', 'hill', 'canyon', 'rock', 'sea', 'lake', 'coast', 'shore', 'mountain', 'pond',
                         'peak', 'lava', 'cave', 'dune', 'island', 'forest', 'desert', 'iceberg']
        elif gv == 7:
            category = "jobs"
            self.imgs = ['clown', 'engineer', 'priest', 'vet', 'judge', 'chef', 'athlete', 'librarian', 'juggler',
                         'police', 'plumber', 'badge', 'queen', 'farmer', 'magic', 'knight', 'doctor', 'bricklayer',
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
            self.imgs = ['sail', 'taxi', 'car', 'bike', 'raft', 'pedal', 'bus', 'handlebar', 'boat', 'truck', 'sleigh',
                         'carpet', 'motorcycle', 'train', 'ship', 'van', 'canoe', 'rocket', 'mast', 'sledge', 'bicycle']
        elif gv == 11:
            category = "food"
            self.imgs = ['candy', 'sausage', 'hamburger', 'steak', 'fudge', 'doughnut', 'coconut', 'rice', 'ice_cream',
                         'jelly', 'yoghurt', 'dessert', 'pretzel', 'peanut', 'jam', 'feast', 'cookie', 'bacon', 'spice',
                         'coffee', 'pie', 'lemonade', 'chocolate', 'water_bottle', 'lunch', 'ice', 'sugar', 'sauce',
                         'soup', 'juice', 'fries', 'cake', 'mashed_potatoes', 'tea', 'bun', 'cheese', 'beef',
                         'sandwich', 'slice', 'sprinkle', 'pizza', 'flour', 'gum', 'spaghetti', 'roast',
                         'stew', 'spread', 'meat', 'milk', 'meal', 'corn', 'bread', 'walnut', 'egg', 'hot_dog', 'ham']

        self.category = category
        self.words = self.d["a4a_%s" % category]
        self.current_image_index = -1
        self.max_image_index = len(self.words) - 1

        l = 100
        self.max_word_len = 35
        while l > self.max_word_len:
            self.w_index = self.current_image_index + 1
            if self.w_index > len(self.words) - 1:
                self.w_index = 0
            self.word = ex.unival(self.words[self.w_index])
            if self.word[0] != "<":
                l = len(self.word)
            else:
                l = 100

            self.current_image_index = self.w_index

        if self.mainloop.lang.lang == "ru":
            self.wordsp = eval("self.dp['a4a_%s']" % category)
            self.wordp = ex.unival(self.wordsp[self.w_index])
        else:
            self.wordp = self.word

        img_src = "%s.jpg" % self.imgs[self.w_index]

        w_len = len(self.word)

        self.mainloop.redraw_needed = [True, True, True]

        data = [14, 9]
        img_w_size = 4
        img_h_size = 4

        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=True)
        if x_count > data[0]:
            data[0] = x_count

        self.data = data

        self.board.set_animation_constraints(0, data[0], 0, data[1])

        self.vis_buttons = [0, 0, 0, 0, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        base_len = data[0] - 2
        img_left = (base_len - img_w_size) // 2 + 1

        color_bg = (255, 255, 255)

        l = (data[0] - w_len) // 2
        self.left_offset = l


        self.board.add_unit(img_left, img_top, img_w_size, img_h_size, classes.board.ImgShip, self.wordp, color_bg,
                            os.path.join('art4apps', category, img_src))

        self.picture = self.board.ships[-1]
        self.picture.immobilize()
        self.picture.highlight = False
        self.picture.outline_highlight = False
        self.picture.animable = False
        self.picture.outline = False
        self.picture.is_door = False
        self.picture.speaker_val = self.wordp
        self.picture.speaker_val_update = False

        self.units = []

        label_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_tint_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        bg_img_src_w = os.path.join('unit_bg', "universal_r6x1_bg.png")
        #fg_img_src_w = os.path.join('unit_bg', "universal_r6x1_door.png")

        if self.mainloop.scheme is None:
            dc_img_src_w = os.path.join('unit_bg', "universal_r6x1_dc.png")
        else:
            dc_img_src_w = None

        #self.board.add_unit(1, img_h_size + img_top + 1, data[0] - 2, 1, classes.board.Letter, self.word, letter_bg, "", 0)
        self.board.add_universal_unit(grid_x=img_left - 4, grid_y=data[1] - 3, grid_w=12, grid_h=2, txt=self.word,
                                      alpha=True, fg_img_src=bg_img_src_w, bg_img_src=bg_img_src_w,
                                      dc_img_src=dc_img_src_w, bg_color=(0, 0, 0, 0), border_color=None,
                                      font_color=font_color, bg_tint_color=label_color, fg_tint_color=fg_tint_color,
                                      txt_align=(0, 0), font_type=25, multi_color=False, immobilized=True,
                                      fg_as_hover=False)
        self.label = self.board.ships[-1]
        #self.label.draggable = False
        #self.label.highlight = False
        #self.label.outline_highlight = False
        #self.label.set_outline(color=border_color, width=2)
        #self.label.font_color = font_color
        self.label.readable = True
        self.label.speaker_val = self.wordp
        self.label.speaker_val_update = False

        self.board.add_unit(img_left - 3, 2, 2, 2, classes.board.ImgCenteredShip, "", (0, 0, 0, 0),
                            img_src='nav_l_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)
        self.lt = self.board.ships[-1]

        self.board.add_unit(img_left + 5, 2, 2, 2, classes.board.ImgCenteredShip, "", (0, 0, 0, 0),
                            img_src='nav_r_mt.png', alpha=True)
        self.board.ships[-1].set_tint_color(arrow_color)
        self.rt = self.board.ships[-1]

        for each in self.board.ships:
            each.immobilize()

    def next_image(self, direction = 1):
        l = 100
        if direction == 1:
            while l > self.max_word_len:
                self.w_index = self.current_image_index + 1
                if self.w_index > len(self.words) - 1:
                    self.w_index = 0
                self.word = ex.unival(self.words[self.w_index])
                if self.word[0] != "<":
                    l = len(self.word)
                else:
                    l = 100
                self.current_image_index = self.w_index
        else:
            while l > self.max_word_len:
                self.w_index = self.current_image_index - 1
                if self.w_index < 0:
                    self.w_index = len(self.words) - 1
                self.word = ex.unival(self.words[self.w_index])
                if self.word[0] != "<":
                    l = len(self.word)
                else:
                    l = 100
                self.current_image_index = self.w_index

        if self.mainloop.lang.lang == "ru":
            self.wordp = ex.unival(self.wordsp[self.w_index])
        else:
            self.wordp = self.word

        # change image and pronunciation
        img_src = "%s.jpg" % self.imgs[self.w_index]
        self.picture.change_image(os.path.join('art4apps', self.category, img_src))
        self.picture.speaker_val = self.wordp
        self.picture.update_me = True

        # change label and pronunciation
        self.label.set_value(self.word)
        self.label.speaker_val = self.wordp
        self.label.update_me = True

        self.mainloop.redraw_needed[0] = True

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = [event.pos[0] - self.layout.game_left, event.pos[1] - self.layout.top_margin]
            if self.lt.rect.topleft[0] < pos[0] < self.lt.rect.topleft[0] + self.lt.rect.width and \
                    self.lt.rect.topleft[1] < pos[1] < self.lt.rect.topleft[1] + self.lt.rect.height:
                self.next_image(-1)
            elif self.rt.rect.topleft[0] < pos[0] < self.rt.rect.topleft[0] + self.rt.rect.width and \
                    self.rt.rect.topleft[1] < pos[1] < self.rt.rect.topleft[1] + self.rt.rect.height:
                self.next_image(1)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)

    def check_result(self):
        pass
