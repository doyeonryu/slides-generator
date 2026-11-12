# Slide Design System (16:9 Pretendard Edition)

> **Output format**: **PowerPoint 기본 16:9 = 13.333" × 7.5"** (12192000 × 6858000 EMU). 설계 단위는 **1280 × 720 px** (1 px = 1/96" = 9525 EMU). 이보다 큰 캔버스(예: 1920×1080 px = 20"×11.25")는 금지 — PowerPoint 기본 생성 크기보다 커져 사용자가 다시 줄여야 한다. 4:3, A4, 세로형 금지.
>
> **Base template**: 모든 슬라이드는 `templates/template.pptx` 의 **'빈 화면' 레이아웃** 위에 그린다 (`lib.new_slide()`). 레이아웃이 수업명·날짜·위/아래 가로선을 이미 그리므로 슬라이드 코드는 챕터 라벨·제목·본문·페이지 번호만 그린다.
>
> **Typeface**: **Pretendard exclusively.** 글자 크기는 **pt** 로 지정한다 (제목 36 / 챕터 라벨 14 / 소제목 16 / 본문 14 / 캡션·표 본문 12). template.pptx 에 Pretendard 가 내장되어 있다.
>
> **Logo asset**: 본문 슬라이드에는 로고를 두지 않는다. 표지·마무리에만 `deck.md` 의 `logo:` (PNG 경로) 하나를 우하단에 넣는다. 로고가 없으면 비워 둔다.

## Overview

This system is a monochrome lecture-deck language — white canvas, near-black type, thin black rules — adapted to **16:9 slide decks**. The voice is plain and technical. Color is reserved for emphasis: the deck stays predominantly monochrome, and at most a single vibrant card per slide carries the *one finding worth remembering*.

**Pretendard** anchors every surface from 80px hero displays down to 12px micro labels. The geometric, slightly humanist character of the face suits both dense data slides (where 14px body type carries 1.5 line-height for long-form prose) and high-impact section openers (where -2px letter-spacing tightens 80px headlines). For all general reading surfaces on slides, **body-like text must not go below 12pt**: this includes table text, caption-band chips, chart axis labels, footers, and other non-decorative support text. Buttons and chips are universally pill-shaped (`rounded-full`) with a sharp two-tier system: black-pill primary and outline-pill secondary. Cards split into two distinct families: **vibrant gradient product/finding cards** (32px corner softening) and **quiet white documentation cards** (16px corner softening). The doubled-radius contrast is the visual signature of "this is a featured moment."

What makes the system distinctive on slides is its **fixed-position chrome**: the course label, date label, chapter label, slide title, and first section bar all live at the same coordinates on every slide. Audiences orient themselves once and never re-anchor. The body region is treated as a content-dense canvas — never left half-empty just because the talking points ran short. A single vibrant 32px-radius card can carry the slide's headline finding; quiet white cards carry supporting detail; and a bottom stat strip or caption band fills any otherwise-empty lower zone.

**Key Characteristics:**
- Stark monochrome base — black ({colors.primary}) and white ({colors.canvas}) — broken open by saturated brand-color gradient cards reserved for emphasis moments
- Distinct product-color encoding preserved as **finding-color encoding**: coral for primary findings, magenta for evidence/data, blue for methodology, purple for limitation/future-work
- **Pretendard only** — every weight from 400 to 700, no other typefaces
- **Fixed positional grid** — chapter, title, and subtitle anchor to identical coordinates on every slide
- **No logo on content slides** — course label top-left, date top-right; a logo (PNG) appears only on the cover and closing slide
- Pill-shaped accents ({rounded.full}) for all chips, tabs, and CTAs
- **Dual card family**: 32px-radius vibrant cards for headline findings, 16px-radius white cards for supporting content
- **Dense body region** — bottom zones are intentionally filled (vibrant accent cards, stat strips, caption bands) rather than left blank
- Hero typography uses tight 1.10 line-height with -2px letter-spacing for impact
- Black promo banner ({colors.primary}) above the persistent chrome on section-divider slides

## Colors

### Brand & Accent
- **Brand Coral** ({colors.brand-coral}): Signature high-impact accent. On slides, used for the single most important finding card per slide, "NEW" badges, and section-divider accents.
- **Brand Magenta** ({colors.brand-magenta}): Secondary identity color; used for evidence/data emphasis cards and audio/qualitative findings.
- **Brand Blue** ({colors.brand-blue}): Methodology and visual/quantitative emphasis; primary blue accent across the system.
- **Brand Blue Deep** ({colors.brand-blue-deep}): Form-control activation, link emphasis, citation marks.
- **Brand Blue 700** ({colors.brand-blue-700}): Tag and reference text color.
- **Brand Cyan** ({colors.brand-cyan}): Atmospheric blue for card gradients and decorative wash.
- **Brand Blue 200** ({colors.brand-blue-200}): Code badges, info-tag backgrounds.
- **Brand Purple** ({colors.brand-purple}): Limitation, future-work, and tertiary emphasis cards; gradient mate for magenta cards.

### Surface
- **Canvas White** ({colors.canvas}): Primary slide background and quiet card surface.
- **Surface** ({colors.surface}): Subtle section backgrounds, secondary card fills, inactive chip surfaces.
- **Surface Soft** ({colors.surface-soft}): Quieter divisions inside dense data slides.
- **Hairline** ({colors.hairline}): 1px border on inputs, primary divider, table outlines.
- **Hairline Soft** ({colors.hairline-soft}): Quieter table-row dividers and secondary section breaks.

### Text
- **Ink** ({colors.ink}): Primary headline and CTA text — the brand's near-black anchor.
- **Ink Strong** ({colors.ink-strong}): Pure black used in promo banners and hero displays for maximum contrast.
- **Charcoal** ({colors.charcoal}): Body text on light surfaces.
- **Slate** ({colors.slate}): Secondary text, metadata.
- **Steel** ({colors.steel}): Tertiary text, table headers, sidebar inactive items, slide subtitles.
- **Stone** ({colors.stone}): Muted captions and tab inactive labels.
- **Muted** ({colors.muted}): Footer link text and de-emphasized labels.

### Semantic
- **Success Background** ({colors.success-bg}): Pale-green wash for success badges and confirmations.
- **Success Text** ({colors.success-text}): Deep-green ink for success badge labels.
- Error tones derive from a `#d45656` red used in error-state borders (not extracted as a top-level system token).

### Emphasis Priority Palette

Within a single slide or chart, repurpose the brand color tokens as a strict **emphasis priority palette**. Pick colors from the top of the rank list as needed; do not skip ranks.

| Rank | Token | Hex | Use |
|---|---|---|---|
| 1 (most emphasized) | `{colors.brand-blue}` | `#2E5BFF` | Primary finding, headline metric, the "our result" series, the row that proves the point |
| 2 | `{colors.brand-coral}` | `#FF4D3D` | Secondary emphasis, the reference comparison, the second-most-important series/row |
| 3 | `{colors.stone}` | `#898989` | Tertiary emphasis, intermediate baseline, neutral comparison anchor |
| 4 (least emphasized) | `{colors.brand-purple}` | `#6E37D5` | Quaternary emphasis, original baseline, the least narratively important vibrant series |

**Application rules:**
- For a 4-series chart (e.g. Figure 2 monthly profile), map series → rank by *narrative importance*, not by data order. The "our outcome" series gets rank 1, the reference it matches gets rank 2, baselines fill ranks 3–4.
- For a comparison table, the highlighted row(s) take ranks 1 and 2 in 3px-left-rule form. The proposed-framework row gets rank 1; the manual-reference row gets rank 2.
- For a single-finding card (only one vibrant card per slide), always use rank 1 (`{colors.brand-blue}`) — *unless* the slide is explicitly demoting the finding (e.g. limitations slide), in which case use rank 4 (`{colors.brand-purple}`).
- Stat strip emphasis: at most one number per strip is tinted; it must be rank 1.
- Do **not** introduce additional vibrant brand colors (magenta, cyan) into the priority hierarchy — they remain reserved for category encoding outside this palette.

## Typography

### Font Family — Pretendard Only

```
font-family: "Pretendard", "Pretendard Variable";
```

There is **no fallback** for design intent. If Pretendard cannot load, the deck should fail loudly rather than substitute. Pretendard's variable weight axis (100–900) covers every role below — the same dual fluency the original system achieved with DM Sans, now with first-class Hangul rendering at the same x-height as Latin.

Pretendard scales cleanly from 80px hero displays (where -2px letter-spacing creates magazine-grade tightness) down to 12px micro labels (where the slightly humanist counters maintain legibility). The face is used without italic emphasis — emphasis comes from weight (500/600/700) instead.

### Hierarchy

모든 크기는 **pt** (PowerPoint 글꼴 크기 그대로). template.pptx 의 원본 강의 덱(base 덱) 실측값.

| Token | Size (pt) | Weight | Line Height | Letter Spacing | Use |
|---|---|---|---|---|---|
| `{typography.hero-display}` | 54 | 700 | 1.10 | -1.5px | 표지 제목 (예: *Finite Difference: Parabolic Equations*) |
| `{typography.slide-title}` | **36** | 700 | 1.10 | -0.5px | 고정 제목 슬롯 (x=48, y=100). 한 줄 유지 |
| `{typography.title-sub}` | 18 | 500 | — | 0 | 제목 뒤에 이어 붙는 작은 부제 run (예: `30.1 THE HEAT-CONDUCTION EQUATION` + ` 열전도 방정식`) |
| `{typography.chapter-label}` | **14** | 400 | 1.20 | 0.3px | 제목 위 `CHAPTER 01 …` 라벨, STEEL. 굵게 쓰지 않는다 |
| `{typography.section-heading}` | **16** | 700 | 1.20 | 0 | 본문 소제목 — 왼쪽 6px 검정 바 + 굵은 글자 (`build_section`) |
| `{typography.body}` | **14** | 400 | 1.50 | 0 | 글머리 본문. lvl0 marL 0.25", lvl1 0.75". 강조는 700 |
| `{typography.caption}` | **12** | 700 | 1.20 | 0 | 그림/표 캡션 `그림 30.1 …`, 가운데 정렬 |
| `{typography.table-header}` | 12 | 700 | 1.20 | 0.3px | 표 머리행 (표는 전부 12pt) |
| `{typography.table-body}` | 12 | 400 | 1.30 | 0 | 표 본문 (강조 행·첫 열은 700) |
| `{typography.card-headline}` | 18 | 700 | 1.10 | -0.3px | finding card 헤드라인 — 본문 상한 |
| `{typography.card-body}` | 12 | 400 | 1.40 | 0 | finding card 본문 (ON_BLUE_SOFT), caption band 본문 (CHARCOAL) |
| `{typography.metric-number}` | 18 | 700 | 1.20 | -0.4px | finding card · stat tile 숫자 — 본문 상한 |
| `{typography.metric-label}` | 10 | 500 | 1.20 | 0 | 지표 라벨, 단위 |
| `{typography.stat-label}` | 12 | 700 | 1.20 | 0 | stat tile 제목 |
| `{typography.micro}` | 9–10 | 400–700 | 1.20 | 1.0px(배지) | 수업명 10 · 날짜 9 · 칩/배지 8–9 |
| `{typography.page-number}` | 12 | 400 | — | 0 | 페이지 번호, STEEL, 우측 정렬 |

### Principles
- **One family, weight-driven hierarchy.** Every level above resolves through Pretendard's weight axis (400 / 500 / 600 / 700) — never through font swaps.
- **Tight hero leading** (1.10) and negative letter-spacing on display sizes keep the 36–48pt titles compact.
- **Generous body leading** (1.50) keeps long-form documentation comfortable; captions push to 1.70 for scientific-paper-grade clarity.
- **위계 고정: 소제목 16 > 본문 14 > 표 12.** 본문 영역(소제목 바 아래 전부)에서 **18pt 를 넘는 글자는 금지** — 카드 헤드라인·stat 숫자도 18 이하. 36pt 는 제목 슬롯에만 쓴다. `lib._run_props` 가 18 초과를 예외로 막는다.
- **12pt floor for reading text:** 표 본문, 캡션, 카드 본문, 글머리는 12pt 미만 금지. 10pt 는 지표 라벨·단위·수업명, 9pt 는 날짜·칩·배지에만 허용.
- **Weight discipline:** 400 (body), 500 (medium emphasis), 600 (headings/buttons/chapter labels), 700 (strong inline emphasis). Heavier weights are not used.
- **Korean and Latin coexist gracefully** — Pretendard's matched x-height between scripts means mixed-script slides need no per-language overrides.

## Layout

### Slide Canvas
- **Aspect ratio**: 16:9 only
- **Size**: 13.333" × 7.5" = **1280 × 720 px** (1 px = 1/96"). PowerPoint 기본 생성 크기와 같아야 한다.
- **Safe margins**: 48px (0.5") 좌우. 위 가로선 y=48, 아래 가로선 y=688 (둘 다 레이아웃이 그림)
- **Body region**: x=48→1232, y=192→672 (**1184 × 480 px**). 첫 소제목 바가 y=192 에서 시작한다.

### Spacing System
- **Base unit**: 4px (8px primary increment).
- **Tokens**: `{spacing.xxs}` (4px) · `{spacing.xs}` (8px) · `{spacing.sm}` (12px) · `{spacing.md}` (16px) · `{spacing.lg}` (20px) · `{spacing.xl}` (24px) · `{spacing.xxl}` (32px) · `{spacing.section}` (40px).
- **Card internal padding**: finding card 20px; quiet card 16px; caption band 18px.
- **Section rhythm**: 소제목 바(36px) → 본문은 바 아래 4px 부터 (`build_section` 이 y+40 반환). 블록 사이 간격 20px.

### Grid
- Body 폭 1184px 를 **24px 거터**로 나눈다.
- Common splits:
  - 640 / 520: 표 또는 글머리(좌) + finding card 또는 그림(우) — base 덱의 기본 패턴
  - 6/6 (580 / 580): 두 개의 quiet card 또는 비교 표
  - 4 × 284 (거터 16): stat strip
  - 12 (1184): 전폭 표·차트·caption band

### Whitespace Philosophy
Cover and section-divider slides give the 80px hero display generous breathing room — `{spacing.hero}` (96px) above-the-fold creates visual oxygen. Inside data-dense content slides, whitespace tightens dramatically: section gaps drop to `{spacing.xxl}` (32px), table rows pack down to `{spacing.md}` (16px), and stat-strip cells use `{spacing.xs}` (8px) vertical rhythm. The bottom 100–140px of every body region must be filled (see Body Region Density Rules below) — empty bottom zones break the system's editorial tone.

## Persistent Slide Chrome (Fixed Position on Every Slide)

This is the **non-negotiable** structural commitment of the system. On every body slide, these elements live at identical coordinates so the audience never re-anchors.

base 덱 실측. 앞 네 줄은 **template.pptx '빈 화면' 레이아웃이 그린다** — 슬라이드 코드가 다시 그리지 않는다.

| Element | Position (1280×720 px) | Spec | 그리는 주체 |
|---|---|---|---|
| 수업명 (course label) | x=48, y=30, w=600, h=16 | Pretendard 10 / 400 / STEEL | 레이아웃 (`new_slide(course=…)` 로 교체) |
| 날짜 | x=1000, y=31, w=232, h=14, 우측 정렬 | Pretendard 9 / 400 / STEEL, `2026.10.27` 형식 | 레이아웃 (`new_slide(date=…)`) |
| 위 가로선 | x=48, y=48, w=1184, h=1 | 1px INK | 레이아웃 |
| 아래 가로선 | x=48, y=688, w=1184, h=1 | 1px INK | 레이아웃 |
| **Chapter label** | x=48, y=77, w=1184, h=23 | 14 / **400** / STEEL — 회색·보통 굵기, `CHAPTER 01 …` | `build_chrome` |
| **Slide title** | x=48, y=100, w=1184, h=60 | 36 / 700 / INK, ls 1.10, -0.5px. **부제 run 은 기본 생략** (영문 제목의 한글 번역처럼 꼭 필요할 때만) | `build_chrome` |
| **Section heading** | 바 x=48, w=6, h=36 · 글자 x=54 | 16 / 700 / INK, 왼쪽 검정 바 | `build_section` |
| Page number | x=944, y=688, w=288, h=32, 우측 정렬 | 12 / 400 / STEEL — 아래 가로선 바로 아래 | `build_footer` |

제목 슬롯은 한 줄이다. 설명성 부제는 쓰지 않는다. 영문 제목의 한글 번역이 필요할 때만 **제목 뒤에 작은 run 으로** 붙인다 (`30.1 THE HEAT-CONDUCTION EQUATION` + ` 열전도 방정식`). 본문은 **y=192 의 첫 소제목 바**에서 시작하며, 챕터·제목·소제목 바 위치는 슬라이드마다 같다.

## Body Region Density Rules

The body region (x=48→1232, y=192→672) **must not be left half-empty**. 기본 구성은 base 덱처럼 **소제목 바 + 내용** 블록을 2~3개 세로로 쌓는 것이다 (예: `열전도 방정식이란` 블록, `29장과의 차이` 블록).

**텍스트박스 단위 = 블록.** 한 소제목 아래의 글머리 전체(1·2단계 포함)를 **텍스트박스 하나**에 문단으로 넣는다 (`build_bullets`). 줄마다 텍스트박스를 따로 만들지 않는다 — PowerPoint 에서 사용자가 문단을 옮기고 고치기 어렵고, 줄 간격이 어긋난다. 소제목 바 + 제목도 블록당 하나다.

남는 공간은 아래 요소로 채운다:

1. **Vibrant finding card** (20px radius, brand-color background, 520px 폭) — 슬라이드의 핵심 결론 하나. 8pt 흰 배지, 20pt 헤드라인, 12pt 본문, 20pt 지표 2×2. 높이는 내용에 맞춰 정하고(보통 200–230px) 옆 표 높이에 묶지 않는다.
2. **Quiet white card / stat strip** (12px radius, hairline border) — 4 × 284px, 높이 84px. 22pt 숫자 + 12pt 제목 + 10pt 설명. 숫자 중 하나만 rank-1 blue.
3. **Figure + caption** — 그림 오른쪽 배치(글 640px 좌 + 그림 520px 우), 아래 12pt bold 가운데 캡션 `그림 N. …`. base 덱은 그림 배경에 연한 하늘색을 쓴다.

**캡션 규칙 (필수).** 모든 표에는 **위**에 `표 N. 설명`(소제목 바로 쓰거나 표 바로 윗줄 12pt bold), 모든 그림에는 **아래**에 `그림 N. 설명`(12pt bold, 가운데). 번호는 덱 전체 순서로 이어지며 페이지 md 에서 `표 #.` / `그림 #.` 으로 쓰면 `render_page.py` 가 자동 부여한다. 캡션이 없으면 렌더가 `LayoutError` 로 멈춘다.
4. **Caption / source / NEXT band** — 56–64px 높이, SURFACE 배경, 12px radius, 12pt 본문 + 9pt 칩.
5. **Pull quote / callout** — 한 줄 강조문, 왼쪽 coral 바.

**Density guideline**: 본문 세로 480px 중 **70% 이상**을 채운다. 마지막 요소는 아래 가로선(y=688)보다 최소 12px 위(y≤676)에서 끝나야 한다.

## Elevation & Depth

The system runs predominantly flat. Elevation is reserved for sticky panels, dropdowns, and the rare floating CTA.

| Level | Treatment | Use |
|---|---|---|
| 0 (flat) | No shadow; `{colors.hairline}` border | Default cards, table rows, form inputs |
| 1 (subtle) | `rgba(0, 0, 0, 0.04) 0px 1px 2px 0px` | Hover-elevated tiles in interactive exports |
| 2 (card) | `rgba(0, 0, 0, 0.08) 0px 4px 6px 0px` | Standard quiet white feature cards |
| 3 (atmospheric) | `rgba(0, 0, 0, 0.08) 0px 0px 22px 0px` | Diffuse glow on featured vibrant cards |
| 4 (modal) | `rgba(36, 36, 36, 0.08) 0px 12px 16px -4px` | Modals, confirmation dialogs in interactive exports |

### Decorative Depth
- The vibrant gradient finding cards carry their own atmospheric depth via internal radial gradients — no shadow needed; the color does the work.
- Brand-tinted shadows (`rgba(44, 30, 116, 0.16) 0px 0px 15px`) appear under purple-themed cards for subtle ambient lift.
- Dotted/grain textures occasionally appear inside vibrant cards as decorative content; these are not formalized as system tokens.

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.xs}` | 4px | Code chips, micro-controls |
| `{rounded.sm}` | 6px | Compact controls, table cells |
| `{rounded.md}` | 8px | Inputs, secondary buttons, image containers |
| `{rounded.lg}` | 12px | Caption bands, recommendation tiles |
| `{rounded.xl}` | 16px | Standard quiet white feature cards |
| `{rounded.xxl}` | 20px | Larger quiet feature panels |
| `{rounded.xxxl}` | 24px | Large white tile feature variants |
| `{rounded.hero}` | 32px | Vibrant gradient finding/section cards |
| `{rounded.full}` | 9999px | All buttons, all pill chips, badges |

### Photography Geometry
- Vibrant finding cards use 32px corner softening — distinct from the 16px used on quiet white cards. The doubled radius is the visual signature of "this is a featured moment."
- Imagery inside cards is treated as photographic content (silhouettes, dark studio lighting) without rounded internal frames.
- Avatar circles (rare, in testimonial-style slides) are `{rounded.full}` — perfect circles.

## Components

> Per the no-hover policy, hover states are NOT documented for slide rendering. Default and pressed/active states only.

### Buttons / Pills

**`button-primary`** — Black pill primary CTA, the dominant interactive element on interactive exports.
- Background `{colors.primary}`, text `{colors.on-primary}`, typography `{typography.button-md}`, padding `11px 24px`, rounded `{rounded.full}`.

**`button-secondary`** — Outlined pill secondary action.
- Background transparent, text `{colors.ink}`, border `1px solid {colors.ink}`, typography `{typography.button-md}`, padding `11px 24px`, rounded `{rounded.full}`.

**`button-tertiary`** — White-fill quieter pill.
- Background `{colors.canvas}`, text `{colors.ink}`, border `1px solid {colors.hairline}`, typography `{typography.button-md}`, padding `11px 24px`, rounded `{rounded.full}`.

**`chip-tag`** — Inline pill used for category/material/encoding chips inside caption bands.
- Background `{colors.surface}`, text `{colors.ink}`, typography `{typography.body-sm-medium}`, padding `6px 12px`, rounded `{rounded.full}`.

### Vibrant Finding Cards

**`finding-card-coral`** — Primary-finding signature card (slide's headline takeaway).
- Background `{colors.brand-coral}`, text `{colors.on-dark}`, rounded `{rounded.hero}` (32px), padding `{spacing.xxl}`.
- Headline in `{typography.display-lg}` or `{typography.heading-lg}` with white tagline beneath.

**`finding-card-magenta`** — Evidence / qualitative-data emphasis card.
- Background `{colors.brand-magenta}`, text `{colors.on-dark}`, rounded `{rounded.hero}`, padding `{spacing.xxl}`.

**`finding-card-blue`** — Methodology / quantitative emphasis card.
- Background `{colors.brand-blue}`, text `{colors.on-dark}`, rounded `{rounded.hero}`, padding `{spacing.xxl}`.

**`finding-card-purple`** — Limitation / future-work emphasis card.
- Background `{colors.brand-purple}`, text `{colors.on-dark}`, rounded `{rounded.hero}`, padding `{spacing.xxl}`.

**`finding-card-photo`** — Dark portrait-style card with overlaid imagery.
- Background `{colors.primary}` (black with overlaid photo), text `{colors.on-dark}`, rounded `{rounded.hero}`, padding `{spacing.xxl}`.

### Quiet Cards & Containers

**`card-base`** — Standard supporting-detail card.
- Background `{colors.canvas}`, rounded `{rounded.xl}` (16px), padding `{spacing.xl}`, border `1px solid {colors.hairline}`.

**`card-feature`** — Quieter feature panel on light gray slide.
- Background `{colors.surface}`, rounded `{rounded.xl}`, padding `{spacing.xxl}`.

**`card-recommendation`** — Compact related-content tile.
- Background `{colors.canvas}`, rounded `{rounded.lg}`, padding `{spacing.lg}`, border `1px solid {colors.hairline}`.

**`promo-cta-card`** — Bright coral promo strip on cover or closing slides.
- Background `{colors.brand-coral}`, text `{colors.on-dark}`, rounded `{rounded.hero}`, padding `{spacing.section}`. Embedded button uses `button-tertiary` (white pill on coral).

**`stat-tile`** — White card in 4-up density stat strip.
- Background `{colors.canvas}`, rounded 24px in the current PPTX implementation, padding `{spacing.xl}`, border `1px solid {colors.hairline}`. Carries a large number top and label/sub-label stack below; one cell may tint the number rank-1 blue.

### Inputs & Forms (interactive exports)

**`text-input`** — Standard text field. Background `{colors.canvas}`, text `{colors.ink}`, border `1px solid {colors.hairline}`, rounded `{rounded.md}`, padding `{spacing.sm} {spacing.md}`, height 40px.

**`text-input-focused`** — Border switches to `2px solid {colors.brand-blue-deep}`.

### Tabs / Encoding Chips

**`segmented-tab`** + **`segmented-tab-active`** — Underline-style tab navigation for interactive exports.
- Inactive: text `{colors.steel}`, transparent background, padding `{spacing.md} {spacing.lg}`. Active: text `{colors.ink}`, 2px bottom border in `{colors.ink}`.

**`pill-tab`** + **`pill-tab-active`** — Pill tab nav for category encoding.
- Inactive: background `{colors.canvas}`, text `{colors.steel}`, border `1px solid {colors.hairline}`, padding `{spacing.xs} {spacing.md}`, rounded `{rounded.full}`.
- Active: background `{colors.primary}`, text `{colors.on-primary}`, no border.

### Badges & Status

**`badge-success`** — Pale-green confirmation badge ("Equivalent", "Verified").
- Background `{colors.success-bg}`, text `{colors.success-text}`, typography `{typography.caption-bold}`, rounded `{rounded.full}`, padding `4px 10px`.

**`badge-new`** — Coral "NEW" / "FINDING" pill for fresh emphasis.
- Background `{colors.brand-coral}`, text `{colors.on-dark}`, typography `{typography.caption-bold}`, rounded `{rounded.full}`, padding `4px 10px`.

**`badge-beta`** — Pale-blue informational pill.
- Background `{colors.brand-blue-200}`, text `{colors.brand-blue-deep}`, typography `{typography.caption-bold}`, rounded `{rounded.full}`, padding `4px 10px`.

**`badge-code`** — Inline code-style chip ("Code", "API", "Q1").
- Background `{colors.brand-blue-200}`, text `{colors.brand-blue-deep}`, typography `{typography.caption-bold}`, rounded `{rounded.sm}`, padding `2px 6px`.

**`promo-banner`** — Sticky black promotional strip on section-divider slides ("Section 03 · Case Study").
- Background `{colors.primary}`, text `{colors.on-primary}`, typography `{typography.body-sm-medium}`, padding `{spacing.sm} {spacing.lg}`.

### Data Tables

**`data-table`** — Comparison table inside the body region.
- Background `{colors.canvas}`, text `{colors.ink}`, typography `{typography.body-sm}`, rounded `{rounded.md}`, border `1px solid {colors.hairline}`.

**`data-table-header`** — Top header row.
- 배경 없음, text `{colors.ink}`, 12pt / 700 with 0.3px tracking, padding 8px horizontal · 4px vertical. **표 맨 위와 머리행 아래에 1pt 검정선.**

**`data-table-row`** — Body rows.
- 배경 없음, text `{colors.ink}`, 12pt / 400, 첫 열 700. **행 사이 선 없음, 세로선 없음.** 표 맨 아래에만 1pt 검정선. 즉 표 하나에 검정선은 위 · 머리행 아래 · 아래 **세 줄뿐**이다.

**`data-table-row-highlight`** — Emphasized row (e.g., headline finding).
- Background `{colors.surface-soft}`, text `{colors.ink}`, typography `{typography.body-md}` with bold scenario names and emphasized values. In the current comparison table, the manual-reference row takes a 3px coral left rule and the proposed-framework row takes a 3px blue left rule.

### Logo (cover and closing only)
- `deck.md` 의 `logo:` 에 PNG 경로 하나. SVG 는 지원하지 않는다 (PNG 로 변환해 둔다)
- 위치: 표지·마무리 우하단 x=1008, y=445, 215×215px 안에 비율 유지 (`build_picture`)
- 본문 슬라이드에는 로고를 두지 않는다. 다른 로고와 나란히 두지 않는다

### Signature Slide Components

**`hero-band-cover`** — Centered cover-slide hero with massive 80px display + dual-pill pair.
- Layout: centered headline in `{typography.hero-display}` `{colors.ink}`, centered subtitle in `{typography.subtitle}` `{colors.steel}`, centered button row (`button-primary` + `button-secondary`).
- Cover slide is the only permitted exception to the persistent-chrome positional grid.

**`product-matrix-grid`** — 4-column row of vibrant gradient cards used for *agenda* / *contributions* slides (homepage analog).
- Each tile is one of the `finding-card-*` variants (coral, magenta, blue, purple).
- Card title in `{typography.display-lg}` (chapter wordmark) or `{typography.heading-lg}` (section title).
- Below: thin tagline in `{typography.body-sm}` 80% white opacity.
- Optional badge top-right: `badge-new` for "NEW FINDING" or `badge-beta` for "PRELIMINARY".
- Card heights uniform (~360–400px).

**`ai-product-matrix`** — 4-column grid of quiet white tiles below the vibrant matrix (e.g., method / data / result / future).
- Each tile is `card-base` chrome with a 100px-tall illustration zone, title in `{typography.card-title}`, description in `{typography.body-sm}` `{colors.steel}`.

**`docs-prose-block`** — Long-form prose region for text-heavy slides.
- Max-width ~720px inside the body region. Body in `{typography.body-md}` `{colors.charcoal}` line-height 1.6.
- Inline code in `{typography.body-md}` monospace fallback with `{colors.surface}` background and `{rounded.xs}` corners.

**`comparison-table`** — Documentation-style table comparing scenarios/models.
- Uses `data-table` chrome. Each row carries a name (linkified, in `{colors.ink}` body-sm-medium), a description column (`{colors.charcoal}`), and a metrics column. Highlight row uses `data-table-row-highlight`.

**`testimonial-stat-row`** — Stats strip ("4 / 4 scenarios", "22 / 22 zones", "12 / 12 months").
- Horizontal row of 4 stat cells; each `stat-tile` chrome.
- Numbers in `{typography.heading-lg}` `{colors.ink}`; optionally a single number tinted `{colors.brand-coral}` for the headline figure.

**`section-divider-slide`** — Black-canvas full-bleed slide that separates major chapters.
- 현재 구현은 흰 배경이다: 표지와 같은 '제목 슬라이드' 레이아웃에 `CHAPTER NN` 24pt + 챕터 제목 48pt (`build_section_divider`). `deck.md` 의 `section_dividers: true` 일 때만 들어간다 (기본 false — base 덱은 구역 머리글 없음).
- Optional vibrant gradient stripe (a single `finding-card-coral` strip) along the bottom 80px for visual punctuation.

## Slide Type Variants (instead of responsive breakpoints)

Because the output is **16:9 only**, there are no breakpoints. Instead, this section governs **inter-slide consistency** — the rules that keep a 40-slide deck feeling like one document.

### Persistent Anchors
| Anchor | Coordinate (1280×720) | Allowed to vary? |
|---|---|---|
| 수업명 | x=48, y=30 | No — 레이아웃 |
| 날짜 | x=1000, y=31 (우측 정렬) | No — 레이아웃 |
| 위 가로선 | y=48 | No — 레이아웃 |
| Chapter label | x=48, y=77 | No |
| Slide title | x=48, y=100 (36pt 한 줄) | No |
| 첫 소제목 바 | y=192 | No |
| 아래 가로선 | y=688 | No — 레이아웃 |
| Page number | x=944, y=688 (우측 정렬) | No |

### Slide Type Variants
1. **Cover slide** (`build_cover`) — '제목 슬라이드' 레이아웃 위에 날짜·위/아래 가로선을 직접 그린다. 텍스트박스 하나에 eyebrow 24pt **회색(STEEL)** / 빈 줄 / 제목 48pt bold / 부제 24pt. 좌하단 정보표: deck.md `info:` 의 행 전부(과목 · 담당교수 · 학과 · 학번 · 이름 · 이메일 · 발표일 중 준 것), 라벨 14pt bold **균등 분할** | 값 14pt, 테두리는 **위·아래 1pt 검정선만**. 우하단 로고(PNG, 선택). 닫는 슬라이드(`build_closing`)는 제목만 **"Q & A"** 로 바뀐 같은 구성 (`closing_title` 로 변경).
2. **Section divider** (`build_section_divider`, 선택) — 표지와 같은 레이아웃에 `CHAPTER NN` + 챕터 제목 48pt. 기본 꺼짐.
3. **Content slide (default)** — persistent anchors + dense body region. Optional single vibrant finding card on left (8/12) + quiet white cards on right (4/12).
4. **Full-bleed visual slide** — image fills body region (y=260→1000); chapter/title/subtitle remain in their slots overlaid with a 60% black scrim behind text if needed.
5. **Closing slide** — mirrors cover; same exception applies. Use a single `finding-card-coral` for the closing statement.

### Density Targets per Slide Type
- Cover slide: ≥40% (allows breathing room for the 80px display)
- Section divider: 0% body content (the title *is* the slide); only acceptable empty body
- Content slide: **≥70%** body vertical occupancy
- Full-bleed visual: 100% (the image is the density)
- Closing slide: ≥40%

## Do's and Don'ts

### Do
- Use **Pretendard for everything** — every heading, body, caption, chip, and badge.
- Keep the **chapter / title / subtitle in identical positions on every slide** — anchor at x=72, y=92/124/180.
- Output **16:9 (1920×1080) slides exclusively**.
- Fill the body region to ≥70% vertical occupancy with a vibrant finding card, quiet supporting cards, stat strips, or caption bands.
- Use `{colors.primary}` (ink) as the dominant CTA color — it's the brand's most recognizable interactive element.
- Reserve product brand colors (`{colors.brand-coral}`, `{colors.brand-magenta}`, `{colors.brand-blue}`, `{colors.brand-purple}`) ONLY for finding-emphasis moments — never for general buttons, body text, or generic surfaces.
- Pair `{rounded.hero}` (32px) vibrant cards with 16–24px quiet white cards in the same body region — the radius contrast is the visual signature.
- Apply `{rounded.full}` to every button, every pill chip, every badge.
- Use `{typography.hero-display}` (80px) with -2px letter-spacing for cover and section-divider hero displays — never compromise the leading or letter-spacing.
- Treat each chapter / finding category as a distinct color identity (coral=primary finding, magenta=evidence, blue=method, purple=limitation). These are deck-level assignments, not free choices.

### Don't
- **Don't introduce other fonts** — no DM Sans, no Inter, no system stacks for design surfaces.
- **Don't move the chapter, title, or subtitle slots between slides** — even an empty subtitle keeps its vertical reservation.
- **Don't put a logo on content slides** — the cover/closing PNG from `deck.md` is the only logo.
- **Don't generate 4:3, A4, or vertical layouts** — 16:9 only.
- **Don't leave the bottom of the body empty** — fill it with a vibrant finding card, stat strip, or caption band.
- Don't use brand-coral or brand-magenta on body text or large surfaces — they lose meaning when overused.
- Don't soften corners on buttons (anything less than `{rounded.full}`); the pill is a brand signature.
- Don't reduce hero leading below 1.10 — the brand needs that breathing room on the 80px display.
- Don't apply heavy shadows on quiet white cards; flat-with-borders is the default.
- Don't put gradient backgrounds on standard buttons; gradients are reserved for vibrant finding-card identity moments.
- Don't put more than one vibrant finding card per slide — the singularity is what gives it weight.

## Iteration Guide

1. 캔버스는 항상 **13.333" × 7.5" (1280×720 px)** — `lib.new_slide()` 가 template.pptx 를 열어 보장한다. `Presentation()` 을 직접 만들지 않는다.
2. Always specify **Pretendard** with pt size and weight (e.g., "Pretendard 36pt 700").
3. Always use the **fixed slot coordinates** for chapter/title/section bar — never invent new positions per slide.
4. 본문 슬라이드에 로고를 넣지 않는다. 수업명·날짜는 `new_slide(course=, date=)` 로 바꾼다.
5. Reference component names and tokens directly (`{colors.primary}`, `{component-name}-pressed`, `{rounded.full}`) — do not paraphrase.
6. When the primary content is sparse, **add a density element** (vibrant finding card, stat strip, caption band, quiet supporting cards) before considering the slide done.
7. Keep brand colors (coral, magenta, blue, purple) confined to finding-card identity. If a brand color appears on a standard button or generic surface, ask whether it earned that surface.
8. Pill-shaped buttons (`{rounded.full}`) always; squared buttons signal "third-party widget" in this language.
9. Default to `{typography.body-md}` for body and `{typography.subtitle}` for emphasis. Headlines step down `hero-display → display-lg → heading-lg → slide-title → heading-md → heading-sm`.
10. Pair 20px-radius vibrant cards with 12px-radius quiet cards — the radius contrast is the system's signature.
11. 생성 후 반드시 PowerPoint 로 PNG 를 뽑아 확인한다: 카드 밖으로 넘친 글자, 표 셀 줄바꿈, 아래 가로선 침범이 가장 흔한 실패다.

## Known Gaps

- Specific dark-mode token values (canvas, surface, ink, hairline) are not surfaced for slide use; use the section-divider variant (`{colors.primary}` background + canvas-white type) as the only "dark slide" pattern.
- Animation/transition timings are not extracted; recommend 150–200ms ease for slide-transition entrance/exit when used in interactive exports.
- Code syntax highlighting palette inside docs-prose blocks is not formalized; samples appear with system-default monospace fallback and minimal coloring.
