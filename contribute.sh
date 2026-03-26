#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./contribute.sh [options] [count] [extra instructions...]

Run one or more Codex contribution passes for this repo. The invoked agent is told to:
- read CONTRIBUTING.md and AGENTS.md first
- promote the next unpublished draft when available, otherwise find and document a missing group, people, org, or op
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

selector_script=""
if [[ -f scripts/select_next_draft.py ]]; then
  selector_script="scripts/select_next_draft.py"
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

build_run_prompt() {
  local run_number="$1"
  local prompt=""
  local selection=""
  local draft_category=""
  local draft_path=""
  local public_path=""
  local draft_title=""

  if [[ -n "$selector_script" ]]; then
    selection="$(python3 "$selector_script" 2>/dev/null || true)"
  fi

  if [[ -n "$selection" ]]; then
    IFS=$'\t' read -r draft_category draft_path public_path draft_title <<< "$selection"
    prompt="This run is $run_number of $count. Promote exactly one unpublished backlog draft into sourced public wiki content. Use the current repository state to avoid duplicating previous work."
    prompt+=$'\n\n'
    prompt+=$'Selected draft:\n'
    prompt+="- Draft category: $draft_category"$'\n'
    prompt+="- Draft path: $draft_path"$'\n'
    prompt+="- Target public path: $public_path"$'\n'
    prompt+="- Draft title: $draft_title"$'\n'
    prompt+=$'\n'
    prompt+=$'Promotion rules:\n'
    prompt+=$'- Read the selected draft before making changes.\n'
    prompt+=$'- Publish a well-sourced page at the target public path or a clearly justified closely related path if the naming must change based on sources.\n'
    prompt+=$'- Update nav, landing page, blog index, and any companion group/people/op pages as needed.\n'
    prompt+=$'- Mark the corresponding checkbox in TODO.md as complete.\n'
    prompt+=$'- Delete the draft file after promotion, then run "python3 scripts/generate_drafts_from_todo.py" to refresh draft indexes and remove stale backlog scaffolds.\n'
    prompt+=$'- If the draft turns out to be too broad for one page, narrow it to one clearly sourceable page and update TODO.md so the backlog still reflects the remaining work.\n'
    prompt+=$'\n'
  else
    prompt="This run is $run_number of $count. Make exactly one primary distinct contribution in this run. A tightly coupled companion People or Groups page is allowed when clearly sourced and needed for taxonomy completeness. Use the current repository state to avoid duplicating previous work."
    prompt+=$'\n\n'
  fi

  prompt+="$base_prompt"
  printf '%s' "$prompt"
}

if [[ $dry_run -eq 1 ]]; then
  prompt="$(build_run_prompt 1)"
  printf 'Command:\n'
  printf '  %q' "${cmd[@]}"
  printf ' -\n\n'
  printf 'Count: %s\n\n' "$count"
  printf 'Prompt:\n%s\n' "$prompt"
  exit 0
fi

for ((i = 1; i <= count; i++)); do
  printf '==> Contribution %d/%d\n' "$i" "$count"
  prompt="$(build_run_prompt "$i")"
  printf '%s\n' "$prompt" | "${cmd[@]}" -
done
