from io import StringIO
import csv
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

logger = logging.getLogger(__name__)

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor

'''
 james_director_router.py
 전설적인 흥행작 <타이타닉>을 연출하여
 "내가 세상의 왕이다!"를 외친 제임스 카메론 감독의 라우터
 완벽주의 성향으로 타이타닉의 모든 세트와 디테일을
 고증한 아키텍처의 총괄 디렉터 역할 수행
'''

james_director_router = APIRouter(prefix="/james", tags=["james"])


@james_director_router.post("/upload")
async def upload_titanic_file(
    file: UploadFile = File(...),
):
    """타이타닉 승객 데이터 CSV 파일 업로드"""
    if file.content_type not in {"text/csv", "application/vnd.ms-excel", "text/plain"}:
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    raw = await file.read()
    text = raw.decode("utf-8", errors="replace")
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    schema = [TitanicRecordSchema(**_normalize_titanic_row(row)) for row in reader]

    # schema 에 상위 5줄 출력 하는 로그
    logger.info("[제임스 라우터] 업로드된 CSV 파일에서 스키마로 옮겨진 상위 5개 레코드:")
    for record in schema[:5]:
        logger.info(record)

    use_case : JamesDirectorUseCase = JamesDirectorInteractor()

    await use_case.receive_uploaded_records(schema)


def _normalize_titanic_row(row: dict) -> dict:
    normalized = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        lower_key = key.lower()
        if lower_key == "sex":
            normalized["gender"] = value
        elif lower_key == "passengerid":
            normalized["passenger_id"] = value
        elif lower_key == "sibsp":
            normalized["sib_sp"] = value
        elif lower_key in {
            "survived",
            "pclass",
            "name",
            "age",
            "parch",
            "ticket",
            "fare",
            "cabin",
            "embarked",
            "gender",
        }:
            normalized[lower_key] = value
        else:
            normalized[key] = value
    return normalized
