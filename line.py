class Line:
    def __init__(self, line_num: int, line: str) -> None:
        self.line_num = line_num 
        self.line = line


    def split_line(self, max_len: int) -> [str]:
        splitted_line = [""]
        for c in self.line:
            if len(splitted_line) == max_len:
                splitted_line.append("")
            splitted_line[-1] += c

        return splitted_line
