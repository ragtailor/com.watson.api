from typing import Any

from titanic.app.rose_model import RoseModel
from titanic.app.walter_reader import WalterReader


class JackService:

    def __init__(self) -> None:
        self.walter = WalterReader()
        self.rose = RoseModel()

    def get_model_name_and_accuracy(self):
        return self.rose.get_model_name()
       
    
