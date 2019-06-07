from .trie import Trie


class List:
    def __init__(self, iterable=None):
        self.list = list(iterable) if iterable else []
        self.trie = Trie(initialize=[
            (element, True) for element in self.list
        ] if iterable else None)

    def __contains__(self, key):
        return key in (m[0] for m in self.trie.get_matches(key))

    def __iter__(self):
        yield from self.list

    def __repr__(self):
        """Returns the representation of the list"""
        return f'basco.List({[e for e in self]})'

    def __len__(self):
        return len(self.list)

    def append(self, value):
        self.insert(len(self), value)

    def extend(self, iterable):
        for element in iterable:
            self.append(element)

    def insert(self, i, value):
        self.list.insert(i, value)
        self.trie[value] = True

    def index(self, value, start=None, end=None):
        try:
            first_match = next(self.trie.get_matches(value))[0]
        except StopIteration:
            raise ValueError(f'No matches for {value} found')
        return self.list[start:end].index(first_match)

    def count(self, value):
        matches = [m[0] for m in self.trie.get_matches(value)]
        return sum([self.list.count(match) for match in matches])

    def reverse(self):
        self.list.reverse()
