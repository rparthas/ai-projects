import chainlit as cl
import ollama


@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "interaction",
        [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ],
    )

    msg = cl.Message(content="")

    start_message = "Hello, I'm your 100% local alternative to ChatGPT running on Llama3.2-Vision. How can I help you today?"

    for token in start_message:
        await msg.stream_token(token)

    await msg.send()


@cl.step(type="tool")
async def tool(input_message, image=None):

    interaction = cl.user_session.get("interaction")

    if image:
        interaction.append({"role": "user", "content": input_message, "images": image})
    else:
        interaction.append({"role": "user", "content": input_message})

    response = ollama.chat(model="llama3.2-vision", messages=interaction)

    interaction.append({"role": "assistant", "content": response.message.content})

    return response


@cl.on_message
async def main(message: cl.Message):

    images = [file for file in message.elements if "image" in file.mime]

    if images:
        tool_res = await tool(message.content, [i.path for i in images])

    else:
        tool_res = await tool(message.content)

    msg = cl.Message(content="")

    for token in tool_res.message.content:
        await msg.stream_token(token)

    await msg.send()
