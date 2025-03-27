"""
Storage module for saving and loading graphs in JSON, XML, and CSV formats.
"""

import json
import xml.etree.ElementTree as ET
import csv
from graph import Graph


def save_to_json(graph: Graph, filename: str) -> None:
    """Save the graph to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(graph.to_dict(), f, indent=4)


def load_from_json(filename: str) -> Graph:
    """Load a graph from a JSON file."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Преобразуем строки обратно в числа
    graph = Graph(directed=data["directed"])
    graph.adj_list = {
        int(node): [(neighbor, weight) for neighbor, weight in edges]
        for node, edges in data["adj_list"].items()
    }

    return graph


def save_to_xml(graph: Graph, filename: str) -> None:
    """Save the graph to an XML file."""
    root = ET.Element("graph", directed=str(graph.directed).lower())
    for node, edges in graph.adj_list.items():
        node_elem = ET.SubElement(root, "node", id=str(node))
        for neighbor, weight in edges:
            ET.SubElement(node_elem, "edge", target=str(neighbor), weight=str(weight))

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)


def load_from_xml(filename: str) -> Graph:
    """Load a graph from an XML file."""
    tree = ET.parse(filename)
    root = tree.getroot()
    directed = root.get("directed", "false").lower() == "true"
    graph = Graph(directed=directed)

    for node_elem in root.findall("node"):
        node = int(node_elem.get("id"))
        graph.add_node(node)
        for edge_elem in node_elem.findall("edge"):
            neighbor = int(edge_elem.get("target"))
            weight = float(edge_elem.get("weight"))
            graph.add_edge(node, neighbor, weight)

    return graph


def save_to_csv(graph: Graph, filename: str) -> None:
    """Save the graph to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node1", "node2", "weight"])
        for node, edges in graph.adj_list.items():
            for neighbor, weight in edges:
                writer.writerow([node, neighbor, weight])


def load_from_csv(filename: str, directed: bool = False) -> Graph:
    """Load a graph from a CSV file."""
    graph = Graph(directed=directed)
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            node1, node2, weight = int(row[0]), int(row[1]), float(row[2])
            graph.add_edge(node1, node2, weight)
    return graph
