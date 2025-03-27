import os
import storage
from graph import Graph


def create_test_graph():
    """Создаёт тестовый граф для проверки хранения."""
    g = Graph(directed=True)
    g.add_edge(1, 2, 3.5)
    g.add_edge(2, 3, 1.2)
    return g


def test_save_load_json():
    """Тестирует сохранение и загрузку JSON."""
    g = create_test_graph()
    storage.save_to_json(g, "test_graph.json")
    loaded_g = storage.load_from_json("test_graph.json")

    assert loaded_g.to_dict() == g.to_dict()

    os.remove("test_graph.json")


def test_save_load_xml():
    """Тестирует сохранение и загрузку XML."""
    g = create_test_graph()
    storage.save_to_xml(g, "test_graph.xml")
    loaded_g = storage.load_from_xml("test_graph.xml")

    assert loaded_g.to_dict() == g.to_dict()

    os.remove("test_graph.xml")


def test_save_load_csv():
    """Тестирует сохранение и загрузку CSV."""
    g = create_test_graph()
    storage.save_to_csv(g, "test_graph.csv")
    loaded_g = storage.load_from_csv("test_graph.csv", directed=True)

    assert loaded_g.to_dict() == g.to_dict()

    os.remove("test_graph.csv")
