# cows

_cows_ (Bidirectional Ambiguous String COllections) is an efficient
implementation of the dict, set, and trie data structures where where keys are
allowed to have ambiguous characters (wildcards).  Unlike the built-in
data-structures, when determining if a key `k` is present in the collection
`c`, wildcards are both allowed in both `k` and the keys in `c`.

It's primary use cases are:

1. Finding if a search string `s` exists in a set of strings `T` where both `s`
   and the elements of `T` may contain wildcard characters.

2. Aggregating (e.g. counting, generating a consensus string) unique strings
   from a large set of strings where every string may contain wildcards.

## Examples

### `cows.Set`

Given the wildcard `*` and the strings:

```
AB*CD
A*CCD
WXYZ*
****A
```

An `cows.Set` could produce the strings:

```
AB*CD
WXYZ*
```

### `cows.Dict`

Given the key/value pairs:

```
AB*CD   1
A*CCD   2
WXYZ*   3
****A   4
```

An `cows.Dict` where the reduction function adds values together could produce:

```
AB*CD   3
WXYZ*   7
```

## Complexity

_cows_ was written because there did not appear to be an efficient method of
comparing one string to a collection of other strings where both the search
string and strings inthe collection could contain wildcards.  Most other
libraries pair-wise compare the values which quickly becomes inefficient.

All _cows_ data structures are built on top of the `cows.Trie` class.  Given an
input list of size `n` with maximum string of length `m`, the complexity is:

| Function  | Complexity |
------------|-------------
| Insertion | O(m)       |
| Lookup    | O(nm)      |
| Iteration | O(m)      |

So, for situations where the search string length, `m`, is less than the number
of strings to be searched, `n`, _cows_ should outperform the naive approach.
