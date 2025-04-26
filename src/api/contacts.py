from typing import List

from fastapi import APIRouter, Query, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.services.contacts import ContactsService
from src.schemas.contacts import (
    ContactCreateModel,
    ContactUpdateModel,
    ResponseContactModel,
)
from src.schemas.users import User
from src.services.auth import get_current_user
from src.utils import bad_request_response_docs, not_found_response_docs

routerContacts = APIRouter(prefix="/contacts", tags=["contacts"])


@routerContacts.get("/", response_model=List[ResponseContactModel])
async def get_contacts(
    search: str | None = Query(
        default=None, description="Search by first name, last name and email"
    ),
    birthdays_within: int | None = Query(
        default=None,
        description="Search for contacts with birthdays within a specified number of days",
    ),
    offset: int | None = Query(default=None, description="Offset"),
    limit: int | None = Query(default=None, description="limit"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    contacts_service = ContactsService(db, user)
    return await contacts_service.get_all(
        search=search, birthdays_within=birthdays_within, offset=offset, limit=limit
    )


@routerContacts.get(
    "/{contact_id}",
    response_model=ResponseContactModel,
    responses={**not_found_response_docs},
)
async def get_contact_by_id(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    contacts_service = ContactsService(db, user)
    return await contacts_service.get_by_id(contact_id)


@routerContacts.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseContactModel,
    responses={**bad_request_response_docs},
)
async def create_contact(
    body: ContactCreateModel,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    contacts_service = ContactsService(db, user)
    return await contacts_service.create(body)


@routerContacts.patch(
    "/{contact_id}",
    response_model=ResponseContactModel,
    responses={
        **bad_request_response_docs,
        **not_found_response_docs,
    },
)
async def update_contact_by_id(
    body: ContactUpdateModel,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    contacts_service = ContactsService(db, user)
    return await contacts_service.update_by_id(contact_id, body)


@routerContacts.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**not_found_response_docs},
)
async def delete_contact_by_id(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    contacts_service = ContactsService(db, user)
    await contacts_service.delete_by_id(contact_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
