class Cursor:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def move_down(self):
        self.row += 1
    
    def move_up(self):
        if self.row > 0:
            self.row -= 1

    def move_right(self):
        self.col += 1
    
    def move_left(self):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.col = 0
            self.row -= 1

    def get_pos(self):
        return (self.row, self.col)
