"""
Extract words from the txt files in a wordbank to a grouping of choice
"""

import os
from m3ta import alphabet, emptyString, show

wordbank = r'E:\Projects\Monties\2019\resources\words'
postParsum = os.path.join(r'E:\Resources\dataSets\Language\PARSON project','parsed')
os.makedirs(postParsum,exist_ok=True)

letters = ''.join(i for i in alphabet if i.isalpha())
punctors = ''.join(i for i in alphabet if not i.isalnum())
digits = ''.join(i for i in alphabet if i.isdigit())
groupnames = [
    'capped',
    'spaced',
    'numeric',
    'punctuated',
    'multi',
    'weird',
    'hyphenated',
    'dotted',
    'apostrophal',
    'negative',
    'pluralesque',
    'verbal',
    'apostromulti',
]

destinations = {name:os.path.join(postParsum,f'{name}.txt') for name in groupnames}
def makefiles(dictionary):
    for val in dictionary.values():
        if not os.path.exists(val):
            f = open(val,'x')
            f.close()
# makefiles(destinations)

capped = lambda x: all(i.isupper() for i in x)
spaced = lambda x: ' ' in x
numeric = lambda x: any(i.isnumeric() for i in x)
punctuated = lambda x: not (all(i.isalpha() for i in x if not i.isalnum()))

_booly = lambda x: (punctuated(x),numeric(x),capped(x),spaced(x))
multi = lambda x: len(tuple(i==True for i in _booly(x)))>1
weird = lambda x: all(_booly)

hyphenated = lambda x: '-' in x
dotted = lambda x: '.' in x

apostrophal = lambda x: "'" in x
negative = lambda x: x.endswith("'t")
pluralesque = lambda x: x.endswith("'s")
verbal = lambda x: any(x.endswith(j) for j in "'ve*'re*'d*'ll".split('*'))
_apostrobooly = lambda x: (negative(x),pluralesque(x),verbal(x))
apostromulti = lambda x: len(tuple(i==True for i in _apostrobooly(x)))>1


def gather(source):
    for root, folders, files in os.walk(source):
        for file in files:
            if os.path.exists((f := os.path.join(root,file))) and os.path.isfile(f):
                yield f

def deliverSingularWords(source):
    # for file in os.listdir(source):
    for file in gather(source):
        # print(file)
        path = os.path.join(source,file)
        # name =
        if os.path.isfile(path):
            name = os.path.split(file)[1]
            with open(path,'r',encoding='utf-8') as bank:
                lines = set(line.replace('\n','').replace("'s",'') for line in bank.readlines() if not emptyString(line))
                print(name)
                for word in lines:
                    print('\t\t',word) if any(char not in letters for char in word) or capped(word) else None
                    yield word if any(char not in letters for char in word) or capped(word) else None
                print()

def scrape(source):
    for file in gather(source):
        path = os.path.join(source,file)
        if os.path.isfile(path):
            name = os.path.split(file)[1]
            with open(path,'r',encoding='utf-8') as bank:
                lines = set(line.replace('\n','') for line in bank.readlines() if not emptyString(line))
                # print(name)
                for word in lines:
                    # print('\t\t',word) if any(char not in letters for char in word) or capped(word) else None
                    yield word #if any(char not in letters for char in word) or capped(word) else None
                # print()

def sorter(word):
    if weird(word):
        with open(destinations['weird'],'a') as dest:
            dest.write(f'{word}\n')
    elif multi(word):
        with open(destinations['multi'],'a') as dest:
            dest.write(f'{word}\n')
    elif capped(word):
        with open(destinations['capped'],'a') as dest:
            dest.write(f'{word}\n')
    elif spaced(word):
        with open(destinations['spaced'],'a') as dest:
            dest.write(f'{word}\n')
    elif numeric(word):
        with open(destinations['numeric'],'a') as dest:
            dest.write(f'{word}\n')
    elif punctuated(word):
        if apostrophal(word):
            if negative(word):
                with open(destinations['weird'],'a') as dest:
                    dest.write(f'{word}\n')
            elif pluralesque(word):
                with open(destinations['weird'],'a') as dest:
                    dest.write(f'{word}\n')
            elif verbal(word):
                with open(destinations['weird'],'a') as dest:
                    dest.write(f'{word}\n')
            elif apostromulti(word):
                with open(destinations['apostromulti'],'a') as dest:
                    dest.write(f'{word}\n')
            else:
                with open(destinations['apostrophal'],'a') as dest:
                    dest.write(f'{word}\n')
        elif dotted(word):
            with open(destinations['dotted'],'a') as dest:
                dest.write(f'{word}\n')
        elif hyphenated(word):
            with open(destinations['hyphenated'],'a') as dest:
                dest.write(f'{word}\n')
        else:
            with open(destinations['punctuated'],'a') as dest:
                dest.write(f'{word}\n')

if __name__ == '__main__':
    # deliverSingularWords(wordbank)
    # for file in gather(wordbank):
        # print(file)
    # show(gather(wordbank),enum=True)
    
    #     with open(file,'r') as f:
    #         for line in f.readlines():
    #             for word in line.split():
    #                 sorter(word)
    #     os.remove(file)
    # for word in scrape(wordbank):
        # print(word)
    show(scrape(wordbank),enum=True)