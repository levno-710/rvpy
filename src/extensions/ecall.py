# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.

from extension import Extension
from instruction import Instruction
from instruction_impl import InstructionImpl
from nums import u32, i32, i8, u8
from state import RVState
import sys
from typing import TextIO

class ECALL(Extension):
    """
    RISC-V ECALL extension for handling system calls.
    This implements pseudo-system calls like exit and print integer.
    It is used for IO in example programs.
    """

    def __init__(self, output_stream: TextIO = sys.stdout):
        """
        Initializes the ECALL extension with an output stream.
        Parameters:
            output_stream (TextIO): The stream to which output will be printed. Defaults to sys.stdout.
        """
        self.output_stream = output_stream

    def get_instruction_implementations(self):
        return [
            Ecall(self.output_stream),
        ]
    
class Ecall(InstructionImpl):
    def __init__(self, output_stream: TextIO):
        self.output_stream = output_stream

    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1110011 \
           and instruction.funct3 == 0b000     \
           and instruction.funct12 == 0b000000000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        """
        Executes the ECALL instruction.
        This instruction is used to make a system call to the operating system.
        """
        # Load the system call number from the a7 register
        syscall_number = state.rf[17]
        # Handle the system call based on the number
        # For now we have:
        # - 10: Exit the program
        # - 1 : Print an integer (in a0)
        if syscall_number == 10:
            state.halt = True
        elif syscall_number == 1:
            # print to the injected stream
            print(state.rf[10], file=self.output_stream)
        else:
            raise NotImplementedError(f"System call {syscall_number} is not implemented.")

        # Increment pc
        state.pc += 4

    def disassemble(self, instruction: Instruction) -> str:
        """
        Disassembles the ECALL instruction.
        """
        return "ecall"