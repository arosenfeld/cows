DRAFT
=================================

.. toctree::
    :maxdepth: 2

    api

**basco** (**b**\ idirectional **a**\ mbiguous **s**\ tring **co**\ llections)
is a Python library that provides efficient ``set``- and ``dict``-like
collections where equality checking allows for wildcards in both the search
string **and** the strings already in the collection.
Motivation
----------

basco was developed for a common problem in bioinformatics: given a set of DNA
sequences with the alphabet ``[A, T, C, G]``, along with a wildcard ``N``
(indicating that the base is unknown), find the unique sequences and perform
some operation on them.  Maybe we want to count how many times each unique
sequence is found or for each unique sequence, generate a consensus sequence.

For a simple example, one may want to count how many times each sequence below
occurs:

.. code-block:: none

    input
    -----
    ATNG
    ATCN
    ANNT
    GTTC

The desired output may be:

.. code-block:: none

    output
    ------
    ATNG 2  # Comprised of ATNG and ATCN
    ANNT 1
    GTTC 1

Notice this task requires comparing strings with wilcards not just in one
string, but in both.  Naively one could pairwise compare the sequences, ignore
the positions where either contains an ``N``, and check if the other positions
match.  However, this quickly becomes time-consuming as it scales with the
square of the number of sequences.

basco uses a modified Trie (:class:`basco.Trie`) to reduce this complexity to
scale linearly with the number of sequences.

``basco.Set`` Example
---------------------

basco sets store unique strings similar to the builtin ``set`` data structure.
Instead of using hashes for equality checks, the underlying :class:`basco.Trie`
is used to check if the pattern being inserted matches any existing member of
the set, taking into account wildcards in both.  For example:

.. code-block:: python

    import basco

    s = basco.Set(wildcard='*')
    s.add('ABCD')
    s.add('*EFG')
    s.add('T')
    s.add('ABC*')  # Matches ABCD, so not added
    s.add('HEF*')  # Matches *EFG, so not added

    print(s)

Produces:

.. code-block:: none

    basco.Set(['ABCD', '*EFG', 'T'])


``basco.Dict`` Example
----------------------

basco dictionaries are similar to the builtin ``dict`` type insofar as they are
key/value stores.  They have a few key differences, however.

Performance
-----------
basco is performant, requiring *O(n)* time for insertions and lookups with
an input size of *n* strings.  The naive approach which is currently quite
common involves pairwise comparing the sequences in a collection resulting in
*O*(n^2)*, quickly becoming intractable.
