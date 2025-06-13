# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.
import numpy as np
from nums import u8, u32, i32

class RVState:
    """
    Represents the state of a RISC-V processor.

    Attributes:
        mem (np.ndarray[u8]): Memory of the processor.
        rf (np.ndarray[i32]): Register file containing 32 registers.
        pc (u32): Program counter.
        halt (bool): Flag indicating whether the processor is halted.
    """
    mem:  np.ndarray[u8]  # Memory
    rf:   np.ndarray[i32] # Register file
    pc:   u32             # Program counter
    halt: bool           # Halt flag

    def __init__(self, mem_size: int = 1024 * 1024 * 1024) -> None:
        """
        Initialized the RVState with a given memory size.

        Parameters:
            mem_size (int): Size of the memory in bytes. Defaults to 1 GiB.
        """
        self.mem = np.zeros(mem_size, dtype=u8)
        self.rf = np.zeros(32, dtype=i32)
        self.pc = u32(0)
        self.halt = False
    
    def reset(self) -> None:
        """
        Resets the RVState to its initial state.

        This method clears the memory, resets the register file, sets the program counter to 0,
        and clears the halt flag.
        """
        self.mem.fill(0)
        self.rf.fill(0)
        self.pc = u32(0)
        self.halt = False

    def load_memory(self, address: int, data: bytes) -> None:
        """
        Loads data into memory at a specified address.

        Parameters:
            address (int): The starting address in memory.
            data (np.ndarray[u8]): The data to load into memory.
        """
        if not isinstance(data, bytes):
            raise TypeError(f"Expected bytes, got {type(data)}")
        if address < 0 or address + len(data) > self.mem.size:
            raise IndexError(f"Memory access out of bounds: {address} + {len(data)} > {self.mem.size}")
        self.mem[address:address + len(data)] = np.frombuffer(data, dtype=u8)

    def __getitem__(self, address: int) -> u8:
        """
        Gets the value at a specified memory address.

        Parameters:
            address (int): The address in memory.

        Returns:
            u8: The value at the specified address.
        """
        return self.mem[address]

    def __repr__(self) -> str:
        """
        Returns a string representation of the RVState.

        Returns:
            str: String representation of the RVState.
        """
        # Format the register file as a string
        rf_str = ', '.join(f'x{i}: {self.rf[i]}' for i in range(32))
        return (f'RVState(\n'
                f'  mem_size={self.mem.size},\n'
                f'  rf=[{rf_str}],\n'
                f'  pc={self.pc},\n'
                f'  halt={self.halt}\n'
                f')')