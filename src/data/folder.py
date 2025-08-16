from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from src.constants.image import IMAGE_EXTENSIONS
from src.data.file import File

@dataclass
class Folder:
    directory: str
    folders: list[Folder] = field(default_factory=list)
    files: list[File] = field(default_factory=list)

    def __post_init__(self):
        for child in Path(self.directory).iterdir():
            if child.is_dir():
                self.folders.append(Folder(child))
                continue

            if child.suffix in IMAGE_EXTENSIONS:
                self.files.append(File(
                    name=child.name,
                    size=child.stat().st_size,
                    directory=str(child)
                ))


    @property
    def files_recursive(self) -> list[File]:
        """
        Returns a flat list of all files in the folder and its subfolders.
        """
        all_files = self.files.copy()
        for folder in self.folders:
            all_files.extend(folder.files_recursive)
        return all_files
