class Cursor:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def move_down(self, col):
        self.col = col
        self.row += 1
    
    def move_up(self):
        if self.row > 0:
            self.row -= 1

    def move_right(self, wrap):
        if wrap:
            self.row += 1
            self.col = 0
        else:
            self.col += 1
    
    def move_left(self, line_len):
        if self.col > 0:
            self.col -= 1
        else:
            self.col = line_len
            self.row -= 1

    def get_pos(self):
        return (self.row, self.col)
