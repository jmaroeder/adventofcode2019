import re
from abc import ABC, abstractmethod
from contextlib import suppress
from enum import Enum
import logging
from typing import Union, Iterable, MutableSequence, Type, MutableMapping

LOG = logging.getLogger(__name__)


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    HALT = 99


class Halt(Exception):
    pass


class Instruction(ABC):
    opcode = ...
    parameter_count = 3

    computer: 'IntcodeComputer' = ...

    # proxy properties
    @property
    def memory(self) -> MutableSequence[int]:
        return self.computer.memory

    @property
    def iptr(self) -> int:
        return self.computer.iptr

    @abstractmethod
    def execute(self):
        ...

    def __init__(self, computer: 'IntcodeComputer'):
        self.computer = computer

    def __getattr__(self, item: str) -> int:
        """helper method for ``input_x``"""
        if item.startswith('input_'):
            input_idx = re.match(r'input_(\d*)$', item).group(1)
            if input_idx:
                input_idx = int(input_idx)
                if input_idx > self.parameter_count:
                    raise AttributeError('Invalid input index: %2', input_idx)
                return self.memory[self.memory[self.iptr + input_idx]]
        raise AttributeError('Invalid attribute: %s', item)

    def __setattr__(self, key, value):
        if key == 'output':
            self.memory[self.memory[self.iptr + self.parameter_count]] = value
        else:
            super().__setattr__(key, value)


class AddInstruction(Instruction):
    opcode = Opcode.ADD

    def execute(self):
        self.output = self.input_1 + self.input_2


class MultiplyInstruction(Instruction):
    opcode = Opcode.MULTIPLY

    def execute(self):
        self.output = self.input_1 * self.input_2


class HaltInstruction(Instruction):
    opcode = Opcode.HALT

    def execute(self):
        raise Halt()


class IntcodeComputer:
    def __init__(self, initial: Union[str, Iterable[Union[int, str]]],
                 instructions: Iterable[Instruction] = None):
        if hasattr(initial, 'split'):
            initial = initial.split(',')
        self.memory = [
            int(val) for val in initial
        ]
        self.iptr = 0
        self.instructions: MutableMapping[Opcode, Instruction] = {}
        for instruction in instructions or [AddInstruction, MultiplyInstruction, HaltInstruction]:
            self.register_instr(instruction)

    def register_instr(self, instr: Type[Instruction]) -> None:
        self.instructions[instr.opcode] = instr(self)

    def run(self) -> None:
        with suppress(Halt):
            while True:
                self.tick()

    def tick(self) -> None:
        LOG.debug('PC=%s, STATE=%s', self.iptr, str(self))
        opcode = Opcode(self.memory[self.iptr])
        LOG.debug('Executing %s', opcode.name)
        instr = self.instructions[opcode]
        instr.execute()
        self.iptr += 1 + instr.parameter_count

    def __str__(self) -> str:
        return ','.join(str(val) for val in self.memory)


def run_intcode(input_data: Union[str, Iterable[int]]) -> str:
    vm = IntcodeComputer(initial=input_data)
    vm.run()
    return str(vm)
