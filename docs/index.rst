cows: Collections for wildcard strings
======================================

.. toctree::
    :hidden:

    data_structures

**cows** (**co**\ llections for **w**\ ildcard **s**\ trings) is a Python
library that provides efficient collection implementations where equality
checking allows for wildcards in both the search string and the strings already
in the collection.

Motivation
----------

cows was developed for a common problem in bioinformatics: given a set of DNA
sequences with the alphabet ``A``, ``T``, ``C``, ``G``, along with a wildcard
``N`` (indicating that the base is unknown), find the unique sequences and
perform some operation on them.  Examples of the operation are: counting how
many times each unique sequence occurs and generate a consensus sequence for
each unique sequence.

For a simple example, for counting unique sequences consider the following
input and desired output:

.. code-block:: none

    input           output
    -----           ------
    ATNG            ATNG 2 # Comprised of ATNG and ATCN
    ATCN            ANNT 1
    ANNT            GTTC 1
    GTTC

Notice this task requires comparing strings with wilcards not just in one
string, but in both.  For example, matching ``ATCN`` to ``ATNG`` requires that
the third and fourth characters both be considered wildcards.

Naively one could pairwise compare the sequences, ignore the positions where
either contains an ``N``, and check if all other positions match.  However,
this quickly becomes intractable as it scales with the square of the number of
sequences.

cows uses a modified implementation of atrie (:class:`cows.trie`) to reduce
this complexity to scale linearly with the number of sequences.

Provided Data Structures
------------------------

Below are examples for the data structures included with cows.  Please see the
documentation in :ref:`data-structures` for detailed
API information.

``cows.List``
^^^^^^^^^^^^^^

A :class:`cows.list` is a simple list implementation where insertion functions
similarly to the builtin ``list`` data structure, but accessor methods take
into account ambiguity.  For example:

.. code-block:: python

    l = cows.List(['ABCD', 'ABC*', '****', 'DEFG'])

    print(l.index('D***'))

The print statement outputs ``2`` since the first match for ``D***`` is at
position 2 (with a value of ``****``).


``cows.Set``
^^^^^^^^^^^^^

A :class:`cows.set` stores unique strings similar to the builtin ``set`` data
structure.  Instead of using hashes for equality checks, the underlying
:class:`cows.trie` is used to check if the pattern being inserted matches any
existing member of the set, taking into account wildcards in both.  For
example:

.. code-block:: python

    import cows

    s = cows.Set(wildcard='*')
    s.add('ABCD')
    s.add('*EFG')
    s.add('T')
    s.add('ABC*')  # Matches ABCD, so not added
    s.add('HEF*')  # Matches *EFG, so not added

    print(s)

Produces:

.. code-block:: none

    cows.Set(['*EFG', 'ABCD', 'T'])


``cows.Dict``
^^^^^^^^^^^^^^

cows dictionaries are similar to the builtin ``dict`` type insofar as they are
key/value stores.  They have a few key differences, however.

First, when setting a value, if there is an existing (potentially ambiguous)
match already in the dictionary, you can set an ``updater`` function to update
the existing value rather than simply overwrite it.  Further, when inserting a
key/value pair, multiple existing keys may match the new key due to ambiguity.
Specifying a ``selector`` function at instantiation lets you define to which of
the matches the ``updater`` should be applied.

See :class:`cows.dictionary` for more detailed information.

.. code-block:: python

    import cows

    def increment(match, old_value, new_value):
        return old_value + new_value

    my_dict = cows.Dict(updater=increment)
    my_dict['ABC'] = 1
    my_dict['DEF'] = 2
    my_dict['AB*'] = 10

    for k, v in sorted(my_dict.items()):
        print('{} --> {}'.format(k, v))

Produces:

.. code-block:: none

    ABC --> 11
    DEF --> 2

cows.Trie
^^^^^^^^^^
.. note::

    Generally the :class:`cows.trie` data structure shouldn't be used
    directly.  Consider using one of its abstractions.

All other cows data structures are based on the :class:`cows.trie` class.  It
allows for ambiguous queries taking into account wildcards both in the query
string and elements in the trie.

An example of it's use:

.. code-block:: python

    import cows

    t = cows.Trie()
    t['ABCD'] = 1
    t['DE*G'] = 5

    print('Matches for ABC* {}'.format(list(t.get_matches("ABC*"))))
    print('Matches for D*FG {}'.format(list(t.get_matches("D*FG"))))

Outputs:

.. code-block:: none

    Matches for ABC* [('ABCD', cows.Trie(D, 1))]
    Matches for D*FG [('DE*G', cows.Trie(G, 5))]


Performance
-----------
cows is performant, requiring *O(n)* time for insertions and lookups with
an input size of *n* strings.  The naive approach which is currently quite
common involves pairwise comparing the sequences in a collection resulting in
*O(n*\ :sup:`2`\ *)*, quickly becoming intractable.
