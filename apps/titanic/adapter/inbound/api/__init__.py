from fastapi import APIRouter

from titanic.adapter.inbound.api.v1.james_router import james_router
from titanic.adapter.inbound.api.v1.rose_router import rose_router
from titanic.adapter.inbound.api.v1.walter_router import walter_router

titanic_router = APIRouter()
titanic_router.include_router(james_router)
titanic_router.include_router(rose_router)
titanic_router.include_router(walter_router)
