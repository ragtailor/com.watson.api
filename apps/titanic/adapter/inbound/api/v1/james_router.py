from io import StringIO
import csv

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.use_cases.james_command import JamesCommand


james_router = APIRouter(prefix="/titanic/james", tags=["james"])


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


def _parse_csv_file(file: UploadFile) -> list[dict]:
    if file.content_type not in {"text/csv", "application/vnd.ms-excel", "text/plain"}:
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    text = file.file.read().decode("utf-8", errors="replace")
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    return [_normalize_titanic_row(row) for row in reader]

@james_router.get("/passengers")
async def list_passengers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """탑승자 목록을 페이지네이션으로 반환합니다."""
    repository = JamesPgRepository(db)
    use_case = JamesCommand(repository)
    return await use_case.list_paginated(page, page_size)


# /titanic/james/upload 엔드포인트에서 CSV 파일을 업로드받아 처리하는 API 라우터입니다.
@james_router.post("/upload")
async def upload_titanic_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Titanic CSV 파일을 업로드하고 NeonDB에 저장합니다."""
    records = _parse_csv_file(file)
    repository = JamesPgRepository(db)
    use_case = JamesCommand(repository)
    return await use_case.receive_uploaded_records(records)
