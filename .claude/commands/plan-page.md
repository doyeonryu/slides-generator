# /plan-page — 페이지 한 장 추가·수정·이동·삭제 → pages/<id>.md 하나 + deck.md 순서

인자: $ARGUMENTS
```
/plan-page add at:5 "민감도 분석 결과"        # 본문 5쪽 자리에 삽입 (기존 5쪽부터 뒤로)
/plan-page add after:step1-test "…"           # 해당 페이지 뒤에 삽입
/plan-page add "…"                            # 맨 뒤에 추가
/plan-page modify 7 "표 대신 글머리로"         # 7쪽(본문 기준) 또는 id
/plan-page move step1-result after:3
/plan-page remove 7
/plan-page list
```
쪽수는 **본문 기준**(표지·목차 제외). `list` 가 최종 쪽수도 같이 보여준다.

## 한눈에
| | |
|---|---|
| **목표** | 덱의 나머지는 건드리지 않고 **페이지 하나**만 계획을 바꾼다 |
| **읽는 것** | `content/deck.md` · 대상 `pages/<id>.md` · 수치가 필요하면 `materials/_digest.md` |
| **만드는 것** | `pages/<id>.md` 하나 (add/modify) · `deck.md` 의 `order` (add/move/remove) |
| **보고 대상** | 사용자 — 바뀐 페이지의 새 쪽수와 뒤 페이지 번호 변화, 다음 명령 |
| **다음 명령** | `/check-plan <id>` → `/generate-slides <id>` → `/build-deck` |

```
"5쪽 뒤에 민감도 분석" ──/plan-page add──▶ pages/sens-analysis.md (신규)
                                           deck.md order: […, step1-result, sens-analysis, …]
                                                  │
                                                  ▼
                                   /check-plan sens-analysis → /generate-slides sens-analysis → /build-deck
```

## 실행 절차

### 공통
- `content/deck.md` 없으면 "/plan-slides 먼저" 후 종료
- 쪽수 → id: `python scripts/build_deck.py list`
- 수치가 필요하면 `_digest.md` 에서 refs 를 고른다 (원본 재읽기 없음)

### add
1. 주제·위치 파싱. 챕터가 불명확하면 묻는다
2. id 결정 (영문 소문자-하이픈, 번호 없음, 중복 금지)
3. `content/pages/<id>.md` 작성 — 형식·규칙은 `/plan-slides` 4절과 같다 (캡션 필수, 480px 분량)
4. deck.md `order` 의 지정 위치에 삽입
5. `build_deck.py list` 로 새 쪽수 확인

### modify
1. 대상 md 를 읽고 지시대로 **그 파일만** 다시 쓴다 (id·chapter 유지)
2. 바뀐 점을 요약한다

### move / remove
- `order` 만 편집. remove 는 파일을 지우지 않고 `content/pages/_removed/` 로 옮긴다
- 뒤 페이지는 쪽수만 바뀐다. 단 `표 #.`/`그림 #.` 자동 번호가 밀리므로 **뒤 페이지도 다시 렌더** 필요 → `/generate-slides all` 안내

## 완료 보고 (사용자에게)
```
[add] sens-analysis → 본문 6쪽 (최종 8쪽). 뒤 페이지 3장 번호 +1
[modify] step1-result: 표 제거, 글머리 5개로 — 분량 ≈ 11줄
다음: /check-plan sens-analysis → /generate-slides sens-analysis → /build-deck
(표·그림 번호가 밀렸으면) 다음: /generate-slides all → /build-deck
```

## 원칙
- 한 번에 한 페이지. 전체 재계획은 `/plan-slides`
- 사용자가 손본 `output/pages/<id>.edited.pptx` 가 있으면 알린다
