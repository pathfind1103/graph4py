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


def test_dijkstra():
    g = Graph()
    g.add_edge(1, 2, 2)
    g.add_edge(1, 3, 4)
    g.add_edge(2, 3, 1)
    g.add_edge(2, 4, 7)

    distances = dijkstra(g, 1)
    assert distances == {1: 0, 2: 2, 3: 3, 4: 9}


def test_a_star():
    g = Graph()
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(1, 3, 2)
    g.add_edge(3, 4, 1)

    heuristic = {1: 3, 2: 2, 3: 1, 4: 0}  # Простейшая эвристика
    path = a_star(g, 1, 4, heuristic)
    assert path == [1, 3, 4]
