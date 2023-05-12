import line


def get_line_lens(buffer: list[line.Line]) -> list[int]:
    line_nums = []
    for current_line in buffer:
        line_nums.append(len(current_line.split_line()))

    return line_nums



def get_line_nums(line_lens):
    line_nums = []
    for i in range(len(line_lens)):
        line_nums.append(sum(line_lens[:i]))
    
    return line_nums



class LineNumbers():
    def __init__(self, buffer):
        self.line_lens = get_line_lens(buffer)
        self.line_nums = get_line_nums(self.line_lens)

    
    def update(self, buffer):
        self.line_lens = get_line_lens(buffer)
        self.line_nums = get_line_nums(self.line_lens)
