from enum import Enum


class TooltipPlacement(Enum):
    AUTO = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


class TooltipTrigger(Enum):
    HOVER = 0
    FOCUS = 1
