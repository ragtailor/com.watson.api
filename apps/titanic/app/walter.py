import json
from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent
_CSV_PATH = _DATA_DIR / "Titanic-Dataset.csv"


class Walter:
    def __init__(self):
        pass

    def get_data(self):
        df = pd.read_csv(_CSV_PATH)
        print(df.head(1))

    def head_records(self, n: int = 1) -> list[dict]:
        df = pd.read_csv(_CSV_PATH)
        return json.loads(df.head(n).to_json(orient="records"))
