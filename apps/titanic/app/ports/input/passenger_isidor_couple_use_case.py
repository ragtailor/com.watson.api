from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IsidorCoupleUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        '''이시도어 커플의 자기소개 메소드'''
        pass
