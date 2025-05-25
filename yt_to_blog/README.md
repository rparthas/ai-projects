# YouTube Transcript to Blog Post Converter

A Python script that takes a YouTube video URL, extracts its transcript, and uses a local Ollama model to convert the transcript into a well-structured blog post.

## Description

This tool automates the process of converting YouTube video content into engaging blog posts. It extracts video transcripts using the YouTube Transcript API and leverages local Ollama language models to transform the raw transcript into professional, readable blog content with proper structure, headings, and formatting.

## Prerequisites

- **Python 3.8+**
- **Ollama installed and running** - Download from [ollama.com](https://ollama.com)
- **A model pulled via Ollama** (e.g., `ollama pull llama3.2`)

## Setup Instructions

1. **Clone the repository** (or download the files):
   ```bash
   git clone <repository-url>
   cd yt_to_blog
   ```

2. **Navigate to the project directory**:
   ```bash
   cd yt_to_blog
   ```

3. **Create and activate a Python virtual environment**:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using traditional venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** in the root directory and add your desired Ollama model name:
   ```env
   OLLAMA_MODEL_NAME="llama3.2"
   ```
   
   **Important**: Ensure this model is pulled in your Ollama setup:
   - Check available models: `ollama list`
   - Pull a model: `ollama pull llama3.2`

## Usage

```bash
# Using uv (recommended)
uv run python main.py <youtube_video_url>

# Or using traditional python
python main.py <youtube_video_url>
```

### Example:

```bash
uv run python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Supported YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`

## Output

The generated blog post will be saved to a file named `<title>.md` where `<title>` is automatically extracted from the generated blog post title.

For example, if the generated blog post has the title "How to Build Amazing Applications", the output file will be `How_to_Build_Amazing_Applications.md`.

**Filename Features:**
- Automatically extracts title from the generated blog post
- Sanitizes invalid filename characters
- Converts spaces to underscores for better compatibility
- Falls back to "blog_post.md" if no title can be extracted
- Limits filename length to 100 characters

## Features

- **Multiple URL format support**: Works with various YouTube URL formats
- **Automatic transcript extraction**: Uses YouTube's official transcript API
- **AI-powered content transformation**: Leverages local Ollama models for blog generation
- **Professional formatting**: Generates well-structured blog posts with titles and headings
- **Smart filename generation**: Uses blog post title for meaningful filenames
- **Error handling**: Comprehensive error handling for common issues
- **File output**: Saves generated content to markdown files
- **Environment configuration**: Easy model configuration via `.env` file

## Troubleshooting

### Common Issues:

1. **"OLLAMA_MODEL_NAME not set"**:
   - Ensure you have created a `.env` file with `OLLAMA_MODEL_NAME="your_model_name"`

2. **"model not found"**:
   - Pull the model: `ollama pull llama3.2`
   - Check available models: `ollama list`

3. **"No transcript found"**:
   - The video may not have transcripts available
   - Try a different video with captions/transcripts

4. **Connection errors**:
   - Ensure Ollama is running: `ollama serve`
   - Check if the service is accessible

## Development

### Running Tests

```bash
# Using uv
uv run python -m unittest test_main.py -v

# Or using traditional python
python -m unittest test_main.py -v
```

### Project Structure

```
yt_to_blog/
├── main.py              # Main script
├── test_main.py         # Unit tests
├── pyproject.toml       # Project configuration (uv)
├── uv.lock             # Dependency lock file
├── .env                # Environment variables
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## License

This project is open source and available under the MIT License. 