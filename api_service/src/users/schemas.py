from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserAuth(UserBase):
    password: str


class UserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
