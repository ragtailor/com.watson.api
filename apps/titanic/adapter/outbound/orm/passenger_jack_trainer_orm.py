
from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from tailor.core.matrix.grid_neo_theone_base import Base


class JackTrainerOrm(Base):
    # 💥 클래스명은 JackTrainer이지만, 실제 DB 테이블은 표준 명칭으로 바인딩!
    __tablename__ = "passengers" 
    
    passenger_id: Mapped[str | None] = mapped_column(String, primary_key=True,  nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(String, nullable=True)
    sib_sp: Mapped[str | None] = mapped_column(String, nullable=True)
    parch: Mapped[str | None] = mapped_column(String, nullable=True)
    survived: Mapped[str | None] = mapped_column(String, nullable=True)
   

