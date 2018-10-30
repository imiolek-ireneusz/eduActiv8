class Layout:
    def __init__(self, mainloop, screen_w, screen_h, x_count=0, y_count=0, game_type="Board"):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.mainloop = mainloop
        self.sizer = self.mainloop.sizer
        self.game_type = game_type
        self.x_count = x_count
        self.y_count = y_count
        self.update_layout(x_count, y_count)

    def update_layout(self, x_count=0, y_count=0):
        self.mainloop.sb.update_me = True
        self.x_count = x_count
        self.y_count = y_count
        self.top_margin = self.sizer.top_margin
        self.bottom_margin = self.sizer.bottom_margin
        scale_x = (self.screen_w - self.sizer.grid_line_w - 6) // x_count
        scale_y = (self.screen_h - self.sizer.grid_line_w - self.sizer.top_margin - self.bottom_margin) // y_count
        if scale_x < scale_y:
            self.scale = scale_x
        else:
            self.scale = scale_y
        self.game_margin = (self.screen_w - self.scale * x_count - self.sizer.grid_line_w) // 2
        self.game_left = self.game_margin
        self.game_right = self.screen_w - self.game_margin
        self.width = self.scale  # width of a single square
        self.height = self.scale
        self.game_h = y_count * self.height + self.sizer.grid_line_w
        self.game_w = self.scale * x_count  # - self.grid_line_w #self.menu_w
        self.game_pos = (self.game_left, self.sizer.top_margin, self.game_w, self.game_h)  # changed
        self.info_bar_pos = (0, self.sizer.top_margin - self.sizer.info_bar_h, self.screen_w, self.sizer.info_bar_h)
        self.score_bar_pos = (0, 0, self.screen_w, self.sizer.score_bar_h)
        self.info_top = self.sizer.top_margin - self.sizer.info_bar_h  # self.game_h + self.info_bar_pos[1] + self.top_margin
        self.game_bg_pos = (0, self.sizer.top_margin, self.screen_w, self.screen_h - self.sizer.top_margin)

        if self.mainloop.layout is not None:
            self.mainloop.recreate_game_screen()

        self.mainloop.redraw_needed = [True, True, True]

    def draw_layout(self):
        pass

    def update_layout_fs(self, screen_w, screen_h, x_count, y_count):
        # update layout after switching from fullscreen to windowed view
        self.game_type = self.mainloop.game_board.game_type
        self.__init__(self.mainloop, screen_w, screen_h, x_count, y_count, self.game_type)
