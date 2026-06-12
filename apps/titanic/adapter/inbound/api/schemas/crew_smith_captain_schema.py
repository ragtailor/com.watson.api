from pydantic import BaseModel, Field
from typing import Literal


class MessageItem(BaseModel):
    role: Literal["user", "assistant"]
    text: str


class ChatSchema(BaseModel):
    messages: list[MessageItem] = Field(..., description="채팅 메시지 히스토리")
    systemInstruction: str | None = Field(None, description="시스템 프롬프트")

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [{"role": "user", "text": "타이타닉 생존율을 분석해줘"}],
            }
        }
    }


class SmithCaptainChatSchema(BaseModel):
    messages: list[MessageItem] = Field(..., description="채팅 메시지 히스토리")


class SmithCaptainSchema(BaseModel):

    id: int = Field(0, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")
    # 타이타닉 선장. 백만장자들의 선장이라 불렸으며 고조되는 위기 속에 배와 운명을 함께함

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Edward Smith",
            }
        }
    }


