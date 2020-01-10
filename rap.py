import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def gaddag(word):
    left = []
    right = list(word)

    while True:
        yield ''.join(reversed(left)) + '#' + ''.join(right) + '@'
        if right: left.append(right.pop(0))
        else: return

class Node:
    n = 0
    def __init__(self, text):
        self.text = text
        self.nexts = []
        self.n = Node.n
        Node.n += 1
        self.end = False

    def add(self, l):
        if l.text == '@':
            self.end = True
            return
        k = [i for i in self.nexts if i.text == l.text]
        if k:
            return k[0]
        self.nexts.append(l)
        return l

    def __str__(self): return self.text
    def __repr__(self): return self.text

    def all_children(self):
        x = [self]
        for i in self.nexts:
            x.extend(i.all_children())
        return x

class Gaddag:
    def __init__(self):
        self.root = Node('')

    def add(self, word):
        for i in gaddag(word):
            curr = self.root
            for l in i:
                curr = curr.add(Node(l))

    def __str__(self):
        s = ""
        return s

    def to_nx(self):
        G = nx.Graph()
        labels = {}
        pos = {}
        
        def add_to_nx(node, depth):
            node.depth = depth
            labels[node.n] = node.text
            for n in node.nexts:
                labels[n.n] = n.text
                G.add_edge(node.n, n.n)
                add_to_nx(n, depth + 1)

        add_to_nx(self.root, 0)

        c = self.root.all_children()
        n_at_depth = defaultdict(list)
        for n in c:
            n_at_depth[n.depth].append(n)

        max_n = max(n_at_depth)
        for n, ns in n_at_depth.items():
            for i, node in enumerate(ns):
                pos[node.n] = (n, i / len(ns))

        pos[0] = (0, 2/5)

        colors = ['red' if i.end else 'blue' for i in c]

        return G, labels, pos, colors


words = [
    "CAR",
    "CARS",
    "CAT",
    "CATS",
    "DO",
    "DOG",
    "DOGS",
    "DONE",
    "EAR",
    "EARS",
    "EAT",
    "EATS"
] # 100/7

words = ["CARE"]

import zarf

words = zarf.search('b', 'PEARLS')
print(words)

g = Gaddag()
for w in words:
    g.add(w)
G, labels, pos, colors = g.to_nx()
# pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=100, node_color=colors)
nx.draw_networkx_labels(G, pos, labels, font_color='white', font_size=7)
plt.savefig("gaddag.png", dpi=300)
plt.show()
