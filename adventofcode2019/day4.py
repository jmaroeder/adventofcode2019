import argparse
import logging
import re
from typing import Union

LOG = logging.getLogger(__name__)


def password_is_valid(password: Union[int, str]) -> bool:
    password = str(password)
    if len(password) != 6:
        return False
    found_double = False
    prev = int(password[0])
    for cur in password[1:]:
        cur = int(cur)
        if cur < prev:
            return False
        if cur == prev:
            found_double = True
        prev = cur
    if found_double:
        LOG.debug(password)
    return found_double


def parta(domain: str) -> int:
    lowest, highest = re.match(r'(\d+)-(\d+)', domain).groups()
    lowest = int(lowest)
    highest = int(highest)

    return sum(password_is_valid(password) for password in range(lowest, highest + 1))


# def parta(wire_paths: Iterable[str]) -> int:
#     panel = FrontPanel(*wire_paths)
#     return manhattan_distance(panel.closest_manhattan)
#
#
# def partb(wire_paths: Iterable[str]) -> int:
#     panel = FrontPanel(*wire_paths)
#     return panel.closest_steps


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day4.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    # print(partb(input_data.splitlines()))
