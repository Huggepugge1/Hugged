import curses
import cursor
import fyle

def process_input(key: str, current_file: fyle.File, stdscr):
    stdscr.addstr(1, 0, str(ord('\n')))
    stdscr.addstr(0, 0, " ".join(list(map(lambda x: str(ord(x)), key))))
    if key == "\n":
        row, col = current_file.cursor.get_pos()
        current_line = current_file.split_row(row, col)

        current_file.buffer[row] = current_line[0]
        current_file.buffer.insert(row + 1, current_line[1])
        current_file.cursor.move_down()

        row, col = current_file.cursor.get_pos()
        current_file.cursor.col = 0
        
        stdscr.clear()
        for row, row_content in enumerate(current_file.buffer):
            stdscr.addstr(row, 0, row_content)
        
        return current_file

    elif key == "KEY_DOWN":
        if current_file.cursor.row < len(current_file.buffer) - 1:
            current_file.cursor.move_down()
        return current_file
    
    elif key == "KEY_UP":
        row, col = current_file.cursor.get_pos()
        if row > 0:
            current_file.cursor.move_up()
        
        row, col = current_file.cursor.get_pos()
        if col > len(current_file.buffer[row]):
            current_file.cursor.col = len(current_file.buffer[row])

        return current_file
    
    elif key == "KEY_RIGHT":
        _, max_cols = stdscr.getmaxyx()

        current_file.cursor.move_right()
        row, col = current_file.cursor.get_pos()
        if col < max_cols and col > len(current_file.buffer[row]):
            current_file.add_space()
        
        if col >= max_cols:
            if len(current_file.buffer) > row:
                current_file.cursor.col = 0
                current_file.cursor.move_down()
            
            else:
                current_file.cursor.move_left()
        
        return current_file
    
    elif key == "KEY_LEFT":
        current_file.cursor.move_left()
        return current_file
 
    elif key == "KEY_BACKSPACE":
        row, col = current_file.cursor.get_pos()
        current_line = current_file.split_row(row, col)
        current_file.buffer[row] = current_line[0][:-1] + current_line[1]
        
        _, max_cols = stdscr.getmaxyx() 
        stdscr.addstr(row, 0, " " * max_cols)
        stdscr.addstr(row, 0, current_file.buffer[row])

        current_file.cursor.move_left()
        return current_file

    else: 
        row, col = current_file.cursor.get_pos()
        if col < len(current_file.buffer[row]):
            current_line = current_file.split_row(row, col)
            current_file.buffer[row] = current_line[0] + key + current_line[1]
            
            _, max_cols = stdscr.getmaxyx() 
            stdscr.addstr(row, 0, " " * max_cols)
            stdscr.addstr(row, 0, current_file.buffer[row])
        
        else:    
            current_file.buffer[row] += key
            stdscr.addstr(row, col, key)
            
        current_file.cursor.move_right()
        return current_file
    

def main(stdscr):
    current_file = fyle.File("", cursor.Cursor(0, 0), [""])
    while True:
        stdscr.move(current_file.cursor.row, current_file.cursor.col)
        key = stdscr.getkey()
        current_file = process_input(key, current_file, stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
