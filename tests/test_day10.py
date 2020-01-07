import logging
from textwrap import dedent

import pytest

from adventofcode2019.day10 import AsteroidMap, parta, partb

LOG = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ('map_str', 'value_map'), [
        (dedent('''\
            .#..#
            .....
            #####
            ....#
            ...##
        '''), dedent('''\
            .7..7
            .....
            67775
            ....7
            ...87
        ''')),

    ],
)
def test_value_map(map_str, value_map, caplog):
    caplog.set_level(logging.DEBUG)
    asteroid_map = AsteroidMap(map_str)
    LOG.info("\n%s", asteroid_map.value_map)
    assert asteroid_map.value_map == value_map


@pytest.mark.parametrize(
    ('map_str', 'best'), [
        (dedent('''\
            ......#.#.
            #..#.#....
            ..#######.
            .#.#.###..
            .#..#.....
            ..#....#.#
            #..#....#.
            .##.#..###
            ##...#..#.
            .#....####
        '''), 33),
        (dedent('''\
            #.#...#.#.
            .###....#.
            .#....#...
            ##.#.#.#.#
            ....#.#.#.
            .##..###.#
            ..#...##..
            ..##....##
            ......#...
            .####.###.
        '''), 35),
        (dedent('''\
            .#..#..###
            ####.###.#
            ....###.#.
            ..###.##.#
            ##.##.#.#.
            ....###..#
            ..#.#..#.#
            #..#.#.###
            .##...##.#
            .....#.#..
        '''), 41),
        (dedent('''\
            .#..##.###...#######
            ##.############..##.
            .#.######.########.#
            .###.#######.####.#.
            #####.##.#.##.###.##
            ..#####..#.#########
            ####################
            #.####....###.#.#.##
            ##.#################
            #####.##.###..####..
            ..######..##.#######
            ####.##.####...##..#
            .#####..#.######.###
            ##...#.##########...
            #.##########.#######
            .####.#.###.###.#.##
            ....##.##.###..#####
            .#.#.###########.###
            #.#.#.#####.####.###
            ###.##.####.##.#..##
        '''), 210),
    ],
)
def test_parta(map_str, best, caplog):
    caplog.set_level(logging.DEBUG)
    assert parta(map_str) == best


@pytest.mark.parametrize(
    ('map_str', 'iterations', 'winner'), [
        (dedent('''\
            .#....#####...#..
            ##...##.#####..##
            ##...#...#.#####.
            ..#.....#...###..
            ..#.#.....#....##
        '''), 1, 801),
        (dedent('''\
            .#....#####...#..
            ##...##.#####..##
            ##...#...#.#####.
            ..#.....#...###..
            ..#.#.....#....##
        '''), 2, 900),
    ],
)
def test_partb(map_str, iterations, winner, caplog):
    caplog.set_level(logging.DEBUG)
    assert partb(map_str, iterations=iterations) == winner


@pytest.mark.parametrize(
    ('iterations', 'winner'), [
        (1, 1112),
        (2, 1201),
        (3, 1202),
        (10, 1208),
        (20, 1600),
        (50, 1609),
        (100, 1016),
        (199, 906),
        (200, 802),
        (201, 1009),
        (299, 1101),
    ],
)
def test_partb_big_map(iterations, winner, caplog):
    caplog.set_level(logging.DEBUG)
    map_str = dedent('''\
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
    ''')
    assert partb(map_str, iterations=iterations) == winner
