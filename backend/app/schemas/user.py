from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    telegram_id: int | None = None


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
