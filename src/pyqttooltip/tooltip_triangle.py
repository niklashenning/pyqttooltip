import math
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QPainter, QPen, QPainterPath
from qtpy.QtCore import Qt, QPoint
from .tooltip_interface import TooltipInterface


class TooltipTriangle(QWidget):

    def __init__(self, tooltip: TooltipInterface):
        """Create a new TooltipTriangle instance

        :param tooltip: tooltip the triangle belongs to
        """

        super(TooltipTriangle, self).__init__(tooltip)

        self.tooltip = tooltip
        self.update()

    def paintEvent(self, event):
        size = self.tooltip.getTriangleSize()
        background_color = self.tooltip.getBackgroundColor()
        border_color = self.tooltip.getBorderColor()
        border_width = self.tooltip.getBorderWidth()

        painter = QPainter()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.begin(self)

        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(size, size)
        path.lineTo(size * 2, 0)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(background_color)
        painter.drawPath(path)

        if border_width > 0:
            painter.setPen(QPen(border_color, border_width))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawLine(QPoint(0, 0), QPoint(size, size))
            painter.drawLine(QPoint(size * 2, 0), QPoint(size, size))

        painter.end()

    def update(self):
        size = self.tooltip.getTriangleSize()
        border_width = self.tooltip.getBorderWidth()
        self.setFixedSize(size * 2, size + math.ceil(border_width / 2))
        super().update()
