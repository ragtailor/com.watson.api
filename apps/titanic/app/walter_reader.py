from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent
_CSV_PATH = _DATA_DIR / "Titanic-Dataset.csv"


class WalterReader:
    def __init__(self):
        pass

    def get_data(self):
        df = pd.read_csv(_CSV_PATH)
        # 인덱스 1번 행만 반환 (DataFrame 형태 유지)
        return df.iloc[[0]].astype(object).where(df.iloc[[0]].notna(), None)

    def get_count(self):
        df = pd.read_csv(_CSV_PATH)
        # 전체 승객 수(행 개수) 반환
        return int(df.shape[0])

    def get_dataframe(self) -> pd.DataFrame:
        """학습·검증용 전체 Titanic 데이터프레임."""
        return pd.read_csv(_CSV_PATH)
