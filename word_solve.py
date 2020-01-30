from string import ascii_uppercase
import pickle, random, statistics
import tqdm
board = ['TRUD', 'IESM', 'LEWO', 'TSLN']
board = ['NOUC', 'EURO', 'LLTD', 'ETAA']
board = 'FSNCBETHAEPOSLRR'
board_of = lambda s: [list(s[i:i+4]) for i in range(0, len(s), 4)]
scores = {
    3: 100,
    4: 400,
    5: 800,
    6: 1400,
    7: 1700,
    8: 2000
}

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

    def __str__(self):
        return self.valie

    def __repr__(self):
        return self.value

class Dawg:
    def __init__(self):
        self.top_node = Node(None, '#')
        for i in tqdm.tqdm(ascii_uppercase):
            for j in ascii_uppercase:
                for word in open(f"resources/{i}{j}.txt").readlines():
                    current = self.top_node
                    for letter in word[:-1]:
                        current = current.add(letter)
                    current.add('@')

    def trawl(self, s):
        current = self.top_node
        for i in s:
            current = current.next(i)
            if current is None:
                return False
        return current


# 

def _solve(board, current_node, current_prefix, prev):
    if len(current_prefix) > 2 and current_node.valid():
        yield current_prefix
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0: continue

            p = (prev[-1][0] + dx, prev[-1][1] + dy)
            if p in prev: continue
            if not(0 <= p[0] < 4 and 0 <= p[1] < 4): continue

            s = board[p[0]][p[1]]
            if next_node := current_node.next(s):
                yield from _solve(board, next_node, current_prefix + s, prev + [p])

def solve(board):
    for (i, row) in enumerate(board):
        for (j, col) in enumerate(row):
            yield from _solve(board, dawg.trawl(col), col, [(i, j)])

if __name__ == "__main__":
    dawg = pickle.load(open("dawg", "rb"))
    print("Loaded dawg from pickle")
    
    import sys

    board = 'NMIBJTROEHGADEDI'
    board = sys.argv[1]
    board = board_of(board)


    a=list(set(solve(board)))

    print(len(a), sum([scores[len(i)] for i in a]))
    for i in range(3, len(max(a, key=len)) + 1):
        print(i, [j for j in a if len(j) == i])
else:
    dawg = Dawg()

##games = []
##boards = []
##for _ in range(1000):
##    board = ''.join(random.choice(ascii_uppercase) for _ in range(16))
##    boards.append(board)
##    board = [list(board[i:i+4]) for i in range(0, len(board), 4)]
##    games.append(sum([scores.get(len(i), 0) for i in list(set(solve(board)))]))
##
##print(statistics.mean(games))
