# Description: This file is the entry point for the CLI application. It uses the Click library to parse the command line arguments and run the generative AI process.
import os
import click
from generativeai.generate import TerminalHelper
from dotenv import load_dotenv


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option("-l", "--list-models", is_flag=True, help="List available models", default=False)
@click.argument("action", type=str, required=False, nargs=-1)
def run_process(list_models: bool, action: tuple) -> None:
    """Run the generative AI process"""

    load_dotenv()
    terminal_helper = TerminalHelper(
        api_provider=os.getenv("API_PROVIDER"),
        api_key=os.getenv("GOOGLE_API_KEY"),
        model_name=os.getenv("MODEL_NAME"),
    )
    terminal_helper.init_setup()

    if list_models:
        terminal_helper.list_available_models()
    else:
        if action:
            action = " ".join(action)
            click.echo(terminal_helper.generate(input_text=action))


if __name__ == "__main__":
    run_process()
