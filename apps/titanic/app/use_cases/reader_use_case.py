import pandas as pd

DEFAULT_COLUMNS = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Survived"]


class WalterReader:
    def __init__(self):
        self.median_age = None
        self.median_fare = None

    def get_data(self) -> pd.DataFrame:
        """CSV 파일이 제거되어 빈 DataFrame을 반환합니다."""
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

    def get_count(self) -> int:
        """CSV 파일이 제거되어 데이터 수 0을 반환합니다."""
        return 0

    def get_dataframe(self) -> pd.DataFrame:
        """CSV 파일이 제거되어 빈 DataFrame을 반환합니다."""
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

    def get_features_and_labels(self):
        """학습 데이터가 없으면 빈 피처/라벨을 반환합니다."""
        df = self.get_dataframe()
        return df[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]], df["Survived"]

    def preprocess_single_passenger(self, passenger_data: dict) -> pd.DataFrame:
        """단일 예측 요청 데이터를 모델 형식에 맞게 전처리"""
        df = pd.DataFrame([passenger_data])

        if isinstance(df["Sex"].iloc[0], str):
            df["Sex"] = df["Sex"].map({"male": 0, "female": 1}).fillna(0).astype(int)

        if self.median_age is None or pd.isna(self.median_age):
            self.median_age = 30.0
            self.median_fare = 20.0

        df["Age"] = df["Age"].fillna(self.median_age)
        df["Fare"] = df["Fare"].fillna(self.median_fare)

        features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]
        return df[features]
