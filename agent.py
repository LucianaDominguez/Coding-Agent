from dotenv import load_dotenv
from openai import OpenAI

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
    MAX_STEPS = 5
    
    for step in range(MAX_STEPS):

        # print(f"\n[STEP {step}]")

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

            # print(f"[TOOL CALL] {name} {args}")

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



