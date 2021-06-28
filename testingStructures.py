"""
TODO
    Plural Recognition
    Morphological Root/extension handling (going of go)
    Combing for expansions (eg - 'monotonous' of 'mono')
    Case handling for letters (eg A and a should have the same object)
    Frequency for upper/lower cased letters
        Decide how/where to update this and how to kee
            create an additional method which handles all samples and updates accordingly
            the sum for this attribute will be the sample count
"""
from structures import Letter, Word
# import structures
from m3ta import alphabet,primes1,freq

letters = ''.join(i for i in alphabet if i.isalpha())

primes = primes1(len(letters))





if __name__ == '__main__':
    test = f'the quick bown fox jumps over the lazy dog'
    # for word in set(test[:].split()):
        # w = Word(word)
        # w.sample(test)
        # print(f'{w}\n{w.antecedents=}\n{w.successors=}\n{w.samples=}\n{w.cohort=}\n')
        # print()
    for char in set(i for i in test if i in letters):
        c = Letter(char)
        for word in test.split():
            c.sample(word)
        # c.sample(word)
        print(f'{c}\n{c.antecedents=}\n{c.successors=}\n{c.samples=}\n{c.cohort=}\n')
