# AI Workload Analyzer

A powerful AI-driven workload analysis tool that combines Databricks agents with a modern Chainlit web interface. This application helps analyze SQL queries, workloads, and provides intelligent insights using Databricks tools and Claude 3.7 Sonnet.

## Features

- 🤖 **Databricks ChatAgent Integration**: Leverages Databricks agents for intelligent workload analysis
- 💬 **Modern Chat Interface**: Beautiful Chainlit web interface for seamless user interaction
- 🔧 **UC Function Toolkit**: Integrates with Unity Catalog functions for enhanced capabilities
- 📊 **SQL Query Analysis**: Analyzes and optimizes SQL queries with intelligent recommendations
- 🔄 **Streaming Responses**: Real-time streaming responses for better user experience
- 🛡️ **Error Handling**: Comprehensive error handling and logging

## Prerequisites

- Python 3.8 or higher
- Databricks workspace with appropriate permissions
- Unity Catalog functions configured
- Model serving endpoint for Claude 3.7 Sonnet

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd ai_workload_analyzer
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit the `.env` file with your Databricks configuration:
   ```env
   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
   DATABRICKS_TOKEN=your_databricks_token_here
   DATABRICKS_CLUSTER_ID=your_cluster_id_here
   DATABRICKS_MODEL_ENDPOINT=databricks-claude-3-7-sonnet
   UC_FUNCTION_NAMES=function1,function2,function3
   ```

4. **Update UC Function Names**:
   Edit `main.py` and replace `["***"]` with your actual Unity Catalog function names:
   ```python
   tools = UCFunctionToolkit(["your_function_1", "your_function_2"]).tools
   ```

## Usage

### Running the Application

1. **Start the Chainlit server**:
   ```bash
   uv run chainlit run main.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to `http://localhost:8000`

3. **Start analyzing**:
   - Ask questions about SQL queries
   - Request workload analysis
   - Get optimization recommendations
   - Explore data insights

### Example Queries

- "Analyze this SQL query for performance optimization"
- "What are the best practices for this workload?"
- "Help me understand the execution plan"
- "Suggest improvements for this data pipeline"

## Project Structure

```
ai_workload_analyzer/
├── main.py              # Main application with Chainlit integration
├── pyproject.toml       # Project configuration and dependencies
├── README.md           # This file
├── env_example.txt     # Environment variables example
└── .env               # Your environment variables (create this)
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABRICKS_HOST` | Your Databricks workspace URL | Yes |
| `DATABRICKS_TOKEN` | Databricks personal access token | Yes |
| `DATABRICKS_CLUSTER_ID` | Cluster ID for computations | Yes |
| `DATABRICKS_MODEL_ENDPOINT` | Model serving endpoint name | Yes |
| `UC_FUNCTION_NAMES` | Comma-separated UC function names | Yes |
| `CHAINLIT_HOST` | Chainlit server host | No (default: 0.0.0.0) |
| `CHAINLIT_PORT` | Chainlit server port | No (default: 8000) |
| `LOG_LEVEL` | Logging level | No (default: INFO) |

### Databricks Setup

1. **Create a personal access token** in your Databricks workspace
2. **Set up Unity Catalog functions** that your agent will use
3. **Configure model serving endpoint** for Claude 3.7 Sonnet
4. **Ensure proper permissions** for accessing UC functions and model endpoints

## Development

### Installing Development Dependencies

```bash
uv sync --dev
```

### Code Formatting

```bash
uv run black .
```

### Type Checking

```bash
uv run mypy .
```

### Running Tests

```bash
uv run pytest
```

## Architecture

The application consists of several key components:

1. **Databricks ChatAgent**: Core AI agent that processes queries and executes tools
2. **UCFunctionToolkit**: Provides access to Unity Catalog functions
3. **Chainlit Interface**: Modern web interface for user interaction
4. **Async Processing**: Handles long-running operations without blocking the UI

## Troubleshooting

### Common Issues

1. **Agent Initialization Failed**:
   - Check your Databricks credentials
   - Verify model endpoint is accessible
   - Ensure UC functions exist and are accessible

2. **Connection Timeout**:
   - Check network connectivity to Databricks
   - Verify firewall settings
   - Increase timeout values if needed

3. **UC Function Errors**:
   - Verify function names in configuration
   - Check function permissions
   - Ensure functions are properly registered

### Logging

The application uses structured logging. Check the console output for detailed error messages and debugging information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review Databricks documentation
- Create an issue in the project repository 