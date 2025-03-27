"""
Graph module for creating and manipulating graphs with support for various algorithms.

This module provides:
- Graph representation supporting directed, undirected, and weighted edges.
- Depth-First Search (DFS) algorithm.
- Breadth-First Search (BFS) algorithm.
- Dijkstra's algorithm for finding the shortest path.
- A* algorithm for finding the shortest path with heuristic.

The graph is represented by an adjacency list.
"""

from typing import Dict, List, Tuple
import heapq


class Graph:
    """Graph representation supporting directed, undirected, and weighted edges."""

    def __init__(self, directed: bool = False):
        """
        Initialize a graph.

        :param directed: If True, creates a directed graph; otherwise, undirected.
        """
        self.directed = directed
        self.adj_list: Dict[int, List[Tuple[int, float]]] = {}

    def add_node(self, node: int) -> None:
        """Add a node to the graph."""
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, node1: int, node2: int, weight: float = 1.0) -> None:
        """
        Add an edge between node1 and node2 with an optional weight.

        :param node1: First node.
        :param node2: Second node.
        :param weight: Edge weight (default is 1.0).
        """
        self.add_node(node1)
        self.add_node(node2)
        self.adj_list[node1].append((node2, weight))
        if not self.directed:
            self.adj_list[node2].append((node1, weight))

    def remove_edge(self, node1: int, node2: int) -> None:
        """Remove the edge between node1 and node2 if it exists."""
        self.adj_list[node1] = [(n, w) for n, w in self.adj_list[node1] if n != node2]
        if not self.directed:
            self.adj_list[node2] = [(n, w) for n, w in self.adj_list[node2] if n != node1]

    def remove_node(self, node: int) -> None:
        """Remove a node and all associated edges."""
        if node in self.adj_list:
            del self.adj_list[node]
            for key in self.adj_list:
                self.adj_list[key] = [(n, w) for n, w in self.adj_list[key] if n != node]

    def get_neighbors(self, node: int) -> List[Tuple[int, float]]:
        """Return a list of neighbors for a given node."""
        return self.adj_list.get(node, [])

    def __repr__(self) -> str:
        """String representation of the graph."""
        return f"Graph(directed={self.directed}, nodes={list(self.adj_list.keys())})"

    def display(self) -> None:
        """Print adjacency list representation."""
        for node, neighbors in self.adj_list.items():
            print(f"{node} -> {neighbors}")

    def dfs(self, start_node: int) -> None:
        """
        Perform Depth-First Search (DFS) starting from the given node.

        :param start_node: The node where DFS should start.
        """
        visited = set()
        self._dfs_helper(start_node, visited)

    def _dfs_helper(self, node: int, visited: set) -> None:
        """Helper method for DFS traversal."""
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            for neighbor, _ in self.adj_list[node]:
                self._dfs_helper(neighbor, visited)

    def bfs(self, start_node: int) -> None:
        """
        Perform Breadth-First Search (BFS) starting from the given node.

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
                    neighbor for neighbor, _ in self.adj_list[node] if neighbor not in visited
                )

    def dijkstra(self, start_node: int) -> Dict[int, float]:
        """
        Perform Dijkstra's algorithm for shortest paths from the start node.

        :param start_node: The node where the algorithm should start.
        :return: A dictionary containing the shortest distances to all nodes.
        """
        distances = {node: float("inf") for node in self.adj_list}
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.adj_list[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

    def a_star(self, start_node: int, goal_node: int, heuristic: Dict[int, float]) -> List[int]:
        """
        Perform A* algorithm for shortest path from start_node to goal_node using heuristic.

        :param start_node: The node where the algorithm should start.
        :param goal_node: The target node to reach.
        :param heuristic: A dictionary containing the heuristic for each node.
        :return: A list of nodes representing the shortest path from start to goal.
        """
        open_set = {start_node}
        came_from = {}
        g_score = {node: float("inf") for node in self.adj_list}
        g_score[start_node] = 0
        f_score = {node: float("inf") for node in self.adj_list}
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
            for neighbor, weight in self.adj_list[current_node]:
                tentative_g_score = g_score[current_node] + weight
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]
                    open_set.add(neighbor)

        return []
