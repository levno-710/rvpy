# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.

from extension import Extension
from instruction import Instruction
from instruction_impl import InstructionImpl
from nums import u32, i32, i8, u8
from state import RVState

class RV32I(Extension):
    """
    RISC-V RV32I base integer instruction set extension.
    This extension implements the base integer instructions for the RV32I architecture.
    """

    def get_instruction_implementations(self):
        return [
            # Arithmetic instructions
            Add(),
            AddI(),
            Sub(),
            # Logical instructions
            Xor(),
            XorI(),
            Or(),
            OrI(),
            And(),
            AndI(),
            # Shift instructions
            Sll(),
            Sra(),
            Srl(),
            SllI(),
            SraI(),
            SrlI(),
            # Set to 1 if less than instructions
            Slt(),
            SltI(),
            Sltu(),
            SltuI(),
            # Branch instructions
            Beq(),
            Bne(),
            Blt(),
            Bge(),
            Bltu(),
            Bgeu(),
            # Jump instructions
            Jal(),
            JalR(),
            # Load Immediate instructions
            Lui(),
            Auipc(),
            # Load Instructions
            Lb(),
            Lbu(),
            Lh(),
            Lhu(),
            Lw(),
            # Store Instructions
            Sb(),
            Sh(),
            Sw(),
            # Miscellaneous instructions
            Fence(),
            Ebreak(),
        ]

class Add(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b000     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the addition
        state.rf[rd] = state.rf[rs1] + state.rf[rs2]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"add x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class AddI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Execute the addition with immediate
        state.rf[rd] = state.rf[rs1] + imm_i

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"addi x{instruction.rd}, x{instruction.rs1}, {instruction.imm_i}"

class Sub(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b000     \
           and instruction.funct7 == 0b0100000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the subtraction
        state.rf[rd] = state.rf[rs1] - state.rf[rs2]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sub x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class Xor(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b100     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the XOR operation
        state.rf[rd] = state.rf[rs1] ^ state.rf[rs2]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"xor x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class XorI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b100
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Execute the XOR operation with immediate
        state.rf[rd] = state.rf[rs1] ^ imm_i

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"xori x{instruction.rd}, x{instruction.rs1}, {instruction.imm_i}"

class Or(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b110     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the OR operation
        state.rf[rd] = state.rf[rs1] | state.rf[rs2]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"or x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class OrI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b110
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Execute the OR operation with immediate
        state.rf[rd] = state.rf[rs1] | imm_i

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"ori x{instruction.rd}, x{instruction.rs1}, {instruction.imm_i}"

class And(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b111     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the AND operation
        state.rf[rd] = state.rf[rs1] & state.rf[rs2]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"and x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class AndI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b111
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Execute the AND operation with immediate
        state.rf[rd] = state.rf[rs1] & imm_i

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"andi x{instruction.rd}, x{instruction.rs1}, {instruction.imm_i}"

class Sll(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b001     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the shift left logical operation
        state.rf[rd] = state.rf[rs1] << (state.rf[rs2] & 0x1F)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sll x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class Sra(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b101     \
           and instruction.funct7 == 0b0100000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the shift right arithmetic operation
        state.rf[rd] = state.rf[rs1] >> (state.rf[rs2] & 0x1F)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sra x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class Srl(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b101     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the shift right logical operation
        state.rf[rd] = u32(state.rf[rs1]) >> (state.rf[rs2] & 0x1F)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"srl x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"

class SllI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm = instruction.rs2 # This is actually the immediate value for SLLI

        # Execute the shift left logical operation with immediate
        state.rf[rd] = state.rf[rs1] << (imm & 0x1F)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"slli x{instruction.rd}, x{instruction.rs1}, {instruction.rs2 & 0x1F}"

class SraI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b101 \
           and instruction.funct7 == 0b0100000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm = instruction.rs2 # This is actually the immediate value for SRAI

        # Execute the shift right arithmetic operation with immediate
        state.rf[rd] = state.rf[rs1] >> (imm & 0x1F)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"srai x{instruction.rd}, x{instruction.rs1}, {instruction.rs2 & 0x1F}"

class SrlI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b101 \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm = instruction.rs2 # This is actually the immediate value for SRLI

        # Execute the shift right logical operation with immediate
        state.rf[rd] = u32(state.rf[rs1]) >> (imm & 0x1F)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"srl x{instruction.rd}, x{instruction.rs1}, {instruction.rs2 & 0x1F}"
    
class Slt(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b010     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the set less than operation
        state.rf[rd] = int(state.rf[rs1] < state.rf[rs2])

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"slt x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class SltI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b010
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Execute the set less than operation with immediate
        state.rf[rd] = int(state.rf[rs1] < imm_i)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"slti x{instruction.rd}, x{instruction.rs1}, {instruction.imm_i}"
    
class Sltu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110011 \
           and instruction.funct3 == 0b011     \
           and instruction.funct7 == 0b0000000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source and destination registers from the instruction
        rd = instruction.rd
        rs1 = instruction.rs1
        rs2 = instruction.rs2

        # Execute the set less than unsigned operation
        state.rf[rd] = int(u32(state.rf[rs1]) < u32(state.rf[rs2]))

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sltu x{instruction.rd}, x{instruction.rs1}, x{instruction.rs2}"
    
class SltuI(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010011 \
           and instruction.funct3 == 0b011
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Execute the set less than unsigned operation with immediate
        state.rf[rd] = int(u32(state.rf[rs1]) < u32(imm_i))

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sltiu x{instruction.rd}, x{instruction.rs1}, {instruction.imm_i}"
    
class Beq(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1100011 \
           and instruction.funct3 == 0b000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source registers and immediate value
        rs1 = instruction.rs1
        rs2 = instruction.rs2
        imm_b = instruction.imm_b

        # Check if the registers are equal
        if state.rf[rs1] == state.rf[rs2]:
            # If equal, update the program counter to the target address
            state.pc += imm_b
        else:
            # If not equal, just increment the program counter
            state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"beq x{instruction.rs1}, x{instruction.rs2}, {instruction.imm_b}"
    
class Bne(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1100011 \
           and instruction.funct3 == 0b001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source registers and immediate value
        rs1 = instruction.rs1
        rs2 = instruction.rs2
        imm_b = instruction.imm_b

        # Check if the registers are not equal
        if state.rf[rs1] != state.rf[rs2]:
            # If not equal, update the program counter to the target address
            state.pc += imm_b
        else:
            # If equal, just increment the program counter
            state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"bne x{instruction.rs1}, x{instruction.rs2}, {instruction.imm_b}"
    
class Blt(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1100011 \
           and instruction.funct3 == 0b100
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source registers and immediate value
        rs1 = instruction.rs1
        rs2 = instruction.rs2
        imm_b = instruction.imm_b

        # Check if rs1 is less than rs2
        if state.rf[rs1] < state.rf[rs2]:
            # If true, update the program counter to the target address
            state.pc += imm_b
        else:
            # If false, just increment the program counter
            state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"blt x{instruction.rs1}, x{instruction.rs2}, {instruction.imm_b}"
    
class Bge(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1100011 \
           and instruction.funct3 == 0b101
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source registers and immediate value
        rs1 = instruction.rs1
        rs2 = instruction.rs2
        imm_b = instruction.imm_b

        # Check if rs1 is greater than or equal to rs2
        if state.rf[rs1] >= state.rf[rs2]:
            # If true, update the program counter to the target address
            state.pc += imm_b
        else:
            # If false, just increment the program counter
            state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"bge x{instruction.rs1}, x{instruction.rs2}, {instruction.imm_b}"
    
class Bltu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1100011 \
           and instruction.funct3 == 0b110
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source registers and immediate value
        rs1 = instruction.rs1
        rs2 = instruction.rs2
        imm_b = instruction.imm_b

        # Check if rs1 is less than rs2 (unsigned comparison)
        if u32(state.rf[rs1]) < u32(state.rf[rs2]):
            # If true, update the program counter to the target address
            state.pc += imm_b
        else:
            # If false, just increment the program counter
            state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"bltu x{instruction.rs1}, x{instruction.rs2}, {instruction.imm_b}"
    
class Bgeu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1100011 \
           and instruction.funct3 == 0b111
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source registers and immediate value
        rs1 = instruction.rs1
        rs2 = instruction.rs2
        imm_b = instruction.imm_b

        # Check if rs1 is greater than or equal to rs2 (unsigned comparison)
        if u32(state.rf[rs1]) >= u32(state.rf[rs2]):
            # If true, update the program counter to the target address
            state.pc += imm_b
        else:
            # If false, just increment the program counter
            state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"bgeu x{instruction.rs1}, x{instruction.rs2}, {instruction.imm_b}"
    
class Jal(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1101111
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and immediate value
        rd = instruction.rd
        imm_j = instruction.imm_j

        # Save the return address in the destination register
        state.rf[rd] = state.pc + 4

        # Update the program counter to the target address
        state.pc = u32(i32(state.pc) + imm_j)

    def disassemble(self, instruction: Instruction):
        return f"jal x{instruction.rd}, {instruction.imm_j}"
    
class JalR(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1100111 \
           and instruction.funct3 == 0b000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and source register
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Save the return address in the destination register
        state.rf[rd] = state.pc + 4

        # Update the program counter to the address in rs1
        state.pc = u32(i32(state.rf[rs1]) + imm_i) & ~u32(1)  # Ensure the address is aligned

    def disassemble(self, instruction: Instruction):
        return f"jalr x{instruction.rd}, x{instruction.rs1}, {instruction.imm_i}"
    
class Lui(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0110111
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and immediate value
        rd = instruction.rd
        imm_u = instruction.imm_u << 12  # Shift the immediate value to the upper 20 bits

        # Load the upper immediate into the destination register
        state.rf[rd] = u32(imm_u)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"lui x{instruction.rd}, {instruction.imm_u}"
    
class Auipc(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0010111
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and immediate value
        rd = instruction.rd
        imm_u = instruction.imm_u << 12  # Shift the immediate value to the upper 20 bits

        # Add the upper immediate to the current program counter
        state.rf[rd] = u32(state.pc + imm_u)

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"auipc x{instruction.rd}, {instruction.imm_u}"
    
class Lb(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0000011 \
           and instruction.funct3 == 0b000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and source register
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Load the byte from memory and sign-extend it
        state.rf[rd] = i8(state.mem[state.rf[rs1] + imm_i])

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"lb x{instruction.rd}, {instruction.imm_i}(x{instruction.rs1})"
    
class Lbu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0000011 \
           and instruction.funct3 == 0b100
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and source register
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Load the byte from memory and zero-extend it
        state.rf[rd] = u8(state.mem[state.rf[rs1] + imm_i])

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"lbu x{instruction.rd}, {instruction.imm_i}(x{instruction.rs1})"
    
class Lh(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0000011 \
           and instruction.funct3 == 0b001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and source register
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Load the halfword from memory and sign-extend it
        state.rf[rd] = (i8(state.mem[state.rf[rs1] + imm_i + 1]) << 8) + state.mem[state.rf[rs1] + imm_i]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"lh x{instruction.rd}, {instruction.imm_i}(x{instruction.rs1})"
    
class Lhu(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0000011 \
           and instruction.funct3 == 0b101
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and source register
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Load the halfword from memory and zero-extend it
        state.rf[rd] = (u8(state.mem[state.rf[rs1] + imm_i + 1]) << 8) + state.mem[state.rf[rs1] + imm_i]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"lhu x{instruction.rd}, {instruction.imm_i}(x{instruction.rs1})"
    
class Lw(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0000011 \
           and instruction.funct3 == 0b010
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the destination register and source register
        rd = instruction.rd
        rs1 = instruction.rs1
        imm_i = instruction.imm_i

        # Load the word from memory
        state.rf[rd] = (i8(state.mem[state.rf[rs1] + imm_i + 3]) << 24) + \
                     (state.mem[state.rf[rs1] + imm_i + 2] << 16) + \
                     (state.mem[state.rf[rs1] + imm_i + 1] << 8) + \
                     state.mem[state.rf[rs1] + imm_i]

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"lw x{instruction.rd}, {instruction.imm_i}(x{instruction.rs1})"
    
class Sb(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0100011 \
           and instruction.funct3 == 0b000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rs2 = instruction.rs2
        rs1 = instruction.rs1
        imm_s = instruction.imm_s

        # Store the byte in memory
        state.mem[state.rf[rs1] + imm_s] = state.rf[rs2] & 0xFF  # Store the least significant byte

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sb x{instruction.rs2}, {instruction.imm_s}(x{instruction.rs1})"
    
class Sh(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0100011 \
           and instruction.funct3 == 0b001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rs2 = instruction.rs2
        rs1 = instruction.rs1
        imm_s = instruction.imm_s

        # Store the halfword in memory (little-endian format)
        state.mem[state.rf[rs1] + imm_s] = (state.rf[rs2] & 0xFF)
        state.mem[state.rf[rs1] + imm_s + 1] = (state.rf[rs2] >> 8) & 0xFF

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sh x{instruction.rs2}, {instruction.imm_s}(x{instruction.rs1})"
    
class Sw(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0100011 \
           and instruction.funct3 == 0b010
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # Extract the source register and immediate value
        rs2 = instruction.rs2
        rs1 = instruction.rs1
        imm_s = instruction.imm_s

        # Store the word in memory (little-endian format)
        state.mem[state.rf[rs1] + imm_s] = (state.rf[rs2] & 0xFF)
        state.mem[state.rf[rs1] + imm_s + 1] = (state.rf[rs2] >> 8) & 0xFF
        state.mem[state.rf[rs1] + imm_s + 2] = (state.rf[rs2] >> 16) & 0xFF
        state.mem[state.rf[rs1] + imm_s + 3] = (state.rf[rs2] >> 24) & 0xFF

        # Increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return f"sw x{instruction.rs2}, {instruction.imm_s}(x{instruction.rs1})"
    
class Fence(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b0001111 \
           and instruction.funct3 == 0b000
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # FENCE is a no-op in this implementation
        # It is used for memory ordering and does not affect the state in a linear execution model
        # Simply increment the program counter
        state.pc += 4

    def disassemble(self, instruction: Instruction):
        return "fence"
    
class Ebreak(InstructionImpl):
    def match(self, instruction: Instruction) -> bool:
        return instruction.opcode == 0b1110011 \
           and instruction.funct3 == 0b000     \
           and instruction.funct12 == 0b000000000001
    
    def execute(self, state: RVState, instruction: Instruction) -> None:
        # EBREAK is used to trigger a breakpoint exception
        # In this implementation, we simply set the halt flag to True
        state.halt = True

    def disassemble(self, instruction: Instruction):
        return "ebreak"