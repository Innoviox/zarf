from string import ascii_uppercase
import tqdm

options = [i.upper() for i in open("sedecordle_acceptable").read().split()]
fives = [i.upper() for i in open("sedecordle_wordlist").read().split()]
# options.extend(fives)

locations = {l: [0 for _ in range(5)] for l in ascii_uppercase}
freqs = {l: 0 for l in ascii_uppercase}

for word in tqdm.tqdm(fives):
    for i, letter in enumerate(word):
        locations[letter][i] += 1
        freqs[letter] += 1 # yeah i could sum it but this is easy

    if all(i not in word for i in 'AEIOYCRWTH') and len(set(word)) == 5:
        print(word)

input("finished")

for i in locations:
    locations[i] = [v / sum(locations[i]) for v in locations[i]]

for k, v in sorted(locations.items(), key=lambda a: -freqs[a[0]]):
   print(k, v)# v.index(max(v)), freqs[k])

def score(words):
    return sum(sum(locations[j][i] for i, j in enumerate(w)) for w in words)

print(score(["SHARE", "CLUNY", "POINT"]))
print(score(["GROUT", "CHAIN", "MELDS"]))
print(score(["GHAST", "BLINK", "CRUMP"]))
    
"""
RTLSNCYDHPMGBFKWVZXQJ
EAOIU


NCUYD
HPMGB
FKWVE
"""

"""
TLISN
CUYDH

SLIMY
CHUTE

ILTND
UMPYC

DUMPY
CLINT
"""
