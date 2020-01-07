import argparse

from adventofcode2019.intcode.computer import run_intcode


def parta(input_data: str, noun: int = 12, verb: int = 2) -> str:
    input_state = [int(val) for val in input_data.split(',')]
    fixed_state = input_state.copy()
    fixed_state[1] = noun
    fixed_state[2] = verb
    return run_intcode(fixed_state).split(',')[0]


def partb(input_data: str) -> str:
    for noun in range(0, 100):
        for verb in range(0, 100):
            if parta(input_data, noun=noun, verb=verb) == '19690720':
                return str(100 * noun + verb)


if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day2.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    print(partb(input_data))
