import argparse
import logging
import re
from collections import defaultdict
from itertools import zip_longest
from typing import List, Mapping, Sequence, Iterator, Optional

LOG = logging.getLogger(__name__)


class SpaceObject:
    def __init__(self, parent: 'SpaceObject' = None, name: str = '?'):
        self.parent = parent
        self.children: List[SpaceObject] = []
        self.name = name

    def __str__(self) -> str:
        return f'{self.name}: {",".join(child.name for child in self.children)}'

    @property
    def parents(self) -> Iterator['SpaceObject']:
        obj = self
        while obj.parent is not None:
            obj = obj.parent
            yield obj

    def dist_to(self, obj: 'SpaceObject') -> int:
        return tuple(self.parents).index(obj) + 1


def count_orbits(obj: SpaceObject) -> int:
    return len(tuple(obj.parents))


def closest_common_ancestor(obj1: SpaceObject, obj2: SpaceObject) -> Optional[SpaceObject]:
    succession1, succession2 = reversed(tuple(obj1.parents)), reversed(tuple(obj2.parents))
    last_anc = None
    for anc1, anc2 in zip_longest(succession1, succession2):
        if anc1 != anc2:
            return last_anc
        last_anc = anc1
    return obj1


def orbital_dist(obj1: SpaceObject, obj2: SpaceObject) -> int:
    ancestor = closest_common_ancestor(obj1, obj2)
    asc_dist = obj1.parent.dist_to(ancestor)
    desc_dist = obj2.parent.dist_to(ancestor)
    return asc_dist + desc_dist


def parta(orbitmap: str) -> int:
    space_objects = parse_orbitmap(orbitmap)

    LOG.info('space_objects:')
    for space_obj in space_objects.values():
        LOG.info(space_obj)

    return sum(count_orbits(space_obj) for space_obj in space_objects.values())


def partb(orbitmap: str) -> int:
    space_objects = parse_orbitmap(orbitmap)

    LOG.info('space_objects:')
    for space_obj in space_objects.values():
        LOG.info(space_obj)

    return orbital_dist(space_objects['YOU'], space_objects['SAN'])


def parse_orbitmap(orbitmap: str) -> Mapping[str, SpaceObject]:
    ret = defaultdict(SpaceObject)
    for line in orbitmap.strip('\n').splitlines():
        orbitee, orbiter = re.match(r'(^.+)\)(.+)$', line).groups()
        ret[orbiter].parent = ret[orbitee]
        ret[orbitee].children.append(ret[orbiter])
        ret[orbitee].name = orbitee
        ret[orbiter].name = orbiter
    return ret



if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day6.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    print(partb(input_data))
