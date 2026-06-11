from fastapi import APIRouter, Depends, Query

from tailor.apps.titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from tailor.apps.titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from tailor.apps.titanic.dependencies.passenger_ruth_validation_provider import get_ruth_validation_use_case

'''
루스 드윗 부카터 (Ruth DeWitt Bukater)
딸 로즈의 코르셋 끈을 강하게 조이며 상류층의 체면을 강요하던
통제욕의 상징. 1등석 승객(상류층) 조회를 담당한다.

추천 파일명: ruth_validation_router.py
'''

ruth_validation_router = APIRouter(prefix="/ruth", tags=["ruth"])


@ruth_validation_router.get("/myself")
async def introduce_myself(
    ruth: RuthValidationUseCase = Depends(get_ruth_validation_use_case)
):
    return await ruth.introduce_myself(
        RuthValidationSchema(
            id=14,
            name="로즈 드윗 부카터 (Rose DeWitt Bukater)"
        )
    )

