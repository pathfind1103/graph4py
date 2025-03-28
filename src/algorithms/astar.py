from typing import Dict, List, Union, Set
from graph import Graph
import heapq


def a_star(
    graph: Graph,
    start_node: Union[int, str],
    goal_node: Union[int, str],
    heuristic: Dict[Union[int, str], float],
) -> List[Union[int, str]]:
    """
    Perform A* algorithm for shortest path from start_node to goal_node using heuristic.

    :param graph: The graph instance
    :param start_node: The node where the algorithm should start
    :param goal_node: The target node to reach
    :param heuristic: A dictionary containing the heuristic for each node
    :return: A list of nodes representing the shortest path from start to goal
    :raises: ValueError if start_node or goal_node don't exist in graph
    """
    if start_node not in graph.nodes:
        raise ValueError(f"Start node {start_node} not found in graph")
    if goal_node not in graph.nodes:
        raise ValueError(f"Goal node {goal_node} not found in graph")

    # Initialize data structures
    open_set: Set[Union[int, str]] = {start_node}
    came_from: Dict[Union[int, str], Union[int, str]] = {}

    # Use infinity as default value
    inf = float("inf")
    g_score: Dict[Union[int, str], float] = {node_id: inf for node_id in graph.nodes}
    g_score[start_node] = 0

    f_score: Dict[Union[int, str], float] = {node_id: inf for node_id in graph.nodes}
    f_score[start_node] = heuristic.get(start_node, inf)

    # Priority queue for efficient min extraction
    open_heap = []
    heapq.heappush(open_heap, (f_score[start_node], start_node))

    while open_set:
        _, current_node = heapq.heappop(open_heap)

        # Skip if this node was already processed with better score
        if current_node not in open_set:
            continue

        if current_node == goal_node:
            # Reconstruct path
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node)
            return path[::-1]

        open_set.remove(current_node)

        for edge in graph.get_edges(current_node):
            neighbor = edge.target.id
            weight = edge.weight

            # Calculate tentative g score
            tentative_g_score = g_score[current_node] + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic.get(neighbor, inf)

                if neighbor not in open_set:
                    open_set.add(neighbor)
                    heapq.heappush(open_heap, (f_score[neighbor], neighbor))

    return []  # No path found
