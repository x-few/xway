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
    offset: int = Query(0, ge=0, title="which page"),
    limit: int = Query(20, gt=0, le=100, title="Page size"),
    _ = Depends(get_gettext),
) -> ListOfOperationLogInResponse:
    oplog_crud = OperationLogCRUD(request.app.state.pgpool)
    # TODO get owner id
    owner = 1
    oplogs, count = await oplog_crud.get_oplog_by_owner(owner=owner, offset=offset, limit=offset)

    return ListOfOperationLogInResponse(data=oplogs, count=count)