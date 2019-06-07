import pytest

import basco


test_set = [
    ['ABCD', '*EFG', 'T', 'ABC*', 'HEF*'],
]


@pytest.mark.parametrize('elements', test_set)
def test_initialize(elements):
    rlist = basco.List(elements)
    assert list(rlist) == elements


@pytest.mark.parametrize('elements', test_set)
def test_append(elements):
    rlist = basco.List()
    for element in elements:
        rlist.append(element)

    assert list(rlist) == elements


@pytest.mark.parametrize('elements', test_set)
def test_extend(elements):
    rlist = basco.List()

    rlist.extend(elements)
    rlist.extend(elements)

    assert list(rlist) == elements * 2

@pytest.mark.parametrize('elements', test_set)
def test_insert(elements):
    rlist = basco.List()

    for element in elements:
        rlist.insert(0, element)

    assert list(rlist) == list(reversed(elements))


@pytest.mark.parametrize('elements', [
    [
        ('ABCD', [0, 1, 2]),
        ('ABC*', [0, 1, 2]),
        ('*BC*', [0, 1, 2]),
        ('T', [3])
    ]
])
def test_index(elements):
    rlist = basco.List([e[0] for e in elements])
    for element, correct_idxs in elements:
        assert rlist.index(element) in correct_idxs

    with pytest.raises(ValueError):
        rlist.index('XXX')

    for element, correct_idxs in elements:
        assert rlist.index(element) in correct_idxs


@pytest.mark.parametrize('elements', [
    [
        ('ABCD', 3),
        ('ABC*', 3),
        ('*BC*', 3),
        ('GGG*', 2),
        ('GGGG', 2),
        ('GGTG', 1),
        ('T', 1)
    ]
])
def test_count(elements):
    rlist = basco.List([e[0] for e in elements])
    for element, correct_cnt in elements:
        assert rlist.count(element) == correct_cnt

@pytest.mark.parametrize('elements', test_set)
def test_contains(elements):
    rlist = basco.List(elements)
    for element in elements:
        assert element in rlist

    assert 'XXXXXX' not in rlist


@pytest.mark.parametrize('elements', test_set)
def test_reverse(elements):
    rlist = basco.List(elements)
    rlist.reverse()
    assert list(rlist) == list(reversed(elements))

def test_repr():
    rlist = basco.List(['A', 'B', 'C'])
    assert rlist.__repr__() == 'basco.List([\'A\', \'B\', \'C\'])'
