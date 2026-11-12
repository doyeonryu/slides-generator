# /check-plan — 페이지 계획 검증 → content/plan_check.md (PASS/FAIL 표)

대상: $ARGUMENTS (id 또는 본문 쪽수, 여러 개 가능. 없으면 전체)

## 한눈에
| | |
|---|---|
| **목표** | 렌더하기 전에 **틀린 수치·빠진 캡션·넘치는 분량**을 잡는다. FAIL 이 있는 페이지는 생성 금지 |
| **읽는 것** | `content/pages/<id>.md` · `materials/_digest.md` · dry-run 결과 |
| **만드는 것** | `content/plan_check.md` (대상 페이지 행 갱신) · 통과 페이지는 manifest 에 검증 표시 |
| **보고 대상** | 사용자 — FAIL 항목과 가장 가까운 ledger 값 제안. **수정은 하지 않는다** |
| **다음 명령** | FAIL 0 → `/generate-slides <id…>` · FAIL 있음 → 사용자가 md 수정 후 `/check-plan <id>` 재실행 |

```
pages/<id>.md + _digest.md ──/check-plan──▶ plan_check.md
        + build_deck.py pages <id> --dry          │
                                                  ├─ FAIL 0 → mark-checked → /generate-slides
                                                  └─ FAIL n → 사용자 수정 → /check-plan 재실행
```

## 실행 절차

### 1. 입력 확인
- `content/deck.md` 없으면 "/plan-slides 먼저", `_digest.md` 없으면 "/read-materials 먼저"
- 대상 id 확정: `python scripts/build_deck.py list`

### 2. 검증 규칙 (전부 엄격)
| 규칙 | 내용 |
|---|---|
| **R1 Refs 존재** | `refs:` 의 모든 id 가 _digest.md 에 있는가 |
| **R2 수치 일치** | 본문 수치 패턴(`[숫자(,./+-)]\s*<unit>`, 단위: kWh, Nm³, MJ, kg, %, m, m², m³, °C, W, kW, zone, 구역, month, 개월, Pa)이 ledger value 와 정확히 같은가. `~` → WARN. 쪽수·챕터 번호 면제 |
| **R3 챕터 커버리지** | 각 챕터에 ledger 매칭 refs 1개 이상 (전체 검사 때만) |
| **R4 Figure** | `type: figure` 는 asset/synthetic ref 1개 이상, 파일 실재 |
| **R5 캡션** | 모든 표에 `표 #.`(위), 모든 그림에 `그림 #.`(아래 alt) |
| **R6 배치** | `python scripts/build_deck.py pages <id…> --dry` — LayoutError(넘침·캡션 누락·그림 없음)면 FAIL, 메시지 그대로 기록 |

### 3. plan_check.md 작성 (대상 행만 갱신, 나머지 유지)
```
| 페이지 | 규칙 | 항목 | 상태 | 비고 |
|---|---|---|---|---|
| step1-result | R1 | refs:table_step1 | PASS | |
| step1-result | R2 | "14,800 Nm³" | FAIL | nearest: 14,880 (manual_gas_annual) |
| step1-result | R6 | dry-run | FAIL | 본문이 42px 넘침 — 페이지를 나누세요 |
```

### 4. 통과 표시
FAIL 0 인 페이지만: `python scripts/build_deck.py mark-checked <id…>`

## 완료 보고 (사용자에게)
```
검증 N쪽: PASS a · WARN b · FAIL c
FAIL 목록: step1-result R2 "14,800 Nm³" → 14,880 (manual_gas_annual) / … R6 42px 넘침
다음: (FAIL 0) /generate-slides <id…>   (FAIL 있음) pages/<id>.md 수정 → /check-plan <id>
```

## 원칙
- 보고만 한다. md 를 고치지 않는다
- `~` 근사 외 예외 없음
