import logging
from textwrap import dedent
import pytest

from adventofcode2019.day6 import parta, parse_orbitmap, closest_common_ancestor, orbital_dist

LOG = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ('orbitmap', 'checksum'), [
        (dedent('''\
            COM)B
            B)C
            C)D
            D)E
            E)F
            B)G
            G)H
            D)I
            E)J
            J)K
            K)L
        '''), 42),
    ],
)
def test_parta(orbitmap, checksum, caplog):
    caplog.set_level(logging.DEBUG)
    assert (parta(orbitmap)) == checksum


@pytest.mark.parametrize(
    ('obj1', 'obj2', 'anc'), [
        ('K', 'I', 'D'),
    ],
)
def test_closest_common_ancestor(obj1, obj2, anc, caplog):
    orbitmap = dedent('''\
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
    ''')
    caplog.set_level(logging.DEBUG)
    space_objects = parse_orbitmap(orbitmap)
    assert closest_common_ancestor(space_objects[obj1], space_objects[obj2]) == space_objects[anc]


@pytest.mark.parametrize(
    ('obj1', 'obj2', 'dist'), [
        ('YOU', 'SAN', 4),
    ],
)
def test_orbital_dist(obj1, obj2, dist, caplog):
    orbitmap = dedent('''\
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        K)YOU
        I)SAN
    ''')
    caplog.set_level(logging.DEBUG)
    space_objects = parse_orbitmap(orbitmap)
    assert orbital_dist(space_objects[obj1], space_objects[obj2]) == dist
