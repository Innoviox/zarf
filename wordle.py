import zarf
import string
import random
import collections
import tqdm
import statistics

class Wordle():
    def __init__(self, word):
        self.word = word

        self.pattern = ["." for _ in range(len(word))]

        # self.known = collections.defaultdict(int)
        self.in_word = []
        self.out = ['' for _ in range(len(word))]

    def evaluate(self, guess):
        out = ['' for _ in range(len(guess))]
        known = collections.defaultdict(int)
        for i, (a, b) in enumerate(zip(guess, self.word)):
            if a == b:
                out[i] = '🟩'
                self.pattern[i] = a
                # self.known[a] += 1
                if a in self.in_word:
                    self.in_word.remove(a)
                # for j in range(len(guess)):
                #     self.out[j] += a

        for i, (a, b) in enumerate(zip(guess, self.word)):
            if out[i] == '':
                if self.word.count(a) > known[a]:
                # if a in self.word:
                    out[i] = '🟨'
                    if a not in self.in_word:
                        self.in_word.append(a)
                    known[a] += 1
                    self.out[i] += a
                else:
                    out[i] = '⬛'
                    if known[a] == 0:
                        for j in range(len(guess)):
                            self.out[j] += a


        self.out = [''.join(sorted(list(set(i)))) for i in self.out] # for debugging
        # print(guess, ''.join(out))
        return out

    def make_pattern(self):
        return ['^' + ''.join('[^' + a + ']' if (b == '.' and a != '') else b for a, b in zip(self.out, self.pattern)) + '$'] + \
               ['@' + i + '@' for i in self.in_word]

    def wordle(self):
        i = 0
        while True:
            i += 1
            if all(i == '🟩' for i in self.evaluate(random.choice(self.options()))):
                print(i)
                return i

    def with_guesses(self, *guesses):
        for g in guesses:
            self.evaluate(g)
        return self

    def options(self):
        p = self.make_pattern()
        options = zarf.multisearch('p' * len(p), p, realret=True)
        return options

fives = open("sedecordle_wordlist").read().split()

class Multicordle():
    def __init__(self, words):
        self.wordles = [Wordle(i.upper()) for i in words]
        self.outputs = [[] for _ in range(len(words))]
        self.solved = [False for _ in range(len(words))]

    @staticmethod
    def random(n=16, length=5):
        # words = random.sample(zarf.search('p', '^' + '.' * length + '$', realret=True), n)
        words = random.sample(fives, n)
        return Multicordle(words)

    def evaluate(self, guess, out=True):
        output = [''.join(w.evaluate(guess)) for w in self.wordles]
        
        for i in range(len(output)):
            if i % 2 == 0:
                end = " "
            else:
                end = "\n"

            o = output[i]
            self.outputs[i].append(guess + " " + o)
            if not self.solved[i]:
                if o == '🟩🟩🟩🟩🟩':
                    if out: print("solved", self.wordles[i].word)
                    self.solved[i] = True
                elif out and len((opts := self.wordles[i].options())) == 1:
                    print(i + 1, opts)

            if out: print(o, end=end)

    def wordle(self):
        i = 0
        while True:
            i += 1
            x = input("Word? ")
            if x == "O":
                for i in range(0, len(self.wordles), 2):
                    print(len(self.wordles[i].options()), len(self.wordles[i + 1].options()))
            elif x == "S":
                n = -1
                while n != 0:
                    n = 0
                    for j in range(len(self.wordles)):
                        if not self.solved[j] and len((opts := self.wordles[j].options())) == 1:
                            n += 1
                            print("solving", opts[0])
                            self.evaluate(opts[0], out=False)
                        
            elif all(j.isdigit() for j in x):
                print("\n".join(self.outputs[int(x) - 1]))
            else:
                self.evaluate(x, out=False)

            if all(self.solved):
                print("solved!")
                return

    def test(self, words):
        for i in words:
            self.evaluate(i, out=False)

        n = -1
        while n != 0:
            n = 0
            for j in range(len(self.wordles)):
                if not self.solved[j] and len((opts := self.wordles[j].options())) == 1:
                    n += 1
                    self.evaluate(opts[0], out=False)

        return sum(self.solved)
        
# Wordle("BUTTE").wordle()
# i = []
# for x in tqdm.trange(1000):
#     i.append(Multicordle.random(n=16).test(['GROUT', 'CHAIN', 'MELDS']))

# print(i)
# print(statistics.mean(i))
import matplotlib.pyplot as plt
import ast
x = ast.literal_eval(open("1000_gcm.txt").read())
plt.hist(x, bins=max(x) - min(x) + 1)
plt.show()
