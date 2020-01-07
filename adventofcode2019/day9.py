import argparse
import logging
from typing import Iterable, Union

from adventofcode2019.intcode.computer import IntcodeComputerV9

LOG = logging.getLogger(__name__)


def parta(code: Union[str, Iterable[Union[int, str]]]) -> int:
    vm = IntcodeComputerV9(code, stdin=[1])
    vm.run()
    output = list(vm.stdout)
    print(output)
    return output[-1]


def partb(code: Union[str, Iterable[Union[int, str]]]) -> int:
    vm = IntcodeComputerV9(code, stdin=[2])
    vm.run()
    output = list(vm.stdout)
    for val in output:
        print(val)


if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day9.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    partb(input_data)
