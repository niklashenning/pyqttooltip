from qtpy.QtWidgets import QWidget, QApplication
from qtpy.QtCore import QRect, QSize
from .enums import TooltipPlacement
from .utils import Utils


class PlacementUtils:

    @staticmethod
    def get_optimal_placement(widget: QWidget, size: QSize, triangle_size: int) -> TooltipPlacement:
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
            TooltipPlacement.RIGHT:  right_space,
            TooltipPlacement.LEFT:   left_space,
            TooltipPlacement.TOP:    top_space,
            TooltipPlacement.BOTTOM: bottom_space
        }

        # Return most optimal placement that also fits on screen
        optimal_placement = None
        for placement, space in sorted(space_placement_map.items(), key=lambda item: item[1], reverse=True):
            if not optimal_placement:
                optimal_placement = placement
            tooltip_rect = PlacementUtils.__get_tooltip_rect(widget, placement, size, triangle_size)
            if PlacementUtils.__rect_contained_by_screen(tooltip_rect):
                return placement

        return optimal_placement

    @staticmethod
    def get_fallback_placement(widget: QWidget, current_placement: TooltipPlacement,
                               fallback_placements: list[TooltipPlacement], size: QSize,
                               triangle_size: int) -> TooltipPlacement | None:
        tooltip_rect = PlacementUtils.__get_tooltip_rect(widget, current_placement,
                                                         size, triangle_size)

        # Return None if current placement is valid
        if PlacementUtils.__rect_contained_by_screen(tooltip_rect):
            return None

        # Check all fallback placements and return first valid placement
        for placement in fallback_placements:
            if placement == current_placement or placement == TooltipPlacement.AUTO:
                continue
            tooltip_rect = PlacementUtils.__get_tooltip_rect(widget, placement,
                                                             size, triangle_size)
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
    def __get_tooltip_rect(widget: QWidget, placement: TooltipPlacement,
                           size: QSize, triangle_size: int) -> QRect:
        top_level_parent = Utils.get_top_level_parent(widget)
        widget_pos = top_level_parent.mapToGlobal(widget.pos())
        rect = QRect()

        if placement == TooltipPlacement.TOP:
            rect.setX(int(widget_pos.x() + widget.width() / 2 - size.width() / 2))
            rect.setY(widget_pos.y() - size.height() - triangle_size)
        elif placement == TooltipPlacement.BOTTOM:
            rect.setX(int(widget_pos.x() + widget.width() / 2 - size.width() / 2))
            rect.setY(widget_pos.y() + widget.height())
        elif placement == TooltipPlacement.LEFT:
            rect.setX(widget_pos.x() - size.width() - triangle_size)
            rect.setY(int(widget_pos.y() + widget.height() / 2 - size.width() / 2))
        elif placement == TooltipPlacement.RIGHT:
            rect.setX(widget_pos.x() + widget.width())
            rect.setY(int(widget_pos.y() + widget.height() / 2 - size.width() / 2))

        rect.setRight(rect.x() + size.width() + triangle_size)
        rect.setBottom(rect.y() + size.height() + triangle_size)
        return rect
