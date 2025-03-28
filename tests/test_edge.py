from edge import Edge


def test_edge_initialization():
    edge = Edge("A", "B", 2.5, True, {"color": "blue"})
    assert edge.source == "A"
    assert edge.target == "B"
    assert edge.weight == 2.5
    assert edge.directed is True
    assert edge.data == {"color": "blue"}


def test_edge_default_values():
    edge = Edge("X", "Y")
    assert edge.source == "X"
    assert edge.target == "Y"
    assert edge.weight == 1.0
    assert edge.directed is False
    assert edge.data == {}


def test_edge_repr_directed():
    edge = Edge(1, 2, 3.0, True)
    assert repr(edge) == "Edge(1 → 2, weight=3.0)"


def test_edge_repr_undirected():
    edge = Edge("A", "B")
    assert repr(edge) == "Edge(A ↔ B, weight=1.0)"


def test_edge_reverse():
    edge = Edge("A", "B", 4.0, False, {"type": "road"})
    reversed_edge = edge.reverse()
    assert reversed_edge.source == "B"
    assert reversed_edge.target == "A"
    assert reversed_edge.weight == 4.0
    assert reversed_edge.directed is False
    assert reversed_edge.data == {"type": "road"}
