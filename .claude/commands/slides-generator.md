# /slides-generator — 워크스페이스 초기화 → deck.md 골격 + CLAUDE.md

발표 제목: $ARGUMENTS

## 한눈에
| | |
|---|---|
| **목표** | 현재 폴더를 페이지 단위 슬라이드 작업 공간으로 만든다 |
| **읽는 것** | `~/.claude/` 의 공유 스크립트·템플릿·ppt_design.md |
| **만드는 것** | 폴더 구조 · `content/deck.md` 골격 · `CLAUDE.md` |
| **보고 대상** | 사용자 — 만든 폴더 목록과 다음 할 일 한 줄 |
| **다음 명령** | 자료를 `materials/` 에 넣고 `/read-materials` |

```
(빈 폴더) ──/slides-generator──▶ materials/ content/pages/ content/notes/ output/pages/ scripts/ templates/
                                 content/deck.md(골격) · CLAUDE.md
                                        │
                                        ▼ 사용자가 materials/*.md 투입
                                  /read-materials
```

## 실행 절차

### 1. 폴더 생성
```bash
mkdir -p materials/figures materials/tables content/pages content/notes output/pages scripts/pages templates
```

### 2. 공유 파일 복사 (`~/.claude/` 에서)
```bash
cp ~/.claude/scripts/{lib.py,deck.py,render_page.py,build_deck.py,render_png.ps1} scripts/
cp ~/.claude/templates/template.pptx templates/
cp ~/.claude/ppt_design.md ./
```
없으면 소스 경로를 사용자에게 확인한다.

### 3. content/deck.md 골격
`$ARGUMENTS` 를 title 로. **발표 시간(분)·수업명·발표일**을 모르면 이 세 가지만 묻는다.
```yaml
---
title: [발표 제목]
subtitle:
eyebrow: LAB MEETING
course: [수업명/모임명 — 모든 본문 페이지 좌상단 라벨]
date: YYYY.MM.DD
duration_min: 15
author:
info:
  - 과목 | …
  - 이름 | …
  - 발표일 | YYYY.MM.DD
chapters:
order:
toc: true
section_dividers: false
closing: true
---
```

### 4. CLAUDE.md 생성
```markdown
# [발표 제목] — slides workspace

## 워크플로우
1. materials/*.md 자료 준비
2. /read-materials                 → materials/_digest.md
3. /plan-slides [메시지, 청중, 분] → content/deck.md + content/pages/*.md
4. /check-plan [id…]               → content/plan_check.md (FAIL 0 이어야 진행)
5. /generate-slides [id…|changed|all] → output/pages/<id>.pptx + .png
6. /build-deck                     → output/deck.pptx
7. /write-script [id…|all]         → content/notes/<id>.md (발표자 노트) → /build-deck 재실행

페이지 추가·수정: /plan-page add|modify|move|remove|list
사용자가 pptx 를 손본 경우: output/pages/<id>.edited.pptx 로 저장 → /review-edit <id>

## 디렉터리
| 폴더 | 용도 |
|---|---|
| materials/ | 원본 .md + _digest.md + figures/ + tables/ |
| content/ | deck.md · pages/<id>.md · notes/<id>.md · manifest.json · plan_check.md · script.md |
| scripts/ | lib.py · deck.py · render_page.py · build_deck.py · pages/<id>.py(block 페이지만) |
| templates/ | template.pptx (마스터·레이아웃·내장 폰트) |
| output/ | pages/<id>.pptx|png · deck.pptx · deck/NN.png |

## 디자인 시스템
ppt_design.md — 캔버스 13.33"×7.5" (1280×720 px) · Pretendard · 소제목 16 > 본문 14 > 표 12 · 본문 18pt 상한
```

## 완료 보고 (사용자에게)
```
워크스페이스 준비 완료: materials/ content/pages/ content/notes/ output/pages/ scripts/ templates/
deck.md: 제목 "…", 발표 N분, 수업명 "…"
다음: materials/ 에 .md 자료를 넣고 /read-materials
```

## 원칙
- `mkdir -p` — 기존 파일 덮어쓰지 않음. 재실행 안전
