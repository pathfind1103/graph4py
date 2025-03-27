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

    def get_edges(self, node_id: Union[int, str]) -> List[Edge]:
        """Получаем ребра для узла по его ID"""
        node = self.nodes.get(node_id)
        if node:
            return self.edges.get(node, [])
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
