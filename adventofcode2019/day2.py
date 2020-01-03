import argparse
from contextlib import suppress
from enum import Enum
import logging
from typing import Iterable, Union

LOG = logging.getLogger(__name__)


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    HALT = 99


class Halt(Exception):
    pass


class Intcode:
    def __init__(self, initial: Union[str, Iterable[Union[int, str]]]):
        if hasattr(initial, 'split'):
            initial = initial.split(',')
        self.state = [
            int(val) for val in initial
        ]
        self.pc = 0

    def run(self) -> None:
        with suppress(Halt):
            while True:
                self.tick()

    def tick(self) -> None:
        LOG.debug('PC=%s, STATE=%s', self.pc, str(self))
        opcode = Opcode(self.state[self.pc])
        LOG.debug('Executing %s', opcode.name)
        getattr(self, f'execute_{opcode.name.lower()}')()
        self.pc += 4

    def execute_add(self):
        self.output = self.input_1 + self.input_2

    def execute_multiply(self):
        self.output = self.input_1 * self.input_2

    def execute_halt(self):
        raise Halt()

    @property
    def input_1(self) -> int:
        return self.state[self.state[self.pc + 1]]

    @property
    def input_2(self) -> int:
        return self.state[self.state[self.pc + 2]]

    def set_output(self, value: int) -> None:
        self.state[self.state[self.pc + 3]] = value

    output = property(fget=None, fset=set_output)

    def __str__(self) -> str:
        return ','.join(str(val) for val in self.state)


def run_intcode(input_data: Union[str, Iterable[int]]) -> str:
    vm = Intcode(initial=input_data)
    vm.run()
    return str(vm)


def parta(input_data: str) -> str:
    input_state = [int(val) for val in input_data.split(',')]
    fixed_state = input_state.copy()
    fixed_state[1] = 12
    fixed_state[2] = 2
    return run_intcode(fixed_state).split(',')[0]


if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day2.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    # print(partb(input_data))
