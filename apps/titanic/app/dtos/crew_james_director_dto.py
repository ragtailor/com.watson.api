from dataclasses import dataclass

@dataclass
class JamesDirectorQuery:
    id: str
    name: str

@dataclass
class PassengerCommand:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str

@dataclass
class BookingCommand:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str

@dataclass
class JamesDirectorResponse:
    answer: str
    
