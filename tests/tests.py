import pytest

from ambigtree import AmbiguousTrie

@pytest.mark.parametrize(
    'keys',
    (('ATCG', 'GCTA'),)
)
def test_set(keys):
    tree = AmbiguousTrie()
    for i, k in enumerate(keys):
        tree[k] = i

    for i, k in enumerate(keys):
        assert tree[k].value == i


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
    ]
)
def test_ambig_match(inputs, pattern, expected):
    tree = AmbiguousTrie()
    for key in inputs:
        tree[key] = key
    assert sorted(tree.get_matches(pattern)) == sorted(expected)
