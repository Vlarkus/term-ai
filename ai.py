import sys
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.markdown import Markdown
from rich import box
from rich.spinner import Spinner
from rich.live import Live
from ollama import chat, list as ollama_list

EXIT_COMMANDS = ["q", "quit", "exit", "bye", "leave"]

models = ollama_list()["models"]
model_names = [m["model"] for m in models]
model = None

user_input_prompt = Text.from_markup("[bold][blue]>>>[/blue][/bold] ", style="white")

def exit_program():
    print("\n[bold yellow]Goodbye![/bold yellow]\n")
    sys.exit()

def is_exit_command(user_input: str) -> bool:
    return user_input.strip().lower() in EXIT_COMMANDS

def print_welcome_message():
    print()
    # Get available models from Ollama

    # Build the welcome message with model list and exit commands
    exit_cmds_str = ", ".join(f"[cyan]'[/cyan][yellow]{cmd}[/yellow][cyan]'[/cyan]" for cmd in EXIT_COMMANDS)
    welcome_message = "[bold white]Welcome to your personal Terminal AI chat![/bold white]\n"
    welcome_message += f"[bold white]Type {exit_cmds_str} to leave at any time.[/bold white]\n\n"
    welcome_message += "[bold blue]Available models:\n[/bold blue]"
    for idx, name in enumerate(model_names, 1):
        welcome_message += f"\n\t[bold yellow]{idx}.[/bold yellow] [bold white]{name}[/bold white]"
    welcome_message += "\n\n[bold white]Use 'ollama pull \[model name]' to download more models.[/bold white]"

    welcome_panel = Panel(
        Align.left(welcome_message),
        border_style="green",
        title="[bold white]Terminal AI Menu[/bold white]",
        box=box.ROUNDED,
        expand=True,
        padding=(1, 2),
    )
    print(welcome_panel)
    print()

def get_user_input():
    print(user_input_prompt, end="")  # Rich prints the styled prompt
    return input()  # input() reads the user's input
    
    
    
def prompt_model():
    # Prompt user to select a model
    while True:
        model_input = get_user_input().strip()
        if is_exit_command(model_input):
            exit_program()
            return
        if model_input in model_names:
            model = model_input
            break
        else:
            print(f"\n[bold red]Model '{model_input}' not found. Please enter a valid model name.[/bold red]\n")
    
    
        
def main():

    # Print welcome message
    print_welcome_message()

    prompt_model()

    # Chat loop
    while True:
        user_input = get_user_input()
        if is_exit_command(user_input):
            exit_program()
            break

        # Show spinner while waiting for AI response
        spinner = Spinner("dots", text="[bold white]Thinking...[/bold white]", style="green")
        with Live(spinner, refresh_per_second=10, transient=True):
            response = chat(
                model=model,
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

        ai_markdown = Markdown(response['message']['content'])
        panel = Panel(
            Align.left(ai_markdown),
            title=model,
            border_style="cyan",
            box=box.ROUNDED,
            expand=True,
            padding=(1, 2),
        )
        print(panel)

if __name__ == "__main__":
    main()
