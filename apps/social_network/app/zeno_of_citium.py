"""
키티온의 제논 (Zeno of Citium): 아고라에 있는 '포이킬레 스토아(채색 주랑)'에서
제자들을 가르쳤습니다.
이 건물 이름에서 그 유명한 스토아학파라는 명칭이 유래되었습니다.

---

## VOTE_RULES (`docs/아고라개발/2026-05-12_투표.md` 스프린트 최소 구현)

프롬프트의 `[가정]`·`[미정]`이 비어 있어, 아래를 **이 모듈의 확정 규칙**으로 둔다.

- **[가정] 스택:** 단일 프로세스 메모리 저장. 영속 DB·HTTP API는 이번 범위 밖.
- **[가정] 동시성:** `cast_vote` / `register_work` 경쟁 시 `threading.Lock`으로 직렬화.
- **[미정→확정] 투표:** 작품당 **유권자 1인 1표**. 표 1건은 가중치 1(점수제 아님).
- **[미정→확정] 신원:** 호출자가 넘기는 불투명 문자열 `voter_id`. (계정 시스템 연동은 범위 밖.)
- **[미정→확정] 마감:** `deadline_utc`가 있으면 그 시각 **엄선(<=)** 이후 투표 거절. `None`이면 기한 없음.

검증: `python -m agora.app.zeno_of_citium` (패키지 경로는 배치 환경에 맞게 조정) 또는 이 파일 직접 실행 시 내장 self-check.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Work:
    """평가에 필요한 최소 필드만."""

    id: str
    title: str
    description: str | None = None


class ZenoOfCitium:
    """등록 작품에 대한 1인 1표 투표와 집계."""

    def __init__(self, deadline_utc: datetime | None = None) -> None:
        self._deadline_utc = deadline_utc
        self._works: Dict[str, Work] = {}
        # (voter_id, artwork_id) -> 투표 시각(감사용). 존재 여부만으로 중복 방지.
        self._votes: Dict[Tuple[str, str], datetime] = {}
        self._lock = threading.Lock()

    def set_deadline(self, deadline_utc: datetime | None) -> None:
        """마감 시각 설정. naive datetime은 UTC로 간주한다."""
        self._deadline_utc = deadline_utc

    def register_work(
        self, work_id: str, title: str, description: str | None = None
    ) -> Work:
        if not work_id or not title:
            raise ValueError("work_id와 title은 비어 있으면 안 된다.")
        with self._lock:
            if work_id in self._works:
                raise ValueError(f"이미 등록된 작품 id: {work_id!r}")
            w = Work(id=work_id, title=title, description=description)
            self._works[work_id] = w
            return w

    def list_works(self) -> List[Work]:
        with self._lock:
            return list(self._works.values())

    def get_work(self, work_id: str) -> Work:
        with self._lock:
            try:
                return self._works[work_id]
            except KeyError as e:
                raise ValueError(f"존재하지 않는 작품: {work_id!r}") from e

    def cast_vote(
        self,
        voter_id: str,
        artwork_id: str,
        *,
        now_utc: datetime | None = None,
    ) -> None:
        if not voter_id:
            raise ValueError("voter_id는 비어 있으면 안 된다.")
        now = now_utc or datetime.now(timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        dl = self._deadline_utc
        if dl is not None:
            if dl.tzinfo is None:
                dl = dl.replace(tzinfo=timezone.utc)
            if now > dl:
                raise ValueError("마감 이후에는 투표할 수 없다.")

        key = (voter_id, artwork_id)
        with self._lock:
            if artwork_id not in self._works:
                raise ValueError(f"존재하지 않는 작품: {artwork_id!r}")
            if key in self._votes:
                raise ValueError("이미 이 작품에 투표했다.")
            self._votes[key] = now

    def tally(self) -> List[dict]:
        """작품별 득표수 내림차순. 동점이면 work id 오름차순."""
        with self._lock:
            counts: Dict[str, int] = {wid: 0 for wid in self._works}
            for _voter, aid in self._votes:
                if aid in counts:
                    counts[aid] += 1
            rows: List[dict] = []
            for wid in sorted(self._works):
                w = self._works[wid]
                rows.append(
                    {
                        "artwork_id": w.id,
                        "title": w.title,
                        "vote_count": counts.get(wid, 0),
                    }
                )
            rows.sort(key=lambda r: (-r["vote_count"], r["artwork_id"]))
            return rows


def _run_vote_self_checks() -> None:
    """규칙 위반·집계·마감 에지를 Assertion으로 검증한다."""
    z = ZenoOfCitium()
    z.register_work("a1", "작품 A", None)
    z.register_work("a2", "작품 B", "설명")
    assert len(z.list_works()) == 2
    assert z.get_work("a1").title == "작품 A"

    z.cast_vote("u1", "a1")
    z.cast_vote("u2", "a1")
    z.cast_vote("u1", "a2")
    tall = z.tally()
    assert tall[0]["vote_count"] == 2 and tall[0]["artwork_id"] == "a1"
    assert tall[1]["vote_count"] == 1

    try:
        z.cast_vote("u1", "a1")
        raise AssertionError("중복 투표가 허용되면 안 된다.")
    except ValueError:
        pass

    try:
        z.cast_vote("u3", "ghost")
        raise AssertionError("없는 작품은 거절되어야 한다.")
    except ValueError:
        pass

    t0 = datetime(2030, 1, 1, tzinfo=timezone.utc)
    z2 = ZenoOfCitium(deadline_utc=t0)
    z2.register_work("x", "마감 테스트", None)
    z2.cast_vote("v", "x", now_utc=t0)
    try:
        z2.cast_vote("v2", "x", now_utc=datetime(2030, 1, 2, tzinfo=timezone.utc))
        raise AssertionError("마감 후 투표는 거절되어야 한다.")
    except ValueError:
        pass


'''
amyshin.dev 🎵
anjgkwl.com 🚪
kimseunga.art 🫦
bestcow.cloud 🐮
iyungyeong8088.cloud 👩🏻
cloverky.cloud 🍀
codenameseol.cloud 💊
eungsang.com 🐥
foodopenlab.com🕕
jsangho.cloud💫
minahdev.cloud 🐱
paiksunggum.com 🪸
pmhllll12.cloud 🍎
proteier.cloud 🥩
redoceanmap.com ✈️ 
seongyuna.cloud 🐛
suvisdev.cloud 🤖
whoareryu.cloud 🦁
woojeongalex.cloud🐶
'''

if __name__ == "__main__":
    _run_vote_self_checks()
    print("zeno vote self-check: ok")
