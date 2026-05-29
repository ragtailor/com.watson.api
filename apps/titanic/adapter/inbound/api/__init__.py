from fastapi import APIRouter

from titanic.adapter.inbound.api.v1.james_router import james_router
from titanic.adapter.inbound.api.v1.rose_router import titanic_router

router = APIRouter()
router.include_router(james_router)
router.include_router(titanic_router)
