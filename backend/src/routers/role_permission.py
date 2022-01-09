from fastapi import APIRouter, Depends, Path, Query, Body, Request
from starlette.status import HTTP_201_CREATED

from models.role_permission import RolePermissionInCreate, \
    RolePermissionListInResponse, \
    RolePermissionInResponse, \
    RolePermissionInUpdate
from db.crud.role_permission import RolePermission as RolePermissionCRUD
from models.errors import HttpClientError, HttpNotFound

router = APIRouter()


@router.get("/role_permissions", response_model=RolePermissionListInResponse)
async def list_role_permissions(
    request: Request,
    page: int = Query(1, ge=1, title="which page"),
    pagesize: int = Query(20, ge=1, le=100, title="Page size"),
) -> RolePermissionListInResponse:
    _ = request.state.get_gettext
    offset = (page - 1) * pagesize
    role_permission_crud = RolePermissionCRUD(request.app.state.pgpool)
    role_permissions, count = await role_permission_crud.list_role_permissions(offset, pagesize)

    return RolePermissionListInResponse(data=role_permissions, count=count)


@router.get("/role_permission/{role_permission_id}", response_model=RolePermissionInResponse,)
async def get_role_permission(
    request: Request,
    role_permission_id: int = Path(..., title="The ID of the role_permission"),
) -> RolePermissionInResponse:
    _ = request.state.get_gettext
    role_permission_crud = RolePermissionCRUD(request.app.state.pgpool)
    target_role_permission = await role_permission_crud.get_role_permission_by_id(role_permission_id)
    if not target_role_permission:
        raise HttpNotFound(_("role_permission not found"))

    return target_role_permission


@router.delete("/role_permission/{role_permission_id}",
               response_model=RolePermissionInResponse,
               )
async def delete_role_permission(
    request: Request,
    role_permission_id: int = Path(..., title="The ID of the role_permission"),
) -> RolePermissionInResponse:
    _ = request.state.get_gettext
    role_permission_crud = RolePermissionCRUD(request.app.state.pgpool)
    target_role_permission = await role_permission_crud.get_role_permission_by_id(role_permission_id)
    if not target_role_permission:
        raise HttpNotFound(_("role_permission not found"))

    await role_permission_crud.delete_role_permission_by_id(role_permission_id)
    return target_role_permission


@router.post("/role_permission",
             status_code=HTTP_201_CREATED,
             response_model=RolePermissionInResponse,
             )
async def add_role_permission(
    request: Request,
    info: RolePermissionInCreate = Body(...,
                                        embed=True, alias="role_permission"),
) -> RolePermissionInResponse:
    _ = request.state.get_gettext
    if not info.role_id:
        raise HttpClientError(_("bad role_permission role_id"))
    if not info.permission_id:
        raise HttpClientError(_("bad role_permission permission_id"))

    role_permission_crud = RolePermissionCRUD(request.app.state.pgpool)
    return await role_permission_crud.add_role_permission(role_permission=info)


@router.put("/role_permission/{role_permission_id}", response_model=RolePermissionInResponse,)
async def update_role_permission(
    request: Request,
    role_permission_id: int = Path(..., title="The ID of the role_permission"),
    info: RolePermissionInUpdate = Body(...,
                                        embed=True, alias="role_permission"),
) -> RolePermissionInResponse:
    _ = request.state.get_gettext
    role_permission_crud = RolePermissionCRUD(request.app.state.pgpool)
    target_role_permission = await role_permission_crud.get_role_permission_by_id(role_permission_id)
    if not target_role_permission:
        raise HttpNotFound(_("role_permission not found"))

    target_role_permission.role_id = info.role_id or target_role_permission.role_id
    target_role_permission.permission_id = info.permission_id or target_role_permission.permission_id

    updated = await role_permission_crud.update_role_permission_by_id(
        id=role_permission_id,
        role_permission=target_role_permission,
    )

    target_role_permission.updated = updated

    return target_role_permission
