import argparse
from math import floor
from os import environ


def parta(input_data: str) -> int:
    masses = [int(mass) for mass in input_data.splitlines()]
    return sum(get_fuel(mass) for mass in masses)


def get_fuel(mass: float) -> int:
    return floor(mass / 3) - 2


def partb(input_data: str) -> int:
    masses = [int(mass) for mass in input_data.splitlines()]
    return sum(get_total_fuel(mass) for mass in masses)


def get_total_fuel(mass: float) -> int:
    total = 0
    next = get_fuel(mass)
    while next > 0:
        total += next
        next = get_fuel(next)
    return total


if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day1.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    print(partb(input_data))
