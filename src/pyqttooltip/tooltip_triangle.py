from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QColor, QPainter, QBrush, QPen, QPainterPath


class TooltipTriangle(QWidget):

    def __init__(self, parent: QWidget):
        """Create a new TooltipTriangle instance

        :param parent: parent of the widget
        """

        super(TooltipTriangle, self).__init__(parent)

        self.size = 7
        self.background_color = QColor('#000000')
        self.border_color = QColor('#403E41')
        self.border_width = 1

        self.setFixedSize(self.size * 2, self.size + 1)

    def paintEvent(self, event):
        painter = QPainter()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.begin(self)

        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(self.size, self.size)
        path.lineTo(self.size * 2, 0)

        painter.setPen(QPen(self.border_color))
        painter.setBrush(QBrush(self.background_color))
        painter.drawPath(path)

        painter.end()
