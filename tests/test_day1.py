import pytest

from adventofcode2019.day1 import get_fuel, get_total_fuel


@pytest.mark.parametrize(
    ('mass', 'fuel'), [
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
    ],
)
def test_parta(mass, fuel):
    assert get_fuel(mass) == fuel


@pytest.mark.parametrize(
    ('mass', 'fuel'), [
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ],
)
def test_partb(mass, fuel):
    assert get_total_fuel(mass) == fuel
