from m3ta import alphabet, primes1
from .words import Word
from .letters import Letter
from ._con import _Con


test = f'the quick bown fox jumps over the lazy dog'
letters = ''.join(i for i in alphabet if i.isalpha())
digits = ''.join(i for i in alphabet if i.isnumeric())
punctors = ''.join(i for i in alphabet if i not in digits and i not in letters)
primes = primes1(len(letters))


def extract(text,mode='letters'):
    if mode=='letters':
        return set(char for char in word if char in letters)
    elif mode=='digits':
        return set(char for char in word if char in digits)
    elif mode=='punctors':
        return set(char for char in word if char in punctors)
    elif mode=='words':
        return set(word for word in text.split())
    elif mode=='all':
        return set(text)
    else:
        raise ValueError(f'"{mode}" is not valid. Please choose "letters", "digits", "punctors" (for punctuation), or "all"')

if __name__ == '__main__':
    print(extract(test))
