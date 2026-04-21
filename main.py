from agent import runAgent, SYSTEM_PROMPT
from rich import print


messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

try: 
    while True:
        print("[bold blue]You:[/bold blue]", end=" ") # sólo para que aparezca en color, desde input no es posible.
        user_input = input()
        messages.append({"role": "user", "content": user_input})

        response = runAgent(messages)
        print(f"[bold green]Agent: [/bold green]{response}")

        messages.append({"role": "assistant", "content": response})

except KeyboardInterrupt:
    print("\n[bold red]Saliendo del REPL...[/bold red]")