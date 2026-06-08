from pydantic import BaseModel


class SamanthaResponse(BaseModel):
    reply: str
