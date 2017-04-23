#---imports
import re
import string
import types

import itertools as it
import collections

#---initializations
diphths = sorted([["".join(i) for i in it.permutations(list(string.ascii_uppercase), 2)] + [j*2 for j in string.ascii_uppercase]][0])
subdicts = {diphth: set(open("resources/" + diphth + ".txt").read().split()) for diphth in diphths}

#---pretty printer
try:
    import tabulate as tb
    installation = 1
    def pprint(u, rack):
        used = sorted(u, key=lambda word:-len(word))
        used = [list(blankPrint(word, rack)) for word in used]
        for i in range(len(used)):
            used[i].insert(0, i+1)
        df = tb.tabulate(used, headers=['', 'Front', 'Words', 'Back'], tablefmt="fancy_grid")
        #print(df)
        return df
except ImportError:
    print("No tabulate installation found; trying pandas")
    try:
        import pandas as pd
        installation = 0
        def pprint(u, rack):
            def _create(f=[], w=[], b=[]):
                return pd.DataFrame(collections.OrderedDict((('Front', f), ('Words', w), ('Back' , b))))
            df = _create().append(_create(*[[i[j] for i in [blankPrint(word, rack) for word in u]] for j in range(3)]).iloc[(lambda series:[series.index(i) for i in sorted(series,key={j:i for i, j in enumerate(sorted(u, key=lambda word:-len(word)))}.get)])(u)], ignore_index=True)
            df.index += 1
            df = df.to_string()
            #print(df)
            return df
    except ImportError:
        print("No pandas installation found")
        raise SystemExit
#------------
#---functions
#------------
#---word generators
def getWords(length='any', max_length=15):
    for d in diphths:
        yield from getSomeWords(d, length, max_length)

def getSomeWords(d, length='any', max_length=15):
    return filter(lambda word: (length == 'any' or (len(word) == length and max_length == 15)) and len(word) <= max_length, subdicts[d])

def getWords_2(r, length='any', max_length=15):
    for d in diphths:
        yield from getSomeWords_2(d, r, length, max_length)

def confirm(seq, n):
    return len(list(filter(bool, seq))) >= n
#sum(1 for i in seq if bool(i)) >= n
#return sum(1 for i in seq if bool(seq)) >= n
#)(confirm((i in r for i in word), len(r)-r.count('.')*2-1)) or len(word)<4))
#(all(i in r for i in word) or ('.' in r  and any(i in r for i in word)))

#confirm((i in r for i in word), min(len(word), len(r)) - r.count('.')
def getSomeWords_2(d, r, length='any', max_length=15):
    return filter(lambda word: (length == 'any' or (len(word) == length and max_length == 15)) and len(word) <= max_length and confirm((i in r for i in word), min(len(word), len(r)) - r.count('.')), subdicts[d])

def hooks(word, side):
    hooks = []
    for letter in string.ascii_uppercase:
        for word2 in getSomeWords([word[:2], letter+word[0]][side == 'f'], len(word)+1):
            if [word + letter, letter + word][side == 'f'] == word2:
                yield letter
					
#---blank logic
def flatten(nested, basetype=types.GeneratorType):
    if isinstance(nested, basetype):
        for sublist in nested:
            yield from flatten(sublist)
    else:
        yield nested

def blanks(word):
    if '.' not in word:
        yield word
    else:
        for (index, letter) in enumerate(word):
            if letter == '.':
                for letter2 in string.ascii_uppercase:
                    yield blanks(word[:index] + letter2 + word[index+1:])
					
def blankPrint(word, rack):
    text = ''
    cases = {letter: True for letter in rack}
    ncases = {letter: True for letter in word}
    for letter in word:
        if word.count(letter) > rack.count(letter):
            if cases.get(letter):
                text += letter.upper()
                cases[letter] = False
            elif ncases.get(letter) and letter not in cases.keys():
                text += letter.lower()
            else:
                text += letter.lower()
                cases[letter] = False
        else:
            text += letter.upper()
            cases[letter] = False

    return ''.join(hooks(word.upper(), 'f')), text, ''.join(hooks(word.upper(), 'b'))

#---logic
def search(mode, rack, textFunc=getWords, ret=None):
    def _create(f=[], w=[], b=[]):
        return pd.DataFrame(collections.OrderedDict((('Front', f), ('Words', w), ('Back' , b))))
    #df = _create()
    used = []
    def _add(word):
        used.append(word.upper())      
    
    if mode == 'p':
        rack = rack.replace('\\V', '[aeiou]').replace('@', '.*').replace('\\C', '[bcdfghjklmnpqrstvwxyz]').upper()
        for word in textFunc():
            if re.match(rack, word):
                _add(word)
    elif mode == 'a':
        for word in getWords_2(rack, length=len(rack)):
            for blankWord in flatten(blanks(rack)):
                if word not in used and sorted(word) == sorted(blankWord):
                    _add(word)
    else:
        for word in getWords_2(rack, max_length=len(rack)):
            for blankWord in flatten(blanks(rack)):
                if word not in used and all(word.count(letter) <= blankWord.count(letter) for letter in word):
                    _add(word)
    df = pprint(used, rack)
    if ret is not None:
        return df
    
    return used

def multisearch(modes, racks, textFunc=getWords, ret=None):
    for mode, rack in zip(modes, racks):
        _last = search(mode, rack, textFunc)
        textFunc = lambda: _last
    return pprint(textFunc(), racks[-1])

def checkInput(func):
    def wrap(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except AssertionError:
                print('invalid input')
            except Exception as e:
                raise e
    return wrap
	
#---interface								
def _submain(textFunc):
    mode = getMode()
    rack = input('Enter rack: ').upper()
    last = search(mode, rack, textFunc)
    return last
			
@checkInput
def getMode():
    mode = input('Pattern, Anagram, Build? (p|a|b|quit(q)) ').lower()
    assert mode in ['p', 'a', 'b', 'q']
    if mode == 'q':
        raise SystemExit
    return mode
	
@checkInput
def getNextSearch():
    cont = input('Search using this sublist? (y|n) ')
    assert cont in ['y', 'n']
    return cont

def main():
    textFunc = getWords
    while True:
        last = _submain(textFunc)
        if getNextSearch() == 'y':
            textFunc = lambda length = 'any', max_length=15: last
        else:
            break

if __name__ == "__main__":
    main()
