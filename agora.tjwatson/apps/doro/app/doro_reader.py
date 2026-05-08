from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent
_CSV_PATH = _DATA_DIR / "한국도로공사_교통사고통계_20241231.csv"


class DoroReader:
    def __init__(self):
        pass

    def get_data(self):
        # 공공데이터 CSV는 utf-8-sig, cp949, euc-kr 중 하나인 경우가 많아서 순차 시도
        last_error = None
        for encoding in ("utf-8-sig", "cp949", "euc-kr"):
            try:
                df = pd.read_csv(_CSV_PATH, encoding=encoding)
                break
            except UnicodeDecodeError as exc:
                last_error = exc
        else:
            raise UnicodeDecodeError(
                "csv",
                b"",
                0,
                1,
                f"지원 인코딩(utf-8-sig/cp949/euc-kr)으로 파일을 읽지 못했습니다: {_CSV_PATH}",
            ) from last_error

        # 인덱스 1번 행만 반환 (DataFrame 형태 유지)
        return df.iloc[[1]].astype(object).where(df.iloc[[1]].notna(), None)
