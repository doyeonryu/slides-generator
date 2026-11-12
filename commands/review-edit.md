# /review-edit — 사용자가 손본 슬라이드 비교 → 규칙 변경 제안 (ppt_design.md · lib.py)

대상: $ARGUMENTS — 페이지 id (또는 비교할 pptx 경로 2개)

## 한눈에
| | |
|---|---|
| **목표** | 사용자가 PowerPoint 로 고친 내용을 **다음 생성부터 자동으로 반영되는 규칙**으로 바꾼다 |
| **읽는 것** | `output/pages/<id>.pptx` (생성본) · `output/pages/<id>.edited.pptx` (수정본) · `ppt_design.md` · `scripts/lib.py` |
| **만드는 것** | 차이 표(분류별) · 규칙 변경 제안 · 승인 후 `ppt_design.md` / `lib.py` / `pages/<id>.md` 수정 |
| **보고 대상** | 사용자 — "무엇이 → 무엇으로, 왜(추정), 어디에 반영" 을 한 줄씩. **승인 전에는 파일을 고치지 않는다** |
| **다음 명령** | 승인·반영 후 `/generate-slides all` → `/build-deck` |

```
<id>.pptx vs <id>.edited.pptx ──/review-edit──▶ 차이 표 ──▶ 사용자 승인 ──▶ ppt_design.md / lib.py / pages/<id>.md
                                                                                  │
                                                                                  ▼
                                                                       /generate-slides all → /build-deck
```

## 실행 절차

### 1. 두 파일 덤프 (python-pptx)
- 도형 종류·이름·위치/크기(px = EMU/9525)·글자 크기(pt)·굵기·색·정렬·행간·텍스트 앞 40자
- 표: 열 폭·행 높이·셀 글자 크기 · 슬라이드 크기 (13.33×7.5" 아니면 즉시 보고)
- PNG 로 나란히 보기:
```bash
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/render_png.ps1 output/pages/<id>.edited.pptx output/pages/review/
```

### 2. 차이 분류
| 분류 | 예 | 되돌릴 곳 |
|---|---|---|
| 내용 | 문장 삭제·추가, 순서 | `pages/<id>.md` |
| 구성 | 블록 수, 2단↔1단, 카드 제거 | `pages/<id>.md` (type·블록) 또는 `render_page.py` 배치 규칙 |
| 스타일 | 글자 크기·간격·폭·색·캡션 위치 | `ppt_design.md` 표 + `lib.py` 상수 |
| 일회성 | 그 페이지에서만 맞는 조정 | 규칙화하지 않음 (기록만) |

### 3. 제안 → 승인 → 반영
- 스타일 변경은 구체적 숫자로 (예: 블록 간격 28 → 36px)
- 기존 규칙(18pt 상한 · 12pt 하한 · 캡션 위치)과 충돌하면 어느 쪽을 바꿀지 묻는다
- 승인된 것만 파일에 반영

## 완료 보고 (사용자에게)
```
차이 N건: 내용 a · 구성 b · 스타일 c · 일회성 d
제안:
  [스타일] 블록 간격 28 → 36px (글머리 블록이 붙어 보임) → ppt_design.md 간격 표 + lib.GAP_BLOCK
  [내용]   3번째 글머리 삭제 → pages/<id>.md
  [일회성] 표 폭 640 → 700 (이 표만) → 규칙화 안 함
승인할 항목을 알려주세요. 반영 후: /generate-slides all → /build-deck
```

## 원칙
- `.edited.pptx` 는 절대 수정·덮어쓰지 않는다
- 배운 규칙은 반드시 파일에 남긴다 — 대화에만 두지 않는다
