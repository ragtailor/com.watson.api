import pytest
import ollama
from kiwipiepy import Kiwi

kiwi = Kiwi()


def run_korean_ai(user_text: str) -> str:
    print("\n--- [1단계] 입력 문장 전처리 중... ---")

    tokens = kiwi.tokenize(user_text)
    cleaned_text = user_text
    print(f"원본 문장: {user_text}")

    nouns = [t.form for t in tokens if t.tag.startswith("NN")]
    print(f"추출된 핵심 명사: {nouns}")

    print("\n--- [2단계] qwen2.5:3b 모델 추론 중... ---")

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[{"role": "user", "content": cleaned_text}],
        options={"num_gpu": 0},
    )

    return response["message"]["content"]


@pytest.mark.ollama
def test_korean_ai():
    """Ollama 서버가 실행 중일 때만 동작하는 통합 테스트."""
    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."
    answer = run_korean_ai(question)

    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)

    assert isinstance(answer, str) and answer, "모델 응답이 비어있습니다."


if __name__ == "__main__":
    question = "타이타닉에서 생존자는 총 몇 명이야 ?"
    answer = run_korean_ai(question)
    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)
