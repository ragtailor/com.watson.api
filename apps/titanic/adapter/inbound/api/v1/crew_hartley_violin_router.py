from fastapi import APIRouter
'''
왈리스 하틀리 (Wallace Hartley - 악단장)
배가 가라앉는 극도의 공포 속에서도 승객들을 진정시키기 위해 끝까지 찬송가 '내 주를 가까이 하게 함은(Nearer, My God, to Thee)'을 연주했던 악단장입니다. 영화에서 가장 눈물지게 만드는 명장면의 주인공입니다. 배경 작업(Background Worker)이나 알림/이벤트 스트리밍 라우터에 어울립니다.

추천 파일명: hartley_violin_router.py (Violin: 마지막까지 켜던 바이올린)
'''
hartley_violin_router = APIRouter(prefix="/titanic/hartley", tags=["hartley"])

@hartley_violin_router.get("/myself")
async def introduce_myself():
    return {"character": "Wallace Hartley", "role": "violin", "memo": "침몰하는 배에서 끝까지 연주한 악단장. 이벤트·스트리밍 담당"}

