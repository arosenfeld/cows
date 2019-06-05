from .trie import AmbiguousTrie


class ReducedDict:
    """Creates a dict-like object which checks that no matching key exists
    before setting a value.  If one or more ambiguous matches do exist,
    optionally update one.

    selector: Called when __setitem__ is called with `key` and `value` and
        an ambiguous match to `key` exists.  Must accept one argument, an
        iterable of matches, and return a single element from the iterator that
        will be updated with `updater`.
    updater: Called when __setitem__ is called with `key` and `value` and an
        ambiguous match to `key` already exists.  Takes a single argument of
        the value assocated with the ambiguous match which it can then mutate
        (e.g. increment a counter).  Return value is ignored.
    **kwargs: Passed to underlying AmbiguousTrie


    """
    def __init__(self, selector=None, updater=None, **kwargs):
        initialize = kwargs.pop('initialize')

        self.selector = selector or (lambda l: sorted(l)[0])
        self.updater = updater
        self.trie = AmbiguousTrie(**kwargs)

        # This needs to override the same loop in AmbiguousTrie because
        # __setitem__ processes calls before calling the same method in
        # AmbiguousTrie
        if initialize:
            for init_key, init_val in initialize:
                self[init_key] = init_val

    def __setitem__(self, key, value):
        """Sets an `key` to `value` if no match for `key` already exists.  If a
        match does exist, select it with `self.selector` and optionally update
        it with `self.updater`"""
        matches = [m for m in self.trie.get_matches(key)]
        if matches:
            if matches and self.updater:
                self.updater(self.selector(matches))
        else:
            self.trie[key] = value

    def __getitem__(self, key):
        return self.trie.get_matches(key)

    def __len__(self):
        return len([l for l in self.values()])

    def values(self):
        """Gets all values inserted into the ReducedDict"""
        return self.trie.values()
