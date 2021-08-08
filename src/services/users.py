# -*- coding: utf-8 -*-

from fastapi import Request

from db.crud.users import User as UserCRUD
from services.operation_log import set_new_data_id
from models.errors import HttpClientError

async def add_user(request: Request, info: dict, _):
    user_crud = UserCRUD(request.app.state.pgpool)

    # TODO get user by username

    # TODO get user by email

    user = await user_crud.add_user(
        username=info.username,
        password=info.password,
        email=info.email)

    # for oplog
    await set_new_data_id(request, user.id)     # user.json()

    return user

