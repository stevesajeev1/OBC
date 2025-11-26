"""
psycopg client-side binding cursors
"""

# Copyright (C) 2022 The Psycopg Team

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from . import adapt
from . import errors as e
from . import pq
from ._cursor_base import BaseCursor
from ._preparing import Prepare
from ._queries import PostgresClientQuery, PostgresQuery
from .abc import ConnectionType, Params, Query
from .cursor import Cursor
from .cursor_async import AsyncCursor
from .rows import Row

if TYPE_CHECKING:
    from typing import Any  # noqa: F401

    from .connection import Connection  # noqa: F401
    from .connection_async import AsyncConnection  # noqa: F401

TEXT = pq.Format.TEXT
BINARY = pq.Format.BINARY


class ClientCursorMixin(BaseCursor[ConnectionType, Row]):
    _query_cls = PostgresClientQuery

    def mogrify(self, query: Query, params: Params | None = None) -> str:
        """
        Return the query and parameters merged.

        Parameters are adapted and merged to the query the same way that
        `!execute()` would do.

        """
        self._tx = adapt.Transformer(self)
        pgq = self._convert_query(query, params)
        return pgq.query.decode(self._tx.encoding)

    def _execute_send(
        self,
        query: PostgresQuery,
        *,
        force_extended: bool = False,
        binary: bool | None = None,
    ) -> None:
        if binary is None:
            fmt = self.format
        else:
            fmt = BINARY if binary else TEXT

        if fmt == BINARY:
            raise e.NotSupportedError(
                "client-side cursors don't support binary results"
            )

        self._query = query

        if self._conn._pipeline:
            # In pipeline mode always use PQsendQueryParams - see #314
            # Multiple statements in the same query are not allowed anyway.
            self._conn._pipeline.command_queue.append(
                partial(self._pgconn.send_query_params, query.query, None)
            )
        elif force_extended:
            self._pgconn.send_query_params(query.query, None)
        else:
            # If we can, let's use simple query protocol,
            # as it can execute more than one statement in a single query.
            self._pgconn.send_query(query.query)

    def _get_prepared(
        self, pgq: PostgresQuery, prepare: bool | None = None
    ) -> tuple[Prepare, bytes]:
        return (Prepare.NO, b"")


class ClientCursor(ClientCursorMixin["Connection[Any]", Row], Cursor[Row]):
    __module__ = "psycopg"


class AsyncClientCursor(
    ClientCursorMixin["AsyncConnection[Any]", Row], AsyncCursor[Row]
):
    __module__ = "psycopg"
