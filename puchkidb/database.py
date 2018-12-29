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

from . import JSONStorage


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


class PuchkiDB(object):
    """
    The main class of PuchkiDB.

    Gives access to the database, provides methods to insert/search/remove
    and getting tables.
    """

    DEFAULT_TABLE = '_default'
    DEFAULT_STORAGE = JSONStorage

    def __init__(self, *args, **kwargs):
        """
        Create a new instance of PuchkiDB.

        All arguments and keyword arguments will be passed to the underlying
        storage class (default: :class:`~puchkidb.storages.JSONStorage`).

        :param storage: The class of the storage to use. Will be initialized
                        with ``args`` and ``kwargs``.
        :param default_table: The name of the default table to populate.
        """

        storage = kwargs.pop('storage', self.DEFAULT_STORAGE)
        default_table = kwargs.pop('default_table', self.DEFAULT_TABLE)
        self._cls_table = kwargs.pop('table_class', self.table_class)
        self._cls_storage_proxy = kwargs.pop('storage_proxy_class',
                                             self.storage_proxy_class)

        # Prepare the storage
        #: :type: Storage
        self._storage = storage(*args, **kwargs)

        self._opened = True

        # Prepare the default table

        self._table_cache = {}
        self._table = self.table(default_table)

    def __repr__(self):
        args = [
            'tables={}'.format(list(self.tables())),
            'tables_count={}'.format(len(self.tables())),
            'default_table_documents_count={}'.format(self.__len__()),
            'all_tables_documents_count={}'.format(
                ['{}={}'.format(table, len(self.table(table))) for table in self.tables()]),
        ]

        return '<{} {}>'.format(type(self).__name__, ', '.join(args))

    def table(self, name=DEFAULT_TABLE, **options):
        """
        Get access to a specific table.

        Creates a new table, if it hasn't been created before, otherwise it
        returns the cached :class:`~puchkidb.Table` object.

        :param name: The name of the table.
        :type name: str
        :param cache_size: How many query results to cache.
        :param table_class: Which table class to use.
        """

        if name in self._table_cache:
            return self._table_cache[name]

        table_class = options.pop('table_class', self._cls_table)
        table = table_class(self._cls_storage_proxy(self._storage, name), name, **options)

        self._table_cache[name] = table

        return table

    def tables(self):
        """
        Get the names of all tables in the database.

        :returns: a set of table names
        :rtype: set[str]
        """

        return set(self._storage.read())

    def purge_tables(self):
        """
        Purge all tables from the database. **CANNOT BE REVERSED!**
        """

        self._storage.write({})
        self._table_cache.clear()

    def purge_table(self, name):
        """
        Purge a specific table from the database. **CANNOT BE REVERSED!**

        :param name: The name of the table.
        :type name: str
        """
        if name in self._table_cache:
            del self._table_cache[name]

        proxy = StorageProxy(self._storage, name)
        proxy.purge_table()

    def close(self):
        """
        Close the database.
        """
        self._opened = False
        self._storage.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._opened:
            self.close()

    def __getattr__(self, name):
        """
        Forward all unknown attribute calls to the underlying standard table.
        """
        return getattr(self._table, name)

    # Methods that are executed on the default table
    # Because magic methods are not handled by __getattr__ we need to forward
    # them manually here

    def __len__(self):
        """
        Get the total number of documents in the default table.

        >>> db = PuchkiDB('db.json')
        >>> len(db)
        0
        """
        return len(self._table)

    def __iter__(self):
        """
        Iter over all documents from default table.
        """
        return self._table.__iter__()
