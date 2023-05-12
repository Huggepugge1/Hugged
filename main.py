#!/usr/bin/env python3
import curses
import cursor
import fyle
import line
import sys
import os

NUMBER_OFFSET = 5


def print_buffer(stdscr, current_file: fyle.File):
    current_file.update_lines()
    stdscr.clear()
    buf = []
    for current_line in current_file.buffer:
        for subline in current_line.split_line():
            buf.append(subline)
        
    for i, line in enumerate(buf):
        stdscr.addstr(i, NUMBER_OFFSET, line)

    for i, line_num in enumerate(current_file.line_nums.line_nums):
        stdscr.addstr(line_num, 0, str(i + 1))


def process_input(key: str, current_file: fyle.File, stdscr):
    if len(key) == 1 and ord(key) == 5:
        with open(current_file.name, "w") as f:
            if current_file.buffer[-1].line != "":
                f.write("\n".join(map(lambda x: x.line, current_file.buffer)) + "\n")
            
            else:
                f.write("\n".join(map(lambda x: x.line, current_file.buffer)))
        
        curses.endwin()
        exit(0)

    elif key == "\n":
        row, col = current_file.get_pos()
        current_line = current_file.split_row()

        current_file.buffer[row].line = current_line[0]
        current_file.buffer.insert(row + 1, line.Line(row + 1, current_line[1], stdscr.getmaxyx()[1] - NUMBER_OFFSET))
        current_file.cursor.move_down(0)
        
        return current_file

    elif key == "KEY_DOWN": 
        row, col = current_file.cursor.get_pos()
        if row < len(current_file.buffer) - 1:
            current_file.cursor.move_down(min(len(current_file.get_line(row + 1)), col))
        return current_file
    
    elif key == "KEY_UP":
        row, col = current_file.cursor.get_pos()
        if row > 0:
            current_file.cursor.move_up()
        
        if col > len(current_file.get_line()):
            current_file.cursor.col = len(current_file.get_line())

        return current_file
    
    elif key == "KEY_RIGHT":
        row, col = current_file.cursor.get_pos()
        if row + 1 < len(current_file.buffer):
            current_file.cursor.move_right(col == len(current_file.get_line()))
        
        elif col < len(current_file.get_line()):
            current_file.cursor.move_right(False)
        
        return current_file
    
    elif key == "KEY_LEFT":
        row, col = current_file.cursor.get_pos()
        if row > 0:
            current_file.cursor.move_left(len(current_file.get_line(row - 1)))
        
        elif col > 0:
            current_file.cursor.move_left(0)

        return current_file
 
    elif key == "KEY_BACKSPACE":
        row, col = current_file.get_pos()
        line_len = len(current_file.get_line(row - 1))
        if col == 0:
            if row > 0:
                current_file.buffer[row - 1].line += current_file.get_line()
                current_file.buffer.pop(row)
        
        else:
            current_line = current_file.split_row()
            current_file.buffer[row].line = current_line[0][:-1] + current_line[1]

        if row > 0:
            current_file.cursor.move_left(line_len)
        
        elif col > 0:
            current_file.cursor.move_left(0)
        
        return current_file

    elif len(key) == 1:
        row, col = current_file.get_pos()

        if col < len(current_file.get_line()):
            current_line = current_file.split_row()
            current_file.buffer[row].line = current_line[0] + key + current_line[1]
            
        else:    
            current_file.buffer[row].line += key
            
        current_file.cursor.move_right((col + 1) % (stdscr.getmaxyx()[1] - NUMBER_OFFSET) == 0)
        return current_file

    else:
        return current_file
    

def split_file(fyle: str, stdscr) -> [line.Line]:
    buf = []
    for line_num, current_line in enumerate(fyle.split("\n")):
        buf.append(line.Line(line_num, current_line, stdscr.getmaxyx()[1] - NUMBER_OFFSET))

    return buf


def main(stdscr):
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r") as f:
            current_file = fyle.File(sys.argv[1], cursor.Cursor(0, 0), split_file(f.read(), stdscr), stdscr.getmaxyx()[1] - NUMBER_OFFSET)

    else:
        current_file = fyle.File(sys.argv[1], cursor.Cursor(0, 0), [line.Line(0, "", stdscr.getmaxyx()[1] - NUMBER_OFFSET)], stdscr.getmaxyx()[1] - NUMBER_OFFSET)

    print_buffer(stdscr, current_file)

    while True:
        current_file.update_lines()
        print_buffer(stdscr, current_file)
        stdscr.move(current_file.cursor.row, current_file.cursor.col + NUMBER_OFFSET)
        key = stdscr.getkey()
        current_file = process_input(key, current_file, stdscr)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: ./main.py <filename>")
        exit(1)
    
    curses.wrapper(main)
