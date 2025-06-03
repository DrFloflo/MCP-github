# MCP (Multi-Cloud Platform) Server

A FastAPI-based server that provides a unified interface for interacting with multiple cloud services, currently supporting GitHub and Azure Log Analytics.

## Features

### GitHub Integration
- **File/Folder Access**: Retrieve files or directory listings from GitHub repositories
- **Workflow Monitoring**: Fetch recent workflow runs and their statuses
- **Code Search**: Search for code across repositories
- **Repository Structure**: Get the complete file structure of a repository
- **Commit History**: View commit history with optional file filtering
- **Commit Diffs**: Inspect file-level changes for specific commits

### Azure Integration
- **Log Analytics Querying**: Run Kusto Query Language (KQL) queries against Azure Log Analytics workspaces
- **Secure Authentication**: OAuth2 client credentials flow for secure API access

### Utilities
- **Timestamp Generation**: Get current UTC timestamp with microsecond precision

## Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- GitHub Personal Access Token (with `repo` scope)
- Azure AD Application credentials (for Azure Log Analytics)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DrFloflo/MCP-github.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:
   ```env
   # GitHub Configuration
   GITHUB_TOKEN=your_github_token
   
   # Azure Configuration
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   AZURE_TENANT_ID=your_tenant_id
   ```

## Create your github token

1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Generate a new token with `repo` scope
3. Copy the token and paste it in the `.env` file

## Create your azure token

### Get your tenant ID

1. Go to [Azure AD](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
2. Click on the application you created (create one for the MCP server if you don't have one)
3. Copy the Directory (tenant) ID and paste it in the `.env` file

### Get your client ID and client secret

1. Go to [Azure AD](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
2. Click on the application you created
3. Copy the Application (client) ID is the client id
4. Click on "Manage"
5. Click on "Certificates and secrets"
6. Click on "New client secret"
7. Copy the value to Azure client secret and paste it in the `.env` file

### Get your Log Analytics workspace ID

1. Go to your Log Analytics workspace (or create one and bind the logs to it)
2. Click on the workspace you created
3. You can find your Workspace ID ask for the tool `run_log_analytics_query`

Warning: You have to configure the Log Analytics workspace to allow the Azure AD Application to access it.

## Add permissions to your Azure AD Application:

1. Go to [Azure AD](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
2. Click on the application you created
3. Click on "Manage"
4. Click on "API Permissions"
5. Click on "Add a permission"
6. Click on "Microsoft Graph"
7. Click on "Delegated permissions"
8. Click on "User.Read"
9. Click on "Add permissions"

## Usage

### Running the Server

```bash
python server.py
```

The server will start on `http://0.0.0.0:6277` by default.

### Docker

Build the Docker image:
```bash
docker build -t mcp-server .
```

Run the container:
```bash
docker run -p 6277:6277 --env-file .env mcp-server
```

## API Endpoints

The server exposes the following tools as API endpoints:

### GitHub Tools
- `get_github_file_folder`: Get file contents or directory listing
- `get_workflow_runs`: Get recent workflow runs
- `search_codebase`: Search for code in a repository
- `get_file_structure`: Get repository file structure
- `get_commit_history`: View commit history
- `get_commit_diff`: View file changes in a specific commit

### Azure Tools
- `run_log_analytics_query`: Execute KQL queries against Log Analytics

### Utility Tools
- `get_current_utc_timestamp`: Get current UTC timestamp
- `get_website_content`: Get the content of a website in Markdown format

### Database Tools
- `read_db`: Read a database from a PostgreSQL server

[!WARNING]
Be carefull, give only SELECT role to the user used to connect to the database.

### Google Tools
- `search_google`: Search Google for a query
- `search_youtube`: Search YouTube for a query
- `get_youtube_transcript`: Get the transcript of a YouTube video

### Azure Vision Tools
- `get_image_analysis`: Get the analysis of an image
