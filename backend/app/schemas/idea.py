from pydantic import BaseModel
from typing import Optional


class IdeaBase(BaseModel):
    title: str
    description: Optional[str] = None


class IdeaCreate(IdeaBase):
    pass


class IdeaOut(IdeaBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
