import json
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
from pyqtgraph import GraphItem, PlotWidget
from graph import Graph


class GraphVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = Graph()
        self.node_positions = {}  # {node_id: (x, y)}
        self.text_items = []  # Хранит текстовые метки узлов

        self.visual_params = {
            "min_node_size": 6,
            "min_edge_width": 0.5,
            "min_font_size": 7,
            "node_zoom_factor": 0.5,  # Параметр плавности масштабирования узлов
            "edge_zoom_factor": 0.3,  # Параметр плавности масштабирования рёбер
            "node_color": "#3F51B5",  # Красивый синий
            "edge_color": "#78909C",  # Серая сталь
            "base_node_size": 1.0,
            "base_pixel_size": 15,
            "base_edge_width": 1.5,
            "base_font_size": 10,
            "node_border_color": "#FFFFFF",  # Белая обводка
            "hover_color": "#FF5722",
            "text_color": "#333333",
            "background_color": "#FFFFFF",
        }

        self.current_zoom = 1.0
        self.initUI()
        self.setWindowTitle("Graph4Py - Interactive Visualizer")
        self.setGeometry(100, 100, 1200, 800)

    def initUI(self):
        # Главный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Область визуализации графа
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground("w")
        self.plot_widget.setMouseEnabled(x=True, y=True)
        self.plot_widget.setLimits(xMin=-1000, xMax=1000, yMin=-1000, yMax=1000)
        self.plot_widget.sigRangeChanged.connect(self.handle_zoom)

        self.graph_item = GraphItem()
        self.plot_widget.addItem(self.graph_item)
        main_layout.addWidget(self.plot_widget, stretch=3)

        # Панель управления
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        control_panel.setMaximumWidth(300)
        main_layout.addWidget(control_panel)

        # Управление узлами
        self.setupNodeManagement(control_layout)
        # Управление рёбрами
        self.setupEdgeManagement(control_layout)
        # Работа с файлами
        self.setupFileOperations(control_layout)
        # Настройки визуализации
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

        # Кнопка сброса масштаба
        reset_zoom_btn = QPushButton("Reset Zoom")
        reset_zoom_btn.clicked.connect(self.reset_zoom)
        vis_layout.addWidget(reset_zoom_btn)

        layout.addWidget(vis_group)

    def handle_zoom(self, _, view_range):
        """Обработчик изменения масштаба"""
        x_range = view_range[0][1] - view_range[0][0]
        self.current_zoom = max(0.2, min(5.0, 100 / x_range))  # Ограничение масштаба
        self.update_graph()

    def reset_zoom(self):
        """Сброс масштаба к исходному"""
        self.plot_widget.setRange(xRange=[-10, 10], yRange=[-10, 10])
        self.current_zoom = 1.0
        self.update_graph()

    def update_node_dropdowns(self):
        """Обновление выпадающих списков узлов"""
        nodes = [str(node.id) for node in self.graph.node_list]
        self.edge_from.clear()
        self.edge_to.clear()
        self.edge_from.addItems(nodes)
        self.edge_to.addItems(nodes)

    def add_node(self):
        """Добавление нового узла"""
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
        """Удаление выбранного узла"""
        name = self.edge_from.currentText()
        if name in [str(node.id) for node in self.graph.node_list]:
            self.graph.remove_node(name)
            if name in self.node_positions:
                del self.node_positions[name]
            self.update_node_dropdowns()
            self.update_graph()

    def add_edge(self):
        """Добавление ребра между узлами"""
        from_node = self.edge_from.currentText()
        to_node = self.edge_to.currentText()
        weight = self.edge_weight.value()

        if from_node and to_node:
            self.graph.add_edge(from_node, to_node, weight)
            self.update_graph()

    def remove_edge(self):
        """Удаление ребра между узлами"""
        from_node = self.edge_from.currentText()
        to_node = self.edge_to.currentText()

        if from_node and to_node:
            self.graph.remove_edge(from_node, to_node)
            self.update_graph()

    def update_graph(self):
        """Обновление визуализации графа с правильным масштабированием"""
        # Получаем параметры визуализации
        params = self.visual_params
        nodes = self.graph.node_list
        if not nodes:
            return

        # Оптимизация: обновлять только изменившиеся узлы и рёбра
        node_ids = {str(node.id): idx for idx, node in enumerate(nodes)}
        edges = []
        for node in nodes:
            for edge in self.graph.get_edges(node.id):
                source_idx = node_ids.get(str(edge.source.id))
                target_idx = node_ids.get(str(edge.target.id))
                if source_idx is not None and target_idx is not None:
                    edges.append((source_idx, target_idx))

        # Проверка корректности узлов и рёбер
        valid_nodes = [node for node in nodes if str(node.id) in node_ids]
        if not valid_nodes:
            return

        # Отображение
        self.graph_item.setData(
            pos=np.array([self.node_positions[node.id] for node in valid_nodes]),
            adj=np.array(edges) if edges else None,
            size=params["base_pixel_size"] * self.current_zoom,
            symbolBrush=params["node_color"],
        )

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
