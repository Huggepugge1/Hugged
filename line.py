class Line:
    def __init__(self, line_num: int, line: str, max_line_len: int) -> None:
        self.line_num = line_num 
        self.line = line
        self.max_line_len = max_line_len


    def split_line(self) -> [str]:
        splitted_line = [""]
        for c in self.line:
            if len(splitted_line[-1]) == self.max_line_len:
                splitted_line.append("")
            splitted_line[-1] += c

        return splitted_line
