# slides-generator

A page-based workflow for building presentation decks with Claude Code slash commands.
`materials/*.md` → **per-page plan** (`content/pages/<id>.md`) → validation → deterministic rendering → deck assembly → speaker script.

The page is the unit of work. Adding or editing one page never touches the others.

---

## Quick start

### 1. Install

```bash
git clone <this-repo>
cd slides-generator
bash install.sh
```

This registers 9 slash commands, 5 shared scripts, `templates/template.pptx`, and `ppt_design.md` under `~/.claude/`.

Requirements: Python 3.9+ · `pip install -r requirements.txt` (python-pptx, lxml, Pillow) · Claude Code CLI · Windows + PowerPoint for PNG previews (optional).

### 2. Create a talk folder

```bash
mkdir my-talk && cd my-talk
claude
```
```
/slides-generator My talk title
```
This creates `materials/`, `content/pages/`, `content/notes/`, `output/pages/`, `scripts/`, `templates/`, a `deck.md` skeleton, and a `CLAUDE.md`.

### 3. Add materials

Drop `.md` files into `materials/`. Paper drafts, research notes, experiment results — any format.

To try the renderer without the commands, run the minimal example from the repo root:
```bash
pip install -r requirements.txt
cp -r examples/minimal/* .
python scripts/build_deck.py pages --all --png     # output/pages/<id>.pptx (+ .png on Windows + PowerPoint)
python scripts/build_deck.py deck --png            # output/deck.pptx
```

### 4. Generate

```
/read-materials                                   → materials/_digest.md (ledger of numbers, tables, figures)
/plan-slides key message, audience, 20 min        → content/deck.md + content/pages/*.md
/check-plan                                       → content/plan_check.md (must have 0 FAIL)
/generate-slides all                              → output/pages/<id>.pptx + .png
/build-deck                                       → output/deck.pptx (cover · TOC · body · closing, numbered)
/write-script all                                 → content/notes/<id>.md → speaker notes + content/script.md
```

### 5. Partial edits

| Goal | Commands |
|---|---|
| Insert a page after page 5 | `/plan-page add after:5 "Sensitivity analysis"` → `/check-plan <id>` → `/generate-slides <id>` → `/build-deck` |
| Change page 7 | `/plan-page modify 7 "bullets instead of the table"` (or edit `pages/<id>.md` directly) → `/generate-slides 7` → `/build-deck` |
| Change a style rule | edit `ppt_design.md` / `scripts/lib.py` → `/generate-slides all` → `/build-deck` |
| Add a source file | drop it in `materials/` → `/read-materials` (processes new files only) → `/plan-page` for the affected pages |
| You edited a slide in PowerPoint | save it as `output/pages/<id>.edited.pptx` → `/review-edit <id>` → approve the proposed rule changes |

Page numbers in arguments count body pages only (cover and TOC excluded). `/plan-page list` shows both body and final numbers.

---

## How it works

```
/slides-generator → /read-materials → /plan-slides ─┬→ /check-plan → /generate-slides → /build-deck → /write-script
                                        /plan-page ─┘        ↑                                  │
                                                             └──────── /review-edit ←───────────┘
```

| Command | Reads | Produces | Done by |
|---|---|---|---|
| `/read-materials [file]` | materials/*.md | _digest.md, figures/, tables/*.csv (incremental, sha-based) | LLM |
| `/plan-slides message, audience, minutes` | _digest.md | deck.md + pages/*.md | LLM, after a short Q&A |
| `/plan-page add·modify·move·remove·list` | a page number or id | one `pages/<id>.md` + the `order` list in deck.md | LLM |
| `/check-plan [id…]` | pages + _digest | plan_check.md, "checked" mark in manifest (R1 refs · R2 numbers · R3 chapter coverage · R4 figures · R5 captions · R6 layout dry-run) | LLM + code |
| `/generate-slides [id…\|changed\|all]` | pages/<id>.md | output/pages/<id>.pptx + .png | **code** (LLM writes a `.py` only for `block` pages) |
| `/build-deck` | the order in deck.md | output/deck.pptx + deck/NN.png | code |
| `/write-script [id…\|all]` | duration_min | notes/<id>.md, script.md | LLM |
| `/review-edit <id>` | generated vs. `.edited.pptx` | proposed rule changes | LLM |

Every command file follows the same template: a one-line "role → output" title, an at-a-glance table (goal · reads · produces · who is told what · next command), a flow diagram, the procedure, and a fixed completion-report format.

### Page file

```yaml
---
id: step1-result
type: text          # text | table | figure | block
chapter: 01
title: Step 1 results   # 36pt, one line
refs: [calib_rmse]      # ids from _digest.md
script: auto            # block pages use custom → scripts/pages/<id>.py with build(slide, ctx)
---
## Section heading                 ← 16pt, black bar on the left
- 14pt bullet, **bold** allowed
  - second level
## Table #. Caption goes above      ← '#' is auto-numbered across the deck
| col | col |
|---|---|
## Text + figure block (text 640px left, figure 520px right)
- explanation
![Figure #. Caption goes below](materials/figures/x.png)
```

`text`, `table`, and `figure` pages are rendered **deterministically** by `scripts/render_page.py`: the same markdown always yields the same slide. If the body overflows (480px) the renderer stops with a `LayoutError` asking you to split the page. Missing table or figure captions also stop the render.

### CLI

```bash
python scripts/build_deck.py list                     # body # · final # · id · status (planned/stale/generated) · checked
python scripts/build_deck.py pages <id|n …> --png     # render pages. --changed / --all / --dry
python scripts/build_deck.py deck --png               # assemble (always re-renders from markdown)
python scripts/build_deck.py notes                    # notes/*.md → content/script.md with per-page and cumulative minutes
python scripts/build_deck.py mark-checked <id…>       # mark pages as passed by /check-plan
```

`content/manifest.json` stores the sha of each page's markdown, script, and the renderer, so `--changed` rebuilds only what changed.

---

## Project layout

```
slides-generator/            ← this repo (the tool)
├── install.sh
├── ppt_design.md            ← design system
├── commands/                ← slash command sources (mirrored in .claude/commands/)
├── templates/template.pptx  ← master · 11 layouts · embedded Pretendard (no content)
├── examples/minimal/        ← minimal example (deck.md · 3 pages · a block script · one note)
├── scripts/
│   ├── lib.py               ← builders: chrome · section · bullets · table · cover/TOC/closing · cards
│   ├── deck.py              ← deck.md / pages / manifest model, page numbering, table & figure numbering
│   ├── render_page.py       ← page markdown → slide (deterministic renderer)
│   ├── build_deck.py        ← CLI
│   └── render_png.ps1       ← PNG export through PowerPoint COM
├── requirements.txt · LICENSE (MIT)

my-talk/                     ← created by /slides-generator
├── CLAUDE.md · ppt_design.md
├── materials/               ← source .md + _digest.md + figures/ + tables/
├── content/                 ← deck.md · pages/<id>.md · notes/<id>.md · manifest.json · plan_check.md · script.md
├── templates/template.pptx
├── scripts/                 ← shared scripts + pages/<id>.py
└── output/                  ← pages/<id>.pptx|png · deck.pptx · deck/NN.png
```

---

## Design system (`ppt_design.md`)

| Item | Value |
|---|---|
| Canvas | PowerPoint default 16:9 = 13.333" × 7.5" (1280×720 px, 1 px = 1/96") |
| Template | the '빈 화면' (blank) layout of template.pptx — course label, date, top and bottom rules come from the layout |
| Type | Pretendard. Title 36 / chapter label 14 / section heading 16 / body 14 / tables & captions 12 pt |
| Limits | nothing above 18pt in the body region (enforced by lib) · reading text never below 12pt |
| Fixed chrome | chapter label y=77 · title y=100 · first section bar y=192 · bottom rule y=688 · page number bottom right |
| Captions | tables above (`표 #.`) · figures below (`그림 #.`) · mandatory · auto-numbered across the deck |
| Text boxes | one per section block, never one per line |
| Emphasis colors | rank 1 `#2E5BFF` · 2 `#FF4D3D` · 3 `#898989` · 4 `#6E37D5` |

Rules grow by editing a generated slide in PowerPoint and running `/review-edit` to diff it against the generated version. Learned rules live only in `ppt_design.md` and `lib.py`.

---

## License

MIT — see `LICENSE`.
