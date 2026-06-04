import logging

from fastapi import APIRouter
from titanic.adapter.inbound.api.schemas.walter_roaster_schema import WalterRoasterSchema
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.use_cases.walter_roaster_interactor import WalterRoasterInteractor

'''
영화 <타이타닉>에서 승객 명단을 관리하는 
일등 항해사 윌터 와일딩(Walter Nichols / 혹은 윌리엄 머독 등 영화 속 관리자 캐릭터) 
또는 승객 명단(Passenger List)을 다루는 '월터'라는 인물의 상황에 맞추어, 
직관적이면서도 센스 있는 중간 키워드를 추천해 드립니다.
'''
logger = logging.getLogger(__name__)
walter_roaster_router = APIRouter(prefix="/walter", tags=["walter"])    

@walter_roaster_router.get("/myself")
async def introduce_myself():
    schema = WalterRoasterSchema()

    logger.info("###############################################")
    logger.info("💊[월터 라우터] 월터의 자기소개글을 가져오는 API 호출")
    logger.info(f"👍🏻ID: {schema.id}")
    logger.info(f"🐥이름: {schema.name}")
    logger.info(f"🦜메모: {schema.memo}")
    logger.info("###############################################")

    walter: WalterRoasterUseCase = WalterRoasterInteractor()
    walter.introduce_myself(schema)

    return {"id": schema.id, "name": schema.name, "memo": schema.memo}
    