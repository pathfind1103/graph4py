import json
import xml.etree.ElementTree as ET
import csv
from graph import Graph

"""
Storage module for saving and loading graphs in JSON, XML, and CSV formats.
"""


def save_to_json(graph: Graph, filename: str) -> None:
    """Save the graph to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(graph.to_dict(), f, indent=4)


def load_from_json(filename: str) -> Graph:
    """Load a graph from a JSON file."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Graph.from_dict(data)


def save_to_xml(graph: Graph, filename: str) -> None:
    """Save the graph to an XML file."""
    root = ET.Element("graph", directed=str(graph.directed).lower())

    nodes_elem = ET.SubElement(root, "nodes")
    for node in graph.node_list:
        ET.SubElement(nodes_elem, "node", id=str(node.id))

    edges_elem = ET.SubElement(root, "edges")
    for edges in graph.edges.values():
        for edge in edges:
            if edge.directed == graph.directed:
                ET.SubElement(
                    edges_elem,
                    "edge",
                    source=str(edge.source.id),
                    target=str(edge.target.id),
                    weight=str(edge.weight),
                )

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)


def load_from_xml(filename: str) -> Graph:
    """Load a graph from an XML file."""
    tree = ET.parse(filename)
    root = tree.getroot()

    directed = root.get("directed", "false").lower() == "true"
    graph = Graph(directed=directed)

    nodes_elem = root.find("nodes")
    if nodes_elem is not None:
        for node_elem in nodes_elem.findall("node"):
            node_id = node_elem.get("id")
            graph.add_node(node_id)

    edges_elem = root.find("edges")
    if edges_elem is not None:
        for edge_elem in edges_elem.findall("edge"):
            source = edge_elem.get("source")
            target = edge_elem.get("target")
            weight = float(edge_elem.get("weight", 1.0))
            graph.add_edge(source, target, weight)

    return graph


def save_to_csv(graph: Graph, filename: str) -> None:
    """Save the graph to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "weight"])

        saved_edges = set()
        for edges in graph.edges.values():
            for edge in edges:
                if edge.directed == graph.directed:
                    edge_key = (
                        (edge.source.id, edge.target.id)
                        if graph.directed
                        else tuple(sorted((edge.source.id, edge.target.id)))
                    )
                    if edge_key not in saved_edges:
                        writer.writerow([edge.source.id, edge.target.id, edge.weight])
                        saved_edges.add(edge_key)


def load_from_csv(filename: str, directed: bool = False) -> Graph:
    """Load a graph from a CSV file."""
    graph = Graph(directed=directed)
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 3:
                continue

            try:
                source, target = int(row[0]), int(row[1])
                weight = float(row[2])
                graph.add_node(source)
                graph.add_node(target)
                graph.add_edge(source, target, weight)
                break
            except (ValueError, IndexError):
                continue

        for row in reader:
            if len(row) < 3:
                continue
            try:
                source, target = int(row[0]), int(row[1])
                weight = float(row[2])
                graph.add_node(source)
                graph.add_node(target)
                graph.add_edge(source, target, weight)
            except (ValueError, IndexError):
                continue

    return graph
