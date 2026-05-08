from pathlib import Path

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

_DATA_DIR = Path(__file__).resolve().parent
_CSV_PATH = _DATA_DIR / "Titanic-Dataset.csv"
_MODEL_PATH = _DATA_DIR / "titanic_decision_tree.joblib"


class Rose:
    MODEL_PATH = _MODEL_PATH

    def __init__(self):
        pass

    def train_and_save_decision_tree(
        self,
        max_depth: int = 5,
        random_state: int = 42,
        model_path: Path = _MODEL_PATH,
    ) -> str:
        """타이타닉 데이터를 학습해 결정트리 모델을 파일로 저장한다."""
        df = pd.read_csv(_CSV_PATH)

        if "Survived" not in df.columns:
            raise ValueError("학습 대상 컬럼(Survived)이 없습니다.")

        y = df["Survived"]
        x = df.drop(columns=["Survived"])

        # 간단 전처리: 수치는 중앙값, 범주는 'unknown'으로 결측치 보정 후 원-핫 인코딩
        numeric_cols = x.select_dtypes(include=["number"]).columns
        object_cols = x.select_dtypes(exclude=["number"]).columns

        x[numeric_cols] = x[numeric_cols].fillna(x[numeric_cols].median())
        x[object_cols] = x[object_cols].fillna("unknown")
        x = pd.get_dummies(x, columns=list(object_cols), drop_first=False)

        model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
        model.fit(x, y)

        payload = {
            "model": model,
            "feature_columns": list(x.columns),
        }
        joblib.dump(payload, model_path)

        return str(model_path)