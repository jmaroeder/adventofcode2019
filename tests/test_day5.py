import logging

import pytest

from adventofcode2019.intcode.computer import run_intcode, IntcodeComputerV5

LOG = logging.getLogger(__name__)

@pytest.mark.parametrize(
    ('initial', 'final'), [
        ('1002,4,3,4,33', '1002,4,3,4,99'),
    ],
)
def test_parta(initial, final, caplog):
    caplog.set_level(logging.DEBUG)
    assert run_intcode(initial, comp_cls=IntcodeComputerV5) == final


@pytest.mark.parametrize(
    ('initial', 'stdin', 'stdout'), [
        ('3,0,4,0,99', [42], [42]),
    ],
)
def test_parta_io(initial, stdin, stdout, caplog):
    caplog.set_level(logging.DEBUG)
    vm = IntcodeComputerV5(initial=initial, stdin=stdin)
    vm.run()
    assert list(vm.stdout) == stdout


@pytest.mark.parametrize(
    ('initial', 'stdin', 'stdout'), [
        ('3,9,8,9,10,9,4,9,99,-1,8', [8], [1]),
        ('3,9,8,9,10,9,4,9,99,-1,8', [7], [0]),
        ('3,9,7,9,10,9,4,9,99,-1,8', [7], [1]),
        ('3,9,7,9,10,9,4,9,99,-1,8', [8], [0]),
        ('3,3,1108,-1,8,3,4,3,99', [8], [1]),
        ('3,3,1108,-1,8,3,4,3,99', [7], [0]),
        ('3,3,1107,-1,8,3,4,3,99', [7], [1]),
        ('3,3,1107,-1,8,3,4,3,99', [8], [0]),
        ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [0], [0]),
        ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [1], [1]),
        ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [0], [0]),
        ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [1], [1]),
        (
            '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
            [7],
            [999],
        ),
        (
            '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
            [8],
            [1000],
        ),
        (
            '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99',
            [9],
            [1001],
        ),
    ],
)
def test_partb(initial, stdin, stdout, caplog):
    caplog.set_level(logging.DEBUG)
    LOG.info('Using stdin: %s, expecting stdout: %s', stdin, stdout)
    vm = IntcodeComputerV5(initial=initial, stdin=stdin)
    vm.run()
    assert list(vm.stdout) == stdout



