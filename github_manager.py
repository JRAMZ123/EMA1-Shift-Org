import os
import requests
import base64
from dotenv import load_dotenv

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')
REPO = 'JRAMZ123/EMA1-Shift-Org'
HEADERS = {'Authorization': f'token {TOKEN}'}


def get_file_sha(filename):
    """Get the SHA of a file (needed for updates)"""
    url = f'https://api.github.com/repos/{REPO}/contents/{filename}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()['sha']
    return None


def save_html(filename, content, commit_message):
    """Save HTML file to GitHub"""
    sha = get_file_sha(filename)

    # Encode content to base64 (GitHub API requirement)
    encoded_content = base64.b64encode(content.encode()).decode()

    url = f'https://api.github.com/repos/{REPO}/contents/{filename}'

    payload = {
        'message': commit_message,
        'content': encoded_content,
        'sha': sha  # Required for updates
    }

    response = requests.put(url, json=payload, headers=HEADERS)

    if response.status_code in [200, 201]:
        print(f"✅ Successfully saved {filename}")
        return response.json()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        return None


def read_html(filename):
    """Read HTML file from GitHub"""
    url = f'https://api.github.com/repos/{REPO}/contents/{filename}'
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        content = base64.b64decode(response.json()['content']).decode()
        return content
    else:
        print(f"❌ Error reading file: {response.status_code}")
        return None