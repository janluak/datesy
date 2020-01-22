import logging
from ._db_helper import *
import mysql.connector

__doc__ = "The mysql module presents a simple I/O interaction for MySQL databases"

__all__ = ["MySQL"]


class _MySQLTable(Table):
    def __init__(self, table_name, database):
        # MySQL specifics
        self._schema_update_query = f"DESCRIBE {table_name}"
        self._query_unequals = "<>"

        super().__init__(table_name, database)

    def _query_contains(self, column, value, boolean):
        if boolean:
            return f"(`{column}` LIKE '%{value}%')"
        else:
            return f"(`{column}` NOT LIKE '%{value}%')"

    def _query_null(self, column, boolean):
        if boolean:
            return f"(`{column}` IS NULL)"
        else:
            return f"(`{column}` IS NOT NULL)"


class MySQL(Database):
    def __init__(self, host, user, password, database, port=3306, auto_creation=False):
        # MySQL specifics
        self._table_update_query = f"SHOW tables"

        super().__init__(host, port, user, password, database, auto_creation)

    def _connect_to_db(self):
        self._conn = mysql.connector.connect(host=self._host, user=self._user, passwd=self._password, db=self._database)
        self._cursor = self._conn.cursor()

    def _constructor(self):
        self._check_auto_creation()
        for table_name in self.tables:
            setattr(self, table_name, _MySQLTable(table_name, self))

    def table(self, table_name):
        return _MySQLTable(table_name, self)



