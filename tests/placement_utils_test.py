from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtCore import QPoint, QSize
from src.pyqttooltip import TooltipPlacement
from src.pyqttooltip.placement_utils import PlacementUtils


def test_get_optimal_placement(qtbot):
    """Test getting the optimal placement"""

    window = QMainWindow()
    button = QPushButton(window)
    offsets = {
        TooltipPlacement.LEFT:   QPoint(0, 0),
        TooltipPlacement.RIGHT:  QPoint(0, 0),
        TooltipPlacement.TOP:    QPoint(0, 0),
        TooltipPlacement.BOTTOM: QPoint(0, 0)
    }
    qtbot.addWidget(window)
    qtbot.addWidget(button)

    # Left placement
    window.setFixedSize(500, 250)
    button.move(400, 100)
    placement = PlacementUtils.get_optimal_placement(button, QSize(100, 30), 5, offsets)
    assert placement == TooltipPlacement.LEFT

    # Right placement
    button.move(0, 100)
    placement = PlacementUtils.get_optimal_placement(button, QSize(100, 30), 5, offsets)
    assert placement == TooltipPlacement.RIGHT

    # Top placement
    button.move(250, 250)
    placement = PlacementUtils.get_optimal_placement(button, QSize(100, 30), 5, offsets)
    assert placement == TooltipPlacement.TOP

    # Bottom placement
    button.move(250, 0)
    placement = PlacementUtils.get_optimal_placement(button, QSize(100, 30), 5, offsets)
    assert placement == TooltipPlacement.BOTTOM


def test_get_fallback_placement(qtbot):
    """Test getting a fallback placement"""

    window = QMainWindow()
    button = QPushButton(window)
    offsets = {
        TooltipPlacement.LEFT:   QPoint(0, 0),
        TooltipPlacement.RIGHT:  QPoint(0, 0),
        TooltipPlacement.TOP:    QPoint(0, 0),
        TooltipPlacement.BOTTOM: QPoint(0, 0)
    }
    qtbot.addWidget(window)
    qtbot.addWidget(button)

    # Primary placement left -> fallback placement right
    button.move(0, 15)
    fallback_placement = PlacementUtils.get_fallback_placement(
        button, TooltipPlacement.LEFT,
        [TooltipPlacement.TOP, TooltipPlacement.RIGHT, TooltipPlacement.BOTTOM],
        QSize(50, 20), 5, offsets
    )
    assert fallback_placement == TooltipPlacement.RIGHT

    # Primary placement left -> fallback placement bottom
    fallback_placement = PlacementUtils.get_fallback_placement(
        button, TooltipPlacement.LEFT,
        [TooltipPlacement.TOP, TooltipPlacement.BOTTOM],
        QSize(50, 20), 5, offsets
    )
    assert fallback_placement == TooltipPlacement.BOTTOM

    # Primary placement left -> fallback placement top
    button.move(0, 50)
    fallback_placement = PlacementUtils.get_fallback_placement(
        button, TooltipPlacement.LEFT,
        [TooltipPlacement.TOP, TooltipPlacement.RIGHT, TooltipPlacement.BOTTOM],
        QSize(50, 20), 5, offsets
    )
    assert fallback_placement == TooltipPlacement.TOP

    # Primary placement left -> fallback placement None
    button.move(100, 15)
    fallback_placement = PlacementUtils.get_fallback_placement(
        button, TooltipPlacement.LEFT,
        [TooltipPlacement.TOP, TooltipPlacement.RIGHT, TooltipPlacement.BOTTOM],
        QSize(50, 20), 5, offsets
    )
    assert fallback_placement is None
