from qtpy.QtWidgets import QWidget, QApplication
from qtpy.QtCore import QRect, QSize, QPoint
from .enums import TooltipPlacement
from .utils import Utils


class PlacementUtils:

    @staticmethod
    def get_optimal_placement(widget: QWidget, size: QSize, triangle_size: int,
                              offsets: dict[TooltipPlacement, QPoint]) -> TooltipPlacement:
        top_level_parent = Utils.get_top_level_parent(widget)
        top_level_parent_pos = top_level_parent.pos()
        top_level_parent_geometry = top_level_parent.geometry()
        widget_pos = top_level_parent.mapToGlobal(widget.pos())

        # Calculate available space for placements
        left_space = widget_pos.x() - top_level_parent_pos.x()
        right_space = top_level_parent_geometry.right() - (widget_pos.x() + widget.width())
        top_space = widget_pos.y() - top_level_parent_pos.y()
        bottom_space = top_level_parent_geometry.bottom() - (widget_pos.y() + widget.height())
        space_placement_map = {
            right_space:  TooltipPlacement.RIGHT,
            left_space:   TooltipPlacement.LEFT,
            top_space:    TooltipPlacement.TOP,
            bottom_space: TooltipPlacement.BOTTOM
        }

        # Return most optimal placement that also fits on screen
        optimal_placement = None
        for space, placement in sorted(space_placement_map.items(), reverse=True):
            if not optimal_placement:
                optimal_placement = placement

            tooltip_rect = PlacementUtils.__get_tooltip_rect(
                widget, placement, size, triangle_size, offsets
            )
            if PlacementUtils.__rect_contained_by_screen(tooltip_rect):
                return placement

        return optimal_placement

    @staticmethod
    def get_fallback_placement(widget: QWidget, current_placement: TooltipPlacement, fallback_placements:
                               list[TooltipPlacement], size: QSize, triangle_size: int, offsets:
                               dict[TooltipPlacement, QPoint]) -> TooltipPlacement | None:
        tooltip_rect = PlacementUtils.__get_tooltip_rect(
            widget, current_placement, size, triangle_size, offsets
        )

        # Return None if current placement is valid
        if PlacementUtils.__rect_contained_by_screen(tooltip_rect):
            return None

        # Check all fallback placements and return first valid placement
        for placement in fallback_placements:
            if placement == current_placement or placement == TooltipPlacement.AUTO:
                continue
            tooltip_rect = PlacementUtils.__get_tooltip_rect(
                widget, placement, size, triangle_size, offsets
            )
            if PlacementUtils.__rect_contained_by_screen(tooltip_rect):
                return placement
        return None

    @staticmethod
    def __rect_contained_by_screen(rect: QRect) -> bool:
        for screen in QApplication.screens():
            if screen.geometry().contains(rect):
                return True
        return False

    @staticmethod
    def __get_tooltip_rect(widget: QWidget, placement: TooltipPlacement, size: QSize,
                           triangle_size: int, offsets: dict[TooltipPlacement, QPoint]) -> QRect:
        top_level_parent = Utils.get_top_level_parent(widget)
        widget_pos = top_level_parent.mapToGlobal(widget.pos())
        rect = QRect()

        if placement == TooltipPlacement.TOP:
            rect.setX(int(widget_pos.x() + widget.width() / 2 - size.width() / 2) + offsets[placement].x())
            rect.setY(widget_pos.y() - size.height() - triangle_size + offsets[placement].y())
            rect.setRight(rect.x() + size.width())
            rect.setBottom(rect.y() + size.height() + triangle_size)
        elif placement == TooltipPlacement.BOTTOM:
            rect.setX(int(widget_pos.x() + widget.width() / 2 - size.width() / 2) + offsets[placement].x())
            rect.setY(widget_pos.y() + widget.height() + offsets[placement].y())
            rect.setRight(rect.x() + size.width())
            rect.setBottom(rect.y() + size.height() + triangle_size)
        elif placement == TooltipPlacement.LEFT:
            rect.setX(widget_pos.x() - size.width() - triangle_size + offsets[placement].x())
            rect.setY(int(widget_pos.y() + widget.height() / 2 - size.width() / 2) + offsets[placement].y())
            rect.setRight(rect.x() + size.width() + triangle_size)
            rect.setBottom(rect.y() + size.height())
        elif placement == TooltipPlacement.RIGHT:
            rect.setX(widget_pos.x() + widget.width() + offsets[placement].x())
            rect.setY(int(widget_pos.y() + widget.height() / 2 - size.width() / 2) + offsets[placement].y())
            rect.setRight(rect.x() + size.width() + triangle_size)
            rect.setBottom(rect.y() + size.height())

        return rect
