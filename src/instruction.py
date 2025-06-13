import numpy as np
from nums import u32, u8, i32

class Instruction:
    """
    Represents a RISC-V instruction. All fields except instruction_word
    are computed on demand.

    Attributes:
        instruction_word (u32): The raw instruction word.
        opcode (u8): The opcode of the instruction.
        funct3 (u8): The funct3 field of the instruction.
        funct7 (u8): The funct7 field of the instruction.
        funct12 (int): The funct12 field of the instruction.
        rd (u8): The destination register.
        rs1 (u8): The first source register.
        rs2 (u8): The second source register.
        imm_i (i32): Immediate value for I-type instructions.
        imm_s (i32): Immediate value for S-type instructions.
        imm_b (i32): Immediate value for B-type instructions.
        imm_u (u32): Immediate value for U-type instructions.
        imm_j (i32): Immediate value for J-type instructions.
    """

    instruction_word: u32

    def __init__(self, instruction_word: u32) -> None:
        self.instruction_word = instruction_word

    @property
    def opcode(self) -> u8:
        return u8(self.instruction_word & 0x7F)

    @property
    def funct3(self) -> u8:
        return u8((self.instruction_word >> 12) & 0x07)

    @property
    def funct7(self) -> u8:
        return u8((self.instruction_word >> 25) & 0x7F)

    @property
    def funct12(self) -> int:
        return (self.instruction_word >> 20) & 0xFFF

    @property
    def rd(self) -> u8:
        return u8((self.instruction_word >> 7) & 0x1F)

    @property
    def rs1(self) -> u8:
        return u8((self.instruction_word >> 15) & 0x1F)

    @property
    def rs2(self) -> u8:
        return u8((self.instruction_word >> 20) & 0x1F)

    @property
    def imm_i(self) -> i32:
        imm = i32(self.instruction_word >> 20) & 0xFFF
        if imm & 0x800:
            imm |= ~0xFFF
        return imm

    @property
    def imm_s(self) -> i32:
        imm = i32((self.instruction_word >> 7) & 0x1F) \
            | (i32((self.instruction_word >> 25) & 0x7F) << 5)
        if imm & 0x800:
            imm |= ~0xFFF
        return imm

    @property
    def imm_b(self) -> i32:
        imm = i32(((self.instruction_word >> 8) & 0xF) << 1) \
            | (i32((self.instruction_word >> 25) & 0x3F) << 5) \
            | (i32((self.instruction_word >> 7) & 0x1) << 11) \
            | (i32((self.instruction_word >> 31) & 0x1) << 12)
        if imm & 0x1000:
            imm |= ~0x1FFF
        return imm

    @property
    def imm_u(self) -> u32:
        return u32(self.instruction_word & 0xFFFFF000)

    @property
    def imm_j(self) -> i32:
        imm = i32(((self.instruction_word >> 21) & 0x3FF) << 1) \
            | (i32((self.instruction_word >> 20) & 0x1) << 11) \
            | (i32((self.instruction_word >> 12) & 0xFF) << 12) \
            | (i32((self.instruction_word >> 31) & 0x1) << 20)
        if imm & 0x100000:
            imm |= ~0x1FFFFF
        return imm

    def __repr__(self) -> str:
        return (
            f"Instruction(opcode={self.opcode:#04x}, funct3={self.funct3:#04x}, "
            f"funct7={self.funct7:#04x}, rd={self.rd:#02x}, rs1={self.rs1:#02x}, "
            f"rs2={self.rs2:#02x}, imm_i={self.imm_i}, imm_s={self.imm_s}, "
            f"imm_b={self.imm_b}, imm_u={self.imm_u:#010x}, imm_j={self.imm_j})"
        )