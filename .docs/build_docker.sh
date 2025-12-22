#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Assuming script is in .docs/, project root is one level up
PROJECT_ROOT="$SCRIPT_DIR/.."

# Move to project root so docker build context is correct
cd "$PROJECT_ROOT"

# Extract version from pyproject.toml using Python's tomllib (available in Python 3.11+)
VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")

if [ -z "$VERSION" ]; then
  echo "Error: Could not extract version from pyproject.toml"
  exit 1
fi

echo "========================================"
echo "Automated Docker Build for Version: $VERSION"
echo "========================================"

# Login (will use cached credentials if available, or prompt)
echo "[1/5] Logging in to Docker..."
docker login

# Build image
echo "[2/5] Building image..."
docker build -t dturkuler/humandesign_api:latest .

# Tag image
echo "[3/5] Tagging image with version $VERSION..."
docker tag dturkuler/humandesign_api:latest dturkuler/humandesign_api:$VERSION

# Show images
echo "[4/5] Verifying images..."
docker images dturkuler/humandesign_api

# Push images
echo "[5/5] Pushing images..."
echo "Pushing latest..."
docker push dturkuler/humandesign_api:latest
echo "Pushing $VERSION..."
docker push dturkuler/humandesign_api:$VERSION

echo "========================================"
echo "SUCCESS: Version $VERSION pushed."
echo "========================================"

# --- Update Docker Hub Description ---
echo "[Optional] Updating Docker Hub Description..."

# Load .env variables if present (for DOCKER_HUB credentials)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Run the update script
python3 .docs/update_hub_desc.py

