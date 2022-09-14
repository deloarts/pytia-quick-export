"""
    Lazy loader for the UI.
"""

import atexit
import os
import time
from pathlib import Path

from pytia.exceptions import (PytiaDocumentNotSavedError,
                              PytiaWrongDocumentTypeError)
from pytia.log import log
from resources import resource


class LazyDocumentHelper:
    """
    Helper class for late imports of any kind of methods related to handle document operations.

    Important: This class loads the current document only once (on instantiation). If the
    document changes all operations will be made on the original document.

    Use the ensure_doc_not_changed method if you're not sure if the part hasn't changed.
    """

    def __init__(self) -> None:
        # Import the PyPartDocument after the GUI exception handler is initialized.
        # Otherwise the CATIA-not-running-exception will not be caught.
        # Also: The UI will load a little bit faster.

        start_time = time.perf_counter()
        # pylint: disable=C0415
        from pytia.framework import framework

        # pylint: enable=C0415

        self.framework = framework
        self.lazy_document = framework.catia.active_document
        self.is_part = self.lazy_document.is_part
        self.is_document = self.lazy_document.is_product

        self._lock_catia(True)
        atexit.register(lambda: self._lock_catia(False))

        if not resource.settings.restrictions.allow_unsaved and not os.path.isabs(
            self.lazy_document.full_name
        ):
            raise PytiaDocumentNotSavedError(
                "It is not allowed to edit the parameters of an unsaved document. "
                "Please save the document first."
            )

        if self.lazy_document.is_part:
            # pylint: disable=C0415
            from pytia.wrapper.documents.part_documents import PyPartDocument

            # pylint: enable=C0415

            self.document = PyPartDocument(strict_naming=False)
            log.debug("Current document is a CATPart.")

        elif self.lazy_document.is_product:
            # pylint: disable=C0415
            from pytia.wrapper.documents.product_documents import \
                PyProductDocument

            # pylint: enable=C0415

            self.document = PyProductDocument(strict_naming=False)
            log.debug("Current document is a CATProduct.")

        else:
            raise PytiaWrongDocumentTypeError(
                "The current document is neither a part nor a product."
            )

        end_time = time.perf_counter()
        log.debug(f"Loaded PyPartDocument in {(end_time-start_time):.4f}s")

        self.document.current()
        self.document.product.part_number = self.document.document.name.split(".CATP")[
            0
        ]
        self.name = self.document.document.name

    @property
    def path(self) -> Path:
        """Returns the documents absolute path with filename and file extension."""
        return Path(self.document.document.full_name)

    @property
    def folder(self) -> Path:
        """Returns the folder as absolute path in which this document is saved."""
        return Path(self.path).parent

    @property
    def partnumber(self) -> str:
        """Returns the part number of the document."""
        return self.document.product.part_number


    def _lock_catia(self, value: bool) -> None:
        """
        Sets the lock-state of catia.

        Args:
            value (bool): True: Locks the catia UI, False: Releases the lock.
        """
        log.debug(f"Setting catia lock to {value!r}")
        self.framework.catia.refresh_display = not value
        self.framework.catia.interactive = not value
        self.framework.catia.display_file_alerts = value
        self.framework.catia.undo_redo_lock = value
        if value:
            self.framework.catia.disable_new_undo_redo_transaction()
        else:
            self.framework.catia.enable_new_undo_redo_transaction()
