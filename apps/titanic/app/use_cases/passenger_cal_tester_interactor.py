from pydantic import BaseModel, Field
from typing import Literal


class CaledonValidation(BaseModel):
    Pclass: int = Field(..., ge=1, le=3, description="티켓 클래스 (1 = 1등석, 2 = 2등석, 3 = 3등석)")
    Sex: Literal["male", "female"] = Field(..., description="성별 (male 또는 female)")
    Age: float = Field(..., ge=0.0, description="나이")
    SibSp: int = Field(..., ge=0, description="함께 탑승한 형제자매 / 배우자의 수")
    Parch: int = Field(..., ge=0, description="함께 탑승한 부모님 / 아이들의 수")
    Fare: float = Field(..., ge=0.0, description="탑승 요금")

    class Config:
        json_schema_extra = {
            "example": {
                "Pclass": 3,
                "Sex": "male",
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 7.25
            }
        }
