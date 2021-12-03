from typing import Iterable
from functools import cached_property

import pytest
import pandas as pd


def count_increases(depths: Iterable[int]) -> int:
    return Depths.from_iter(depths).total_increases


def count_3_window_increases(depths: Iterable[int]) -> int:
    return Depths.from_iter(depths).total_window_increases


class Depths:
    def __init__(self, df):
        self.df = df
        self.state = 'raw'

    @classmethod
    def from_iter(cls, it):
        df = pd.DataFrame({'depths': list(it)}, columns=['depths'])
        return cls(df)

    @cached_property
    def depths(self):
        return self.df.depths

    @cached_property
    def n1(self):
        return self.depths.shift(-1)

    @cached_property
    def n2(self):
        return self.n1.shift(-1)

    @cached_property
    def has_increased(self):
        return self.depths.lt(self.n1)

    @cached_property
    def sum_of_3_window(self):
        df = self.df
        df['n1'] = self.n1
        df['n2'] = self.n2
        return df.sum(axis=1)

    @cached_property
    def total_increases(self):
        return self.has_increased.sum()

    @cached_property
    def window_has_increased(self):
        return self.sum_of_3_window.lt(self.next_sum_of_three)

    @cached_property
    def next_sum_of_three(self):
        return self.sum_of_3_window.shift(-1)

    @cached_property
    def total_window_increases(self):
        return self.window_has_increased.sum()


@pytest.fixture
def depths():
    return [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_count_increases(depths):
    assert count_increases(depths) == 7


def test_count_3_window_increases(depths):
    assert count_3_window_increases(depths) == 5


def test_regression1():
    assert main1() == 1711


def test_regression2():
    assert main2() == 1743


def main1():
    return count_increases(parse_input('1.txt', int))


def main2():
    return count_3_window_increases(parse_input('1.txt', int))


def parse_input(filename, cast):
    with open(filename) as f:
        for line in f:
            yield cast(line.strip())


if __name__ == "__main__":
    print(1, main1())
    print(2, main2())
    pytest.main([__file__])
