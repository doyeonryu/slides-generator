#!/usr/bin/env python3
"""
lib.py — ppt_design.md 공유 헬퍼
사용법: from lib import *

캔버스  : PowerPoint 기본 16:9 = 13.333" × 7.5"  →  설계 단위 1280 × 720 px (1 px = 1/96")
템플릿  : templates/template.pptx 의 '빈 화면' 레이아웃을 그대로 사용
          (수업명 · 날짜 · 위/아래 가로선은 레이아웃이 그린다)
글자    : Pretendard, 크기는 pt 로 지정 (제목 36 / 챕터 14 / 소제목 16 / 본문 14 / 표·캡션 12)
          본문 영역은 18pt 초과 금지 (_run_props 가 예외를 던짐) — 카드 헤드라인·지표 숫자도 18 이하
강조    : rank1=BRAND_BLUE  rank2=BRAND_CORAL  rank3=STONE  rank4=BRAND_PURPLE
"""

from datetime import date as _date
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_MARKER_STYLE

ROOT      = Path(__file__).resolve().parent.parent
TEMPLATE  = ROOT / "templates" / "template.pptx"
LAYOUT_NAME = "빈 화면"

COURSE_LABEL = "수업명"                       # 좌상단 라벨 (레이아웃 텍스트 교체)
DATE_LABEL   = _date.today().strftime("%Y.%m.%d")   # 우상단 날짜

# ── 색상 토큰 ─────────────────────────────────────────────
INK          = RGBColor(0x0a, 0x0a, 0x0a)
INK_STRONG   = RGBColor(0x00, 0x00, 0x00)
CHARCOAL     = RGBColor(0x2a, 0x2a, 0x2a)
SLATE        = RGBColor(0x4a, 0x4a, 0x4a)
STEEL        = RGBColor(0x6e, 0x6e, 0x6e)
STONE        = RGBColor(0x89, 0x89, 0x89)
MUTED        = RGBColor(0xb5, 0xb5, 0xb5)
CANVAS       = RGBColor(0xff, 0xff, 0xff)
SURFACE      = RGBColor(0xf5, 0xf5, 0xf7)
SURFACE_SOFT = RGBColor(0xfa, 0xfa, 0xfb)
HAIRLINE     = RGBColor(0xe0, 0xe0, 0xe0)
HAIRLINE_SOFT= RGBColor(0xef, 0xef, 0xef)

BRAND_BLUE   = RGBColor(0x2e, 0x5b, 0xff)
BRAND_BLUE_DP= RGBColor(0x00, 0x33, 0xcc)
BRAND_BLUE_200=RGBColor(0xdb, 0xea, 0xfe)
BRAND_CORAL  = RGBColor(0xff, 0x4d, 0x3d)
BRAND_PURPLE = RGBColor(0x6e, 0x37, 0xd5)
BRAND_MAGENTA= RGBColor(0xe8, 0x33, 0x8f)
BRAND_CYAN   = RGBColor(0x38, 0xbd, 0xf8)
ON_BLUE_SOFT = RGBColor(0xd5, 0xde, 0xff)  # 80% white on BRAND_BLUE

HEX_BRAND_BLUE  = "2E5BFF"
HEX_BRAND_CORAL = "FF4D3D"
HEX_STONE       = "898989"
HEX_BRAND_PRPL  = "6E37D5"
HEX_HAIRLINE    = "E0E0E0"
HEX_BLACK       = "000000"

EMPHASIS_RANKS     = [BRAND_BLUE, BRAND_CORAL, STONE, BRAND_PURPLE]
EMPHASIS_RANKS_HEX = [HEX_BRAND_BLUE, HEX_BRAND_CORAL, HEX_STONE, HEX_BRAND_PRPL]

# ── 슬라이드 상수 (px, 96 dpi) ─────────────────────────────
EMU_PER_PX = 9525
SLIDE_W, SLIDE_H = 1280, 720
MARGIN_X   = 48            # 좌우 여백 (0.5")
BODY_X     = MARGIN_X
BODY_W     = SLIDE_W - 2 * MARGIN_X   # 1184
BODY_TOP   = 192           # 첫 소제목 바 y
BODY_BOTTOM= 672           # 아래 가로선(688) 위 여유
FONT = "Pretendard"

# 고정 chrome 좌표 (base 덱 실측)
CHROME = dict(
    chapter = (48,  77, 1184, 23),   # 14pt bold STEEL
    title   = (48, 100, 1184, 60),   # 36pt bold INK, ls 1.1
    pagenum = (944, 688, 288, 32),   # 12pt STEEL, 우측 정렬 (아래 선 바로 아래)
)


# ── 단위 변환 ─────────────────────────────────────────────
def E(px): return Emu(int(round(px * EMU_PER_PX)))
def P(pt): return Pt(pt)


# ── 저수준 XML 헬퍼 ───────────────────────────────────────

def _set_corner_radius(shape, radius_px):
    short = min(shape.width, shape.height) / EMU_PER_PX
    adj = 50000 if radius_px * 2 >= short else int(radius_px * 2 / short * 50000)
    spPr = shape._element.find(qn("p:spPr"))
    prstGeom = spPr.find(qn("a:prstGeom"))
    avLst = prstGeom.find(qn("a:avLst"))
    if avLst is None:
        avLst = etree.SubElement(prstGeom, qn("a:avLst"))
    for c in list(avLst): avLst.remove(c)
    gd = etree.SubElement(avLst, qn("a:gd"))
    gd.set("name", "adj"); gd.set("fmla", f"val {adj}")


def _add_outer_shadow(shape, blur_px=16, dist_px=0, alpha_pct=8, color_hex="000000"):
    spPr = shape._element.find(qn("p:spPr"))
    for el in spPr.findall(qn("a:effectLst")): spPr.remove(el)
    eff = etree.SubElement(spPr, qn("a:effectLst"))
    s = etree.SubElement(eff, qn("a:outerShdw"))
    s.set("blurRad", str(int(blur_px * EMU_PER_PX)))
    s.set("dist",    str(int(dist_px * EMU_PER_PX)))
    s.set("dir", "5400000"); s.set("algn", "ctr"); s.set("rotWithShape", "0")
    clr = etree.SubElement(s, qn("a:srgbClr")); clr.set("val", color_hex)
    etree.SubElement(clr, qn("a:alpha")).set("val", str(alpha_pct * 1000))


def _suppress_effects(shape):
    spPr = shape._element.find(qn("p:spPr"))
    for el in spPr.findall(qn("a:effectLst")): spPr.remove(el)
    etree.SubElement(spPr, qn("a:effectLst"))


def _set_spc(run, spacing_pt):
    run._r.get_or_add_rPr().set("spc", str(int(spacing_pt * 100)))


def _set_cell_borders(tcPr, L=None, R=None, T=None, B=None):
    """
    표 셀 테두리. 각 인자는 None(선 없음) 또는 (폭 EMU, hex 색).
    OOXML 은 tcPr 안에서 lnL·lnR·lnT·lnB 가 채우기(noFill/solidFill)보다 **앞**에 와야 한다 —
    뒤에 붙이면 PowerPoint 가 선을 통째로 무시하므로 항상 맨 앞에 순서대로 삽입한다.
    """
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for el in tcPr.findall(qn(tag)): tcPr.remove(el)
    for i, (tag, spec) in enumerate((("a:lnL", L), ("a:lnR", R), ("a:lnT", T), ("a:lnB", B))):
        ln = etree.Element(qn(tag))
        if spec is None:
            ln.set("w", "0"); etree.SubElement(ln, qn("a:noFill"))
        else:
            w, hex_ = spec
            ln.set("w", str(int(w))); ln.set("cap", "flat"); ln.set("cmpd", "sng"); ln.set("algn", "ctr")
            sf = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr")).set("val", hex_)
            etree.SubElement(ln, qn("a:prstDash")).set("val", "solid")
        tcPr.insert(i, ln)


def _set_bullet(paragraph, level, char="•"):
    """base 덱 스타일 글머리: lvl0 marL 0.25", lvl1 0.75" (indent −0.25")."""
    pPr = paragraph._p.get_or_add_pPr()
    marL = 228600 + level * 457200
    pPr.set("marL", str(marL)); pPr.set("indent", "-228600")
    for tag in ("a:buNone", "a:buChar", "a:buFont", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)): pPr.remove(el)
    bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", "Arial")
    etree.SubElement(pPr, qn("a:buChar")).set("char", char)


# ── 도형 기본 ─────────────────────────────────────────────

def add_rect(slide, x, y, w, h, fill, *,
             radius_px=0, shadow=False, force_no_shadow=False,
             line_color=None, line_w_pt=1,
             shadow_blur_px=16, shadow_alpha_pct=8, shadow_color_hex="000000"):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius_px > 0 else MSO_SHAPE.RECTANGLE,
        E(x), E(y), E(w), E(h)
    )
    if radius_px > 0: _set_corner_radius(shp, radius_px)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line_color:
        shp.line.color.rgb = line_color; shp.line.width = Pt(line_w_pt)
    else:
        shp.line.fill.background()
    if shadow:
        _add_outer_shadow(shp, blur_px=shadow_blur_px,
                          alpha_pct=shadow_alpha_pct, color_hex=shadow_color_hex)
    elif force_no_shadow:
        _suppress_effects(shp)
    return shp


MAX_BODY_PT = 18   # 본문 영역 글자 크기 상한 (소제목 16 > 본문 14 > 표 12). 제목 chrome 만 예외.
_CHROME_MODE = [False]


def _run_props(run, *, size, weight=400, color=INK, letter_spacing=0):
    if size > MAX_BODY_PT and not _CHROME_MODE[0]:
        raise ValueError(f"본문 글자 {size}pt > {MAX_BODY_PT}pt 상한 (text={run.text[:20]!r}). "
                         f"제목 외에는 18pt 를 넘기지 않는다.")
    run.font.name = FONT; run.font.size = P(size)
    run.font.bold = (weight >= 600); run.font.color.rgb = color
    if letter_spacing: _set_spc(run, letter_spacing)


def add_text(slide, x, y, w, h, text, *,
             size=14, weight=400, color=INK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             line_spacing=None, letter_spacing=0, upper=False, margin_px=0):
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = E(margin_px)
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True; tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    if line_spacing: p.line_spacing = line_spacing
    r = p.add_run(); r.text = text.upper() if upper else text
    _run_props(r, size=size, weight=weight, color=color, letter_spacing=letter_spacing)
    return tb


def add_text_runs(slide, x, y, w, h, runs, *,
                  align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=None):
    """runs: [{"text","size","weight","color","letter_spacing"}, ...] 한 문단에 이어 붙임."""
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True; tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    if line_spacing: p.line_spacing = line_spacing
    for spec in runs:
        r = p.add_run(); r.text = spec["text"]
        _run_props(r, size=spec.get("size", 14), weight=spec.get("weight", 400),
                   color=spec.get("color", INK), letter_spacing=spec.get("letter_spacing", 0))
    return tb


def add_pill(slide, x, y, w, h, text, *,
             fill=SURFACE, fg=INK, border=None, size=10, weight=600, letter_spacing=0):
    add_rect(slide, x, y, w, h, fill, radius_px=999, line_color=border, line_w_pt=1)
    add_text(slide, x, y, w, h, text, size=size, weight=weight, color=fg,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, letter_spacing=letter_spacing)


# ── 슬라이드 유틸 ─────────────────────────────────────────

def _layout(prs):
    for l in prs.slide_layouts:
        if l.name == LAYOUT_NAME: return l
    raise SystemExit(f"[ERROR] template.pptx 에 '{LAYOUT_NAME}' 레이아웃이 없습니다: "
                     f"{[l.name for l in prs.slide_layouts]}")


def _set_layout_labels(layout, course, date):
    """레이아웃의 수업명/날짜 텍스트박스 내용 교체 (출력 파일에만 반영)."""
    for sh in layout.shapes:
        if not sh.has_text_frame or sh.is_placeholder: continue
        p = sh.text_frame.paragraphs[0]
        if not p.runs: continue
        new = date if p.alignment == PP_ALIGN.RIGHT else course
        p.runs[0].text = new
        for r in p.runs[1:]: r._r.getparent().remove(r._r)


def _layout_named(prs, name):
    for l in prs.slide_layouts:
        if l.name == name: return l
    raise SystemExit(f"[ERROR] template.pptx 에 '{name}' 레이아웃이 없습니다: "
                     f"{[l.name for l in prs.slide_layouts]}")


def new_presentation(course=None, date=None):
    """template.pptx 를 열고 슬라이드 0장인 Presentation 반환 (수업명·날짜 레이아웃 텍스트 교체)."""
    if not TEMPLATE.exists():
        raise SystemExit(f"[ERROR] 템플릿 없음: {TEMPLATE}")
    prs = Presentation(TEMPLATE)
    _set_layout_labels(_layout(prs), course or COURSE_LABEL, date or DATE_LABEL)
    return prs


def add_slide(prs, layout=LAYOUT_NAME):
    """prs 에 슬라이드 추가 (기본 '빈 화면'). 레이아웃이 복사한 placeholder 는 제거."""
    slide = prs.slides.add_slide(_layout_named(prs, layout))
    for ph in list(slide.placeholders):
        ph._element.getparent().remove(ph._element)
    return slide


def new_slide(course=None, date=None, layout=LAYOUT_NAME):
    """template.pptx 를 열고 슬라이드 하나를 추가해 (prs, slide) 반환."""
    prs = new_presentation(course, date)
    return prs, add_slide(prs, layout)


def set_notes(slide, text):
    """발표자 노트(대본) 기록."""
    if not text: return
    tf = slide.notes_slide.notes_text_frame
    tf.text = text
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.name = FONT; r.font.size = Pt(12)


# ── 텍스트 분량 추정 ──────────────────────────────────────

def estimate_lines(text, width_px, size_pt=14, indent_px=0):
    """한 문단이 몇 줄로 접히는지 추정. 한글 ≈ 1.0em, 영문·숫자 ≈ 0.55em 폭 가정."""
    em = size_pt * 96 / 72
    w = 0.0
    for ch in text.replace("**", ""):
        w += em * (1.0 if ord(ch) > 0x2E7F else 0.55)
    avail = max(1, width_px - indent_px)
    return max(1, int(w // avail) + 1)


def line_px(size_pt=14, line_spacing=1.5):
    return size_pt * line_spacing * 96 / 72


def bullets_height(items, width_px=BODY_W, size_pt=14, line_spacing=1.5):
    """build_bullets 가 차지할 높이(px) 추정."""
    total = 0
    for it in items:
        text, level = (it, 0) if isinstance(it, str) else (it[0], it[1]) if isinstance(it, tuple) else (it["text"], it.get("level", 0))
        indent = 20 + 24 + level * 48
        total += estimate_lines(text, width_px, size_pt, indent) * line_px(size_pt, line_spacing)
    return int(total) + 8


def save(prs, filename):
    out = ROOT / "output" / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out); print(f"[OK] {out}")


# ── 섹션 빌더 ─────────────────────────────────────────────

def build_chrome(slide, chapter, title, title_sub=""):
    """
    고정 chrome 중 슬라이드가 직접 그리는 부분: 챕터 라벨 + 제목.
    (수업명 · 날짜 · 가로선은 레이아웃이 그린다)
    title_sub: 기본 생략. 영문 제목의 한글 번역이 필요할 때만 (예: '열전도 방정식').
               설명성 부제("정리 결과" 같은 것)는 쓰지 않는다.
    """
    x, y, w, h = CHROME["chapter"]
    add_text(slide, x, y, w, h, chapter, size=14, weight=400, color=STEEL, letter_spacing=0.3)   # 회색·보통 굵기
    x, y, w, h = CHROME["title"]
    runs = [{"text": title, "size": 36, "weight": 700, "color": INK, "letter_spacing": -0.5}]
    if title_sub:
        runs.append({"text": "  " + title_sub, "size": 18, "weight": 500, "color": INK})
    _CHROME_MODE[0] = True
    try:
        add_text_runs(slide, x, y, w, h, runs, line_spacing=1.1)
    finally:
        _CHROME_MODE[0] = False


def build_footer(slide, page_num):
    """페이지 번호 (아래 가로선은 레이아웃이 그린다)."""
    x, y, w, h = CHROME["pagenum"]
    add_text(slide, x, y, w, h, str(page_num), size=12, weight=400, color=STEEL,
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, margin_px=10)


def build_section(slide, y, text, x=BODY_X, w=BODY_W, size=16):
    """base 덱 소제목: 왼쪽 6px 검정 바 + 16pt bold. 높이 36px. 본문은 y+40 부터."""
    add_rect(slide, x, y, 6, 36, INK, force_no_shadow=True)
    add_text(slide, x + 6, y - 1, w - 6, 38, text, size=size, weight=700, color=INK,
             anchor=MSO_ANCHOR.MIDDLE, margin_px=10)
    return y + 40


def build_bullets(slide, x, y, w, h, items, *, size=14, line_spacing=1.5, color=INK):
    """
    글머리 본문 — 소제목 하나 아래의 글머리 전체를 **텍스트박스 하나**에 문단으로 넣는다.
    (줄마다 박스를 따로 만들지 않는다: 사용자가 PowerPoint 에서 고치기 어렵다)
    items: ["문장", ("문장", 1), {"text":..., "level":1, "bold":True}, ...]
    굵은 강조는 '**굵게**' 구간으로 지정.
    """
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = E(10); tf.margin_top = tf.margin_bottom = E(4)
    tf.word_wrap = True
    first = True
    for it in items:
        if isinstance(it, str):   text, level, bold = it, 0, False
        elif isinstance(it, tuple): text, level, bold = it[0], it[1], False
        else: text, level, bold = it["text"], it.get("level", 0), it.get("bold", False)
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.line_spacing = line_spacing
        _set_bullet(p, level)
        # **굵게** 구간 분리
        parts = text.split("**")
        for i, seg in enumerate(parts):
            if not seg: continue
            r = p.add_run(); r.text = seg
            _run_props(r, size=size, weight=700 if (bold or i % 2 == 1) else 400, color=color)
    return tb


def build_paragraphs(slide, x, y, w, h, lines, *, size=14, line_spacing=1.5, color=INK):
    """글머리 없는 문단 묶음 (목차 항목 등). '**굵게**' 지원. 블록당 텍스트박스 하나."""
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = E(10); tf.margin_top = tf.margin_bottom = E(4)
    tf.word_wrap = True
    for i, text in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        for j, seg in enumerate(text.split("**")):
            if not seg: continue
            r = p.add_run(); r.text = seg
            _run_props(r, size=size, weight=700 if j % 2 == 1 else 400, color=color)
    return tb


def build_caption(slide, x, y, w, text, size=12, align=PP_ALIGN.CENTER):
    """그림 캡션: 12pt bold 가운데 정렬, 그림 **아래** (base 덱 '그림 30.1 …' 스타일)."""
    add_text(slide, x, y, w, 24, text, size=size, weight=700, color=INK,
             align=align, anchor=MSO_ANCHOR.MIDDLE)


def build_table_caption(slide, x, y, w, text):
    """표 캡션: 12pt bold 왼쪽 정렬, 표 **위**. (소제목 바가 '표 N.' 으로 시작하면 그것이 캡션)"""
    add_text(slide, x, y, w, 22, text, size=12, weight=700, color=INK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, margin_px=10)


def build_picture(slide, path, x, y, max_w, max_h, align="center"):
    """비율 유지로 (max_w × max_h) 안에 그림을 넣고 실제 (x, y, w, h) 반환."""
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(max_w / iw, max_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    if align == "center": x = x + (max_w - w) // 2
    elif align == "right": x = x + (max_w - w)
    slide.shapes.add_picture(str(path), E(x), E(y), E(w), E(h))
    return x, y, w, h


# ── 표지 · 목차 · 구역 · 마무리 (base 덱 실측) ─────────────

def _title_layout_chrome(slide, date=None):
    """'제목 슬라이드' 레이아웃에는 chrome 이 없으므로 날짜 + 위/아래 가로선을 직접 그린다."""
    add_text(slide, 1000, 31, 232, 14, date or DATE_LABEL, size=9, weight=400, color=STEEL,
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(slide, 48, 48, 1184, 1, INK, force_no_shadow=True)
    add_rect(slide, 48, 688, 1184, 1, INK, force_no_shadow=True)


def _info_table(slide, rows, x=48, y=445, col_widths=(88, 200), row_h=30):
    """
    표지 좌하단 정보표 (과목·학과·학번·이름·이메일·발표일 등 deck.info 에 있는 행 전부).
    라벨 14pt bold **균등 분할** | 값 14pt. 테두리는 **위·아래 1pt 검정선만** (세로선 없음).
    """
    if not rows: return
    tbl = slide.shapes.add_table(len(rows), 2, E(x), E(y), E(sum(col_widths)), E(row_h * len(rows))).table
    for i, w in enumerate(col_widths): tbl.columns[i].width = E(w)
    for r, (label, value) in enumerate(rows):
        tbl.rows[r].height = E(row_h)
        for c, txt in enumerate((label, value)):
            cell = tbl.cell(r, c)
            cell.margin_left = E(8); cell.margin_right = E(8); cell.margin_top = E(2); cell.margin_bottom = E(2)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.background()
            tf = cell.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.DISTRIBUTE if c == 0 else PP_ALIGN.LEFT
            run = p.runs[0] if p.runs else p.add_run(); run.text = txt
            _run_props(run, size=14, weight=700 if c == 0 else 400, color=INK)
            _set_cell_borders(cell._tc.get_or_add_tcPr(),
                              T=(12700, HEX_BLACK) if r == 0 else None,
                              B=(12700, HEX_BLACK) if r == len(rows) - 1 else None)


def _hero(slide, eyebrow, title, subtitle=""):
    """표지/마무리 공통 텍스트박스: eyebrow 24pt 회색 / (빈 줄) / 제목 48pt bold / 부제 24pt."""
    _CHROME_MODE[0] = True
    try:
        tb = slide.shapes.add_textbox(E(48), E(155), E(1175), E(240))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]; p.line_spacing = 1.5
        r = p.add_run(); r.text = eyebrow; _run_props(r, size=24, weight=400, color=STEEL)
        p = tf.add_paragraph(); p.line_spacing = 1.5
        p = tf.add_paragraph(); p.line_spacing = 1.1
        r = p.add_run(); r.text = title; _run_props(r, size=48, weight=700, color=INK, letter_spacing=-0.5)
        if subtitle:
            p = tf.add_paragraph(); p.line_spacing = 1.3
            r = p.add_run(); r.text = subtitle; _run_props(r, size=24, weight=400, color=INK)
    finally:
        _CHROME_MODE[0] = False


def build_cover(slide, deck):
    """
    표지 ('제목 슬라이드' 레이아웃 위). deck 키:
      eyebrow(기본 course) · title · subtitle · info([[라벨, 값], …]) · logo(PNG 경로, 선택) · date
    """
    _title_layout_chrome(slide, deck.get("date"))
    _hero(slide, deck.get("eyebrow") or deck.get("course", ""), deck.get("title", ""), deck.get("subtitle", ""))
    _info_table(slide, deck.get("info") or [])
    logo = deck.get("logo")
    if logo and Path(logo).exists():
        build_picture(slide, logo, 1008, 445, 215, 215, align="right")


def build_closing(slide, deck):
    """마무리: 표지와 같은 구성, 제목만 'Q & A' (deck.closing_title 로 변경 가능)."""
    _title_layout_chrome(slide, deck.get("date"))
    _hero(slide, deck.get("eyebrow") or deck.get("course", ""), deck.get("closing_title", "Q & A"))
    _info_table(slide, deck.get("info") or [])
    logo = deck.get("logo")
    if logo and Path(logo).exists():
        build_picture(slide, logo, 1008, 445, 215, 215, align="right")


def build_toc(slide, deck, chapters, page_num):
    """목차 ('빈 화면' 위): 챕터 라벨 + 제목 + '목차' 소제목 바 + 16pt 항목 (**번호** 제목 | 부제)."""
    build_chrome(slide, deck.get("toc_chapter") or (deck.get("eyebrow") or deck.get("course", "")).upper(),
                 deck.get("toc_title", "목차"))
    y = build_section(slide, BODY_TOP, "목차")
    lines = []
    for ch in chapters:
        line = f"**{ch['num']}** {ch['title']}"
        if ch.get("sub"): line += f" | {ch['sub']}"
        lines.append(line)
    h = int(len(lines) * line_px(16, 1.5)) + 8
    build_paragraphs(slide, BODY_X, y, BODY_W, h, lines, size=16, line_spacing=1.5)
    build_footer(slide, page_num)


def build_section_divider(slide, deck, chapter, page_num):
    """구역 머리글 ('제목 슬라이드' 위): CHAPTER NN / 챕터 제목 48pt. deck.section_dividers=true 일 때만."""
    _title_layout_chrome(slide, deck.get("date"))
    _hero(slide, f"CHAPTER {chapter['num']}", chapter["title"], chapter.get("sub", ""))
    build_footer(slide, page_num)


def build_caption_band(slide, label="NOTE", label_color=INK,
                       text="", chips=None, by=600, bh=64, bx=BODY_X, bw=BODY_W):
    """
    하단 정보 띠 (SURFACE 배경, 12px 라운드).
    chips: list of (label, width_px, fill_color, fg_color) — fill=CANVAS 면 hairline 테두리
    """
    add_rect(slide, bx, by, bw, bh, SURFACE, radius_px=12, force_no_shadow=True)
    chip_h = 24; chip_y = by + (bh - chip_h) // 2

    label_w = max(56, len(label) * 8 + 20)
    add_pill(slide, bx + 18, chip_y, label_w, chip_h, label,
             fill=label_color, fg=CANVAS, size=9, weight=700, letter_spacing=1.0)

    chips = chips or []
    gap = 6
    total_chip_w = sum(w for _, w, *_ in chips) + gap * max(0, len(chips) - 1)
    right_edge = bx + bw - 18
    cur_x = right_edge - total_chip_w
    legend_left = cur_x
    for spec in chips:
        lbl, w = spec[0], spec[1]
        clr = spec[2] if len(spec) > 2 else CANVAS
        fg  = spec[3] if len(spec) > 3 else INK
        bdr = HAIRLINE if clr == CANVAS else None
        add_pill(slide, cur_x, chip_y, w, chip_h, lbl, fill=clr, fg=fg, border=bdr, size=9, weight=600)
        cur_x += w + gap

    if text:
        tx = bx + 18 + label_w + 14
        tw = legend_left - tx - 12
        add_text(slide, tx, by + 10, tw, bh - 20, text, size=12, weight=400, color=CHARCOAL,
                 line_spacing=1.4, anchor=MSO_ANCHOR.MIDDLE)


# ── 표 빌더 ───────────────────────────────────────────────

def _is_num(s):
    t = s.replace(",", "").replace("%", "").replace("−", "-").replace("+", "").strip()
    try: float(t.split()[0]); return True
    except Exception: return False


def build_table(slide, x, y, col_widths, row_heights, data,
                highlight_rows=None, highlight_hex=None, right_cols=None,
                header_size=12, body_size=12):
    """
    표는 12pt (헤더 12 bold / 본문 12). 소제목 16 > 본문 14 > 표 12 위계.
    data            : list[list[str]] — 헤더 행 포함
    highlight_rows  : set[int]        — 강조 행 (3px 왼쪽 색선 + 연한 배경, 기본 rank1 blue / rank2 coral)
    right_cols      : set[int]        — 우측 정렬 열 (None 이면 숫자 열 자동 판별)
    스타일: 배경 없음. 검정 1pt 선 **세 줄만** — 표 맨 위, 머리행 아래, 표 맨 아래. 행 사이·세로선 없음
    """
    highlight_rows = highlight_rows or set()
    highlight_hex  = highlight_hex  or {}
    rows, cols = len(data), len(col_widths)
    if right_cols is None:
        right_cols = {c for c in range(1, cols)
                      if all(_is_num(data[r][c]) for r in range(1, rows) if c < len(data[r]) and data[r][c])}

    tbl = slide.shapes.add_table(rows, cols, E(x), E(y), E(sum(col_widths)), E(sum(row_heights))).table
    for i, w in enumerate(col_widths): tbl.columns[i].width = E(w)
    for i, h in enumerate(row_heights): tbl.rows[i].height = E(h)

    sorted_hl = sorted(highlight_rows)
    default_hex = {sorted_hl[0]: HEX_BRAND_CORAL, sorted_hl[-1]: HEX_BRAND_BLUE} \
                  if len(sorted_hl) >= 2 else {r: HEX_BRAND_BLUE for r in sorted_hl}

    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left  = E(10 if (r in highlight_rows and c == 0) else 8)
            cell.margin_right = E(8); cell.margin_top = E(4); cell.margin_bottom = E(4)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r in highlight_rows:
                cell.fill.solid(); cell.fill.fore_color.rgb = SURFACE_SOFT
            else:
                cell.fill.background()
            tf = cell.text_frame; tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if c in right_cols else PP_ALIGN.LEFT
            run = p.runs[0] if p.runs else p.add_run()
            run.text = data[r][c] if r < len(data) and c < len(data[r]) else ""
            _run_props(run,
                       size   = header_size if r == 0 else body_size,
                       weight = 700 if (r == 0 or c == 0 or r in highlight_rows) else 400,
                       color  = INK_STRONG if r == 0 else INK,
                       letter_spacing = 0.3 if r == 0 else 0)

    _table_borders(tbl, rows, cols, highlight_rows, {**default_hex, **highlight_hex})


def _table_borders(tbl, rows, cols, hl_rows, hl_hex):
    """검정 1pt 선 세 줄: 표 맨 위 · 머리행 아래 · 표 맨 아래. 강조 행 첫 열만 3px 색 왼쪽선."""
    for r in range(rows):
        for c in range(cols):
            _set_cell_borders(
                tbl.cell(r, c)._tc.get_or_add_tcPr(),
                L=(3 * 9525, hl_hex.get(r, HEX_BRAND_BLUE)) if (r in hl_rows and c == 0) else None,
                T=(12700, HEX_BLACK) if r == 0 else None,
                B=(12700, HEX_BLACK) if (r == 0 or r == rows - 1) else None,
            )


# ── 차트 빌더 ─────────────────────────────────────────────

def build_chart(slide, x, y, w, h,
                categories, data_dict, series_order, series_colors,
                header="", chart_type=XL_CHART_TYPE.LINE_MARKERS):
    if header:
        add_text(slide, x, y, w, 20, header, size=12, weight=700, color=INK)
        y += 24; h -= 24
    cd = CategoryChartData()
    cd.categories = categories
    for s in series_order: cd.add_series(s, data_dict[s])
    chart = slide.shapes.add_chart(chart_type, E(x), E(y), E(w), E(h), cd).chart
    chart.has_title = False; chart.has_legend = False
    for i, series in enumerate(chart.series):
        line = series.format.line
        line.color.rgb = series_colors[i]; line.width = Pt(2)
        try:
            series.marker.style = XL_MARKER_STYLE.CIRCLE; series.marker.size = 6
            series.marker.format.fill.solid()
            series.marker.format.fill.fore_color.rgb = series_colors[i]
            series.marker.format.line.color.rgb = series_colors[i]
        except Exception:
            pass
    for axis in (chart.category_axis, chart.value_axis):
        try:
            axis.tick_labels.font.name = FONT
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = STEEL
        except Exception:
            pass
    try:
        chart.value_axis.major_gridlines.format.line.color.rgb = HAIRLINE_SOFT
        chart.value_axis.major_gridlines.format.line.width = Pt(0.5)
    except Exception:
        pass
