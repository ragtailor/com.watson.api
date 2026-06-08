from fastapi import APIRouter

'''
이시도르 & 이다 스트라우스 부부 (Isidor & Ida Straus)
구명보트 탑승을 거부하고 "우리는 평생을 함께했으니 함께 갈 것입니다"라며 침대 위에서 서로를 꼭 껴안고 물이 차오르는 것을 맞이한 노부부입니다. 짧은 단역이었지만 엄청난 충격을 준 인물들입니다. (이름은 남편인 isidor로 대표)

추천 파일명: isidor_couple_router.py (Couple: 마지막을 함께한 부부)
'''
isidor_couple_router = APIRouter(prefix="/titanic/isidor", tags=["isidor"])

@isidor_couple_router.get("/myself")
async def introduce_myself():
    return {"character": "Isidor & Ida Straus", "role": "couple", "memo": "함께 운명을 맞이한 노부부. 커플 생존 데이터 담당"}

