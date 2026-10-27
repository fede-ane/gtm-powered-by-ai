#!/usr/bin/env bash
# Adds the GTM workspace and the ICP module's folders to a project folder (default: the current one).
# The .gitignore block goes in first, before any data lands in gtm/. Never overwrites a file.
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-$PWD}"
cd "$TARGET"

# A gtm/ folder that isn't ours: stop, so nothing of the owner's is mixed in.
if [ -d gtm ] && [ ! -f gtm/RULES.md ] && ! grep -qs "GTM powered by AI" gtm/README.md; then
  echo "Folder: $TARGET"
  echo "STOP: a gtm/ folder already exists and was not made by this plugin. Rename or move it, then run setup again."
  exit 3
fi

# 1. Data stays local: the .gitignore block, once.
touch .gitignore
if grep -qx 'gtm/inputs/\*\*' .gitignore; then
  gi="already there"
else
  printf '\n' >> .gitignore
  cat "$ROOT/templates/gitignore-block.txt" >> .gitignore
  gi="added"
fi

# 2. The workspace files, skipping anything that exists.
created=0; kept=0
while IFS= read -r -d '' src; do
  rel="${src#"$ROOT/templates/"}"
  if [ -e "$rel" ]; then kept=$((kept+1)); continue; fi
  mkdir -p "$(dirname "$rel")"
  cp "$src" "$rel"
  created=$((created+1))
done < <(find "$ROOT/templates/gtm" -type f -print0)
mkdir -p gtm/outputs/icp/work

# 3. Rules version: report, never replace.
ver() { sed -n 's/^version: *\([0-9][0-9]*\).*/\1/p' "$1" | head -1; }
mine="$(ver gtm/RULES.md)"; theirs="$(ver "$ROOT/templates/gtm/RULES.md")"
if [ -n "$mine" ] && [ -n "$theirs" ] && [ "$theirs" -gt "$mine" ]; then
  rules="your copy is version $mine, the plugin has version $theirs: ask the owner before replacing it"
else
  rules="version ${mine:-?}"
fi

echo "Folder: $TARGET"
echo ".gitignore block: $gi"
echo "Files created: $created. Existing files kept: $kept."
echo "gtm/RULES.md: $rules"
if command -v python3 >/dev/null 2>&1; then echo "python3: found"; else echo "python3: not found (numbers will be computed in the chat and shown in a table)"; fi
