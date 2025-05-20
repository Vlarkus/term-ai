from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.markdown import Markdown
from rich import box
from rich.spinner import Spinner
from rich.live import Live
from ollama import chat

def main():
    print("[bold cyan]Welcome to your AI chat! Type 'q', 'quit', or 'exit' to leave.[/bold cyan]\n")
    while True:
        user_input = input(">>> ")
        if user_input.strip().lower() in {"q", "quit", "exit"}:
            print("[bold red]Goodbye![/bold red]")
            break

        # Show spinner while waiting for AI response
        spinner = Spinner("dots", text="[bold green]Thinking...[/bold green]", style="green")
        with Live(spinner, refresh_per_second=10, transient=True):
            response = chat(
                model="mistral",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

        ai_markdown = Markdown(response['message']['content'])
        panel = Panel(
            Align.left(ai_markdown),
            title="Mistral",
            border_style="cyan",
            box=box.ROUNDED,
            expand=True,
            padding=(1, 2),
        )
        print(panel)

if __name__ == "__main__":
    main()
