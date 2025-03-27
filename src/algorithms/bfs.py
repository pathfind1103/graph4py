def bfs(graph, start_node: int) -> None:
    """
    Perform Breadth-First Search (BFS) starting from the given node.

    :param graph: The graph instance.
    :param start_node: The node where BFS should start.
    """
    visited = set()
    queue = [start_node]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            queue.extend(
                neighbor for neighbor, _ in graph.get_neighbors(node) if neighbor not in visited
            )
