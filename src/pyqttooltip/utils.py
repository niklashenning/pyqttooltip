from qtpy.QtWidgets import QWidget


class Utils:

    @staticmethod
    def get_top_level_parent(widget: QWidget) -> QWidget:
        if widget.parent() is None:
            return widget

        parent = widget.parent()

        while parent.parent() is not None:
            parent = parent.parent()
        return parent

    @staticmethod
    def get_parents(widget: QWidget) -> list[QWidget]:
        parents = []

        while widget.parent() is not None:
            parents.append(widget.parent())
            widget = widget.parent()
        return parents
