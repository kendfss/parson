from m3ta import alphabet, primes1

letters = ''.join(i for i in alphabet if i.isalpha())
primes = primes1(len(letters))
# from . import primes, letters

class Letter:
    def __init__(self,sign):
        self.id = sign
        self.signature = ''.join((sign.lower() if sign.isupper() else sign.upper(), sign.upper() if sign.isupper() else sign.lower())[::-1])
        self.transmorph = sign.lower() if sign.isupper() else sign.upper() if sign.islower() else None
        self.sequent = primes[letters.index(sign)]
        self.antecedents = {}
        self.successors = {}
        self.cohort = {
            'pred':{},
            'succ':{}
        }
        self.samples = 0
        self.cases = {'lower':0,'upper':0}
    def __repr__(self):
        return self.id
    def __str__(self):
        return self.id
    def _dumpCohort(self,iterable,att=None):
        assert att != None, f"Target attribute is undefined:\n\t\t{att=}"
        if iterable==None:
            if iterable not in self.cohort[att].keys():
                self.cohort[att][iterable] = 0
            self.cohort[att][iterable] += 1
        else:
            for i in range(len(iterable)):
                if iterable[i] not in self.cohort[att].keys():
                    self.cohort[att][iterable[i]] = 0
                self.cohort[att][iterable[i]] += 1
    def _getNeighbors(self,word):
        word = [char for char in word] if isinstance(word,str) else word
        while self.id in word:
            form = 'lower' if self.id.islower() else 'upper'
            position = word.index(self.id) if self.id in word else word.index(self.transmorph)
            pred = word[position-1] if position!=0 else None
            succ = word[position+1] if position!=len(word)-1 else None
            if pred not in self.antecedents.keys():
                self.antecedents[pred] = 0
            if succ not in self.successors.keys():
                self.successors[succ] = 0
            self.antecedents[pred] += 1
            self.successors[succ] += 1
            self.cases[form] += 1
            del word[position]
        while self.transmorph in word:
            form = 'lower' if self.transmorph.islower() in word else 'upper'
            position = word.index(self.id) if self.id in word else word.index(self.transmorph)
            pred = word[position-1] if position!=0 else None
            succ = word[position+1] if position!=len(word)-1 else None
            if pred not in self.antecedents.keys():
                self.antecedents[pred] = 0
            if succ not in self.successors.keys():
                self.successors[succ] = 0
            self.antecedents[pred] += 1
            self.successors[succ] += 1
            self.cases[form] += 1
            del word[position]

    def _getCohort(self,word):
        word = word.split() if isinstance(word,str) else word
        while self.id in word:
            position = word.index(self.id)
            pred = word[:position] if position!=0 else None
            succ = word[position+1:] if position!=len(word)-1 else None
            # print(f'{pred=}\n{succ=}')
            self._dumpCohort(pred,'pred')
            self._dumpCohort(succ,'succ')
            del word[position]
            # self.cohortSamples += 1
    def sample(self,word):
        self._getNeighbors(word)
        self._getCohort(word)
        self.samples += 1

if __name__ == '__main__':
    test = f'the quick bown fox jumps over the lazy dog'
    for char in set(i for i in test if i in letters):
        c = Letter(char)
        # print(c.forms)
        for word in test.split():
            if any(form in word for form in c.signature):
                c.sample(word)
        print(f'{c}\n{c.signature=}\n{c.antecedents=}\n{c.successors=}\n{c.samples=}\n{c.cohort=}\n')
