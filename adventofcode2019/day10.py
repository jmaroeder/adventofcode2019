import argparse
import logging
import math
from typing import Mapping, MutableMapping, Optional, Set, Tuple

import numpy

LOG = logging.getLogger(__name__)


def asteroid_dist(src: Tuple[int, int], dst: Tuple[int, int]) -> int:
    return abs(dst[0] - src[0]) + abs(dst[1] - src[1])


class AsteroidMap:
    def __init__(self, map_str: str) -> None:
        map_str = map_str.strip()
        self.height = map_str.count('\n') + 1
        self.width = map_str.index('\n')
        self.asteroids = self.load_map(map_str)

        self._detectables_asteroid_count: Optional[int] = None
        self._detectables: MutableMapping[Tuple[int, int], int] = {}

        self.laser_angle: float = numpy.nextafter(math.atan2(-1, 0), -numpy.inf)  # "up" in map coords, slightly left
        self.last_vaporized: Optional[Tuple[int, int]] = None

        self.base_position: Tuple[int, int] = self._get_base_position()

    @staticmethod
    def load_map(map_str: str) -> Set[Tuple[int, int]]:
        ret = set()
        for y, row in enumerate(map_str.strip().splitlines()):
            for x, char in enumerate(row.strip()):
                if char == '#':
                    ret.add((x, y))
        return ret

    def _get_base_position(self) -> Tuple[int, int]:
        return max(self.detectables.keys(), key=lambda d: self.detectables[d])

    def count_visible_asteroids(self, src: Tuple[int, int]) -> int:
        return len(self.get_visible_asteroids(src))

    def get_visible_asteroids(self, src: Tuple[int, int]) -> Set[Tuple[int, int]]:
        return set(self.get_angle_map(src).values())

    def get_angle_map(self, src: Tuple[int, int] = None) -> Mapping[float, Tuple[int, int]]:
        src = src or self.base_position
        angle_map: MutableMapping[float, Tuple[int, int]] = {}
        for dst in self.asteroids:
            if dst == src:
                continue
            angle = math.atan2(dst[1] - src[1], dst[0] - src[0])
            if angle not in angle_map or asteroid_dist(src, dst) < asteroid_dist(src,
                                                                                 angle_map[angle]):
                angle_map[angle] = dst
                continue

        return angle_map

    def get_next_angle_and_asteroid(self) -> Tuple[float, Tuple[int, int]]:
        def angle_picker(angle_and_asteroid: Tuple[float, Tuple[int, int]]) -> float:
            angle, asteroid = angle_and_asteroid
            dangle = ((angle - self.laser_angle + 3 * math.pi) % (2 * math.pi) - (math.pi)) % (2 * math.pi)
            if angle == self.laser_angle:
                dangle += 2 * math.pi
            return dangle

        return min(self.get_angle_map().items(), key=angle_picker)

    @property
    def detectables(self) -> Mapping[Tuple[int, int], int]:
        if self._detectables_asteroid_count == len(self.asteroids):
            return self._detectables
        LOG.warning('(re)Computing detectables...')
        self._detectables = {}
        for asteroid in self.asteroids:
            self._detectables[asteroid] = self.count_visible_asteroids(asteroid)
        self._detectables_asteroid_count = len(self.asteroids)
        return self._detectables

    @property
    def value_map(self) -> str:
        ret = ''
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.detectables:
                    ret += '.'
                    continue
                ret += chr(ord('0') + self.detectables[(x, y)])
            ret += '\n'
        return ret

    def vaporize(self) -> None:
        angle, asteroid = self.get_next_angle_and_asteroid()
        self.laser_angle = angle
        self.asteroids.remove(asteroid)
        self.last_vaporized = asteroid


def parta(map_str: str) -> int:
    amap = AsteroidMap(map_str)
    return amap.detectables[amap.base_position]


def partb(map_str: str, iterations: int = 200) -> int:
    amap = AsteroidMap(map_str)
    for _ in range(iterations):
        amap.vaporize()
    return amap.last_vaporized[0] * 100 + amap.last_vaporized[1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day10.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    print(partb(input_data))
