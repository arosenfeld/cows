from .dictionary import Dict


class Set:
    def __init__(self, iterable=None):
        self.dict = Dict()
        if iterable:
            for element in iterable:
                self.dict[element] = True

    def add(self, value):
        self.dict[value] = True

    def __iter__(self):
        yield from self.dict.keys()

    def __len__(self):
        return len(self.dict)

    def __repr__(self):
        return f'basco.Set({sorted(list(self.dict.keys()))})'
