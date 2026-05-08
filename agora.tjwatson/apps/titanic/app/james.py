from pathlib import Path

from fastapi import FastAPI

from titanic.app.walter import Walter


app = FastAPI(title="Titanic (James)")
_MODEL_PATH = Path(__file__).resolve().parent / "titanic_decision_tree.joblib"


class James:
    def __init__(self):
        pass


    def get_data(self):
        w = Walter()
        return w.get_data()

    def get_count(self):
        w = Walter()
        return w.get_count()

    def has_decision_tree_model(self):
        """저장된 결정트리 모델 파일 존재 여부 반환."""
        return _MODEL_PATH.exists() and _MODEL_PATH.is_file()







