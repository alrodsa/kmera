import fire

from src.cli.naming import naming

def main() -> None:
    """
    CLI entrypoint.
    """
    fire.Fire({
        "naming": naming
    })
