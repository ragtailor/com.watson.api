
from abc import ABC, abstractmethod

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema


class WalterRoasterUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: WalterRoasterSchema):
        '''월터의 자기소개 메소드'''
        pass