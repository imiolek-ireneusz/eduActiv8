class Layout:
    def __init__(self, mainloop, screen_w, screen_h, x_count=26, y_count=11, game_type="Board"):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.mainloop = mainloop
        self.game_type = game_type
        self.update_layout(x_count, y_count)

    def update_layout(self, x_count=0, y_count=0):

        self.mainloop.sb.update_me = True
        self.x_count = x_count
        self.y_count = y_count
        if self.mainloop.android is None:
            self.score_bar_h = 36
        else:
            self.score_bar_h = 56

        self.menu_w = 166 + 26 + 12  # 124 #+5 - extra space to make the gap for tabs to look ok
        self.menu_a_w = self.menu_w
        # 50+10+50+10+1
        self.grid_line_w = 1
        self.info_bar_h = 90  # 76
        self.info_bar_offset_h_init = 80  # 76

        self.top_margin = self.score_bar_h + self.info_bar_h

        # self.info_bar_m_top = 10 #margin top - moved to info_bar
        self.menu_w_offset = 0
        self.avail_game_w = self.screen_w - self.menu_w - 10
        self.avail_game_h = self.screen_h - self.top_margin  # - self.info_bar_h
        # self.score_bar_h = 0 #32
        if self.game_type == "Board":
            # find the right size (scale) for a single square and calculate panels' sizes
            scale_x = (self.screen_w - self.menu_w - self.grid_line_w - 6) // x_count
            scale_y = (self.screen_h - self.grid_line_w - self.top_margin) // y_count

            if scale_x < scale_y:
                self.scale = scale_x
            else:
                self.scale = scale_y

            self.menu_w_offset = 0  # (self.screen_w - self.menu_w) - self.scale*x_count - self.grid_line_w#(screen_w - menu_w) % x_count

            # self.game_bg_l = ((self.screen_w - self.menu_w) - self.scale*x_count - self.grid_line_w)
            self.game_margin = ((self.screen_w - self.menu_w) - self.scale * x_count - self.grid_line_w) // 2

            self.game_left = self.menu_w + self.game_margin

            self.game_right = self.screen_w - self.game_margin

            self.menu_w_offset = ((self.screen_w - self.menu_w) - self.scale * x_count - self.grid_line_w) // 2
            # self.menu_w += self.menu_w_offset
            self.width = self.scale  # width of a single square
            self.height = self.scale
            self.game_h = y_count * self.height + self.grid_line_w

        elif self.game_type == "Puzzle":
            self.game_h = self.screen_h - self.top_margin  # - self.info_bar_h

        self.game_w = self.scale * x_count  # - self.grid_line_w #self.menu_w
        self.info_bar_offset_h = self.screen_h - self.game_h - self.top_margin
        self.score_bar_top = 0  # self.info_bar_offset_h - self.info_bar_h - self.top_margin
        self.menu_pos = (0, 0, self.menu_w, self.screen_h)

        self.menu_l_w = 96
        self.menu_r_w = 70 + 26 + 12 # self.menu_w - self.menu_l_w
        self.menu_l_pos = (0, 0, self.menu_l_w, self.screen_h)
        self.menu_r_pos = (self.menu_l_w, 0, self.menu_r_w, self.screen_h)
        # self.game_pos = (self.menu_w,0, self.game_w, self.game_h) #changed
        # self.game_pos = (self.menu_w,self.top_margin, self.game_w, self.game_h) #changed
        self.game_pos = (self.game_left, self.top_margin, self.game_w, self.game_h)  # changed

        #self.misio_pos = (0, 0, 204, 146)
        self.misio_pos = (0, 0, 204, 120)
        """
        self.info_bar_offset_pos = (self.menu_w - self.menu_w_offset, self.game_h+self.top_margin, self.game_w + self.menu_w_offset, self.info_bar_offset_h)
        self.info_bar_pos = (1, self.info_bar_offset_h - self.info_bar_h, self.game_w - 1 + self.menu_w_offset, self.info_bar_h)
        self.score_bar_pos = (self.menu_w - self.menu_w_offset, 0, self.game_w + self.menu_w_offset, self.score_bar_h)
        self.info_top = self.game_h + self.info_bar_pos[1] + self.top_margin
        """
        # self.info_bar_offset_pos = (self.menu_w, self.game_h+self.top_margin, self.screen_w - self.menu_w, self.info_bar_offset_h)
        self.info_bar_pos = (
        self.menu_w, self.top_margin - self.info_bar_h, self.screen_w - self.menu_w, self.info_bar_h)
        self.score_bar_pos = (self.menu_w, 0, self.screen_w - self.menu_w, self.score_bar_h)
        self.info_top = self.top_margin - self.info_bar_h  # self.game_h + self.info_bar_pos[1] + self.top_margin
        self.game_bg_pos = (self.menu_w, self.top_margin, self.screen_w - self.menu_w, self.screen_h - self.top_margin)
        self.dialogwnd_w = 620
        self.dialogwnd_h = 400
        self.dialogwnd_pos = (
        (self.screen_w - self.menu_w - self.dialogwnd_w) // 2 + self.menu_w, (self.screen_h - self.dialogwnd_h) // 2,
        self.dialogwnd_w, self.dialogwnd_h)
        self.dialogbg_pos = (0, 0, self.screen_w, self.screen_h)

        self.mainloop.redraw_needed = [True, True, True]

    def draw_layout(self):
        pass

    def update_layout_fs(self, screen_w, screen_h, x_count, y_count):
        # update layout after switching from fullscreen to windowed view
        self.game_type = self.mainloop.game_board.game_type
        self.__init__(self.mainloop, screen_w, screen_h, x_count, y_count, self.game_type)
        # self.mainloop.m.update_scroll_pos()
