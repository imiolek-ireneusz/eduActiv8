# -*- coding: utf-8 -*-

class Sizer:
    def __init__(self, mainloop, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.mainloop = mainloop
        if self.mainloop.android is None:
            self.score_bar_h = 36
        else:
            self.score_bar_h = 56
        self.grid_line_w = 1
        self.info_bar_h = 90  # 76
        self.info_bar_offset_h_init = 80  # 76
        self.top_margin = self.score_bar_h + self.info_bar_h
        self.bottom_margin = 10
        self.avail_game_w = self.screen_w - 10
        self.avail_game_h = self.screen_h - self.top_margin - self.bottom_margin # - self.info_bar_h
        self.info_bar_offset_h = self.screen_h - self.avail_game_h - self.top_margin
        self.score_bar_top = 0  # self.info_bar_offset_h - self.info_bar_h - self.top_margin
        self.game_bg_pos = (0, self.top_margin, self.screen_w, self.screen_h - self.top_margin)
        self.info_bar_pos = (0, self.top_margin - self.info_bar_h, self.screen_w, self.info_bar_h)
        self.score_bar_pos = (0, 0, self.screen_w, self.score_bar_h)
        self.info_top = self.top_margin - self.info_bar_h  # self.game_h + self.info_bar_pos[1] + self.top_margin
        self.game_bg_pos = (0, self.top_margin, self.screen_w, self.screen_h - self.top_margin)
        self.dialogwnd_w = 620
        self.dialogwnd_h = 400
        self.dialogwnd_pos = ((self.screen_w - self.dialogwnd_w) // 2, (self.screen_h - self.dialogwnd_h) // 2,
                              self.dialogwnd_w, self.dialogwnd_h)
        self.dialogbg_pos = (0, 0, self.screen_w, self.screen_h)

    def update_sizer(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.avail_game_w = self.screen_w - 10
        self.avail_game_h = self.screen_h - self.top_margin - self.bottom_margin  # - self.info_bar_h
        self.game_bg_pos = (0, self.top_margin, self.screen_w, self.screen_h - self.top_margin)
        self.info_bar_pos = (0, self.top_margin - self.info_bar_h, self.screen_w, self.info_bar_h)
        self.score_bar_pos = (0, 0, self.screen_w, self.score_bar_h)
        self.info_top = self.top_margin - self.info_bar_h  # self.game_h + self.info_bar_pos[1] + self.top_margin
        self.game_bg_pos = (0, self.top_margin, self.screen_w, self.screen_h - self.top_margin)
        self.dialogwnd_pos = ((self.screen_w - self.dialogwnd_w) // 2, (self.screen_h - self.dialogwnd_h) // 2,
                              self.dialogwnd_w, self.dialogwnd_h)
        self.dialogbg_pos = (0, 0, self.screen_w, self.screen_h)
