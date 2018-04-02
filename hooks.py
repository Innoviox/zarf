import string, random
import itertools as it

diphths = sorted([["".join(i) for i in it.permutations(list(string.ascii_uppercase), 2)] + [j*2 for j in string.ascii_uppercase]][0])
subdicts = {diphth: set(open("resources/" + diphth + ".txt").read().split()) for diphth in diphths}

def get_length(l):
    for s in subdicts.values():
        yield from filter(lambda w: len(w) == l, s)

def extract_hooks(words):
    bases = {}  # word : [front, back]
    for w in words:
        fstem, bstem = w[1:], w[:-1]
        if fstem in bases:
            bases[fstem][0].append(w[0])
        else:
            bases[fstem] = [[w[0]], []]

        if bstem in bases:
            bases[bstem][1].append(w[-1])
        else:
            bases[bstem] = [[], [w[-1]]]
    return bases

twos, threes, fours, fives = lists = [extract_hooks(get_length(l)) for l in [2, 3, 4, 5]]

def quiz(words, side):
    stem = random.choice(list(words.keys()))
    hooks = words[stem][side]
    alphabet = string.ascii_uppercase + "?!*"
    correct = []
    incorr = []
    print(stem, "has", "?", ["front", "back"][side], "hooks.")  # len(hooks), 
    # if len(hooks) != 0:
    while True:  # sorted(correct) != sorted(hooks):
        letter = input("Enter the letter: ").upper()
        while letter not in alphabet:
            print("Invalid input.")
            letter = input("Enter the letter: ").upper()
        if letter == "?" or letter == "!":
            break
        elif letter == "*":
            print("There are ", len(hooks), end='.')
        elif letter in incorr or letter in correct:
            print("Already tried.")
        elif letter in hooks:
            correct.append(letter)
            print("Correct.")  # , len(hooks) - len(correct), "to go.")
        else:
            incorr.append(letter)
            print("Incorrect.")
    print("The answers were:", ', '.join(hooks))
    if incorr:
        print("Incorrect guesses:", ', '.join(incorr))
    if sorted(correct) != sorted(hooks):
        print("You missed", ', '.join(i for i in hooks if i not in correct))
    elif letter == "!":
        print("You got them all correct! Good job!")
    print()

while 1:
    quiz(random.choice(lists), random.choice([0, 1]))
        
