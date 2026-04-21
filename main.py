from agent import runAgent
from rich import print

messages = []

try: 
    while True:
        user_input = input("[bold blue]You: [/bold blue]")
        messages.append({"role": "user", "content": user_input})

        response = runAgent(messages)
        print(f"[bold green]Agent: [/bold green]{response}")

        messages.append({"role": "assistant", "content": response})

except KeyboardInterrupt:
    print("\n[bold red]Saliendo del REPL...[/bold red]")