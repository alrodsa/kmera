from pathlib import Path
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

import cv2
import numpy as np

from src.data.file import File
from src.data.folder import Folder
from src.core.processor import Processor

class TestProcessor(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.input_dir = str(Path(self.tmpdir) / "test_input")
        self.output_dir = str(Path(self.tmpdir) / "test_output")
        self.mode = "copy"
        self.file_path = Path(self.input_dir) / "subfolder_1" / "test_file1.jpg"

        Path(self.input_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        (Path(self.input_dir) / "subfolder_1").mkdir(parents=True, exist_ok=True)
        self.file_path.touch(exist_ok=True)

        self.file = File(
            name=self.file_path.name,
            directory=self.file_path,
            size=0,
        )

        (Path(self.output_dir) / "subfolder_1").mkdir(parents=True, exist_ok=True)
        self.file_copy_path = Path(self.output_dir) / "subfolder_1" / self.file_path.name

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def fake_copy(self, dst_file):
            Path(dst_file).touch()

    def fake_replace(self, dst_file):
            Path(dst_file).with_name("replaced_" + Path(dst_file).name).touch()
            shutil.rmtree(Path(dst_file))

    @patch.object(Processor, "add_metadata_inside_image")
    @patch("src.core.processor.shutil.move")
    def test_copy_naming_metadata_with_in_image_true(self, mock_move, mock_add_metadata):
        mock_add_metadata.side_effect = None
        mock_move.side_effect = self.fake_copy(
            str(self.file_copy_path)
        )
        Processor.copy_naming_metadata(
            Folder(directory=self.input_dir),
            Path(self.input_dir),
            Path(self.output_dir),
            True
        )
        self.assertTrue(self.file_copy_path.exists())
        self.assertTrue(self.file_copy_path.is_file())
        self.assertTrue(mock_add_metadata.called)
        self.assertEqual(mock_add_metadata.call_count, 1)

    @patch("src.core.processor.shutil.copy2")
    def test_copy_naming_metadata_with_in_image_false(self, mock_copy):
        mock_copy.side_effect = self.fake_copy(
            str(self.file_copy_path)
        )
        Processor.copy_naming_metadata(
            Folder(directory=self.input_dir),
            Path(self.input_dir),
            Path(self.output_dir),
            False
        )
        self.assertTrue(self.file_copy_path.exists())
        self.assertTrue(self.file_copy_path.is_file())

    @patch.object(Processor, "add_metadata_inside_image")
    @patch.object(File, "__str__", return_value="replaced_test_file1.jpg")
    def test_replace_naming_metadata_with_in_image_true(self, mock_str, mock_add_metadata):
        Processor.replace_naming_metadata(
            Folder(directory=self.input_dir),
            True
        )
        self.assertFalse(self.file_copy_path.exists())
        self.assertFalse(self.file_copy_path.is_file())
        self.assertTrue(mock_add_metadata.called)

        replaced_file_path = Path(self.input_dir) / "subfolder_1" / "replaced_test_file1.jpg"
        self.assertTrue(replaced_file_path.exists())
        self.assertTrue(replaced_file_path.is_file())

    def test_add_metadata_inside_image_correct_image(
        self
    ):
        array = np.full((100, 100, 3), 255, dtype=np.uint8)
        cv2.imwrite(str(self.file_path), array)

        self.assertTrue(self.file_path.exists())
        self.assertTrue(self.file_path.is_file())

        image_file = File(
            name=str(self.file_path.name),
            directory=str(self.file_path),
            size=0,
        )

        Processor.add_metadata_inside_image(image_file, str(self.file_copy_path))

        self.assertTrue(self.file_copy_path.exists())
        self.assertTrue(self.file_copy_path.is_file())
        self.assertTrue(self.file_copy_path.stat().st_size > 0)

    def test_add_metadata_inside_image_non_image_file(self):
        non_image_file = File(
            name="test_file.txt",
            directory=str(Path(self.input_dir) / "test_file.txt"),
            size=0,
        )
        Path(non_image_file.directory).touch()

        Processor.add_metadata_inside_image(non_image_file, str(self.file_copy_path))
        self.assertFalse(self.file_copy_path.exists())
        self.assertFalse(self.file_copy_path.is_file())
