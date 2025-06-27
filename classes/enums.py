# -*- coding: utf-8 -*-

from enum import IntEnum #, Enum

class MenuLevel(IntEnum):
    HOME = 0
    CATEGORIES = 1
    SUB_CATEGORIES = 2
    GAMES_IN_CATEGORY = 3
    GAME = 4

class DialogType(IntEnum):
    EXIT_GAME = 0
    LOGOUT = 1
    INFO_ONLY = 2
    CUSTOM_FUNCTION = 3

class GamePlayConfig(IntEnum):
    # --- Constants for GamePlay ---
    DEFAULT_WINDOWED_WIDTH = 800
    DEFAULT_WINDOWED_HEIGHT = 570
    SETTINGS_SAVE_DEBOUNCE_DELAY_SECONDS = 2
    RESIZE_DEBOUNCE_FRAMES = 15  # Number of frames to wait after last resize event before processing
    GAME_FPS = 30  # Frames per second for the game loop
