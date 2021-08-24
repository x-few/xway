from fastapi import APIRouter, Depends, Path, Query, Body, Request
from starlette.status import HTTP_201_CREATED

from models.role import RoleInCreate, \
    RoleListInResponse, \
    RoleInResponse, \
    RoleInUpdate
from db.crud.role import Role as RoleCRUD
from models.errors import HttpClientError, HttpNotFound
from services.localization import get_gettext

router = APIRouter()


@router.get("/roles", response_model=RoleListInResponse)
async def list_roles(
    request: Request,
    page: int = Query(1, ge=1, title="which page"),
    pagesize: int = Query(20, ge=1, le=100, title="Page size"),
    _=Depends(get_gettext),
) -> RoleListInResponse:
    offset = (page - 1) * pagesize
    role_crud = RoleCRUD(request.app.state.pgpool)
    roles, count = await role_crud.list_roles(offset, pagesize)

    return RoleListInResponse(data=roles, count=count)


@router.get("/role/{role_id}", response_model=RoleInResponse,)
async def get_role(
    request: Request,
    role_id: int = Path(..., title="The ID of the role"),
    _=Depends(get_gettext),
) -> RoleInResponse:
    role_crud = RoleCRUD(request.app.state.pgpool)
    target_role = await role_crud.get_role_by_id(role_id)
    if not target_role:
        raise HttpNotFound(_("role not found"))

    return target_role


@router.delete("/role/{role_id}",
               response_model=RoleInResponse,
               )
async def delete_role(
    request: Request,
    role_id: int = Path(..., title="The ID of the role"),
    _=Depends(get_gettext),
) -> RoleInResponse:
    role_crud = RoleCRUD(request.app.state.pgpool)
    target_role = await role_crud.get_role_by_id(role_id)
    if not target_role:
        raise HttpNotFound(_("role not found"))

    await role_crud.delete_role_by_id(role_id)
    return target_role


@router.post("/role",
             status_code=HTTP_201_CREATED,
             response_model=RoleInResponse,
             )
async def add_role(
    request: Request,
    info: RoleInCreate = Body(..., embed=True, alias="role"),
    _=Depends(get_gettext),
) -> RoleInResponse:
    if not info.name:
        raise HttpClientError(_("bad name"))

    role_crud = RoleCRUD(request.app.state.pgpool)
    return await role_crud.add_role(role=info)


@router.put("/role/{role_id}", response_model=RoleInResponse,)
async def update_role(
    request: Request,
    role_id: int = Path(..., title="The ID of the role"),
    info: RoleInUpdate = Body(..., embed=True, alias="role"),
    _=Depends(get_gettext),
) -> RoleInResponse:
    role_crud = RoleCRUD(request.app.state.pgpool)
    target_role = await role_crud.get_role_by_id(role_id)
    if not target_role:
        raise HttpNotFound(_("role not found"))

    target_role.name = info.name or target_role.name
    target_role.description = info.description or target_role.description

    updated = await role_crud.update_role_by_id(
        id=role_id,
        role=target_role,
    )

    target_role.updated = updated

    return target_role
