import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QLineEdit,
    QSpinBox,
    QFileDialog,
    QMessageBox,
    QComboBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from pyqtgraph import GraphItem, PlotWidget, TextItem
from graph import Graph
from storage import (
    save_to_json,
    load_from_json,
    save_to_xml,
    load_from_xml,
    save_to_csv,
    load_from_csv,
)


class GraphVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = Graph()
        self.node_positions = {}  # Stores node positions {node_id: (x, y)}
        self.text_items = []  # Stores text labels for nodes
        self.initUI()
        self.setWindowTitle("Graph4Py - Obsidian-like Visualizer")
        self.setGeometry(100, 100, 1200, 800)

    def initUI(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Graph visualization area
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground("w")
        self.graph_item = GraphItem()
        self.plot_widget.addItem(self.graph_item)
        main_layout.addWidget(self.plot_widget, stretch=3)

        # Control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        control_panel.setMaximumWidth(300)
        main_layout.addWidget(control_panel)

        # Node management
        node_group = QWidget()
        node_layout = QVBoxLayout(node_group)
        node_layout.addWidget(QLabel("<b>Node Management</b>"))

        self.node_name_input = QLineEdit()
        self.node_name_input.setPlaceholderText("Node name")
        node_layout.addWidget(self.node_name_input)

        add_node_btn = QPushButton("Add Node")
        add_node_btn.clicked.connect(self.add_node)
        node_layout.addWidget(add_node_btn)

        remove_node_btn = QPushButton("Remove Selected Node")
        remove_node_btn.clicked.connect(self.remove_node)
        node_layout.addWidget(remove_node_btn)

        control_layout.addWidget(node_group)

        # Edge management
        edge_group = QWidget()
        edge_layout = QVBoxLayout(edge_group)
        edge_layout.addWidget(QLabel("<b>Edge Management</b>"))

        self.edge_from = QComboBox()
        self.edge_to = QComboBox()
        self.edge_weight = QSpinBox()
        self.edge_weight.setValue(1)

        edge_layout.addWidget(QLabel("From:"))
        edge_layout.addWidget(self.edge_from)
        edge_layout.addWidget(QLabel("To:"))
        edge_layout.addWidget(self.edge_to)
        edge_layout.addWidget(QLabel("Weight:"))
        edge_layout.addWidget(self.edge_weight)

        add_edge_btn = QPushButton("Add Edge")
        add_edge_btn.clicked.connect(self.add_edge)
        edge_layout.addWidget(add_edge_btn)

        remove_edge_btn = QPushButton("Remove Edge")
        remove_edge_btn.clicked.connect(self.remove_edge)
        edge_layout.addWidget(remove_edge_btn)

        control_layout.addWidget(edge_group)

        # File operations
        file_group = QWidget()
        file_layout = QVBoxLayout(file_group)
        file_layout.addWidget(QLabel("<b>File Operations</b>"))

        save_btn = QPushButton("Save Graph")
        save_btn.clicked.connect(self.save_graph)
        file_layout.addWidget(save_btn)

        load_btn = QPushButton("Load Graph")
        load_btn.clicked.connect(self.load_graph)
        file_layout.addWidget(load_btn)

        self.format_selector = QComboBox()
        self.format_selector.addItems(["JSON", "XML", "CSV"])
        file_layout.addWidget(self.format_selector)

        control_layout.addWidget(file_group)

        # Visualization settings
        vis_group = QWidget()
        vis_layout = QVBoxLayout(vis_group)
        vis_layout.addWidget(QLabel("<b>Visualization</b>"))

        refresh_btn = QPushButton("Refresh Layout")
        refresh_btn.clicked.connect(self.update_graph)
        vis_layout.addWidget(refresh_btn)

        control_layout.addWidget(vis_group)

        self.update_node_dropdowns()
        self.update_graph()

    def update_node_dropdowns(self):
        """Update the node selection dropdowns"""
        nodes = [str(node.id) for node in self.graph.node_list]
        self.edge_from.clear()
        self.edge_to.clear()
        self.edge_from.addItems(nodes)
        self.edge_to.addItems(nodes)

    def add_node(self):
        """Add a new node to the graph"""
        name = self.node_name_input.text()
        if name and name not in [str(node.id) for node in self.graph.node_list]:
            self.graph.add_node(name)
            self.node_positions[name] = np.random.rand(2) * 10  # Random initial position
            self.update_node_dropdowns()
            self.update_graph()
            self.node_name_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Node name must be unique and not empty")

    def remove_node(self):
        """Remove selected node from the graph"""
        name = self.edge_from.currentText()
        if name in [str(node.id) for node in self.graph.node_list]:
            self.graph.remove_node(name)
            if name in self.node_positions:
                del self.node_positions[name]
            self.update_node_dropdowns()
            self.update_graph()

    def add_edge(self):
        """Add an edge between selected nodes"""
        from_node = self.edge_from.currentText()
        to_node = self.edge_to.currentText()
        weight = self.edge_weight.value()

        if from_node and to_node:
            self.graph.add_edge(from_node, to_node, weight)
            self.update_graph()

    def remove_edge(self):
        """Remove edge between selected nodes"""
        from_node = self.edge_from.currentText()
        to_node = self.edge_to.currentText()

        if from_node and to_node:
            self.graph.remove_edge(from_node, to_node)
            self.update_graph()

    def update_graph(self):
        """Update the graph visualization"""
        # Clear previous text items
        for item in self.text_items:
            self.plot_widget.removeItem(item)
        self.text_items = []

        nodes = [node for node in self.graph.node_list]
        node_ids = [str(node.id) for node in nodes]
        edges = []

        # Create edges list with proper indices
        for node in nodes:
            for edge in self.graph.get_edges(node.id):
                if edge.directed == self.graph.directed:  # Avoid duplicates for undirected
                    source_idx = node_ids.index(str(edge.source.id))
                    target_idx = node_ids.index(str(edge.target.id))
                    edges.append((source_idx, target_idx))

        # Use existing positions or create new ones
        pos = np.zeros((len(nodes), 2))
        for i, node in enumerate(nodes):
            node_id = str(node.id)
            if node_id in self.node_positions:
                pos[i] = self.node_positions[node_id]
            else:
                pos[i] = np.random.rand(2) * 10
                self.node_positions[node_id] = pos[i]

            # Update node position in the Node object
            node.update_position(pos[i][0], pos[i][1])

        # Visual styling similar to Obsidian
        self.graph_item.setData(
            pos=pos,
            adj=np.array(edges) if edges else np.zeros((0, 2)),
            symbolBrush="#4CAF50",
            symbolPen="w",
            symbolSize=20,
            pxMode=True,
            pen=QPen(QColor("#2196F3"), 2),
            hoverPen=QPen(QColor("#FF5722"), 3),
            hoverSymbolBrush="#FF5722",
            hoverSymbolSize=25,
        )

        # Add node labels
        for i, node in enumerate(nodes):
            text = TextItem(str(node.id), color="#333333")
            self.plot_widget.addItem(text)
            text.setPos(pos[i][0] + 0.5, pos[i][1] + 0.5)
            self.text_items.append(text)

    def save_graph(self):
        """Save graph to file"""
        options = QFileDialog.Options()
        file_format = self.format_selector.currentText()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            f"Save Graph As {file_format}",
            "",
            f"{file_format} Files (*.{file_format.lower()})",
            options=options,
        )

        if filename:
            try:
                if file_format == "JSON":
                    save_to_json(self.graph, filename)
                elif file_format == "XML":
                    save_to_xml(self.graph, filename)
                elif file_format == "CSV":
                    save_to_csv(self.graph, filename)
                QMessageBox.information(self, "Success", "Graph saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save graph: {str(e)}")

    def load_graph(self):
        """Load graph from file"""
        options = QFileDialog.Options()
        file_format = self.format_selector.currentText()
        filename, _ = QFileDialog.getOpenFileName(
            self,
            f"Load {file_format} Graph",
            "",
            f"{file_format} Files (*.{file_format.lower()})",
            options=options,
        )

        if filename:
            try:
                if file_format == "JSON":
                    self.graph = load_from_json(filename)
                elif file_format == "XML":
                    self.graph = load_from_xml(filename)
                elif file_format == "CSV":
                    self.graph = load_from_csv(filename)

                # Reset positions for loaded graph
                self.node_positions = {}
                self.update_node_dropdowns()
                self.update_graph()
                QMessageBox.information(self, "Success", "Graph loaded successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load graph: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphVisualizer()
    window.show()
    sys.exit(app.exec())
