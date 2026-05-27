import logging
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# 위에서 정의한 SQLModel 클래스를 정의한 위치에 맞게 임포트하세요.
# 예: from secom.app.models.user_model import User
from secom.app.models.user_model import User

logger = logging.getLogger(__name__)


class JasonRepositoryImpl():

    def __init__(self, session: AsyncSession) -> None:
        """FastAPI의 디펜던시 주입(Depends) 등을 통해 비동기 세션을 받습니다."""
        self.session = session

    async def save_user(self, user: User) -> None:
        logger.info(
            "[JasonRepository] save_user 레이어 진입 — %s",
            user.model_dump(),
        )

        # 1. 동적 테이블 생성 검증 (Neon DB 최초 접속 시 테이블이 없으면 생성)
        engine = self.session.bind
        if engine is not None:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("[JasonRepository] DB 테이블 검증 및 생성 완료")

        # 2. SQLModel 객체를 세션에 추가 및 커밋 (영속화)
        # 이제 별도의 DTO/스키마 변환 과정 없이 user 객체를 그대로 사용할 수 있습니다.
        self.session.add(user)
        await self.session.commit()
        
        # 3. 데이터베이스에서 자동으로 할당된 증가 ID(id)를 파이썬 객체에 동기화
        await self.session.refresh(user)

        logger.info(
            "[JasonRepository] save_user 레이어 완료 — id=%s, userId(user_id)=%s",
            user.id,
            user.user_id,
        )