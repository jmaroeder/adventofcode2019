import logging

import pytest

from adventofcode2019.day4 import password_is_valid


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


# @pytest.mark.parametrize(
#     ('wire_paths', 'dist'), [
#         (('R8,U5,L5,D3', 'U7,R6,D4,L4'), 30),
#         (('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83'), 610),
#         (('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'), 410),
#     ],
# )
# def test_partb(wire_paths, dist, caplog):
#     caplog.set_level(logging.DEBUG)
#     assert partb(wire_paths) == dist
