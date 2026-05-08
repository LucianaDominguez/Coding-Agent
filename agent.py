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
    "listFiles" : listFiles,
    "editFile" : editFile
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
You are a coding agent specialized in helping users interact with a local codebase and filesystem.

You have access to the following tools:

{toolsDescription}

GENERAL BEHAVIOR:

- Be concise, precise, and action-oriented.
- Prefer using tools over assumptions.
- Never invent filesystem contents.
- Never pretend a file was created, modified, or read if no tool was used.
- Use tools whenever filesystem information is required.

FILESYSTEM RULES:

- To read file contents → use readFile
- To inspect directories → use listFiles
- To create files → use editFile
- To modify existing files → use editFile

TOOL USAGE RULES:

- You may call multiple tools sequentially if needed.
- Before editing a file, read it first when context is necessary.
- Preserve existing code unless the user explicitly asks to replace it.
- Make minimal, targeted edits whenever possible.
- If a tool fails, analyze the error and recover intelligently when possible.

IMPORTANT:

- Do NOT output fake tool syntax.
- Do NOT describe tool calls in plain text.
- Use the provided function calling interface directly.
- Respond normally only after completing the necessary tool actions.

Your goal is to behave like a real autonomous coding assistant.
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
        messages.append(message)
       
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
            else:
                result = {"error": f"Unknown tool: {name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result)
            })
    

    return "Se alcanzó el máximo de pasos sin una respuesta definitiva."


