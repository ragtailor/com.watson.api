from pydantic import BaseModel, Field


class TitanicRequest(BaseModel):
    passenger: str = Field(..., description="Passenger identifier")
    survived: str = Field(..., description="Survival label")
    pclass: str = Field(..., description="Ticket class")
    name: str = Field(..., description="Passenger name")
    gender: str = Field(..., description="성별 (sex 대신 gender)")
    age: str = Field(..., description="Age")
    sibsp: str = Field(..., description="Number of siblings/spouses aboard")
    parch: str = Field(..., description="Number of parents/children aboard")
    ticket: str = Field(..., description="Ticket number")
    fare: str = Field(..., description="Ticket fare")
    cabin: str = Field(..., description="Cabin identifier")
    embarked: str = Field(..., description="Port of embarkation")

    class Config:
        schema_extra = {
            "example": {
                "passenger": "1",
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
