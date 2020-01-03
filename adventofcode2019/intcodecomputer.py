import logging
import re
from abc import ABC, abstractmethod
from contextlib import suppress
from enum import Enum
from typing import Iterable, List, MutableMapping, MutableSequence, Type, Union, Optional

LOG = logging.getLogger(__name__)


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


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
                return self.computer.get_parameter(input_idx)
        raise AttributeError('Invalid attribute: %s', item)

    def __setattr__(self, key, value):
        if key == 'result':
            self.computer.set_parameter(self.parameter_count, value)
        else:
            super().__setattr__(key, value)


class AddInstruction(Instruction):
    opcode = Opcode.ADD

    def execute(self):
        self.result = self.input_1 + self.input_2


class MultiplyInstruction(Instruction):
    opcode = Opcode.MULTIPLY

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
        self.result = self.computer.stdin.pop(0)


class OutputInstruction(Instruction):
    opcode = Opcode.OUTPUT
    parameter_count = 1

    def execute(self):
        self.computer.stdout.append(self.input_1)


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


class IntcodeComputer:
    default_instruction_classes: List[Type[Instruction]] = [
        AddInstruction,
        MultiplyInstruction,
        HaltInstruction,
    ]

    def __init__(self, initial: Union[str, Iterable[Union[int, str]]],
                 instruction_classes: Iterable[Type[Instruction]] = None,
                 stdin: Iterable[int] = None):
        if hasattr(initial, 'split'):
            initial = initial.split(',')
        self.memory = [
            int(val) for val in initial
        ]
        self.iptr = 0
        self.stdin = stdin or []
        self.stdout = []
        self.jumped: Optional[bool] = None
        self.instructions: MutableMapping[Opcode, Instruction] = {}
        for instruction in instruction_classes or self.default_instruction_classes:
            self.register_instr(instruction)

    def register_instr(self, instr_cls: Type[Instruction]) -> None:
        self.instructions[instr_cls.opcode] = instr_cls(self)

    def run(self) -> None:
        with suppress(Halt):
            while True:
                self.tick()

    def tick(self) -> None:
        LOG.debug('PC=%s, MEM=%s', self.iptr, str(self))
        opcode = Opcode(self.memory[self.iptr] % 100)
        LOG.debug('Executing %s', opcode.name)
        instr = self.instructions[opcode]
        self.jumped = False
        instr.execute()
        if not self.jumped:
            self.iptr += 1 + instr.parameter_count

    def jump(self, newptr: int) -> None:
        self.jumped = True
        self.iptr = newptr

    def get_parameter(self, idx: int) -> int:
        parameter_mode = self.get_parameter_mode(idx)
        if parameter_mode == ParameterMode.POSITION:
            return self.memory[self.memory[self.iptr + idx]]
        elif parameter_mode == ParameterMode.IMMEDIATE:
            return self.memory[self.iptr + idx]

    def get_parameter_mode(self, idx: int) -> ParameterMode:
        digit = (self.memory[self.iptr] // 10 ** (idx + 1)) % 10
        return ParameterMode(digit)

    def set_parameter(self, idx: int, value: int) -> None:
        self.memory[self.memory[self.iptr + idx]] = value

    def __str__(self) -> str:
        return ','.join(str(val) for val in self.memory)


class IntcodeComputerV5(IntcodeComputer):
    default_instruction_classes = IntcodeComputer.default_instruction_classes + [
        SaveInstruction,
        OutputInstruction,
        JumpIfTrueInstruction,
        JumpIfFalseInstruction,
        LessThanInstruction,
        EqualsInstruction,
    ]


def run_intcode(input_data: Union[str, Iterable[int]],
                comp_cls: Type[IntcodeComputer] = IntcodeComputer) -> str:
    vm = comp_cls(initial=input_data)
    vm.run()
    return str(vm)
