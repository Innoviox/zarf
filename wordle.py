import zarf
import string
import random

class Wordle():
    def __init__(self, word):
        self.word = word

        self.pattern = list(".....")

        self.in_word = ''
        self.out = ['' for _ in range(5)]

    def evaluate(self, guess):
        clues = []
        for i, (a, b) in enumerate(zip(guess, self.word)):
            if a == b:
                print('G', end='')
                self.pattern[i] = a
            elif a in (self.word[:i] + self.word[i + 1:]):
                print('Y', end='')
                if a not in self.in_word:
                    self.in_word += a
                self.out[i] += a
            else:
                print('B', end='')
                for j in range(len(guess)):
                    self.out[j] += a
        
        print()

    def make_pattern(self):
        return ['^' + ''.join('[^' + a + ']' if (b == '.' and a != '') else b for a, b in zip(self.out, self.pattern)) + '$'] + \
               ['@' + i + '@' for i in self.in_word]

    def wordle(self):
        for i in range(6):
            p = self.make_pattern()
            print(zarf.multisearch('p' * len(p), p, ret=True))
            guess = random.choice(zarf.multisearch('p' * len(p), p))
            print(guess, end=' ')
            self.evaluate(guess)

Wordle("SHARD").wordle()

"""

pattern is .....
get: a correct i = 1
so pattern is .a...
get: s yellow i = 2
so pattern is (sa...|.a.s.|.a..s)

"""

"""
.....
BARBE BYYBG
['
"""
