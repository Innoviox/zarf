import vigenerecipher as vc
from itertools import repeat
key = "abcdefghijklmnopqrstuvwxyz"
vc.decode("hi", "bye")

crypt = "fmcj{aj_rzxn_mpxc_knwxabb}"

def r(c, j):
    for i in c:
        for k in range(j):
            yield i

def inter_decode(code, l):
    for j in range(1, 5):
        a = [''.join(r(code, j))[i:i+l:j] for i in range(0, len(code), l)]
        b = [''.join(r(code, j))[i:i+l:j] for i in range(0, len(key), l)]
        s = ''
        for plain, subk in zip(a, b):
            s += vc.decode(plain, subk)
        yield j, s


print(list(inter_decode(crypt, 5)))


def inter_encode(plain, l):
    for j in range(1, 5):
        a = [plain[i:i+l:j] for i in range(0, len(plain), l)]
        b = [key[i:i+l:j] for i in range(0, len(key), l)]
        s = ''
        for t, subk in zip(a, b):
            s += vc.encode(t, subk)
        yield j, s



'''
plain = "flag{vd_jqnc_zbim_succeed}"
code = inter_encode(plain, 4)
new = inter_decode(code, 4)
print(plain, code, new)
'''
