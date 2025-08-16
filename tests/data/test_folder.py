from pathlib import Path
import shutil
import tempfile
from unittest import TestCase
from src.data.file import File
from src.data.folder import Folder

class TestFolder(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.input_dir = str(Path(self.tmpdir) / "test_input")

        Path(self.input_dir).mkdir(parents=True, exist_ok=True)

        # Create subfolders and files for testing with the following structure:
        # test_input/
        # ├── subfolder_0
        # │   ├── file_0.jpg
        # │   └── file_1.jpg
        # ├── subfolder_1
        # │   ├── file_0.jpg
        # │   └── file_1.jpg
        # └── subfolder_2
        #     ├── file_0.jpg
        #     └── file_1.jpg
        for i in range(3):
            Path(self.input_dir, f"subfolder_{i}").mkdir(parents=True, exist_ok=True)
            for j in range(2):
                Path(self.input_dir, f"subfolder_{i}", f"file_{j}.jpg").touch()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_files_recursive(self):
        folder = Folder(self.input_dir)
        files = folder.files_recursive

        # Check that we have 6 files in total (2 files in each of the 3 subfolders)
        self.assertEqual(len(files), 6)

        # Check that all files are of type File and have the correct properties
        for i, file in enumerate(files):
            self.assertIsInstance(file, File)
            self.assertTrue(file.name.startswith("file_"))
            self.assertTrue(file.name.endswith(".jpg"))
