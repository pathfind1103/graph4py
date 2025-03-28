from graph import Graph


def test_graph_initialization():
    graph = Graph()
    assert graph.directed is False
    assert graph.nodes == {}
    assert graph.edges == {}


def test_add_node():
    graph = Graph()
    node = graph.add_node("A", {"value": 10})
    assert node.id == "A"
    assert node.data == {"value": 10}
    assert graph.nodes["A"] == node
    assert graph.edges[node] == []


def test_add_edge_directed():
    graph = Graph(directed=True)
    graph.add_edge("A", "B", 2.5, {"type": "road"})
    assert len(graph.edges[graph.nodes["A"]]) == 1
    assert graph.edges[graph.nodes["B"]] == []
    edge = graph.edges[graph.nodes["A"]][0]
    assert edge.source.id == "A"
    assert edge.target.id == "B"
    assert edge.weight == 2.5
    assert edge.data == {"type": "road"}


def test_add_edge_undirected():
    graph = Graph(directed=False)
    graph.add_edge("X", "Y", 3.0)
    assert len(graph.edges[graph.nodes["X"]]) == 1
    assert len(graph.edges[graph.nodes["Y"]]) == 1
    assert graph.edges[graph.nodes["X"]][0].target.id == "Y"
    assert graph.edges[graph.nodes["Y"]][0].target.id == "X"


def test_remove_node():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.remove_node("A")
    assert "A" not in graph.nodes
    assert "A" not in graph.edges
    assert len(graph.edges[graph.nodes["B"]]) == 0


def test_remove_edge():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.remove_edge("A", "B")
    assert len(graph.edges[graph.nodes["A"]]) == 0
    assert len(graph.edges[graph.nodes["B"]]) == 0


def test_to_dict():
    graph = Graph()
    graph.add_edge("A", "B", 2.0, {"road": "highway"})
    graph_dict = graph.to_dict()

    assert graph_dict["directed"] is False
    assert graph_dict["nodes"] == {"A": {}, "B": {}}

    expected_edges = [
        {"source": "A", "target": "B", "weight": 2.0, "data": {"road": "highway"}},
        {"source": "B", "target": "A", "weight": 2.0, "data": {"road": "highway"}},
    ]

    assert sorted(graph_dict["edges"], key=lambda e: (e["source"], e["target"])) == sorted(
        expected_edges, key=lambda e: (e["source"], e["target"])
    )


def test_from_dict():
    data = {
        "directed": True,
        "nodes": {"A": {}, "B": {}},
        "edges": [{"source": "A", "target": "B", "weight": 2.0, "data": {}}],
    }
    graph = Graph.from_dict(data)
    assert graph.directed is True
    assert "A" in graph.nodes
    assert "B" in graph.nodes
    assert len(graph.edges[graph.nodes["A"]]) == 1
    assert len(graph.edges[graph.nodes["B"]]) == 0
