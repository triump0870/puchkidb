"""
PuchkiDB stores differrent types of python data types using a configurable
backend. It has support for handy querying and tables.

.. codeauthor:: Rohan Roy <rohan@rohanroy.com>

Usage example:

>>> from puchkidb. import PuchkiDB, where
>>> from puchkidb.storages import MemoryStorage
>>> db = PuchkiDB(storage=MemoryStorage)
>>> db.insert({'data': 5})  # Insert into '_default' table
>>> db.search(where('data') == 5)
[{'data': 5, '_id': 1}]
>>> # Now let's create a new table
>>> tbl = db.table('our_table')
>>> for i in range(10):
...     tbl.insert({'data': i})
...
>>> len(tbl.search(where('data') < 5))
5
"""

from .queries import Query, where
from .storages import Storage, JSONStorage
from .database import PuchkiDB
from .version import __version__

__all__ = ('PuchkiDB', 'Storage', 'JSONStorage', 'Query', 'where')
