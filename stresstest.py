#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# To run this test uncomment the stresstest.step(self) line in the run method in the eduactiv8.py file
# just under the line "while self.done is False:".
# This will attempt to start all games and levels in all languages as well as in all colour schemes
# Running this test will take a good while it's nearly 300 games in 15 languages in 4 colour schemes
# and then there are quite a few levels in each activity, which means thousands of activities being started.

run_counter = 0
current_id = 0
prev_lang = 18
current_lang = 0
schemes = [None, "WB", "BW", "BY"]
current_scheme = 0
test_lang = False


def lang_selection(ml):
    ml.m.start_hidden_game(ml.m.games[3].item_id)


def next_language(ml, lng):
    ml.game_board.change_language(ml.game_board.languages[lng], ml.game_board.lang_titles[lng], lng)
    print("testing language id = %i" % lng)


def next_scheme(ml):
    global run_counter
    global prev_lang
    global current_lang
    global current_scheme
    global schemes
    # set run counter to the last number so that the language gets changed
    run_counter = len(ml.m.games)
    current_lang = 0
    if current_scheme < 3:
        current_scheme += 1
        ml.switch_scheme(schemes[current_scheme])
        print("testing theme id = ", schemes[current_scheme])


def step(ml):
    global run_counter
    global current_lang
    global prev_lang
    global schemes
    global current_scheme
    global test_lang

    if ml.game_board is not None:
        if ml.game_board.level.lvl < ml.game_board.level.lvl_count:
            ml.game_board.level.lvl += 1
            ml.game_board.level.load_level_plus(None)
        else:
            if run_counter < len(ml.m.games):
                # test all games
                ml.m.start_hidden_game(ml.m.games[run_counter].item_id)
                ml.game_board.level.lvl = 1
            elif run_counter == len(ml.m.games):
                if test_lang and current_lang < len(ml.config.ok_lng)-1:
                    # change language
                    current_lang += 1
                    lang_selection(ml)
                else:
                    # change colour theme
                    next_scheme(ml)
                    if not test_lang:
                        run_counter = -1
            else:
                if test_lang and current_lang != prev_lang:
                    # process language change
                    prev_lang = current_lang
                    next_language(ml, current_lang)
                    run_counter = -1

            run_counter += 1
