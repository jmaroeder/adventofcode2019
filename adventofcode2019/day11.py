import argparse
import logging
import queue
from collections import defaultdict
from contextlib import suppress
from enum import Enum
from typing import Iterable, Union, MutableMapping, MutableSet

from adventofcode2019.boundless_grid import BoundlessGrid, Coord
from adventofcode2019.intcode.computer import IntcodeComputerV11
from adventofcode2019.intcode.exceptions import WaitingForInput

LOG = logging.getLogger(__name__)


class Color(Enum):
    BLACK = 0
    WHITE = 1


class Direction(Enum):
    N = Coord(0, 1)
    E = Coord(1, 0)
    S = Coord(0, -1)
    W = Coord(-1, 0)


TURNS = {
    Direction.N: [Direction.W, Direction.E],
    Direction.E: [Direction.N, Direction.S],
    Direction.S: [Direction.E, Direction.W],
    Direction.W: [Direction.S, Direction.N],
}


class Hull(BoundlessGrid):
    def default_factory(self):
        return Color.BLACK

    def str_for_value(self, value: Color) -> str:
        if value == Color.BLACK:
            return ' '
        elif value == Color.WHITE:
            return '#'


class PaintingRobot:
    def __init__(self, code: str) -> None:
        self.computer = IntcodeComputerV11(code)
        self.hull: MutableMapping[Coord, Color] = Hull()
        self.location = Coord(0, 0)
        self.direction = Direction.N
        self.painted_locations: MutableSet[Coord] = set()

    def run(self) -> None:
        while not self.computer.is_terminated:
            try:
                self.computer.run()
            except WaitingForInput:
                # print(self.hull)
                self.check_computer_output()
                self.give_computer_input()

    def check_computer_output(self) -> None:
        with suppress(queue.Empty):
            color = Color(self.computer.get_stdout_nowait())
            turn = self.computer.get_stdout_nowait()
            self.hull[self.location] = color
            self.painted_locations.add(self.location)
            self.direction = TURNS[self.direction][turn]
            self.location += self.direction.value

    def give_computer_input(self) -> None:
        self.computer.put_stdin(self.detect_color())

    def detect_color(self) -> int:
        return self.hull[self.location].value


def parta(code: Union[str, Iterable[Union[int, str]]]) -> int:
    pr = PaintingRobot(code)
    pr.run()
    return len(pr.painted_locations)


def partb(code: Union[str, Iterable[Union[int, str]]]) -> int:
    pr = PaintingRobot(code)
    pr.hull[0, 0] = Color.WHITE
    pr.run()
    print(pr.hull)


# def partb(code: Union[str, Iterable[Union[int, str]]]) -> int:
#     vm = IntcodeComputerV9(code, stdin=[2])
#     vm.run()
#     output = list(vm.stdout)
#     for val in output:
#         print(val)
#

if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day11.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    partb(input_data)
