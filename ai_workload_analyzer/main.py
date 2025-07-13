import os
import asyncio
from typing import Dict, Any, Optional
import chainlit as cl
from databricks.agents import ChatAgent
from databricks_langchain import ChatDatabricks, UCFunctionToolkit
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent variable
agent: Optional[ChatAgent] = None

def initialize_agent() -> ChatAgent:
    """Initialize the Databricks ChatAgent with tools."""
    try:
        # Point at your model serving endpoint
        llm = ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")
        
        # Grab whatever tools you need from the UC Function Registry
        # Replace "***" with actual function names from your UC Function Registry
        tools = UCFunctionToolkit(["***"]).tools
        
        # Instantiate the agent which will call the tools for the SQL query
        agent = ChatAgent(
            llm=llm,
            tools=tools,
            system_message="Execute all the necessary tools for each of the tables in the SQL query",
            streaming=True,
            confirm_tool_calls=True
        )
        
        logger.info("Databricks ChatAgent initialized successfully")
        return agent
    except Exception as e:
        logger.error(f"Failed to initialize agent: {str(e)}")
        raise

@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    global agent
    
    # Display welcome message
    await cl.Message(
        content="🤖 **AI Workload Analyzer** powered by Databricks\n\n"
                "I can help you analyze workloads, execute SQL queries, and provide insights using Databricks tools.\n\n"
                "**Available commands:**\n"
                "- Ask me to analyze any SQL query or workload\n"
                "- Request data insights and recommendations\n"
                "- Get help with Databricks-related tasks\n\n"
                "What would you like to analyze today?"
    ).send()
    
    # Initialize the agent
    try:
        agent = initialize_agent()
        await cl.Message(
            content="✅ Agent initialized successfully! Ready to process your queries.",
            author="System"
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"❌ Failed to initialize agent: {str(e)}\n\n"
                   "Please check your Databricks configuration and try again.",
            author="System"
        ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    global agent
    
    if agent is None:
        await cl.Message(
            content="❌ Agent not initialized. Please restart the chat session.",
            author="System"
        ).send()
        return
    
    # Show thinking indicator
    async with cl.Step(name="Processing", type="run") as step:
        step.output = "Analyzing your query with Databricks agent..."
        
        try:
            # Process the message with the agent
            response = await process_with_agent(message.content)
            
            # Send the response
            await cl.Message(
                content=response,
                author="AI Workload Analyzer"
            ).send()
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await cl.Message(
                content=f"❌ An error occurred while processing your request: {str(e)}\n\n"
                       "Please try again or contact support if the issue persists.",
                author="System"
            ).send()

async def process_with_agent(user_input: str) -> str:
    """Process user input with the Databricks agent."""
    try:
        # Since the agent might not have async methods, we'll run it in a thread
        import concurrent.futures
        
        def run_agent():
            # This is a simplified example - adjust based on actual agent API
            # You might need to use agent.chat() or similar method
            return f"Agent response for: {user_input}"
        
        # Run the agent in a thread pool to avoid blocking
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_agent)
            response = future.result(timeout=30)  # 30 second timeout
        
        return response
    
    except concurrent.futures.TimeoutError:
        return "⏱️ Request timed out. Please try again with a simpler query."
    except Exception as e:
        logger.error(f"Agent processing error: {str(e)}")
        return f"❌ Error processing request: {str(e)}"

@cl.on_stop
async def stop():
    """Clean up when chat stops."""
    logger.info("Chat session ended")

if __name__ == "__main__":
    # Run the Chainlit app
    cl.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )