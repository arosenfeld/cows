from .dictionary import Dict


class Set:
    """Creates a set-like object which checks for ambiguous inclusion.

    This class provides a basic implementation of the ``set``, a group of
    distinct (unique) values.  Uniqueness is checked based on ambiguous strings
    so ``ABC*`` and ``*BCD`` would be considered equivalent.


    Args:
        iterable (iterable): An optional set of elements with which to populate
        the set.
        **kwargs: Passed to underlying Trie

    Example:
        .. code-block:: python

            import basco

            s = basco.Set()
            s.add('ABCD')
            s.add('*EFG')
            s.add('T')
            s.add('ABC*')  # Matches ABCD, so not added
            s.add('HEF*')  # Matches *EFG, so not added

            print(s)

        Produces:

        .. code-block:: none

            basco.Set(['*EFG', 'ABCD', 'T'])


    """
    def __init__(self, iterable=None, **kwargs):
        self.dict = Dict(**kwargs)
        if iterable:
            for element in iterable:
                self.dict[element] = True

    def add(self, element):
        """Adds an element to the set.

        Args:
            element (str): The element to add.

        """
        self.dict[element] = True

    def __iter__(self):
        """Yields the elements in the set"""
        yield from self.dict.keys()

    def __len__(self):
        """Returns the number of elements in the set"""
        return len(self.dict)

    def __repr__(self):
        """Returns the representation of the set"""
        return f'basco.Set({sorted(list(self.dict.keys()))})'
