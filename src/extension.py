# Author: Elias Oelschner
#
# This file is part of my project for the bachelor's seminar "Moderne Hardware" at Heinrich-Heine-Universität Düsseldorf.
# It is released under the GNU General Public License v3.0.
from abc import ABC, abstractmethod

class Extension(ABC):
    """
    Abstract base class for RISC-V extensions.
    
    Extensions can add new instructions or modify existing ones.
    """

    @abstractmethod
    def get_instruction_implementations(self) -> list:
        """
        Returns a list of instruction implementations provided by this extension.
        
        Returns:
            list: A list of instruction implementations.
        """
        pass
