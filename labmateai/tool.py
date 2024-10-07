# tool.py

"""
This module contains the Tool class, which represents a tool used in the lab.

Classes:
    Tool: A class representing a tool used in the lab.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Tool:
    """
    A class to represent a tool used in the lab.
    """

    tool_id: int
    name: str
    category: str
    features: Tuple[str, ...]  # Changed to Tuple for immutability
    cost: str  # Changed from float to str to accommodate 'Free'
    description: str
    url: str
    language: str
    platform: str

    def __hash__(self):
        """
        Return the hash value of the tool based on its name.

        Returns:
            int: The hash value of the tool.
        """
        return hash(self.name.lower())

    def __eq__(self, other):
        """
        Check if two tools are equal based on their names.

        Args:
            other (Tool): The other tool to compare.

        Returns:
            bool: True if the tools are equal, False otherwise.
        """

        if isinstance(other, Tool):
            return self.name.lower() == other.name.lower()
        return False

    def __repr__(self):
        """
        Return a string representation of the tool.

        Returns:
            str: A string representation of the tool.
        """

        return f"Tool(tool_id={self.tool_id}, name='{self.name}')"
