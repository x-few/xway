import asyncpg
from fastapi import FastAPI, Depends
from loguru import logger
from config.config import POSTGRESQL as pgconfig
from asyncpg.connection import Connection
from asyncpg.pool import Pool
from starlette.requests import Request
from typing import AsyncGenerator, Callable, Type

async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to postgres://{}:{}@{}:{}/{}",
        pgconfig['user'], pgconfig['password'],
        pgconfig['host'], pgconfig['port'], pgconfig['database'])

    try:
        app.state.pgpool = await asyncpg.create_pool(**pgconfig)
        logger.info("Connection established")
    except ConnectionRefusedError:
        app.state.pgpool = None
        logger.error("Connection Refused")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    if app.state.pgpool is None:
        logger.warning("Connection not found")
    else:
        await app.state.pgpool.close()

    logger.info("Connection closed")
