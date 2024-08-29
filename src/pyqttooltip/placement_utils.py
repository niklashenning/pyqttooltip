from qtpy.QtWidgets import QWidget
from .enums import TooltipPlacement
from .utils import Utils


class PlacementUtils:

    @staticmethod
    def get_optimal_placement(widget: QWidget) -> TooltipPlacement:
        top_level_parent = Utils.get_top_level_parent(widget)
        top_level_parent_pos = top_level_parent.pos()
        top_level_parent_geometry = top_level_parent.geometry()
        widget_pos = top_level_parent.mapToGlobal(widget.pos())

        # Calculate position that has the most available space
        left_space = widget_pos.x() - top_level_parent_pos.x()
        right_space = top_level_parent_geometry.right() - (widget_pos.x() + widget.width())
        top_space = widget_pos.y() - top_level_parent_pos.y()
        bottom_space = top_level_parent_geometry.bottom() - (widget_pos.y() + widget.height())
        max_space = max(left_space, right_space, top_space, bottom_space)

        if right_space == max_space:
            return TooltipPlacement.RIGHT
        elif left_space == max_space:
            return TooltipPlacement.LEFT
        elif top_space == max_space:
            return TooltipPlacement.TOP
        return TooltipPlacement.BOTTOM
