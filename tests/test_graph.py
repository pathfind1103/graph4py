from graph import Graph


def test_add_node():
    g = Graph()
    g.add_node(1)
    assert 1 in g.adj_list


def test_add_edge():
    g = Graph()
    g.add_edge(1, 2)
    assert (2, 1.0) in g.adj_list[1]
    assert (1, 1.0) in g.adj_list[2]


def test_remove_edge():
    g = Graph()
    g.add_edge(1, 2)
    g.remove_edge(1, 2)
    assert (2, 1.0) not in g.adj_list[1]
    assert (1, 1.0) not in g.adj_list[2]


def test_remove_node():
    g = Graph()
    g.add_edge(1, 2)
    g.remove_node(1)
    assert 1 not in g.adj_list
    assert (1, 1.0) not in g.adj_list[2]


def test_dfs():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)

    from io import StringIO
    import sys

    captured_output = StringIO()
    sys.stdout = captured_output
    g.dfs(1)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == "1 2 4 3"


def test_bfs():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)

    from io import StringIO
    import sys

    captured_output = StringIO()
    sys.stdout = captured_output
    g.bfs(1)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == "1 2 3 4"


def test_dijkstra():
    g = Graph()
    g.add_edge(1, 2, 2)
    g.add_edge(1, 3, 4)
    g.add_edge(2, 3, 1)

    distances = g.dijkstra(1)
    assert distances[1] == 0
    assert distances[2] == 2
    assert distances[3] == 3


def test_a_star():
    g = Graph()
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 4, 1)
    heuristic = {1: 3, 2: 2, 3: 1, 4: 0}

    path = g.a_star(1, 4, heuristic)
    assert path == [1, 2, 3, 4]
