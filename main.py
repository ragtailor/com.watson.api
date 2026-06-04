import asyncio
import logging
import sys
import os
from contextlib import asynccontextmanager

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "apps"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.matrix.oracle_database import dispose_engine, get_db, init_engine, create_all_tables
from titanic.adapter.inbound.api import titanic_router


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
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(titanic_router)





@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}



if __name__ == "__main__":
    import uvicorn

    # Windows: psycopg async는 SelectorEventLoop 필요 (ProactorEventLoop 미지원)
    # loop="none"으로 uvicorn이 루프를 강제하지 않게 하고, policy만 먼저 설정
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    uvicorn.run("main:app", host="127.0.0.1", port=8000, loop="none")
