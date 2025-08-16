from pathlib import Path
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.data.file import File
from src.core.namer import Namer
from src.common.enums import NamingMode
from src.data.folder import Folder

class TestNamer(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.input_dir = str(Path(self.tmpdir) / "test_input")
        self.output_dir = str(Path(self.tmpdir) / "test_output")
        self.in_image = False

        Path(self.input_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        self.folder = Folder(directory=self.input_dir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @patch("src.core.namer.Processor.copy_naming_metadata")
    def test_run_copy_mode(self, mock_copy_naming_metadata):
        namer = Namer(mode=NamingMode.COPY, in_image=self.in_image).run(
            folder=self.folder, output_dir=self.output_dir
        )
        mock_copy_naming_metadata.assert_called_once_with(
            self.folder, Path(self.input_dir), Path(self.output_dir), in_image=self.in_image
        )
        self.assertIsInstance(namer, Namer)

    @patch("src.core.namer.Processor.replace_naming_metadata")
    def test_run_replace_mode(self, mock_replace_naming_metadata):
        namer = Namer(mode=NamingMode.REPLACE, in_image=self.in_image).run(
            folder=self.folder, output_dir=self.output_dir
        )
        mock_replace_naming_metadata.assert_called_once_with(self.folder, in_image=self.in_image)
        self.assertIsInstance(namer, Namer)
        
    def test_run_invalid_mode(self):
        with self.assertRaises(ValueError):
            Namer(mode="invalid_mode", in_image=self.in_image).run(
                folder=self.folder, output_dir=self.output_dir
            )
