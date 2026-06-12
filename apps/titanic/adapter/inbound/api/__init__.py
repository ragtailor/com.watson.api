from __future__ import annotations

# titanic_router는 main.py에서 처음 접근할 때 지연 생성됩니다.
# 이 패키지의 schemas/* 서브모듈을 임포트할 때 라우터 체인이 즉시 로드되지 않도록
# PEP 562 (module __getattr__) 패턴을 사용합니다.

_titanic_router = None


def __getattr__(name: str):
    global _titanic_router

    if name == "titanic_router":
        if _titanic_router is None:
            _titanic_router = _build_titanic_router()
        return _titanic_router

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _build_titanic_router():
    from fastapi import APIRouter

    from titanic.adapter.inbound.api.v1.crew_andrews_architect_router import andrews_architect_router
    from titanic.adapter.inbound.api.v1.passenger_cal_tester_router import cal_tester_router
    from titanic.adapter.inbound.api.v1.crew_hartley_violin_router import hartley_violin_router
    from titanic.adapter.inbound.api.v1.passenger_isidor_couple_router import isidor_couple_router
    from titanic.adapter.inbound.api.v1.passenger_jack_trainer_router import jack_trainer_router
    from titanic.adapter.inbound.api.v1.crew_james_director_router import james_director_router
    from titanic.adapter.inbound.api.v1.passenger_rose_model_router import rose_model_router
    from tailor.apps.titanic.adapter.inbound.api.v1.passenger_ruth_validation_router import ruth_validation_router
    from titanic.adapter.inbound.api.v1.crew_smith_captain_router import smith_captain_router
    from titanic.adapter.inbound.api.v1.crew_walter_roaster_router import walter_roaster_router

    router = APIRouter(prefix="/titanic", tags=["titanic"])
    router.include_router(james_director_router)
    router.include_router(walter_roaster_router)
    router.include_router(rose_model_router)
    router.include_router(ruth_validation_router)
    router.include_router(smith_captain_router)
    router.include_router(jack_trainer_router)
    router.include_router(cal_tester_router)
    router.include_router(andrews_architect_router)
    router.include_router(hartley_violin_router)
    router.include_router(isidor_couple_router)
    return router
