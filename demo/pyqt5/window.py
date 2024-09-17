from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox
)
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor
from pyqttooltip import Tooltip, TooltipPlacement


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)

        # Window settings
        self.setWindowTitle('PyQt Tooltip Demo')
        self.setFixedSize(600, 320)

        # Create tooltip widget and tooltip
        self.tooltip_widget = QPushButton('Show tooltip', self)
        self.tooltip_widget.setFixedSize(110, 30)

        self.tooltip = Tooltip(self.tooltip_widget, 'This is a tooltip')

        # Create settings layout
        settings_layout = QHBoxLayout()
        settings_layout.addLayout(self.create_left_settings_layout())
        settings_layout.addLayout(self.create_right_settings_layout())
        settings_layout.setContentsMargins(0, 35, 0, 0)

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tooltip_widget, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addLayout(settings_layout)
        main_layout.setContentsMargins(25, 40, 25, 25)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_left_settings_layout(self):
        # Create settings widgets
        self.placement_dropdown = QComboBox()
        self.placement_dropdown.addItems(['AUTO', 'LEFT', 'RIGHT', 'TOP', 'BOTTOM'])
        self.placement_dropdown.currentTextChanged.connect(self.placement_dropdown_changed)

        self.text_input = QLineEdit()
        self.text_input.setText(self.tooltip.getText())
        self.text_input.textChanged.connect(self.text_input_changed)

        self.max_width_input = QSpinBox()
        self.max_width_input.setRange(50, 1000)
        self.max_width_input.setValue(self.tooltip.maximumWidth())
        self.max_width_input.valueChanged.connect(self.max_width_input_changed)

        self.opacity_input = QDoubleSpinBox()
        self.opacity_input.setRange(0.0, 1.0)
        self.opacity_input.setSingleStep(0.05)
        self.opacity_input.setValue(self.tooltip.getOpacity())
        self.opacity_input.valueChanged.connect(self.opacity_input_changed)

        self.fade_duration_input = QSpinBox()
        self.fade_duration_input.setRange(0, 5000)
        self.fade_duration_input.setValue(self.tooltip.getFadeInDuration())
        self.fade_duration_input.valueChanged.connect(self.fade_duration_input_changed)

        self.delay_input = QSpinBox()
        self.delay_input.setRange(0, 2500)
        self.delay_input.setValue(self.tooltip.getShowDelay())
        self.delay_input.valueChanged.connect(self.delay_input_changed)

        self.triangle_size_input = QSpinBox()
        self.triangle_size_input.setRange(0, 25)
        self.triangle_size_input.setValue(self.tooltip.getTriangleSize())
        self.triangle_size_input.valueChanged.connect(self.triangle_size_input_changed)

        # Add widgets to layout
        left_settings_layout = QFormLayout()
        left_settings_layout.addRow('Placement: ', self.placement_dropdown)
        left_settings_layout.addRow('Text: ', self.text_input)
        left_settings_layout.addRow('Max width: ', self.max_width_input)
        left_settings_layout.addRow('Opacity: ', self.opacity_input)
        left_settings_layout.addRow('Fade duration: ', self.fade_duration_input)
        left_settings_layout.addRow('Delay: ', self.delay_input)
        left_settings_layout.addRow('Triangle size: ', self.triangle_size_input)
        left_settings_layout.setContentsMargins(0, 0, 10, 0)

        return left_settings_layout

    def create_right_settings_layout(self):
        # Create settings widgets
        self.border_radius_input = QSpinBox()
        self.border_radius_input.setRange(0, 10)
        self.border_radius_input.setValue(self.tooltip.getBorderRadius())
        self.border_radius_input.valueChanged.connect(self.border_radius_input_changed)

        self.offset_x_input = QSpinBox()
        self.offset_x_input.setRange(-500, 500)
        self.offset_x_input.valueChanged.connect(self.offset_x_input_changed)

        self.offset_y_input = QSpinBox()
        self.offset_y_input.setRange(-500, 500)
        self.offset_y_input.valueChanged.connect(self.offset_y_input_changed)

        self.background_color_input = QLineEdit()
        self.background_color_input.setText(self.tooltip.getBackgroundColor().name())
        self.background_color_input.textChanged.connect(self.background_color_input_changed)

        self.text_color_input = QLineEdit()
        self.text_color_input.setText(self.tooltip.getTextColor().name())
        self.text_color_input.textChanged.connect(self.text_color_input_changed)

        self.border_color_input = QLineEdit()
        self.border_color_input.setText(self.tooltip.getBorderColor().name())
        self.border_color_input.textChanged.connect(self.border_color_input_changed)

        self.border_enabled_input = QCheckBox('Border enabled')
        self.border_enabled_input.stateChanged.connect(self.border_enabled_input_changed)

        # Add widgets to layout
        right_settings_layout = QFormLayout()
        right_settings_layout.addRow('Border radius: ', self.border_radius_input)
        right_settings_layout.addRow('Offset X: ', self.offset_x_input)
        right_settings_layout.addRow('Offset Y: ', self.offset_y_input)
        right_settings_layout.addRow('Background color: ', self.background_color_input)
        right_settings_layout.addRow('Text color: ', self.text_color_input)
        right_settings_layout.addRow('Border color: ', self.border_color_input)
        right_settings_layout.addWidget(self.border_enabled_input)
        right_settings_layout.setContentsMargins(10, 0, 0, 0)

        return right_settings_layout

    def placement_dropdown_changed(self, item):
        if item == 'AUTO':
            self.tooltip.setPlacement(TooltipPlacement.AUTO)
        elif item == 'LEFT':
            self.tooltip.setPlacement(TooltipPlacement.LEFT)
        elif item == 'RIGHT':
            self.tooltip.setPlacement(TooltipPlacement.RIGHT)
        elif item == 'TOP':
            self.tooltip.setPlacement(TooltipPlacement.TOP)
        elif item == 'BOTTOM':
            self.tooltip.setPlacement(TooltipPlacement.BOTTOM)

    def text_input_changed(self, text):
        self.tooltip.setText(text)

    def max_width_input_changed(self, max_width):
        self.tooltip.setMaximumWidth(max_width)

    def opacity_input_changed(self, opacity):
        self.tooltip.setOpacity(opacity)

    def fade_duration_input_changed(self, fade_duration):
        self.tooltip.setFadeInDuration(fade_duration)
        self.tooltip.setFadeOutDuration(fade_duration)

    def delay_input_changed(self, delay):
        self.tooltip.setShowDelay(delay)
        self.tooltip.setHideDelay(delay)

    def triangle_size_input_changed(self, triangle_size):
        self.tooltip.setTriangleSize(triangle_size)

    def border_radius_input_changed(self, border_radius):
        self.tooltip.setBorderRadius(border_radius)

    def offset_x_input_changed(self, offset_x):
        self.tooltip.setOffsetsAll(
            QPoint(offset_x, self.tooltip.getOffsetByPlacement(self.tooltip.getActualPlacement()).y())
        )

    def offset_y_input_changed(self, offset_y):
        self.tooltip.setOffsetsAll(
            QPoint(self.tooltip.getOffsetByPlacement(self.tooltip.getActualPlacement()).x(), offset_y)
        )

    def background_color_input_changed(self, text):
        self.tooltip.setBackgroundColor(QColor(text))

    def text_color_input_changed(self, text):
        self.tooltip.setTextColor(QColor(text))

    def border_color_input_changed(self, text):
        self.tooltip.setBorderColor(QColor(text))

    def border_enabled_input_changed(self, state):
        self.tooltip.setBorderEnabled(state)
