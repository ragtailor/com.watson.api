import pandas as pd
from typing import Any

from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository import WalterRepository

DEFAULT_COLUMNS = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Survived"]


class WalterQuery(WalterUseCase):
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository
        self.median_age: float = 30.0
        self.median_fare: float = 20.0

    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        total, items = await self._repository.list_paginated(page, page_size)
        return {"total": total, "page": page, "page_size": page_size, "items": items}

    # ML helpers — used by JackQuery (deferred)
    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

    def get_features_and_labels(self):
        df = self.get_dataframe()
        return df[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]], df["Survived"]

    def preprocess_single_passenger(self, passenger_data: dict) -> pd.DataFrame:
        df = pd.DataFrame([passenger_data])
        if isinstance(df["Sex"].iloc[0], str):
            df["Sex"] = df["Sex"].map({"male": 0, "female": 1}).fillna(0).astype(int)
        df["Age"] = df["Age"].fillna(self.median_age)
        df["Fare"] = df["Fare"].fillna(self.median_fare)
        return df[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]]
