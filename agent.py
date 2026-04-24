import json
import inspect
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

def buildSystemPrompt():
    signature = inspect.signature(readFileTool)
    doc = readFileTool.__doc__

    return f"""
    You are a coding assistant whose goal is to help solve coding tasks.

    You have access to the following tools:

    TOOL: readFileTool
    Description:
    {doc}

    Signature: {signature}

    When you want to use a tool, respond EXACTLY with:
    tool: NAME({{"arg": "value"}})

    After that, you will receive a message with tool_result(...).
    If you do not need a tool, respond normally.
    """

def readFileTool (filename: str) -> dict:
    """
    Lee el contenido completo de un archivo.
    :param filename: ruta al archivo (absoluta o relativa al cwd).
    :return: dict con 'filePath' y 'content'.
    """


    try:
        with open(filename, "r") as f:
            content = f.read()
        return {
            "filePath": filename,
            "content": content
    }
    except Exception as e:
        return {
            "error": str(e)
        }

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
    
    results = []

    for name, args in toolCalls:
        if name == "readFileTool":
            result = readFileTool(**args)
            
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



