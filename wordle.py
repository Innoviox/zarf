import zarf
import string
import random
import collections

class Wordle():
    def __init__(self, word):
        self.word = word

        self.pattern = ["." for _ in range(len(word))]

        # self.known = collections.defaultdict(int)
        self.in_word = []
        self.out = ['' for _ in range(len(word))]

    def evaluate(self, guess):
        out = ['' for _ in range(len(guess))]
        for i, (a, b) in enumerate(zip(guess, self.word)):
            if a == b:
                out[i] = 'G'
                self.pattern[i] = a
                # self.known[a] += 1
                if a in self.in_word:
                    self.in_word.remove(a)
                # for j in range(len(guess)):
                #     self.out[j] += a

        for i, (a, b) in enumerate(zip(guess, self.word)):
            if out[i] == '':
                # if self.word.count(a) > self.known[a]:
                if a in self.word:
                    out[i] = 'Y'
                    if a not in self.in_word:
                        self.in_word.append(a)
                    # self.known[a] += 1
                    self.out[i] += a
                else:
                    out[i] = 'B'
                    for j in range(len(guess)):
                        self.out[j] += a

        self.out = [''.join(sorted(list(set(i)))) for i in self.out] # for debugging
        print(guess, ''.join(out))
        return out

    def make_pattern(self):
        return ['^' + ''.join('[^' + a + ']' if (b == '.' and a != '') else b for a, b in zip(self.out, self.pattern)) + '$'] + \
               ['@' + i + '@' for i in self.in_word]

    def wordle(self):
        i = 0
        while True:
            i += 1
            p = self.make_pattern()
            # print(p) # for debugging
            options = zarf.multisearch('p' * len(p), p)
            # print(len(options))
            if all(i == 'G' for i in self.evaluate(random.choice(options))):
                print(i)
                return i

Wordle("SHARD").wordle()

'''
BRIAR
'''
