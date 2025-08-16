from pathlib import Path
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

from src.metadata.photo import PhotoMetadata
from src.data.file import File


class TestFile(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.input_dir = str(Path(self.tmpdir) / "test_input")
        self.input_file_dir = str(Path(self.input_dir) / "test_file.jpg")

        Path(self.input_dir).mkdir(parents=True, exist_ok=True)
        Path(self.input_file_dir).touch()


    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_file_creation_success(self):
        file = File(
            name=str(Path(self.input_file_dir).name),
            size=Path(self.input_file_dir).stat().st_size,
            directory=str(Path(self.input_file_dir))
        )
        self.assertTrue(Path(file.directory).exists())
        self.assertEqual(file.name, Path(self.input_file_dir).name)
        self.assertEqual(file.size, Path(self.input_file_dir).stat().st_size)

    @patch.object(PhotoMetadata, "__str__", return_value="metadata")
    def test_file_str(self, _):
        file = File(
            name=str(Path(self.input_file_dir).name),
            size=Path(self.input_file_dir).stat().st_size,
            directory=str(Path(self.input_file_dir))
        )
        self.assertEqual(str(file), f"{Path(file.name).stem}_metadata{file.extension}")

    @patch("src.data.file.piexif.dump", return_value=b"exif_bytes")
    @patch("src.data.file.piexif.load", return_value={})
    def test_file_exif_metadata(self, mock_load, mock_dump):
        file = File(
            name=str(Path(self.input_file_dir).name),
            size=Path(self.input_file_dir).stat().st_size,
            directory=str(Path(self.input_file_dir))
        )
        metadata = file.photo_metadata
        self.assertIsInstance(metadata, PhotoMetadata)
        self.assertEqual(metadata.camera_model, "")
        self.assertEqual(metadata.exposure_time, "")
        self.assertEqual(metadata.aperture, "f")
        self.assertEqual(metadata.iso, "")
        self.assertEqual(metadata.focal_length, "")
        self.assertEqual(metadata.date_taken, "")
        self.assertEqual(metadata.location, "")
        self.assertEqual(metadata.description, "")
        self.assertEqual(metadata.exposure_bias, "")
        self.assertEqual(file.exif_bytes, b"exif_bytes")
        mock_load.assert_called_once_with(file.directory)
        mock_dump.assert_called_once_with({})
