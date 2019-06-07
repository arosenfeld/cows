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

    assert list(sorted(trie)) == list(sorted(keys))

@pytest.mark.parametrize(
    'inputs,pattern,expected',
    [
        (
            ('ATCG', 'A*TT', 'CTCG'),
            '*TCG',
            ('ATCG', 'CTCG')
        ),
        (
            ('ATCG', 'A*TT', 'CTCG'),
            'ATTT',
            ('A*TT',)
        ),
        (
            ('ATCG', 'A*TT', 'CTCG'),
            'ATC',
            ()
        ),
        (
            ('ATCG', 'A*TT', 'CTCG'),
            '*TC',
            ()
        ),
        (
            ('ATCG', 'A*TT', 'CTCG'),
            '****',
            ('ATCG', 'A*TT', 'CTCG')
        ),
        (
            ('ATCG', 'A*TT', 'A*CG'),
            '*TCG',
            ('ATCG', 'A*CG')
        ),
        (
            ('ATCG', 'GCTA', 'TT*A'),
            'T*GA',
            ('TT*A',)
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
        (('ABC', 1), ('DEF', 2), ('DE*', 5)),
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
