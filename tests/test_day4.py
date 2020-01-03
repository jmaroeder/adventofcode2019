import logging

import pytest

from adventofcode2019.day4 import password_is_valid, password_is_valider


@pytest.mark.parametrize(
    ('password', 'is_valid'), [
        (111111, True),
        (223450, False),
        (123789, False),
    ],
)
def test_password_is_valid(password, is_valid, caplog):
    caplog.set_level(logging.DEBUG)
    assert password_is_valid(password) == is_valid


@pytest.mark.parametrize(
    ('password', 'is_valid'), [
        (111111, False),
        (223450, False),
        (123789, False),
        (112233, True),
        (123444, False),
        (111122, True),
    ],
)
def test_password_is_valider(password, is_valid, caplog):
    caplog.set_level(logging.DEBUG)
    assert password_is_valider(password) == is_valid
