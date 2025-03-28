from node import Node


def test_node_initialization():
    node = Node(1, {"color": "red"})
    assert node.id == 1
    assert node.data == {"color": "red"}
    assert node.position is None


def test_node_default_data():
    node = Node("A")
    assert node.id == "A"
    assert node.data == {}


def test_node_str():
    node = Node(5)
    assert str(node) == "5"


def test_node_repr():
    node = Node("B", {"size": 10})
    assert repr(node) == "Node(id=B, data={'size': 10})"


def test_node_equality():
    node1 = Node(3)
    node2 = Node(3)
    node3 = Node(4)
    assert node1 == node2
    assert node1 != node3
    assert node1 == 3


def test_node_hash():
    node1 = Node("X")
    node2 = Node("X")
    node3 = Node("Y")
    assert hash(node1) == hash(node2)
    assert hash(node1) != hash(node3)


def test_update_position():
    node = Node(10)
    node.update_position(5.5, 7.2)
    assert node.position == (5.5, 7.2)
