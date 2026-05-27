import logging
from typing import Dict, Any

from apps.titanic.app.use_cases.rose_query import RoseModel
from titanic.app.use_cases.walter_reader import WalterReader
from titanic.app.use_cases.caledon_validation import CaledonValidation

logger = logging.getLogger(__name__)


class JackService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """싱글톤 패턴을 적용하여 단 한 번만 모델을 학습하고 메모리에 상주하도록 최적화합니다."""
        if cls._instance is None:
            cls._instance = super(JackService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        
        self.walter = WalterReader()
        self.rose = RoseModel()
        self.trained = False
        
        # 서버 구동 시 최초 1회 전체 데이터를 학습하여 캐싱
        self._train_model()
        self._initialized = True

    def _train_model(self) -> None:
        try:
            X, y = self.walter.get_features_and_labels()
            if X.empty or y.empty:
                logger.warning("[JackService] 학습 데이터를 찾을 수 없어 모델 훈련을 건너뜁니다.")
                self.accuracy = 0.0
                self.trained = False
                return

            self.rose.train(X, y)
            self.accuracy = self.rose.get_accuracy(X, y)
            self.trained = True
            logger.info(
                "[JackService] RoseModel (DecisionTreeClassifier) 학습 완료. 정확도: %.2f%%", 
                self.accuracy * 100
            )
        except Exception as e:
            logger.error("[JackService] 모델 학습 중 에러 발생: %s", str(e))
            self.accuracy = 0.0
            self.trained = False

    def get_model_name_and_accuracy(self) -> Dict[str, Any]:
        return {
            "model_name": self.rose.get_model_name(),
            "train_accuracy": f"{self.accuracy * 100:.2f}%"
        }

    def predict_survival(self, passenger: CaledonValidation) -> Dict[str, Any]:
        """승객 데이터를 받아 전처리 및 생존 여부, 확률 예측"""
        passenger_dict = passenger.model_dump()
        
        preprocessed_x = self.walter.preprocess_single_passenger(passenger_dict)

        if not self.trained:
            return {
                "survived": 0,
                "survival_probability": "0.00%",
                "death_probability": "100.00%",
                "passenger_info": passenger_dict,
                "message": "학습 데이터가 없어 예측을 제공할 수 없습니다."
            }

        prediction = self.rose.predict(preprocessed_x)[0]
        probabilities = self.rose.predict_proba(preprocessed_x)[0]
        
        survival_prob = float(probabilities[1])
        death_prob = float(probabilities[0])
        
        return {
            "survived": int(prediction),
            "survival_probability": f"{survival_prob * 100:.2f}%",
            "death_probability": f"{death_prob * 100:.2f}%",
            "passenger_info": passenger_dict
        }

    def analyze_jack_dawson(self) -> Dict[str, Any]:
        jack = CaledonValidation(
            Pclass=3,
            Sex="male",
            Age=20.0,
            SibSp=0,
            Parch=0,
            Fare=0.0
        )
        
        result = self.predict_survival(jack)
        result["analysis"] = (
            "당시 타이타닉호 탈출 시 '여성 및 아이 우선' 원칙이 엄격하게 지켜졌고, "
            "잭은 탈출 우선순위가 최하위였던 3등석 남성이었기 때문에 생존율이 극도로 낮게 나옵니다. "
            "실제 예측 결과 모델에서도 잭의 생존 가능성은 절망적이었으며, 디카프리오가 바다에 남게 된 것은 "
            "통계적으로도 피하기 어려운 비극이었음을 시사합니다."
        )
        return result

    def analyze_rose_dewitt_bukater(self) -> Dict[str, Any]:
        rose = CaledonValidation(
            Pclass=1,
            Sex="female",
            Age=17.0,
            SibSp=1,
            Parch=1,
            Fare=150.0
        )
        
        result = self.predict_survival(rose)
        result["analysis"] = (
            "로즈는 생존 우선순위가 가장 높았던 1등석 여성이었기 때문에, "
            "모델 예측 결과에서도 생존 확률이 압도적으로 높게 분석됩니다. "
            "여성 및 아이 우선 탑승 정책과 상류층(1등석)의 빠른 구조 순서 혜택을 온전히 누려 "
            "기적적으로 생존할 수 있었습니다."
        )
        return result
