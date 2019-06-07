.. _implementation:

Implementation Details
======================
This page details how the :class:`cows.trie` data structure is implemented.
This is the most important class in cows since all other data structures are
built on top of it.

Overview
--------
A :class:`cows.trie` is non-recursive implementation of a `trie
<https://en.wikipedia.org/wiki/Trie>`_ with an additional accessor operation,
:meth:`cows.trie.Trie.get_matches` which accepts a pattern to match.

When a key/value pair is inserted into the trie via
:meth:`cows.trie.Trie.__setitem__`, it is inserted as in a traditional trie:
wildcard characters are not treated specially and the value associated with the
key is stored at a leaf node.

The novelty of :class:`cows.trie` is primarily in the
:meth:`cows.trie.Trie.get_matches` method which finds all values in the trie
that match the query string.
