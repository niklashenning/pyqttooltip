from qtpy.QtWidgets import QWidget
from qtpy.QtCore import QSize
from .tooltip_interface import TooltipInterface
from .constants import *


class DropShadow(QWidget):

    def __init__(self, tooltip: TooltipInterface):
        """Create a new DropShadow instance

        :param tooltip: tooltip the drop shadow belongs to
        """

        super(DropShadow, self).__init__(tooltip)

        self.tooltip = tooltip

        # Drop shadow drawn manually since only one graphics effect can be applied
        self.layers = []

        for i in range(DROP_SHADOW_SIZE):
            layer = QWidget(self)
            self.__apply_layer_stylesheet(layer, i)
            self.layers.append(layer)

    def update(self):
        """Update the stylesheets of the layers"""

        for i, layer in enumerate(self.layers):
            self.__apply_layer_stylesheet(layer, i)

    def resize(self, size: QSize):
        """Resize the drop shadow widget

        :param size: new size
        """

        super().resize(size)
        width = size.width()
        height = size.height()

        # Resize and move drop shadow layers
        for i, layer in enumerate(self.layers):
            layer.resize(width - i * 2, height - i * 2)
            layer.move(i, i)

    def __apply_layer_stylesheet(self, layer: QWidget, index: int):
        """Apply stylesheet to a layer widget

        :param layer: layer to apply the stylesheet to
        :param index: index of the layer
        """

        layer.setStyleSheet(
            'background: rgba(0, 0, 0, {}); '
            'border-radius: 8px;'
            .format((index + 1) * 0.001 * self.tooltip.getDropShadowStrength())
        )
