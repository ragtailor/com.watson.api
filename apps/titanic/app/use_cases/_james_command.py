from typing import Dict, Any

from titanic.app.use_cases.jack_query import JackService
from titanic.app.use_cases.caledon_query import CaledonValidation


class JamesController:
    def __init__(self):
        # JackService는 싱글톤이므로 첫 인스턴스 생성 시 모델 학습이 이루어집니다.
        self.service = JackService()

    def get_data(self) -> "pandas.DataFrame":
        """기존 뼈대 API 지원: 첫 번째 승객 데이터 리턴"""
        return self.service.walter.get_data()

    def get_count(self) -> int:
        """기존 뼈대 API 지원: 전체 탑승자 수 리턴"""
        return self.service.walter.get_count()

    def has_decision_tree_model(self) -> bool:
        """의사결정 트리 모델이 준비되어 있는지 여부 리턴"""
        return self.service.rose.model is not None

    def get_model_name_and_accuracy(self) -> Dict[str, Any]:
        """기존 뼈대 API 지원: 모델명과 훈련 정확도 리턴"""
        return self.service.get_model_name_and_accuracy()

    def predict_survival(self, passenger: CaledonValidation) -> Dict[str, Any]:
        """새로 입력된 탑승자 데이터에 대해 생존 가능성을 예측하고 확률 반환"""
        return self.service.predict_survival(passenger)

    def analyze_jack(self) -> Dict[str, Any]:
        """디카프리오(잭 도슨)의 가상 탑승 데이터를 바탕으로 한 생존 분석 결과 리턴"""
        return self.service.analyze_jack_dawson()

    def analyze_rose(self) -> Dict[str, Any]:
        """로즈 드윗 부카터의 가상 탑승 데이터를 바탕으로 한 생존 분석 결과 리턴"""
        return self.service.analyze_rose_dewitt_bukater()
