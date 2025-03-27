from typing import Dict, List, Optional, Union
from node import Node
from edge import Edge


class Graph:
    """Graph representation using Node and Edge classes"""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.nodes: Dict[Union[int, str], Node] = {}
        self.edges: Dict[Node, List[Edge]] = {}

    @property
    def node_list(self) -> List[Node]:
        """Get list of all nodes"""
        return list(self.nodes.values())

    def add_node(self, node_id: Union[int, str], data: Optional[Dict] = None) -> Node:
        """Add or get existing node"""
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, data)
            self.edges[self.nodes[node_id]] = []
        return self.nodes[node_id]

    def add_edge(
        self,
        source_id: Union[int, str],
        target_id: Union[int, str],
        weight: float = 1.0,
        data: Optional[Dict] = None,
    ) -> None:
        """Add edge between nodes"""
        source = self.add_node(source_id)
        target = self.add_node(target_id)

        edge = Edge(source, target, weight, self.directed, data)
        self.edges[source].append(edge)

        if not self.directed:
            reverse_edge = edge.reverse()
            self.edges[target].append(reverse_edge)

    def remove_node(self, node_id: Union[int, str]) -> None:
        """Remove node and all connected edges"""
        if node_id not in self.nodes:
            return

        node = self.nodes[node_id]

        # Remove all edges connected to this node
        del self.edges[node]
        for edges_list in self.edges.values():
            edges_list[:] = [e for e in edges_list if e.target.id != node_id]

        # Remove the node itself
        del self.nodes[node_id]

    def remove_edge(self, source_id: Union[int, str], target_id: Union[int, str]) -> None:
        """Remove edge between two nodes"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return

        source = self.nodes[source_id]
        target = self.nodes[target_id]

        # Remove edge in source -> target direction
        self.edges[source] = [e for e in self.edges[source] if e.target.id != target_id]

        # For undirected graphs, also remove target -> source edge
        if not self.directed:
            self.edges[target] = [e for e in self.edges[target] if e.target.id != source_id]

    def get_edges(self, node_id: Union[int, str]) -> List[Edge]:
        """Get all edges for a node"""
        if node_id in self.nodes:
            return self.edges.get(self.nodes[node_id], [])
        return []

    def to_dict(self) -> Dict:
        """Serialize graph to dictionary"""
        return {
            "directed": self.directed,
            "nodes": {str(n.id): n.data for n in self.nodes.values()},
            "edges": [
                {
                    "source": str(e.source.id),
                    "target": str(e.target.id),
                    "weight": e.weight,
                    "data": e.data,
                }
                for edges in self.edges.values()
                for e in edges
                if e.directed == self.directed
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Graph":
        """Deserialize graph from dictionary"""
        graph = cls(data["directed"])
        for node_id, node_data in data["nodes"].items():
            graph.add_node(node_id, node_data)

        for edge_data in data["edges"]:
            graph.add_edge(
                edge_data["source"],
                edge_data["target"],
                edge_data.get("weight", 1.0),
                edge_data.get("data", {}),
            )
        return graph

    def __repr__(self):
        return f"Graph(directed={self.directed}, nodes={len(self.nodes)}, edges={sum(len(e) for e in self.edges.values())})"
