import pytest

import cows

test_set = [(
    ('ABCD', '*EFG', 'T', 'ABC*', 'HEF*'),
    ('ABCD', '*EFG', 'T')
)]


@pytest.mark.parametrize('keys,expected', test_set)
def test_initialize(keys, expected):
    rset = cows.Set(keys)
    assert sorted(rset) == sorted(expected)


@pytest.mark.parametrize(
    'keys,expected', test_set
)
def test_add(keys, expected):
    rset = cows.Set()
    for key in keys:
        rset.add(key)

    assert len(rset) == len(expected)
    for key in rset:
        assert key in expected
    for key in expected:
        assert key in rset


def test_repr():
    rset = cows.Set(['A', 'B', 'C'])
    assert rset.__repr__() == 'cows.Set([\'A\', \'B\', \'C\'])'
