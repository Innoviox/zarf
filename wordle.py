import zarf
import string
import random

class Wordle():
    def __init__(self, word):
        self.word = word

        self.pattern = [list(".....")]

        self.out = ' '

    def evaluate(self, guess):
        for i, (a, b) in enumerate(zip(guess, self.word)):
            if a == b:
                print('G', end='')
                # pattern[i + 1] = a
                for p in self.pattern:
                    p[i] = a
            elif a in (self.word[:i] + self.word[i + 1:]):
                print('Y', end='')
                new_patterns = []
                for p in self.pattern:
                    for j in range(len(guess)):
                        if j != i:
                            new_patterns.append(p[:j] + [a] + p[j + 1:])
                            # print(new_patterns)
                self.pattern = new_patterns[:]
            else:
                print('B', end='')
                self.out += a
                
        print()

    def make_pattern(self):
        # .replace('.', f'[^{self.out}]')
        return '^(' + '|'.join(''.join(i).replace('.', f'[^{self.out}]') for i in self.pattern) + ')$'

    def wordle(self):
        for i in range(6):
            print(self.make_pattern())
            guess = random.choice(zarf.search('p', self.make_pattern()))
            print(guess, end=' ')
            self.evaluate(guess)

Wordle("IRATE").wordle()

"""

pattern is .....
get: a correct i = 1
so pattern is .a...
get: s yellow i = 2
so pattern is (sa...|.a.s.|.a..s)

"""
