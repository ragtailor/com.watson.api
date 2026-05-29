import logging

from friday13th.app.schemas.user_schema import UserSchema
from friday13th.app.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserController(object):

    def __init__(self) -> None:
        self.user_service = UserService()

    def save_user(self, user_schema: UserSchema) -> None:
        
        self.user_service.save_user(user_schema)
        logger.info("[UserController] save_user 레이어 완료 — userId=%s", user_schema.userId)


        
   