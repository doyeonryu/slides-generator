# /generate-slides — 페이지 렌더 → output/pages/<id>.pptx + .png

대상: $ARGUMENTS — `id` / 본문 쪽수 / `changed` / `all` (없으면 `changed`)

## 한눈에
| | |
|---|---|
| **목표** | 검증된 페이지 md 를 **슬라이드 한 장**으로 만들고 눈으로 확인할 PNG 를 낸다 |
| **읽는 것** | `content/pages/<id>.md` · `ppt_design.md` · block 페이지면 `scripts/pages/<id>.py` |
| **만드는 것** | `output/pages/<id>.pptx` · `output/pages/<id>.png` · manifest 갱신. block 페이지는 `scripts/pages/<id>.py` 도 |
| **보고 대상** | 사용자 — 페이지별 파일 경로와 최종 쪽수, PNG 에서 발견한 문제 |
| **다음 명령** | `/build-deck` · 손볼 페이지는 PowerPoint 로 고쳐 `.edited.pptx` 저장 → `/review-edit <id>` |

```
pages/<id>.md ──(text/table/figure: render_page.py 결정적)──▶ output/pages/<id>.pptx + .png ──▶ /build-deck
              ──(block: LLM 이 scripts/pages/<id>.py 작성)──▶          │
                                                            사용자가 손봄 → <id>.edited.pptx → /review-edit
```

## 실행 절차

### 1. 전제 확인
- `python scripts/build_deck.py list` — 대상 중 검증(✓) 안 된 페이지가 있으면 "/check-plan 먼저" 후 종료
- `ppt_design.md` 숙지: 캔버스 1280×720 · 소제목 16 > 본문 14 > 표 12 · 본문 18pt 상한 · 표 캡션 위 / 그림 캡션 아래

### 2. block 페이지만 스크립트 작성 (`script: custom`)
`scripts/pages/<id>.py` 가 없거나 md 가 바뀌었으면:
```python
from lib import *
def build(slide, ctx):          # chrome·쪽번호는 render_page 가 그린다. 본문만.
    t = ctx.counters[ctx.page["id"]]["table"]      # 덱 전체 표 번호
    y = build_section(slide, BODY_TOP, f"표 {t}. …")
    build_table(slide, x=BODY_X, y=y, col_widths=[…], row_heights=[…], data=[…])
    …                                              # 마지막 요소 y ≤ 672
```
참고: `examples/minimal/scripts/pages/next-steps.py` (글머리 + finding card + stat strip). 18pt 초과는 lib 가 예외로 막는다.

### 3. 렌더
```bash
python scripts/build_deck.py pages <id…> --png        # 또는 --changed / --all
```
- LayoutError(넘침·캡션 누락·그림 없음) → 메시지대로 md/스크립트 수정 후 재실행
- PNG 확인: 카드 밖 글자, 표 셀 줄바꿈, 아래 가로선 침범

## 완료 보고 (사용자에게)
```
렌더 N쪽:
  step1-result   → output/pages/step1-result.pptx (.png)  최종 7쪽
  …
확인 사항: [PNG 에서 본 문제. 없으면 "이상 없음"]
다음: /build-deck   ·   손볼 페이지는 output/pages/<id>.edited.pptx 로 저장 후 /review-edit <id>
```

## 원칙
- **`output/pages/<id>.edited.pptx` 는 절대 건드리지 않는다**
- text 페이지에 커스텀 스크립트를 쓰지 않는다 (md 로 해결)
- 디자인 판단은 ppt_design.md
