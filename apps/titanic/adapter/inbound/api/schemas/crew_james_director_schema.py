from typing import Optional

from pydantic import BaseModel, Field

class JamesDirectorSchema(BaseModel):
    id: int = Field(0, description="Musician ID")
    name: str = Field("제임스 카메론", description="Titanic Director")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "James Carmeron",
            }
        }
    }


class FileUploadSchema(BaseModel):
    
    passenger_id: Optional[str] = Field(None, description="승객 번호")
    survived: Optional[str] = Field(None, description="생존 여부 (0=사망, 1=생존)")
    pclass: Optional[str] = Field(None, description="티켓 등급 (1=1등석, 2=2등석, 3=3등석)")
    name: Optional[str] = Field(None, description="승객 이름")
    gender: Optional[str] = Field(None, description="성별 (male / female) — CSV의 Sex 컬럼을 정규화")
    age: Optional[str] = Field(None, description="나이")
    sib_sp: Optional[str] = Field(None, description="동승한 형제자매/배우자 수")
    parch: Optional[str] = Field(None, description="동승한 부모/자녀 수")
    ticket: Optional[str] = Field(None, description="티켓 번호")
    fare: Optional[str] = Field(None, description="탑승 요금")
    cabin: Optional[str] = Field(None, description="객실 번호")
    embarked: Optional[str] = Field(None, description="탑승 항구 (C=Cherbourg, Q=Queenstown, S=Southampton)")

    model_config = {
        "json_schema_extra" : {
            "example": {
                "passenger_id": "1",
                "survived": "0",
                "pclass": "3",
                "name": "Braund, Mr. Owen Harris",
                "gender": "male",
                "age": "22",
                "sibsp": "1",
                "parch": "0",
                "ticket": "A/5 21171",
                "fare": "7.25",
                "cabin": "",
                "embarked": "S",
            }
        }
     }


class UploadResultSchema(BaseModel):
    saved: int = Field(..., description="저장된 레코드 수")
