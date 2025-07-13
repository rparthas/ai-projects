# AI Projects Collection

A curated collection of AI-powered applications built for learning and practical use. Each project demonstrates different aspects of AI integration, from document processing to workload analysis.

## 🚀 Projects Overview

### 1. [AI Workload Analyzer](./ai_workload_analyzer/)
**A Databricks-integrated AI workload analysis tool**

- 🤖 **Databricks ChatAgent Integration**: Leverages Databricks agents for intelligent workload analysis
- 💬 **Modern Chat Interface**: Beautiful Chainlit web interface for seamless interaction
- 📊 **SQL Query Analysis**: Analyzes and optimizes SQL queries with intelligent recommendations
- 🔧 **UC Function Toolkit**: Integrates with Unity Catalog functions for enhanced capabilities
- 🔄 **Streaming Responses**: Real-time streaming responses for better user experience

**Tech Stack**: `Python` • `Databricks` • `Chainlit` • `Claude 3.7 Sonnet` • `Unity Catalog`

### 2. [Local GPT with PDF Q&A](./local_gpt/)
**A local PDF document analysis and Q&A system**

- 📄 **PDF Document Q&A**: Upload multiple PDFs and ask questions about their content
- 🔍 **Semantic Search**: ChromaDB vector database for intelligent document retrieval
- 🧠 **Context-Aware Responses**: Understands document context for accurate answers
- 💾 **Local Processing**: Runs entirely on your machine using Ollama
- 🔄 **Smart Chunking**: Intelligent text chunking with sentence-transformers

**Tech Stack**: `Python` • `Ollama` • `ChromaDB` • `Chainlit` • `sentence-transformers` • `PyPDF2`

### 3. [YouTube to Blog Converter](./yt_to_blog/)
**Transform YouTube videos into structured blog posts**

- 🎥 **YouTube Transcript Extraction**: Automatic transcript extraction from YouTube videos
- 📝 **AI-Powered Content Transformation**: Converts raw transcripts into professional blog posts
- 🔗 **Multiple URL Format Support**: Works with various YouTube URL formats
- 💾 **Smart File Naming**: Automatic filename generation based on content
- 🛠️ **Environment Configuration**: Easy model configuration via `.env` file

**Tech Stack**: `Python` • `Ollama` • `YouTube Transcript API` • `Markdown`

## 🛠️ Prerequisites

### Common Requirements
- **Python 3.11+**
- **uv package manager** (recommended) - Install from [uv.astral.sh](https://uv.astral.sh/)
- **Ollama** (for local_gpt and yt_to_blog) - Download from [ollama.com](https://ollama.com)

### Project-Specific Requirements
- **AI Workload Analyzer**: Databricks workspace with appropriate permissions
- **Local GPT**: Ollama with a compatible model (e.g., `deepseek-r1:8b`)
- **YouTube to Blog**: Ollama with a compatible model (e.g., `llama3.2`)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-projects
```

### 2. Choose Your Project
Navigate to the project directory you want to use:

```bash
# For AI Workload Analyzer
cd ai_workload_analyzer

# For Local GPT
cd local_gpt

# For YouTube to Blog
cd yt_to_blog
```

### 3. Install Dependencies
```bash
uv sync
```

### 4. Configure Environment
Each project has its own setup requirements. Check the individual project README for specific configuration steps.

### 5. Run the Application
```bash
# For Chainlit-based projects (AI Workload Analyzer, Local GPT)
uv run chainlit run main.py

# For YouTube to Blog
uv run python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 📁 Project Structure

```
ai-projects/
├── ai_workload_analyzer/     # Databricks workload analysis tool
│   ├── main.py              # Chainlit app with Databricks integration
│   ├── pyproject.toml       # Dependencies and config
│   ├── README.md           # Detailed project documentation
│   └── env_example.txt     # Environment variables template
├── local_gpt/              # Local PDF Q&A system
│   ├── main.py             # Chainlit app with PDF processing
│   ├── pyproject.toml      # Dependencies and config
│   ├── README.md          # Detailed project documentation
│   └── chainlit.md        # Chainlit welcome screen
├── yt_to_blog/            # YouTube to blog converter
│   ├── main.py            # Main conversion script
│   ├── test_main.py       # Unit tests
│   ├── pyproject.toml     # Dependencies and config
│   └── README.md         # Detailed project documentation
└── README.md            # This file
```

## 🎯 Use Cases

### AI Workload Analyzer
- **Data Engineers**: Optimize SQL queries and data pipelines
- **Database Administrators**: Analyze workload performance and bottlenecks
- **Analytics Teams**: Get intelligent insights about data processing

### Local GPT
- **Researchers**: Analyze research papers and academic documents
- **Students**: Study from uploaded course materials and textbooks
- **Professionals**: Extract insights from business documents and reports

### YouTube to Blog
- **Content Creators**: Convert video content into written blog posts
- **Educators**: Create text-based resources from educational videos
- **Marketers**: Transform video content for multi-channel distribution

## 🔧 Development

### Setting Up Development Environment
```bash
# Clone the repository
git clone <repository-url>
cd ai-projects

# Set up each project
for project in ai_workload_analyzer local_gpt yt_to_blog; do
    cd $project
    uv sync
    cd ..
done
```

### Running Tests
```bash
# Navigate to project directory
cd yt_to_blog

# Run tests
uv run python -m unittest test_main.py -v
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

Each project has its own detailed README with:
- Comprehensive setup instructions
- API documentation
- Troubleshooting guides
- Advanced configuration options

## 🐛 Troubleshooting

### Common Issues

**Ollama Connection Errors**
- Ensure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`
- Verify model name in configuration

**Python Environment Issues**
- Use Python 3.11+ for all projects
- Prefer `uv` over `pip` for dependency management
- Check virtual environment activation

**Databricks Integration (AI Workload Analyzer)**
- Verify Databricks credentials and permissions
- Check Unity Catalog function accessibility
- Ensure model serving endpoint is available

## 🤝 Support

For issues and questions:
- Check the individual project README files
- Review the troubleshooting sections
- Create an issue in the project repository
- Join relevant community discussions

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: These projects are primarily created for learning AI development patterns and techniques. As they mature and become more production-ready, they may be moved to separate repositories.
