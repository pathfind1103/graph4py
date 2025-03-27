"""
Graph module for creating and manipulating graphs.
"""

from typing import Dict, List, Tuple, Any


class Graph:
    """Graph representation supporting directed, undirected, and weighted edges."""

    def __init__(self, directed: bool = False):
        """
        Initialize a graph.

        :param directed: If True, creates a directed graph; otherwise, undirected.
        """
        self.directed = directed
        self.adj_list: Dict[int, List[Tuple[int, float]]] = {}

    def add_node(self, node: int) -> None:
        """Add a node to the graph."""
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, node1: int, node2: int, weight: float = 1.0) -> None:
        """
        Add an edge between node1 and node2 with an optional weight.

        :param node1: First node.
        :param node2: Second node.
        :param weight: Edge weight (default is 1.0).
        """
        self.add_node(node1)
        self.add_node(node2)
        self.adj_list[node1].append((node2, weight))
        if not self.directed:
            self.adj_list[node2].append((node1, weight))

    def remove_edge(self, node1: int, node2: int) -> None:
        """Remove the edge between node1 and node2 if it exists."""
        self.adj_list[node1] = [(n, w) for n, w in self.adj_list[node1] if n != node2]
        if not self.directed:
            self.adj_list[node2] = [(n, w) for n, w in self.adj_list[node2] if n != node1]

    def remove_node(self, node: int) -> None:
        """Remove a node and all associated edges."""
        if node in self.adj_list:
            del self.adj_list[node]
            for key in self.adj_list:
                self.adj_list[key] = [(n, w) for n, w in self.adj_list[key] if n != node]

    def get_neighbors(self, node: int) -> List[Tuple[int, float]]:
        """Return a list of neighbors for a given node."""
        return self.adj_list.get(node, [])

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to a dictionary format."""
        return {"directed": self.directed, "adj_list": self.adj_list}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Graph":
        """Create a Graph instance from a dictionary."""
        graph = cls(directed=data["directed"])
        graph.adj_list = {int(k): v for k, v in data["adj_list"].items()}
        return graph

    def __repr__(self) -> str:
        """String representation of the graph."""
        return f"Graph(directed={self.directed}, nodes={list(self.adj_list.keys())})"

    def display(self) -> None:
        """Print adjacency list representation."""
        for node, neighbors in self.adj_list.items():
            print(f"{node} -> {neighbors}")
