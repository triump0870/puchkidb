import pytest

from puchkidb.middlewares import CachingMiddleware
from puchkidb.storages import MemoryStorage
from puchkidb import PuchkiDB


@pytest.fixture
def db():
    db_ = PuchkiDB(storage=MemoryStorage)
    db_.purge_tables()
    db_.insert_multiple({'int': 1, 'char': c} for c in 'abc')
    return db_


@pytest.fixture
def storage():
    _storage = CachingMiddleware(MemoryStorage)
    return _storage()  # Initialize MemoryStorage
