import os
import requests
from dotenv import load_dotenv

# Load .env to get GITHUB_TOKEN
load_dotenv()

def fetch_azure_ad_token(scope: str) -> dict:
    """
    Obtain an OAuth2 access token from Azure AD using client credentials flow.

    Args:
        scope: Space-separated list of scopes, e.g. "https://graph.microsoft.com/.default"

    Returns:
        On success: {"access_token": "...", "expires_in": 3599, ...}
        On failure: {"error": "...", "error_description": "..."}
    """
    # 1. Read credentials from environment
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    tenant_id = os.getenv("AZURE_TENANT_ID")
    if not client_id or not client_secret or not tenant_id:
        return {"error": "missing_credentials", "error_description": "CLIENT_ID or CLIENT_SECRET or TENANT_ID not set in environment"}

    # 2. Token endpoint URL
    token_url = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    # 3. Build payload
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        resp = requests.post(token_url, data=payload, headers=headers)
        data = resp.json()
    except Exception:
        return {"error": "request_failed", "error_description": "Unable to connect or parse response"}

    if resp.status_code != 200:
        # Azure returns error and description in JSON on 4xx/5xx
        return {
            "error": data.get("error", "unknown_error"),
            "error_description": data.get("error_description", "No description")
        }

    # Success: return the full token response (access_token, expires_in, etc.)
    return data

import requests

def run_log_analytics_query(workspace: str, query: str) -> dict:
    """
    Execute a Log Analytics query against a given workspace.

    Args:
        workspace: Log Analytics workspace ID
        query:     KQL query string

    Returns:
        On success: parsed JSON response from Log Analytics
        On failure: {"error": "...", "error_description": "..."}
    """
    token = fetch_azure_ad_token("https://graph.microsoft.com/.default").get("access_token")
    url = f"https://api.loganalytics.io/v1/workspaces/{workspace}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"query": query}

    try:
        resp = requests.post(url, headers=headers, json=payload)
        data = resp.json()
    except Exception:
        return {"error": "request_failed", "error_description": "Unable to connect or parse response"}

    if resp.status_code != 200:
        return {
            "error": data.get("error", "api_error"),
            "error_description": data.get("error_description", data.get("message", "Unknown error"))
        }

    return data