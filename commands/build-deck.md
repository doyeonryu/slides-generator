# /build-deck — 덱 조립 → output/deck.pptx (표지·목차·본문·마무리 + 쪽번호 + 발표자 노트)

## 한눈에
| | |
|---|---|
| **목표** | 페이지들을 deck.md 순서대로 **한 파일**로 만들어 발표에 쓸 수 있게 한다 |
| **읽는 것** | `content/deck.md` · `content/pages/*.md` · `content/notes/*.md` (있으면) |
| **만드는 것** | `output/deck.pptx` · `output/deck/NN.png` |
| **보고 대상** | 사용자 — 최종 쪽수 표, 대본 없는 페이지, 열어서 확인할 것 |
| **다음 명령** | 대본이 없으면 `/write-script` · 손본 페이지는 `/review-edit <id>` · 끝이면 PowerPoint 로 최종 확인 |

```
deck.md(순서) + pages/*.md + notes/*.md ──/build-deck──▶ output/deck.pptx (1 표지 · 2 목차 · 3… 본문 · 끝 마무리)
                                                              │
                                                              ├─ 대본 없음 → /write-script → /build-deck 재실행
                                                              └─ 사용자 최종 확인 (손봤으면 다른 이름으로 저장)
```

## 실행 절차

### 1. 전제 확인
```bash
python scripts/build_deck.py list
```
`stale`/`planned` 페이지가 있으면 알린다. 조립은 md 에서 다시 렌더하므로 결과는 최신이지만 미리보기 PNG 와 다를 수 있다.

### 2. 조립
```bash
python scripts/build_deck.py deck --png
```
실패 페이지가 있으면 중단된다 → `/generate-slides <id>` 로 먼저 고친다.

## 완료 보고 (사용자에게)
```
output/deck.pptx — N장
  1 표지 · 2 목차 · 3 [제목] · … · N 마무리
발표자 노트: K/P 쪽에 있음. 없는 쪽: [id …]
다음: /write-script (대본)   ·   PowerPoint 로 열어 확인. 손본 덱은 다른 이름으로 저장 (deck.pptx 는 재조립 때 덮어씀)
```

## 원칙
- 조립은 항상 md 에서 다시 렌더 (슬라이드 복사 없음). `deck.pptx` 는 덮어쓴다
- 표지·목차·마무리 내용은 deck.md 만 고쳐서 바꾼다
