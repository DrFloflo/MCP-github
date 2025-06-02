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
   git clone <repository-url>
   cd MCP
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

## Environment Variables

- `GITHUB_TOKEN`: GitHub Personal Access Token with appropriate scopes
- `AZURE_CLIENT_ID`: Azure AD Application Client ID
- `AZURE_CLIENT_SECRET`: Azure AD Application Client Secret
- `AZURE_TENANT_ID`: Azure AD Tenant ID

## Security Considerations

- Never commit your `.env` file or expose your tokens/secrets
- Use appropriate token scopes (minimum required permissions)
- Consider using Azure Key Vault or similar for production secret management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Specify your license here]

## Support

For support, please open an issue in the GitHub repository.
