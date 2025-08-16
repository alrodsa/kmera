from pathlib import Path
from src.core.namer import Namer
from src.data.folder import Folder
from src.common.enums import NamingMode


def check_naming_args(mode: NamingMode, input_dir: str) -> None:
    """
    Check the arguments for the naming function.
    """
    if mode not in NamingMode.choices():
        raise ValueError(f"Invalid naming mode: {mode}. Available modes: {NamingMode.choices()}")
    if not Path(input_dir).exists():
        raise ValueError(f"Input directory does not exist: {input_dir}")
    if not Path(input_dir).is_dir():
        raise ValueError(f"Input path is not a directory: {input_dir}")

def naming(
    input_dir: str,
    mode: NamingMode = NamingMode.COPY,
    in_image: bool = False,
    output_dir: str = "./naming/"
) -> None:
    check_naming_args(mode, input_dir)

    Namer(mode=NamingMode(mode), in_image=in_image).run(
        folder=Folder(input_dir), output_dir=output_dir
    )
