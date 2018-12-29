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


def _get_doc_id(doc_id, eid):
    # Backwards-compatibility shim
    if eid is not None:
        if doc_id is not None:
            raise TypeError('cannot pass both eid and doc_id')

        warnings.warn('eid has been renamed to doc_id', DeprecationWarning)
        return eid
    else:
        return doc_id


def _get_doc_ids(doc_ids, eids):
    # Backwards-compatibility shim
    if eids is not None:
        if doc_ids is not None:
            raise TypeError('cannot pass both eids and doc_ids')

        warnings.warn('eids has been renamed to doc_ids', DeprecationWarning)
        return eids
    else:
        return doc_ids


class DataProxy(dict):
    """
    A proxy to a table's data that remembers the storage's
    data dictionary.
    """

    def __init__(self, table, raw_data, **kwargs):
        super(DataProxy, self).__init__(**kwargs)
        self.update(table)
        self.raw_data = raw_data


class StorageProxy(object):
    """
    A proxy that only allows to read a single table from a
    storage.
    """

    def __init__(self, storage, table_name):
        self._storage = storage
        self._table_name = table_name

    def _new_document(self, key, val):
        doc_id = int(key)
        return Document(val, doc_id)

    def read(self):
        raw_data = self._storage.read() or {}

        try:
            table = raw_data[self._table_name]
        except KeyError:
            raw_data.update({self._table_name: {}})
            self._storage.write(raw_data)

            return DataProxy({}, raw_data)

        docs = {}
        for key, val in iteritems(table):
            doc = self._new_document(key, val)
            docs[doc.doc_id] = doc

        return DataProxy(docs, raw_data)

    def write(self, data):
        try:
            # Try accessing the full data dict from the data proxy
            raw_data = data.raw_data
        except AttributeError:
            # Not a data proxy, fall back to regular reading
            raw_data = self._storage.read()

        raw_data[self._table_name] = dict(data)
        self._storage.write(raw_data)

    def purge_table(self):
        try:
            data = self._storage.read() or {}
            del data[self._table_name]
            self._storage.write(data)
        except KeyError:
            pass
