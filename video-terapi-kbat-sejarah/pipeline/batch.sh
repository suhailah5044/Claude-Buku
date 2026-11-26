#!/bin/bash
# Render HD setiap varian ikut susunan, mux audio+SFX, semak decode, commit & push setiap 2 video.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd); TMP=${TMP_DIR:-/tmp}; mkdir -p "$ROOT/final/variants"
n=0
for d in "$ROOT"/variants/v*/; do
  id=$(basename "$d"); out="$ROOT/final/variants/terapi-kbat-$id.mp4"
  [ -f "$out" ] && continue
  (cd "$d" && npx --yes hyperframes@0.9.6 render --quality delivery -o "$TMP/$id.mp4" > "$TMP/$id.log" 2>&1)
  SFX="$d/sfx.json" python3 "$ROOT/pipeline/mux.py" "$TMP/$id.mp4" "$d/assets/vo.wav" "$TMP/$id-final.mp4" 19
  ffmpeg -v error -i "$TMP/$id-final.mp4" -f null - && cp "$TMP/$id-final.mp4" "$out" && rm -f "$TMP/$id.mp4"
  echo "DONE $id $(du -m "$out" | cut -f1)MB"
  n=$((n+1))
  if [ $((n % 2)) -eq 0 ] || [ "$id" = "v10_pemeriksa" ]; then
    cd "$ROOT/.." && git add .gitignore video-terapi-kbat-sejarah && git commit -qm "Terapi KBAT Sejarah: varian hook ($id)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Y2B1CidcG6TNpQKZNv79zt" && git push -q origin claude/intelligent-galileo-seq3sp && echo "PUSHED $id"
  fi
done
