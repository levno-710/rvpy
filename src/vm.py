# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.
import numpy as np
from state import RVState
from instruction_impl import InstructionImpl
from instruction import Instruction
from nums import u32
from extension import Extension

class VM:
    """
    Virtual Machine (VM) for executing RISC-V instructions.
    """
    state: RVState
    instruction_implementations: list[InstructionImpl]

    def __init__(self, mem_size: int = 1024 * 1024 * 1024, extensions: list[Extension] = []) -> None:
        """
        Initializes the VM with a given memory size.

        Parameters:
            mem_size (int): Size of the memory in bytes. Defaults to 1 GiB.
            extensions (list[Extension]): List of extensions to load into the VM.
        """
        # Validate memory size
        if not isinstance(mem_size, int) or mem_size <= 0:
            raise ValueError(f"Memory size must be a positive integer, got {mem_size}")
        
        # Initialize the state and instruction implementations
        self.state = RVState(mem_size)

        # Initialize the instruction implementations list and load extensions
        self.instruction_implementations = []
        for ext in extensions:
            if not isinstance(ext, Extension):
                raise TypeError(f"Expected Extension, got {type(ext)}")
            self.load_extension(ext)

    def load_extension(self, extension: Extension) -> None:
        """
        Loads an extension into the VM, adding its instruction implementations.
        Parameters:
            extension (Extension): The extension to load.
        """
        ext_impls = extension.get_instruction_implementations()
        if not isinstance(ext_impls, list):
            raise TypeError(f"Expected list of instruction implementations, got {type(ext_impls)}")
        self.instruction_implementations.extend(ext_impls)

    def load_memory(self, address: int, data: np.ndarray[u32]) -> None:
        """
        Loads data into memory at a specified address.

        Parameters:
            address (int): The starting address in memory.
            data (np.ndarray[u32]): The data to load into memory.
        """
        if not isinstance(data, np.ndarray) or data.dtype != u32:
            raise TypeError(f"Data must be a numpy array of type u32, got {type(data)}")
        if address < 0 or address + len(data) * 4 > len(self.state.mem):
            raise ValueError(f"Memory access out of bounds: {address} + {len(data) * 4} exceeds memory size")
        
        self.state.mem[address:address + len(data) * 4] = data.tobytes()

    def reset(self) -> None:
        """
        Resets the VM to its initial state.
        """
        self.state.reset()

    def match_impl(self, instruction: Instruction) -> InstructionImpl | None:
        """
        Finds the instruction implementation that matches the given instruction.
        Parameters:
            instruction (Instruction): The instruction to match.
        Returns:
            InstructionImpl: The matching instruction implementation.
        Raises:
            ValueError: If multiple implementations match the instruction.
        """
        # Try to find a matching instruction implementation
        matches = [impl for impl in self.instruction_implementations if impl.match(instruction)]
        if not matches:
            return None  # No matching implementation found
        if len(matches) > 1:
            raise ValueError(f"Multiple instruction implementations match {instruction}")
        return matches[0]

    def dump_next_instruction(self) -> str:
        """
        Dumps the next instruction to be executed in disassembled form.
        
        Returns:
            str: The disassembled instruction as a string.
        """
        pc = self.state.pc
        instruction_word = np.frombuffer(self.state.mem[pc:pc + 4], dtype=u32)[0]
        instruction = Instruction(instruction_word)
        impl = self.match_impl(instruction)
        if impl is None:
            return f"Unknown instruction at PC={pc:#010x}: {instruction_word:#010x}"
        return impl.disassemble(instruction)

    def step(self) -> None:
        """
        Executes a single instruction in the VM.
        """
        if self.state.halt:
            return # If the VM is halted, do nothing
        
        # Fetch the instruction from memory as little-endian
        pc = self.state.pc
        instruction_word = np.frombuffer(self.state.mem[pc:pc + 4], dtype=u32)[0]
        instruction = Instruction(instruction_word)
        
        # Execute the instruction
        impl = self.match_impl(instruction)
        if impl is None:
            raise ValueError(f"No matching instruction implementation for {instruction}")
        impl.execute(self.state, instruction)

        # Ensure x0 register is always zero
        self.state.rf[0] = 0

    def run(self, n_steps: int = -1) -> None:
        """
        Runs the VM for a specified number of steps.

        Parameters:
            n_steps (int): Number of steps to execute. If -1, runs indefinitely until halted.
        """
        steps = 0
        while not self.state.halt and (n_steps == -1 or steps < n_steps):
            self.step()
            steps += 1
