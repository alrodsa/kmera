from pathlib import Path
from src.core.namer import Namer
from src.data.folder import Folder
from src.common.enums import NamingMode


def check_naming_args(mode: NamingMode, input_dir: str) -> None:
    """
    Check the arguments for the naming function.

    Parameters
    ----------
    mode : NamingMode
        The naming mode to be used (COPY or REPLACE).
    input_dir : str
        The input directory to process.
    """
    if mode not in NamingMode.choices():
        raise ValueError(f"Invalid naming mode: {mode}. Available modes: {NamingMode.choices()}")
    if not Path(input_dir).exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not Path(input_dir).is_dir():
        raise ValueError(f"Input path is not a directory: {input_dir}")

def show_execution_info(input_dir: str, mode: NamingMode, in_image: bool, output_dir: str) -> None:
    """
    Display the execution information for the naming process.

    Parameters
    ----------
    input_dir : str
        The input directory to process.
    mode : NamingMode
        The naming mode to be used (COPY or REPLACE).
    in_image : bool
        If True, metadata will be added inside the image files.
    output_dir : str
        The output directory where files will be copied or replaced.
    """
    print(
        f"🚀 Running naming with:\n"
        f"\t📂 Input Directory: {input_dir}\n"
        f"\t⚙️ Mode: {mode}\n"
        f"\t🖼️ In Image: {in_image}\n", end=""
    )
    if NamingMode(mode) == NamingMode.COPY:
        print(f"\t➡️ Output Directory: {output_dir}")

def naming(
    input_dir: str,
    mode: NamingMode = NamingMode.COPY,
    in_image: bool = False,
    output_dir: str = "./naming/"
) -> None:
    """
    Main function to handle the naming process.

    Parameters
    ----------
    input_dir : str
        The input directory containing files to be processed.
    mode : NamingMode, optional
        The naming mode to be used (COPY or REPLACE). Default is COPY.
    in_image : bool, optional
        If True, metadata will be added inside the image files. Default is False.
    output_dir : str, optional
        The output directory where files will be copied or replaced. Default is "./naming/".
    """
    check_naming_args(mode, input_dir)
    show_execution_info(input_dir, mode, in_image, output_dir)

    Namer(mode=NamingMode(mode), in_image=in_image).run(
        folder=Folder(input_dir), output_dir=output_dir
    )

    print("✅ Naming completed successfully!")
