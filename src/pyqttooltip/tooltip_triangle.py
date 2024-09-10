import math
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QPainter, QPen, QPainterPath, QTransform
from qtpy.QtCore import Qt, QPoint
from .tooltip_interface import TooltipInterface
from .enums import TooltipPlacement


class TooltipTriangle(QWidget):

    def __init__(self, tooltip: TooltipInterface):
        """Create a new TooltipTriangle instance

        :param tooltip: tooltip the triangle belongs to
        """

        super(TooltipTriangle, self).__init__(tooltip)

        self.tooltip = tooltip

    def paintEvent(self, event):
        if not self.tooltip.isTriangleEnabled():
            return

        if self.tooltip.getActualPlacement() is None:
            return

        # Get parameters
        size = self.tooltip.getTriangleSize()
        actual_placement = self.tooltip.getActualPlacement()
        background_color = self.tooltip.getBackgroundColor()
        border_color = self.tooltip.getBorderColor()
        border_width = self.tooltip.getBorderWidth()

        # Init painter
        painter = QPainter()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.begin(self)

        # Rotate widget by 180° depending on placement
        if actual_placement == TooltipPlacement.RIGHT:
            transform = QTransform()
            transform.translate(self.width() / 2 - 0.5, self.height() / 2)
            transform.rotate(180)
            transform.translate(-self.width() / 2, -self.height() / 2)
            painter.setTransform(transform)
        if actual_placement == TooltipPlacement.BOTTOM:
            transform = QTransform()
            if border_width == 1:
                transform.translate(self.width() / 2 + 0.25, self.height() / 2 - 0.5)
            else:
                transform.translate(self.width() / 2, self.height() / 2)
            transform.rotate(180)
            transform.translate(-self.width() / 2, -self.height() / 2)
            painter.setTransform(transform)

        # Draw triangle shape
        path = QPainterPath()

        if actual_placement == TooltipPlacement.BOTTOM or actual_placement == TooltipPlacement.TOP:
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

        elif actual_placement == TooltipPlacement.LEFT or actual_placement == TooltipPlacement.RIGHT:
            path.moveTo(0, 0)
            path.lineTo(size, size)
            path.lineTo(0, size * 2)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(background_color)
            painter.drawPath(path)

            if border_width > 0:
                painter.setPen(QPen(border_color, border_width))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawLine(QPoint(0, 0), QPoint(size, size))
                painter.drawLine(QPoint(0, size * 2), QPoint(size, size))

        painter.end()

    def update(self):
        # Get parameters
        enabled = self.tooltip.isTriangleEnabled()
        size = self.tooltip.getTriangleSize()
        actual_placement = self.tooltip.getActualPlacement()
        border_width = self.tooltip.getBorderWidth()

        # Resize depending on parameters
        if enabled:
            if actual_placement == TooltipPlacement.BOTTOM or actual_placement == TooltipPlacement.TOP:
                self.resize(size * 2, size + math.ceil(border_width / 2))
            elif actual_placement == TooltipPlacement.LEFT or actual_placement == TooltipPlacement.RIGHT:
                self.resize(size + math.ceil(border_width / 2), size * 2)
        else:
            self.resize(0, 0)

        # Fire paint event
        super().update()
