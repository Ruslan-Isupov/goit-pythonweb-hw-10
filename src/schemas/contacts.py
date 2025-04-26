from datetime import date
from typing import Any, Optional
from pydantic import BaseModel, Field, EmailStr, model_validator

from src.utils import HTTPBadRequestException


def validate_birthday(birthday: Any):
    try:
        date.fromisoformat(birthday)
    except ValueError:
        raise HTTPBadRequestException("Invalid date format. Should be YYYY-MM-DD.")


class ContactCreateModel(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=180)
    phone: str = Field(min_length=3, max_length=80)
    birthday: date

    @model_validator(mode="before")
    @classmethod
    def validator_before_create(cls, values):
        birthday = values.get("birthday")
        validate_birthday(birthday)
        return values


class ContactUpdateModel(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=180)
    phone: str | None = Field(default=None, min_length=3, max_length=80)
    birthday: date | None = None

    @model_validator(mode="before")
    @classmethod
    def validator_before_update(cls, values):
        if "birthday" in values:
            birthday = values.get("birthday")
            validate_birthday(birthday)
        return values


class ResponseContactModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
