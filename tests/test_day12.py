import logging
import string
from textwrap import dedent

import pytest

from adventofcode2019.day12 import GravitationalSystem, partb

LOG = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ('steps', 'pos_and_vel'), [
        (0, dedent('''\
            pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>
        ''')),
        (1, dedent('''\
            pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
            pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
            pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
            pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>
        ''')),
        (2, dedent('''\
            pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
            pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
            pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
            pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>
        ''')),
        (3, dedent('''\
            pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>
            pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>
            pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>
            pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>
        ''')),
        (4, dedent('''\
            pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>
            pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>
            pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>
            pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>
        ''')),
        (5, dedent('''\
            pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>
            pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>
            pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>
            pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>
        ''')),
        (6, dedent('''\
            pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>
            pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>
            pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>
            pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>
        ''')),
        (7, dedent('''\
            pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>
            pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>
            pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>
            pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>
        ''')),
        (8, dedent('''\
            pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>
            pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>
            pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>
            pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>
        ''')),
        (9, dedent('''\
            pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>
            pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>
            pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>
            pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>
        ''')),
        (10, dedent('''\
            pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
            pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
            pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
            pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
        ''')),
    ],
)
def test_positions(steps: int, pos_and_vel: str, caplog):
    caplog.set_level(logging.DEBUG)
    initial_positions = dedent('''\
        <x=-1, y=0, z=2>
        <x=2, y=-10, z=-7>
        <x=4, y=-8, z=8>
        <x=3, y=5, z=-1>
    ''')
    gs = GravitationalSystem(initial_positions.strip())
    for _ in range(steps):
        gs.tick()
    whitespace_remover = str.maketrans(dict.fromkeys(string.whitespace))
    assert gs.pos_and_vel.translate(whitespace_remover) == pos_and_vel.translate(whitespace_remover)



@pytest.mark.parametrize(
    ('steps', 'pos_and_vel'), [
        (0, dedent('''\
            pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
            pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
            pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
            pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>
        ''')),
        (10, dedent('''\
            pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
            pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
            pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
            pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>
        ''')),
        (20, dedent('''\
            pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>
            pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>
            pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>
            pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>
        ''')),
        (30, dedent('''\
            pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>
            pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>
            pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>
            pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>
        ''')),
        (40, dedent('''\
            pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>
            pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>
            pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>
            pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>
        ''')),
        (50, dedent('''\
            pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
            pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
            pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
            pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>
        ''')),
        (60, dedent('''\
            pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>
            pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>
            pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>
            pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>
        ''')),
        (70, dedent('''\
            pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>
            pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>
            pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>
            pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>
        ''')),
        (80, dedent('''\
            pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>
            pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>
            pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>
            pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>
        ''')),
        (90, dedent('''\
            pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>
            pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>
            pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>
            pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>
        ''')),
        (100, dedent('''\
            pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
            pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
            pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
            pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>
        ''')),
    ],
)
def test_positions_2(steps: int, pos_and_vel: str, caplog):
    caplog.set_level(logging.DEBUG)
    initial_positions = dedent('''\
        <x=-8, y=-10, z=0>
        <x=5, y=5, z=10>
        <x=2, y=-7, z=3>
        <x=9, y=-8, z=-3>
    ''')
    gs = GravitationalSystem(initial_positions.strip())
    for _ in range(steps):
        gs.tick()
    whitespace_remover = str.maketrans(dict.fromkeys(string.whitespace))
    assert gs.pos_and_vel.translate(whitespace_remover) == pos_and_vel.translate(whitespace_remover)

@pytest.mark.parametrize(
    ('steps', 'total_energy', 'initial_positions'), [
        (10, 179, dedent('''\
            <x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>
        ''')),
        (100, 1940, dedent('''\
            <x=-8, y=-10, z=0>
            <x=5, y=5, z=10>
            <x=2, y=-7, z=3>
            <x=9, y=-8, z=-3>
        ''')),
    ]
)
def test_energy(steps: int, total_energy: int, initial_positions: str, caplog):
    caplog.set_level(logging.DEBUG)
    gs = GravitationalSystem(initial_positions.strip())
    for _ in range(steps):
        gs.tick()
    assert(gs.total_energy == total_energy)


@pytest.mark.parametrize(
    ('steps', 'initial_positions'), [
        (2772, dedent('''\
            <x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>
        ''')),
        (4686774924, dedent('''\
            <x=-8, y=-10, z=0>
            <x=5, y=5, z=10>
            <x=2, y=-7, z=3>
            <x=9, y=-8, z=-3>
        ''')),
    ]
)
def test_partb(steps: int, initial_positions: str, caplog):
    caplog.set_level(logging.DEBUG)
    assert partb(initial_positions) == steps
