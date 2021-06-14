# -*- coding: utf-8 -*-

from fastapi import Request

from db.crud.user import User as UserCRUD
from services.operation_log import set_new_data_id
from models.errors import HttpClientError


async def get_owner(current_user):
    return current_user.owner or current_user.id


async def add_user(request: Request, info: dict, typ: int):
    owner = 0
    creator = 0
    if typ == 2:
        current_user = request.state.current_user
        if not current_user:
            raise HttpClientError()
        owner = await get_owner(current_user)
        creator = current_user.id

    user_crud = UserCRUD(request.app.state.pgpool)
    user = await user_crud.add_user( \
        username=info.username, password=info.password, \
        creator=creator, owner=owner, typ=info.typ, email=info.email)

    # for oplog
    await set_new_data_id(request, user.id)     # user.json()

    return user

