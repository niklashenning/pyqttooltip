from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QColor
from .enums import TooltipPlacement


class TooltipInterface(QWidget):

    def isTriangleEnabled(self) -> bool:
        pass

    def getTriangleSize(self) -> int:
        pass

    def getPlacement(self) -> TooltipPlacement:
        pass

    def getBorderWidth(self) -> int:
        pass

    def getBackgroundColor(self) -> QColor:
        pass

    def getBorderColor(self) -> QColor:
        pass
