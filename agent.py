from dotenv import load_dotenv
from openai import OpenAI
from tools_schema import TOOLS

load_dotenv()
client = OpenAI()

import os
import json
import inspect

from tools import readFile, listFiles, editFile

TOOL_REGISTRY = {
    "readFile": readFile,
    "ListFiles" : listFiles,
    "EditFiles" : editFile
}


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

    IMPORTANT RULES:

    - You MUST use tools for any action that involves the filesystem.
    - Creating files → use editFile
    - Editing files → use editFile
    - Reading files → use readFile
    - Listing directories → use listFiles

    - NEVER simulate file operations.
    - If a task requires a tool, you MUST call it.

    TOOL USAGE FORMAT:

    When you want to use a tool, respond EXACTLY with:
    tool: NAME({{"arg": "value"}})

    - Do NOT include explanations.
    - Do NOT include extra text.
    - ONLY return the tool call.

    After that, you will receive a message with tool_result(...).

    Only respond normally when no tool is needed.
    """


""" def extractToolInvocations(text: str):
    results = []

    pattern = r'tool:\s*(\w+)\((\{.*?\})\)'

    matches = re.findall(pattern, text, re.DOTALL)

    for name, argsStr in matches:
        try:
            argsDict = json.loads(argsStr)
            results.append((name, argsDict))
        except Exception as e:
            print(f"Error parsing tool: {e}")

    return results
"""


def runAgent(messages):
    MAX_STEPS = 5
    
    for step in range(MAX_STEPS):

        print(f"\n[STEP {step}]")

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages,
            tools=TOOLS
        )

        message = response.choices[0].message

        if message.content and not message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": message.content
            })
       
        toolCalls = message.tool_calls

        if not toolCalls:
            return message.content
    
   

        for call in toolCalls:
            name = call.function.name
            args = json.loads(call.function.arguments)

            print(f"[TOOL CALL] {name} {args}")

            if name in TOOL_REGISTRY:
                try:
                    result = TOOL_REGISTRY[name](**args)
                except Exception as e:
                    result = {"error": str(e)}
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result)
                })
    

    return "Se alcanzó el máximo de pasos sin una respuesta definitiva."


