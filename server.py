from mcp.server.fastmcp import FastMCP
from github.tools import get_github_file_content, get_workflow_runs, search_codebase, get_file_structure, get_commit_history, get_commit_diff

mcp = FastMCP("GitHubMCP")
mcp.settings.host = "0.0.0.0"
mcp.settings.port = 6277
mcp.settings.log_level = "DEBUG"

if __name__ == "__main__":
    # Run over stdio so any MCP-compatible client (e.g., Claude Desktop) can connect.
    mcp.add_tool(get_github_file_content, name="get_github_file_folder", description="Get a file or folder from GitHub, / for root")
    mcp.add_tool(get_workflow_runs, name="get_workflow_runs", description="Get the latest N workflow runs from a GitHub repo")
    mcp.add_tool(search_codebase, name="search_codebase", description="Search for a keyword in a GitHub repository using the Code Search API")
    mcp.add_tool(get_file_structure, name="get_file_structure", description="Get the full file structure of a GitHub repo")
    mcp.add_tool(get_commit_history, name="get_commit_history", description="Get recent commit history (optionally for a specific file)")
    mcp.add_tool(get_commit_diff, name="get_commit_diff", description="Fetch file-level diffs for a specific commit")
    mcp.run(transport="sse")