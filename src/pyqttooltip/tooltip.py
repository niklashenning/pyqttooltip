import math
from qtpy.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect, QWIDGETSIZE_MAX
from qtpy.QtCore import (Qt, Signal, QMargins, QPoint, QSize, QTimer,
                         QPropertyAnimation, QEasingCurve, QEvent, QObject)
from qtpy.QtGui import QColor, QFont
from .tooltip_interface import TooltipInterface
from .tooltip_triangle import TooltipTriangle
from .enums import TooltipPlacement
from .placement_utils import PlacementUtils
from .utils import Utils


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
        self.__fallback_placements = []
        self.__triangle_enabled = True
        self.__triangle_size = 5
        self.__offsets = {
            TooltipPlacement.LEFT:   QPoint(0, 0),
            TooltipPlacement.RIGHT:  QPoint(0, 0),
            TooltipPlacement.TOP:    QPoint(0, 0),
            TooltipPlacement.BOTTOM: QPoint(0, 0)
        }
        self.__show_delay = 50
        self.__hide_delay = 50
        self.__fade_in_duration = 150
        self.__fade_out_duration = 150
        self.__fade_in_easing_curve = QEasingCurve.Type.Linear
        self.__fade_out_easing_curve = QEasingCurve.Type.Linear
        self.__text_centering_enabled = True
        self.__border_radius = 2
        self.__border_width = 0
        self.__background_color = QColor('#111214')
        self.__text_color = QColor('#CFD2D5')
        self.__border_color = QColor('#403E41')
        self.__font = QFont('Arial', 9, QFont.Weight.Bold)
        self.__margins = QMargins(12, 8, 12, 7)

        self.__actual_placement = None
        self.__current_opacity = 0.0
        self.__watched_widgets = [self.__widget] if self.__widget else []

        # Widget settings
        self.setWindowFlags(Qt.WindowType.ToolTip |
                            Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Opacity effect for fading animations
        self.__opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.__opacity_effect)

        # Create widgets
        self.__tooltip_body = QLabel(self)
        self.__triangle_widget = TooltipTriangle(self)

        self.__text_widget = QLabel(self.__tooltip_body)
        self.__text_widget.setText(text)
        self.__text_widget.setFont(self.__font)

        # Init delay timers
        self.__show_delay_timer = QTimer(self)
        self.__show_delay_timer.setInterval(self.__show_delay)
        self.__show_delay_timer.setSingleShot(True)
        self.__show_delay_timer.timeout.connect(self.__start_fade_in)

        self.__hide_delay_timer = QTimer(self)
        self.__hide_delay_timer.setInterval(self.__hide_delay)
        self.__hide_delay_timer.setSingleShot(True)
        self.__hide_delay_timer.timeout.connect(self.__start_fade_out)

        # Init duration timer
        self.__duration_timer = QTimer(self)
        self.__duration_timer.setInterval(self.__duration)
        self.__duration_timer.setSingleShot(True)
        self.__duration_timer.timeout.connect(self.__start_fade_out)

        # Init fade animations
        self.__fade_in_animation = QPropertyAnimation(self.__opacity_effect, b'opacity')
        self.__fade_in_animation.setDuration(self.__fade_in_duration)
        self.__fade_in_animation.setEasingCurve(self.__fade_in_easing_curve)
        self.__fade_in_animation.valueChanged.connect(self.__update_current_opacity)
        self.__fade_in_animation.finished.connect(self.__start_duration_timer)

        self.__fade_out_animation = QPropertyAnimation(self.__opacity_effect, b'opacity')
        self.__fade_out_animation.setDuration(self.__fade_out_duration)
        self.__fade_out_animation.setEasingCurve(self.__fade_out_easing_curve)
        self.__fade_out_animation.valueChanged.connect(self.__update_current_opacity)
        self.__fade_out_animation.finished.connect(self.__hide)

        # Init stylesheet and event filters
        self.__update_stylesheet()
        self.__install_event_filters()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == event.Type.HoverEnter and watched == self.__widget:
            # Mouse enters widget
            self.show()
        elif event.type() == event.Type.HoverLeave and watched == self.__widget:
            # Mouse leaves widget
            self.hide()

        # Widget or parent moved, resized, shown or hidden
        if (event.type() == event.Type.Move or event.type() == event.Type.Resize
                or event.type() == event.Type.Show or event.type() == event.Type.Hide):
            self.__update_ui()

        # One of the parents changed
        if event.type() == event.Type.ParentChange:
            self.__install_event_filters()

        # Parent or widget deleted
        if event.type() == event.Type.DeferredDelete:
            self.__install_event_filters()
            self.hide()
            if watched == self.__widget:
                self.__widget = None
        return False

    def getWidget(self) -> QWidget:
        return self.__widget

    def setWidget(self, widget: QWidget):
        if self.__current_opacity != 0:
            super().hide()
        self.__widget = widget
        self.__install_event_filters()

    def getText(self) -> str:
        return self.__text

    def setText(self, text: str):
        self.__text = text
        self.__text_widget.setText(text)
        self.__update_ui()

    def getDuration(self) -> int:
        return self.__duration

    def setDuration(self, duration: int):
        self.__duration = duration
        self.__duration_timer.setInterval(duration)

    def getPlacement(self) -> TooltipPlacement:
        return self.__placement

    def setPlacement(self, placement: TooltipPlacement):
        self.__placement = placement
        self.__update_ui()

    def getActualPlacement(self) -> TooltipPlacement:
        return self.__actual_placement

    def getFallbackPlacements(self) -> list[TooltipPlacement]:
        return self.__fallback_placements

    def setFallbackPlacements(self, fallback_placements: list[TooltipPlacement]):
        self.__fallback_placements = fallback_placements
        self.__update_ui()

    def isTriangleEnabled(self) -> bool:
        return self.__triangle_enabled

    def setTriangleEnabled(self, enabled: bool):
        self.__triangle_enabled = enabled
        self.__update_ui()

    def getTriangleSize(self) -> int:
        return self.__triangle_size

    def setTriangleSize(self, size: int):
        self.__triangle_size = size
        self.__update_ui()

    def getOffsets(self) -> dict[TooltipPlacement, QPoint]:
        return self.__offsets

    def getOffset(self, placement: TooltipPlacement) -> QPoint:
        return self.__offsets[placement]

    def setOffsets(self, offsets: dict[TooltipPlacement, QPoint]):
        for placement, offset in offsets.items():
            self.__offsets[placement] = offset
        self.__update_ui()

    def setOffset(self, placement: TooltipPlacement, offset: QPoint):
        self.__offsets[placement] = offset
        self.__update_ui()

    def setOffsetAll(self, offset: QPoint):
        for placement, _ in self.__offsets.items():
            self.__offsets[placement] = offset
        self.__update_ui()

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
        if enabled:
            self.__text_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.__text_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__update_ui()

    def getBorderRadius(self) -> int:
        return self.__border_radius

    def setBorderRadius(self, border_radius: int):
        self.__border_radius = border_radius
        self.__update_stylesheet()
        self.__update_ui()

    def getBorderWidth(self) -> int:
        return self.__border_width

    def setBorderWidth(self, width: int):
        self.__border_width = width
        self.__update_stylesheet()
        self.__update_ui()

    def getBackgroundColor(self) -> QColor:
        return self.__background_color

    def setBackgroundColor(self, color: QColor):
        self.__background_color = color
        self.__update_stylesheet()
        self.__update_ui()

    def getTextColor(self) -> QColor:
        return self.__text_color

    def setTextColor(self, color: QColor):
        self.__text_color = color
        self.__update_stylesheet()
        self.__update_ui()

    def getBorderColor(self) -> QColor:
        return self.__border_color

    def setBorderColor(self, color: QColor):
        self.__border_color = color
        self.__update_stylesheet()
        self.__update_ui()

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
        self.__text_widget.setFont(font)
        self.__update_ui()

    def getMargins(self) -> QMargins:
        return self.__margins

    def setMargins(self, margins: QMargins):
        self.__margins = margins
        self.__update_ui()

    def setMarginLeft(self, margin: int):
        self.__margins.setLeft(margin)
        self.__update_ui()

    def setMarginTop(self, margin: int):
        self.__margins.setTop(margin)
        self.__update_ui()

    def setMarginRight(self, margin: int):
        self.__margins.setRight(margin)
        self.__update_ui()

    def setMarginBottom(self, margin: int):
        self.__margins.setBottom(margin)
        self.__update_ui()

    def show(self):
        self.__duration_timer.stop()
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
        if self.__current_opacity == 0.0:
            self.shown.emit()

        self.__fade_in_animation.setStartValue(self.__current_opacity)
        self.__fade_in_animation.setEndValue(1)
        self.__fade_in_animation.start()
        super().show()

    def __start_duration_timer(self):
        if self.__duration != 0:
            self.__duration_timer.start()

    def __start_hide_delay(self):
        self.__show_delay_timer.stop()
        self.__hide_delay_timer.start()

    def __start_fade_out(self):
        self.__fade_out_animation.setStartValue(self.__current_opacity)
        self.__fade_out_animation.setEndValue(0)
        self.__fade_out_animation.start()

    def __hide(self):
        self.__duration_timer.stop()
        super().hide()
        self.hidden.emit()

    def __update_current_opacity(self, value):
        self.__current_opacity = value

    def __update_stylesheet(self):
        self.__tooltip_body.setStyleSheet('background: {}; '
                                          'border-radius: {}px; '
                                          'border: {}px solid {};'
                                          .format(self.__background_color.name(),
                                                  self.__border_radius,
                                                  self.__border_width,
                                                  self.__border_color.name()))

        self.__text_widget.setStyleSheet('border: none;'
                                         'color: {}'.format(self.__text_color.name()))

    def __update_ui(self):
        # Calculate text width and height
        self.__text_widget.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        font_metrics = self.__text_widget.fontMetrics()
        bounding_rect = font_metrics.boundingRect(self.__text)
        text_width = bounding_rect.width() + 2
        text_height = bounding_rect.height()

        # Calculate body width and height
        body_width = self.__margins.left() + text_width + self.__margins.right()
        body_height = self.__margins.top() + text_height + self.__margins.bottom()

        # Handle width greater than maximum width
        if body_width > self.maximumWidth():
            self.__text_widget.setWordWrap(True)
            text_width = self.maximumWidth() - self.__margins.left() - self.__margins.right()
            text_height = self.__text_widget.heightForWidth(text_width)

            # Minimize text width for calculated text height
            new_text_height = self.__text_widget.heightForWidth(text_width - 1)
            new_text_width = text_width
            while new_text_height == text_height:
                new_text_width -= 1
                new_text_height = self.__text_widget.heightForWidth(new_text_width)
            text_width = new_text_width + 1

        # Recalculate body width and height
        body_width = self.__margins.left() + text_width + self.__margins.right()
        body_height = self.__margins.top() + text_height + self.__margins.bottom()

        # Handle height greater than maximum height
        if body_height > self.maximumHeight():
            body_height = self.maximumHeight()

        # Calculate actual tooltip placement
        if self.__placement == TooltipPlacement.AUTO:
            self.__actual_placement = PlacementUtils.get_optimal_placement(self.__widget,
                                                                           QSize(body_width, body_height),
                                                                           self.__triangle_size, self.__offsets)
        else:
            self.__actual_placement = self.__placement
            # Calculate fallback placement
            if self.__fallback_placements:
                fallback_placement = PlacementUtils.get_fallback_placement(self.__widget, self.__actual_placement,
                                                                           self.__fallback_placements,
                                                                           QSize(body_width, body_height),
                                                                           self.__triangle_size, self.__offsets)
                if fallback_placement:
                    self.__actual_placement = fallback_placement

        # Calculate total size and widget positions based on placement
        width = body_width
        height = body_height
        tooltip_triangle_pos = QPoint(0, 0)
        tooltip_body_pos = QPoint(0, 0)
        tooltip_pos = QPoint(0, 0)
        widget_pos = Utils.get_top_level_parent(self.__widget).mapToGlobal(self.__widget.pos())
        self.__triangle_widget.update()

        if self.__actual_placement == TooltipPlacement.TOP:
            height = body_height + self.__triangle_widget.height() - self.__border_width
            tooltip_triangle_pos.setX(math.ceil(width / 2 - self.__triangle_size))
            tooltip_triangle_pos.setY(body_height - self.__border_width)
            tooltip_pos.setX(int(widget_pos.x() + self.__widget.width() / 2 - width / 2)
                             + self.__offsets[self.__actual_placement].x())
            tooltip_pos.setY(widget_pos.y() - height + -self.__offsets[self.__actual_placement].y())

        elif self.__actual_placement == TooltipPlacement.BOTTOM:
            height = body_height + self.__triangle_widget.height() - self.__border_width
            tooltip_triangle_pos.setX(math.ceil(width / 2 - self.__triangle_size))
            tooltip_body_pos.setY(self.__triangle_widget.height() - self.__border_width)
            tooltip_pos.setX(int(widget_pos.x() + self.__widget.width() / 2 - width / 2)
                             + self.__offsets[self.__actual_placement].x())
            tooltip_pos.setY(widget_pos.y() + self.__widget.height()
                             + self.__offsets[self.__actual_placement].y())

        elif self.__actual_placement == TooltipPlacement.LEFT:
            width = body_width + self.__triangle_widget.width() - self.__border_width
            tooltip_triangle_pos.setX(body_width - self.__border_width)
            tooltip_triangle_pos.setY(math.ceil(height / 2 - self.__triangle_size))
            tooltip_pos.setX(widget_pos.x() - width + -self.__offsets[self.__actual_placement].x())
            tooltip_pos.setY(int(widget_pos.y() + self.__widget.height() / 2 - height / 2)
                             + self.__offsets[self.__actual_placement].y())

        elif self.__actual_placement == TooltipPlacement.RIGHT:
            width = body_width + self.__triangle_widget.width() - self.__border_width
            tooltip_triangle_pos.setY(math.ceil(height / 2 - self.__triangle_size))
            tooltip_body_pos.setX(self.__triangle_widget.width() - self.__border_width)
            tooltip_pos.setX(widget_pos.x() + self.__widget.width()
                             + self.__offsets[self.__actual_placement].x())
            tooltip_pos.setY(int(widget_pos.y() + self.__widget.height() / 2 - height / 2)
                             + self.__offsets[self.__actual_placement].y())

        # Move and resize widgets
        self.__text_widget.resize(text_width, text_height)
        self.__text_widget.move(self.__margins.left(), self.__margins.top())
        self.__tooltip_body.resize(body_width, body_height)
        self.__tooltip_body.move(tooltip_body_pos)
        self.__triangle_widget.move(tooltip_triangle_pos)
        self.resize(width, height)
        self.move(tooltip_pos)

    def __install_event_filters(self):
        self.__remove_event_filters()
        if not self.__widget:
            return
        self.__watched_widgets.append(self.__widget)
        self.__watched_widgets += Utils.get_parents(self.__widget)

        for widget in self.__watched_widgets:
            widget.installEventFilter(self)

    def __remove_event_filters(self):
        for widget in self.__watched_widgets:
            widget.removeEventFilter(self)
        self.__watched_widgets.clear()
