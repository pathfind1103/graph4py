import heapq


def dijkstra(graph, start_node: int):
    """
    Perform Dijkstra's algorithm for shortest paths from the start node.

    :param graph: The graph instance.
    :param start_node: The node where the algorithm should start.
    :return: A dictionary containing the shortest distances to all nodes.
    """
    distances = {node: float("inf") for node in graph.adj_list}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.get_neighbors(current_node):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances
