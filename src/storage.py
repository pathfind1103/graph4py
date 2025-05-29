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


def save_to_xml(graph: Graph, filename: str, node_positions: dict = None) -> None:
    """Save the graph to an XML file, including node positions if provided."""
    root = ET.Element("graph", directed=str(graph.directed).lower())

    nodes_elem = ET.SubElement(root, "nodes")
    for node in graph.node_list:
        node_attrs = {"id": str(node.id)}
        if node_positions and str(node.id) in node_positions:
            pos = node_positions[str(node.id)]
            node_attrs["x"] = str(pos[0])
            node_attrs["y"] = str(pos[1])
        ET.SubElement(nodes_elem, "node", **node_attrs)

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


def load_from_xml(filename: str) -> tuple[Graph, dict]:
    """Load a graph and node positions from an XML file."""
    tree = ET.parse(filename)
    root = tree.getroot()

    directed = root.get("directed", "false").lower() == "true"
    graph = Graph(directed=directed)
    node_positions = {}

    nodes_elem = root.find("nodes")
    if nodes_elem is not None:
        for node_elem in nodes_elem.findall("node"):
            node_id = node_elem.get("id")
            graph.add_node(node_id)
            x = node_elem.get("x")
            y = node_elem.get("y")
            if x is not None and y is not None:
                try:
                    node_positions[node_id] = (float(x), float(y))
                except ValueError:
                    pass  # Игнорируем некорректные позиции

    edges_elem = root.find("edges")
    if edges_elem is not None:
        for edge_elem in edges_elem.findall("edge"):
            source = edge_elem.get("source")
            target = edge_elem.get("target")
            weight = float(edge_elem.get("weight", 1.0))
            graph.add_edge(source, target, weight)

    return graph, node_positions


def save_to_csv(graph: Graph, filename: str, node_positions: dict = None) -> None:
    """Save the graph to a CSV file, including node positions if provided."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "id", "source", "target", "weight", "x", "y"])

        if node_positions:
            for node_id, pos in node_positions.items():
                writer.writerow(["node", node_id, "", "", "", pos[0], pos[1]])

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
                        writer.writerow(
                            ["edge", "", edge.source.id, edge.target.id, edge.weight, "", ""]
                        )
                        saved_edges.add(edge_key)


def load_from_csv(filename: str, directed: bool = False) -> tuple[Graph, dict]:
    """Load a graph and node positions from a CSV file."""
    graph = Graph(directed=directed)
    node_positions = {}

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 7:
                continue
            try:
                record_type = row[0]
                if record_type == "node":
                    node_id, x, y = row[1], row[5], row[6]
                    graph.add_node(node_id)
                    if x and y:
                        node_positions[node_id] = (float(x), float(y))
                elif record_type == "edge":
                    source, target, weight = row[2], row[3], float(row[4])
                    graph.add_node(source)
                    graph.add_node(target)
                    graph.add_edge(source, target, weight)
            except (ValueError, IndexError):
                continue

    return graph, node_positions
