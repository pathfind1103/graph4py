import json
import sys
import numpy as np
import time
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
    QTextEdit,
)
from PyQt6.QtCore import Qt
from pyqtgraph import GraphItem, PlotWidget, TextItem
from graph import Graph
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import a_star


class GraphVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = Graph()
        self.node_positions = {}  # {node_id: (x, y)}
        self.text_items = []  # Хранит текстовые метки узлов
        self.selected_node = None  # Узел для перетаскивания

        # Obsidian-inspired visual parameters
        self.visual_params = {
            "min_node_size": 6,
            "min_edge_width": 0.5,
            "min_font_size": 7,
            "node_zoom_factor": 0.5,
            "edge_zoom_factor": 0.3,
            "node_color": "#4682B4",  # Steel blue
            "edge_color": "#A9A9A9",  # Dark gray
            "base_node_size": 1.0,
            "base_pixel_size": 12,
            "base_edge_width": 1.0,
            "base_font_size": 8,
            "node_border_color": "#F5F6F5",  # Light gray
            "hover_color": "#FF4500",  # Orange red
            "text_color": "#333333",
            "background_color": "#F5F6F5",  # Light gray background
        }

        self.current_zoom = 1.0
        self.initUI()
        self.setWindowTitle("Graph4Py - Interactive Visualizer")
        self.setGeometry(100, 100, 1200, 800)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Graph visualization area
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground(self.visual_params["background_color"])
        self.plot_widget.setMouseEnabled(x=True, y=True)
        self.plot_widget.setLimits(xMin=-1000, xMax=1000, yMin=-1000, yMax=1000)
        self.plot_widget.sigRangeChanged.connect(self.handle_zoom)
        self.graph_item = GraphItem()
        self.plot_widget.addItem(self.graph_item)
        main_layout.addWidget(self.plot_widget, stretch=3)

        # Control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        control_panel.setMaximumWidth(300)
        main_layout.addWidget(control_panel)

        self.setupNodeManagement(control_layout)
        self.setupEdgeManagement(control_layout)
        self.setupAlgorithmExecution(control_layout)
        self.setupFileOperations(control_layout)
        self.setupVisualization(control_layout)

        self.update_node_dropdowns()
        self.update_graph()

    def setupNodeManagement(self, layout):
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
        layout.addWidget(node_group)

    def setupEdgeManagement(self, layout):
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
        layout.addWidget(edge_group)

    def setupAlgorithmExecution(self, layout):
        algo_group = QWidget()
        algo_layout = QVBoxLayout(algo_group)
        algo_layout.addWidget(QLabel("<b>Algorithm Execution</b>"))
        self.algo_selector = QComboBox()
        self.algo_selector.addItems(["BFS", "DFS", "Dijkstra", "A*"])
        algo_layout.addWidget(QLabel("Algorithm:"))
        algo_layout.addWidget(self.algo_selector)
        self.start_node_input = QComboBox()
        algo_layout.addWidget(QLabel("Start Node:"))
        algo_layout.addWidget(self.start_node_input)
        self.end_node_input = QComboBox()
        algo_layout.addWidget(QLabel("End Node (for A*):"))
        algo_layout.addWidget(self.end_node_input)
        run_algo_btn = QPushButton("Run Algorithm")
        run_algo_btn.clicked.connect(self.run_algorithm)
        algo_layout.addWidget(run_algo_btn)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFixedHeight(100)
        algo_layout.addWidget(QLabel("Results:"))
        algo_layout.addWidget(self.result_display)
        layout.addWidget(algo_group)

    def setupFileOperations(self, layout):
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
        layout.addWidget(file_group)

    def setupVisualization(self, layout):
        vis_group = QWidget()
        vis_layout = QVBoxLayout(vis_group)
        vis_layout.addWidget(QLabel("<b>Visualization</b>"))
        refresh_btn = QPushButton("Refresh Layout")
        refresh_btn.clicked.connect(self.update_graph)
        vis_layout.addWidget(refresh_btn)
        reset_zoom_btn = QPushButton("Reset Zoom")
        reset_zoom_btn.clicked.connect(self.reset_zoom)
        vis_layout.addWidget(reset_zoom_btn)
        layout.addWidget(vis_group)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.plot_widget.mapToScene(event.pos())
            for node_id, node_pos in self.node_positions.items():
                distance = np.linalg.norm(np.array(node_pos) - np.array([pos.x(), pos.y()]))
                if distance < 0.5 * self.current_zoom:  # Adjust for zoom
                    self.selected_node = node_id
                    break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selected_node:
            pos = self.plot_widget.mapToScene(event.pos())
            self.node_positions[self.selected_node] = [pos.x(), pos.y()]
            self.update_graph()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected_node = None
        super().mouseReleaseEvent(event)

    def handle_zoom(self, _, view_range):
        x_range = view_range[0][1] - view_range[0][0]
        self.current_zoom = max(0.2, min(5.0, 100 / x_range))
        self.update_graph()

    def reset_zoom(self):
        self.plot_widget.setRange(xRange=[-10, 10], yRange=[-10, 10])
        self.current_zoom = 1.0
        self.update_graph()

    def update_node_dropdowns(self):
        nodes = [str(node.id) for node in self.graph.node_list]
        self.edge_from.clear()
        self.edge_to.clear()
        self.start_node_input.clear()
        self.end_node_input.clear()
        self.edge_from.addItems(nodes)
        self.edge_to.addItems(nodes)
        self.start_node_input.addItems(nodes)
        self.end_node_input.addItems(nodes)

    def add_node(self):
        name = self.node_name_input.text()
        if name and name not in [str(node.id) for node in self.graph.node_list]:
            self.graph.add_node(name)
            self.node_positions[name] = np.random.rand(2) * 10
            self.update_node_dropdowns()
            self.update_graph()
            self.node_name_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Node name must be unique and not empty")

    def remove_node(self):
        name = self.edge_from.currentText()
        if name in [str(node.id) for node in self.graph.node_list]:
            self.graph.remove_node(name)
            if name in self.node_positions:
                del self.node_positions[name]
            self.update_node_dropdowns()
            self.update_graph()

    def add_edge(self):
        from_node = self.edge_from.currentText()
        to_node = self.edge_to.currentText()
        weight = self.edge_weight.value()
        if from_node and to_node:
            self.graph.add_edge(from_node, to_node, weight)
            self.update_graph()

    def remove_edge(self):
        from_node = self.edge_from.currentText()
        to_node = self.edge_to.currentText()
        if from_node and to_node:
            self.graph.remove_edge(from_node, to_node)
            self.update_graph()

    def update_graph(self):
        params = self.visual_params
        nodes = self.graph.node_list
        if not nodes:
            return

        node_ids = {str(node.id): idx for idx, node in enumerate(nodes)}
        edges = []
        for node in nodes:
            for edge in self.graph.get_edges(node.id):
                source_idx = node_ids.get(str(edge.source.id))
                target_idx = node_ids.get(str(edge.target.id))
                if source_idx is not None and target_idx is not None:
                    edges.append((source_idx, target_idx))

        valid_nodes = [node for node in nodes if str(node.id) in node_ids]
        if not valid_nodes:
            return

        # Clear all old text labels
        for text_item in self.text_items:
            self.plot_widget.removeItem(text_item)
        self.text_items.clear()

        # Add new text labels for nodes
        for node in valid_nodes:
            pos = self.node_positions[node.id]
            text = TextItem(str(node.id), anchor=(0.5, 0.5))
            text.setPos(pos[0], pos[1] + 0.5)  # Offset to place above node
            text.setColor(params["text_color"])
            font = text.textItem.font()
            font.setPointSizeF(
                max(params["min_font_size"], params["base_font_size"] * self.current_zoom)
            )
            text.setFont(font)
            self.plot_widget.addItem(text)
            self.text_items.append(text)

        self.graph_item.setData(
            pos=np.array([self.node_positions[node.id] for node in valid_nodes]),
            adj=np.array(edges) if edges else None,
            size=params["base_pixel_size"] * self.current_zoom,
            symbolBrush=params["node_color"],
            pen=params["edge_color"],
        )

    def run_algorithm(self):
        algo = self.algo_selector.currentText()
        start_node = self.start_node_input.currentText()
        end_node = self.end_node_input.currentText() if algo == "A*" else None

        if not start_node:
            QMessageBox.warning(self, "Warning", "Please select a start node")
            return

        try:
            start_time = time.perf_counter()
            result = None

            if algo == "BFS":
                from io import StringIO

                old_stdout = sys.stdout
                sys.stdout = StringIO()
                bfs(self.graph, start_node)
                result = sys.stdout.getvalue().strip()
                sys.stdout = old_stdout
            elif algo == "DFS":
                from io import StringIO

                old_stdout = sys.stdout
                sys.stdout = StringIO()
                dfs(self.graph, start_node)
                result = sys.stdout.getvalue().strip()
                sys.stdout = old_stdout
            elif algo == "Dijkstra":
                distances = dijkstra(self.graph, start_node)
                result = "\n".join(f"{node}: {dist}" for node, dist in distances.items())
            elif algo == "A*":
                if not end_node:
                    QMessageBox.warning(self, "Warning", "Please select an end node for A*")
                    return
                heuristic = {str(node.id): 0.0 for node in self.graph.node_list}
                path = a_star(self.graph, start_node, end_node, heuristic)
                result = " -> ".join(path) if path else "No path found"

            end_time = time.perf_counter()
            execution_time = end_time - start_time

            self.result_display.setText(
                f"Result:\n{result}\n\nExecution Time: {execution_time:.6f} seconds"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run algorithm: {str(e)}")

    def save_graph(self):
        file_format = self.format_selector.currentText()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            f"Save Graph As {file_format}",
            "",
            f"{file_format} Files (*.{file_format.lower()})",
        )
        if not filename:
            return
        try:
            if file_format == "JSON":
                graph_data = {
                    "graph": self.graph.to_dict(),
                    "node_positions": {
                        str(k): v.tolist() if isinstance(v, np.ndarray) else list(v)
                        for k, v in self.node_positions.items()
                    },
                }
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(graph_data, f, indent=4)
            else:
                from storage import save_to_xml, save_to_csv

                if file_format == "XML":
                    save_to_xml(self.graph, filename, node_positions=self.node_positions)
                elif file_format == "CSV":
                    save_to_csv(self.graph, filename, node_positions=self.node_positions)
            QMessageBox.information(self, "Success", "Graph saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save graph: {str(e)}")

    def load_graph(self):
        file_format = self.format_selector.currentText()
        filename, _ = QFileDialog.getOpenFileName(
            self, f"Load {file_format} Graph", "", f"{file_format} Files (*.{file_format.lower()})"
        )
        if filename:
            try:
                if file_format == "JSON":
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.graph = Graph(directed=data["graph"]["directed"])
                    for node_id, node_data in data["graph"]["nodes"].items():
                        self.graph.add_node(node_id, node_data)
                    added_edges = set()
                    for edge_data in data["graph"]["edges"]:
                        source = edge_data["source"]
                        target = edge_data["target"]
                        if not self.graph.directed:
                            edge_key = tuple(sorted((source, target)))
                            if edge_key in added_edges:
                                continue
                            added_edges.add(edge_key)
                        self.graph.add_edge(
                            source,
                            target,
                            edge_data.get("weight", 1.0),
                            edge_data.get("data", {}),
                        )
                    self.node_positions = {
                        k: (
                            tuple(v)
                            if isinstance(v, list)
                            and len(v) == 2
                            and all(isinstance(x, (int, float)) for x in v)
                            else np.random.rand(2) * 10
                        )
                        for k, v in data.get("node_positions", {}).items()
                    }
                else:
                    from storage import load_from_xml, load_from_csv

                    if file_format == "XML":
                        self.graph, self.node_positions = load_from_xml(filename)
                    elif file_format == "CSV":
                        self.graph, self.node_positions = load_from_csv(
                            filename, directed=self.graph.directed
                        )
                for node in self.graph.node_list:
                    if str(node.id) not in self.node_positions:
                        self.node_positions[str(node.id)] = np.random.rand(2) * 10
                self.reset_zoom()
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
