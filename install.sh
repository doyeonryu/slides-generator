#!/bin/bash
# Slides Generator 전역 설치 스크립트
# 사용법: bash install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "[*] Slides Generator 설치 중..."

mkdir -p "$CLAUDE_DIR/commands" "$CLAUDE_DIR/scripts" "$CLAUDE_DIR/templates"

# 커맨드 (~/.claude/commands/)
cp "$SCRIPT_DIR/commands/"*.md "$CLAUDE_DIR/commands/"
echo "[+] 커맨드 설치:"
for f in "$SCRIPT_DIR/commands/"*.md; do echo "    /$(basename "$f" .md)"; done

# 공유 스크립트 (~/.claude/scripts/) — 페이지별 scripts/pages/*.py 는 프로젝트 로컬
echo "[+] 스크립트 설치:"
for name in lib.py deck.py render_page.py build_deck.py render_png.ps1; do
  f="$SCRIPT_DIR/scripts/$name"
  if [ -f "$f" ]; then cp "$f" "$CLAUDE_DIR/scripts/"; echo "    $name"; else echo "    [!] 없음: $name"; fi
done

# 템플릿 (~/.claude/templates/template.pptx)
if [ -f "$SCRIPT_DIR/templates/template.pptx" ]; then
  cp "$SCRIPT_DIR/templates/template.pptx" "$CLAUDE_DIR/templates/"
  echo "[+] template.pptx 설치 완료"
else
  echo "[!] templates/template.pptx 없음 — 수동 복사 필요"
fi

# ppt_design.md (~/.claude/)
if [ -f "$SCRIPT_DIR/ppt_design.md" ]; then
  cp "$SCRIPT_DIR/ppt_design.md" "$CLAUDE_DIR/"
  echo "[+] ppt_design.md 설치 완료"
else
  echo "[!] ppt_design.md 없음 — 수동 복사 필요"
fi

# 의존성: python-pptx, lxml, Pillow
echo ""
echo "[*] 의존성 확인 중..."
PYTHON=""
for cmd in python3 python; do
  if command -v "$cmd" &>/dev/null && "$cmd" -c "import pptx, lxml, PIL" 2>/dev/null; then PYTHON="$cmd"; break; fi
done
if [ -n "$PYTHON" ]; then
  echo "[+] python-pptx, lxml, Pillow 이미 설치됨 ($PYTHON)"
else
  pip3 install python-pptx lxml pillow 2>/dev/null || pip install python-pptx lxml pillow 2>/dev/null \
    || echo "[!] 자동 설치 실패 — 수동으로: pip install python-pptx lxml pillow"
fi

echo ""
echo "=== 설치 완료 ==="
echo ""
echo "워크플로우:"
echo "  1. 발표 폴더 생성 후 Claude Code 실행 → /slides-generator 발표제목"
echo "  2. materials/ 에 .md 자료 추가 → /read-materials"
echo "  3. /plan-slides [핵심 메시지, 청중, 분]   (부분 수정: /plan-page)"
echo "  4. /check-plan → /generate-slides → /build-deck → /write-script"
echo "  PNG 미리보기는 Windows + PowerPoint 에서만 (scripts/render_png.ps1)"
