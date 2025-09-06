from langchain_ollama import ChatOllama

# This assumes Ollama is running and has a model like 'llama3' pulled.
# You can change the model name to any other model you have available.
llm = ChatOllama(model="llama3.2:latest", temperature=0)
