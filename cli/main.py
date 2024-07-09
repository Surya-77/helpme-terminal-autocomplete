import click
from generativeai.generate import generate, init_setup, list_available_models


@click.command()
@click.help_option("-h", "--help", help="Show this message and exit")
@click.option(
    "-l", "--list-models", is_flag=True, help="List available models", default=False
)
@click.argument("action", type=str, required=False, nargs=-1)
def run_process(list_models: bool, action: str) -> None:
    """Run the generative AI process"""

    init_setup()

    if list_models:
        click.echo(list_available_models())
    else:
        if action:
            action = " ".join(action)    
            click.echo(generate(input_text=action))


if __name__ == "__main__":
    run_process()
