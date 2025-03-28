from typing import Set, Union
from graph import Graph


def dfs(graph: Graph, start_node: Union[int, str]) -> None:
    """
    Perform Depth-First Search (DFS) starting from the given node.

    :param graph: The graph instance
    :param start_node: The node ID where DFS should start (can be int or str)
    """
    visited: Set[Union[int, str]] = set()
    _dfs_helper(graph, start_node, visited)


def _dfs_helper(graph: Graph, node_id: Union[int, str], visited: Set[Union[int, str]]) -> None:
    """Helper method for DFS traversal."""
    if node_id not in visited:
        print(node_id, end=" ")
        visited.add(node_id)

        # Get all edges from current node
        for edge in graph.get_edges(node_id):
            _dfs_helper(graph, edge.target.id, visited)
