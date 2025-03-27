def dfs(graph, start_node: int) -> None:
    """
    Perform Depth-First Search (DFS) starting from the given node.

    :param graph: The graph instance.
    :param start_node: The node where DFS should start.
    """
    visited = set()
    _dfs_helper(graph, start_node, visited)


def _dfs_helper(graph, node: int, visited: set) -> None:
    """Helper method for DFS traversal."""
    if node not in visited:
        print(node, end=" ")
        visited.add(node)
        for neighbor, _ in graph.get_neighbors(node):
            _dfs_helper(graph, neighbor, visited)
