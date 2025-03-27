from typing import Dict, Optional, Any


class Edge:
    """Class representing a graph edge"""

    def __init__(
        self,
        source: Any,
        target: Any,
        weight: float = 1.0,
        directed: bool = False,
        data: Optional[Dict] = None,
    ):
        """
        Initialize an edge.

        :param source: Source node
        :param target: Target node
        :param weight: Edge weight
        :param directed: Whether edge is directed
        :param data: Additional edge data
        """
        self.source = source
        self.target = target
        self.weight = weight
        self.directed = directed
        self.data = data or {}

    def __repr__(self):
        direction = "→" if self.directed else "↔"
        return f"Edge({self.source} {direction} {self.target}, weight={self.weight})"

    def reverse(self):
        """Return reversed edge (for undirected graphs)"""
        return Edge(self.target, self.source, self.weight, self.directed, self.data)
