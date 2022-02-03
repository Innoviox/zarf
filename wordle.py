import zarf
import string
import random

word = "SHARD"

pattern = [list(".....")]

def evaluate(guess):
    for i, (a, b) in enumerate(zip(guess, word)):
        if a == b:
            print('G', end='')
            # pattern[i + 1] = a
            for p in pattern:
                p[i] = a
        elif a in (word[:i] + word[i + 1:]):
            print('Y', end='')
            for j in range(len(pattern)):
                for j in range(len(word)):
                    if j != i:
                        
        else:
            print('B', end='')
            
    print()

def make_pattern():
    return '^(' + '|'.join(pattern) + ')$'

for i in range(6):
    # guess = random.choice(zarf.search('p', ''.join(pattern)))
    ...

"""

pattern is .....
get: a correct i = 1
so pattern is .a...
get: s yellow i = 2
so pattern is 

"""
