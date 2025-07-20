
# Journal RAG Application

This application uses Ollama and Chainlit to provide a RAG (Retrieval-Augmented Generation) interface for your journal entries. You can use it to perform weekly reviews, ask questions about your past entries, and gain insights from your journal.

## Setup

1.  **Create a virtual environment:**
    ```bash
    uv venv
    ```

2.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -e .
    ```

2.  **Set up your environment:**
    Create a `.env` file and add any necessary environment variables (e.g., for Ollama).

3.  **Add your journal entries:**
    Place your journal entries in the `data` directory.

4.  **Run the application:**
    ```bash
    chainlit run main.py
    ```
