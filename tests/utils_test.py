from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton
from src.pyqttooltip.utils import Utils


def test_get_top_level_parent(qtbot):
    """Test getting the top level parent of a widget"""

    window = QMainWindow()
    widget = QWidget(window)
    button1 = QPushButton(widget)
    button2 = QPushButton()

    assert Utils.get_top_level_parent(button1) == window
    assert Utils.get_top_level_parent(button2) == button2


def test_get_parents(qtbot):
    """Test getting all the parents of a widget"""

    window = QMainWindow()
    widget = QWidget(window)
    button1 = QPushButton(widget)
    button2 = QPushButton()

    assert Utils.get_parents(button1) == [widget, window]
    assert Utils.get_parents(button2) == []
