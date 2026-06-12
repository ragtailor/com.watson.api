# Agora — FlutterFlow 화면 설계 명세서

> **앱명:** Agora  
> **플랫폼:** FlutterFlow (Flutter)  
> **목적:** 에이전트 과정 학생 결과물 동료 평가 (20명 투표)  
> **생성일:** 2026-05-06  
> **태그:** #agora #flutterflow #cloud-tjwatson #agent-vote

---

## 1. 앱 개요

```
CLOUD.TJWATSON
└── apps
    ├── doro
    ├── titanic
    └── agora   ← NEW
```

| 항목 | 내용 |
|------|------|
| 앱 이름 | Agora |
| 테마 | 다크 모드 (Dark) |
| 주 색상 | Primary `#4F7FFA` / Secondary `#7C5CFC` |
| 배경색 | `#0F1117` |
| Surface | `#1A1D27` |
| Card | `#22263A` |
| 텍스트 (기본) | `#F0F2FF` |
| 텍스트 (보조) | `#8B90A7` |
| 성공 색상 | `#34D399` |
| Border | `rgba(255,255,255,0.08)` |

---

## 2. 화면 구성 (Pages)

```
LoginPage
  └─(로그인 성공)─→ StudentListPage
                        └─(학생 카드 탭)─→ StudentDetailPage
                                              └─(뒤로가기)─→ StudentListPage
```

---

## 3. Page 1 — LoginPage

### 3-1. 레이아웃

```
Column (MainAxisAlignment: center, CrossAxisAlignment: center)
├── Container [로고]
│     width: 80, height: 80, borderRadius: 24
│     gradient: LinearGradient(#4F7FFA → #7C5CFC, 135deg)
│     child: Text("🏛️", fontSize: 36)
│
├── SizedBox(height: 20)
├── Text("Agora", fontSize: 28, fontWeight: bold, color: #F0F2FF)
├── SizedBox(height: 6)
├── Text("에이전트 과정 결과물\n동료 평가 플랫폼",
│         fontSize: 13, color: #8B90A7, textAlign: center)
│
├── SizedBox(height: 28)
├── Container [구분선]
│     width: 40, height: 2
│     gradient: LinearGradient(#4F7FFA → #7C5CFC)
│     borderRadius: 2
│
├── SizedBox(height: 28)
│
├── GoogleLoginButton [컴포넌트]
│     width: double.infinity
│     height: 52
│     backgroundColor: #FFFFFF
│     borderRadius: 14
│     child: Row
│       ├── GoogleLogoImage (width: 20, height: 20)
│       └── Text("Google 계정으로 로그인",
│                 fontSize: 15, fontWeight: semiBold, color: #1F1F1F)
│
├── SizedBox(height: 16)
└── Container [안내 뱃지]
      padding: 10px 16px
      backgroundColor: rgba(79,127,250,0.08)
      border: 0.5px solid rgba(79,127,250,0.2)
      borderRadius: 10
      child: Text("🔒 등록된 이메일 계정만 접근 가능합니다",
                  fontSize: 11, color: #8B90A7, textAlign: center)
```

### 3-2. 액션 설정

| 컴포넌트 | 이벤트 | 액션 |
|----------|--------|------|
| GoogleLoginButton | OnTap | **[Phase 1]** Navigate → StudentListPage (무조건 성공) |
| GoogleLoginButton | OnTap | **[Phase 2]** Google Auth → 이메일 whitelist 검증 → 성공 시 Navigate |

### 3-3. Phase 2 구현 메모 (향후)
- Firebase Authentication → Google Sign-In 활성화
- Firestore `allowed_users` 컬렉션에 허용 이메일 목록 저장
- 로그인 후 `currentUser.email` → Firestore 조회 → 미등록 시 로그아웃 + SnackBar 표시

---

## 4. Page 2 — StudentListPage

### 4-1. AppBar

```
AppBar
├── backgroundColor: #0F1117
├── elevation: 0
├── bottomBorder: 0.5px solid rgba(255,255,255,0.08)
└── Row
    ├── Text("🏛️ Agora", fontSize: 20, fontWeight: bold, color: #F0F2FF)
    └── Container [뱃지]
          padding: 3px 10px, borderRadius: 20
          backgroundColor: rgba(79,127,250,0.15)
          border: 0.5px solid rgba(79,127,250,0.3)
          child: Text("20명 투표 중", fontSize: 11, color: #7BA4FF)
```

Subtitle: `Text("학생을 선택하여 작품을 확인하세요", fontSize: 12, color: #8B90A7)`

### 4-2. 학생 그리드

```
GridView
├── crossAxisCount: 4
├── mainAxisSpacing: 10
├── crossAxisSpacing: 10
├── padding: EdgeInsets.all(16)
└── children: StudentCard × 20
```

### 4-3. StudentCard 컴포넌트

```
GestureDetector (OnTap → StudentDetailPage, data: student)
└── Container
      backgroundColor: #22263A
      borderRadius: 16
      border: 0.5px solid rgba(255,255,255,0.08)
      padding: 12px 6px 10px
      └── Column (center)
          ├── Text(emoji, fontSize: 28)
          ├── SizedBox(height: 4)
          ├── Text(studentNumber, fontSize: 9, color: #7BA4FF, fontWeight: semiBold)
          └── Text(name, fontSize: 10, color: #8B90A7,
                    overflow: ellipsis, textAlign: center)
```

### 4-4. 학생 데이터 목록 (20명)

| # | 이모지 | 이름 | 조 | 프로젝트 | 기술스택 |
|---|--------|------|-----|----------|----------|
| 01 | 🦁 | 김민준 | 1조 | 멀티에이전트 뉴스 요약기 | LangGraph · OpenAI · FastAPI |
| 02 | 🐯 | 이서연 | 2조 | RAG 기반 법률 Q&A 챗봇 | LlamaIndex · pgvector · Streamlit |
| 03 | 🐻 | 박지호 | 1조 | 코드 리뷰 자동화 에이전트 | GitHub Actions · GPT-4o · Python |
| 04 | 🦊 | 최수아 | 3조 | 감정 분석 고객 응대 봇 | HuggingFace · FastAPI · Redis |
| 05 | 🐺 | 정도현 | 2조 | 재무 리포트 생성 에이전트 | Pandas · LangChain · GPT-4o |
| 06 | 🦋 | 한유진 | 4조 | 강의 자동 요약 & 퀴즈 생성 | Whisper · GPT-4 · Next.js |
| 07 | 🐸 | 윤재원 | 3조 | SNS 컨텐츠 스케줄러 | LangChain · Selenium · Flask |
| 08 | 🦅 | 임나연 | 4조 | 의료 증상 1차 분류 에이전트 | Fine-tuned LLM · FastAPI · PostgreSQL |
| 09 | 🐬 | 강현서 | 1조 | 스마트 이메일 초안 생성기 | Gmail API · GPT-4o · React |
| 10 | 🦜 | 조예린 | 2조 | 특허 유사도 검색 에이전트 | SentenceTransformers · Qdrant · FastAPI |
| 11 | 🐙 | 신태양 | 3조 | 여행 일정 자동 플래너 | LangGraph · Google Maps API · Streamlit |
| 12 | 🦚 | 오하은 | 4조 | GitHub Issue 자동 분류기 | GitHub API · Classification LLM · Python |
| 13 | 🦩 | 문성민 | 1조 | 개인화 뉴스레터 에이전트 | RSS · LangChain · SendGrid |
| 14 | 🐧 | 배수빈 | 2조 | 데이터 정제 자동화 에이전트 | Pandas · LLM · Airflow |
| 15 | 🦄 | 서준혁 | 3조 | HR 채용 서류 1차 스크리닝 | LlamaIndex · GPT-4 · FastAPI |
| 16 | 🐲 | 홍다은 | 4조 | 실시간 번역 에이전트 API | DeepL API · LangChain · Docker |
| 17 | 🦝 | 권민혁 | 1조 | 재고 예측 에이전트 | Time-series LLM · PostgreSQL · Grafana |
| 18 | 🦦 | 엄지아 | 2조 | 소셜 댓글 모니터링 에이전트 | Twitter API · Sentiment LLM · Slack Bot |
| 19 | 🐝 | 남건우 | 3조 | 회의록 자동 작성 에이전트 | Whisper · GPT-4o · Notion API |
| 20 | 🦋 | 류소희 | 4조 | 커리큘럼 맞춤 학습 에이전트 | RAG · LangGraph · Next.js |

---

## 5. Page 3 — StudentDetailPage

### 5-1. AppBar

```
AppBar
├── backgroundColor: #0F1117
├── leading: IconButton(icon: Icons.arrow_back, onTap: Navigator.pop)
└── title: Text("{studentName}의 작품", fontSize: 16, fontWeight: semiBold)
```

### 5-2. 바디 레이아웃

```
SingleChildScrollView
└── Column
    ├── [히어로 카드]
    │   Container
    │   backgroundColor: #22263A, borderRadius: 20, padding: 28px 20px
    │   textAlign: center
    │   ├── Text(emoji, fontSize: 56)
    │   ├── SizedBox(height: 12)
    │   ├── Text(name, fontSize: 18, fontWeight: bold, color: #F0F2FF)
    │   └── Container [태그 뱃지]
    │         margin-top: 6, padding: 4px 12px, borderRadius: 20
    │         backgroundColor: rgba(124,92,252,0.15)
    │         border: 0.5px solid rgba(124,92,252,0.3)
    │         child: Text(tag, fontSize: 11, color: #A88DFF)
    │
    ├── SizedBox(height: 14)
    │
    ├── [투표 바]
    │   Container
    │   backgroundColor: #22263A, borderRadius: 14, padding: 14px 16px
    │   border: 0.5px solid rgba(255,255,255,0.08)
    │   └── Row (SpaceBetween)
    │       ├── Column
    │       │   ├── Text(voteCount, fontSize: 24, fontWeight: bold, color: #4F7FFA)
    │       │   └── Text("현재 투표 수", fontSize: 11, color: #8B90A7)
    │       └── VoteButton [컴포넌트]
    │
    ├── SizedBox(height: 14)
    │
    ├── [섹션 라벨] Text("프로젝트", fontSize: 11, color: #8B90A7,
    │                    fontWeight: semiBold, letterSpacing: 0.5)
    ├── WorkCard(title: projectName, desc: projectDesc)
    │
    ├── SizedBox(height: 14)
    │
    ├── [섹션 라벨] Text("사용 기술", ...)
    └── WorkCard(desc: techStack)
```

### 5-3. VoteButton 상태

| 상태 | 텍스트 | 배경 | 텍스트색 |
|------|--------|------|----------|
| 미투표 | 👍 투표하기 | Gradient (#4F7FFA → #7C5CFC) | #FFFFFF |
| 투표 완료 | ✅ 투표 완료 | #1A1D27 | #34D399 |

### 5-4. 투표 액션

```
OnTap(VoteButton)
  IF voted == false
    → Firestore: votes/{studentId} 카운트 +1
    → AppState: voted[studentId] = true
    → UI: 버튼 상태 → '투표 완료'로 전환
    → voteCount + 1 (로컬 업데이트)
  ELSE
    → 무반응 (또는 "이미 투표하셨습니다" SnackBar)
```

---

## 6. Firestore 데이터 구조 (Phase 2)

```
firestore/
├── allowed_users/          # 허용 이메일 whitelist
│   └── {docId}
│       └── email: "user@example.com"
│
├── students/               # 학생 정보
│   └── {studentId}
│       ├── id: 1
│       ├── emoji: "🦁"
│       ├── name: "김민준"
│       ├── tag: "에이전트 1조"
│       ├── project: "멀티에이전트 뉴스 요약기"
│       ├── description: "..."
│       ├── techStack: "LangGraph · OpenAI · FastAPI"
│       └── voteCount: 0
│
└── votes/                  # 투표 기록 (중복 방지)
    └── {userId}_{studentId}
        ├── userId: "abc123"
        ├── studentId: 1
        └── createdAt: Timestamp
```

---

## 7. FlutterFlow 작업 체크리스트

### Phase 1 (현재 — 화면만)
- [ ] Design System → Colors 세팅 (Primary, Secondary, Background 등)
- [ ] LoginPage 생성 및 구글 버튼 OnTap → Navigate 연결
- [ ] StudentListPage 생성 → GridView 4열 구성
- [ ] StudentCard 컴포넌트 생성 (파라미터: emoji, name, number)
- [ ] StudentDetailPage 생성 → 히어로 카드 + 투표 바 + 정보 카드
- [ ] VoteButton 컴포넌트 생성 (상태: voted / unvoted)
- [ ] 페이지 간 네비게이션 연결

### Phase 2 (에이전트 진화 준비)
- [ ] Firebase 프로젝트 연결
- [ ] Google Sign-In 활성화
- [ ] Firestore `allowed_users` 이메일 whitelist 검증 로직
- [ ] Firestore `students` 컬렉션 연동
- [ ] 투표 중복 방지 로직 (`votes/{userId}_{studentId}`)
- [ ] 실시간 voteCount 반영 (StreamBuilder)

### Phase 3 (에이전트 심의)
- [ ] 투표 마감 후 결과 집계 에이전트 연동
- [ ] 멀티에이전트 평가 코멘트 자동 생성
- [ ] Agora 본래 의미 실현: 에이전트들의 광장

---

## 8. 컴포넌트 재사용 구조

```
components/
├── StudentCard       (emoji, name, studentNumber, onTap)
├── VoteButton        (isVoted, onVote)
├── WorkCard          (title?, description)
├── SectionLabel      (text)
└── TagBadge          (text, color)
```

---

*generated by Claude Sonnet 4.6 | ragwatson agent data | cloud.tjwatson > apps > agora*
