import pytest

import basco


@pytest.mark.parametrize(
    'keys,expected',
    [
        (
            ('ATCG', 'GCTA', 'NNNN'),
            ('ATCG', 'GCTA')
        )
    ]
)
def test_initialize(keys, expected):
    rdict = basco.Dict(initialize=[(k, k) for k in keys])
    assert sorted(rdict.keys()) == sorted(expected)


@pytest.mark.parametrize(
    'keys,expected',
    [
        (
            (('ATCG', 1), ('GCTA', 2), ('TTNA', 3), ('TNGA', 4), ('NNNN', 5)),
            {'ATCG': 6, 'GCTA': 2, 'TTNA': 7}
        )
    ]
)
def test_update(keys, expected):
    def incr(match, current_value, new_value):
        return current_value + new_value

    rdict = basco.Dict(updater=incr, initialize=keys)

    assert len(rdict) == len(expected)
    for key, value in rdict.items():
        assert expected[key] == value

    for k, v in expected.items():
        vals = list(rdict[k])
        assert len(vals) == 1
        assert next(rdict[k]) == v

def test_repr():
    trie = basco.Dict()
    assert trie.__repr__() == 'basco.Dict()'
