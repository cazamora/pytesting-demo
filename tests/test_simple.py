import pytest
from pytesting import app
from hypothesis import given
import hypothesis.strategies as strat

# basic example testing
def test_reverse_list():
    numbers = [1,2,3,4,5]
    result=app.reverse_list(numbers)
    assert len(numbers)==len(result)
    assert numbers[0] == result[-1]


def test_reverse_list_bad_test():
    numbers = []
    result=app.reverse_list(numbers)

    assert len(numbers)==len(result)

    # this will fail
    # assert numbers[0] == result[-1]

    # out of bounds
    with pytest.raises(IndexError):
        assert result[0]


# using hypothesis
@given(strat.lists(strat.integers(), min_size=1))
def test_reverse_list_hypothesis(numbers):
    result=app.reverse_list(numbers)
    assert len(numbers)==len(result)
    assert numbers[0] == result[-1]


# better
@given(strat.lists(strat.integers()))
def test_reverse_list_hypothesis_better(numbers):
    result=app.reverse_list(numbers)
    assert numbers == app.reverse_list(app.reverse_list(numbers))