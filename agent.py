import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are a coding assistant whose goal it is to help us solve coding tasks. 

You have access to the following tools:

TOOL: readFile
Description: Reads the full content of a file.
Signature: (filename: str) -> dict

When you want to use a tool, respond EXACTLY with:
tool: NAME({"arg": "value"})

After that, you will receive a message with tool_result(...).
If you do not need a tool, respond normally.
"""
def readFileTool (filename: str) -> dict:
    """
    Lee el contenido completo de un archivo.
    :param filename: ruta al archivo (absoluta o relativa al cwd).
    :return: dict con 'file_path' y 'content'.
    """
    try:
        with open(filename, "r") as f:
            content = f.read()
        return {
            "file_path": filename,
            "content": content
    }
    except Exception as e:
        return {
            "error": str(e)
        }

def extract_tool_invocations(text: str):
    results = []

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line.startswith("tool:"):
            try:
                tool_call = line.replace("tool:", "").strip()

                name, args = tool_call.split("(", 1)
                args = args[:-1]  # quitar ")"

                args_dict = json.loads(args)

                results.append((name, args_dict))

            except Exception as e:
                print(f"Error parsing tool: {e}")

    return results






def runAgent(messages):
    # tool_calls = extract_tool_invocations(text) CHECKEAR
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )

    return response.choices[0].message.content



