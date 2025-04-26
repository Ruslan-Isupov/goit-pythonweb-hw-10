from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
