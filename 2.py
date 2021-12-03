from typing import Iterable
from functools import cached_property

import pytest
import pandas as pd


def test_regression1():
    assert main1() == 1670340


def test_regression2():
    assert main2() == 1954293920


class Directions:
    def __init__(self, df):
        self.df = df

    @classmethod
    def from_iter(cls, it: Iterable[str]):
        raw_directions = (val.split() for val in it)
        directions = [(d, int(m)) for d, m in raw_directions]
        df = pd.DataFrame(directions, columns=['direction', 'magnitude'])
        return cls(df)

    @cached_property
    def forwards(self) -> pd.DataFrame:
        return self.df.loc[self.df['direction'] == 'forward']

    @cached_property
    def downs(self) -> pd.DataFrame:
        return self.df.loc[self.df['direction'] == 'down']

    @cached_property
    def ups(self) -> pd.DataFrame:
        return self.df.loc[self.df['direction'] == 'up']

    @cached_property
    def horizontal_change(self):
        return self.forwards.magnitude.sum()

    @cached_property
    def vertical_change(self):
        return self.downs.magnitude.sum() - self.ups.magnitude.sum()

    @cached_property
    def horizontal_position(self) -> int:
        return self.horizontal_change.sum()

    @cached_property
    def depth(self) -> int:
        return self.vertical_change.sum()



class DirectionsUsingTheManual(Directions):

    @cached_property
    def aim_delta(self):
        down_values = self.downs.magnitude.fillna(0)
        up_values = self.ups.magnitude.fillna(0) * -1
        return down_values.combine_first(up_values)

    @cached_property
    def aim(self):
        return self.aim_delta.cumsum().astype(int)

    @cached_property
    def vertical_change(self):
        df = self.df
        df['aim'] = self.aim
        df['aim_multiplier'] = self.forwards.magnitude
        vertical_change = (df.aim.fillna(method='ffill') * df.aim_multiplier.fillna(0))
        return vertical_change.fillna(0)


def main1():
    directions = Directions.from_iter(parse_input('2.txt'))
    return directions.horizontal_position * directions.depth


def main2():
    directions = DirectionsUsingTheManual.from_iter(parse_input('2.txt'))
    return directions.horizontal_position * directions.depth


def parse_input(filename, cast=str):
    with open(filename) as f:
        for line in f:
            yield cast(line.strip())


if __name__ == "__main__":
    print(1, main1())
    print(2, main2())
    pytest.main([__file__])
