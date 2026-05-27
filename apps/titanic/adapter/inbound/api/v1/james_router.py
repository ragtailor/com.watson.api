from fastapi import APIRouter

from titanic.app.use_cases.titanic_query_impl import JamesController
from titanic.app.use_cases.caledon_validation import CaledonValidation
from titanic.adapter.inbound.schemas.titanic_request import TitanicRequest

titanic_router = APIRouter(prefix="/titanic", tags=["titanic"])


@titanic_router.post("/command")
def titanic_command(request: TitanicRequest):
    """인바운드 어댑터: CSV형 요청을 도메인 검증 모델로 변환하고 서비스에 전달합니다."""
    validation = CaledonValidation(
        Pclass=int(request.pclass),
        Sex=request.gender.lower(),
        Age=float(request.age),
        SibSp=int(request.sibsp),
        Parch=int(request.parch),
        Fare=float(request.fare),
    )

    controller = JamesController()
    return controller.predict_survival(validation)
