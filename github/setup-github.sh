#!/usr/bin/env bash
# Crée milestones, labels, tickets et project board sur un dépôt GitHub NEUF,
# pousse branches et tags, puis ferme les milestones des phases terminées.
# Prérequis : gh installé, `gh auth login` puis `gh auth refresh -s project`,
# remote `origin` configuré.
# Usage : bash github/setup-github.sh <owner>/<repo>
set -euo pipefail

REPO="${1:?usage: setup-github.sh <owner>/<repo>}"
OWNER="${REPO%%/*}"
DIR="$(cd "$(dirname "$0")" && pwd)"

for m in "Lancement" "Élaboration" "Construction" "Transition"; do
  gh api "repos/$REPO/milestones" -f title="$m" >/dev/null
done

gh label create cas-utilisation --repo "$REPO" --color 1D76DB --force
gh label create risque-technique --repo "$REPO" --color D93F0B --force
gh label create phase --repo "$REPO" --color 5319E7 --force

PROJECT=$(gh project create --owner "$OWNER" --title "Location vélos — TP1" --format json --jq .number)

# Ordre important : UC1..UC6 = #1..#6, puis #7 Lancement, #8 Élaboration, #9 Transition.
for f in "$DIR"/issues/*.md; do
  title=$(sed -n '1s/^# //p' "$f")
  milestone=$(sed -n 's/^Milestone: //p' "$f")
  labels=$(sed -n 's/^Labels: //p' "$f" | tr -d ' ')
  body=$(tail -n +4 "$f")
  url=$(gh issue create --repo "$REPO" --title "$title" --body "$body" \
        --milestone "$milestone" --label "$labels")
  gh project item-add "$PROJECT" --owner "$OWNER" --url "$url" >/dev/null
  echo "créé : $url"
done

git push --all origin
git push --tags origin

gh issue close 7 --repo "$REPO" --comment "Jalon LCO atteint (tag v0.0-lancement)."
gh issue close 8 --repo "$REPO" --comment "Jalon LCA atteint (tag v0.1-elaboration)." || true
for m in "Lancement" "Élaboration"; do
  num=$(gh api "repos/$REPO/milestones?state=all" --jq ".[] | select(.title==\"$m\") | .number")
  gh api -X PATCH "repos/$REPO/milestones/$num" -f state=closed >/dev/null
  echo "milestone fermé : $m"
done
