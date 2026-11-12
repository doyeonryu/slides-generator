# /plan-slides — 덱 전체 계획 → content/deck.md + content/pages/<id>.md

발표 정보: $ARGUMENTS  (예: `/plan-slides LLM 자동화 재현 가능성, 연구실 세미나, 20분`)

## 한눈에
| | |
|---|---|
| **목표** | 발표 전체의 순서와 페이지별 내용을 **페이지 파일 단위**로 확정한다 |
| **읽는 것** | `materials/_digest.md` 만 (원본 재읽기 없음) · 기존 `content/deck.md` 가 있으면 그것 |
| **만드는 것** | `content/deck.md` (메타·챕터·순서·발표 시간) · `content/pages/<id>.md` (페이지마다 하나) |
| **보고 대상** | 사용자 — 쓰기 전 Q&A 로 우선순위 확정, 쓴 뒤 목차 표(id ↔ 쪽수 ↔ 제목)로 **승인**을 받는다 |
| **다음 명령** | `/check-plan` (전체) |

```
_digest.md ──/plan-slides──▶ deck.md ─┐
   + Q&A(메시지·청중·분·rank)         ├──▶ build_deck.py list ──▶ 사용자 승인 ──▶ /check-plan
                              pages/*.md ─┘
```

## 실행 절차

### 1. 전제 확인
- `materials/_digest.md` 없으면 "/read-materials 먼저" 후 종료
- `content/deck.md` 에 order 가 이미 있으면: "기존 계획이 있습니다. 전체를 다시 짤까요, `/plan-page` 로 부분 수정할까요?" — 답을 받기 전에는 쓰지 않는다
- $ARGUMENTS 파싱: 핵심 메시지 / 청중 / 시간(분)

### 2. Q&A (누락 정보만, 한 번에)
- 핵심 메시지(한 문장) · 청중 수준 · 시간(분) → 본문 쪽수 ≈ 시간 × 0.7 (1쪽 ≈ 1.5분)
- 수업명(좌상단 라벨) · 발표일 · 표지 정보표 항목: **과목 · 담당교수 · 학과 · 학번 · 이름 · 이메일** 중 사용자가 준 것은 모두 `info:` 에 넣는다 (deck.md 에 이미 있으면 다시 묻지 않음)
- emphasis rank: 어느 finding 이 rank 1(blue) ~ 4(purple)인가

### 3. deck.md 작성
```yaml
---
title: …            # 표지 제목
subtitle: …         # 표지 부제 (선택)
eyebrow: …          # 표지 상단 소제 (예: LAB MEETING / CHAPTER 30)
course: …           # 본문 페이지 좌상단 라벨
date: 2026.11.12
duration_min: 20    # /write-script 가 시간 배분에 사용
author: …
info:               # 표지 정보표 — 준 항목 전부, 이 순서로
  - 과목 | …
  - 담당교수 | …
  - 학과 | …
  - 학번 | …
  - 이름 | …
  - 이메일 | …
  - 발표일 | …
closing_title: Q & A   # 마지막 장 제목 (기본 Q & A)
chapters:
  - 01 | 방법론 구성 | Methodology    # 번호 | 제목 | 영문부제(선택)
toc: true
section_dividers: false   # base 덱은 구역 머리글 없음
closing: true
order:                    # 본문 페이지 id, 발표 순서
  - method-overview
---
```

### 4. pages/<id>.md 작성 (페이지마다)
id 는 영문 소문자-하이픈, 내용을 말해주는 이름(`step1-result`). 번호를 넣지 않는다.
```yaml
---
id: step1-result
type: text          # text | table | figure | block
chapter: 01
title: Step 1 결과   # 36pt 한 줄. 설명성 부제 금지
refs: [calib_rmse, table_step1]   # _digest.md id
script: auto        # block 이면 custom
---
## 소제목 (16pt, 왼쪽 바)
- 본문 14pt 글머리. **굵게** 가능
  - 2단계 글머리
## 표 #. 캡션은 표 위 — 소제목으로 쓰거나 표 바로 윗줄에 '표 #. …'
| 열 | 열 |
|---|---|
| 값 | 값 |
## 글 + 그림 블록 (글 640px 좌, 그림 520px 우)
- 설명 글머리
![그림 #. 캡션은 그림 아래](materials/figures/x.png)
```
**본문 규칙**
- 수치는 _digest.md value 와 정확히 일치. 근사치는 `~`. refs 에 없는 수치 금지
- **표·그림 캡션 필수.** 표는 위(`표 #.`), 그림은 아래(`그림 #.`). `#` 은 자동 번호
- 한 페이지 = 소제목 블록 2~3개, 14pt·행간 1.5 로 본문 480px(≈17줄) 이내. 넘치면 나눈다
- `type: figure` 는 asset/synthetic ref 1개 이상
- `type: block` 은 드물게(표+카드+지표). 본문엔 요약만, `script: custom`

### 5. 승인
```bash
python scripts/build_deck.py list
```
목차 표를 보여주고 "이 구성으로 진행할까요?" → 피드백 반영 → 저장.

## 완료 보고 (사용자에게)
```
deck.md: "제목" · N분 · 챕터 K개 · 본문 P쪽 (전체 P+3장)
pages/: id 목록 (쪽수 · type · 제목)
다음: /check-plan   (수치·캡션·배치 검증 → 통과해야 /generate-slides)
```

## 원칙
- _digest.md 의 id·value 만 사용
- 핵심 finding 은 적어도 한 페이지에
- 기존 pages/*.md 를 덮어쓸 때는 반드시 확인
