class IntcodeException(Exception):
    """Base exception class"""


class Halt(IntcodeException):
    """Raised when a program is completed"""


class ParameterError(IntcodeException):
    """Raised when an invalid parameter is encountered"""


class WaitingForInput(IntcodeException):
    """Raised when computer needs input"""


class InvalidState(IntcodeException):
    """Invalid state"""
