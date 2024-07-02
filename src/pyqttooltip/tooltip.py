from qtpy.QtWidgets import QWidget
from qtpy.QtCore import Qt, Signal, QMargins, QPoint, QSize
from qtpy.QtGui import QColor, QFont
from .enums import TooltipPlacement, TooltipTrigger


class Tooltip(QWidget):

    # Signals
    shown = Signal()
    hidden = Signal()

    def __init__(self, widget: QWidget = None, text: str = ''):
        """Create a new Tooltip instance

        :param widget: widget to show the tooltip for
        :param text: text that will be displayed on the tooltip
        """

        super(Tooltip, self).__init__(None)

        # Init attributes
        self.__widget = widget
        self.__text = text
        self.__placement = TooltipPlacement.AUTO
        self.__fallback_placement = []
        self.__triangle_enabled = True
        self.__trigger = TooltipTrigger.HOVER
        self.__offset = QPoint(0, 0)
        self.__showing_delay = 250
        self.__hiding_delay = 250
        self.__fade_in_duration = 100
        self.__fade_out_duration = 100
        self.__text_centering_enabled = True
        self.__showing_on_disabled_widgets = False
        self.__border_radius = 0
        self.__background_color = QColor('#000000')
        self.__text_color = QColor('#FFFFFF')
        self.__font = QFont('Arial', 9)
        self.__margins = QMargins(0, 0, 0, 0)

        # Window settings
        self.setWindowFlags(Qt.WindowType.ToolTip |
                            Qt.WindowType.CustomizeWindowHint |
                            Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def getWidget(self) -> QWidget:
        pass

    def setWidget(self, widget: QWidget):
        pass

    def getText(self) -> str:
        pass

    def setText(self, text: str):
        pass

    def getPlacement(self) -> TooltipPlacement:
        pass

    def setPlacement(self, placement: TooltipPlacement):
        pass

    def getFallbackPlacement(self) -> list[TooltipPlacement]:
        pass

    def setFallbackPlacement(self, fallback_placement: list[TooltipPlacement]):
        pass

    def isTriangleEnabled(self) -> bool:
        pass

    def setTriangleEnabled(self, enabled: bool):
        pass

    def getTrigger(self) -> TooltipTrigger:
        pass

    def setTrigger(self, trigger: TooltipTrigger):
        pass

    def getOffset(self) -> QPoint:
        pass

    def setOffset(self, offset_x: int, offset_y: int):
        pass

    def getOffsetX(self) -> int:
        pass

    def setOffsetX(self, offset: int):
        pass

    def getOffsetY(self) -> int:
        pass

    def setOffsetY(self, offset: int):
        pass

    def getShowingDelay(self) -> int:
        pass

    def setShowingDelay(self, delay: int):
        pass

    def getHidingDelay(self) -> int:
        pass

    def setHidingDelay(self, delay: int):
        pass

    def getFadeInDuration(self) -> int:
        pass

    def setFadeInDuration(self, duration: int):
        pass

    def getFadeOutDuration(self) -> int:
        pass

    def setFadeOutDuration(self, duration: int):
        pass

    def isTextCenteringEnabled(self) -> int:
        pass

    def setTextCenteringEnabled(self, enabled: bool):
        pass

    def isShowOnDisabledWidgets(self) -> bool:
        pass

    def setShowOnDisabledWidgets(self, enabled: bool):
        pass

    def getBorderRadius(self) -> int:
        pass

    def setBorderRadius(self, border_radius: int):
        pass

    def getOpacity(self) -> float:
        pass

    def setOpacity(self, opacity: float):
        pass

    def getBackgroundColor(self) -> QColor:
        pass

    def setBackgroundColor(self, color: QColor):
        pass

    def getTextColor(self) -> QColor:
        pass

    def setTextColor(self, color: QColor):
        pass

    def font(self) -> QFont:
        pass

    def getFont(self) -> QFont:
        pass

    def setFont(self, font: QFont):
        pass

    def getMargins(self) -> QMargins:
        pass

    def setMargins(self, margins: QMargins):
        pass

    def setMarginLeft(self, margin: int):
        pass

    def setMarginTop(self, margin: int):
        pass

    def setMarginRight(self, margin: int):
        pass

    def setMarginBottom(self, margin: int):
        pass

    def setFixedSize(self, size: QSize):
        pass

    def setFixedWidth(self, width: int):
        pass

    def setFixedHeight(self, height: int):
        pass

    def setMinimumWidth(self, minimum_width: int):
        pass

    def setMaximumWidth(self, maximum_width: int):
        pass

    def setMinimumHeight(self, minimum_height: int):
        pass

    def setMaximumHeight(self, maximum_height: int):
        pass
