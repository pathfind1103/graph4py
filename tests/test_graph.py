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
