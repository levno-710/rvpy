# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.

import numpy as np
from extension import Extension
from instruction import Instruction
from instruction_impl import InstructionImpl
from nums import u32, i32, i8, u8, i64, u64
from state import RVState

class M(Extension):
    """
    RISC-V M extension for integer multiplication and division.
    This extension implements the M extension instructions for integer multiplication.
    """

    def get_instruction_implementations(self):
        return [
            # Multiplication instructions
            Mul(),
            Mulh(),
            Mulhu(),
            Mulhsu(),
            # Division instructions
            Div(),
            Divu(),
            Rem(),
            Remu(),
        ]
    
def muls(a: i32, b: i32) -> i64:
    """
    Perform signed multiplication of two 32-bit integers.
    Parameters:
        a (i32): The first integer.
        b (i32): The second integer.
    """
    return np.multiply(a, b, dtype=i64)

def mulu(a: u32, b: u32) -> u64:
    """
    Perform unsigned multiplication of two 32-bit integers.
    Parameters:
        a (u32): The first integer.
        b (u32): The second integer.
    """
    return np.multiply(a, b, dtype=u64)

def div(a: i32 | u32, b: i32 | u32) -> int:
    """
    Perform division of two integers.
    Parameters:
        a (i32 | u32): The dividend.
        b (i32 | u32): The divisor.
    Returns:
        i32 | u32: The result of the division.
    """
    return np.fix(a / b).astype(int)

def rem(a: i32 | u32, b: i32 | u32) -> int:
    """
    Perform remainder operation of two integers.
    Parameters:
        a (i32 | u32): The dividend.
        b (i32 | u32): The divisor.
    Returns:
        i32 | u32: The result of the remainder operation.
    """
    return a - b * div(a, b)


class Mul(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b000     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the multiplication
        state.rf[rd] = muls(state.rf[rs1], state.rf[rs2])

    def disassemble(self, instruction: Instruction):
        return f"mul x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class Mulh(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b001     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the multiplication and take the high part
        state.rf[rd] = muls(state.rf[rs1], state.rf[rs2]) >> 32

    def disassemble(self, instruction: Instruction):
        return f"mulh x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class Mulhu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b011     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the multiplication and take the high part (unsigned)
        state.rf[rd] = mulu(state.rf[rs1], state.rf[rs2]) >> u32(32)

    def disassemble(self, instruction: Instruction):
        return f"mulhu x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class Mulhsu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b010     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the multiplication with signed and unsigned operands
        state.rf[rd] = muls(state.rf[rs1], u32(state.rf[rs2])) >> 32

    def disassemble(self, instruction: Instruction):
        return f"mulhsu x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class Div(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b100     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the division
        if state.rf[rs2] == 0:
            state.rf[rd] = -1  # Handle division by zero by setting the result to -1
        else:
            state.rf[rd] = div(state.rf[rs1], state.rf[rs2])  # Store the result as a signed integer

    def disassemble(self, instruction: Instruction):
        return f"div x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class Divu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b101     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the unsigned division
        if state.rf[rs2] == 0:
            state.rf[rd] = -1  # Handle division by zero by setting the result to -1
        else:
            state.rf[rd] = div(u32(state.rf[rs1]), u32(state.rf[rs2]))  # Store the result as an unsigned integer

    def disassemble(self, instruction: Instruction):
        return f"divu x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class Rem(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b110     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the remainder operation
        if state.rf[rs2] == 0:
            state.rf[rd] = state.rf[rs1]  # Handle division by zero by returning the dividend
        else:
            state.rf[rd] = rem(state.rf[rs1], state.rf[rs2])  # Store the result as a signed integer

    def disassemble(self, instruction: Instruction):
        return f"rem x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class Remu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b111     \
           and instruction.funct7 == 0b0000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Perform the unsigned remainder operation
        if state.rf[rs2] == 0:
            state.rf[rd] = state.rf[rs1]  # Handle division by zero by returning the dividend
        else:
            state.rf[rd] = rem(u32(state.rf[rs1]), u32(state.rf[rs2]))

    def disassemble(self, instruction: Instruction):
        return f"remu x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"


    
