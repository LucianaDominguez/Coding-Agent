from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
def runAgent(messages):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )

    return response.choices[0].message.content
