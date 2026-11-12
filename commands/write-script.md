# /write-script — 발표 대본 → content/notes/<id>.md (발표자 노트) + content/script.md

대상: $ARGUMENTS — `id` / 본문 쪽수 / `all` (없으면 대본 없는 페이지 전부)

## 한눈에
| | |
|---|---|
| **목표** | `duration_min` 안에서 쪽별 시간을 배분하고, **말로 읽을 대본**을 쪽마다 쓴다 |
| **읽는 것** | `content/deck.md` (duration_min, 청중) · `content/pages/<id>.md` · `materials/_digest.md` (수치 확인) |
| **만드는 것** | `content/notes/<id>.md` (쪽별, `minutes:` 포함) · `content/script.md` (전체 대본, 누적 시간) · `output/deck.pptx` 의 발표자 노트 |
| **보고 대상** | 사용자 — 쪽별 분 배분 표와 합계/목표. ±10% 넘게 어긋나면 조정안을 **확인받는다** |
| **다음 명령** | `/build-deck` 가 자동 재실행됨. 끝이면 PowerPoint 발표자 보기로 확인 |

```
deck.md(duration_min) + pages/*.md ──/write-script──▶ notes/<id>.md (⏱ 분 + 대본)
                                                            │
                                            build_deck.py notes ──▶ content/script.md (쪽별·누적 시간)
                                            build_deck.py deck  ──▶ output/deck.pptx 발표자 노트
```

## 실행 절차

### 1. 전제 확인
- `duration_min` 없으면 묻고 deck.md 에 기록
- `python scripts/build_deck.py list` 로 순서·쪽수 확인

### 2. 시간 배분
- 표지+목차 0.5분, 마무리 0.5분, 나머지를 본문에 배분
- 가중치: block/figure/table 1.5 · text 1.0 · 결론·핵심 finding +0.5
- 0.5분 단위 반올림. 합계가 목표 ±10% 를 벗어나면 조정안을 보여주고 확인

### 3. 대본 작성 (쪽마다 `content/notes/<id>.md`)
```markdown
---
minutes: 1.5
---
⏱ 1.5분

(구어체. 1분 ≈ 250자. 슬라이드 문장을 그대로 읽지 않는다:
 왜 이 페이지가 있는지 → 핵심 1~2개 → 다음 페이지로 넘어가는 한 문장)
```
- 수치는 pages/<id>.md 와 동일 (refs 밖 수치 금지)
- 표지 `_cover.md` · 목차 `_toc.md` · 마무리 `_closing.md`
- 청중 수준은 /plan-slides 때 정한 것

### 4. 묶기 + 주입
```bash
python scripts/build_deck.py notes
python scripts/build_deck.py deck
```

## 완료 보고 (사용자에게)
```
대본 N쪽 작성. 배분: 표지+목차 0.5 · 3쪽 1.5 · 4쪽 1.0 · … · 마무리 0.5 = 합계 M분 / 목표 D분
content/script.md 갱신 · output/deck.pptx 발표자 노트 반영
다음: PowerPoint 발표자 보기로 확인. 고친 대본은 notes/<id>.md 에 — all 로 다시 돌려도 덮어쓰지 않음
```

## 원칙
- 대본은 notes 에만. pages/*.md 는 건드리지 않는다
- 사용자가 고친 notes 파일은 `all` 로도 덮어쓰지 않는다 (명시적으로 지목했을 때만)
