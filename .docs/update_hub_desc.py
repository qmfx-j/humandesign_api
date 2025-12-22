import os
import json
import urllib.request
import urllib.error
import re
from pathlib import Path

# Configuration
USERNAME = os.getenv("DOCKER_HUB_USERNAME") or os.getenv("DOCKER_USERNAME")
PASSWORD = os.getenv("DOCKER_HUB_PASSWORD") or os.getenv("DOCKER_PASSWORD")
REPO_NAME = "humandesign_api" # Adjust if your repo name differs on Hub
NAMESPACE = USERNAME # Defaults to username, usually correct
API_BASE = "https://hub.docker.com/v2"

def get_latest_changelog(changelog_path):
    """
    Extracts the first version section from the Changelog.
    Assumes standard 'Keep a Changelog' format.
    """
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex to find the first version header (e.g., ## [1.2.4]...) 
        # and capture everything until the next version header
        pattern = r"(## \[\d+\.\d+\.\d+\].*?)(?=\n## \[|$)"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return None
    except Exception as e:
        print(f"Warning: Could not extract changelog: {e}")
        return None

def update_docker_hub_description():
    if not USERNAME or not PASSWORD:
        print("Skipping Docker Hub description update: DOCKER_HUB_USERNAME or DOCKER_HUB_PASSWORD not set.")
        return

    print(f"Updating Docker Hub description for {NAMESPACE}/{REPO_NAME}...")

    # 1. Login to get JWT
    login_url = f"{API_BASE}/users/login"
    login_data = json.dumps({"username": USERNAME, "password": PASSWORD}).encode('utf-8')
    
    try:
        req = urllib.request.Request(login_url, data=login_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            token = json.loads(response.read().decode('utf-8'))['token']
    except urllib.error.HTTPError as e:
        print(f"Error logging in to Docker Hub: {e}")
        return

    # 2. Prepare Description
    # Read README
    readme_path = Path(__file__).parent.parent / "README.md"
    changelog_path = Path(__file__).parent.parent / "CHANGELOG.md"
    
    try:
        description_text = readme_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading README.md: {e}")
        return

    # Get Changelog snippet
    latest_changes = get_latest_changelog(changelog_path)
    
    # Combine (Append Changelog to README for the Hub Overview)
    if latest_changes:
        full_description = f"{description_text}\n\n---\n\n# Latest Changes\n\n{latest_changes}"
    else:
        full_description = description_text

    # 3. Patch Repository
    repo_url = f"{API_BASE}/repositories/{NAMESPACE}/{REPO_NAME}/"
    patch_data = json.dumps({"full_description": full_description}).encode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'JWT {token}'
    }
    
    try:
        req = urllib.request.Request(repo_url, data=patch_data, headers=headers, method='PATCH')
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("Successfully updated Docker Hub repository description.")
            else:
                print(f"Failed to update description. Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"Error updating repository description: {e}")
        print(e.read().decode('utf-8'))

if __name__ == "__main__":
    update_docker_hub_description()
