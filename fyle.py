import cursor
import line
import curses

def get_line_nums(buffer: list[line.Line], max_line_len: int) -> list[int]:
    line_nums = []
    for current_line in buffer:
        line_nums.append(len(current_line.split_line(max_line_len)))

    return line_nums

class File: 
    def __init__(self, name: str, cursor: cursor.Cursor, buffer: list[line.Line], max_line_len: int) -> None:
        self.name         = name
        self.cursor       = cursor
        self.buffer       = buffer
        self.max_line_len = max_line_len
        self.lines        = get_line_nums(self.buffer, self.max_line_len) 


    def update_lines(self):
        self.lines = get_line_nums(self.buffer, self.max_line_len)
    

    def get_pos(self) -> (int, int):
        self.update_lines()
        current_pos = 0
        current_row = 0

        while self.cursor.row > current_pos:
            current_row += 1
            current_pos += self.lines[current_row]


        return (current_row - (self.cursor.row - current_pos), self.cursor.col + (self.cursor.row - current_pos) * self.max_line_len)

        
    def split_row(self, row: int = -1, col: int = -1) -> (str, str):
        if row == -1:
            row = self.get_pos()[0]
        if col == -1:
            col = self.get_pos()[1]

        return (self.buffer[row].line[:col], self.buffer[row].line[col:])

    
    def get_line(self, row: int = -1) -> str:
        if row == -1:
            row = self.get_pos()[0]
        
        return self.buffer[row].line
