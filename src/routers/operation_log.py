# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, Request
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from models.operation_log import OperationLog, ListOfOperationLogInResponse
from db.crud.operation_log import OperationLog as OperationLogCRUD
from services.localization import get_gettext
from services.user import get_owner


router = APIRouter()

@router.get("/oplogs", response_model=ListOfOperationLogInResponse)
async def get_oplogs(
    request: Request,
    skip: int = Query(0, ge=0, title="which page"),
    limit: int = Query(20, gt=0, le=100, title="Page size"),
    _ = Depends(get_gettext),
) -> ListOfOperationLogInResponse:
    owner = await get_owner(request.state.current_user)
    oplog_crud = OperationLogCRUD(request.app.state.pgpool)
    oplogs, count = await oplog_crud.get_oplog_by_owner(owner=owner, offset=skip, limit=limit)

    return ListOfOperationLogInResponse(data=oplogs, count=count)


@router.put("/rollback/{oplog_id}", status_code=HTTP_204_NO_CONTENT,)
async def rollback(
    request: Request,
    oplog_id: int = Path(..., title="The ID of the oplog"),
):
    current_user = request.state.current_user
    owner = await get_owner(current_user)
    oplog_crud = OperationLogCRUD(request.app.state.pgpool)
    await oplog_crud.rollback(id=oplog_id, owner=owner, creator=current_user.id)