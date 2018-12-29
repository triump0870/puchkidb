"""
Contains the :class:`database <puchkidb.database.PuchkiDB>` and
:class:`tables <puchkidb.database.Table>` implementation.
"""
# Python 2/3 independent Mapping import
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
import warnings


class Document(dict):
    """
    Represents a document stored in the database.

    This is a transparent proxy for database records. It exists
    to provide a way to access a record's id via ``el.doc_id``.
    """

    def __init__(self, value, doc_id, **kwargs):
        super(Document, self).__init__(**kwargs)

        self.update(value)
        self.doc_id = doc_id

    @property
    def eid(self):
        warnings.warn('eid has been renamed to doc_id', DeprecationWarning)
        return self.doc_id


Element = Document
