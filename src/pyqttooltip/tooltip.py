import math
from qtpy.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect
from qtpy.QtCore import (
    Qt, Signal, QMargins, QPoint, QSize, QTimer,
    QPropertyAnimation, QEasingCurve, QEvent, QObject
)
from qtpy.QtGui import QColor, QFont
from .tooltip_interface import TooltipInterface
from .tooltip_triangle import TooltipTriangle
from .enums import TooltipPlacement
from .drop_shadow import DropShadow
from .placement_utils import PlacementUtils
from .utils import Utils
from .constants import *


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
        self.__border_enabled = False
        self.__background_color = QColor('#111214')
        self.__text_color = QColor('#CFD2D5')
        self.__border_color = QColor('#403E41')
        self.__font = QFont('Arial', 9, QFont.Weight.Bold)
        self.__margins = QMargins(12, 8, 12, 7)
        self.__drop_shadow_enabled = True
        self.__drop_shadow_strength = 2.0
        self.__showing_on_disabled = False
        self.__maximum_width = QWIDGETSIZE_MAX

        self.__actual_placement = None
        self.__current_opacity = 0.0
        self.__watched_widgets = []

        # Widget settings
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Opacity effect for fading animations
        self.__opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.__opacity_effect)

        # Create widgets
        self.__drop_shadow_widget = DropShadow(self)
        self.__tooltip_body = QLabel(self)
        self.__triangle_widget = TooltipTriangle(self)

        self.__text_widget = QLabel(self.__tooltip_body)
        self.__text_widget.setText(text)
        self.__text_widget.setFont(self.__font)
        self.__text_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        """Event filter that watched widget and all of its parents
        and updates the tooltip or event filters when necessary

        :param watched: object that is watched
        :param event: event that is received
        :return: whether further processing of the event is stopped
        """

        if event.type() == event.Type.HoverEnter and watched == self.__widget:
            # Mouse enters widget
            if self.__widget and self.__widget.isEnabled():
                self.show(delay=True)
            elif self.__widget and not self.__widget.isEnabled() and self.__showing_on_disabled:
                self.show(delay=True)
        elif event.type() == event.Type.HoverLeave and watched == self.__widget:
            # Mouse leaves widget
            self.hide(delay=True)

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
        """Get the widget that triggers the tooltip

        :return: widget
        """

        return self.__widget

    def setWidget(self, widget: QWidget):
        """Set the widget that triggers the tooltip

        :param widget: new widget
        """

        if self.__current_opacity != 0:
            super().hide()
        self.__widget = widget
        self.__install_event_filters()

    def getText(self) -> str:
        """Get the text of the tooltip

        :return: text
        """

        return self.__text

    def setText(self, text: str):
        """Set the text of the tooltip

        :param text: new text
        """

        self.__text = text
        self.__text_widget.setText(text)
        self.__update_ui()

    def getDuration(self) -> int:
        """Get the duration of the tooltip. If the duration is 0,
         the tooltip will stay open until the mouse leaves the widget.

        :return: duration
        """

        return self.__duration

    def setDuration(self, duration: int):
        """Set the duration of the tooltip. If the duration is 0,
         the tooltip will stay open until the mouse leaves the widget.

        :param duration: new duration
        """

        self.__duration = duration
        self.__duration_timer.setInterval(duration)

    def getPlacement(self) -> TooltipPlacement:
        """Get the placement of the tooltip

        :return: placement
        """

        return self.__placement

    def setPlacement(self, placement: TooltipPlacement):
        """Set the placement of the tooltip

        :param placement: new placement
        """

        self.__placement = placement
        self.__update_ui()

    def getActualPlacement(self) -> TooltipPlacement:
        """Get the actual placement of the tooltip. This will be different
        from the placement if the placement is TooltipPlacement.AUTO
        or the tooltip is shown in a fallback placement.

        :return: actual placement (LEFT / RIGHT / TOP / BOTTOM)
        """

        return self.__actual_placement

    def getFallbackPlacements(self) -> list[TooltipPlacement]:
        """Get the fallback placements of the tooltip. If the tooltip
        doesn't fit on the screen with the main placement, one of the
        fallback placements will be chosen instead.

        :return: fallback placements
        """

        return self.__fallback_placements

    def setFallbackPlacements(self, fallback_placements: list[TooltipPlacement]):
        """Set the fallback placements of the tooltip. If the tooltip
        doesn't fit on the screen with the main placement, one of the
        fallback placements will be chosen instead.

        :param fallback_placements: new fallback placements
        """

        self.__fallback_placements = fallback_placements
        self.__update_ui()

    def isTriangleEnabled(self) -> bool:
        """Get whether the triangle is enabled

        :return: whether the triangle is enabled
        """

        return self.__triangle_enabled

    def setTriangleEnabled(self, enabled: bool):
        """Get whether the triangle should be enabled

        :param enabled: whether the triangle should be enabled
        """

        self.__triangle_enabled = enabled
        self.__update_ui()

    def getTriangleSize(self) -> int:
        """Get the size of the triangle

        :return: size
        """

        return self.__triangle_size

    def setTriangleSize(self, size: int):
        """Set the size of the triangle

        :param size: new size
        """

        self.__triangle_size = size
        self.__update_ui()

    def getOffsets(self) -> dict[TooltipPlacement, QPoint]:
        """Get the offsets of the tooltip

        :return: offsets
        """

        return self.__offsets

    def getOffsetByPlacement(self, placement: TooltipPlacement) -> QPoint:
        """Get a specific offset of the tooltip

        :param placement: placement to get the offset for
        :return: offset
        """

        return self.__offsets[placement]

    def setOffsets(self, offsets: dict[TooltipPlacement, QPoint]):
        """Set the offsets of the tooltip individually

        :param offsets: dict with placements as the keys and offsets as values
        """

        for placement, offset in offsets.items():
            self.__offsets[placement] = offset
        self.__update_ui()

    def setOffsetByPlacement(self, placement: TooltipPlacement, offset: QPoint):
        """Set a specific offset of the tooltip

        :param placement: placement to set the offset for
        :param offset: new offset
        """

        self.__offsets[placement] = offset
        self.__update_ui()

    def setOffsetsAll(self, offset: QPoint):
        """Set the offsets of all the placements to a value

        :param offset: new offset for all the placements
        """

        for placement, _ in self.__offsets.items():
            self.__offsets[placement] = offset
        self.__update_ui()

    def getShowDelay(self) -> int:
        """Get the delay before the tooltip is starting to fade in

        :return: delay
        """

        return self.__show_delay

    def setShowDelay(self, delay: int):
        """Set the delay before the tooltip is starting to fade in

        :param delay: new delay
        """

        self.__show_delay = delay
        self.__show_delay_timer.setInterval(delay)

    def getHideDelay(self) -> int:
        """Get the delay before the tooltip is starting to fade out

        :return: delay
        """

        return self.__hide_delay

    def setHideDelay(self, delay: int):
        """Set the delay before the tooltip is starting to fade out

        :param delay: new delay
        """

        self.__hide_delay = delay
        self.__hide_delay_timer.setInterval(delay)

    def getFadeInDuration(self) -> int:
        """Get the duration of the fade in animation

        :return: duration
        """

        return self.__fade_in_duration

    def setFadeInDuration(self, duration: int):
        """Set the duration of the fade in animation

        :param duration: new duration
        """

        self.__fade_in_duration = duration
        self.__fade_in_animation.setStartValue(self.__current_opacity)
        self.__fade_in_animation.setDuration(duration)

    def getFadeOutDuration(self) -> int:
        """Get the duration of the fade out animation

        :return: duration
        """

        return self.__fade_out_duration

    def setFadeOutDuration(self, duration: int):
        """Set the duration of the fade out animation

        :param duration: new duration
        """

        self.__fade_out_duration = duration
        self.__fade_out_animation.setStartValue(self.__current_opacity)
        self.__fade_out_animation.setDuration(duration)

    def getFadeInEasingCurve(self) -> QEasingCurve.Type:
        """Get the easing curve of the fade in animation

        :return: easing curve
        """

        return self.__fade_in_easing_curve

    def setFadeInEasingCurve(self, easing_curve: QEasingCurve.Type | None):
        """Set the easing curve of the fade in animation

        :param easing_curve: new easing curve (or None)
        """

        if easing_curve is None:
            easing_curve = QEasingCurve.Type.Linear

        self.__fade_in_easing_curve = easing_curve
        self.__fade_in_animation.setEasingCurve(easing_curve)

    def getFadeOutEasingCurve(self) -> QEasingCurve.Type:
        """Get the easing curve of the fade out animation

        :return: easing curve
        """

        return self.__fade_out_easing_curve

    def setFadeOutEasingCurve(self, easing_curve: QEasingCurve.Type | None):
        """Set the easing curve of the fade out animation

        :param easing_curve: new easing curve (or None)
        """

        if easing_curve is None:
            easing_curve = QEasingCurve.Type.Linear

        self.__fade_out_easing_curve = easing_curve
        self.__fade_out_animation.setEasingCurve(easing_curve)

    def isTextCenteringEnabled(self) -> bool:
        """Get whether text centering is enabled

        :return: whether text centering is enabled
        """

        return self.__text_centering_enabled

    def setTextCenteringEnabled(self, enabled: bool):
        """Set whether text centering should be enabled

        :param enabled: whether text centering should be enabled
        """

        self.__text_centering_enabled = enabled
        if enabled:
            self.__text_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.__text_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__update_ui()

    def getBorderRadius(self) -> int:
        """Get the border radius of the tooltip

        :return: border radius
        """

        return self.__border_radius

    def setBorderRadius(self, border_radius: int):
        """Set the border radius of the tooltip

        :param border_radius: new border radius
        """

        self.__border_radius = border_radius
        self.__update_stylesheet()
        self.__update_ui()

    def isBorderEnabled(self) -> bool:
        """Get whether the border is enabled

        :return: whether the border is enabled
        """

        return self.__border_enabled

    def setBorderEnabled(self, enabled: bool):
        """Set whether the border should be enabled

        :param enabled: whether the border should be enabled
        """

        self.__border_enabled = enabled
        self.__update_stylesheet()
        self.__update_ui()

    def getBackgroundColor(self) -> QColor:
        """Get the background color of the tooltip

        :return: background color
        """

        return self.__background_color

    def setBackgroundColor(self, color: QColor):
        """Set the background color of the tooltip

        :param color: new background color
        """

        self.__background_color = color
        self.__update_stylesheet()
        self.__update_ui()

    def getTextColor(self) -> QColor:
        """Get the text color of the tooltip

        :return: text color
        """

        return self.__text_color

    def setTextColor(self, color: QColor):
        """Set the text color of the tooltip

        :param color: new text color
        """

        self.__text_color = color
        self.__update_stylesheet()
        self.__update_ui()

    def getBorderColor(self) -> QColor:
        """Get the border color of the tooltip

        :return: border color
        """

        return self.__border_color

    def setBorderColor(self, color: QColor):
        """Set the border color of the tooltip

        :param color: new border color
        """

        self.__border_color = color
        self.__update_stylesheet()
        self.__update_ui()

    def getOpacity(self) -> float:
        """Get the opacity of the tooltip

        :return: opacity
        """

        return self.windowOpacity()

    def setOpacity(self, opacity: float):
        """Set the opacity of the tooltip

        :param opacity: new opacity
        """

        self.setWindowOpacity(opacity)

    def font(self) -> QFont:
        """Get the font of the tooltip

        :return: font
        """

        return self.getFont()

    def getFont(self) -> QFont:
        """Get the font of the tooltip

        :return: font
        """

        return self.__font

    def setFont(self, font: QFont):
        """Set the font of the tooltip

        :param font: new font
        """

        self.__font = font
        self.__text_widget.setFont(font)
        self.__update_ui()

    def getMargins(self) -> QMargins:
        """Get the margins of the tooltip

        :return: margins
        """

        return self.__margins

    def setMargins(self, margins: QMargins):
        """Get the margins of the tooltip

        :param margins: new margins
        """

        self.__margins = margins
        self.__update_ui()

    def setMarginLeft(self, margin: int):
        """Set the left margin of the tooltip

        :param margin: new margin
        """

        self.__margins.setLeft(margin)
        self.__update_ui()

    def setMarginTop(self, margin: int):
        """Set the top margin of the tooltip

        :param margin: new margin
        """

        self.__margins.setTop(margin)
        self.__update_ui()

    def setMarginRight(self, margin: int):
        """Set the right margin of the tooltip

        :param margin: new margin
        """

        self.__margins.setRight(margin)
        self.__update_ui()

    def setMarginBottom(self, margin: int):
        """Set the bottom margin of the tooltip

        :param margin: new margin
        """

        self.__margins.setBottom(margin)
        self.__update_ui()

    def isDropShadowEnabled(self) -> bool:
        """Get whether the drop shadow is enabled

        :return: whether the drop shadow is enabled
        """

        return self.__drop_shadow_enabled

    def setDropShadowEnabled(self, enabled: bool):
        """Set whether the drop shadow should be enabled

        :param enabled: whether the drop shadow should be enabled
        """

        self.__drop_shadow_enabled = enabled
        self.__update_ui()

    def getDropShadowStrength(self) -> float:
        """Get the strength of the drop shadow

        :return: strength
        """

        return self.__drop_shadow_strength

    def setDropShadowStrength(self, strength: float):
        """Set the strength of the drop shadow

        :param strength: new strength
        """

        self.__drop_shadow_strength = strength
        self.__drop_shadow_widget.update()

    def isShowingOnDisabled(self) -> bool:
        """Get whether the tooltip will also be shown on disabled widgets

        :return: whether the tooltip will also be shown on disabled widgets
        """

        return self.__showing_on_disabled

    def setShowingOnDisabled(self, on: bool):
        """Set whether the tooltip should also be shown on disabled widgets

        :param on: whether the tooltip should also be shown on disabled widgets
        """

        self.__showing_on_disabled = on

    def maximumSize(self) -> QSize:
        """Get the maximum size of the tooltip

        :return: maximum size
        """

        return QSize(self.__maximum_width, self.maximumHeight())

    def setMaximumSize(self, max_size: QSize):
        """Set the maximum size of the tooltip

        :param max_size: new maximum size
        """

        self.__maximum_width = max_size.width()
        self.setMaximumHeight(max_size.height())
        self.__update_ui()

    def maximumWidth(self) -> int:
        """Get the maximum width of the tooltip

        :return: maximum width
        """

        return self.__maximum_width

    def setMaximumWidth(self, max_width: int):
        """Set the maximum width of the tooltip

        :param max_width: new maximum width
        """

        self.__maximum_width = max_width
        self.__update_ui()

    def show(self, delay: bool = False):
        """Start the process of showing the tooltip

        :param delay: whether the tooltip should be shown with the delay (default: False)
        """

        self.__duration_timer.stop()
        self.__update_ui()

        if delay:
            self.__start_show_delay()
        else:
            self.__start_fade_in()

    def hide(self, delay: bool = False):
        """Start the process of hiding the tooltip

        :param delay: whether the tooltip should be hidden with the delay (default: False)
        """

        if delay:
            self.__start_hide_delay()
        else:
            self.__start_fade_out()

    def update(self):
        """Update the tooltip"""

        self.__update_ui()
        super().update()

    def __start_show_delay(self):
        """Start a delay that will start the fade in animation when finished"""

        self.__hide_delay_timer.stop()
        self.__show_delay_timer.start()

    def __start_fade_in(self):
        """Start the fade in animation"""

        # Emit shown signal if currently hidden
        if self.__current_opacity == 0.0:
            self.shown.emit()

        # Start fade in animation and show
        self.__fade_in_animation.setStartValue(self.__current_opacity)
        self.__fade_in_animation.setEndValue(1)
        self.__fade_in_animation.start()
        super().show()

    def __start_duration_timer(self):
        """Start the duration timer that hides the tooltip after
         a specific amount of time if enabled"""

        if self.__duration != 0:
            self.__duration_timer.start()

    def __start_hide_delay(self):
        """Start a delay that will start the fade out animation when finished"""

        self.__show_delay_timer.stop()
        self.__hide_delay_timer.start()

    def __start_fade_out(self):
        """Start the fade out animation"""

        self.__fade_out_animation.setStartValue(self.__current_opacity)
        self.__fade_out_animation.setEndValue(0)
        self.__fade_out_animation.start()

    def __hide(self):
        """Hide the tooltip"""

        self.__duration_timer.stop()
        super().hide()
        self.hidden.emit()

    def __update_current_opacity(self, value: float):
        """Update the current_opacity attribute with the new value of the animation

        :param value: value received by the valueChanged event
        """

        self.__current_opacity = value

    def __update_stylesheet(self):
        """Update the stylesheet of the widgets that are part of the tooltip"""

        self.__tooltip_body.setStyleSheet(
            'background: {}; '
            'border-radius: {}px; '
            'border: {}px solid {};'
            .format(
                self.__background_color.name(),
                self.__border_radius,
                1 if self.__border_enabled else 0,
                self.__border_color.name()
            )
        )
        self.__text_widget.setStyleSheet(
            'border: none;'
            'color: {}'.format(self.__text_color.name())
        )

    def __update_ui(self):
        """Update the UI of the tooltip"""

        if not self.__widget:
            return

        # Calculate text width and height
        self.__text_widget.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        font_metrics = self.__text_widget.fontMetrics()
        bounding_rect = font_metrics.boundingRect(self.__text)
        text_size = QSize(bounding_rect.width() + 2, bounding_rect.height())

        # Calculate body width and height
        body_size = QSize(
            self.__margins.left() + text_size.width() + self.__margins.right(),
            self.__margins.top() + text_size.height() + self.__margins.bottom()
        )

        # Handle width greater than maximum width
        if body_size.width() > self.__maximum_width:
            self.__text_widget.setWordWrap(True)
            text_size.setWidth(self.__maximum_width - self.__margins.left() - self.__margins.right())
            text_size.setHeight(self.__text_widget.heightForWidth(text_size.width()))

            # Minimize text width for calculated text height
            new_text_height = self.__text_widget.heightForWidth(text_size.width() - 1)
            new_text_width = text_size.width()
            while new_text_height == text_size.height():
                new_text_width -= 1
                new_text_height = self.__text_widget.heightForWidth(new_text_width)
            text_size.setWidth(new_text_width + 1)

            # Recalculate body width and height
            body_size.setWidth(self.__margins.left() + text_size.width() + self.__margins.right())
            body_size.setHeight(self.__margins.top() + text_size.height() + self.__margins.bottom())

        # Calculate actual tooltip placement
        if self.__placement == TooltipPlacement.AUTO:
            self.__actual_placement = PlacementUtils.get_optimal_placement(
                self.__widget, body_size, self.__triangle_size, self.__offsets
            )
        else:
            self.__actual_placement = self.__placement
            # Calculate fallback placement
            if self.__fallback_placements:
                fallback_placement = PlacementUtils.get_fallback_placement(
                    self.__widget, self.__actual_placement, self.__fallback_placements,
                    body_size, self.__triangle_size, self.__offsets
                )
                if fallback_placement:
                    self.__actual_placement = fallback_placement

        # Calculate total size and widget positions based on placement
        size = QSize(body_size.width(), body_size.height())
        tooltip_triangle_pos = QPoint(0, 0)
        tooltip_body_pos = QPoint(0, 0)
        tooltip_pos = QPoint(0, 0)
        widget_pos = Utils.get_top_level_parent(self.__widget).mapToGlobal(self.__widget.pos())
        border_width = 1 if self.__border_enabled else 0
        self.__triangle_widget.update()

        if self.__actual_placement == TooltipPlacement.TOP:
            size.setHeight(body_size.height() + self.__triangle_widget.height() - border_width)
            tooltip_triangle_pos.setX(math.ceil(size.width() / 2 - self.__triangle_size))
            tooltip_triangle_pos.setY(body_size.height() - border_width)
            tooltip_pos.setX(
                int(widget_pos.x() + self.__widget.width() / 2 - size.width() / 2)
                + self.__offsets[self.__actual_placement].x()
            )
            tooltip_pos.setY(widget_pos.y() - size.height() + self.__offsets[self.__actual_placement].y())

        elif self.__actual_placement == TooltipPlacement.BOTTOM:
            size.setHeight(body_size.height() + self.__triangle_widget.height() - border_width)
            tooltip_triangle_pos.setX(math.ceil(size.width() / 2 - self.__triangle_size))
            tooltip_body_pos.setY(self.__triangle_widget.height() - border_width)
            tooltip_pos.setX(
                int(widget_pos.x() + self.__widget.width() / 2 - size.width() / 2)
                + self.__offsets[self.__actual_placement].x()
            )
            tooltip_pos.setY(
                widget_pos.y() + self.__widget.height() + self.__offsets[self.__actual_placement].y()
            )

        elif self.__actual_placement == TooltipPlacement.LEFT:
            size.setWidth(body_size.width() + self.__triangle_widget.width() - border_width)
            tooltip_triangle_pos.setX(body_size.width() - border_width)
            tooltip_triangle_pos.setY(math.ceil(size.height() / 2 - self.__triangle_size))
            tooltip_pos.setX(widget_pos.x() - size.width() + self.__offsets[self.__actual_placement].x())
            tooltip_pos.setY(
                int(widget_pos.y() + self.__widget.height() / 2 - size.height() / 2)
                + self.__offsets[self.__actual_placement].y()
            )

        elif self.__actual_placement == TooltipPlacement.RIGHT:
            size.setWidth(body_size.width() + self.__triangle_widget.width() - border_width)
            tooltip_triangle_pos.setY(math.ceil(size.height() / 2 - self.__triangle_size))
            tooltip_body_pos.setX(self.__triangle_widget.width() - border_width)
            tooltip_pos.setX(
                widget_pos.x() + self.__widget.width()
                + self.__offsets[self.__actual_placement].x()
            )
            tooltip_pos.setY(
                int(widget_pos.y() + self.__widget.height() / 2 - size.height() / 2)
                + self.__offsets[self.__actual_placement].y()
            )

        # Move and resize widgets
        self.__text_widget.resize(text_size)
        self.__text_widget.move(self.__margins.left(), self.__margins.top())
        self.__tooltip_body.resize(body_size)

        if self.__drop_shadow_enabled:
            # Adjust positions and sizes for drop shadow if enabled
            self.__tooltip_body.move(
                tooltip_body_pos.x() + DROP_SHADOW_SIZE, tooltip_body_pos.y() + DROP_SHADOW_SIZE
            )
            self.__triangle_widget.move(
                tooltip_triangle_pos.x() + DROP_SHADOW_SIZE, tooltip_triangle_pos.y() + DROP_SHADOW_SIZE
            )
            self.__drop_shadow_widget.resize(
                QSize(body_size.width() + DROP_SHADOW_SIZE * 2, body_size.height() + DROP_SHADOW_SIZE * 2)
            )
            self.__drop_shadow_widget.move(tooltip_body_pos)
            self.__drop_shadow_widget.update()
            self.__drop_shadow_widget.setVisible(True)
            self.setFixedSize(
                max(size.width(), self.__drop_shadow_widget.width() + tooltip_body_pos.x()),
                max(size.height(), self.__drop_shadow_widget.height() + tooltip_body_pos.y())
            )
            self.move(tooltip_pos.x() - DROP_SHADOW_SIZE, tooltip_pos.y() - DROP_SHADOW_SIZE)
        else:
            self.__tooltip_body.move(tooltip_body_pos)
            self.__triangle_widget.move(tooltip_triangle_pos)
            self.setFixedSize(size)
            self.move(tooltip_pos)
            self.__drop_shadow_widget.setVisible(False)

    def __install_event_filters(self):
        """Install / reinstall event filters on widget and its parents"""

        self.__remove_event_filters()
        if not self.__widget:
            return
        self.__watched_widgets.append(self.__widget)
        self.__watched_widgets += Utils.get_parents(self.__widget)

        for widget in self.__watched_widgets:
            widget.installEventFilter(self)

    def __remove_event_filters(self):
        """Remove installed event filters"""

        for widget in self.__watched_widgets:
            widget.removeEventFilter(self)
        self.__watched_widgets.clear()
