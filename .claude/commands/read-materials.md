# /read-materials — 자료 파싱 → materials/_digest.md (수치·표·그림 ledger)

폴더: $ARGUMENTS (기본 materials/)

## 한눈에
| | |
|---|---|
| **목표** | 원본 자료에서 쓸 수 있는 수치·표·그림을 **id 가 붙은 ledger** 로 뽑는다. 이후 모든 단계는 원본 대신 이 ledger 만 본다 |
| **읽는 것** | `materials/*.md` (새 파일·바뀐 파일만. sha 로 판별) |
| **만드는 것** | `materials/_digest.md` · `materials/tables/<slug>.csv` · `materials/figures/<slug>.png` |
| **보고 대상** | 사용자 — 추출 건수와 충돌 경고. 원본이 바뀐 항목은 갱신 여부를 **묻는다** |
| **다음 명령** | 처음이면 `/plan-slides`, 이미 계획이 있으면 `/plan-page` (필요한 페이지만) |

```
materials/*.md ──/read-materials──▶ _digest.md (id | type | unit | value | source | sha)
                                    tables/*.csv · figures/*.png
                                          │
                                          ▼
                                 /plan-slides 또는 /plan-page  (ledger 의 id·value 만 사용)
```

## 실행 절차

### 1. 파일 확인
$ARGUMENTS 또는 materials/ 의 .md 목록. 없으면 "materials/ 에 .md 를 넣어 주세요" 후 종료.

### 2. 파싱 & 산출
각 .md 에서:

**수치 (number)** — 패턴 `[숫자(,./+-포함)]\s*<unit>`, 단위: kWh, Nm³, MJ, kg, %, m, m², m³, °C, W, kW, zone, 구역, month, 개월, Pa
→ `id | number | unit | value | source:행 | sha`

**표 (table)** — 마크다운 표 → `materials/tables/<slug>.csv` → `id | table | — | — | source:행범위 | sha`

**자산 그림 (asset)** — `![[파일]]` / `![](경로)` 참조 + 파일 실재 → `materials/figures/<slug>.png` 복사 → `id | asset | — | 파일명 | source | sha`

**합성 그림 (synthetic)** — 데이터는 있으나 PNG 없는 시각화 대상 → csv 저장 → `id | synthetic | — | csv | source | sha`

**존재 확인** — slug+sha 일치 → skip · slug 같고 sha 다름 → "원본 변경 감지. 갱신할까요?" 확인 · 신규 → 생성

### 3. _digest.md 작성
```
| id                   | type      | unit | value   | source              | sha    |
|----------------------|-----------|------|---------|---------------------|--------|
| baseline_elec_annual | number    | kWh  | 198,294 | paper_draft.md:80   | a3f1ac |
| table_2              | table     | —    | —       | paper_draft.md:78-86| b9c2f3 |
| fig_2                | synthetic | —    | csv     | tables/fig_2.csv    | c4d301 |
| fig_1                | asset     | —    | png     | figures/fig_1.png   | d5e4ab |
```

## 완료 보고 (사용자에게)
```
_digest.md 갱신: 수치 N · 표 M · 그림 K · 합성 J  (신규 a / 갱신 b / 유지 c)
경고: [같은 수치가 소스마다 다른 경우 명시]
다음: /plan-slides [핵심 메시지, 청중, 분]   또는   /plan-page add … (페이지만 추가할 때)
```

## 원칙
- 원본 수치·표현 그대로 (임의 해석·반올림 금지)
- sha 는 추출 내용의 해시 (파일 전체 해시 아님)
