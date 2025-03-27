def a_star(graph, start_node: int, goal_node: int, heuristic):
    """
    Perform A* algorithm for shortest path from start_node to goal_node using heuristic.

    :param graph: The graph instance.
    :param start_node: The node where the algorithm should start.
    :param goal_node: The target node to reach.
    :param heuristic: A dictionary containing the heuristic for each node.
    :return: A list of nodes representing the shortest path from start to goal.
    """
    open_set = {start_node}
    came_from = {}
    g_score = {node: float("inf") for node in graph.adj_list}
    g_score[start_node] = 0
    f_score = {node: float("inf") for node in graph.adj_list}
    f_score[start_node] = heuristic[start_node]

    while open_set:
        current_node = min(open_set, key=lambda node: f_score[node])

        if current_node == goal_node:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node)
            return path[::-1]

        open_set.remove(current_node)
        for neighbor, weight in graph.get_neighbors(current_node):
            tentative_g_score = g_score[current_node] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]
                open_set.add(neighbor)

    return []
