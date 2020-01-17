import argparse
import functools
import itertools
import logging
import math
import re
from typing import List, Sequence, MutableSet, MutableMapping

import attr

LOG = logging.getLogger(__name__)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Vec3:
    x: int = 0
    y: int = 0
    z: int = 0

    @property
    def as_list(self) -> List[int]:
        return [self.x, self.y, self.z]

    def __add__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self) -> str:
        return f'x={self.x}, y={self.y}, z={self.z}'


@attr.s(auto_attribs=True, slots=True)
class GravitationalObject:
    pos: Vec3
    vel: Vec3 = attr.Factory(Vec3)

    def gravitate_with(self, other: 'GravitationalObject') -> None:
        """modifies THIS and OTHER object's velocity - make sure not to double!"""
        my_vel = self.vel.as_list
        their_vel = other.vel.as_list

        for idx, poses in enumerate(zip(self.pos.as_list, other.pos.as_list)):
            my_pos, their_pos = poses
            diff = (0, 0)
            if my_pos < their_pos:
                diff = (1, -1)
            elif my_pos > their_pos:
                diff = (-1, 1)
            my_vel[idx] += diff[0]
            their_vel[idx] += diff[1]
        self.vel = Vec3(*my_vel)
        other.vel = Vec3(*their_vel)

    def tick(self) -> None:
        self.pos += self.vel

    @property
    def pos_and_vel(self) -> str:
        return f'pos=<{self.pos}>, vel=<{self.vel}>'

    @property
    def potential_energy(self) -> int:
        return sum(abs(val) for val in self.pos.as_list)

    @property
    def kinetic_energy(self) -> int:
        return sum(abs(val) for val in self.vel.as_list)

    @property
    def total_energy(self) -> int:
        return self.potential_energy * self.kinetic_energy


class GravitationalSystem:
    def __init__(self, initial: str) -> None:
        self.objects = self.load_objects(initial)

    def load_objects(self, initial: str) -> Sequence[GravitationalObject]:
        ret: List[GravitationalObject] = []
        for obj_desc in initial.strip().splitlines():
            x, y, z = (int(value) for value in
                       re.match(r'^<x=([0-9-]+), y=([0-9-]+), z=([0-9-]+)>$', obj_desc).groups())
            ret.append(GravitationalObject(pos=Vec3(x, y, z)))
        return ret

    def tick(self) -> None:
        for obj1, obj2 in itertools.combinations(self.objects, 2):
            obj1.gravitate_with(obj2)

        for obj in self.objects:
            obj.tick()

    @property
    def pos_and_vel(self) -> str:
        return '\n'.join(obj.pos_and_vel for obj in self.objects)

    @property
    def total_energy(self) -> int:
        return sum(obj.total_energy for obj in self.objects)

    def state(self, dimension: str) -> Sequence[int]:
        return [getattr(obj.pos, dimension) for obj in self.objects] + \
               [getattr(obj.vel, dimension) for obj in self.objects]


def parta(moon_locs: str, steps: int = 1000) -> int:
    gs = GravitationalSystem(moon_locs.strip())
    for _ in range(steps):
        gs.tick()
    return gs.total_energy


def lcm(a: int, b: int) -> int:
    return abs(a*b) // math.gcd(a, b)


def partb(moon_locs: str) -> int:
    gs = GravitationalSystem(moon_locs.strip())
    ticks = 0
    ticks_to_repeat: MutableMapping[str, int] = {}
    unknown_dimensions = {'x', 'y', 'z'}
    states_by_dimension: MutableMapping[str, MutableSet[Sequence[int]]] = {dimension: set() for dimension in unknown_dimensions}
    while unknown_dimensions:
        for dimension in unknown_dimensions:
            state = tuple(gs.state(dimension))
            if state in states_by_dimension[dimension]:
                ticks_to_repeat[dimension] = ticks
            states_by_dimension[dimension].add(state)
        gs.tick()
        ticks += 1
        unknown_dimensions -= set(ticks_to_repeat.keys())

    # strategy: find the ticks when each individual **dimension** repeats,
    # then find the LCM of those 3
    return functools.reduce(lcm, ticks_to_repeat.values())


if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day12.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    print(partb(input_data))
