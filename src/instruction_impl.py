# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.
import numpy as np
from abc import ABC, abstractmethod
from nums import u32
from state import RVState
from instruction import Instruction

class InstructionImpl(ABC):
    """
    Abstract base class for RISC-V instruction implementations.
    
    Attributes:
        opcode (int): The opcode of the instruction.
        funct3 (int): The funct3 field of the instruction.
        funct7 (int): The funct7 field of the instruction.
    """

    @abstractmethod
    def match(self, instruction: Instruction) -> bool:
        """
        Checks if the given instruction matches this instruction type.
        Parameters:
            instruction (Instruction): The instruction to check.
        Returns:
            bool: True if the instruction matches, False otherwise.
        """
        pass

    @abstractmethod
    def execute(self, state: RVState, instruction: Instruction) -> None:
        """
        Executes the instruction on the given state.
        
        Parameters:
            state (RVState): The current state of the RISC-V processor.
            instruction (Instruction): The instruction to execute.
        """
        pass

    @abstractmethod
    def disassemble(self, instruction: Instruction) -> str:
        """
        Disassembles the instruction into a human-readable format.
        
        Parameters:
            instruction (Instruction): The instruction to disassemble.
        Returns:
            str: The disassembled instruction as a string.
        """
        pass