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
    # Github tool
    if (settings.GITHUB_TOKEN != ""):
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
    else:
        logger.warning("GITHUB_TOKEN not found in .env, skipping GitHub tools")

    # Utils tool
    mcp.add_tool(get_current_utc_timestamp, name="get_current_utc_timestamp", description="Get the current UTC time in the format: YYYY-MM-DDTHH:MM:SS.ffffff0Z")
    mcp.add_tool(get_website_content, name="get_website_content", description="Get the content of a website in Markdown format", annotations={
        "url": "The URL of the website to get the content for"
    })
    
    # Azure tool
    if (settings.AZURE_CLIENT_ID != "" and settings.AZURE_CLIENT_SECRET != "" and settings.AZURE_TENANT_ID != ""):
        mcp.add_tool(run_log_analytics_query, name="run_log_analytics_query", description="Run a Log Analytics query against a given workspace using API", annotations={
            "workspace": "Log Analytics workspace ID",
            "query": "KQL query string (data queries only)"
        })
    else:
        logger.warning("AZURE_CLIENT_ID, AZURE_CLIENT_SECRET or AZURE_TENANT_ID not found in .env, skipping Azure tools")
    
    # Google tool
    mcp.add_tool(search_google, name="search_google", description="Search Google for a query", annotations={
        "query": "The query to search for",
        "num_results": "The number of results to return"
    })
    mcp.add_tool(search_youtube, name="search_youtube", description="Search YouTube for a query", annotations={
        "query": "The query to search for"
    })
    mcp.add_tool(get_youtube_transcript, name="get_youtube_transcript", description="Get the transcript of a YouTube video", annotations={
        "video_id": "The ID of the video to get the transcript for"
    })

    # Azure vision tool
    if (settings.VISION_ENDPOINT != "" and settings.VISION_KEY != ""):
        mcp.add_tool(get_image_analysis, name="get_image_analysis", description="Get the analysis of an image", annotations={
            "image_url": "The URL of the image to analyze"
        })
    else:
        logger.warning("VISION_ENDPOINT or VISION_KEY not found in .env, skipping Azure vision tools")

    #Database tool
    if (settings.POSTGRES_HOST != "" and settings.POSTGRES_DB != "" and settings.POSTGRES_USER != "" and settings.POSTGRES_PASSWORD != ""):
        mcp.add_tool(read_db, name="read_db", description="Read a database from a PostgreSQL server", annotations={
            "query": "The query to execute"
        })
    else:
        logger.warning("POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER or POSTGRES_PASSWORD not found in .env, skipping database tools")

    # LLM tool
    if (settings.AZURE_OPENAI_ENDPOINT != "" and settings.AZURE_OPENAI_KEY != ""):
        mcp.add_tool(get_azure_openai_response, name="get_azure_openai_response", description="Get a response from Azure OpenAI", annotations={
            "message": "The message to send to the model"
        })
    else:
        logger.warning("AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_KEY not found in .env, skipping LLM tools")

    # Code execution tool
    mcp.add_tool(execute_python_code, 
    name="execute_python_code", 
    description="Execute Python code in a restricted environment, import available: " + ", ".join(ALLOWED_MODULES), 
    annotations={
        "code": "Python code to execute",
        "max_output_length": "Maximum length of the output (default: 1000)"
    })

    mcp.run(transport="sse")