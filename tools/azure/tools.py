import requests
from core.config import settings
from core.logger import logger

def fetch_azure_ad_token(scope: str) -> dict:
    """
    Obtain an OAuth2 access token from Azure AD using client credentials flow.

    Args:
        scope: Space-separated list of scopes, e.g. "https://graph.microsoft.com/.default"

    Returns:
        On success: {"access_token": "...", "expires_in": 3599, ...}
        On failure: {"error": "...", "error_description": "..."}
    """
    # 1. Read credentials
    client_id = settings.AZURE_CLIENT_ID
    client_secret = settings.AZURE_CLIENT_SECRET
    tenant_id = settings.AZURE_TENANT_ID

    if not client_id or not client_secret or not tenant_id:
        logger.error("AZURE_CLIENT_ID, AZURE_CLIENT_SECRET or AZURE_TENANT_ID not found in .env, skipping Azure tools")
        return None

    # 2. Token endpoint URL
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

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
        logger.error("Unable to connect or parse response")
        return None

    if resp.status_code != 200:
        # Azure returns error and description in JSON on 4xx/5xx
        logger.error(data.get("error_description", "Unknown error"))
        return None

    # Success: return the full token response (access_token, expires_in, etc.)
    return data

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
    token = fetch_azure_ad_token("https://api.loganalytics.io/.default")
    if token is None:
        logger.error("Failed to fetch Azure AD token")
        return None
    
    token = token.get("access_token")
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
        logger.error("Unable to connect or parse response")
        return None

    if resp.status_code != 200:
        logger.error(data.get("error_description", "Unknown error"))
        return None

    return data