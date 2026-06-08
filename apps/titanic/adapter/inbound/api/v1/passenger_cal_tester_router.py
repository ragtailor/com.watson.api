from fastapi import APIRouter
from titanic.app.use_cases.passenger_cal_tester_interactor import CaledonValidation

'''
칼 캘던 하클리 (Caledon Hockley)
오만하고 부유한 자산가이자, 소유욕이 강하고 빌런으로서의
면모를 드러내는 키워드입니다.
승객 입력값 유효성 검사를 담당합니다.
'''

cal_test_router = APIRouter(prefix="/titanic/cal", tags=["cal"])


@cal_test_router.get("/myself")
async def introduce_myself():
    return {"character": "Caledon Hockley", "role": "validation", "memo": "오만한 자산가. 승객 입력값 유효성 검사 담당"}


