from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

import os
import re
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
    - Creating files → use edit_file
    - Editing files → use edit_file
    - Reading files → use read_file
    - Listing directories → use list_files

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


def extractToolInvocations(text: str):
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



def runAgent(messages):
    MAX_STEPS = 5
    
    for step in range(MAX_STEPS):

        print(f"\n[STEP {step}]")

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages
        )

        text = response.choices[0].message.content

        # print("MODEL: ", text)
        messages.append({
            "role": "assistant",
            "content": text
        })

        toolCalls = extractToolInvocations(text)

        if not toolCalls:
            return text
    
   

        for name, args in toolCalls:

            print(f"[TOOL CALL] {name} {args}")

            if name in TOOL_REGISTRY:
                try:
                    result = TOOL_REGISTRY[name](**args)
                except Exception as e:
                    result = {"error": str(e)}
                
                messages.append({
                    "role": "assistant",
                    "content": f"tool_result: ({result})"
                })
    

    return "Se alcanzó el máximo de pasos sin una respuesta definitiva."



