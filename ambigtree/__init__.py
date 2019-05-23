class AmbiguousTrie:
    """Creates a trie which stores potentially ambiguous (i.e. wildcard)
    characters.  Inserting into the trie is essentially the same as a
    normal trie, but lookups take into account the ambiguous character both
    in the query string and strings to be matched

    For examplean AmbiguousTrie containing the strings ATCG, ANTT, and ANCG
    when queried with ``get_matches('NTCG')`` will return ATCG and ANCG.

    key: The character representing the trie node.
    value: An arbitrary Python object representing the data at the trie
            node.
    ambig_char: The character representing ambiguity.


    """
    def __init__(self, key=None, value=None, ambig_char='N'):
        self.children = {}
        self.key = key
        self.value = value
        self.ambig_char = ambig_char

    def __getitem__(self, key):
        node = self
        while True:
            if not key:
                return node
            prefix, rest = key[0], key[1:]
            node = node.children[prefix]
            key = rest

    def __setitem__(self, key, value):
        node = self
        while True:
            prefix, rest = key[0], key[1:]
            node = node.children.setdefault(
                prefix, AmbiguousTrie(prefix, ambig_char=self.ambig_char)
            )
            if not rest:
                node.value = value
                break
            key = rest

    def children_matching(self, prefix):
        """Gets all children matching the single character prefix."""
        if not (isinstance(prefix, str) and len(prefix) == 1):
            raise ValueError('Prefix must be a single character')

        if prefix == self.ambig_char:
            yield from self.children.values()
        elif prefix in self.children:
            yield self.children[prefix]
            if self.ambig_char in self.children:
                yield self.children[self.ambig_char]

    def get_matches(self, key):
        """Gets all ``values`` from trie nodes matching the input ``key``."""
        next_visit = (key, self)
        to_visit = []

        while True:
            key, node = next_visit
            prefix, rest = key[0], key[1:]
            matching_children = node.children_matching(prefix)
            if not rest:
                yield from [c.value for c in matching_children if c.value]
            else:
                to_visit.extend((rest, c) for c in matching_children)

            try:
                next_visit = to_visit.pop()
            except IndexError:
                break
