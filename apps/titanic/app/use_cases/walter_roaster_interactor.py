from titanic.app.ports.input.walter_roaster_use_case import WaterRoasterUseCase
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery


class WalterRoasterInteractor(WaterRoasterUseCase):
    
    def __init__(self):
        pass
    
    def introduce_myself(self):
        '''월터의 자기소개 메소드'''
        query = WalterRoasterQuery()
        pass