
import chainlit as cl
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings
import os

load_dotenv()

# Configure the settings
Settings.llm = Ollama(model=os.getenv("OLLAMA_MODEL", "llama2"), request_timeout=300)
Settings.embed_model = OllamaEmbedding(model_name=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"), request_timeout=120.0)

@cl.on_chat_start
async def on_chat_start():
    """Initializes the chat session, asks for files, and builds the query engine."""
    # Ask the user to upload files
    response = None
    while response is None:
        response = await cl.AskFileMessage(
            content="Hello! I'm your journal assistant. Please upload one or more text files to begin.",
            accept=[".md", ".txt"],
            max_size_mb=100,
            max_files=20,
        ).send()

    # The response is a list of file objects.
    files = response

    # Process the uploaded files
    processing_msg = cl.Message(content="Processing your journal entries...")
    await processing_msg.send()

    documents = []
    for file in files:
        content = open(file.path).read()
        documents.append(Document(text=content, doc_id=file.name))

    # Create the index and query engine
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    # Store the query engine in the user session
    cl.user_session.set("query_engine", query_engine)

    await processing_msg.remove()
    await cl.Message(
        content=f"I have processed {len(files)} file(s). You can now ask me questions about them!"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handles incoming messages."""
    query_engine = cl.user_session.get("query_engine")

    if query_engine is None:
        await cl.Message(content="Please restart the chat and upload your journal files.").send()
        return

    # Query the engine
    response = await cl.make_async(query_engine.query)(message.content)

    # Send the response
    await cl.Message(content=str(response)).send()
