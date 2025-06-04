from core.logger import logger

from core.config import settings

from mcp.server.fastmcp import FastMCP
from tools.github.tools import get_github_file_content, get_workflow_runs, search_codebase, get_file_structure, get_commit_history, get_commit_diff
from tools.utils.tools import get_current_utc_timestamp, get_website_content
from tools.azure.tools import run_log_analytics_query
from tools.google.search import search_google
from tools.google.youtube import search_youtube, get_youtube_transcript
from tools.azure.vision import get_image_analysis
from tools.database.postgre import read_db
from tools.llm.azure import get_azure_openai_response
from tools.code.tools import execute_python_code, ALLOWED_MODULES

mcp = FastMCP("GitHubMCP")
mcp.settings.host = "0.0.0.0"
mcp.settings.port = 6277
mcp.settings.log_level = "DEBUG"

if __name__ == "__main__":
    #Go to docs/HowToAddTools.md to add tools
    #Example : mcp.add_tool(get_github_file_content, 
    # name="get_github_file_content", 
    # description="Get a file from GitHub", 
    # annotations={"owner": "GitHub user/org", "repo": "Repository name", "path": "File path to scope commits (\"\" for root)"})
    mcp.run(transport="sse")