from pydantic import BaseModel


class SignupResponse(BaseModel):
    message: str
    id: str
    nickname: str
    email: str
