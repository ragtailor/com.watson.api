import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier


class RoseModel:
    def __init__(self) -> None:
        # 학습의 일관성을 위해 random_state를 지정합니다.
        self.model = DecisionTreeClassifier(random_state=42, max_depth=5)

    def get_model_name(self) -> str:
        return type(self.model).__name__

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """독립변수 X와 종속변수 y 데이터를 받아 의사결정 나무 모델 학습"""
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """주어진 입력 데이터 X에 대해 생존 여부(0 또는 1) 예측"""
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """생존 및 사망에 대한 각각의 확률 반환"""
        return self.model.predict_proba(X)

    def get_accuracy(self, X: pd.DataFrame, y: pd.Series) -> float:
        """학습된 모델의 정확도 반환"""
        return float(self.model.score(X, y))
