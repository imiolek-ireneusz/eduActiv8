# -*- coding: utf-8 -*-

# --- Constants for Sizer Dimensions ---
# These can be moved to a central config file if preferred,
# but defining them here makes the Sizer class self-contained for this example.
ANDROID_SCORE_BAR_HEIGHT = 56
DESKTOP_SCORE_BAR_HEIGHT = 36
INFO_BAR_HEIGHT = 90
BOTTOM_MARGIN = 10
GAME_HORIZONTAL_PADDING = 10 # Padding on left/right for the game area
DIALOG_WIDTH = 620
DIALOG_HEIGHT = 400

class Sizer:
    """
    Calculates and holds dimensions and positions for various UI elements
    based on the current screen resolution.
    """
    def __init__(self, mainloop, screen_w, screen_h):
        self.mainloop = mainloop

        # Initialize fixed dimensions based on platform
        self.score_bar_h = ANDROID_SCORE_BAR_HEIGHT if self.mainloop.android else DESKTOP_SCORE_BAR_HEIGHT
        self.grid_line_w = 1 # Width of grid lines, if any
        self.info_bar_h = INFO_BAR_HEIGHT
        self.bottom_margin = BOTTOM_MARGIN
        self.dialogwnd_w = DIALOG_WIDTH
        self.dialogwnd_h = DIALOG_HEIGHT

        # Calculate all dynamic dimensions and positions
        self._calculate_dimensions(screen_w, screen_h)

    def _calculate_dimensions(self, screen_w, screen_h):
        """
        Internal helper method to calculate and set all dynamic dimensions
        and positions based on the current screen width and height.
        This method is called during initialization and on every resize.
        """
        self.screen_w = screen_w
        self.screen_h = screen_h

        # Calculate margins
        self.top_margin = self.score_bar_h + self.info_bar_h

        # Calculate available space for the game content
        self.avail_game_w = self.screen_w - GAME_HORIZONTAL_PADDING
        self.avail_game_h = self.screen_h - self.top_margin - self.bottom_margin

        # Define positions (x, y, width, height) for various UI elements
        # Game background area (below info bar, extending to bottom)
        self.game_bg_pos = (0, self.top_margin, self.screen_w, self.screen_h - self.top_margin)

        # Info bar area (below score bar)
        self.info_bar_pos = (0, self.top_margin - self.info_bar_h, self.screen_w, self.info_bar_h)

        # Score bar area (at the very top)
        self.score_bar_pos = (0, 0, self.screen_w, self.score_bar_h)

        # Dialog window position (centered on screen)
        self.dialogwnd_pos = (
            (self.screen_w - self.dialogwnd_w) // 2,
            (self.screen_h - self.dialogwnd_h) // 2,
            self.dialogwnd_w,
            self.dialogwnd_h
        )

        # Full-screen background for dialogs
        self.dialogbg_pos = (0, 0, self.screen_w, self.screen_h)
        self.info_bar_offset_h_init = 80
        self.info_bar_offset_h = self.screen_h - self.avail_game_h - self.top_margin
        self.score_bar_top = 0
        self.info_top = self.top_margin - self.info_bar_h

    def update_sizer(self, screen_w, screen_h):
        """
        Updates the sizer's dimensions and positions when the screen size changes.
        This is the public method to be called from GamePlay.
        """
        self._calculate_dimensions(screen_w, screen_h)
