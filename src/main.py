# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.
import argparse

from extensions.ecall import ECALL
from vm import VM
from extensions.rv32i import RV32I
import struct

def load_hex(file_path: str) -> bytes:
    """
    Loads a RISC-V hex program file and returns its machine code as bytes.
    Each line in the file is expected to be a 32-bit instruction in hex.
    """
    instructions = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            try:
                # Convert the hex string (e.g. "0x00900313") to an integer.
                instr = int(line, 16)
                # Pack the 32-bit instruction in little-endian format.
                instructions.append(struct.pack('<I', instr))
            except ValueError:
                continue
    return b''.join(instructions)

def main():
    parser = argparse.ArgumentParser(description="rvpy: A RISC-V virtual machine for executing RISC-V programs.")
    # Program argument	
    parser.add_argument("program", type=str, help="path to the RISC-V program to execute")

    # Hex flag
    parser.add_argument("-x", "--hex", action="store_true",
                        help="interpret the program as a hex file instead of a binary file")
    # Memory size argument
    parser.add_argument("-m", "--mem-size", type=int, default=1024 * 1024 * 1024,
                        help="size of the memory in bytes (default: 1 GiB)")
    # Disassemble flag
    parser.add_argument("-d", "--disassemble", action="store_true",
                        help="print executed instructions in disassembled form")

    args = parser.parse_args()

    # Try to load the program file
    try:
        if args.hex:
            program_data = load_hex(args.program)
        else:
            with open(args.program, 'rb') as f:
                program_data = f.read()
    except FileNotFoundError:
        print(f"Error: Program file '{args.program}' not found.")
        return
    except Exception as e:
        print(f"Error loading program file: {e}")
        return
    
    # Initialize the VM with the specified memory size and load all extensions
    vm = VM(mem_size=args.mem_size, extensions=[
        RV32I(),
        ECALL(),
    ])

    # Load the program into memory at address 0 and set the program counter to 0
    vm.state.load_memory(0, program_data)
    vm.state.pc = 0

    # Execute the program until halted
    while not vm.state.halt:
        if args.disassemble:
            print(vm.dump_next_instruction())
        vm.step()

if __name__ == "__main__":
    main()