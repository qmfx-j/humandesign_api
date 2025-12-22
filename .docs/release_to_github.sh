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

# 3. Extract Changelog for this version
# We use python to robustly extract the text between ## [VERSION] and the next ##
CHANGELOG_TEXT=$(VERSION="$VERSION" python3 -c "
import re
import os
version = os.environ.get('VERSION')
try:
    with open('CHANGELOG.md', 'r') as f:
        content = f.read() 
    # escape dots for regex
    ver_safe = re.escape(version)
    pattern = rf'(## \[{ver_safe}\].*?)(?=\n## \[|$)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print(match.group(1).strip())
    else:
        print(f'Version {version} Release')
except Exception as e:
    print(f'Version {version} Release')
")

echo "----------------------------------------"
echo "Release Notes:"
echo "$CHANGELOG_TEXT"
echo "----------------------------------------"

# 4. Git Operations
echo "Step 1: Staging changes..."
git add .

echo "Step 2: Committing..."
# Only commit if there are changes
if git diff-index --quiet HEAD --; then
    echo "No changes to commit."
else
    # We use a simple subject for the commit, but could include body if needed
    git commit -m "Release version $VERSION" -m "$CHANGELOG_TEXT"
fi

echo "Step 3: Tagging..."
# Check if tag exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo "Tag v$VERSION already exists. Skipping tag creation."
else
    # Create annotated tag with the changelog as the message
    git tag -a "v$VERSION" -m "$CHANGELOG_TEXT"
    echo "Created tag v$VERSION"
fi

echo "Step 4: Pushing to GitHub..."
git push origin main
git push origin "v$VERSION"

echo "========================================"
echo "GitHub Release Complete!"
echo "Check it at: https://github.com/dturkuler/humandesign_api/releases/tag/v$VERSION"
echo "========================================"
