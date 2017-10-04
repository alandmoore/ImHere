"""
This is the data model for the signin application.
"""

import sqlite3 as sql
from datetime import datetime

db_create_queries = [
    """CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    has_appointment INTEGER,
    appointment_time TEXT,
    signin_time TEXT,
    helped_time TEXT,
    helped_by TEXT,
    expired INTEGER
    );""",
    """CREATE VIEW customers_rept AS
    SELECT name,
    CASE WHEN has_appointment THEN appointment_time
    ELSE 'walk-in' END AS appointment,
    signin_time,
    helped_time,
    helped_by
    FROM customers
    ;
    """
]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Model(object):

    def __init__(self, dbfile):
        """Construct the model.

        Takes a path to the db file.
        """

        self.dbpath = dbfile
        self.cx = sql.connect(self.dbpath)
        self.cx.row_factory = dict_factory
        self._cursor = None

        # see if the database has been built
        built = self.query(
            """SELECT * FROM sqlite_master
            WHERE type='table' AND name='customers'"""
        )
        if not built:
            self.__build_db()

    def query(self, query, parameters=None):
        """Run a query on the database, optionally with parameters"""

        if parameters:
            self.cursor().execute(query, parameters)
        else:
            self.cursor().execute(query)
        self.cx.commit()
        return self.cursor().fetchall()

    def cursor(self):
        if not self._cursor:
            self._cursor = self.cx.cursor()
        return self._cursor

    def __build_db(self):
        """Construct the database tables and objects"""
        return all([
            self.query(db_create_query)
            for db_create_query in db_create_queries
        ])

    ####################
    # Public Callbacks #
    ####################

    def submit_customer(self, **kwargs):
        """Enter a customer into the db"""
        print(kwargs)

        params = {
            "name": kwargs.get("name", ["unknown"])[0],
            "has_appointment": (
                1 if (kwargs.get("has_appointment", ['0'])[0] == '1')
                else 0
            ),
            "appointment_time": kwargs.get("appointment_time", [None])[0],
            "signin_time": datetime.now().isoformat()
        }

        query = """
        INSERT INTO customers
            (name, has_appointment, appointment_time, signin_time, expired)
        VALUES (:name, :has_appointment, :appointment_time, :signin_time, 0)
        """
        return self.query(query, params)

    def list_customers(self):
        """Return a list of all customers in the table"""

        query = """SELECT * FROM customers WHERE expired=0 ORDER BY id ASC"""
        return self.query(query)

    def customer_dump(self):
        """Return all customer data for reporting"""
        query = """SELECT * FROM customers_rept ORDER BY signin_time ASC"""

        return self.query(query)

    def table_headers(self, table="customers"):
        """Return the table column names"""
        raw = self.cursor().execute('SELECT * FROM "{}" LIMIT 1'.format(table))
        return [x[0] for x in raw.description]

    def clear_old_customers(
            self,
            claim_limit='30 minutes',
            unclaim_limit='8 hours'
    ):
        """Remove customer entries from the database if customers:

          - have been claimed more than <claim_limit> minutes ago
          - signed in more than unclaim_limit ago.
        """
        # we need to make these negative values
        data = {
            "claim_limit": "-" + claim_limit,
            "unclaim_limit": "-" + unclaim_limit
        }

        query = """UPDATE  customers SET expired=1
        WHERE (helped_time IS NOT NULL
              AND datetime(helped_time)
              < datetime('now', :claim_limit, 'localtime')
              )
        OR (helped_time IS NULL
            AND datetime(signin_time)
            < datetime('now', :unclaim_limit, 'localtime')
             )
        """

        self.query(query, data)

    def claim_customer(self, **kwargs):
        """Claim a customer id"""

        myname = kwargs.get("myname", ["Unknown"])[0]
        customer_id = kwargs.get("customer_id", [None])[0]

        if not customer_id:
            return False
        else:
            customer_id = int(customer_id)

        query = """UPDATE customers
        SET helped_time=:helped_time, helped_by=:myname
        WHERE id=:customer_id
        """
        data = {
            "helped_time": datetime.now().isoformat(),
            "myname": myname,
            "customer_id": customer_id
        }

        return self.query(query, data)

    def unclaim_customer(self, **kwargs):
        """Remove a claim on a customer"""
        customer_id = kwargs.get("customer_id", [None])[0]

        if not customer_id:
            return False
        else:
            customer_id = int(customer_id)

        query = """UPDATE customers SET helped_time=NULL, helped_by=NULL
        WHERE id=:customer_id"""

        return self.query(query, {"customer_id": customer_id})
