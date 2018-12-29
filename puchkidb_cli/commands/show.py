from json import dumps

from .base import Base


class Show(Base):
    """Show the databases and the tables using this command.
    Usage:
        puchkidb show [options]

    options:
        dbs:    show all the databases in the server
        tables: show all the tables inside a database

    Example:
        puchkidb show dbs
    """

    def run(self):
        print('Hello, world!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
