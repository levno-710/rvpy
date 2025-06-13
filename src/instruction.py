# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.
import numpy as np
from nums import u32, u8, i32, i8

class Instruction:
    """
    Represents a RISC-V instruction.

    Attributes:
        instruction_word (u32): The raw instruction word.
        opcode (u8): The opcode of the instruction.
        funct3 (u8): The funct3 field of the instruction.
        funct7 (u8): The funct7 field of the instruction.
        rd (u8): Destination register.
        rs1 (u8): Source register 1.
        rs2 (u8): Source register 2.
        imm_i (i32): Immediate value for I-type instructions.
        imm_s (i32): Immediate value for S-type instructions.
        imm_b (i32): Immediate value for B-type instructions.
        imm_u (u32): Immediate value for U-type instructions.
        imm_j (i32): Immediate value for J-type instructions.
    """

    instruction_word: u32

    # Opcode and function fields
    opcode: u8
    funct3: u8
    funct7: u8
    funct12: int

    # Register fields
    rd: u8
    rs1: u8
    rs2: u8

    # Immediate fields
    imm_i: i32
    imm_s: i32
    imm_b: i32
    imm_u: u32
    imm_j: i32

    def __init__(self, instruction_word: u32) -> None:
        """
        Initializes the instruction with a given instruction word.

        Parameters:
            ins (u32): The instruction word.
        """
        self.instruction_word = instruction_word

        # Opcode and function fields
        self.opcode = u8(instruction_word & 0x7F)
        self.funct3 = u8((instruction_word >> 12) & 0x07)
        self.funct7 = u8((instruction_word >> 25) & 0x7F)
        self.funct12 = (instruction_word >> 20) & 0xFFF

        # Register fields
        self.rd = u8((instruction_word >> 7) & 0x1F)
        self.rs1 = u8((instruction_word >> 15) & 0x1F)
        self.rs2 = u8((instruction_word >> 20) & 0x1F)

        # Immediate fields
        imm_i = i32(instruction_word >> 20) & 0xFFF
        if imm_i & 0x800:
            imm_i |= ~0xFFF
        self.imm_i = imm_i

        # S-type immediate (12-bit signed)
        imm_s = i32((instruction_word >> 7) & 0x1F) \
                | (((instruction_word >> 25) & 0x7F) << 5)
        if imm_s & 0x800:
            imm_s |= ~0xFFF
        self.imm_s = imm_s

        # B-type immediate (13-bit signed, branch offset)
        imm_b = i32(((instruction_word >> 8) & 0xF) << 1) \
                | (((instruction_word >> 25) & 0x3F) << 5) \
                | (((instruction_word >> 7) & 0x1) << 11) \
                | (((instruction_word >> 31) & 0x1) << 12)
        if imm_b & 0x1000:
            imm_b |= ~0x1FFF
        self.imm_b = imm_b

        # U-type immediate (20-bit upper)
        self.imm_u = u32(instruction_word & 0xFFFFF000)

        # J-type immediate (21-bit signed, jump offset)
        imm_j = i32(((instruction_word >> 21) & 0x3FF) << 1) \
                | (((instruction_word >> 20) & 0x1) << 11) \
                | (((instruction_word >> 12) & 0xFF) << 12) \
                | (((instruction_word >> 31) & 0x1) << 20)
        if imm_j & 0x100000:
            imm_j |= ~0x1FFFFF
        self.imm_j = imm_j

    def __repr__(self) -> str:
        """
        Returns a string representation of the instruction.

        Returns:
            str: String representation of the instruction.
        """
        return (f"Instruction(opcode={self.opcode:#04x}, funct3={self.funct3:#04x}, funct7={self.funct7:#04x}, "
                f"rd={self.rd:#02x}, rs1={self.rs1:#02x}, rs2={self.rs2:#02x}, "
                f"imm_i={self.imm_i}, imm_s={self.imm_s}, imm_b={self.imm_b}, "
                f"imm_u={self.imm_u:#010x}, imm_j={self.imm_j})")

