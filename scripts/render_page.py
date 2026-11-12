#!/usr/bin/env python3
"""
render_page.py — 페이지 md → 슬라이드 (결정적 렌더러)

페이지 md 본문 문법
    ## 소제목                     → 왼쪽 바 소제목 (블록 시작)
    - 글머리 / (2칸 들여쓰기)- 2단계  → 14pt 글머리, 블록당 텍스트박스 하나
    일반 문장                      → 글머리 없는 14pt 문단
    | 표 | … |                     → 표 (12pt). **캡션 필수, 표 위**:
                                     소제목이 '표 N.' 으로 시작하거나, 표 바로 윗줄에 '표 N. 설명'
    ![그림 N. 캡션](경로)            → 그림. **캡션 필수, 그림 아래** (alt 텍스트가 캡션)
    번호 자리에 '#' 을 쓰면 덱 전체 순서로 자동 번호 (표 #. / 그림 #.)

배치 규칙
    - 블록 = 소제목 + 그 아래 요소들. 블록 사이 28px, 요소 사이 12px
    - 한 블록에 글(글머리/문단/표)과 그림이 같이 있으면 2단: 글 640px (좌) + 그림 520px (우)
    - 그림만 있으면 가운데 정렬, 폭 ≤ 1184
    - 본문은 y=192 에서 시작, y=672 를 넘으면 LayoutError (페이지를 나누라는 뜻)

커스텀 페이지 (script: custom): scripts/pages/<id>.py 의 build(slide, ctx) 가 본문을 그린다.
"""
import importlib.util, re
from pathlib import Path
from types import SimpleNamespace

import lib
from lib import *   # noqa
import deck as D


class LayoutError(Exception):
    pass


GAP_BLOCK, GAP_ITEM = 28, 12
COL_L, COL_R_X, COL_R_W = 640, 712, 520
CAPTION_H = 26


# ── md 블록 파서 ──────────────────────────────────────────

def parse_blocks(body):
    """[{heading: str|None, items: [(kind, payload), ...]}]  kind ∈ bullets|para|table|image"""
    blocks, cur = [], {"heading": None, "items": []}
    def flush_bullets():
        pass
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)     # 주석 제거
    body = body.replace("`", "")                            # 코드 스팬 백틱은 슬라이드에서 의미 없음
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1; continue
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            if cur["heading"] is not None or cur["items"]:
                blocks.append(cur)
            cur = {"heading": m.group(1).strip(), "items": []}
            i += 1; continue
        m = re.match(r"^(\s*)-\s+(.+)$", line)
        if m:
            level = 1 if len(m.group(1)) >= 2 else 0
            if cur["items"] and cur["items"][-1][0] == "bullets":
                cur["items"][-1][1].append((m.group(2).strip(), level))
            else:
                cur["items"].append(("bullets", [(m.group(2).strip(), level)]))
            i += 1; continue
        if line.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            cur["items"].append(("table", rows))
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line.strip())
        if m:
            cur["items"].append(("image", {"caption": m.group(1).strip(), "path": m.group(2).strip()}))
            i += 1; continue
        cur["items"].append(("para", line.strip()))
        i += 1
    if cur["heading"] is not None or cur["items"]:
        blocks.append(cur)
    return blocks


# ── 번호 / 캡션 ───────────────────────────────────────────

def _number(text, kind, state):
    """'표 #.' / '그림 #.' 자동 번호"""
    key = "표" if kind == "table" else "그림"
    if re.match(rf"^{key}\s*#\.", text):
        n = state[kind]; state[kind] += 1
        return re.sub(rf"^{key}\s*#\.", f"{key} {n}.", text)
    if re.match(rf"^{key}\s*\S+\.", text):
        state[kind] += 1
    return text


def _is_table_caption(text):  return bool(re.match(r"^표\s*\S+\.", text or ""))
def _is_fig_caption(text):    return bool(re.match(r"^그림\s*\S+\.", text or ""))


# ── 표 치수 ───────────────────────────────────────────────

def _text_px(s, size_pt):
    """글자 폭 추정: 한글 1.0em · 대문자 0.72em · 그 외 ASCII 0.58em"""
    em = size_pt * 96 / 72
    total = 0.0
    for ch in s.replace("**", ""):
        if ord(ch) > 0x2E7F: total += em
        elif ch.isupper():   total += em * 0.72
        else:                total += em * 0.58
    return total


def table_dims(rows, max_w):
    cols = max(len(r) for r in rows)
    rows = [r + [""] * (cols - len(r)) for r in rows]
    widths = []
    for c in range(cols):
        w = max(_text_px(r[c], 12) for r in rows) + 24      # 셀 여백 16 + 굵은 머리행 여유
        widths.append(int(max(60, w)))
    total = sum(widths)
    if total > max_w:
        k = max_w / total
        widths = [int(w * k) for w in widths]
    heights = []
    for ri, r in enumerate(rows):
        lines = max(lib.estimate_lines(r[c], widths[c] - 16, 12) for c in range(cols))
        heights.append(30 if ri == 0 and lines == 1 else int(lines * lib.line_px(12, 1.3)) + 10)
    return rows, widths, heights


# ── 요소 렌더 ─────────────────────────────────────────────

def _render_text_items(slide, items, x, y, w, state, pid):
    """글머리/문단/표를 세로로 그린다. 끝 y 반환."""
    for idx, (kind, payload) in enumerate(items):
        if idx: y += GAP_ITEM
        if kind == "bullets":
            h = lib.bullets_height(payload, w)
            build_bullets(slide, x, y, w, h, payload)
            y += h
        elif kind == "para":
            h = int(lib.estimate_lines(payload, w - 20, 14) * lib.line_px(14, 1.5)) + 8
            build_paragraphs(slide, x, y, w, h, [payload])
            y += h
        elif kind == "table":
            rows, widths, heights = table_dims(payload, w)
            build_table(slide, x, y, widths, heights, rows)
            y += sum(heights)
    return y


def _render_image(slide, img, x, y, max_w, max_h, pid):
    path = (D.ROOT / img["path"]) if not Path(img["path"]).is_absolute() else Path(img["path"])
    if not path.exists():
        raise LayoutError(f"[{pid}] 그림 파일 없음: {img['path']}")
    px, py, pw, ph = build_picture(slide, path, x, y, max_w, max_h - CAPTION_H, align="center")
    build_caption(slide, px, py + ph + 2, pw, img["caption"])
    return py + ph + CAPTION_H


def _prepare_captions(block, state, pid):
    """표·그림 캡션 필수 검사 + 번호 부여. 표 캡션이 소제목이면 그대로, 아니면 표 윗줄 para 를 캡션으로 승격."""
    items, out = block["items"], []
    heading = block["heading"]
    if heading and _is_table_caption(heading):
        heading = _number(heading, "table", state)
    tables_seen = 0
    for i, (kind, payload) in enumerate(items):
        if kind == "table":
            prev = out[-1] if out else None
            if prev and prev[0] == "para" and _is_table_caption(prev[1]):
                out[-1] = ("tcaption", _number(prev[1], "table", state))
            elif tables_seen == 0 and heading and _is_table_caption(heading):
                pass  # 소제목이 캡션
            else:
                raise LayoutError(f"[{pid}] 표 캡션 누락 — 소제목을 '표 #. 설명' 으로 쓰거나 표 바로 윗줄에 '표 #. 설명' 을 적으세요")
            tables_seen += 1
            out.append((kind, payload))
        elif kind == "image":
            if not _is_fig_caption(payload["caption"]):
                raise LayoutError(f"[{pid}] 그림 캡션 누락 — ![그림 #. 설명](경로) 형식으로 적으세요 ({payload['path']})")
            payload = dict(payload, caption=_number(payload["caption"], "figure", state))
            out.append((kind, payload))
        else:
            out.append((kind, payload))
    return heading, out


# ── 본문 렌더 ─────────────────────────────────────────────

def render_body(slide, page, ctx):
    pid = page["id"]
    blocks = parse_blocks(page["body"])
    state = dict(ctx.counters.get(pid, {"table": 1, "figure": 1}))
    y = BODY_TOP
    for bi, block in enumerate(blocks):
        if bi: y += GAP_BLOCK
        heading, items = _prepare_captions(block, state, pid)
        if heading:
            y = build_section(slide, y, heading)
        images = [p for k, p in items if k == "image"]
        texts  = [(k, p) for k, p in items if k != "image"]
        # 표 캡션(tcaption)은 표 위 12pt bold 줄
        def draw_texts(x, w, y0):
            yy = y0
            pending = []
            for k, p in texts:
                if k == "tcaption":
                    if pending: yy = _render_text_items(slide, pending, x, yy, w, state, pid) + GAP_ITEM; pending = []
                    build_table_caption(slide, x, yy, w, p); yy += 24
                else:
                    pending.append((k, p))
            if pending: yy = _render_text_items(slide, pending, x, yy, w, state, pid)
            return yy
        avail_h = BODY_BOTTOM - y
        if images and texts:
            y_text = draw_texts(BODY_X, COL_L, y)
            y_img = y
            for img in images:
                y_img = _render_image(slide, img, COL_R_X, y_img, COL_R_W, max(80, avail_h - (y_img - y)), pid) + GAP_ITEM
            y = max(y_text, y_img - GAP_ITEM)
        elif images:
            for ii, img in enumerate(images):
                if ii: y += GAP_ITEM
                y = _render_image(slide, img, BODY_X, y, BODY_W, max(80, BODY_BOTTOM - y), pid)
        else:
            y = draw_texts(BODY_X, BODY_W, y)
        if y > BODY_BOTTOM:
            raise LayoutError(f"[{pid}] 본문이 {y - BODY_BOTTOM}px 넘침 (y={y} > {BODY_BOTTOM}) — 페이지를 나누거나 내용을 줄이세요")
    return y


def _load_custom(pid):
    path = D.script_path(pid)
    spec = importlib.util.spec_from_file_location(f"page_{pid.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "build"):
        raise LayoutError(f"[{pid}] scripts/pages/{pid}.py 에 build(slide, ctx) 가 없습니다")
    return mod


def chapter_label(deck, page):
    meta = page["meta"]
    if meta.get("chapter_label"): return str(meta["chapter_label"])
    num = str(meta.get("chapter", "")).strip()
    if not num: return (deck.get("eyebrow") or deck.get("course", "")).upper()
    ch = D.chapter_of(deck, num)
    return f"CHAPTER {ch['num']} {ch['title']}".strip()


def render(slide, page, deck, page_num, ctx=None):
    """chrome + 본문(auto|custom) + 쪽번호 + 발표자 노트"""
    ctx = ctx or make_ctx(deck)
    build_chrome(slide, chapter_label(deck, page), str(page["meta"].get("title", "")),
                 str(page["meta"].get("title_sub", "") or ""))
    if page["meta"].get("script") == "custom":
        mod = _load_custom(page["id"])
        mod.build(slide, SimpleNamespace(page=page, deck=deck, lib=lib, counters=ctx.counters,
                                         numbering=ctx.numbering, page_num=page_num))
    else:
        render_body(slide, page, ctx)
    build_footer(slide, page_num)
    notes = D.load_notes(page["id"])
    if notes: set_notes(slide, notes["text"])


def make_ctx(deck):
    return SimpleNamespace(counters=D.counters(deck), numbering=D.numbering(deck))
