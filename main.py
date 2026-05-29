import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import dispose_engine, get_db, init_engine, create_all_tables
from titanic.adapter.inbound.api.v1.rose_router import titanic_router
from titanic.adapter.inbound.api.v1.james_router import james_router


def _configure_logging() -> None:
    """uvicorn 콘솔에 앱 logger.info가 보이도록 기본 핸들러를 설정합니다."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:\t%(message)s",
        force=True,
    )


_configure_logging()
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_engine()
    await create_all_tables()
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="TJ Watson Main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(titanic_router)
app.include_router(james_router)





@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
