#!/bin/bash

# Ensure we’re in a Git repo
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
  echo "❌ Not inside a Git repository."
  exit 1
fi

# Find all folders that previously had .git dirs (now removed)
echo "🔍 Scanning for nested directories with removed .git folders..."

# We'll consider a folder if it has files but is untracked
UNTRACKED_DIRS=$(find . -type d -not -path "./.git/*" | while read -r dir; do
  # Skip .git and node_modules or similar big folders
  [[ "$dir" =~ \.git|node_modules|venv|__pycache__ ]] && continue

  # Check if folder is untracked
  if [[ -n $(git status --porcelain "$dir" | grep '^??') ]]; then
    echo "$dir"
  fi
done)

# If nothing found
if [ -z "$UNTRACKED_DIRS" ]; then
  echo "✅ No untracked directories found."
  exit 0
fi

echo "📁 Found untracked directories:"
echo "$UNTRACKED_DIRS"
echo

# Confirm with user
read -rp "👉 Add and commit all of these? [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "❌ Aborted."
  exit 0
fi

# Add all untracked directories
echo "➕ Adding..."
echo "$UNTRACKED_DIRS" | xargs git add

# Commit
echo "📝 Committing..."
git commit -m "Fix: add previously nested directories after removing inner .git folders"

# Push
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "🚀 Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo "✅ All done."
