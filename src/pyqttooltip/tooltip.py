from qtpy.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect
from qtpy.QtCore import Qt, Signal, QMargins, QPoint, QTimer, QPropertyAnimation, QEasingCurve
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
        self.__triangle_enabled = True
        self.__triangle_size = 7
        self.__offset = QPoint(0, 0)
        self.__show_delay = 250
        self.__hide_delay = 250
        self.__fade_in_duration = 100
        self.__fade_out_duration = 100
        self.__fade_in_easing_curve = QEasingCurve.Type.Linear
        self.__fade_out_easing_curve = QEasingCurve.Type.Linear
        self.__text_centering_enabled = True
        self.__showing_on_disabled_widgets = False
        self.__border_radius = 0
        self.__border_width = 0
        self.__background_color = QColor('#000000')
        self.__text_color = QColor('#FFFFFF')
        self.__border_color = QColor('#403E41')
        self.__font = QFont('Arial', 9)
        self.__margins = QMargins(10, 5, 10, 5)

        self.__current_opacity = 0.0

        # Widget settings
        self.setWindowFlags(Qt.WindowType.ToolTip |
                            Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Opacity effect for fading animations
        self.__opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.__opacity_effect)

        # Create tooltip body widget
        self.__tooltip_body = QWidget(self)

        # Create triangle widget
        self.__triangle_widget = TooltipTriangle(self)

        # Create text widget
        self.__text_widget = QLabel(self)
        self.__text_widget.setText(text)

        # Install event filter on widget
        if self.__widget is not None:
            self.__widget.installEventFilter(self)

        # Init delay timers
        self.__show_delay_timer = QTimer(self)
        self.__show_delay_timer.setInterval(self.__show_delay)
        self.__show_delay_timer.setSingleShot(True)
        self.__show_delay_timer.timeout.connect(self.__start_fade_in)

        self.__hide_delay_timer = QTimer(self)
        self.__hide_delay_timer.setInterval(self.__hide_delay)
        self.__hide_delay_timer.setSingleShot(True)
        self.__hide_delay_timer.timeout.connect(self.__start_fade_out)

        # Init fade animations
        self.__fade_in_animation = QPropertyAnimation(self.__opacity_effect, b'opacity')
        self.__fade_in_animation.setDuration(self.__fade_in_duration)
        self.__fade_in_animation.setEasingCurve(self.__fade_in_easing_curve)
        self.__fade_in_animation.valueChanged.connect(self.__fade_animation_value_changed)

        self.__fade_out_animation = QPropertyAnimation(self.__opacity_effect, b'opacity')
        self.__fade_out_animation.setDuration(self.__fade_out_duration)
        self.__fade_out_animation.setEasingCurve(self.__fade_out_easing_curve)
        self.__fade_out_animation.valueChanged.connect(self.__fade_animation_value_changed)
        self.__fade_out_animation.finished.connect(self.__hide)
        self.__fade_out_animation.start()

    def eventFilter(self, watched, event):
        if watched == self.__widget:
            # Mouse enters widget
            if event.type() == event.Type.HoverEnter:
                self.show()
            # Mouse leaves widget
            elif event.type() == event.Type.HoverLeave:
                self.hide()
        return False

    def getWidget(self) -> QWidget:
        return self.__widget

    def setWidget(self, widget: QWidget):
        # TODO: uninstall and reinstall event filter
        self.__widget = widget

    def getText(self) -> str:
        return self.__text

    def setText(self, text: str):
        self.__text = text
        self.__text_widget.setText(text)

    def getDuration(self) -> int:
        return self.__duration

    def setDuration(self, duration: int):
        self.__duration = duration

    def getPlacement(self) -> TooltipPlacement:
        return self.__placement

    def setPlacement(self, placement: TooltipPlacement):
        self.__placement = placement

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

    def getShowDelay(self) -> int:
        return self.__show_delay

    def setShowDelay(self, delay: int):
        self.__show_delay = delay
        self.__show_delay_timer.setInterval(delay)

    def getHideDelay(self) -> int:
        return self.__hide_delay

    def setHideDelay(self, delay: int):
        self.__hide_delay = delay
        self.__hide_delay_timer.setInterval(delay)

    def getFadeInDuration(self) -> int:
        return self.__fade_in_duration

    def setFadeInDuration(self, duration: int):
        self.__fade_in_duration = duration
        self.__fade_in_animation.setDuration(duration)

    def getFadeOutDuration(self) -> int:
        return self.__fade_out_duration

    def setFadeOutDuration(self, duration: int):
        self.__fade_in_duration = duration
        self.__fade_out_animation.setDuration(duration)

    def getFadeInEasingCurve(self) -> QEasingCurve.Type:
        return self.__fade_out_easing_curve

    def setFadeInEasingCurve(self, easing_curve: QEasingCurve.Type | None):
        if easing_curve is None:
            easing_curve = QEasingCurve.Type.Linear

        self.__fade_in_easing_curve = easing_curve
        self.__fade_in_animation.setEasingCurve(easing_curve)

    def getFadeOutEasingCurve(self) -> QEasingCurve.Type:
        return self.__fade_out_easing_curve

    def setFadeOutEasingCurve(self, easing_curve: QEasingCurve.Type | None):
        if easing_curve is None:
            easing_curve = QEasingCurve.Type.Linear

        self.__fade_out_easing_curve = easing_curve
        self.__fade_out_animation.setEasingCurve(easing_curve)

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

    def show(self):
        self.__update_ui()
        self.__start_show_delay()

    def hide(self):
        self.__start_hide_delay()

    def update(self):
        self.__update_ui()
        super().update()

    def __start_show_delay(self):
        self.__hide_delay_timer.stop()
        self.__show_delay_timer.start()

    def __start_fade_in(self):
        self.__fade_in_animation.setStartValue(self.__current_opacity)
        self.__fade_in_animation.setEndValue(1)
        self.__fade_in_animation.start()
        super().show()

    def __start_hide_delay(self):
        self.__show_delay_timer.stop()
        self.__hide_delay_timer.start()

    def __start_fade_out(self):
        self.__fade_out_animation.setStartValue(self.__current_opacity)
        self.__fade_out_animation.setEndValue(0)
        self.__fade_out_animation.start()

    def __hide(self):
        super().hide()

    def __fade_animation_value_changed(self, value):
        self.__current_opacity = value

    def __update_stylesheet(self):
        self.__tooltip_body.setStyleSheet('background: {}; '
                                          'border-radius: {}px; '
                                          'border: {}px solid {};'
                                          .format(self.__background_color.name(),
                                                  self.__border_radius,
                                                  self.__border_width,
                                                  self.__border_color.name()))

        self.__text_widget.setStyleSheet('color: {}'.format(self.__text_color.name()))

    def __update_ui(self):
        self.__update_stylesheet()
        self.__triangle_widget.update()

        font_metrics = self.__text_widget.fontMetrics()
        bounding_rect = font_metrics.boundingRect(self.__text)
        text_width = bounding_rect.width() + 3
        text_height = bounding_rect.height()
        self.__text_widget.setFixedSize(text_width, text_height)
        self.__text_widget.move(self.__margins.left(), self.__margins.top())

        body_width = self.__margins.left() + text_width + self.__margins.right()
        body_height = self.__margins.top() + text_height + self.__margins.bottom()
        self.__tooltip_body.setFixedSize(body_width, body_height)

        width = body_width
        height = body_height + self.__triangle_widget.height() - self.__border_width
        self.setFixedSize(width, height)

        widget_pos = self.__widget.parent().mapToGlobal(self.__widget.pos())
        tooltip_pos_x = widget_pos.x() + int(self.__widget.width() / 2) - int(width / 2)
        tooltip_pos_y = widget_pos.y() - height
        self.move(tooltip_pos_x, tooltip_pos_y)

        tooltip_triangle_pos_x = int(width / 2) - self.__triangle_size
        tooltip_triangle_pos_y = self.__tooltip_body.height() - self.__border_width
        self.__triangle_widget.move(tooltip_triangle_pos_x, tooltip_triangle_pos_y)
