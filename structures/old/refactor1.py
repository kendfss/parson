from itertools import chain
from string import punctuation
import re

from m3ta import main, show, tipo, join, freq, pop, Address, defaultdict

ignorables = '-'
punctuation = join(i for i in punctuation if not i in ignorables)
_special_endings = "mars ver ther ter fer".split()

special_endings = map(re.escape, _special_endings)
special_endings = [i+"$" for i in special_endings]
special_endings = join(special_endings, '|')
special_endings = re.compile(special_endings, re.I)
_extensions = "es s ies ing er ers ly ive ish esque ed 's 've 're 'll 'm 'd , .".split()
extensions = map(re.escape, _extensions)
extensions = [i+"$" for i in extensions]
extensions = re.compile(join(extensions, '|'), re.I)

def normalize(term):
    while extensions.search(term) and not special_endings.search(term):
        term = join(extensions.split(term))
    return term.lower()

class Word:
    def __init__(self, id:str):
        self.id = normalize(id)
        self.leaders = defaultdict(int)
        self.followers = defaultdict(int)
        self.predecessors = predecessors = defaultdict(int)
        self.successors = successors = defaultdict(int)
        self.multiplicities = defaultdict(int)
        self.forms = defaultdict(int)
        self.indices = defaultdict(int)
    def __hash__(self):
        return hash(self.id)
    # def __str__(self):
        # return self.id
    def __repr__(self):
        t = tipo(self).split('.')[-1]
        return f"{t}(id={self.id}, frequency={self.frequency})"
    @property
    def frequency(self):
        return sum(self.forms.values())
    def train(self, arg, flags=re.I):
        # extensions = insigs + [*punctuation]
        variations = map(re.escape, (i for i in _extensions if not self.id.endswith(i)))
        escapees = (re.escape(self.id+i) for i in variations)
        pattern = join((f"{i}|\S+{i}|{i}\S+" for i in [*escapees, self.id]), sep='|')
        ctr = 0
        terms = arg.split()
        for i, term in enumerate(terms):
            if re.match(pattern, term, flags):
                ctr += 1
                self.indices[i] += 1
                self.forms[term] += 1
                if len(terms)-1 > i:
                    if not re.match(pattern, terms[i+1], flags):
                        self.followers[term] += 1
                    self.leaders[term] += 1
                if i > 0:
                    if not re.match(pattern, terms[i-1], flags):
                        self.leaders[term] += 1
                    self.followers[term] += 1
            if any(re.match(pattern, j, flags) for j in terms[i:]):
                self.successors[term] += 1
            if any(re.match(pattern, j, flags) for j in terms[:i]):
                self.predecessors[term] += 1
        self.multiplicities[ctr] += 1
        return self
    def __getitem__(self, other):
        if isinstance(other, str):
            string = other
        elif issubclass(type(other), Word):
            string = other.id
        keys = (self.leaders, self.followers, self.predecessors, self.successors)
        keystrs = ('leading', 'following', 'predecessing', 'successing')
        items = zip(keystrs, map(lambda x: x.get(string), keys))
        pairs = (join(pair, ': ') for pair in items)
        rack = join(pairs, ',\n   ')
        return f"{string} wrt {self.id}\n" + "{  " + rack + "}"

def pattern(term):
    variations = map(re.escape, (i for i in _extensions if not term.endswith(i)))
    escapees = (re.escape(term+i) for i in variations)
    pattern = join((f"{i}|\S+{i}|{i}\S+" for i in [*escapees, term]), sep='|')
    return pattern

def uniqueTerms(statement, shortest=2):
    terms = set(statement.split())
    matchers = {term: re.compile(pattern(term)) for term in terms}# if len(term)>shortest}
    matches = {term: [t for t in terms if matchers[term].match(t)] for term in terms}
    otherChain = lambda term: chain.from_iterable(matches[t] for t in terms if t!=term)
    otherTerms = lambda term: [t for t in terms if not t==term]
    opred = lambda term: sum(1 for i in terms if any(term in i for i in otherTerms(term)))
    pred = lambda x: not (len(matches[x])==1 and freq(x, otherChain(x))>0)
    # return [*filter(pred, terms)]
    
    """
    while there are terms longer than anything they match, remove terms
    """
    return [*filter(pred, terms)]
    # minima = {term for term in terms if term==min(matches[term],key=len)}
    # minima = {min((t for t in matches),key=len) for matches in matches.values()}
    # nets =
    # return minima

def notpunctuated(term, tf=False, ignorables='-'):
    puncs = join(map(re.escape, (i for i in punctuation if not i in ignorables)),'|')
    result = [*re.finditer(puncs, term)]
    return not bool(result) if tf else result



class Bank(dict):
    pass

if eval(main):
    test = "that motherfucking motherfuck motherfucker fuck's a cunt never fucking learn that's why i twat all the fucking sodbollocking fuck nuts, fuck"
    # test = "The quick brown fox jumps over the lazy dog"
    # bank = Bank((word, Word(word)) for word in set(test.split()))
    print(test.split())
    print(uniqueTerms(test))
    # z = notpunctuated('nuts,')
    term = "nut's,"
    # term = "sodbollocking"
    z = normalize(term)
    # z = normalize("nuts,")
    # z = normalize()
    print(z)
    print(set(map(normalize, test.split())))
    for term in set(filter(normalize, test.split())):
        n = Word(term)
        n.train(test)
        print(n)
        # print(n['cheese'])
    # print(Word('fuck').train(test))
    # print(Word('fuck').train(test).forms)