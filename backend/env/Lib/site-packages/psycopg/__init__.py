"""
psycopg -- PostgreSQL database adapter for Python
"""

# Copyright (C) 2020 The Psycopg Team

import logging

from . import pq  # noqa: F401 import early to stabilize side effects
from . import dbapi20, postgres, types
from ._capabilities import Capabilities, capabilities
from ._column import Column
from ._connection_base import BaseConnection, Notify
from ._connection_info import ConnectionInfo
from ._enums import IsolationLevel
from ._pipeline import Pipeline
from ._pipeline_async import AsyncPipeline
from ._server_cursor import ServerCursor
from ._server_cursor_async import AsyncServerCursor
from ._tpc import Xid
from .client_cursor import AsyncClientCursor, ClientCursor
from .connection import Connection
from .connection_async import AsyncConnection
from .copy import AsyncCopy, Copy
from .cursor import Cursor
from .cursor_async import AsyncCursor
from .dbapi20 import (
    BINARY,
    DATETIME,
    NUMBER,
    ROWID,
    STRING,
    Binary,
    Date,
    DateFromTicks,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
)
from .errors import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)
from .raw_cursor import AsyncRawCursor, AsyncRawServerCursor, RawCursor, RawServerCursor
from .transaction import AsyncTransaction, Rollback, Transaction
from .version import __version__ as __version__  # noqa: F401

# Set the logger to a quiet default, can be enabled if needed
if (logger := logging.getLogger("psycopg")).level == logging.NOTSET:
    logger.setLevel(logging.WARNING)

# DBAPI compliance
connect = Connection.connect
apilevel = "2.0"
threadsafety = 2
paramstyle = "pyformat"

# register default adapters for PostgreSQL
adapters = postgres.adapters  # exposed by the package
postgres.register_default_types(adapters.types)
postgres.register_default_adapters(adapters)

# After the default ones, because these can deal with the bytea oid better
dbapi20.register_dbapi20_adapters(adapters)

# Must come after all the types have been registered
types.array.register_all_arrays(adapters)

# Note: defining the exported methods helps both Sphynx in documenting that
# this is the canonical place to obtain them and should be used by MyPy too,
# so that function signatures are consistent with the documentation.
__all__ = [
    "AsyncClientCursor",
    "AsyncConnection",
    "AsyncCopy",
    "AsyncCursor",
    "AsyncPipeline",
    "AsyncRawCursor",
    "AsyncRawServerCursor",
    "AsyncServerCursor",
    "AsyncTransaction",
    "BaseConnection",
    "Capabilities",
    "capabilities",
    "ClientCursor",
    "Column",
    "Connection",
    "ConnectionInfo",
    "Copy",
    "Cursor",
    "IsolationLevel",
    "Notify",
    "Pipeline",
    "RawCursor",
    "RawServerCursor",
    "Rollback",
    "ServerCursor",
    "Transaction",
    "Xid",
    # DBAPI exports
    "connect",
    "apilevel",
    "threadsafety",
    "paramstyle",
    "Warning",
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "OperationalError",
    "IntegrityError",
    "InternalError",
    "ProgrammingError",
    "NotSupportedError",
    # DBAPI type constructors and singletons
    "Binary",
    "Date",
    "DateFromTicks",
    "Time",
    "TimeFromTicks",
    "Timestamp",
    "TimestampFromTicks",
    "BINARY",
    "DATETIME",
    "NUMBER",
    "ROWID",
    "STRING",
]
