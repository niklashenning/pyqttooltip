from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QPainter
from qtpy.QtCore import QPoint, QEvent
from .tooltip_interface import TooltipInterface
from .enums import TooltipPlacement


class TooltipTriangle(QWidget):

    def __init__(self, tooltip: TooltipInterface):
        """Create a new TooltipTriangle instance

        :param tooltip: tooltip the triangle belongs to
        """

        super(TooltipTriangle, self).__init__(tooltip)

        self.tooltip = tooltip

    def paintEvent(self, event: QEvent):
        """Paint event that paints the triangle based on the current
        settings of the tooltip

        :param event: event that is received
        """

        # Ignore if triangle is disabled or actual placement not yet set
        if not self.tooltip.isTriangleEnabled():
            return

        if self.tooltip.getActualPlacement() is None:
            return

        # Get parameters
        size = self.tooltip.getTriangleSize()
        actual_placement = self.tooltip.getActualPlacement()
        background_color = self.tooltip.getBackgroundColor()
        border_color = self.tooltip.getBorderColor()
        border_enabled = self.tooltip.isBorderEnabled()
        border_width = 1 if border_enabled else 0

        # Init painter
        painter = QPainter()
        painter.begin(self)
        painter.setPen(border_color if border_enabled else background_color)

        # Draw triangle shape depending on tooltip placement
        if actual_placement == TooltipPlacement.RIGHT:
            start = QPoint(0, size - 1)
            painter.drawPoint(start)

            for i in range(1, size + border_width):
                painter.setPen(background_color)
                painter.drawLine(
                    QPoint(start.x() + i, start.y() - i), QPoint(start.x() + i, start.y() + i)
                )
                if border_width > 0:
                    painter.setPen(border_color)
                    painter.drawPoint(start.x() + i, start.y() - i)
                    painter.drawPoint(start.x() + i, start.y() + i)

        elif actual_placement == TooltipPlacement.LEFT:
            start = QPoint(size - 1 + border_width, size - 1)
            painter.drawPoint(start)

            for i in range(1, size + border_width):
                painter.setPen(background_color)
                painter.drawLine(
                    QPoint(start.x() - i, start.y() - i), QPoint(start.x() - i, start.y() + i)
                )
                if border_width > 0:
                    painter.setPen(border_color)
                    painter.drawPoint(start.x() - i, start.y() - i)
                    painter.drawPoint(start.x() - i, start.y() + i)

        elif actual_placement == TooltipPlacement.TOP:
            start = QPoint(size - 1, size - 1 + border_width)
            painter.drawPoint(start)

            for i in range(1, size + border_width):
                painter.setPen(background_color)
                painter.drawLine(
                    QPoint(start.x() - i, start.y() - i), QPoint(start.x() + i, start.y() - i)
                )
                if border_width > 0:
                    painter.setPen(border_color)
                    painter.drawPoint(start.x() - i, start.y() - i)
                    painter.drawPoint(start.x() + i, start.y() - i)

        elif actual_placement == TooltipPlacement.BOTTOM:
            start = QPoint(size - 1, 0)
            painter.drawPoint(start)

            for i in range(1, size + border_width):
                painter.setPen(background_color)
                painter.drawLine(
                    QPoint(start.x() - i, start.y() + i), QPoint(start.x() + i, start.y() + i)
                )
                if border_width > 0:
                    painter.setPen(border_color)
                    painter.drawPoint(start.x() - i, start.y() + i)
                    painter.drawPoint(start.x() + i, start.y() + i)

        painter.end()

    def update(self):
        """Update the size of the triangle and call the paint event"""

        # Get parameters
        enabled = self.tooltip.isTriangleEnabled()
        size = self.tooltip.getTriangleSize()
        actual_placement = self.tooltip.getActualPlacement()
        border_width = 1 if self.tooltip.isBorderEnabled() > 0 else 0

        # Resize depending on placement
        if enabled:
            if actual_placement == TooltipPlacement.BOTTOM or actual_placement == TooltipPlacement.TOP:
                self.resize(size * 2 - 1, size + border_width)
            elif actual_placement == TooltipPlacement.LEFT or actual_placement == TooltipPlacement.RIGHT:
                self.resize(size + border_width, size * 2 - 1)
        else:
            self.resize(0, 0)

        # Fire paint event
        super().update()
