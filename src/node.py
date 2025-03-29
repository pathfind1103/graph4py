from typing import Dict, Any, Optional


class Node:
    """Class representing a graph node"""

    def __init__(self, id: Any, data: Optional[Dict] = None):
        """
        Initialize a node.

        :param id: Unique identifier for the node (int or str)
        :param data: Additional node data as dictionary
        """
        self.id = id
        self.data = data or {}
        self.position = None  # Will store (x, y) coordinates for visualization

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"Node(id={self.id}, data={self.data})"

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return self.id == other

    def __hash__(self):
        return hash(self.id)

    def update_position(self, x: float, y: float):
        """Update node position for visualization"""
        # х
        self.position = (x, y)
