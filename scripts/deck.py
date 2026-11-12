#!/usr/bin/env python3
"""
deck.py — 덱 모델: content/deck.md + content/pages/<id>.md + content/manifest.json

front matter 는 PyYAML 없이 읽는 최소 문법만 지원한다:
    key: 값                 (따옴표 제거, true/false, 정수 인식)
    key: [a, b, c]
    key:
      - 항목
      - 라벨 | 값           (파이프 구분은 소비자가 나눈다)
"""
import hashlib, json, re
from datetime import datetime
from pathlib import Path

ROOT     = Path(__file__).resolve().parent.parent
CONTENT  = ROOT / "content"
PAGES    = CONTENT / "pages"
NOTES    = CONTENT / "notes"
SCRIPTS  = ROOT / "scripts" / "pages"
OUT      = ROOT / "output"
MANIFEST = CONTENT / "manifest.json"
DECK_MD  = CONTENT / "deck.md"


class DeckError(Exception):
    pass


# ── front matter ─────────────────────────────────────────

def _scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'": return v[1:-1]
    if v.lower() in ("true", "yes"): return True
    if v.lower() in ("false", "no"): return False
    if re.fullmatch(r"-?[1-9]\d*|0", v): return int(v)     # "01" 같은 앞자리 0 은 문자열로 유지
    return v


def parse_front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m: return {}, text
    meta, key = {}, None
    for raw in m.group(1).split("\n"):
        if not raw.strip() or raw.strip().startswith("#"): continue
        if re.match(r"^\s+-\s+", raw) and key is not None:
            meta.setdefault(key, []).append(_scalar(re.sub(r"^\s+-\s+", "", raw)))
            continue
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if not km: continue
        key, val = km.group(1), km.group(2).strip()
        if val == "": meta[key] = []
        elif val.startswith("[") and val.endswith("]"):
            meta[key] = [_scalar(x) for x in val[1:-1].split(",") if x.strip()]
        else: meta[key] = _scalar(val)
    return meta, text[m.end():]


def sha(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


# ── deck ─────────────────────────────────────────────────

def load_deck():
    if not DECK_MD.exists():
        raise DeckError(f"content/deck.md 가 없습니다. /plan-slides 를 먼저 실행하세요.")
    meta, body = parse_front_matter(DECK_MD.read_text(encoding="utf-8"))
    chapters = []
    for item in meta.get("chapters", []) or []:
        parts = [p.strip() for p in str(item).split("|")]
        ch = {"num": parts[0], "title": parts[1] if len(parts) > 1 else ""}
        if len(parts) > 2: ch["sub"] = parts[2]
        chapters.append(ch)
    info = []
    for item in meta.get("info", []) or []:
        parts = [p.strip() for p in str(item).split("|", 1)]
        info.append((parts[0], parts[1] if len(parts) > 1 else ""))
    deck = dict(meta)
    deck["chapters"] = chapters
    deck["info"] = info
    deck["order"] = [str(x) for x in (meta.get("order", []) or [])]
    deck.setdefault("toc", True)
    deck.setdefault("closing", True)
    deck.setdefault("section_dividers", False)
    deck["body"] = body
    return deck


def _norm(num): return str(num).strip().lstrip("0") or "0"

def chapter_of(deck, num):
    for ch in deck["chapters"]:
        if _norm(ch["num"]) == _norm(num): return ch
    return {"num": str(num), "title": ""}


# ── pages ────────────────────────────────────────────────

def page_path(pid):  return PAGES / f"{pid}.md"
def script_path(pid): return SCRIPTS / f"{pid}.py"
def notes_path(pid): return NOTES / f"{pid}.md"


def load_page(pid):
    p = page_path(pid)
    if not p.exists():
        raise DeckError(f"페이지 파일 없음: content/pages/{pid}.md")
    raw = p.read_text(encoding="utf-8")
    meta, body = parse_front_matter(raw)
    meta.setdefault("id", pid)
    meta.setdefault("type", "text")
    meta.setdefault("script", "custom" if script_path(pid).exists() else "auto")
    meta.setdefault("frozen", False)
    return {"id": pid, "meta": meta, "body": body, "raw": raw, "path": p}


def body_pages(deck):
    return [load_page(pid) for pid in deck["order"]]


def load_notes(pid):
    p = notes_path(pid)
    if not p.exists(): return None
    meta, body = parse_front_matter(p.read_text(encoding="utf-8"))
    return {"meta": meta, "text": body.strip()}


def resolve(deck, ref):
    """id 또는 본문 쪽수(1-based) → id"""
    ref = str(ref).strip()
    if ref in deck["order"]: return ref
    if re.fullmatch(r"\d+", ref):
        n = int(ref)
        if 1 <= n <= len(deck["order"]): return deck["order"][n - 1]
        raise DeckError(f"본문 {n}쪽은 없습니다 (총 {len(deck['order'])}쪽)")
    raise DeckError(f"알 수 없는 페이지: {ref}")


# ── 조립 순서 / 쪽번호 ───────────────────────────────────

def sequence(deck):
    """
    최종 슬라이드 순서. 각 항목: {"kind": cover|toc|divider|page|closing, "num": 최종 쪽번호, ...}
    """
    seq = [{"kind": "cover"}]
    if deck["toc"] and deck["chapters"]:
        seq.append({"kind": "toc"})
    last_ch = None
    for i, pid in enumerate(deck["order"]):
        pg = load_page(pid)
        ch = str(pg["meta"].get("chapter", ""))
        if deck["section_dividers"] and ch and ch != last_ch:
            seq.append({"kind": "divider", "chapter": chapter_of(deck, ch)})
        last_ch = ch
        seq.append({"kind": "page", "id": pid, "body_num": i + 1, "page": pg})
    if deck["closing"]:
        seq.append({"kind": "closing"})
    for n, item in enumerate(seq, start=1):
        item["num"] = n
    return seq


def numbering(deck):
    """id → 최종 쪽번호"""
    return {it["id"]: it["num"] for it in sequence(deck) if it["kind"] == "page"}


# ── 표·그림 번호 (덱 전체 연속) ───────────────────────────

_TABLE_BLOCK = re.compile(r"(?:^\|.*\|\s*$\n?)+", re.M)
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]+\)")

def counters(deck):
    """id → {"table": 시작번호, "figure": 시작번호} (앞 페이지까지의 누적 개수 + 1)"""
    out, t, f = {}, 0, 0
    for pid in deck["order"]:
        pg = load_page(pid)
        out[pid] = {"table": t + 1, "figure": f + 1}
        t += len(_TABLE_BLOCK.findall(pg["body"]))
        f += len(_IMAGE.findall(pg["body"]))
    return out


# ── manifest ─────────────────────────────────────────────

def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(m):
    CONTENT.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def lib_sha():
    return sha((ROOT / "scripts" / "lib.py").read_text(encoding="utf-8") +
               (ROOT / "scripts" / "render_page.py").read_text(encoding="utf-8"))


def fingerprint(page):
    s = script_path(page["id"])
    return {
        "md_sha": sha(page["raw"]),
        "script_sha": sha(s.read_text(encoding="utf-8")) if s.exists() else "",
        "lib_sha": lib_sha(),
    }


def status(page, manifest):
    rec = manifest.get(page["id"])
    fp = fingerprint(page)
    checked = bool(rec) and rec.get("checked_sha") == fp["md_sha"]
    if not rec or not rec.get("rendered_at"):
        st = "planned"
    elif any(rec.get(k) != v for k, v in fp.items()):
        st = "stale"
    else:
        st = "generated"
    return st, checked


def mark_rendered(manifest, page, output):
    rec = manifest.setdefault(page["id"], {})
    rec.update(fingerprint(page))
    rec["rendered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rec["output"] = str(output.relative_to(ROOT)) if output else ""


def mark_checked(manifest, page):
    rec = manifest.setdefault(page["id"], {})
    rec["checked_sha"] = sha(page["raw"])
    rec["checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
