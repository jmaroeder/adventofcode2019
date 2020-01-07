import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .exceptions import Halt, ParameterError
from .opcode import Opcode

if TYPE_CHECKING:
    from .computer import IntcodeComputer


class Instruction(ABC):
    opcode: Opcode = ...
    parameter_count: int = ...

    computer: 'IntcodeComputer' = ...

    @abstractmethod
    def execute(self) -> None:
        ...

    def __init__(self, computer: 'IntcodeComputer') -> None:
        self.computer = computer

    def __getattr__(self, item: str) -> int:
        """helper method for ``input_x``"""
        if item.startswith('input_'):
            input_idx = re.match(r'input_(\d*)$', item).group(1)
            if input_idx:
                input_idx = int(input_idx)
                if input_idx > self.parameter_count:
                    raise ParameterError('Invalid input index: %2', input_idx)
                return self.computer.get_parameter(input_idx)
        raise ParameterError('Invalid attribute: %s', item)

    def __setattr__(self, key, value) -> None:
        if key == 'result':
            self.computer.set_parameter(self.parameter_count, value)
        else:
            super().__setattr__(key, value)


class AddInstruction(Instruction):
    opcode = Opcode.ADD
    parameter_count = 3

    def execute(self):
        self.result = self.input_1 + self.input_2


class MultiplyInstruction(Instruction):
    opcode = Opcode.MULTIPLY
    parameter_count = 3

    def execute(self):
        self.result = self.input_1 * self.input_2


class HaltInstruction(Instruction):
    opcode = Opcode.HALT
    parameter_count = 0

    def execute(self):
        raise Halt()


class SaveInstruction(Instruction):
    opcode = Opcode.SAVE
    parameter_count = 1

    def execute(self):
        self.result = self.computer.get_stdin()


class OutputInstruction(Instruction):
    opcode = Opcode.OUTPUT
    parameter_count = 1

    def execute(self):
        self.computer.put_stdout(self.input_1)


class JumpIfTrueInstruction(Instruction):
    opcode = Opcode.JUMP_IF_TRUE
    parameter_count = 2

    def execute(self):
        if self.input_1 != 0:
            self.computer.jump(self.input_2)


class JumpIfFalseInstruction(Instruction):
    opcode = Opcode.JUMP_IF_FALSE
    parameter_count = 2

    def execute(self):
        if self.input_1 == 0:
            self.computer.jump(self.input_2)


class LessThanInstruction(Instruction):
    opcode = Opcode.LESS_THAN
    parameter_count = 3

    def execute(self):
        if self.input_1 < self.input_2:
            self.result = 1
        else:
            self.result = 0


class EqualsInstruction(Instruction):
    opcode = Opcode.EQUALS
    parameter_count = 3

    def execute(self):
        if self.input_1 == self.input_2:
            self.result = 1
        else:
            self.result = 0


class AdjustRelativeBaseInstruction(Instruction):
    opcode = Opcode.ADJUST_RELATIVE_BASE
    parameter_count = 1

    def execute(self):
        self.computer.rbptr += self.input_1
