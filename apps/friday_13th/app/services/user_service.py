import logging

from friday_13th.app.port.output.jason_repository_port import JasonRepository
from friday_13th.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self) -> None:
        pass

    def save_user(self, user_schema: UserSchema) -> None:
        logger.info(
            "[UserService] save_user 레이어 진입 — %s",
            user_schema.model_dump(),
        )
        user_repository = JasonRepository()
        user_repository.save_user(user_schema)
        logger.info("[UserService] save_user 레이어 완료 — userId=%s", user_schema.userId)
