import pytest

import basco

test_set = [(
    ('ABCD', 'NEFG', 'T', 'ABCN', 'HEFN'),
    ('ABCD', 'NEFG', 'T')
)]


@pytest.mark.parametrize('keys,expected', test_set)
def test_initialize(keys, expected):
    rset = basco.Set(keys)
    assert sorted(rset) == sorted(expected)

@pytest.mark.parametrize(
    'keys,expected', test_set
)
def test_add(keys, expected):
    rset = basco.Set()
    for key in keys:
        rset.add(key)

    assert len(rset) == len(expected)
    for key in rset:
        assert key in expected


def test_repr():
    rset = basco.Set(['A', 'B', 'C'])
    assert rset.__repr__() == 'basco.Set([\'A\', \'B\', \'C\'])'