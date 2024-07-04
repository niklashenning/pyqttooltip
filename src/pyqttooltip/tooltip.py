from qtpy.QtWidgets import QWidget
from qtpy.QtCore import Qt, Signal, QMargins, QPoint
from qtpy.QtGui import QColor, QFont
from .tooltip_triangle import TooltipTriangle
from .enums import TooltipPlacement


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
        self.__duration = 0
        self.__placement = TooltipPlacement.AUTO
        self.__fallback_placement = []
        self.__triangle_enabled = True
        self.__triangle_size = 7
        self.__offset = QPoint(0, 0)
        self.__showing_delay = 250
        self.__hiding_delay = 250
        self.__fade_in_duration = 100
        self.__fade_out_duration = 100
        self.__text_centering_enabled = True
        self.__showing_on_disabled_widgets = False
        self.__border_radius = 0
        self.__border_width = 0
        self.__background_color = QColor('#000000')
        self.__text_color = QColor('#FFFFFF')
        self.__border_color = QColor('#403E41')
        self.__font = QFont('Arial', 9)
        self.__margins = QMargins(0, 0, 0, 0)

        # Widget settings
        self.setWindowFlags(Qt.WindowType.ToolTip |
                            Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Create tooltip body widget
        self.tooltip_body = QWidget(self)
        self.tooltip_body.setStyleSheet('background: #000000; '
                                        'border-radius: 3px; '
                                        'border: 1px solid #403E41;')   # TEMPORARY

        # Create tooltip triangle
        self.tooltip_triangle = TooltipTriangle(self)
        self.tooltip_triangle.move(40, 29)  # TEMPORARY

        # Install event filter on widget
        if self.__widget is not None:
            self.__widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched == self.__widget:
            # Mouse enters widget
            if event.type() == event.Type.HoverEnter:
                self.show()
                widget_pos = self.__widget.parent().mapToGlobal(self.__widget.pos())
                self.move(widget_pos.x(), widget_pos.y() - self.height())
            # Mouse leaves widget
            elif event.type() == event.Type.HoverLeave:
                self.hide()
        return False

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

    def getTriangleSize(self) -> int:
        pass

    def setTriangleSize(self, size: int):
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
