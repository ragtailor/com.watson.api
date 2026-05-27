import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.db_health_adapter import DbHealthAdapter
from database import dispose_engine, get_db
from doro.app.doro_director import DoroDirector
from matrix.app.keymaker import get_keymaker

from secom.app.models import user_model as _secom_user_model  # noqa: F401 — ORM 메타데이터 등록
from titanic.app.use_cases.titanic_query_impl import JamesController
from titanic.app.use_cases.caledon_validation import CaledonValidation
from titanic.adapter.inbound.api.v1.titanic_query_router import router as titanic_query_router
from secom.app.schemas.user_schema import UserSchema
from secom.app.controllers.user_controller import UserController

keymaker = get_keymaker()


def _configure_logging() -> None:
    """uvicorn 콘솔에 앱 logger.info가 보이도록 기본 핸들러를 설정합니다."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:\t%(message)s",
        force=True,
    )


_configure_logging()
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """채팅 요청 본문. 사용자 메시지를 JSON으로 전달합니다."""

    message: str = Field(..., min_length=1, description="사용자 메시지")


class ChatResponse(BaseModel):
    reply: str


class SignupRequest(BaseModel):
    id: str = Field(..., min_length=1, description="아이디")
    password: str = Field(..., min_length=1, description="비밀번호")
    nickname: str = Field(..., min_length=1, description="닉네임")
    email: str = Field(..., min_length=1, description="이메일")


class SignupResponse(BaseModel):
    message: str
    id: str
    nickname: str
    email: str


@asynccontextmanager
async def lifespan(app: FastAPI):
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

app.include_router(titanic_query_router)




@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    JSON 본문 `{"message": "..."}` 를 받아 Gemini 답변 문자열을 반환합니다.
    """
    if not keymaker.is_gemini_ready():
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
        )

    model = keymaker.get_gemini_model()
    try:
        response = model.generate_content(req.message)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini 호출 실패: {e!s}",
        ) from e

    try:
        text = (response.text or "").strip()
    except ValueError as e:
        feedback = getattr(response, "prompt_feedback", None)
        raise HTTPException(
            status_code=400,
            detail=f"응답 텍스트를 읽을 수 없습니다: {e!s}. prompt_feedback={feedback}",
        ) from e

    if not text:
        reason = None
        if getattr(response, "candidates", None):
            c0 = response.candidates[0]
            reason = getattr(c0, "finish_reason", None)
        raise HTTPException(
            status_code=502,
            detail=(
                "모델이 비어 있는 응답을 반환했습니다."
                + (f" (finish_reason={reason})" if reason else "")
            ),
        )

    return ChatResponse(reply=text)


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DbHealthAdapter.neon_time_check(db)









@app.post("/titanic/predict")
def predict_titanic_survival(req: CaledonValidation):
    controller = JamesController()
    result = controller.predict_survival(req)
    return JSONResponse(content=jsonable_encoder(result))

@app.get("/doro/data")
def read_doro_data():
    doro_director = DoroDirector()
    df = doro_director.get_data()

    return df.to_dict(orient="records")

@app.post("/signup", response_model=SignupResponse)
def signup(req: SignupRequest) -> SignupResponse:
    logger.info(
        "회원가입 요청 수신 — userId=%s, password=%s, nickname=%s, email=%s",
        req.userId,
        req.password,
        req.nickname,
        req.email,
    )
    #  프론트엔드에서 가져온 데이터를 스키마에 담아서 DB 로 보내는 코드 
    user_schema = UserSchema(
        userId=req.userId,
        password=req.password,
        nickname=req.nickname,
        email=req.email,
        role="user",
    )

    user_controller = UserController()
    user_controller.save_user(user_schema)



    return SignupResponse(
        message="회원가입 요청이 접수되었습니다.",
        id=req.id,
        nickname=req.nickname,
        email=req.email,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
