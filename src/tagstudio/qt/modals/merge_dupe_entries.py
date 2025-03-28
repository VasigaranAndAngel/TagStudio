# Copyright (C) 2024 Travis Abendshien (CyanVoxel).
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio


import typing

from PySide6.QtCore import QObject, Signal

from tagstudio.core.library.alchemy.library import Library
from tagstudio.core.utils.dupe_files import DupeRegistry
from tagstudio.qt.translations import Translations
from tagstudio.qt.widgets.progress import ProgressWidget

# Only import for type checking/autocompletion, will not be imported at runtime.
if typing.TYPE_CHECKING:
    from tagstudio.qt.ts_qt import QtDriver


class MergeDuplicateEntries(QObject):
    done = Signal()

    def __init__(self, library: "Library", driver: "QtDriver"):
        super().__init__()
        self.lib = library
        self.driver = driver
        self.tracker = DupeRegistry(library=self.lib)

    def merge_entries(self):
        pw = ProgressWidget(
            cancel_button_text=None,
            minimum=0,
            maximum=self.tracker.groups_count,
        )
        pw.setWindowTitle(Translations["entries.duplicate.merge.label"])
        pw.update_label(Translations["entries.duplicate.merge.label"])

        pw.from_iterable_function(self.tracker.merge_dupe_entries, None, self.done.emit)
