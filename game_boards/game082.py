# -*- coding: utf-8 -*-

import os
import random
import pygame

import classes.board
import classes.extras as ex
import classes.game_driver as gd
import classes.level_controller as lc

class Board(gd.BoardGame):
    def __init__(self, mainloop, speaker, config, screen_w, screen_h):
        self.level = lc.Level(self, mainloop, 5, 5)
        gd.BoardGame.__init__(self, mainloop, speaker, config, screen_w, screen_h, 20, 10)

    def create_game_objects(self, level=1):
        self.board.draw_grid = False
        color = (234, 218, 225)
        self.color = color

        white = (255, 255, 255)

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

        self.words = self.d["a4a_%s" % category]

        self.level.games_per_lvl = 10

        l = 100
        max_word_len = 20

        while l > max_word_len:
            self.w_index = random.randint(0, len(self.words) - 1)
            self.word = ex.unival(self.words[self.w_index])
            if self.word[0] != "<":
                l = len(self.word)
            else:
                l = 100

        if self.mainloop.lang.lang == "ru":
            self.wordsp = eval("self.dp['a4a_%s']" % category)
            self.wordp = ex.unival(self.wordsp[self.w_index])
        else:
            self.wordp = self.word
        if self.mainloop.m.game_var2 == 0:
            img_src = "%s.jpg" % self.imgs[self.w_index]
        elif self.mainloop.m.game_var2 == 1:
            img_src = "speaker_icon.png"

        w_len = len(self.word)
        self.mainloop.redraw_needed = [True, True, True]

        if w_len % 2 == 0:
            even = True
            data = [w_len, 10]
            img_w_size = 4
        else:
            even = False
            data = [w_len, 10]
            img_w_size = 5
        img_h_size = 4

        # stretch width to fit the screen size
        x_count = self.get_x_count(data[1], even=even)
        if x_count > data[0]:
            data[0] = x_count

        self.data = data

        self.board.set_animation_constraints(0, data[0], 0, data[1])

        self.vis_buttons = [0, 1, 1, 1, 1, 0, 1, 0, 0]
        self.mainloop.info.hide_buttonsa(self.vis_buttons)

        self.layout.update_layout(data[0], data[1])
        scale = self.layout.scale
        self.board.level_start(data[0], data[1], scale)

        self.unit_mouse_over = None
        self.units = []

        self.board.board_bg.update_me = True
        self.board.board_bg.line_color = (20, 20, 20)

        base_len = data[0] - 2
        img_left = (base_len - img_w_size) // 2 + 1

        n_letters = self.level.lvl + 1
        if self.level.lvl == 3:
            if n_letters >= w_len:
                n_letters = w_len - 1
        if n_letters > w_len or self.level.lvl == 5:
            n_letters = w_len

        color_bg = (255, 255, 255)
        # frame around image caption
        if self.mainloop.scheme is not None:
            clx = self.mainloop.scheme.u_color
            if self.mainloop.scheme.dark:
                color_bg = (0, 0, 0)
        else:
            clx = white

        l = (data[0] - w_len) // 2
        self.left_offset = l

        # frame around image - white/  clx
        self.board.add_door(img_left - 1, 1, img_w_size + 2, img_h_size + 3, classes.board.Door, "", white, "", font_size=2)
        self.board.units[-1].image.set_colorkey(None)
        self.board.units[-1].is_door = False

        self.board.add_door(1, img_w_size + 3, base_len, 3, classes.board.Door, "", clx, "", font_size=2)
        self.board.units[-1].image.set_colorkey(None)
        self.board.units[-1].is_door = False

        # dummy frame hiding bottom line of the image frame
        self.board.add_door(img_left - 1, img_w_size + img_top + 1, img_h_size + 2, 1, classes.board.Door, "", clx, "",
                            font_size=2)
        self.board.units[-1].image.set_colorkey(None)
        self.board.units[-1].is_door = False
        if self.mainloop.m.game_var2 == 0:
            self.board.add_unit(img_left, img_top, img_w_size, img_h_size, classes.board.ImgCenteredShip, self.wordp, color_bg,
                                os.path.join('art4apps', category, img_src))
        elif self.mainloop.m.game_var2 == 1:
            self.mainloop.sb.toggle_espeak(True)
            self.board.add_unit(img_left, img_top, img_w_size, img_h_size, classes.board.ImgCenteredShip, self.wordp, color_bg,
                                img_src, alpha=True)
        self.board.ships[-1].immobilize()
        self.board.ships[-1].highlight = False
        self.board.ships[-1].outline_highlight = False
        self.board.ships[-1].animable = False
        self.board.ships[-1].outline = False
        self.board.units[-1].is_door = False

        choice_list = self.word[:]
        index_list = [x for x in range(w_len)]
        lowered_ind = [0 for x in range(w_len)]
        lowered = []
        for i in range(n_letters):  # picking letters to lower
            index = random.randrange(0, len(index_list))
            lowered.append(choice_list[index_list[index]])
            lowered_ind[index_list[index]] = 1
            del (index_list[index])

        random.shuffle(lowered)

        # set images and colors
        if self.mainloop.scheme is None:
            dc_img_src = os.path.join('unit_bg', "universal_sq_dc.png")
        else:
            dc_img_src = None
        h = random.randint(0, 255)
        bg_img_src = os.path.join('unit_bg', "universal_sq_bg.png")
        bg_door_img_src = os.path.join('unit_bg', "universal_sq_door.png")
        door_bg_tint = ex.hsv_to_rgb(h, self.mainloop.cl.door_bg_tint_s, self.mainloop.cl.door_bg_tint_v)
        number_color = ex.hsv_to_rgb(h, self.mainloop.cl.bg_color_s, self.mainloop.cl.bg_color_v)
        font_color = [ex.hsv_to_rgb(h, self.mainloop.cl.font_color_s, self.mainloop.cl.font_color_v), ]
        fg_number_color = ex.hsv_to_rgb(h, self.mainloop.cl.fg_hover_s, self.mainloop.cl.fg_hover_v)

        # create table to store 'binary' solution
        self.solution_grid = [0 for x in range(data[0])]
        x = l
        y = img_h_size + img_top + 1

        self.sol_grid_y = y

        x2 = (data[0] - len(lowered)) // 2
        y2 = img_h_size + img_top + 3

        j = 0
        for i in range(len(self.word)):
            picked = False
            if lowered_ind[i] == 1:
                picked = True
            self.solution_grid[x] = 1
            # change y
            if picked:
                caption = lowered[j]
                self.board.add_universal_unit(grid_x=x2 + j, grid_y=y2, grid_w=1, grid_h=1, txt=caption,
                                              fg_img_src=bg_img_src,
                                              bg_img_src=bg_img_src,
                                              dc_img_src=dc_img_src,
                                              bg_color=(0, 0, 0, 0),
                                              border_color=None, font_color=font_color,
                                              bg_tint_color=number_color,
                                              fg_tint_color=fg_number_color,
                                              txt_align=(0, 0), font_type=0, multi_color=False, alpha=True,
                                              immobilized=False, fg_as_hover=True)
                self.units.append(self.board.ships[-1])

                # empty slot
                self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=None,
                                              fg_img_src=None,
                                              bg_img_src=bg_door_img_src,
                                              dc_img_src=None,
                                              bg_color=(0, 0, 0, 0),
                                              border_color=None, font_color=None,
                                              bg_tint_color=door_bg_tint,
                                              fg_tint_color=None,
                                              txt_align=(0, 0), font_type=10, multi_color=False, alpha=True,
                                              immobilized=True, mode=2)

                self.board.ships[-1].readable = False
                self.board.ships[-1].checkable = True
                self.board.ships[-1].init_check_images()
                j += 1
            else:
                caption = self.word[i]
                self.board.add_universal_unit(grid_x=x, grid_y=y, grid_w=1, grid_h=1, txt=caption,
                                              fg_img_src=None,
                                              bg_img_src=bg_img_src,
                                              dc_img_src=dc_img_src,
                                              bg_color=(0, 0, 0, 0),
                                              border_color=None, font_color=font_color,
                                              bg_tint_color=number_color,
                                              fg_tint_color=fg_number_color,
                                              txt_align=(0, 0), font_type=0, multi_color=False, alpha=True,
                                              immobilized=True, fg_as_hover=False)

                self.board.ships[-1].readable = False
                self.board.ships[-1].checkable = True
                self.board.ships[-1].init_check_images()
            x += 1
        for i in range(3, 3 + n_letters):
            self.board.all_sprites_list.move_to_front(self.board.units[i])

        if self.mainloop.m.game_var2 == 1:
            self.mainloop.speaker.say(self.wordp)

    def handle(self, event):
        gd.BoardGame.handle(self, event)
        if event.type == pygame.MOUSEBUTTONUP:
            for each in self.board.units:
                if each.is_door is True:
                    self.board.all_sprites_list.move_to_front(each)
            self.check_result(auto=True)

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            self.default_hover(event)

    def auto_check(self):
        if self.board.grid[self.sol_grid_y] == self.solution_grid:
            for i in range(1, len(self.board.ships)):
                if self.board.ships[i].grid_y == self.sol_grid_y:
                    if self.board.ships[i].value == self.word[self.board.ships[i].grid_x - self.left_offset]:
                        self.board.ships[i].set_display_check(True)
                    else:
                        self.board.ships[i].set_display_check(False)

    def auto_check_reset(self):
        for each in self.board.ships:
            each.update_me = True
            each.set_display_check(None)

    def update(self, game):
        game.fill(self.color)
        gd.BoardGame.update(self, game)

    def check_result(self, auto=False):

        result = [" " for i in range(self.data[0])]
        if self.board.grid[self.sol_grid_y] == self.solution_grid:
            for i in range(1, len(self.board.ships)):
                if self.board.ships[i].grid_y == self.sol_grid_y:
                    result[self.board.ships[i].grid_x] = self.board.ships[i].value
            re = "".join(result)
            re = re.strip()
            if self.word == re:
                self.auto_check()
                self.level.next_board()
            else:
                if auto:
                    self.auto_check()
                else:
                    self.level.try_again()
        else:
            if auto:
                self.auto_check_reset()
            else:
                self.level.try_again()
