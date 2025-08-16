from dataclasses import dataclass
from pathlib import Path
from src.core.processor import Processor
from src.data.folder import Folder
from src.common.enums import NamingMode


@dataclass
class Namer:
    mode: NamingMode
    in_image: bool

    def run(self, folder: Folder, output_dir: str) -> "Namer":
        if self.mode == NamingMode.COPY:
            Processor.copy_naming_metadata(
                folder, Path(folder.directory), Path(output_dir), in_image=self.in_image
            )
            print(f"📂 Copied files from {folder.directory} ➝ {output_dir}...")
        elif self.mode == NamingMode.REPLACE:
            Processor.replace_naming_metadata(folder, in_image=self.in_image)
            print(f"✍️ Replaced files in {folder.directory} with photo metadata info.")
        else:
            raise ValueError(f"Unsupported naming mode: {self.mode}")
    
        return self
