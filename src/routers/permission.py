from fastapi import APIRouter, Depends, Path, Query, Body, Request
from starlette.status import HTTP_201_CREATED

from models.permission import PermissionInCreate, \
    PermissionListInResponse, \
    PermissionInResponse, \
    PermissionInUpdate
from db.crud.permission import Permission as PermissionCRUD
from models.errors import HttpClientError, HttpNotFound
from services.localization import get_gettext

router = APIRouter()


@router.get("/permissions", response_model=PermissionListInResponse)
async def list_permissions(
    request: Request,
    page: int = Query(1, ge=1, title="which page"),
    pagesize: int = Query(20, ge=1, le=100, title="Page size"),
    _=Depends(get_gettext),
) -> PermissionListInResponse:
    offset = (page - 1) * pagesize
    permission_crud = PermissionCRUD(request.app.state.pgpool)
    permissions, count = await permission_crud.list_permissions(offset, pagesize)

    return PermissionListInResponse(data=permissions, count=count)


@router.get("/permission/{permission_id}", response_model=PermissionInResponse,)
async def get_permission(
    request: Request,
    permission_id: int = Path(..., title="The ID of the permission"),
    _=Depends(get_gettext),
) -> PermissionInResponse:
    permission_crud = PermissionCRUD(request.app.state.pgpool)
    target_permission = await permission_crud.get_permission_by_id(permission_id)
    if not target_permission:
        raise HttpNotFound(_("permission not found"))

    return target_permission


@router.delete("/permission/{permission_id}",
               response_model=PermissionInResponse,
               )
async def delete_permission(
    request: Request,
    permission_id: int = Path(..., title="The ID of the permission"),
    _=Depends(get_gettext),
) -> PermissionInResponse:
    permission_crud = PermissionCRUD(request.app.state.pgpool)
    target_permission = await permission_crud.get_permission_by_id(permission_id)
    if not target_permission:
        raise HttpNotFound(_("permission not found"))

    await permission_crud.delete_permission_by_id(permission_id)
    return target_permission


@router.post("/permission",
             status_code=HTTP_201_CREATED,
             response_model=PermissionInResponse,
             )
async def add_permission(
    request: Request,
    info: PermissionInCreate = Body(..., embed=True, alias="permission"),
    _=Depends(get_gettext),
) -> PermissionInResponse:
    if not info.name:
        raise HttpClientError(_("bad permission name"))
    if not info.uri:
        raise HttpClientError(_("bad permission uri"))

    permission_crud = PermissionCRUD(request.app.state.pgpool)
    return await permission_crud.add_permission(permission=info)


@router.put("/permission/{permission_id}", response_model=PermissionInResponse,)
async def update_permission(
    request: Request,
    permission_id: int = Path(..., title="The ID of the permission"),
    info: PermissionInUpdate = Body(..., embed=True, alias="permission"),
    _=Depends(get_gettext),
) -> PermissionInResponse:
    permission_crud = PermissionCRUD(request.app.state.pgpool)
    target_permission = await permission_crud.get_permission_by_id(permission_id)
    if not target_permission:
        raise HttpNotFound(_("permission not found"))

    target_permission.name = info.name or target_permission.name
    target_permission.uri = info.uri or target_permission.uri
    target_permission.description = info.description or target_permission.description
    target_permission.method = info.method or target_permission.method
    target_permission.status = info.status or target_permission.status

    updated = await permission_crud.update_permission_by_id(
        id=permission_id,
        permission=target_permission,
    )

    target_permission.updated = updated

    return target_permission
