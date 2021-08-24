# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, Request
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from models.operation_log import OperationLog, ListOfOperationLogInResponse
from db.crud.operation_log import OperationLog as OperationLogCRUD
from services.localization import get_gettext

router = APIRouter()


@router.get("/operation_logs", response_model=ListOfOperationLogInResponse)
async def list_operation_log(
    request: Request,
    skip: int = Query(0, ge=0, title="which page"),
    limit: int = Query(20, gt=0, le=100, title="Page size"),
    _=Depends(get_gettext),
) -> ListOfOperationLogInResponse:
    operation_log_crud = OperationLogCRUD(request.app.state.pgpool)
    operation_logs, count = await operation_log_crud.list_operation_log(offset=skip, limit=limit)

    return ListOfOperationLogInResponse(data=operation_logs, count=count)
