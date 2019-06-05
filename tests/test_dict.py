import pytest

from ambigtree import ReducedDict


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
    rdict = ReducedDict(initialize=[(k, k) for k in keys])
    assert sorted(rdict.values()) == sorted(expected)


@pytest.mark.parametrize(
    'keys,expected',
    [
        (
            ('ATCG', 'GCTA', 'TTNA', 'TNGA', 'NNNN'),
            {'TTNA': 2, 'GCTA': 2, 'ATCG': 1}
        )
    ]
)
def test_update(keys, expected):
    def _updater(selected):
        selected.counter += 1

    class _TestObj:
        def __init__(self, key):
            self.key = key
            self.counter = 1

        def incr(self):
            self.counter += 1

        def __gt__(self, other):
            return self.counter > other.counter

    rdict = ReducedDict(
        updater=_updater,
        initialize=[(k, _TestObj(k)) for k in keys]
    )
    assert len(rdict) == len(expected)
    for obj in rdict.values():
        assert obj.counter == expected[obj.key]

    for k, v in expected.items():
        assert len(list(rdict[k])) == 1
        assert next(rdict[k]).counter == v
