#!/usr/bin/env python3
"""
block 페이지 예시 — build(slide, ctx) 만 구현한다.
chrome(챕터·제목)과 쪽번호는 render_page.render 가 그린다. 본문 영역은 y=192 → 672.
ctx: page(meta, body) · deck · lib · counters · numbering · page_num
"""
from lib import *   # noqa

CARD_HEAD = "제안 모델 → 실제 데이터 검증"
CARD_BODY = "1차 결과에서 가장 낮은 오차를 보인 제안 모델을 3개월분 실제 데이터로 검증하고, 학습 시간을 절반으로 줄인다."
CARD_METRICS = [("0.20", "", "목표 RMSE"), ("90", " s", "학습 시간 상한"),
                ("3", " 개월", "검증 데이터"), ("2/3", " 주", "보고 시점")]
STATS = [
    ("1", "주차", "데이터 정리",   "검증 구간 확정 · 전처리 재사용", INK),
    ("2", "주차", "모델 경량화",   "특징 수 축소 · 배치 크기 조정",  INK),
    ("3", "주차", "검증 실행",     "지표 산출 · 오차 분석",         BRAND_BLUE),
    ("4", "주차", "보고서",        "결과 정리 · 다음 분기 제안",     INK),
]


def _finding_card(slide, cx, cy, cw, ch):
    add_rect(slide, cx, cy, cw, ch, BRAND_BLUE, radius_px=20, shadow=True,
             shadow_color_hex=HEX_BRAND_BLUE, shadow_alpha_pct=16, shadow_blur_px=16)
    pad = 20; ix, iy, iw = cx + pad, cy + 16, cw - pad * 2
    add_pill(slide, cx + cw - pad - 64, cy + pad - 6, 64, 20, "GOAL",
             fill=CANVAS, fg=BRAND_BLUE, size=8, weight=700, letter_spacing=1.2)
    add_text(slide, ix, iy + 6, iw - 72, 28, CARD_HEAD, size=18, weight=700, color=CANVAS, line_spacing=1.1)
    add_text(slide, ix, iy + 40, iw, 48, CARD_BODY, size=12, weight=400, color=ON_BLUE_SOFT, line_spacing=1.4)
    col_w = (iw - 16) // 2
    for i, (num, unit, lbl) in enumerate(CARD_METRICS):
        mx = ix + (i % 2) * (col_w + 16); my = iy + 100 + (i // 2) * 46
        add_text_runs(slide, mx, my, col_w, 24, [
            {"text": num, "size": 18, "weight": 700, "color": CANVAS},
            {"text": unit, "size": 10, "weight": 500, "color": ON_BLUE_SOFT}])
        add_text(slide, mx, my + 24, col_w, 14, lbl, size=10, weight=500, color=ON_BLUE_SOFT)


def _stat_strip(slide, sy, sh=84):
    gap = 16; card_w = (BODY_W - gap * 3) // 4
    for i, (num, unit, lbl, sub, color) in enumerate(STATS):
        cx = BODY_X + i * (card_w + gap)
        add_rect(slide, cx, sy, card_w, sh, CANVAS, radius_px=12, line_color=HAIRLINE, force_no_shadow=True)
        ix, iy = cx + 16, sy + 10
        add_text_runs(slide, ix, iy, card_w - 32, 28, [
            {"text": num, "size": 18, "weight": 700, "color": color},
            {"text": " " + unit, "size": 10, "weight": 500, "color": STEEL}])
        add_text(slide, ix, iy + 32, card_w - 32, 18, lbl, size=12, weight=700, color=CHARCOAL)
        add_text(slide, ix, iy + 50, card_w - 32, 16, sub, size=10, weight=400, color=STEEL)


def build(slide, ctx):
    y = build_section(slide, BODY_TOP, "핵심 목표")
    items = ["검증 구간: 최근 **3개월** 실제 운영 데이터", "성능 기준: 1차 결과(0.21) 보다 낮은 **RMSE 0.20**",
             "배포 조건: 학습 **90 s 이내** — 특징 수 축소와 배치 조정으로 달성", "보고: 2월 셋째 주 세미나"]
    h = bullets_height(items, 640)
    build_bullets(slide, BODY_X, y, 640, h, items)
    _finding_card(slide, cx=BODY_X + 640 + 24, cy=y, cw=BODY_W - 640 - 24, ch=224)
    y2 = build_section(slide, y + max(h, 224) + 20, "주차별 일정")
    _stat_strip(slide, sy=y2)
