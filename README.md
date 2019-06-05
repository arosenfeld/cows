# ambigtree

ambigtree is an efficient implementation of the dict, set, and trie data structures where where keys are allowed to have wildcards.  Unlike the built-in data-structures, when determining if a key `k` is present in the collection `c`, wildcards are both allowed in both `k` and the keys in `c`.

It's primary use cases are:

1. Finding if a search string `s` exists in a set of strings `T` where both `s` and the elements of `T` may contain wildcard characters.

2. Aggregating (e.g. counting, generating a consensus string) unique strings from a large set of strings where every string may contain wildcards.

## Examples

### `AmbiguousSet`

Given the wildcard `*` and the strings:

```
AB*CD
A*CCD
WXYZ*
****A
```

An `AmbiguousSet` could produce the strings:

```
AB*CD
WXYZ*
```

### `AmbiguousDict`

Given the key/value pairs:

```
AB*CD   1
A*CCD   2
WXYZ*   3
****A   4
```

An `AmbiguousDict` where the reduction function adds values together could produce:

```
AB*CD   3
WXYZ*   7
```

## Complexity

ambigtree was written because there did not appear to be an efficient method of comparing one string to a set of other strings where both the search string and other strings could contain wildcards.  Most other libraries pair-wise compare the values which quickly becomes inefficient.

All ambigtree data structures are built on top of the `AmbiguousTrie` class.  Given an input list of size `n` with maximum string of length `m`, the complexity is:

| Function  | Complexity |
------------|-------------
| Insertion | O(m)       |
| Lookup    | O(nm)      |
| Iteration | O(m)      |

So, for situations where the search string length, `m`, is less than the number of strings to be searched, `n`, ambigtree should outperform the naive approach.
