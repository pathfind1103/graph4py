import pytest
import xml.etree.ElementTree as ET
import csv
from graph import Graph
from storage import (
    save_to_json,
    load_from_json,
    save_to_xml,
    load_from_xml,
    save_to_csv,
    load_from_csv,
)


@pytest.fixture
def sample_graph():
    """Фикстура с тестовым графом."""
    graph = Graph(directed=True)
    graph.add_edge(1, 2, 5.0)
    graph.add_edge(2, 3, 3.0)
    graph.add_edge(1, 3, 10.0)
    return graph


@pytest.fixture
def sample_undirected_graph():
    """Фикстура с ненаправленным графом."""
    graph = Graph(directed=False)
    graph.add_edge(1, 2, 5.0)
    graph.add_edge(2, 3, 3.0)
    return graph


def test_save_and_load_json(sample_graph, tmp_path):
    """Тест сохранения и загрузки JSON."""
    filename = tmp_path / "test_graph.json"

    save_to_json(sample_graph, filename)
    loaded_graph = load_from_json(filename)

    assert loaded_graph.directed == sample_graph.directed
    assert len(loaded_graph.node_list) == len(sample_graph.node_list)
    assert sum(len(e) for e in loaded_graph.edges.values()) == sum(
        len(e) for e in sample_graph.edges.values()
    )


def test_save_and_load_xml(sample_graph, tmp_path):
    """Тест сохранения и загрузки XML."""
    filename = tmp_path / "test_graph.xml"

    save_to_xml(sample_graph, filename)
    loaded_graph = load_from_xml(filename)

    assert loaded_graph.directed == sample_graph.directed
    assert len(loaded_graph.node_list) == len(sample_graph.node_list)
    assert sum(len(e) for e in loaded_graph.edges.values()) == sum(
        len(e) for e in sample_graph.edges.values()
    )


def test_save_and_load_csv(sample_graph, tmp_path):
    """Тест сохранения и загрузки CSV."""
    filename = tmp_path / "test_graph.csv"

    save_to_csv(sample_graph, filename)
    loaded_graph = load_from_csv(filename, directed=True)

    assert loaded_graph.directed == sample_graph.directed
    assert len(loaded_graph.node_list) == len(sample_graph.node_list)
    assert sum(len(e) for e in loaded_graph.edges.values()) == sum(
        len(e) for e in sample_graph.edges.values()
    )


def test_load_csv_undirected(sample_undirected_graph, tmp_path):
    """Тест загрузки ненаправленного графа из CSV."""
    filename = tmp_path / "test_undirected_graph.csv"

    save_to_csv(sample_undirected_graph, filename)
    loaded_graph = load_from_csv(filename, directed=False)

    assert not loaded_graph.directed
    assert len(loaded_graph.node_list) == len(sample_undirected_graph.node_list)
    # В ненаправленном графе должно быть в 2 раза больше рёбер (каждое ребро сохраняется в обе стороны)
    assert sum(len(e) for e in loaded_graph.edges.values()) == sum(
        len(e) for e in sample_undirected_graph.edges.values()
    )


def test_load_nonexistent_file(tmp_path):
    """Тест загрузки из несуществующего файла."""
    with pytest.raises(FileNotFoundError):
        load_from_json(tmp_path / "nonexistent.json")

    with pytest.raises(FileNotFoundError):
        load_from_xml(tmp_path / "nonexistent.xml")

    with pytest.raises(FileNotFoundError):
        load_from_csv(tmp_path / "nonexistent.csv")


def test_xml_invalid_format(tmp_path):
    """Тест загрузки XML с некорректным форматом."""
    filename = tmp_path / "invalid.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("This is not XML at all")

    with pytest.raises((ET.ParseError, UnicodeDecodeError)):
        load_from_xml(filename)


def test_csv_missing_header(tmp_path):
    """Тест загрузки CSV без заголовка."""
    filename = tmp_path / "no_header.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([1, 2, 5.0])
        writer.writerow([2, 3, 3.0])

    graph = load_from_csv(filename)
    assert len(graph.node_list) == 3
    assert any(e.target.id == 2 for edges in graph.edges.values() for e in edges)
    assert any(e.target.id == 3 for edges in graph.edges.values() for e in edges)


def test_csv_invalid_data(tmp_path):
    """Тест загрузки CSV с некорректными данными."""
    filename = tmp_path / "invalid.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "weight"])
        writer.writerow(["not_a_number", 2, 5.0])
        writer.writerow([1, "invalid_weight", "not_a_float"])
        writer.writerow([3, 4, 1.0])

    graph = load_from_csv(filename)
    assert len(graph.node_list) == 2
    assert set(node.id for node in graph.node_list) == {3, 4}
    assert any(e.target.id == 4 for edges in graph.edges.values() for e in edges)


def test_json_empty_graph(tmp_path):
    """Тест сохранения и загрузки пустого графа в JSON."""
    filename = tmp_path / "empty.json"
    empty_graph = Graph(directed=False)

    save_to_json(empty_graph, filename)
    loaded_graph = load_from_json(filename)

    assert not loaded_graph.directed
    assert len(loaded_graph.node_list) == 0
    assert len(loaded_graph.edges) == 0


def test_xml_directed_attribute(tmp_path):
    """Тест корректности сохранения directed атрибута в XML."""
    filename = tmp_path / "directed_test.xml"
    directed_graph = Graph(directed=True)
    undirected_graph = Graph(directed=False)

    save_to_xml(directed_graph, filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    assert root.get("directed") == "true"

    save_to_xml(undirected_graph, filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    assert root.get("directed") == "false"
