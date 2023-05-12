import cursor
import line
import curses
import lineNumbers


class File: 
    def __init__(self, name: str, cursor: cursor.Cursor, buffer: list[line.Line], max_line_len: int) -> None:
        self.name                  = name
        self.cursor                = cursor
        self.buffer                = buffer
        self.max_line_len          = max_line_len
        self.line_nums          = lineNumbers.LineNumbers(self.buffer)


    def update_lines(self):
        self.line_nums.update(self.buffer)
    
    
    def get_pos(self) -> (int, int):
        current_pos = 0
        current_row = -1

        for line_num in self.line_nums.line_nums:
            if line_num <= self.cursor.row:
                current_row += 1
                current_pos = line_num
            else:
                break

        return (current_row, self.cursor.col + (self.cursor.row - current_pos) * self.max_line_len)

        
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
