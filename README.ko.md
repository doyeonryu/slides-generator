# slides-generator

[English](README.md) · **한국어**

Claude Code 슬래시 커맨드로 발표 덱을 만드는 **페이지 단위** 워크플로우.
`materials/*.md` → 페이지별 계획(`content/pages/<id>.md`) → 검증 → 결정적 렌더 → 덱 조립 → 대본.

페이지가 작업 단위다. 한 장을 추가하거나 고쳐도 다른 페이지는 건드리지 않는다.

---

## 빠른 시작

### 1. 설치

```bash
git clone <this-repo>
cd slides-generator
bash install.sh
```

슬래시 커맨드 9개, 공유 스크립트 5개, `templates/template.pptx`, `ppt_design.md` 가 `~/.claude/` 에 등록된다.

요구사항: Python 3.9+ · `pip install -r requirements.txt` (python-pptx, lxml, Pillow) · Claude Code CLI · PNG 미리보기는 Windows + PowerPoint (선택)

### 2. 발표 폴더 만들기

```bash
mkdir my-talk && cd my-talk
claude
```
```
/slides-generator 내 발표 제목
```
`materials/` `content/pages/` `content/notes/` `output/pages/` `scripts/` `templates/` 와 `deck.md` 골격, `CLAUDE.md` 가 생성된다.

### 3. 자료 넣기

`materials/` 에 `.md` 파일을 넣는다. 논문 초안, 연구 노트, 실험 결과 등 형식 무관.

명령 없이 렌더러만 먼저 보려면 레포 루트에서 최소 예제를 돌린다:
```bash
pip install -r requirements.txt
cp -r examples/minimal/* .
python scripts/build_deck.py pages --all --png     # output/pages/<id>.pptx (+ .png, Windows + PowerPoint)
python scripts/build_deck.py deck --png            # output/deck.pptx
```

### 4. 생성

```
/read-materials                                   → materials/_digest.md (수치·표·그림 ledger)
/plan-slides 핵심 메시지, 청중, 20분               → content/deck.md + content/pages/*.md
/check-plan                                       → content/plan_check.md (FAIL 0 이어야 진행)
/generate-slides all                              → output/pages/<id>.pptx + .png
/build-deck                                       → output/deck.pptx (표지·목차·본문·마무리 + 쪽번호)
/write-script all                                 → content/notes/<id>.md → 발표자 노트 + content/script.md
```

### 5. 부분 수정

| 하고 싶은 것 | 명령 |
|---|---|
| 5쪽 뒤에 한 장 추가 | `/plan-page add after:5 "민감도 분석"` → `/check-plan <id>` → `/generate-slides <id>` → `/build-deck` |
| 7쪽 내용 수정 | `/plan-page modify 7 "표 대신 글머리로"` (또는 `pages/<id>.md` 직접 편집) → `/generate-slides 7` → `/build-deck` |
| 스타일 규칙 수정 | `ppt_design.md` / `scripts/lib.py` 수정 → `/generate-slides all` → `/build-deck` |
| 자료 추가 | `materials/` 에 파일 추가 → `/read-materials` (새 파일만 처리) → 필요한 페이지만 `/plan-page` |
| PowerPoint 에서 직접 고침 | `output/pages/<id>.edited.pptx` 로 저장 → `/review-edit <id>` → 제안된 규칙 승인 |

쪽수 인자는 본문 기준(표지·목차 제외). `/plan-page list` 가 최종 쪽수도 함께 보여준다.

---

## 작동 방식

```
/slides-generator → /read-materials → /plan-slides ─┬→ /check-plan → /generate-slides → /build-deck → /write-script
                                        /plan-page ─┘        ↑                                  │
                                                             └──────── /review-edit ←───────────┘
```

| 명령 | 읽는 것 | 만드는 것 | 누가 |
|---|---|---|---|
| `/read-materials [파일]` | materials/*.md | _digest.md, figures/, tables/*.csv (sha 기반 증분) | LLM |
| `/plan-slides 메시지, 청중, 분` | _digest.md | deck.md + pages/*.md | LLM (짧은 Q&A 후) |
| `/plan-page add·modify·move·remove·list` | 쪽수 또는 id | `pages/<id>.md` 하나 + deck.md 의 `order` | LLM |
| `/check-plan [id…]` | pages + _digest | plan_check.md, manifest 검증 표시 (R1 refs · R2 수치 · R3 챕터 커버리지 · R4 그림 · R5 캡션 · R6 배치 dry-run) | LLM + 코드 |
| `/generate-slides [id…\|changed\|all]` | pages/<id>.md | output/pages/<id>.pptx + .png | **코드** (block 페이지만 LLM 이 `.py` 작성) |
| `/build-deck` | deck.md 의 순서 | output/deck.pptx + deck/NN.png | 코드 |
| `/write-script [id…\|all]` | duration_min | notes/<id>.md, script.md | LLM |
| `/review-edit <id>` | 생성본 vs `.edited.pptx` | 규칙 변경 제안 | LLM |

모든 명령 파일은 같은 틀을 따른다: "역할 → 산출물" 한 줄 제목, 한눈에 표(목표 · 읽는 것 · 만드는 것 · 누구에게 무엇을 보고 · 다음 명령), 흐름도, 실행 절차, 고정된 완료 보고 형식.

### 페이지 파일

```yaml
---
id: step1-result
type: text          # text | table | figure | block
chapter: 01
title: Step 1 결과   # 36pt 한 줄
refs: [calib_rmse]  # _digest.md 의 id
script: auto        # block 페이지는 custom → scripts/pages/<id>.py 의 build(slide, ctx)
---
## 소제목                       ← 16pt, 왼쪽 검정 바
- 14pt 글머리, **굵게** 가능
  - 2단계
## 표 #. 캡션은 표 위              ← '#' 은 덱 전체 자동 번호
| 열 | 열 |
|---|---|
## 글 + 그림 블록 (글 640px 좌, 그림 520px 우)
- 설명
![그림 #. 캡션은 그림 아래](materials/figures/x.png)
```

`text` · `table` · `figure` 페이지는 `scripts/render_page.py` 가 **결정적으로** 그린다. 같은 md 는 항상 같은 슬라이드가 된다. 본문이 넘치면(480px 초과) `LayoutError` 로 멈추고 페이지를 나누라고 알린다. 표·그림 캡션이 없어도 멈춘다.

### CLI

```bash
python scripts/build_deck.py list                     # 본문쪽수 · 최종쪽수 · id · 상태(planned/stale/generated) · 검증
python scripts/build_deck.py pages <id|n …> --png     # 페이지 렌더. --changed / --all / --dry
python scripts/build_deck.py deck --png               # 조립 (항상 md 에서 다시 렌더)
python scripts/build_deck.py notes                    # notes/*.md → content/script.md (쪽별·누적 시간)
python scripts/build_deck.py mark-checked <id…>       # /check-plan 통과 표시
```

`content/manifest.json` 이 페이지별 md·스크립트·렌더러의 sha 를 기억해 `--changed` 가 바뀐 것만 다시 만든다.

---

## 프로젝트 구조

```
slides-generator/            ← 이 레포 (도구)
├── install.sh
├── ppt_design.md            ← 디자인 시스템
├── commands/                ← 슬래시 커맨드 소스 (.claude/commands/ 와 동일)
├── templates/template.pptx  ← 마스터 · 레이아웃 11 · 내장 Pretendard (내용 없음)
├── examples/minimal/        ← 최소 예제 (deck.md · 페이지 3장 · block 스크립트 · 대본 1개)
├── scripts/
│   ├── lib.py               ← 빌더: chrome · section · bullets · table · 표지/목차/마무리 · 카드
│   ├── deck.py              ← deck.md / pages / manifest 모델, 쪽번호, 표·그림 번호
│   ├── render_page.py       ← 페이지 md → 슬라이드 (결정적 렌더러)
│   ├── build_deck.py        ← CLI
│   └── render_png.ps1       ← PowerPoint COM 으로 PNG 내보내기
├── requirements.txt · LICENSE (MIT)

my-talk/                     ← /slides-generator 로 생성되는 폴더
├── CLAUDE.md · ppt_design.md
├── materials/               ← 원본 .md + _digest.md + figures/ + tables/
├── content/                 ← deck.md · pages/<id>.md · notes/<id>.md · manifest.json · plan_check.md · script.md
├── templates/template.pptx
├── scripts/                 ← 공유 스크립트 + pages/<id>.py
└── output/                  ← pages/<id>.pptx|png · deck.pptx · deck/NN.png
```

---

## 디자인 시스템 (`ppt_design.md`)

| 항목 | 값 |
|---|---|
| 캔버스 | PowerPoint 기본 16:9 = 13.333" × 7.5" (1280×720 px, 1 px = 1/96") |
| 템플릿 | template.pptx 의 '빈 화면' 레이아웃 — 수업명 · 날짜 · 위/아래 가로선은 레이아웃이 그림 |
| 글자 | Pretendard. 제목 36 / 챕터 라벨 14 / 소제목 16 / 본문 14 / 표·캡션 12 pt |
| 상한·하한 | 본문 영역 18pt 초과 금지 (lib 가 예외) · 읽는 글 12pt 미만 금지 |
| 고정 chrome | 챕터 라벨 y=77 · 제목 y=100 · 첫 소제목 바 y=192 · 아래 가로선 y=688 · 쪽번호 우하단 |
| 캡션 | 표는 위 `표 #.` · 그림은 아래 `그림 #.` · 필수 · 덱 전체 자동 번호 |
| 텍스트박스 | 소제목 블록당 하나 (줄마다 만들지 않음) |
| 강조 색 | rank 1 `#2E5BFF` · 2 `#FF4D3D` · 3 `#898989` · 4 `#6E37D5` |

규칙은 생성된 슬라이드를 PowerPoint 로 고친 뒤 `/review-edit` 로 생성본과 비교해서 늘려 간다. 배운 규칙은 `ppt_design.md` 와 `lib.py` 에만 남긴다.

---

## 라이선스

MIT — `LICENSE` 참고.
