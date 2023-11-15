"""
This file defines the interface between python and the Rust SurrealDB library for logging in.
"""
from typing import Dict, Optional

from surrealdb.rust_surrealdb import blocking_authenticate
from surrealdb.rust_surrealdb import blocking_sign_in
from surrealdb.rust_surrealdb import blocking_sign_up

from surrealdb.errors import SurrealDbError
from surrealdb.asyncio_runtime import AsyncioRuntime


class SignInMixin:
    """
    This class is responsible for the interface between python and the Rust SurrealDB library for logging in.
    """
    def signin(self: "SurrealDB", data: Optional[Dict[str, str]] = None) -> None:
        """
        Signs in to the database.

        :param password: the password to sign in with
        :param username: the username to sign in with

        :return: None
        """
        async def _signin(connection, password, username):
            return await blocking_sign_in(connection, password, username)

        if data is None:
            data = dict()
        data = {key.lower(): value for key, value in data.items()}

        password: str = data.get("password", data.get("pass", data.get("p", "root")))
        username: str = data.get("username", data.get("user", data.get("u", "root")))

        try:
            loop_manager = AsyncioRuntime()
            loop_manager.loop.run_until_complete(_signin(self._connection, password, username))
        except Exception as e:
            SurrealDbError(e)

    def signup(self: "SurrealDB", namespace: str, database: str, data: Optional[Dict[str, str]] = None) -> str:
        """
        Signs up to an auth scope within a namespace and database.

        :param namespace: the namespace the auth scope is associated with
        :param database: the database the auth scope is associated with
        :param data: the data to sign up with
        :return: an JWT for that auth scope
        """
        async def _signup(connection, data, namespace, database):
            return await blocking_sign_up(connection, data, namespace, database)

        try:
            loop_manager = AsyncioRuntime()
            return loop_manager.loop.run_until_complete(_signup(self._connection, data, namespace, database))
        except Exception as e:
            SurrealDbError(e)

    def authenticate(self: "SurrealDB", jwt: str) -> bool:
        """
        Authenticates a JWT.

        :param jwt: the JWT to authenticate
        :return: None
        """
        async def _authenticate(connection, jwt):
            return await blocking_authenticate(connection, jwt)

        try:
            loop_manager = AsyncioRuntime()
            return loop_manager.loop.run_until_complete(_authenticate(self._connection, jwt))
        except Exception as e:
            SurrealDbError(e)
