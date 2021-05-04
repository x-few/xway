# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, Request
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from models.operation_log import OperationLog, ListOfOperationLogInResponse
from db.crud.operation_log import OperationLog as OperationLogCRUD
from services.localization import get_gettext


router = APIRouter()

@router.get("/oplogs", response_model=ListOfOperationLogInResponse)
async def get_users(
    request: Request,
    skip: int = Query(0, ge=0, title="which page"),
    limit: int = Query(20, gt=0, le=100, title="Page size"),
    _ = Depends(get_gettext),
) -> ListOfOperationLogInResponse:
    oplog_crud = OperationLogCRUD(request.app.state.pgpool)
    current_user = request.state.current_user
    owner = current_user.owner or current_user.id
    print("current_user.owner = ", current_user.owner)
    oplogs, count = await oplog_crud.get_oplog_by_owner(owner=owner, offset=skip, limit=limit)

    return ListOfOperationLogInResponse(data=oplogs, count=count)