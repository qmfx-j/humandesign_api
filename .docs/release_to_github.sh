#!/bin/bash
set -e

# 1. Get Project Root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
cd "$PROJECT_ROOT"

# 2. Extract Version
VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")

if [ -z "$VERSION" ]; then
  echo "Error: Could not extract version from pyproject.toml"
  exit 1
fi

echo "========================================"
echo "releasing to GitHub: v$VERSION"
echo "========================================"

# 3. Git Operations
echo "Step 1: Staging changes..."
git add .

echo "Step 2: Committing..."
# Only commit if there are changes
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
else
    git commit -m "Release version $VERSION"
fi

echo "Step 3: Tagging..."
# Check if tag exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo "Tag v$VERSION already exists. Skipping tag creation."
else
    git tag -a "v$VERSION" -m "Version $VERSION Release"
    echo "Created tag v$VERSION"
fi

echo "Step 4: Pushing to GitHub..."
git push origin main
git push origin "v$VERSION"

echo "========================================"
echo "GitHub Release Complete!"
echo "Check it at: https://github.com/dturkuler/humandesign_api/releases/tag/v$VERSION"
echo "========================================"
