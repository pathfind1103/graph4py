from typing import Set, Union, List
from graph import Graph


def bfs(graph: Graph, start_node: Union[int, str]) -> None:
    """
    Perform Breadth-First Search (BFS) starting from the given node.

    :param graph: The graph instance
    :param start_node: The node ID where BFS should start (can be int or str)
    """
    if start_node not in graph.nodes:
        raise ValueError(f"Node {start_node} not found in graph")

    visited: Set[Union[int, str]] = set()
    queue: List[Union[int, str]] = [start_node]

    while queue:
        current_node = queue.pop(0)
        if current_node not in visited:
            print(current_node, end=" ")
            visited.add(current_node)

            # Get all edges from current node
            for edge in graph.get_edges(current_node):
                neighbor = edge.target.id
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
