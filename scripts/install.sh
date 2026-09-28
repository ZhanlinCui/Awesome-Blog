#!/usr/bin/env bash
# Awesome-Blog Agent Skills Kit installer
#
# Installs skills into the skills directory of Agent Skills compatible hosts
# (Claude Code, Cursor, Codex, ...). Two modes:
#
#   copy  (default): each selected skill is copied as a SELF-CONTAINED folder;
#                    the kit's shared assets (references/, templates/,
#                    checklists/, scripts/) are bundled INSIDE the skill and
#                    internal paths are rewritten, so a single copied folder
#                    works standalone and can be shared with teammates.
#   link:            symlinks the whole repo's skill folders; all shared assets
#                    resolve to the cloned repo (best for development).
#
# This installer never logs into anything, never uploads, and never publishes.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="copy"
HOST="claude"
DEST=""
LINK_MODE=0
ONLY=()

ALL_SKILLS=(
  tech-blog-en dev-post-zh deep-research-report content-research-writer
  blogkit-assets topic-brief research-evidence collaborative-outline
  technical-blog-writing wechat-zhihu-longform fact-checker code-verifier
  editor-polish-zh editor-polish-en seo-geo-optimizer preflight-gatekeeper
  article-refresh-decay
)

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [options] [skill ...]

Options:
  --host claude|cursor|codex   target host (default: claude)
  --dest DIR                   explicit skills directory (overrides --host)
  --mode copy|link             copy self-contained skills (default) or symlink repo
  --all                        install every skill (default if none given)
  -h, --help                   show this help

Examples:
  # 1) Install the three Chinese-name entry stacks (recommended starting set)
  scripts/install.sh tech-blog-en dev-post-zh deep-research-report

  # 2) Install only one self-contained skill
  scripts/install.sh dev-post-zh

  # 3) Everything, into Cursor's skill directory
  scripts/install.sh --host cursor --all

  # 4) Development mode: symlink the clone instead of copying
  scripts/install.sh --mode link --all

Host directories used by default (created if missing):
  claude : ~/.claude/skills
  cursor : ~/.cursor/skills
  codex  : ~/.codex/skills
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) HOST="$2"; shift 2 ;;
    --dest) DEST="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --all) ONLY=("${ALL_SKILLS[@]}"); shift ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; usage; exit 2 ;;
    *) ONLY+=("$1"); shift ;;
  esac
done

if [[ -z "$DEST" ]]; then
  case "$HOST" in
    claude) DEST="$HOME/.claude/skills" ;;
    cursor) DEST="$HOME/.cursor/skills" ;;
    codex)  DEST="$HOME/.codex/skills" ;;
    *) echo "Unknown --host '$HOST' (use claude|cursor|codex or --dest)" >&2; exit 2 ;;
  esac
fi

[[ ${#ONLY[@]} -gt 0 ]] || ONLY=("${ALL_SKILLS[@]}")
mkdir -p "$DEST"

if [[ "$MODE" == "link" ]]; then
  LINK_MODE=1
elif [[ "$MODE" != "copy" ]]; then
  echo "Unknown --mode '$MODE' (use copy|link)" >&2; exit 2
fi

SHARED_DIRS=(references templates checklists scripts)

for skill in "${ONLY[@]}"; do
  src="$REPO_ROOT/skills/$skill"
  [[ -d "$src" ]] || { echo "SKIP  $skill (not found in repo)"; continue; }
  dst="$DEST/$skill"

  if [[ $LINK_MODE -eq 1 ]]; then
    rm -rf "$dst"
    ln -s "$src" "$dst"
    echo "LINK  $skill -> $dst"
    continue
  fi

  rm -rf "$dst"
  mkdir -p "$dst"
  # skill's own files first
  cp -R "$src/." "$dst/"
  # bundle shared assets inside the skill folder
  for d in "${SHARED_DIRS[@]}"; do
    mkdir -p "$dst/$d"
    cp -R "$REPO_ROOT/$d/." "$dst/$d/"
  done
  # rewrite '../../<shared>' paths to bundled local paths inside markdown files
  while IFS= read -r f; do
    sed -i -E "s#\.\./\.\./(references|templates|checklists|scripts)/#\1/#g" "$f"
  done < <(find "$dst" -type f -name "*.md")
  echo "COPY  $skill (self-contained) -> $dst"
done

cat <<EOF

Done. ${#ONLY[@]} skill(s) installed into:
  $DEST

Notes:
  - Restart / reload your host so it rescans the skills directory.
  - Chinese-name entry points: 英文技术博客=tech-blog-en,
    中文社区文章=dev-post-zh, 行业深研报告=deep-research-report,
    协作研究写作=content-research-writer.
  - The kit produces LOCAL drafts only; uploading to any platform is always
    done manually by you. No login, cookie or auto-publish tooling is included.
EOF
