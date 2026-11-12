#!/usr/bin/env python3
"""
build_deck.py — 페이지 렌더 · 덱 조립 · 상태 조회 CLI

  python scripts/build_deck.py list
  python scripts/build_deck.py pages <id|쪽수 ...> [--png] [--dry]     # 특정 페이지
  python scripts/build_deck.py pages --changed [--png]                  # 바뀐 페이지만
  python scripts/build_deck.py pages --all [--png]
  python scripts/build_deck.py deck [--png] [--out output/deck.pptx]    # 표지·목차·본문·마무리 조립
  python scripts/build_deck.py notes                                    # content/notes/*.md → content/script.md
  python scripts/build_deck.py mark-checked <id|쪽수 ...> | --all       # /check-plan 통과 표시

페이지 미리보기: output/pages/<id>.pptx (+ .png)   덱: output/deck.pptx (+ output/deck/NN.png)
"""
import argparse, subprocess, sys, re
from pathlib import Path

for _s in (sys.stdout, sys.stderr):          # Windows 콘솔(cp949)에서도 한글·기호 출력
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib
from lib import *   # noqa
import deck as D
import render_page as R

PNG_PS1 = Path(__file__).resolve().parent / "render_png.ps1"


def _png(pptx, outdir):
    """PowerPoint COM 으로 PNG 내보내기 (Windows + PowerPoint 필요). 실패해도 치명적이지 않음."""
    if sys.platform != "win32":
        print("  [png] Windows 가 아니어서 건너뜀"); return
    outdir.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(PNG_PS1),
                            str(pptx), str(outdir)], capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            print(f"  [png] 실패: {r.stderr.strip()[:200] or r.stdout.strip()[:200]}")
        else:
            print(f"  [png] {outdir}")
    except Exception as e:
        print(f"  [png] 실패: {e}")


def _deck_kwargs(deck):
    return dict(course=deck.get("course"), date=deck.get("date"))


# ── list ─────────────────────────────────────────────────

def cmd_list(args):
    deck = D.load_deck()
    manifest = D.load_manifest()
    seq = D.sequence(deck)
    print(f"덱: {deck.get('title','')}  ·  {deck.get('duration_min','?')}분  ·  본문 {len(deck['order'])}쪽 / 전체 {len(seq)}장")
    print(f"{'본문':>4} {'최종':>4}  {'id':<28} {'type':<7} {'상태':<9} {'검증':<4} 제목")
    for it in seq:
        if it["kind"] != "page":
            label = {"cover": "표지", "toc": "목차", "closing": "마무리", "divider": "구역"}[it["kind"]]
            extra = it["chapter"]["title"] if it["kind"] == "divider" else ""
            print(f"{'':>4} {it['num']:>4}  {label:<28} {'':<7} {'':<9} {'':<4} {extra}")
            continue
        pg = it["page"]
        st, checked = D.status(pg, manifest)
        print(f"{it['body_num']:>4} {it['num']:>4}  {pg['id']:<28} {pg['meta'].get('type',''):<7} {st:<9} {'✓' if checked else '-':<4} {pg['meta'].get('title','')}")


# ── pages ────────────────────────────────────────────────

def _select(deck, args):
    manifest = D.load_manifest()
    if args.all:
        return deck["order"]
    if args.changed:
        return [pid for pid in deck["order"] if D.status(D.load_page(pid), manifest)[0] != "generated"]
    if not args.refs:
        raise D.DeckError("페이지 id/쪽수, --changed, --all 중 하나를 지정하세요")
    return [D.resolve(deck, r) for r in args.refs]


def render_page_file(deck, pid, ctx, dry=False, png=False):
    pg = D.load_page(pid)
    num = ctx.numbering[pid]
    prs, slide = new_slide(layout=LAYOUT_NAME, **_deck_kwargs(deck))
    R.render(slide, pg, deck, num, ctx)
    if dry:
        print(f"  [dry] {pid}  (최종 {num}쪽) 배치 OK"); return None
    out = D.OUT / "pages" / f"{pid}.pptx"
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    print(f"  [+] {pid}  →  {out.relative_to(D.ROOT)}  (최종 {num}쪽)")
    if png: _png(out, out.parent)
    return out


def cmd_pages(args):
    deck = D.load_deck()
    ids = _select(deck, args)
    if not ids:
        print("바뀐 페이지가 없습니다."); return
    ctx = R.make_ctx(deck)
    manifest = D.load_manifest()
    failed = []
    for pid in ids:
        try:
            out = render_page_file(deck, pid, ctx, dry=args.dry, png=args.png)
            if not args.dry:
                D.mark_rendered(manifest, D.load_page(pid), out)
        except (R.LayoutError, D.DeckError, ValueError) as e:
            failed.append((pid, str(e))); print(f"  [FAIL] {pid}: {e}")
    if not args.dry: D.save_manifest(manifest)
    if failed:
        print(f"\n{len(failed)}쪽 실패 — 페이지 md 를 고치고 다시 실행하세요.")
        sys.exit(1)


# ── deck ─────────────────────────────────────────────────

def cmd_deck(args):
    deck = D.load_deck()
    ctx = R.make_ctx(deck)
    prs = new_presentation(**_deck_kwargs(deck))
    seq = D.sequence(deck)
    failed = []
    for it in seq:
        kind = it["kind"]
        if kind == "cover":
            s = add_slide(prs, "제목 슬라이드"); build_cover(s, deck)
            n = D.load_notes("_cover");  set_notes(s, n["text"]) if n else None
        elif kind == "toc":
            s = add_slide(prs); build_toc(s, deck, deck["chapters"], it["num"])
            n = D.load_notes("_toc");    set_notes(s, n["text"]) if n else None
        elif kind == "divider":
            s = add_slide(prs, "제목 슬라이드"); build_section_divider(s, deck, it["chapter"], it["num"])
        elif kind == "closing":
            s = add_slide(prs, "제목 슬라이드"); build_closing(s, deck)
            n = D.load_notes("_closing"); set_notes(s, n["text"]) if n else None
        else:
            s = add_slide(prs)
            try:
                R.render(s, it["page"], deck, it["num"], ctx)
            except (R.LayoutError, D.DeckError, ValueError) as e:
                failed.append((it["id"], str(e))); print(f"  [FAIL] {it['id']}: {e}")
    if failed:
        print(f"\n{len(failed)}쪽 실패 — 조립을 중단합니다."); sys.exit(1)
    out = Path(args.out) if args.out else D.OUT / "deck.pptx"
    if not out.is_absolute(): out = D.ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    print(f"[OK] {out.relative_to(D.ROOT)}  ({len(seq)}장)")
    for it in seq:
        tag = it["kind"] if it["kind"] != "page" else it["page"]["meta"].get("title", it["id"])
        print(f"   {it['num']:>3}  {tag}")
    if args.png: _png(out, D.OUT / "deck")


# ── notes → script.md ────────────────────────────────────

def _minutes(meta, text):
    for key in ("minutes", "min", "time"):
        if key in meta:
            try: return float(meta[key])
            except Exception: pass
    m = re.search(r"⏱\s*([\d.]+)\s*분", text)
    return float(m.group(1)) if m else None


def cmd_notes(args):
    deck = D.load_deck()
    seq = D.sequence(deck)
    lines = [f"# 대본 — {deck.get('title','')}", "",
             f"발표 시간 {deck.get('duration_min','?')}분 · 전체 {len(seq)}장", ""]
    total = 0.0; missing = []
    for it in seq:
        pid = {"cover": "_cover", "toc": "_toc", "closing": "_closing"}.get(it["kind"], it.get("id"))
        if not pid: continue
        title = {"cover": "표지", "toc": "목차", "closing": "마무리"}.get(it["kind"]) or it["page"]["meta"].get("title", pid)
        n = D.load_notes(pid)
        if not n:
            if it["kind"] == "page": missing.append(pid)
            continue
        mins = _minutes(n["meta"], n["text"])
        if mins: total += mins
        lines += [f"## {it['num']}. {title}" + (f"  (⏱ {mins:g}분, 누적 {total:g}분)" if mins else ""), "", n["text"], ""]
    out = D.CONTENT / "script.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] {out.relative_to(D.ROOT)}  합계 {total:g}분 / 목표 {deck.get('duration_min','?')}분")
    if missing: print(f"  대본 없는 페이지: {', '.join(missing)}")


# ── mark-checked ─────────────────────────────────────────

def cmd_mark_checked(args):
    deck = D.load_deck()
    ids = deck["order"] if args.all else [D.resolve(deck, r) for r in args.refs]
    manifest = D.load_manifest()
    for pid in ids: D.mark_checked(manifest, D.load_page(pid))
    D.save_manifest(manifest)
    print(f"[OK] checked: {', '.join(ids)}")


# ── CLI ──────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="slides-generator 덱 빌더")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("pages"); p.add_argument("refs", nargs="*")
    p.add_argument("--all", action="store_true"); p.add_argument("--changed", action="store_true")
    p.add_argument("--png", action="store_true"); p.add_argument("--dry", action="store_true")
    p = sub.add_parser("deck"); p.add_argument("--png", action="store_true"); p.add_argument("--out", default=None)
    sub.add_parser("notes")
    p = sub.add_parser("mark-checked"); p.add_argument("refs", nargs="*"); p.add_argument("--all", action="store_true")
    args = ap.parse_args()
    try:
        {"list": cmd_list, "pages": cmd_pages, "deck": cmd_deck, "notes": cmd_notes,
         "mark-checked": cmd_mark_checked}[args.cmd](args)
    except D.DeckError as e:
        print(f"[ERROR] {e}"); sys.exit(2)


if __name__ == "__main__":
    main()
