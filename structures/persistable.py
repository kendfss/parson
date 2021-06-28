from itertools import chain
from collections import defaultdict, Counter

from nltk import FreqDist, ConditionalFreqDist
import pyperclip as pc

from m3ta import pop, getsource, show, main, freq, tight, tipo

class table:
    def __init__(self, *args, **kwargs):
        self.cache = dict(*args, **kwargs)
    def __repr__(self):
        return f'{tipo(self)}({self.cache})'
    def __setitem__(self, key, value):
        self.cache[key] = value
        return
    def __getitem__(self, key):
        return self.cache[key]
    def __len__(self):
        return len(self.cache)
    def __getattr__(self, attr):
        return eval(f"self.cache.{attr}")
    def __lt__(self, other):
        return self <= other and not self == other
    def __gt__(self, other):
        return self >= other and not self == other
    def tabulate(self, *args, **kwargs):
        """
        Tabulate the given samples from the frequency distribution (cumulative),
        displaying the most frequent sample first.  If an integer
        parameter is supplied, stop after this many samples have been
        plotted.

        :param samples: The samples to plot (default is all samples)
        :type samples: list
        :param cumulative: A flag to specify whether the freqs are cumulative (default = False)
        :type title: bool
        """
        if len(args) == 0:
            args = [len(self)]
        samples = [item for item, _ in self.most_common(*args)]

        cumulative = _get_kwarg(kwargs, "cumulative", False)
        if cumulative:
            freqs = list(self._cumulative_frequencies(samples))
        else:
            freqs = [self[sample] for sample in samples]
        # percents = [f * 100 for f in freqs]  only in ProbDist?

        width = max(len("{}".format(s)) for s in samples)
        width = max(width, max(len("%d" % f) for f in freqs))

        for i in range(len(samples)):
            print("%*s" % (width, samples[i]), end=" ")
        print()
        for i in range(len(samples)):
            print("%*d" % (width, freqs[i]), end=" ")
        print()

    def copy(self):
        """
        Create a copy of this frequency distribution.

        :rtype: FreqDist
        """
        return self.__class__(self)

    # Mathematical operatiors

    def __add__(self, other):
        """
        Add counts from two counters.

        >>> FreqDist('abbb') + FreqDist('bcc')
        FreqDist({'b': 4, 'c': 2, 'a': 1})

        """
        return self.__class__(super(FreqDist, self).__add__(other))

    def __sub__(self, other):
        """
        Subtract count, but keep only results with positive counts.

        >>> FreqDist('abbbc') - FreqDist('bccd')
        FreqDist({'b': 2, 'a': 1})

        """
        return self.__class__(super(FreqDist, self).__sub__(other))

    def __or__(self, other):
        """
        Union is the maximum of value in either of the input counters.

        >>> FreqDist('abbb') | FreqDist('bcc')
        FreqDist({'b': 3, 'c': 2, 'a': 1})

        """
        return self.__class__(super(FreqDist, self).__or__(other))

    def __and__(self, other):
        """
        Intersection is the minimum of corresponding counts.

        >>> FreqDist('abbb') & FreqDist('bcc')
        FreqDist({'b': 1})

        """
        return self.__class__(super(FreqDist, self).__and__(other))

    def __le__(self, other):
        """
        Returns True if this frequency distribution is a subset of the other
        and for no key the value exceeds the value of the same key from
        the other frequency distribution.

        The <= operator forms partial order and satisfying the axioms
        reflexivity, antisymmetry and transitivity.

        >>> FreqDist('a') <= FreqDist('a')
        True
        >>> a = FreqDist('abc')
        >>> b = FreqDist('aabc')
        >>> (a <= b, b <= a)
        (True, False)
        >>> FreqDist('a') <= FreqDist('abcd')
        True
        >>> FreqDist('abc') <= FreqDist('xyz')
        False
        >>> FreqDist('xyz') <= FreqDist('abc')
        False
        >>> c = FreqDist('a')
        >>> d = FreqDist('aa')
        >>> e = FreqDist('aaa')
        >>> c <= d and d <= e and c <= e
        True
        """
        if not isinstance(other, type(self)):
            raise TypeError(f'Other must be "{type(self)}')
        return set(self).issubset(other) and all(
            self[key] <= other[key] for key in self
        )

    def __ge__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f'Other must be "{type(self)}')
        return set(self).issuperset(other) and all(
            self[key] >= other[key] for key in other
        )
    # def __iter__(self):
        # self.cache.__iter__()
    # @property
    # def keys(self):
        # return self.cache.keys()
    # @property
    # def values(self):
        # return self.cache.values()
    # @property
    # def items(self):
        # return self.cache.items()

class glossary(table):
    def __init__(self, kind, *args, **kwargs):
        if not hasattr(kind, '__call__'):
            raise AttributeError(f'"{kind}" does not have a "__call__" method')
        table.__init__(self, *args, **kwargs)
        self.kind = kind
    def __setitem__(self, key, value):
        if isinstance(value, self.kind):
            self.cache[key] = value
            return
        raise TypeError(f'"{value}" is not "{self.kind}"')
    def __getitem__(self, key):
        if not key in self.cache.keys():
            self.cache[key] = self.kind()
        return self.cache[key]
    


class freqDist(table):
    def __init__(self, samples=None, **kwargs):
        self.cache = glossary(int, **kwargs)
        if samples:
            for sample in samples:
                self.cache[sample] += 1
    def __repr__(self):
        """
        Return a string representation of this FreqDist.

        :rtype: string
        """
        return "<freqDist with %d samples and %d outcomes>" % (len(self), self.mass)
    # def __getitem__(self, key):
        # return self.cache[key]
    # @property
    # def keys(self):
        # return self.cache.keys
    # @property
    # def values(self):
        # return self.cache.values
    # @property
    # def items(self):
        # return self.cache.items
    # @property
    # def mass(self):
        # return sum(self.values)
    # def __len__(self):
        # return sum(1 for i in self.keys)
    
class node:
    def __init__(self, term):
        self.id = term
        self.cohort = freqDist()
        


class edge:
    pass
    



if eval(main):
    getsource(FreqDist)
    sent = 'to be or not to be'.split()
    t = table()
    g = glossary(int)
    fd = freqDist(sent)