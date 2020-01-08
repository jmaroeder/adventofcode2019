import logging
from collections import defaultdict
from contextlib import suppress
from queue import Empty, Queue
from typing import Iterable, List, MutableMapping, Optional, Type, Union

from .exceptions import Halt, ParameterError, WaitingForInput, InvalidState
from .instruction import AddInstruction, AdjustRelativeBaseInstruction, EqualsInstruction, \
    HaltInstruction, Instruction, JumpIfFalseInstruction, JumpIfTrueInstruction, \
    LessThanInstruction, MultiplyInstruction, OutputInstruction, SaveInstruction
from .opcode import Opcode
from .parameter_mode import ParameterMode

LOG = logging.getLogger(__name__)


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
        self.memory: MutableMapping[int, int] = defaultdict(int, enumerate(int(val) for val in initial))
        self.iptr = 0
        self.rbptr = 0
        self._stdin = Queue()
        for item in stdin or []:
            self.put_stdin(item)
        self._stdout = Queue()
        self.jumped: Optional[bool] = None
        self.instructions: MutableMapping[Opcode, Instruction] = {}
        self._alive = False
        self._started = False
        for instruction in instruction_classes or self.default_instruction_classes:
            self.register_instr(instruction)

    @property
    def is_terminated(self) -> bool:
        return self._started and not self._alive

    def get_stdin(self) -> int:
        return self._stdin.get()

    def get_stdout(self) -> int:
        return self._stdout.get()

    def get_stdout_nowait(self) -> int:
        return self._stdout.get_nowait()

    def put_stdout(self, value: int) -> None:
        self._stdout.put(value)

    def put_stdin(self, value: int) -> None:
        self._stdin.put(value)

    @property
    def stdout(self) -> Iterable[int]:
        with suppress(Empty):
            while True:
                yield self._stdout.get_nowait()

    def register_instr(self, instr_cls: Type[Instruction]) -> None:
        self.instructions[instr_cls.opcode] = instr_cls(self)

    def kill(self) -> None:
        self._alive = False

    def run(self) -> None:
        with suppress(Halt):
            while not self.is_terminated:
                self.tick()

    def tick(self) -> None:
        if not self._started:
            self._started = True
            self._alive = True
        if not self._alive:
            raise InvalidState("Computer has already halted!")

        # LOG.debug('iptr=%s, rbptr=%s, MEM=%s', self.iptr, self.rbptr, str(self))
        opcode = Opcode(self.memory[self.iptr] % 100)
        # LOG.debug('Executing %s', opcode.name)
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
        elif parameter_mode == ParameterMode.RELATIVE:
            return self.memory[self.memory[self.iptr + idx] + self.rbptr]
        else:
            raise ParameterError("Invalid parameter mode: %s", parameter_mode)

    def get_parameter_mode(self, idx: int) -> ParameterMode:
        digit = (self.memory[self.iptr] // 10 ** (idx + 1)) % 10
        return ParameterMode(digit)

    def set_parameter(self, idx: int, value: int) -> None:
        parameter_mode = self.get_parameter_mode(idx)
        if parameter_mode == ParameterMode.POSITION:
            self.memory[self.memory[self.iptr + idx]] = value
        elif parameter_mode == ParameterMode.RELATIVE:
            self.memory[self.memory[self.iptr + idx] + self.rbptr] = value
        else:
            raise ParameterError("Invalid parameter mode: %s", parameter_mode)

    def __str__(self) -> str:
        ret = []
        last_address = 0
        for address, value in self.memory.items():
            item = ''
            if address > last_address + 1:
                item += f'...{hex(address)}::'
            item += str(value)
            ret.append(item)
            last_address = address
        return ','.join(ret)


class IntcodeComputerV5(IntcodeComputer):
    default_instruction_classes = IntcodeComputer.default_instruction_classes + [
        SaveInstruction,
        OutputInstruction,
        JumpIfTrueInstruction,
        JumpIfFalseInstruction,
        LessThanInstruction,
        EqualsInstruction,
    ]


class IntcodeComputerV9(IntcodeComputerV5):
    default_instruction_classes = IntcodeComputerV5.default_instruction_classes + [
        AdjustRelativeBaseInstruction
    ]


class IntcodeComputerV11(IntcodeComputerV9):
    def get_stdin(self) -> int:
        # overridden to raise an error when waiting for input
        if self._stdin.empty():
            raise WaitingForInput()
        return super().get_stdin()


def run_intcode(input_data: Union[str, Iterable[int]],
                comp_cls: Type[IntcodeComputer] = IntcodeComputer) -> str:
    vm = comp_cls(initial=input_data)
    vm.run()
    return str(vm)
