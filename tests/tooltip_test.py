from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtCore import QMargins, QPoint, QEasingCurve
from PyQt6.QtGui import QColor, QFont
from src.pyqttooltip import Tooltip, TooltipPlacement
from src.pyqttooltip.constants import DROP_SHADOW_SIZE


def test_initial_values(qtbot):
    """Test initial values after instantiating"""

    tooltip = Tooltip()
    qtbot.addWidget(tooltip)

    assert tooltip.getWidget() is None
    assert tooltip.getText() == ''
    assert tooltip.getDuration() == 0
    assert tooltip.getPlacement() == TooltipPlacement.AUTO
    assert tooltip.getFallbackPlacements() == []
    assert tooltip.isTriangleEnabled() == True
    assert tooltip.getTriangleSize() == 5
    assert tooltip.getOffsetByPlacement(TooltipPlacement.LEFT) == QPoint(0, 0)
    assert tooltip.getOffsetByPlacement(TooltipPlacement.RIGHT) == QPoint(0, 0)
    assert tooltip.getOffsetByPlacement(TooltipPlacement.TOP) == QPoint(0, 0)
    assert tooltip.getOffsetByPlacement(TooltipPlacement.BOTTOM) == QPoint(0, 0)
    assert tooltip.getOffsets() == {
        TooltipPlacement.LEFT:   QPoint(0, 0),
        TooltipPlacement.RIGHT:  QPoint(0, 0),
        TooltipPlacement.TOP:    QPoint(0, 0),
        TooltipPlacement.BOTTOM: QPoint(0, 0)
    }
    assert tooltip.getShowDelay() == 50
    assert tooltip.getHideDelay() == 50
    assert tooltip.getFadeInDuration() == 150
    assert tooltip.getFadeOutDuration() == 150
    assert tooltip.getFadeInEasingCurve() == QEasingCurve.Type.Linear
    assert tooltip.getFadeOutEasingCurve() == QEasingCurve.Type.Linear
    assert tooltip.isTextCenteringEnabled() == True
    assert tooltip.getBorderRadius() == 2
    assert tooltip.isBorderEnabled() == False
    assert tooltip.getBackgroundColor() == QColor('#111214')
    assert tooltip.getTextColor() == QColor('#CFD2D5')
    assert tooltip.getBorderColor() == QColor('#403E41')
    assert tooltip.getOpacity() == 1.0
    assert tooltip.getFont() == QFont('Arial', 9, QFont.Weight.Bold)
    assert tooltip.getMargins() == QMargins(12, 8, 12, 7)
    assert tooltip.isDropShadowEnabled() == True
    assert tooltip.getDropShadowStrength() == 2.0
    assert tooltip.isShowingOnDisabled() == False


def test_show_hide(qtbot):
    """Test showing and hiding the tooltip"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)

    # Show
    tooltip.show()
    qtbot.wait(250)
    assert tooltip.isVisible() == True

    # Hide
    tooltip.hide()
    qtbot.wait(250)
    assert tooltip.isVisible() == False


def test_set_widget(qtbot):
    """Test setting the widget of the tooltip"""

    button1 = QPushButton()
    button2 = QPushButton()
    tooltip = Tooltip(button1, 'Tooltip')

    tooltip.setWidget(button2)
    assert tooltip.getWidget() == button2


def test_set_text(qtbot):
    """Test setting the text of the tooltip"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setText('New tooltip text')
    assert tooltip.getText() == 'New tooltip text'


def test_set_duration(qtbot):
    """Test setting the duration of the tooltip"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDuration(50)
    assert tooltip.getDuration() == 50

    # Tooltip should get hidden 50ms after showing
    tooltip.show()
    qtbot.wait(500)
    assert tooltip.isVisible() == False


def test_set_placement(qtbot):
    """Test setting the placement of the tooltip"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)
    tooltip.show()
    qtbot.wait(250)

    # Left
    tooltip.setPlacement(TooltipPlacement.LEFT)
    assert tooltip.x() == -tooltip.width()

    # Right
    tooltip.setPlacement(TooltipPlacement.RIGHT)
    assert tooltip.x() == button.width()

    # Top
    tooltip.setPlacement(TooltipPlacement.TOP)
    assert tooltip.y() == -tooltip.height()

    # Bottom
    tooltip.setPlacement(TooltipPlacement.BOTTOM)
    assert tooltip.y() == button.height()


def test_set_fallback_placements(qtbot):
    """Test setting the fallback placements of the tooltip"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.LEFT)

    fallback_placements = [TooltipPlacement.BOTTOM, TooltipPlacement.RIGHT]
    tooltip.setFallbackPlacements(fallback_placements)
    assert tooltip.getFallbackPlacements() == fallback_placements
    assert tooltip.getActualPlacement() == TooltipPlacement.BOTTOM


def test_set_triangle(qtbot):
    """Test enabling and disabling triangle and changing its size"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.RIGHT)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    width = tooltip.width()

    # Bigger triangle
    tooltip.setTriangleSize(7)
    assert tooltip.width() == width + 2

    # Disabled triangle
    tooltip.setTriangleEnabled(False)
    assert tooltip.width() == width - 5


def test_set_offsets(qtbot):
    """Test setting the offsets of the tooltip"""

    offsets = {
        TooltipPlacement.LEFT:   QPoint(-10, 0),
        TooltipPlacement.RIGHT:  QPoint(10, 0),
        TooltipPlacement.TOP:    QPoint(0, -10),
        TooltipPlacement.BOTTOM: QPoint(0, 10)
    }

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setOffsets(offsets)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)

    # Left
    tooltip.setPlacement(TooltipPlacement.LEFT)
    assert tooltip.x() == -tooltip.width() - 10

    # Right
    tooltip.setPlacement(TooltipPlacement.RIGHT)
    assert tooltip.x() == button.width() + 10

    # Top
    tooltip.setPlacement(TooltipPlacement.TOP)
    assert tooltip.y() == -tooltip.height() - 10

    # Bottom
    tooltip.setPlacement(TooltipPlacement.BOTTOM)
    assert tooltip.y() == button.height() + 10


def test_set_delays(qtbot):
    """Test setting the delays"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setShowDelay(100)
    tooltip.setHideDelay(80)
    assert tooltip.getShowDelay() == 100
    assert tooltip.getHideDelay() == 80


def test_set_fade_durations(qtbot):
    """Test setting the fade in / out animation durations"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setFadeInDuration(250)
    tooltip.setFadeOutDuration(220)
    assert tooltip.getFadeInDuration() == 250
    assert tooltip.getFadeOutDuration() == 220


def test_set_easing_curves(qtbot):
    """Test setting the easing curves for the fade animations"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setFadeInEasingCurve(QEasingCurve.Type.OutCurve)
    tooltip.setFadeOutEasingCurve(QEasingCurve.Type.InCubic)
    assert tooltip.getFadeInEasingCurve() == QEasingCurve.Type.OutCurve
    assert tooltip.getFadeOutEasingCurve() == QEasingCurve.Type.InCubic

    tooltip.setFadeInEasingCurve(None)
    tooltip.setFadeOutEasingCurve(None)
    assert tooltip.getFadeInEasingCurve() == QEasingCurve.Type.Linear
    assert tooltip.getFadeOutEasingCurve() == QEasingCurve.Type.Linear


def test_set_text_centering_enabled(qtbot):
    """Test disabling text centering for wrapped text"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setTextCenteringEnabled(False)
    assert tooltip.isTextCenteringEnabled() == False


def test_set_border_radius(qtbot):
    """Test setting the border radius"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setBorderRadius(4)
    assert tooltip.getBorderRadius() == 4


def test_set_border_enabled(qtbot):
    """Test enabling the border"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setBorderEnabled(True)
    assert tooltip.isBorderEnabled() == True


def test_set_colors(qtbot):
    """Test setting the colors of the tooltip"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setBackgroundColor(QColor('#FFFFFF'))
    tooltip.setTextColor(QColor('#000000'))
    tooltip.setBorderColor(QColor('#DEDEDE'))
    assert tooltip.getBackgroundColor() == QColor('#FFFFFF')
    assert tooltip.getTextColor() == QColor('#000000')
    assert tooltip.getBorderColor() == QColor('#DEDEDE')


def test_set_font(qtbot):
    """Test setting the font of the tooltip"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    font = QFont('Arial', 9, QFont.Weight.Medium)
    tooltip.setFont(font)
    assert tooltip.getFont() == font
    assert tooltip.font() == font


def test_set_margins(qtbot):
    """Test setting the margins of the tooltip content"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setMargins(QMargins(0, 0, 0, 0))
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    size = tooltip.size()

    tooltip.setMargins(QMargins(10, 5, 10, 5))
    assert tooltip.width() == size.width() + 20
    assert tooltip.height() == size.height() + 10


def test_set_drop_shadow_enabled(qtbot):
    """Test disabling the drop shadow"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.TOP)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.show()
    qtbot.wait(250)
    size = tooltip.size()

    tooltip.setDropShadowEnabled(False)
    assert tooltip.width() == size.width() - DROP_SHADOW_SIZE * 2
    assert tooltip.height() == size.height() - DROP_SHADOW_SIZE * 2 + tooltip.getTriangleSize()


def test_set_drop_shadow_strength(qtbot):
    """Test setting the strength of the drop shadow"""

    button = QPushButton()
    tooltip = Tooltip(button, 'Tooltip')

    tooltip.setDropShadowStrength(3.5)
    assert tooltip.getDropShadowStrength() == 3.5


def test_set_maximum_width(qtbot):
    """Test setting a maximum width for the tooltip"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr')
    tooltip.setMaximumWidth(150)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)

    assert tooltip.maximumWidth() == 150
    assert tooltip.width() <= 150


def test_change_top_level_parent(qtbot):
    """Test changing the top level parent of the widget"""

    window1 = QMainWindow()
    window2 = QMainWindow()
    window2.move(100, 150)
    button = QPushButton(window1)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.TOP)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)
    x = tooltip.x()
    y = tooltip.y()

    # Change button parent and check if tooltip changes position
    button.setParent(window2)
    tooltip.update()
    assert tooltip.x() == x + 100
    assert tooltip.y() == y + 150


def test_delete_parent(qtbot):
    """Test deleting the parent of the widget while the tooltip is showing"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.TOP)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)
    tooltip.show()
    qtbot.wait(250)
    assert tooltip.isVisible() == True

    # Delete window and check if tooltip is now hidden
    window.deleteLater()
    qtbot.wait(250)
    assert tooltip.isVisible() == False


def test_move_top_level_parent(qtbot):
    """Test moving the top level parent of the widget"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.TOP)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)
    x = tooltip.x()
    y = tooltip.y()

    # Move window and check if tooltip follows its position
    window.move(100, 50)
    tooltip.update()
    assert tooltip.x() == x + 100
    assert tooltip.y() == y + 50


def test_resize_widget(qtbot):
    """Test resizing the widget of the tooltip"""

    window = QMainWindow()
    button = QPushButton(window)
    button.resize(100, 25)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.BOTTOM)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)
    y = tooltip.y()

    # Change button height by 25px and check if y position changed by 25px
    button.resize(100, 50)
    tooltip.update()
    assert tooltip.y() == y + 25


def test_move_widget(qtbot):
    """Test moving the widget of the tooltip"""

    window = QMainWindow()
    button = QPushButton(window)
    tooltip = Tooltip(button, 'Tooltip')
    tooltip.setPlacement(TooltipPlacement.BOTTOM)
    tooltip.setOpacity(0)
    tooltip.setFadeInDuration(0)
    tooltip.setShowDelay(0)
    tooltip.setDropShadowEnabled(False)
    x = tooltip.x()
    y = tooltip.y()

    # Move button and check if tooltip follows its position
    button.move(100, 50)
    tooltip.update()
    assert tooltip.x() == x + 100
    assert tooltip.y() == y + 50
