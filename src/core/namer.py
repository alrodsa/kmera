from dataclasses import dataclass
from pathlib import Path
import shutil

from src.data.folder import Folder
from src.common.enums import NamingMode


@dataclass
class Namer:
    mode: NamingMode
    in_image: bool

    def _copy_folder(
        self, folder: Folder, source_root: Path, output_root: Path
    ) -> None:

        relative_path = Path(folder.directory).relative_to(source_root)
        dest_dir = output_root / relative_path
        dest_dir.mkdir(parents=True, exist_ok=True)

        for file in folder.files:
            src_file = Path(file.directory)
            dst_file = dest_dir / file.name
            shutil.copy2(src_file, dst_file)

        for subfolder in folder.folders:
            self._copy_folder(subfolder, source_root, output_root)

    def run(self, folder: Folder, output_dir: str) -> "Namer":
        print ("Running namer")
        print(self.mode == NamingMode.COPY)
        if self.mode == NamingMode.COPY:
            print(f"Copying files from {folder.directory} to {output_dir}")
            self._copy_folder(folder, Path(folder.directory), Path(output_dir))




