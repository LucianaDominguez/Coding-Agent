import json
import inspect
from openai import OpenAI
from dotenv import load_dotenv

from tools import readFile, listFiles

TOOL_REGISTRY = {
    "readFile": readFile,
    "ListFiles" : listFiles,
   # "EditFiles" : editFile
}


load_dotenv()
client = OpenAI()

def buildSystemPrompt():
    toolsDescription = ""

    for name, func in TOOL_REGISTRY.items():
        signature = inspect.signature(func)
        doc = func.__doc__

        toolsDescription += f"""

        TOOL: {name}
        Description:
        {doc}

        Signature: {signature}
        """

    return f"""
    You are a coding agent.

    You have access to the following tools:

    {toolsDescription}

    When you want to use a tool, respond EXACTLY with:
    tool: NAME({{"arg": "value"}})

    After that, you will receive a message with tool_result(...).
    If you do not need a tool, respond normally.
    """


def extractToolInvocations(text: str):
    results = []

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line.startswith("tool:"):
            try:
                toolCall = line.replace("tool:", "").strip()

                name, args = toolCall.split("(", 1)
                args = args[:-1]  # saca ")"

                argsDict = json.loads(args)

                results.append((name, argsDict))

            except Exception as e:
                print(f"Error parsing tool: {e}")

    return results



def runAgent(messages):
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )

    text = response.choices[0].message.content
    toolCalls = extractToolInvocations(text)

    if not toolCalls:
        return text
    
    # results = []

    for name, args in toolCalls:
        if name in TOOL_REGISTRY:
            result = TOOL_REGISTRY[name](**args)
            
            messages.append({
                "role": "assistant",
                "content": f"toolResult({result})"
            })
    
    secondResponse = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )

    finalText = secondResponse.choices[0].message.content
    
    return finalText



