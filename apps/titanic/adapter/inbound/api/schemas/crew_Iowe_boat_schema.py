from pydantic import BaseModel, Field

class LoweBoatSchema(BaseModel):
    
    id: int = Field(0, description="Officer ID")
    name: str = Field("해롤드 로우", description="Officer's name")
    known_for: str = Field("타이타닉 5등 항해사", description="Famous work")
    memo: str = Field("구명보트(14호)를 이끌고 유일하게 지원자를 구하러 되돌아옴", description="Famous quote")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Harold Lowe",
                "known_for": "Fifth Officer",
                "memo": "The only officer to return for survivors with lifeboat No. 14"
            }
        }
    }