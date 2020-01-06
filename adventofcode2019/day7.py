import argparse
import itertools
import logging
import queue
import threading
from contextlib import suppress
from time import sleep
from typing import Union, Iterable, Sequence

from adventofcode2019.intcodecomputer import IntcodeComputerV5

LOG = logging.getLogger(__name__)


def parta(code: Union[str, Iterable[Union[int, str]]]) -> int:
    code = [int(instruction) for instruction in code.split(',')]
    best = None, -1
    for phase_settings in itertools.permutations(range(5)):
        result = output_for_phase_settings(code, phase_settings)
        if result > best[1]:
            LOG.debug('Found setting %s -> %s', phase_settings, result)
            best = phase_settings, result

    return best[1]


def partb(code: Union[str, Iterable[Union[int, str]]]) -> int:
    code = [int(instruction) for instruction in code.split(',')]
    best = None, -1
    for phase_settings in itertools.permutations(range(5, 10)):
        result = feedback_for_phase_settings(code, phase_settings)
        if result > best[1]:
            LOG.debug('Found setting %s -> %s', phase_settings, result)
            best = phase_settings, result

    return best[1]




def output_for_phase_settings(code: Sequence[int], phase_settings: Iterable[int]) -> int:
    input_signal = 0

    for phase_setting in phase_settings:
        vm = IntcodeComputerV5(code, stdin=[int(phase_setting), input_signal])
        vm.run()
        input_signal = list(vm.stdout)[0]

    return input_signal


def feedback_for_phase_settings(code: Sequence[int], phase_settings: Iterable[int]) -> int:
    vms = [IntcodeComputerV5(code, stdin=[int(phase_setting)]) for phase_setting in phase_settings]
    threads = []
    for vm in vms:
        threads.append(threading.Thread(target=vm.run))
        threads[-1].start()

    vms[0].put_stdin(0)

    while any(thread.is_alive() for thread in threads):
        for idx in range(len(vms)):
            vm = vms[idx]
            with suppress(queue.Empty):
                vms[(idx + 1) % len(vms)].put_stdin(vm.get_stdout_nowait())
        sleep(0)  # ensure we rotate threads

    return vms[-1].get_stdout()


if __name__ == '__main__':
    import subprocess

    subprocess.run(['pwd'])
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='../inputs/day7.txt')
    args = parser.parse_args()
    input_data = args.infile.read()
    print(parta(input_data))
    print(partb(input_data))
