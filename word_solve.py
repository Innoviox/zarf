from string import ascii_uppercase

board = [
    'T', 'R', 'U', 'D',
    'I', 'E', 'S', 'M',
    'L', 'E', 'W', 'O',
    'T', 'S', 'L', 'N'
]

class Node:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
        self.nexts = []

    def add(self, value):
        if n := self.next(value):
            return n
        n = Node(self, value)
        self.nexts.append(n)
        return n

    def next(self, value):
        for i in self.nexts:
            if i.value == value:
                return i
        return None

    def valid(self):
        return bool(self.next('@'))

class Dawg:
    def __init__(self):
        self.top_node = Node(None, '#')
        for i in ascii_uppercase:
            for j in ascii_uppercase:
                current = self.top_node
                for word in open(f"resources/{i}{j}.txt"):
                    for letter in word:
                        current = current.add(letter)
                    current.add('@')

    def trawl(self, s):
        current = self.top_node
        for i in s:
            if current := current.next(i):
                continue
            return False
        return current

dawg = Dawg()
print("Dawg loaded")

def _solve(board, current_node, current_prefix, current_pos):
    if current_node.valid():
        yield current_prefix
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0: continue
            p = (current_pos[0] + dx, current_pos[1] + dy)
            if not(0 <= p[0] < 4 and 0 <= p[1] < 4): continue
            print(board, p)
            s = board[p[0]][p[1]]
            if next_node := current_node.next(s):
                yield from _solve(board, next_node, current_prefix + s, p)

def solve(board):
    for (i, row) in enumerate(board):
        for (j, col) in enumerate(row):
            yield from _solve(board, dawg.trawl(col), col, (i, j))

print(list(solve(board)))
    
