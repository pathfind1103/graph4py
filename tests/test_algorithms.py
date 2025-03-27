from graph import Graph
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import a_star


def test_bfs(capsys):
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 5)

    bfs(g, 1)
    captured = capsys.readouterr()
    assert captured.out.strip() == "1 2 3 4 5"


def test_dfs(capsys):
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 5)

    dfs(g, 1)
    captured = capsys.readouterr()
    assert captured.out.strip() in ["1 2 4 3 5", "1 3 5 2 4"]


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
