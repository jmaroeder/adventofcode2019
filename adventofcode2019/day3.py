import argparse
from collections import defaultdict
import logging
from typing import Tuple, Iterable

LOG = logging.getLogger(__name__)


class FrontPanel:
    def __init__(self, *wires: str):
        self.grid = defaultdict(int)
        self.wire_count = 0
        self.closest_manhattan = None
        self.closest_steps = None
        self.step_grid = defaultdict(int)

        for wire in wires:
            self.add_wire(segs=wire)
        LOG.debug(self)

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        top, right, bottom, left = 0, 0, 0, 0
        for key in self.grid.keys():
            x, y = key
            left = min(x, left)
            right = max(x, right)
            top = max(y, top)
            bottom = min(y, bottom)
        return (left, bottom), (right, top)

    def str_for_coord(self, coord: Tuple[int, int]) -> str:
        if coord == (0, 0):
            return 'o'
        elif coord in self.grid:
            return chr(ord('A') + self.grid[coord])
        else:
            return '.'

    def __str__(self) -> str:
        ret = ''
        bounds = self.bounds
        for y in range(bounds[1][1] + 1, bounds[0][1] - 1, -1):
            for x in range(bounds[0][0] - 1, bounds[1][0] + 2):
                ret += self.str_for_coord((x, y))
            ret += '\n'
        return ret

    DELTAS = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0),
    }

    def add_wire(self, segs: str, signifier: int = None) -> None:
        signifier = signifier or 2 ** self.wire_count
        self.wire_count += 1
        segs = segs.split(',')
        coord = (0, 0)
        steps = 0
        for seg in segs:
            direction = seg[0]
            dist = int(seg[1:])
            delta = self.DELTAS[direction]
            for _ in range(dist):
                coord = (
                    coord[0] + delta[0],
                    coord[1] + delta[1],
                )
                steps += 1
                if self.grid[coord] != signifier:
                    self.grid[coord] += signifier
                    self.step_grid[coord] += steps
                    if self.grid[coord] != signifier:
                        if self.closest_manhattan is None or \
                            manhattan_distance(coord) < manhattan_distance(self.closest_manhattan):
                            self.closest_manhattan = coord
                        if self.closest_steps is None or self.step_grid[coord] < self.closest_steps:
                            self.closest_steps = self.step_grid[coord]


def manhattan_distance(coord: Tuple[int, int]) -> int:
    return abs(coord[0]) + abs(coord[1])


def parta(wire_paths: Iterable[str]) -> int:
    panel = FrontPanel(*wire_paths)
    return manhattan_distance(panel.closest_manhattan)


def partb(wire_paths: Iterable[str]) -> int:
    panel = FrontPanel(*wire_paths)
    return panel.closest_steps


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day3.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data.splitlines()))
    print(partb(input_data.splitlines()))
