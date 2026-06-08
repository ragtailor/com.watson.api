from fastapi import APIRouter
from fastapi import APIRouter, Depends

from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
'''
토마스 앤드류스 (Thomas Andrews)
타이타닉을 설계한 수석 디자이너입니다. 배의 침몰을 가장 먼저 직감하고, 마지막 순간 흡연실 시계 앞에서 죄책감에 잠겨 있던 모습이 관객들에게 깊은 여운을 남겼습니다. 시스템의 구조나 메타데이터를 다루는 역할로 좋습니다.

추천 파일명: andrews_architect_router.py (Architect: 타이타닉 설계자)
'''
andrews_architect_router = APIRouter(prefix="/titanic/andrews", tags=["andrews"])

@andrews_architect_router.get("/myself")
async def introduce_myself(
    andrew: AndrewsArchitectUseCase = Depends()
)-> Andews:
    return {"character": "Thomas Andrews", "role": "architect", "memo": "타이타닉을 설계한 수석 디자이너. 시스템 구조·메타데이터 담당"}


