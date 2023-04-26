import cursor

class File:
    def __init__(self, name: str, cursor: cursor.Cursor, buffer: list[str]):
        self.name = name
        self.cursor = cursor
        self.buffer = buffer

    def add_space(self):
        self.buffer[self.cursor.row] += " "
        return self.buffer
        
    def split_row(self, row, col):
        return (self.buffer[row][:col], self.buffer[row][col:])
