from fastapi import FastAPI

from titanic.app.jack_service import JackService
app = FastAPI(title="Titanic (James)")


class JamesController:
    def __init__(self):
        self.service = JackService()

    def get_model_name_and_accuracy(self):
        return self.service.get_model_name_and_accuracy()
      


   






