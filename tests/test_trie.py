import pytest

from ambigtree import AmbiguousTrie


@pytest.mark.parametrize(
    'keys',
    (('ATCG', 'GCTA'),)
)
def test_set(keys):
    trie = AmbiguousTrie(initialize=[(k, i) for i, k in enumerate(keys)])

    for i, k in enumerate(keys):
        assert trie[k].value == i


@pytest.mark.parametrize(
    'inputs,pattern,expected',
    [
        (
            ('ATCG', 'ANTT', 'CTCG'),
            'NTCG',
            ('ATCG', 'CTCG')
        ),
        (
            ('ATCG', 'ANTT', 'CTCG'),
            'ATTT',
            ('ANTT',)
        ),
        (
            ('ATCG', 'ANTT', 'CTCG'),
            'ATC',
            ()
        ),
        (
            ('ATCG', 'ANTT', 'CTCG'),
            'NTC',
            ()
        ),
        (
            ('ATCG', 'ANTT', 'CTCG'),
            'NNNN',
            ('ATCG', 'ANTT', 'CTCG')
        ),
        (
            ('ATCG', 'ANTT', 'ANCG'),
            'NTCG',
            ('ATCG', 'ANCG')
        ),
        (
            ('ATCG', 'GCTA', 'TTNA'),
            'TNGA',
            ('TTNA',)
        )
    ]
)
def test_ambig_match(inputs, pattern, expected):
    trie = AmbiguousTrie(initialize=[(k, k) for k in inputs])

    assert sorted(trie.get_matches(pattern)) == sorted(expected)


def test_invalid():
    trie = AmbiguousTrie()
    with pytest.raises(ValueError):
        list(trie.children_matching('bad'))


@pytest.mark.parametrize(
    'inputs',
    [
        (('ATCG', 'ATCN', 'NNNN', 'GCTA'),)
    ]
)
def test_values(inputs):
    trie = AmbiguousTrie(initialize=[(k, k) for k in inputs])

    assert sorted(trie.values()) == sorted(inputs)


def test_repr():
    trie = AmbiguousTrie(key='abc', value=456)
    assert trie.__repr__() == 'AmbiguousTrie(abc, 456)'
