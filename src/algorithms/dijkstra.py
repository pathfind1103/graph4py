from typing import Dict, Union
from graph import Graph
import heapq


def dijkstra(graph: Graph, start_node: Union[int, str]) -> Dict[Union[int, str], float]:
    """
    Perform Dijkstra's algorithm for shortest paths from the start node.

    :param graph: The graph instance
    :param start_node: The node ID where the algorithm should start (can be int or str)
    :return: A dictionary containing the shortest distances to all nodes
    :raises: ValueError if start_node doesn't exist in graph
    """
    if start_node not in graph.nodes:
        raise ValueError(f"Start node {start_node} not found in graph")

    # Initialize distances with infinity
    distances: Dict[Union[int, str], float] = {node.id: float("inf") for node in graph.node_list}
    distances[start_node] = 0

    # Priority queue: (distance, node_id)
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_node))

    # Set of visited nodes for optimization
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if we've already found a better path
        if current_node in visited:
            continue

        visited.add(current_node)

        # Explore all edges from current node
        for edge in graph.get_edges(current_node):
            neighbor = edge.target.id
            distance = current_distance + edge.weight

            # If found a shorter path to neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances
