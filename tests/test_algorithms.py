import sys
import pytest

from graph import Graph
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import a_star
from six import StringIO


def test_bfs_directed():
    g = Graph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    bfs(g, 1)
    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert output == "1 2 3 4"


def test_bfs_undirected():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    bfs(g, 1)
    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert output == "1 2 3 4"


def test_bfs_invalid_node():
    g = Graph()
    with pytest.raises(ValueError):
        bfs(g, 99)


def test_dfs_directed():
    g = Graph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)

    # Захватываем вывод print
    from io import StringIO
    import sys

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    dfs(g, 1)
    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert output == "1 2 4 3"


def test_dfs_undirected():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    g.add_edge(2, 3)

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    dfs(g, 1)
    output = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    assert output == "1 2 3"


def test_dijkstra_basic():
    g = Graph(directed=True)
    g.add_edge(1, 2, 1.0)
    g.add_edge(2, 3, 2.0)
    g.add_edge(1, 3, 4.0)

    distances = dijkstra(g, 1)
    assert distances == {1: 0, 2: 1.0, 3: 3.0}


def test_dijkstra_unreachable():
    g = Graph(directed=True)
    g.add_edge(1, 2, 1.0)
    g.add_node(3)

    distances = dijkstra(g, 1)
    assert distances[3] == float("inf")


def test_dijkstra_invalid_start():
    g = Graph()
    with pytest.raises(ValueError):
        dijkstra(g, 99)


def test_a_star_basic():
    g = Graph(directed=True)
    g.add_edge(1, 2, 1.0)
    g.add_edge(2, 3, 1.0)
    g.add_edge(1, 3, 3.0)

    heuristic = {1: 2.0, 2: 1.0, 3: 0.0}
    path = a_star(g, 1, 3, heuristic)
    assert path == [1, 2, 3]


def test_a_star_no_path():
    g = Graph(directed=True)
    g.add_edge(1, 2, 1.0)
    g.add_node(3)

    heuristic = {1: 1.0, 2: 0.0, 3: 0.0}
    path = a_star(g, 1, 3, heuristic)
    assert path == []


def test_a_star_invalid_nodes():
    g = Graph()
    with pytest.raises(ValueError):
        a_star(g, 1, 2, {})
