import os
import base64
import requests
from dotenv import load_dotenv

# Load .env to get GITHUB_TOKEN
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not found in .env")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_github_file_content(owner: str, repo: str, path: str = "") -> dict:
    """
    Fetch a file’s content or folder from a GitHub repository.

    Args:
        owner:   GitHub username or organization
        repo:    Repository name
        path:    Path to the file within the repo (e.g., "src/app.py" or "/" for root)

    Returns:
        A dict with:
          - "path": the file path
          - "content": the decoded UTF-8 content of the file
          - "message": if GitHub returned a message (e.g., on errors)
    """
    if path == "/":
        path = ""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=HEADERS)
    try:
        data = resp.json()
    except ValueError:
        return {"type": "error", "message": "Invalid JSON response from GitHub"}

    if resp.status_code != 200:
        msg = data.get("message", "Failed to fetch content") if isinstance(data, dict) else "GitHub API error"
        return {"type": "error", "message": msg}

    if isinstance(data, list):
        return {
            "type": "dir",
            "entries": [
                {
                    "name": entry.get("name"),
                    "path": entry.get("path"),
                    "type": entry.get("type")
                }
                for entry in data
            ]
        }

    # Handle single file
    raw_b64 = data.get("content")
    if raw_b64 is None:
        return {"type": "file", "path": data.get("path"), "content": None}

    decoded = base64.b64decode(raw_b64).decode("utf-8", errors="replace")
    return {
        "type": "file",
        "path": data.get("path"),
        "content": decoded,
    }

def get_workflow_runs(owner: str, repo: str, last_req: int = 5) -> dict:
    """
    Fetch the latest N workflow runs from a GitHub repo.

    Args:
        owner:     GitHub username or org
        repo:      Repository name
        last_req:  Number of most recent workflow runs to fetch (max 100)

    Returns:
        dict with:
          - "total": number of runs returned
          - "runs": list of dicts with run info
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    params = {"per_page": min(last_req, 100)}

    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        data = resp.json()
    except Exception:
        return {"error": "Failed to fetch or parse response from GitHub"}

    if resp.status_code != 200:
        return {"error": data.get("message", "GitHub API error")}

    runs = data.get("workflow_runs", [])[:last_req]
    result = []
    for run in runs:
        result.append({
            "id": run.get("id"),
            "name": run.get("name"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "created_at": run.get("created_at"),
            "html_url": run.get("html_url"),
        })

    return {
        "total": len(result),
        "runs": result
    }

def search_codebase(owner: str, repo: str, keyword: str, limit: int = 10) -> dict:
    """
    Search for a keyword in a GitHub repository using the Code Search API.

    Args:
        owner:   GitHub username or organization
        repo:    Repository name
        keyword: String to search for
        limit:   Max number of results to return (GitHub allows up to 1000)

    Returns:
        dict with:
          - "total": total matches from GitHub
          - "results": list of matches with file path and URL
    """
    url = "https://api.github.com/search/code"
    params = {
        "q": f"{keyword} repo:{owner}/{repo}",
        "per_page": min(limit, 100)
    }

    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        data = resp.json()
    except Exception:
        return {"error": "Failed to query GitHub Code Search API"}

    if resp.status_code != 200:
        return {"error": data.get("message", "GitHub API error")}

    items = data.get("items", [])
    results = []
    for item in items:
        results.append({
            "path": item.get("path"),
            "html_url": item.get("html_url"),
        })

    return {
        "total": data.get("total_count", 0),
        "results": results
    }

def get_file_structure(owner: str, repo: str, branch: str = "main") -> dict:
    """
    Get full file structure of a GitHub repo using the Git Trees API.

    Args:
        owner:  GitHub user/org
        repo:   Repository name
        branch: Branch to inspect (default: "main")

    Returns:
        dict with:
          - "tree": list of {path, type}
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    try:
        resp = requests.get(url, headers=HEADERS)
        data = resp.json()
    except Exception:
        return {"error": "Failed to fetch or parse Git tree"}

    if resp.status_code != 200:
        return {"error": data.get("message", "GitHub API error")}

    tree = data.get("tree", [])
    return {
        "tree": [
            {"path": item["path"], "type": item["type"]}
            for item in tree if item["type"] in ("blob", "tree")
        ]
    }

def get_commit_history(owner: str, repo: str, path: str = None, limit: int = 10) -> dict:
    """
    Fetch recent commit history (optionally for a specific file).

    Args:
        owner: GitHub user/org
        repo:  Repository name
        path:  File path to scope commits ("" for root)
        limit: Max number of commits to return

    Returns:
        dict with:
          - "commits": list of {sha, author, date, message}
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"per_page": limit}
    if path:
        params["path"] = path

    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        data = resp.json()
    except Exception:
        return {"error": "Failed to fetch or parse commit history"}

    if resp.status_code != 200:
        return {"error": data.get("message", "GitHub API error")}
    return {
        "commits": [
            {
                "sha": c.get("sha"),
                "author": c.get("commit", {}).get("author", {}).get("name"),
                "date": c.get("commit", {}).get("author", {}).get("date"),
                "message": c.get("commit", {}).get("message")
            }
            for c in data
        ]
    }

def get_commit_diff(owner: str, repo: str, sha: str) -> dict:
    """
    Fetch file-level diffs for a specific commit.

    Args:
        owner: GitHub user/org
        repo:  Repository name
        sha:   Commit SHA to inspect

    Returns:
        dict with:
          - "files": list of {filename, status, patch}
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"

    try:
        resp = requests.get(url, headers=HEADERS)
        data = resp.json()
    except Exception:
        return {"error": "Failed to fetch or parse commit details"}

    if resp.status_code != 200:
        return {"error": data.get("message", "GitHub API error")}

    files = data.get("files", [])
    results = []
    for f in files:
        results.append({
            "filename": f.get("filename"),
            "status": f.get("status"),  # added, modified, removed
            "patch": f.get("patch")     # unified diff (can be None)
        })

    return {"files": results}
