from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery


class AndrewsArchitectRepository(ABC):
    
    @abstractmethod
    def introduce_myself(self, query: AndrewsArchitectQuery):
        '''월터의 자기 소개 레포지토리 추상 메소드'''
        pass
    