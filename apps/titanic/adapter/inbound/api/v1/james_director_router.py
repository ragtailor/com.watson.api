from io import StringIO
import csv

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
'''
 james_director_router.py
 전설적인 흥행작 <타이타닉>을 연출하여 
 "내가 세상의 왕이다!"를 외친 제임스 카메론 감독의 라우터
 완벽주의 성향으로 타이타닉의 모든 세트와 디테일을 
 고증한 아키텍처의 총괄 디렉터 역할 수행
'''

james_director_router = APIRouter(prefix="/james", tags=["james"])


# /titanic/james/upload 엔드포인트는 CSV 파일을 업로드 받아서, 파일을 파싱한 후, 데이터베이스에 저장하는 역할을 합니다.
@james_director_router.post("/upload")
async def upload_titanic_file(
    file: UploadFile = File(...),
):
    """타이타닉 승객 데이터 CSV 파일 업로드"""
    if file.content_type not in {"text/csv", "application/vnd.ms-excel", "text/plain"}:
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    text = file.file.read().decode("utf-8", errors="replace")
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    schema = [TitanicRecordSchema(**_normalize_titanic_row(row)).model_dump() for row in reader]

    # schema 에 상위 5줄 출력 하는 로그
    print("[제임스 라우터] 업로드된 CSV 파일에서 스키마로 옮겨진 상위 5개 레코드:")
    for record in schema[:5]:
        print(record)

    use_case = JamesDirectorUseCase()  # 의존성 주입
    use_case.receive_uploaded_records(schema)




def _normalize_titanic_row(row: dict) -> dict:
    normalized = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        lower_key = key.lower()
        if lower_key == "sex":
            normalized["gender"] = value
        elif lower_key in {
            "passenger",
            "survived",
            "pclass",
            "name",
            "age",
            "sibsp",
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


