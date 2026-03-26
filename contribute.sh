#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./contribute.sh [options] [count] [extra instructions...]

Run one or more Codex contribution passes for this repo. The invoked agent is told to:
- read CONTRIBUTING.md and AGENTS.md first
- find and document a missing group, people, org, or op
- verify the site build
- commit and push the result

Options:
  -c, --count N      Run Codex N times sequentially
  -n, --dry-run      Print the generated prompt and command without invoking Codex
  -m, --model MODEL  Pass a specific model to codex exec
      --no-search    Disable Codex web search
  -h, --help         Show this help

Examples:
  ./contribute.sh
  ./contribute.sh 10
  ./contribute.sh --count 3
  ./contribute.sh "Focus on supply-chain compromises from the last 30 days"
  ./contribute.sh --dry-run "Prefer documenting a missing op or companion people page"
EOF
}

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$repo_root"

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found in PATH" >&2
  exit 1
fi

if [[ ! -f CONTRIBUTING.md ]]; then
  echo "CONTRIBUTING.md not found in $repo_root" >&2
  exit 1
fi

if [[ ! -f AGENTS.md ]]; then
  echo "AGENTS.md not found in $repo_root" >&2
  exit 1
fi

dry_run=0
search=1
model=""
count=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--count)
      if [[ $# -lt 2 ]]; then
        echo "--count requires a value" >&2
        exit 1
      fi
      count="$2"
      shift 2
      ;;
    -n|--dry-run)
      dry_run=1
      shift
      ;;
    -m|--model)
      if [[ $# -lt 2 ]]; then
        echo "--model requires a value" >&2
        exit 1
      fi
      model="$2"
      shift 2
      ;;
    --no-search)
      search=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -gt 0 && "$1" =~ ^[0-9]+$ ]]; then
  count="$1"
  shift
fi

if [[ ! "$count" =~ ^[1-9][0-9]*$ ]]; then
  echo "count must be a positive integer" >&2
  exit 1
fi

extra_instructions="${*:-}"

read -r -d '' base_prompt <<EOF || true
Read CONTRIBUTING.md and AGENTS.md before making any changes.

Perform one focused contribution pass for this repository:
- Identify exactly one primary high-confidence missing group, people, org, or op that fits the documented taxonomy and contribution rules.
- Use public, durable, source-linked reporting. Prefer primary sources and investigative writeups.
- Follow the taxonomy quirks in CONTRIBUTING.md exactly, including the current handling of orgs and the stable docs/actors/ path for group pages.
- Prefer names used by operators, maintainers, projects, or other firsthand sources over later vendor-generated brands when source support is clear. If alternate names matter, attribute them to the report or vendor that used them.
- When the primary contribution is an op or group, explicitly investigate whether a clearly sourceable companion People or Groups page should also be added in the same run.
- For People pages, prefer a GitHub username, maintainer persona, or other public handle when that is the strongest supported identifier.
- Update any required supporting files such as mkdocs.yml, docs/index.md, docs/blog/index.md, notes, or related pages when needed.
- Verify the result with \`uvx --from mkdocs-material mkdocs build --strict\`.
- Commit the finished work with a specific git commit message and push it to origin.

If the first candidate is too weak, ambiguous, or redundant, pick a different one instead of stopping.
Do not leave the repo half-updated.
Summarize what you changed at the end.
EOF

if [[ -n "$extra_instructions" ]]; then
  base_prompt+=$'\n\nAdditional user instructions:\n'
  base_prompt+="$extra_instructions"
fi

cmd=(codex)

if [[ $search -eq 1 ]]; then
  cmd+=(--search)
fi

if [[ -n "$model" ]]; then
  cmd+=(-m "$model")
fi

cmd+=(exec --dangerously-bypass-approvals-and-sandbox -C "$repo_root")

if [[ $dry_run -eq 1 ]]; then
  prompt="This run is 1 of $count. Make exactly one primary distinct contribution in this run. A tightly coupled companion People or Groups page is allowed when clearly sourced and needed for taxonomy completeness. Use the current repository state to avoid duplicating previous work."
  prompt+=$'\n\n'
  prompt+="$base_prompt"
  printf 'Command:\n'
  printf '  %q' "${cmd[@]}"
  printf ' -\n\n'
  printf 'Count: %s\n\n' "$count"
  printf 'Prompt:\n%s\n' "$prompt"
  exit 0
fi

for ((i = 1; i <= count; i++)); do
  printf '==> Contribution %d/%d\n' "$i" "$count"
  prompt="This run is $i of $count. Make exactly one primary distinct contribution in this run. A tightly coupled companion People or Groups page is allowed when clearly sourced and needed for taxonomy completeness. Use the current repository state to avoid duplicating previous work."
  prompt+=$'\n\n'
  prompt+="$base_prompt"
  printf '%s\n' "$prompt" | "${cmd[@]}" -
done
