from pydantic import BaseModel, Field


class SamanthaRequest(BaseModel):
    """채팅 요청 본문. 사용자 메시지를 JSON으로 전달합니다."""
    message: str = Field(..., min_length=1, description="사용자 메시지")
