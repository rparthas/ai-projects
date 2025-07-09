# Local GPT with PDF Q&A

A powerful Chainlit application that provides PDF document analysis and Q&A capabilities using Ollama and ChromaDB.

## Features

### 📄 PDF Document Q&A
- Upload multiple PDF documents
- Semantic search through document content using ChromaDB vector database
- Intelligent chunking and embedding with sentence-transformers
- Context-aware responses based on document content

### 🔍 Smart Context Management
- Automatically searches PDF documents for relevant information
- Provides context-aware responses based on document content
- Falls back to general knowledge when no relevant documents are found

## Installation

1. **Install dependencies:**
```bash
cd local_gpt
uv sync
```

2. **Set up environment variables:**
Create a `.env` file (optional - uses defaults):
```env
# Optional configuration
```

3. **Start Ollama:**
```bash
ollama serve
ollama pull deepseek-r1:8b  # or your preferred model
```

## Usage

### Starting the Application
```bash
uv run chainlit run main.py -w
```

### Basic Operations

1. **Upload PDFs**: Use the attachment button to upload PDF documents
2. **Ask Questions**: Type any question - the system will search PDFs for relevant context
3. **Use Commands**: 
   - `/help` - Show available features and commands
   - `/debug` - Check database status and loaded documents

### Query Types

**PDF-focused queries:**
- "What does this document say about X?"
- "Summarize the main points from the uploaded paper"
- "Find information about Y in the documents"

**General queries:**
- "Explain concept Z"
- "How does X work?"
- "What are the benefits of Y?"

## Technical Architecture

### Components
- **Chainlit**: Web interface and chat management
- **ChromaDB**: Vector database for document storage and semantic search
- **sentence-transformers**: Text embedding for semantic similarity
- **PyPDF2**: PDF text extraction
- **Ollama**: Local LLM for response generation (DeepSeek-R1)

### Document Processing Pipeline
1. **PDF Upload**: Files uploaded through Chainlit interface
2. **Text Extraction**: PyPDF2 extracts text from PDF pages
3. **Text Chunking**: Documents split into overlapping chunks
4. **Embedding Generation**: sentence-transformers creates vector embeddings
5. **Vector Storage**: ChromaDB stores embeddings with metadata
6. **Semantic Search**: Query embeddings matched against document embeddings
7. **Context Assembly**: Relevant chunks combined for LLM context
8. **Response Generation**: Ollama generates contextual responses

## Configuration

### Customization Options
- **Distance threshold**: Adjust semantic search sensitivity (currently 0.8)
- **Chunk size**: Control document chunking size (default: 1000 characters)
- **Overlap**: Set chunk overlap for better context continuity (default: 200 characters)
- **Results limit**: Number of search results to consider (default: 5)

## Logging and Debugging

The application provides comprehensive logging:
- PDF processing steps (10-step detailed logging)
- Document chunking and embedding generation
- Search operations and results
- Context decision making
- Model response generation

Use `/debug` command to check:
- Number of documents in database
- Sample document content
- Database health status

## Troubleshooting

### Common Issues

**"Processing query without PDF context"**
- Check if PDFs were successfully uploaded and processed
- Use `/debug` to verify database content
- Ensure PDF files contain extractable text
- Try lowering the distance threshold if you expect matches

**"No content found" during PDF upload**
- Ensure PDF files are not corrupted
- Check that PDFs contain selectable text (not just images)
- Try uploading one PDF at a time to isolate issues

**Ollama connection errors**
- Verify Ollama is running: `ollama serve`
- Ensure model is downloaded: `ollama pull deepseek-r1:8b`
- Check if the model name matches in the code

**Poor search results**
- Try rephrasing your question
- Use more specific keywords from the document
- Check if the document content matches your query language

## Development

### Adding New Features
- Extend search functionality in `search_documents()`
- Modify chunking strategy in `chunk_text()`
- Add new commands following the existing pattern
- Customize the LLM prompt in `process_query()`

### Testing
- Test PDF upload and processing with various file types
- Verify semantic search accuracy with different queries
- Test edge cases (empty PDFs, large files, special characters)
- Validate context assembly and response quality

## Performance Tips

- **Chunk size**: Smaller chunks (500-800 chars) for precise answers, larger chunks (1000-1500 chars) for comprehensive context
- **Overlap**: Higher overlap (300-400 chars) for better context continuity
- **Distance threshold**: Lower values (0.6-0.7) for stricter matching, higher values (0.8-0.9) for broader results
- **Model selection**: Choose appropriate Ollama model based on speed vs quality needs

## License

This project is open source and available under the MIT License. 