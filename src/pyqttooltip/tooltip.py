from qtpy.QtWidgets import QWidget
from qtpy.QtCore import Qt, Signal, QMargins, QPoint
from qtpy.QtGui import QColor, QFont
from .tooltip_interface import TooltipInterface
from .tooltip_triangle import TooltipTriangle
from .enums import TooltipPlacement


class Tooltip(TooltipInterface):

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
                                        'border: 0px solid #403E41;')   # TEMPORARY

        # Create tooltip triangle
        self.tooltip_triangle = TooltipTriangle(self)
        self.tooltip_triangle.move(40, self.tooltip_body.height() - self.__border_width)  # TEMPORARY

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
        return self.__widget

    def setWidget(self, widget: QWidget):
        self.__widget = widget

    def getText(self) -> str:
        return self.__text

    def setText(self, text: str):
        self.__text = text

    def getDuration(self) -> int:
        return self.__duration

    def setDuration(self, duration: int):
        self.__duration = duration

    def getPlacement(self) -> TooltipPlacement:
        return self.__placement

    def setPlacement(self, placement: TooltipPlacement):
        self.__placement = placement

    def getFallbackPlacement(self) -> list[TooltipPlacement]:
        return self.__fallback_placement

    def setFallbackPlacement(self, fallback_placement: list[TooltipPlacement]):
        self.__fallback_placement = fallback_placement

    def isTriangleEnabled(self) -> bool:
        return self.__triangle_enabled

    def setTriangleEnabled(self, enabled: bool):
        self.__triangle_enabled = enabled

    def getTriangleSize(self) -> int:
        return self.__triangle_size

    def setTriangleSize(self, size: int):
        self.__triangle_enabled = size

    def getOffset(self) -> QPoint:
        return self.__offset

    def setOffset(self, offset: QPoint):
        self.__offset = offset

    def getOffsetX(self) -> int:
        return self.__offset.x()

    def setOffsetX(self, offset: int):
        self.setOffset(QPoint(offset, self.__offset.y()))

    def getOffsetY(self) -> int:
        return self.__offset.y()

    def setOffsetY(self, offset: int):
        self.setOffset(QPoint(self.__offset.x(), offset))

    def getShowingDelay(self) -> int:
        return self.__showing_delay

    def setShowingDelay(self, delay: int):
        self.__showing_delay = delay

    def getHidingDelay(self) -> int:
        return self.__hiding_delay

    def setHidingDelay(self, delay: int):
        self.__hiding_delay = delay

    def getFadeInDuration(self) -> int:
        return self.__fade_in_duration

    def setFadeInDuration(self, duration: int):
        self.__fade_in_duration = duration

    def getFadeOutDuration(self) -> int:
        return self.__fade_out_duration

    def setFadeOutDuration(self, duration: int):
        self.__fade_in_duration = duration

    def isTextCenteringEnabled(self) -> int:
        return self.__text_centering_enabled

    def setTextCenteringEnabled(self, enabled: bool):
        self.__text_centering_enabled = enabled

    def isShowingOnDisabledWidgets(self) -> bool:
        return self.__showing_on_disabled_widgets

    def setShowingOnDisabledWidgets(self, enabled: bool):
        self.__showing_on_disabled_widgets = enabled

    def getBorderRadius(self) -> int:
        return self.__border_radius

    def setBorderRadius(self, border_radius: int):
        self.__border_radius = border_radius

    def getBorderWidth(self) -> int:
        return self.__border_width

    def setBorderWidth(self, width: int):
        self.__border_width = width

    def getBackgroundColor(self) -> QColor:
        return self.__background_color

    def setBackgroundColor(self, color: QColor):
        self.__background_color = color

    def getTextColor(self) -> QColor:
        return self.__text_color

    def setTextColor(self, color: QColor):
        self.__text_color = color

    def getBorderColor(self) -> QColor:
        return self.__border_color

    def setBorderColor(self, color: QColor):
        self.__border_color = color

    def getOpacity(self) -> float:
        return self.windowOpacity()

    def setOpacity(self, opacity: float):
        self.setWindowOpacity(opacity)

    def font(self) -> QFont:
        return self.getFont()

    def getFont(self) -> QFont:
        return self.__font

    def setFont(self, font: QFont):
        self.__font = font

    def getMargins(self) -> QMargins:
        return self.__margins

    def setMargins(self, margins: QMargins):
        self.__margins = margins

    def setMarginLeft(self, margin: int):
        self.__margins.setLeft(margin)

    def setMarginTop(self, margin: int):
        self.__margins.setTop(margin)

    def setMarginRight(self, margin: int):
        self.__margins.setRight(margin)

    def setMarginBottom(self, margin: int):
        self.__margins.setBottom(margin)
