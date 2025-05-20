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
    
    welcome_panel = Panel(
        Align.center("[bold white]Welcome to your personal Terminal AI chat! Type 'q', 'quit', or 'exit' to leave.[/bold white]"),
        border_style="cyan",
        title="Terminal AI Chat",
        box=box.ROUNDED,
        expand=True,
        padding=(1, 2),
    )
    print()
    print(welcome_panel)
    
    while True:
        user_input = input("\n>>> ")
        print()
        if user_input.strip().lower() in {"q", "quit", "exit"}:
            print("[bold cyan]Goodbye![/bold cyan]\n")
            break

        # Show spinner while waiting for AI response
        spinner = Spinner("dots", text="[bold white]Thinking...[/bold white]", style="green")
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
        print()
        print(panel)

if __name__ == "__main__":
    main()
