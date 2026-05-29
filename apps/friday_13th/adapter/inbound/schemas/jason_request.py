from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    id: str = Field(..., min_length=1, description="아이디")
    password: str = Field(..., min_length=1, description="비밀번호")
    nickname: str = Field(..., min_length=1, description="닉네임")
    email: str = Field(..., min_length=1, description="이메일")
