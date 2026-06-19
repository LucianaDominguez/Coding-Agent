# python -m venv venv o py -m venv venv 
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
# venv\Scripts\activate
# pip install -r requirements.txt
# para arrancar back: python -m uvicorn backend.main:app --reload

# para front abrir otra terminal
# cd frontend
# npm install
#npm run dev

# EJECUTAR CON: python main.py , teniendo (venv)

from agent import runAgent, buildSystemPrompt
from rich import print


messages = [
    {"role": "system", "content": buildSystemPrompt()}
]

try: 
    while True:
        print("[bold blue]You:[/bold blue]", end=" ") # sólo para que aparezca en color, desde input no es posible.
        userInput = input()
        messages.append({"role": "user", "content": userInput})

        response = runAgent(messages)
        print(f"[bold green]Agent: [/bold green]{response}")

        messages.append({"role": "assistant", "content": response})

except KeyboardInterrupt:
    print("\n[bold red]Closing...[/bold red]")

