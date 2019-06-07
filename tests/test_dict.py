import pytest

import basco


@pytest.mark.parametrize(
    'keys,expected',
    [
        (
            ('ATCG', 'GCTA', '****'),
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
            (('ATCG', 1), ('GCTA', 2), ('TT*A', 3), ('T*GA', 4), ('****', 5)),
            {'ATCG': 6, 'GCTA': 2, 'TT*A': 7}
        )
    ]
)
def test_update(keys, expected):
    def incr(match, current_value, new_value):
        return current_value + new_value

    rdict = basco.Dict(updater=incr, initialize=keys)

    assert len(rdict) == len(expected)

    # To cover .items()
    for key, value in rdict.items():
        assert expected[key] == value

    # To cover __iter__
    for key in rdict:
        assert [expected[key]] == list(rdict[key])


    for k, v in expected.items():
        vals = list(rdict[k])
        assert len(vals) == 1
        assert next(rdict[k]) == v


def test_repr():
    rdict = basco.Dict()
    assert rdict.__repr__() == 'basco.Dict()'

