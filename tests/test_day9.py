from adventofcode2019.day9 import *

from adventofcode2019.intcode.computer import IntcodeComputerV9

LOG = logging.getLogger(__name__)


def test_quine(caplog):
    caplog.set_level(logging.DEBUG)
    code = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    vm = IntcodeComputerV9(code)
    vm.run()
    assert list(vm.stdout) == [int(val) for val in code.split(',')]


def test_16digit(caplog):
    caplog.set_level(logging.DEBUG)
    code = '1102,34915192,34915192,7,4,7,99,0'
    vm = IntcodeComputerV9(code)
    vm.run()
    output = list(vm.stdout)[0]
    assert len(str(output)) == 16


def test_middle_num(caplog):
    caplog.set_level(logging.DEBUG)
    code = '104,1125899906842624,99'
    vm = IntcodeComputerV9(code)
    vm.run()
    output = list(vm.stdout)[0]
    assert output == 1125899906842624


