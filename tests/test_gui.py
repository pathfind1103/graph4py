import json

import numpy as np
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QPushButton
from unittest.mock import patch
from gui import GraphVisualizer  # Замените your_module на имя вашего файла


@pytest.fixture
def app(qtbot):
    """Фикстура для создания и управления приложением."""
    test_app = GraphVisualizer()
    qtbot.addWidget(test_app)
    return test_app


def test_initial_state(app):
    """Тест начального состояния интерфейса."""
    assert app.graph.node_list == []
    assert app.edge_from.count() == 0
    assert app.edge_to.count() == 0
    assert app.node_name_input.text() == ""


def test_add_node(qtbot, app):
    """Тест добавления узла."""
    with patch("PyQt6.QtWidgets.QMessageBox.warning") as mock_warning:
        # Вводим имя узла и нажимаем кнопку
        qtbot.keyClicks(app.node_name_input, "TestNode")
        add_button = [btn for btn in app.findChildren(QPushButton) if btn.text() == "Add Node"][0]
        qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)

        # Явно обрабатываем event loop
        qtbot.waitUntil(lambda: len(app.graph.node_list) == 1, timeout=2000)

        # Проверяем результат
        assert "TestNode" in [str(node.id) for node in app.graph.node_list]
        assert app.edge_from.count() == 1
        mock_warning.assert_not_called()  # Проверяем, что warning не вызывался


def test_add_node_duplicate(qtbot, app):
    """Тест добавления дубликата узла."""
    # Находим кнопку по тексту
    add_buttons = [btn for btn in app.findChildren(QPushButton) if btn.text() == "Add Node"]
    assert len(add_buttons) == 1
    add_button = add_buttons[0]

    # Первое добавление узла
    qtbot.keyClicks(app.node_name_input, "TestNode")
    qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: len(app.graph.node_list) == 1, timeout=1000)

    # Второе добавление того же узла
    qtbot.keyClicks(app.node_name_input, "TestNode")

    with patch("PyQt6.QtWidgets.QMessageBox.warning") as mock_warning:
        # Настраиваем mock перед вызовом
        mock_warning.return_value = QMessageBox.StandardButton.Ok

        qtbot.mouseClick(add_button, Qt.MouseButton.LeftButton)
        qtbot.wait(100)  # Даем время на обработку

        # Проверяем вызов warning
        mock_warning.assert_called_once()
        args, _ = mock_warning.call_args
        assert "must be unique" in args[2]  # Проверяем текст сообщения


def test_add_edge(qtbot, app):
    """Тест добавления ребра."""
    # Добавляем узлы с позициями
    app.graph.add_node("A")
    app.graph.add_node("B")
    app.node_positions["A"] = np.random.rand(2) * 10
    app.node_positions["B"] = np.random.rand(2) * 10
    app.update_node_dropdowns()

    # Находим кнопку
    add_edge_btn = [btn for btn in app.findChildren(QPushButton) if btn.text() == "Add Edge"][0]

    # Устанавливаем выбор в комбобоксах
    app.edge_from.setCurrentIndex(0)
    app.edge_to.setCurrentIndex(1)

    # Добавляем ребро
    with patch("PyQt6.QtWidgets.QMessageBox.warning"):
        qtbot.mouseClick(add_edge_btn, Qt.MouseButton.LeftButton)
        qtbot.wait(200)  # Даем время на обработку

        # Проверяем результат
        edges_a = app.graph.get_edges("A")
        edges_b = app.graph.get_edges("B")

        if app.graph.directed:
            assert len(edges_a) == 1
            assert edges_a[0].target.id == "B"
            assert len(edges_b) == 0
        else:
            assert len(edges_a) == 1
            assert len(edges_b) == 1
            assert edges_a[0].target.id == "B"
            assert edges_b[0].target.id == "A"


def test_save_load_graph(qtbot, app, tmp_path, mocker):
    """Тест сохранения и загрузки графа."""
    # Добавляем тестовые данные
    app.graph.add_node("A")
    app.graph.add_node("B")
    app.node_positions["A"] = [1.0, 2.0]
    app.node_positions["B"] = [3.0, 4.0]
    app.graph.add_edge("A", "B", 1.5)
    app.update_node_dropdowns()
    app.update_graph()

    # Находим кнопки
    save_btn = next(btn for btn in app.findChildren(QPushButton) if btn.text() == "Save Graph")

    # 1. Тестируем сохранение
    test_file = tmp_path / "test_graph.json"

    # Мокаем все вызовы внутри save_graph
    mocker.patch("PyQt6.QtWidgets.QFileDialog.getSaveFileName", return_value=(str(test_file), ""))
    mocker.patch("PyQt6.QtWidgets.QMessageBox.information")

    # Вызываем сохранение
    qtbot.mouseClick(save_btn, Qt.MouseButton.LeftButton)
    qtbot.wait(500)  # Даем время на выполнение

    # Проверяем, что файл создан
    assert test_file.exists(), "Файл не был создан"

    # Проверяем содержимое файла
    with open(test_file, "r") as f:
        data = json.load(f)
        assert "A" in data["nodes"]
        assert "B" in data["nodes"]
        assert data["edges"][0]["source"] == "A"
        assert data["edges"][0]["target"] == "B"

    # 2. Тестируем загрузку
    new_app = GraphVisualizer()
    qtbot.addWidget(new_app)

    # Находим кнопку загрузки в новом окне
    new_load_btn = next(
        btn for btn in new_app.findChildren(QPushButton) if btn.text() == "Load Graph"
    )

    # Мокаем диалог загрузки
    mocker.patch("PyQt6.QtWidgets.QFileDialog.getOpenFileName", return_value=(str(test_file), ""))
    mocker.patch("PyQt6.QtWidgets.QMessageBox.information")

    # Вызываем загрузку
    qtbot.mouseClick(new_load_btn, Qt.MouseButton.LeftButton)
    qtbot.wait(500)  # Даем время на выполнение

    # Проверяем загруженные данные
    assert len(new_app.graph.node_list) == 2
    assert "A" in [node.id for node in new_app.graph.node_list]
    assert "B" in [node.id for node in new_app.graph.node_list]
    assert new_app.node_positions["A"] == [1.0, 2.0]
    assert new_app.node_positions["B"] == [3.0, 4.0]
    assert len(new_app.graph.get_edges("A")) == 1

    # Закрываем второе окно
    new_app.close()


def test_zoom_handling(qtbot, app):
    """Тест обработки масштабирования."""
    # Добавляем тестовые данные с позициями
    app.graph.add_node("A")
    app.graph.add_node("B")
    app.node_positions["A"] = np.random.rand(2) * 10
    app.node_positions["B"] = np.random.rand(2) * 10

    initial_zoom = app.current_zoom

    # Эмулируем изменение масштаба
    app.handle_zoom(None, [[-5, 5], [-5, 5]])
    qtbot.wait(100)
    assert app.current_zoom != initial_zoom

    # Находим кнопку сброса
    reset_btn = [btn for btn in app.findChildren(QPushButton) if btn.text() == "Reset Zoom"][0]

    # Тест сброса масштаба
    qtbot.mouseClick(reset_btn, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: app.current_zoom == 1.0, timeout=1000)


def test_remove_node(qtbot, app):
    """Тест удаления узла."""
    # Добавляем узел
    app.graph.add_node("A")
    app.update_node_dropdowns()

    # Находим кнопки
    remove_btn = [
        btn for btn in app.findChildren(QPushButton) if btn.text() == "Remove Selected Node"
    ][0]

    # Ждем обновления интерфейса
    qtbot.waitUntil(lambda: app.edge_from.count() == 1, timeout=1000)

    # Удаляем узел
    with patch("PyQt6.QtWidgets.QMessageBox.question", return_value=QMessageBox.StandardButton.Yes):
        qtbot.mouseClick(remove_btn, Qt.MouseButton.LeftButton)
        qtbot.waitUntil(lambda: len(app.graph.node_list) == 0, timeout=1000)

    assert app.edge_from.count() == 0
