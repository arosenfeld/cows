import pytest

import basco


@pytest.mark.parametrize(
    'keys',
    (
        ('ATCG', 'GCTA'),
    )
)
def test_set(keys):
    trie = basco.Trie(initialize=[(k, i) for i, k in enumerate(keys)])

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
    trie = basco.Trie(initialize=[(k, k) for k in inputs])
    matches = sorted([m[1].value for m in trie.get_matches(pattern)])
    assert matches == sorted(expected)


def test_invalid():
    trie = basco.Trie()
    with pytest.raises(ValueError):
        list(trie.children_matching('bad'))


def test_repr():
    trie = basco.Trie(key='abc', value=456)
    assert trie.__repr__() == 'basco.Trie(abc, 456)'


@pytest.mark.parametrize(
    'inputs',
    [
        (('ABC', 1), ('DEF', 2), ('DEN', 5)),
    ]
)
def test_items(inputs):
    trie = basco.Trie(initialize=inputs)
    inputs = dict(inputs)

    assert len(inputs) == len(trie)
    assert sorted(trie.keys()) == sorted(inputs.keys())
    assert sorted(trie.values(extract_values=True)) == sorted(inputs.values())

    for k, v in trie.items(extract_values=True):
        assert inputs[k] == v
