"""
Example 23
Snapshot transactions

Explanations about locks: https://www.exasol.com/support/browse/SOL-214
"""

import pyexasol
import _config as config

import pprint
printer = pprint.PrettyPrinter(indent=4, width=140)

# First connection, read first table, update second table
C1 = pyexasol.connect(dsn=config.dsn, user=config.user, password=config.password, schema=config.schema)
C1.set_autocommit(False)

C1.execute("SELECT * FROM TAB1")
C1.execute("INSERT INTO TAB2 VALUES (1)")

# Second connection, update first table
C2 = pyexasol.connect(dsn=config.dsn, user=config.user, password=config.password, schema=config.schema)
C2.set_autocommit(False)

C2.execute("INSERT INTO TAB1 VALUES(1)")
C2.commit()

# Third connection, read second table
C3 = pyexasol.connect(dsn=config.dsn, user=config.user, password=config.password, schema=config.schema,
                      snapshot_transactions=True, debug=True)

# Exasol locks on this query without snapshot transactions
stmt = C3.execute("SELECT column_name, column_type FROM EXA_ALL_COLUMNS WHERE column_schema=CURRENT_SCHEMA AND column_table='TAB2'")
printer.pprint(stmt.fetchall())
