# slides-generator — 페이지 단위 슬라이드 생성 도구

이 레포는 **도구 소스**다. 실제 발표는 별도 폴더에서 `/slides-generator`로 시작하지만, 이 레포 루트에서 그대로 돌려도 된다
(`content/`, `materials/`, `output/` 을 여기 만들면 된다. `examples/minimal/` 을 복사하면 바로 시험할 수 있다).

## 워크플로우
1. `materials/*.md` 자료 준비
2. `/read-materials`                       → materials/_digest.md (수치·표·그림 ledger)
3. `/plan-slides [메시지, 청중, 분]`       → content/deck.md + content/pages/<id>.md
4. `/check-plan [id…]`                     → content/plan_check.md (FAIL 0 이어야 진행)
5. `/generate-slides [id…|changed|all]`    → output/pages/<id>.pptx + .png
6. `/build-deck`                           → output/deck.pptx (표지·목차·본문·마무리 + 쪽번호)
7. `/write-script [id…|all]`               → content/notes/<id>.md → `/build-deck` 재실행 시 발표자 노트

페이지 추가·수정·이동·삭제: `/plan-page add|modify|move|remove|list` (쪽수 또는 id)
사용자가 PowerPoint 로 손본 페이지: `output/pages/<id>.edited.pptx` 로 저장 → `/review-edit <id>`

## 디렉터리
| 폴더 | 용도 |
|---|---|
| `commands/` | 슬래시 커맨드 소스. `.claude/commands/` 와 같은 내용 (install.sh 가 ~/.claude 로 복사). **둘 다 고친다** |
| `scripts/` | lib.py(빌더) · deck.py(모델) · render_page.py(렌더러) · build_deck.py(CLI) · render_png.ps1 |
| `templates/` | template.pptx — 마스터 · 레이아웃 11 · 내장 Pretendard. 모든 슬라이드의 base. 내용 없음 |
| `examples/minimal/` | 최소 예제 (deck.md · 페이지 3장 · block 스크립트 · 대본) |
| `ppt_design.md` | 디자인 규칙. 렌더러가 따르는 수치는 lib.py 상수와 같아야 한다 |
| 작업 폴더 (생성됨) | `materials/` · `content/`(deck.md · pages/ · notes/ · manifest.json) · `output/`(pages/ · deck.pptx) · `scripts/pages/<id>.py` |

## CLI
```bash
python scripts/build_deck.py list                      # id ↔ 쪽수 ↔ 상태
python scripts/build_deck.py pages <id|n …> --png      # 페이지 렌더 (--changed / --all / --dry)
python scripts/build_deck.py deck --png                # 조립
python scripts/build_deck.py notes                     # 대본 묶기 → content/script.md
```

## 디자인 시스템 요약 (ppt_design.md)
- 캔버스 PowerPoint 기본 16:9 = 13.333" × 7.5" (1280×720 px). 다른 크기 금지
- Pretendard · 제목 36 / 챕터 라벨 14 / 소제목 16 / 본문 14 / 표·캡션 12 (pt). 본문 영역 18pt 초과 금지
- 수업명·날짜·위/아래 가로선은 템플릿 레이아웃이 그린다. 본문 슬라이드에 로고 없음
- 표 캡션은 표 위(`표 #.`), 그림 캡션은 그림 아래(`그림 #.`). 필수. `#` 은 자동 번호
- 글머리는 소제목 블록당 텍스트박스 하나. 제목 뒤 설명성 부제 금지

## 작업 규칙
- 생성 출력은 사용자가 손볼 수 있다. `.edited.pptx` 는 절대 덮어쓰지 않는다
- 사용자 수정에서 배운 규칙은 ppt_design.md 와 lib.py 에 남긴다
- 개인 정보(이름·과목·학번)는 레포에 넣지 않는다. deck.md 의 `info:` 로만 들어간다
