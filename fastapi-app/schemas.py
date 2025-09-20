from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
