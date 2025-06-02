from mcp.server.fastmcp import FastMCP
from tools.github.tools import get_github_file_content, get_workflow_runs, search_codebase, get_file_structure, get_commit_history, get_commit_diff
from tools.utils.tools import get_current_utc_timestamp
from tools.azure.tools import run_log_analytics_query

mcp = FastMCP("GitHubMCP")
mcp.settings.host = "0.0.0.0"
mcp.settings.port = 6277
mcp.settings.log_level = "DEBUG"

# Route /health
@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    return JSONResponse({"status": "ok"})

# Route /config
@mcp.custom_route("/config", methods=["GET"])
async def config(request):
    return JSONResponse({
        "name": "default",  # ← peut être modifié, mais reste cohérent
        "entrypoint": "GitHubMCP"  # ← DOIT correspondre au nom que tu donnes à FastMCP
    })

if __name__ == "__main__":
    # Github tool
    mcp.add_tool(get_github_file_content, 
    name="get_github_file_folder", 
    description="Get a file or folder from GitHub, / for root",
    annotations={
        "owner": "GitHub user/org",
        "repo": "Repository name",
        "path": "File path to scope commits (\"\" for root)"
    })
    mcp.add_tool(get_workflow_runs, name="get_workflow_runs", description="Get the latest N workflow runs from a GitHub repo", annotations={
        "owner": "GitHub user/org",
        "repo": "Repository name",
        "last_req": "Number of most recent workflow runs to fetch (max 100)"
    })
    mcp.add_tool(search_codebase, name="search_codebase", description="Search for a keyword in a GitHub repository using the Code Search API", annotations={
        "owner": "GitHub user/org",
        "repo": "Repository name",
        "keyword": "Keyword to search for"
    })
    mcp.add_tool(get_file_structure, name="get_file_structure", description="Get the full file structure of a GitHub repo", annotations={
        "owner": "GitHub user/org",
        "repo": "Repository name"
    })
    mcp.add_tool(get_commit_history, name="get_commit_history", description="Get recent commit history (optionally for a specific file)", annotations={
        "owner": "GitHub user/org",
        "repo": "Repository name",
        "path": "File path to scope commits (\"\" for root)"
    })
    mcp.add_tool(get_commit_diff, name="get_commit_diff", description="Fetch file-level diffs for a specific commit", annotations={
        "owner": "GitHub user/org",
        "repo": "Repository name",
        "sha": "Commit SHA to inspect"
    })

    # Utils tool
    mcp.add_tool(get_current_utc_timestamp, name="get_current_utc_timestamp", description="Get the current UTC time in the format: YYYY-MM-DDTHH:MM:SS.ffffff0Z")
    
    # Azure tool
    mcp.add_tool(run_log_analytics_query, name="run_log_analytics_query", description="Run a Log Analytics query against a given workspace", annotations={
        "workspace": "Log Analytics workspace ID",
        "query": "KQL query string"
    })
    
    mcp.run(transport="sse")