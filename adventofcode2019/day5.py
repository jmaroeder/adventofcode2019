import argparse

from adventofcode2019.intcodecomputer import run_intcode, IntcodeComputerV5


def parta(instructions: str) -> None:
    instructions = [int(val) for val in instructions.split(',')]
    vm = IntcodeComputerV5(initial=instructions, stdin=[1])
    vm.run()
    for line in vm.stdout:
        print(line)


def partb(instructions: str) -> None:
    instructions = [int(val) for val in instructions.split(',')]
    vm = IntcodeComputerV5(initial=instructions, stdin=[5])
    vm.run()
    for line in vm.stdout:
        print(line)



if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day5.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    parta(input_data)
    partb(input_data)
