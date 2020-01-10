from zipfile import ZipFile
from zarf import subdicts, diphths

for d in diphths:
    print(d)
    for word in subdicts[d]:
        with ZipFile('zip1.zip') as zf:
            try:
                zf.extractall(pwd=word.lower().encode())
                print(word)
            except RuntimeError:
                pass
            except Exception as e: # RuntimeError: # wrong password
                #print(word, e)
                pass
