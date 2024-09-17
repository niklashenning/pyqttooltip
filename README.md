# PyQt Tooltip

[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/pyqttooltip/)
[![Python](https://img.shields.io/badge/python-3.7+-blue)](https://github.com/niklashenning/pyqttooltip)
[![Build](https://img.shields.io/badge/build-passing-neon)](https://github.com/niklashenning/pyqttooltip)
[![Coverage](https://img.shields.io/badge/coverage-92%25-green)](https://github.com/niklashenning/pyqttooltip)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/niklashenning/pyqttooltip/blob/master/LICENSE)


A modern and fully customizable tooltip library for PyQt and PySide

![pyqttooltip](https://github.com/user-attachments/assets/0313ffc7-560b-4665-a652-e1e2601fcbaa)

## Features
- Fixed and automatic placement
- Supports fallback placements
- Customizable triangle
- Customizable animations and delays
- Fully customizable and modern UI
- Works with `PyQt5`, `PyQt6`, `PySide2`, and `PySide6`

## Installation
```
pip install pyqttooltip
```

## Usage
```python
from PyQt6.QtWidgets import QMainWindow, QPushButton
from pyqttooltip import Tooltip, TooltipPlacement


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        # Add button
        self.button = QPushButton('Button', self)
        
        # Add tooltip to button
        self.tooltip = Tooltip(self.button, 'This is a tooltip')
```


The tooltip will automatically be shown while hovering the widget. If you want to manually
show and hide the tooltip, you can use the `show()` and `hide()` methods:
```python
tooltip.show()
tooltip.hide()
```


To delete a tooltip, you can use the `deleteLater()` method:
```python
tooltip.deleteLater()
```


To get notified when a tooltip gets shown or hidden, you can subscribe to the `shown` and `hidden` signals:
```python
tooltip.shown.connect(lambda: print('shown'))
tooltip.hidden.connect(lambda: print('hidden'))
```


## Customization

* **Setting the widget:**
```python
tooltip.setWidget(widget)  # Default: None
```


* **Setting the text:**
```python
tooltip.setText('Text of the tooltip')  # Default: ''
```


* **Setting the placement:**
```python
tooltip.setPlacement(TooltipPlacement.RIGHT)  # Default: TooltipPlacement.AUTO
```
> **AVAILABLE PLACEMENTS:** <br> `AUTO`, `LEFT`, `RIGHT`, `TOP`, `BOTTOM`


* **Setting the fallback placements:**
```python
tooltip.setFallbackPlacements([TooltipPlacement.TOP, TooltipPlacement.BOTTOM])  # Default: []
```
> If the tooltip doesn't fit on the screen with the primary placement, one of the
> fallback placements will be chosen instead in the order of the provided list.
> <br> To get the current placement of the tooltip, you can use the `getActualPlacement()` method.


* **Enabling or disabling the triangle:**
```python
tooltip.setTriangleEnabled(False)  # Default: True
```


* **Setting the size of the triangle:**
```python
tooltip.setTriangleSize(7)  # Default: 5
```


* **Setting a duration:**
```python
tooltip.setDuration(1000)  # Default: 0
```
> The duration is the time in milliseconds after which the tooltip will start fading out again.
> If the duration is set to `0`, the tooltip will stay visible for as long as the widget is hovered.


* **Setting the offsets:**
```python
# Setting the offset for a specific placement
tooltip.setOffsetByPlacement(TooltipPlacement.LEFT, QPoint(-10, 5))

# Using a dict that specifies the offset for each placement you want to set
offsets = {
    TooltipPlacement.LEFT:   QPoint(-10, 5),
    TooltipPlacement.RIGHT:  QPoint(10, 5),
    TooltipPlacement.TOP:    QPoint(5, -10),
    TooltipPlacement.BOTTOM: QPoint(5, 10)
}
tooltip.setOffsets(offsets)

# Setting the offsets for all the placements to a single value
tooltip.setOffsetsAll(QPoint(10, 5))
```
> Each placement / side has its own offset to allow for full customizability.
> Each offset is a QPoint, which is made up of an x and y value.
> <br> By default, all the offsets are set to `QPoint(0, 0)`.


* **Adding delays to the fade in / out animations after hovering the widget:**
```python
tooltip.setShowDelay(500)  # Default: 50
tooltip.setHideDelay(500)  # Default: 50
```


* **Setting the durations of the fade in / out animations:**
```python
tooltip.setFadeInDuration(250)   # Default: 150
tooltip.setFadeOutDuration(250)  # Default: 150
```


* **Setting the border radius:**
```python
tooltip.setBorderRadius(0)   # Default: 2
```


* **Enabling or disabling the border:**
```python
tooltip.setBorderEnabled(True)   # Default: False
```


* **Setting custom colors:**
```python
tooltip.setBackgroundColor(QColor('#FCBA03'))   # Default: QColor('#111214')
tooltip.setTextColor(QColor('#000000'))         # Default: QColor('#CFD2D5')
tooltip.setBorderColor(QColor('#A38329'))       # Default: QColor('#403E41')
```


* **Setting a custom font:**
```python
tooltip.setFont(QFont('Consolas', 10))  # Default: QFont('Arial', 9, QFont.Weight.Bold)
```


* **Applying margins to the content of the tooltip:**
```python
tooltip.setMargins(QMargins(10, 8, 10, 8))  # Default: QMargins(12, 8, 12, 7)
```


* **Setting a maximum width:**
```python
tooltip.setMaximumWidth(150)  # Default: 16777215 (QWIDGETSIZE_MAX)
```


* **Enabling or disabling text centering for wrapped text:**
```python
tooltip.setTextCenteringEnabled(False)  # Default: True
```


* **Enabling or disabling the drop shadow:**
```python
tooltip.setDropShadowEnabled(False)  # Default: True
```


* **Changing the drop shadow strength:**
```python
tooltip.setDropShadowStrength(3.5)  # Default: 2.0
```


* **Making the tooltip translucent:**
```python
tooltip.setOpacity(0.8)  # Default: 1.0
```


**<br>Other customization options:**

| Option                      | Description                                                   | Default                    |
|-----------------------------|---------------------------------------------------------------|----------------------------|
| `setShowingOnDisabled()`    | Whether the tooltips should also be shown on disabled widgets | `False`                    |
| `setFadeInEasingCurve()`    | The easing curve of the fade in animation                     | `QEasingCurve.Type.Linear` |
| `setFadeOutEasingCurve()`   | The easing curve of the fade out animation                    | `QEasingCurve.Type.Linear` |
| `setMarginLeft()`           | Set left margin individually                                  | `12`                       |
| `setMarginRight()`          | Set right margin individually                                 | `12`                       |
| `setMarginTop()`            | Set top margin individually                                   | `8`                        |
| `setMarginBottom()`         | Set bottom margin individually                                | `7`                        |


## Demo

https://github.com/user-attachments/assets/fa768d30-f3cc-4883-aa8b-fed3a8824b23

The demos for PyQt5, PyQt6, and PySide6 can be found in the [demo](https://github.com/niklashenning/pyqttooltip/blob/master/demo) folder.

> To keep the demo simple, only the most important features are included.
> To get an overview of all the customization options, check out the documentation above.


## Tests
Installing the required test dependencies [PyQt6](https://pypi.org/project/PyQt6/), [pytest](https://github.com/pytest-dev/pytest), and [coveragepy](https://github.com/nedbat/coveragepy):
```
pip install PyQt6 pytest coverage
```

To run the tests with coverage, clone this repository, go into the main directory and run:
```
coverage run -m pytest
coverage report --ignore-errors -m
```

## License
This software is licensed under the [MIT license](https://github.com/niklashenning/pyqttooltip/blob/master/LICENSE).
