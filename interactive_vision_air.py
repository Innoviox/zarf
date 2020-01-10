# ben oliver 11.01.2013
# a (functional) python 3.x vigenere encoder / decoder.
# encode and decode functions are mathematical, no dictionary lookups.

from itertools import cycle
from functools import partial
import itertools as it
from string import ascii_uppercase
from zarf import subdicts
import random

def transform(crypt_function,k,s):
    """ (Int -> Int -> Int) -> Char -> Char -> Char """
    return chr(crypt_function(ord(k), ord(s)))

def encode26(a,b):
    """ Int -> Int -> Int """
    return (((a + b) - 130) % 26) + 65
 
def decode26(a,b):
    """ Int -> Int -> Int """
    return (((b - a) - 130) % 26) + 65

def cipher(crypt_function,key,string):
    """ (Int -> Int -> Int) -> String -> String -> String """
    transform_function = partial(transform, crypt_function)
    mapped_transform = map(transform_function, cycle(key), string)
    return ''.join(mapped_transform)

def safe_cipher(crypt_function,key,string):
    """ (Int -> Int -> Int) -> String -> String -> (String,String) 
    converts lowercase to uppercase , removing digits, whitespace & punctuation"""
    k = ''.join(filter(lambda k: k in ascii_uppercase, key.upper()))
    s = ''.join(filter(lambda s: s in ascii_uppercase, string.upper()))
    return (k, cipher(crypt_function,k,s))

def chown(word, a="efghijklmnopqr"):
    q = []
    for i in range(0, len(a)):
        for j in range(2, len(a)+1):
            key = a[i:j]
            if len(key) == len(word):
                print(key, cipher(decode26, key, word))
                q.append(cipher(decode26, key, word))
    
    print()
    print(word)
    used = []
    qef = []
    for i in it.permutations(a, len(word)):
        key = ''.join(i)
        if key == ''.join(sorted(key)):
            dc = cipher(decode26, key, word)
            if dc in subdicts[dc[:2]] and key not in used:
                used.append(key)
                qef.append(dc)
                print(key, dc)

    print()
    for i in range(0, len(a)):
        for j in range(2, len(a)+1):
            key = a[i:j]
            dc = cipher(decode26, key, word)
            if len(dc) >= 2 and dc in subdicts[dc[:2]]:
                print(key, dc)
    return qef
crypt = "fmcj_aj_rzxn_mpxc_knwxabb"

key = "stuvwxyzefabcd"

a1, a2, b1, b2, c = "abcdefg", "ef", "ghij", "klmn", "stuvwxyz"

c11, c12, c2, c3, c4 = crypt.split("_")
'''
print(cipher(decode26, a1, c11))
print(cipher(decode26, a1, c12))
print(cipher(decode26, b1, c2))
print(cipher(decode26, b2, c3))
# print(cipher(decode26, c, c4))

for i in [c11, c12, c2, c3, c4]:
    print(i)
    # chown(i)
    print()
    '''
chown(c4)
mid1, mid2 = chown(c2), chown(c3)

for w1 in mid1:
    for w2 in mid2:
        print(f"flag{{we_{w1}_{w2}_succeed}}".lower())
'''
for l in range(1, len(key) + 1):
        for j in range(1, 5):
            a = [crypt[i:i+l] for i in range(0, len(crypt), l)]
            b = [key[i:i+l] for i in range(0, len(key), l)]
            for plain, subk in zip(a, b):
                    print(l, plain, subk)
'''
# chown(c3)
